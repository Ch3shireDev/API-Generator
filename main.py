import yaml
import os


class Property:
    def __init__(self, name, props):
        self.type = props[name]['type']
        self.name = name.capitalize()

    def __str__(self):
        return f'''public {self.type} {self.name} {{get;set;}}'''


class Element:

    parent = None

    def __init__(self, name, schemas):
        self.name = name
        scheme = schemas[name]
        self.properties = list(self.get_properties(scheme))
        if 'parent' in scheme:
            self.parent = scheme['parent']

    def get_properties(self, model):
        props = model['properties']
        for name in props:
            yield Property(name, props)

    def get_model(self):
        output = ''
        output += 'using System.Collections.Generic;'
        output += 'namespace ResourceAPI.Models\n{\n'
        output += f'''public class {self.name}{{\n'''
        for prop in self.properties:
            output += str(prop)+'\n'
        if self.parent:
            output += f'public {self.parent.name} Parent{self.parent.name} {{get;set;}}\n'
        output += '''}\n}\n'''
        return output

    def set_parent(self, elements):
        if self.parent == None:
            return
        for element in elements:
            if element.name == self.parent:
                self.parent = element

    def get_parents(self):
        tab = []
        if self.parent:
            tab += self.parent.get_parents()
        return tab + [self]

    def get_controller(self):
        route = self.get_main_route()
        output = "using System.Linq;using Microsoft.AspNetCore.Mvc;\nusing ResourceAPI.Models;\n"
        output += "namespace ResourceAPI.Controllers{\n"
        output += f"[Route(\"{self.get_main_route()}\")]\n"
        output += f"[ApiController]\npublic class {self.get_plural()}Controller : ControllerBase\n"
        output += f'{{public readonly AppDbContext Context;public {self.get_plural()}Controller(AppDbContext context){{Context = context;}}'
        output += self.get_GET_ALL()
        output += self.get_GET()
        output += self.get_POST()
        output += self.get_PUT()
        output += self.get_DELETE()
        output += "}\n}\n"
        return output

    def get_id(self):
        return self.name.lower() + 'Id'

    def get_plural(self):
        return self.name+'s'

    def get_name(self):
        return self.name

    def get_parents_strings(self):
        return",".join(
            [f'int {element.get_id()}' for element in self.get_parents()[:-1]])

    def get_parents_and_element(self):
        tab = [f'int {element.get_id()}' for element in self.get_parents()[
            :-1]] + [self.get_parents()[-1].get_name()+' element']
        return ','.join(tab)

    def get_all_strings(self):
        return",".join([f'int {element.get_id()}' for element in self.get_parents()])

    def get_GET_ALL(self):
        return f"[HttpGet]public ActionResult GetAll({self.get_parents_strings()}){{var elements = Context.{self.get_plural()}.ToList();return StatusCode(200, elements);}}\n"

    def get_GET(self):
        return f"[HttpGet][Route(\"{{{self.get_id()}}}\")]public ActionResult Get({self.get_all_strings()}){{var element=Context.{self.get_plural()}.First(x=>x.Id=={self.get_id()});return StatusCode(200,element);}}\n"

    def get_POST(self):
        return f"[HttpPost]public ActionResult Create({self.get_parents_and_element()}){{Context.{self.get_plural()}.Add(element);Context.SaveChanges();return StatusCode(204);}}\n"

    def get_PUT(self):
        return f"[HttpPut][Route(\"{{{self.get_id()}}}\")]public ActionResult Update({self.get_parents_and_element()}){{return StatusCode(503);}}\n"

    def get_DELETE(self):
        return f"[HttpDelete][Route(\"{{{self.get_id()}}}\")]public ActionResult Delete({self.get_all_strings()}){{var element = Context.{self.get_plural()}.First(x=>x.Id=={self.get_id()});Context.{self.get_plural()}.Remove(element);Context.SaveChanges();return StatusCode(204);}}\n"

    def get_main_route(self):
        if self.parent:
            return f"{self.parent.get_element_route()}/{self.name}s"
        else:
            return f"api/v1/{self.name}s"

    def get_element_route(self):
        return f"{self.get_main_route()}/{{{self.get_id()}}}"


def get_elements(schemas):
    elements = [Element(key, schemas) for key in schemas]
    for element in elements:
        element.set_parent(elements)
    return elements


def get_program_file():
    return '''
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Hosting;
namespace ResourceAPI{public class Program{
public static void Main(string[] args){CreateHostBuilder(args).Build().Run();}
public static IHostBuilder CreateHostBuilder(string[] args){
return Host.CreateDefaultBuilder(args).ConfigureWebHostDefaults(webBuilder => { webBuilder.UseStartup<Startup>(); });}}}
'''


def get_startup_file():
    return '''
using System;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Hosting;
namespace ResourceAPI{
public class Startup{public Startup(IConfiguration configuration){Configuration = configuration;}
public IConfiguration Configuration { get; set; }
public void ConfigureServices(IServiceCollection services){
services.AddEntityFrameworkSqlite().AddDbContext<AppDbContext>((sp, options) =>
{options.UseSqlite("Data Source=app.db").UseInternalServiceProvider(sp);});
services.AddDbContext<AppDbContext>();services.AddControllers();
services.AddCors(o =>o.AddDefaultPolicy(configure => configure.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));}
public void Configure(IApplicationBuilder app, IWebHostEnvironment env){
if (env.IsDevelopment()) app.UseDeveloperExceptionPage();app.UseRouting();
app.UseCors(options => options.AllowAnyHeader().AllowAnyMethod().AllowAnyOrigin());
app.UseEndpoints(endpoints => { endpoints.MapControllers(); });}}}'''


def get_project_file():
    return '''
<Project Sdk="Microsoft.NET.Sdk.Web">
  <PropertyGroup>
    <TargetFramework>netcoreapp3.1</TargetFramework>
  </PropertyGroup>
  <ItemGroup>
    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="3.1.3" />
  </ItemGroup>
</Project>
'''


def get_context_file(elements):
    output = '''
using Microsoft.EntityFrameworkCore;
using ResourceAPI.Models;
namespace ResourceAPI{
public class AppDbContext : DbContext{
public AppDbContext(DbContextOptions<AppDbContext> options) : base(options){}\n'''
    for element in elements:
        output += f'public DbSet<{element.name}> {element.name}s {{ get; set; }}\n'
    output += '''}}'''
    return output


txt = open('api.yaml').read()
data = yaml.load(txt, Loader=yaml.FullLoader)

schemas = data['components']['schemas']

elements = get_elements(schemas)

if not os.path.exists('ResourceAPI'):
    os.mkdir('ResourceAPI')

os.chdir('ResourceAPI')
open('Program.cs', 'w+').write(get_program_file())
open('Startup.cs', 'w+').write(get_startup_file())
open('Context.cs', 'w+').write(get_context_file(elements))


if not os.path.exists('Models'):
    os.mkdir('Models')
os.chdir('Models')
for element in elements:
    open(f"{element.name.capitalize()}.cs", 'w+').write(element.get_model())
os.chdir('..')

if not os.path.exists('Controllers'):
    os.mkdir('Controllers')
os.chdir('Controllers')
for element in elements:
    open(f"{element.name.capitalize()}sController.cs",
         'w+').write(element.get_controller())
os.chdir('..')

open('ResourceAPI.csproj', 'w+').write(get_project_file())
open('appsettings.development.json', 'w+').write(
    '''{"Logging":{"LogLevel":{"Default":"Information","Microsoft":"Warning","Microsoft.Hosting.Lifetime":"Information"}}}''')
open('appsettings.json', 'w+').write(
    '''{"Logging":{"LogLevel":{"Default":"Information","Microsoft":"Warning","Microsoft.Hosting.Lifetime":"Information"}},"AllowedHosts": "*"}''')

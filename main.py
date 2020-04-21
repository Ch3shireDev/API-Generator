import yaml


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

    def get_controller(self):
        route = self.get_main_route()
        output = "using Microsoft.AspNetCore.Mvc;\n"
        output += "namespace ResourceAPI.Controllers{\n"
        output += f"[Route(\"{self.get_main_route()}\")]\n"
        output += "[ApiController]\n"
        output += f"public class {self.name}sController : ControllerBase\n"
        output += "{"
        output += self.get_GET_ALL()
        output += self.get_GET()
        output += self.get_POST()
        output += self.get_PUT()
        output += self.get_DELETE()
        output += "}\n}\n"
        return output

    def get_GET_ALL(self):
        return "[HttpGet]public ActionResult GetAll(){return StatusCode(503);}\n"

    def get_GET(self):
        return f"[HttpGet][Route(\"{{ {self.name}Id }}\")]public ActionResult Get(){{return StatusCode(503);}}\n"

    def get_POST(self):
        return f"[HttpPost]public ActionResult Create(){{return StatusCode(503);}}\n"

    def get_PUT(self):
        return f"[HttpPut][Route(\"{{ {self.name}Id }}\")]public ActionResult Update(){{return StatusCode(503);}}\n"

    def get_DELETE(self):
        return f"[HttpDelete][Route(\"{{ {self.name}Id }}\")]public ActionResult Delete(){{return StatusCode(503);}}\n"

    def get_main_route(self):
        if self.parent:
            return f"{self.parent.get_element_route()}/{self.name}s"
        else:
            return f"api/v1/{self.name}s"

    def get_element_route(self):
        return f"{self.get_main_route()}/{{ {self.name}Id }}"


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
using Microsoft.Extensions.Hosting;
using ResourceAPI.Contexts;
namespace ResourceAPI{
public class Startup{public Startup(IConfiguration configuration){Configuration = configuration;}
public IConfiguration Configuration { get; set; }
public void ConfigureServices(IServiceCollection services){
services.AddDbContext<AppDbContext>();
services.AddControllers();
services.AddCors(o =>o.AddDefaultPolicy(configure => configure.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));}
public void Configure(IApplicationBuilder app, IWebHostEnvironment env){
if (env.IsDevelopment()) app.UseDeveloperExceptionPage();
app.UseRouting();
app.UseCors(options => options.AllowAnyHeader().AllowAnyMethod().AllowAnyOrigin());
app.UseEndpoints(endpoints => { endpoints.MapControllers(); });}}}'''


def get_project_file():
    return '''<Project Sdk="Microsoft.NET.Sdk.Web"><PropertyGroup><TargetFramework>netcoreapp3.1</TargetFramework></PropertyGroup></Project>'''


txt = open('api.yaml').read()
data = yaml.load(txt, Loader=yaml.FullLoader)

schemas = data['components']['schemas']

elements = get_elements(schemas)

open('Program.cs', 'w+').write(get_program_file())
open('Startup.cs', 'w+').write(get_startup_file())

for element in elements:
    open(f"{element.name.capitalize()}.cs", 'w+').write(element.get_model())
    open(f"{element.name.capitalize()}sController.cs",
         'w+').write(element.get_controller())

open('ResourceAPI.csproj', 'w+').write(get_project_file())
open('appsettings.development.json', 'w+').write('''{"Logging":{"LogLevel":{"Default":"Information","Microsoft":"Warning","Microsoft.Hosting.Lifetime":"Information"}}}''')
open('appsettings.json', 'w+').write('''{"Logging":{"LogLevel":{"Default":"Information","Microsoft":"Warning","Microsoft.Hosting.Lifetime":"Information"}},"AllowedHosts": "*"}''')

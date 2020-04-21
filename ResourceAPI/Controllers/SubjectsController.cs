using System.Linq;
using Microsoft.AspNetCore.Mvc;
using ResourceAPI.Models;

namespace ResourceAPI.Controllers
{
    [Route("api/v1/Subjects")]
    [ApiController]
    public class SubjectsController : ControllerBase
    {
        public readonly AppDbContext Context;

        public SubjectsController(AppDbContext context)
        {
            Context = context;
        }

        [HttpGet]
        public ActionResult GetAll()
        {
            var elements = Context.Subjects.ToList();
            return StatusCode(200, elements);
        }

        [HttpGet]
        [Route("{subjectId}")]
        public ActionResult Get(int subjectId)
        {
            var element = Context.Subjects.First(x => x.Id == subjectId);
            return StatusCode(200, element);
        }

        [HttpPost]
        public ActionResult Create(Subject element)
        {
            Context.Subjects.Add(element);
            Context.SaveChanges();
            return StatusCode(204);
        }

        [HttpPut]
        [Route("{subjectId}")]
        public ActionResult Update(Subject element)
        {
            return StatusCode(503);
        }

        [HttpDelete]
        [Route("{subjectId}")]
        public ActionResult Delete(int subjectId)
        {
            var element = Context.Subjects.First(x => x.Id == subjectId);
            Context.Subjects.Remove(element);
            Context.SaveChanges();
            return StatusCode(204);
        }
    }
}
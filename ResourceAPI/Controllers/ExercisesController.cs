using System.Linq;
using Microsoft.AspNetCore.Mvc;
using ResourceAPI.Models;

namespace ResourceAPI.Controllers
{
    [Route("api/v1/Subjects/{subjectId}/Exercises")]
    [ApiController]
    public class ExercisesController : ControllerBase
    {
        public readonly AppDbContext Context;

        public ExercisesController(AppDbContext context)
        {
            Context = context;
        }

        [HttpGet]
        public ActionResult GetAll(int subjectId)
        {
            var elements = Context.Exercises.ToList();
            return StatusCode(200, elements);
        }

        [HttpGet]
        [Route("{exerciseId}")]
        public ActionResult Get(int subjectId, int exerciseId)
        {
            var element = Context.Exercises.First(x => x.Id == exerciseId);
            return StatusCode(200, element);
        }

        [HttpPost]
        public ActionResult Create(int subjectId, Exercise element)
        {
            Context.Exercises.Add(element);
            Context.SaveChanges();
            return StatusCode(204);
        }

        [HttpPut]
        [Route("{exerciseId}")]
        public ActionResult Update(int subjectId, Exercise element)
        {
            return StatusCode(503);
        }

        [HttpDelete]
        [Route("{exerciseId}")]
        public ActionResult Delete(int subjectId, int exerciseId)
        {
            var element = Context.Exercises.First(x => x.Id == exerciseId);
            Context.Exercises.Remove(element);
            Context.SaveChanges();
            return StatusCode(204);
        }
    }
}
using System.Linq;
using Microsoft.AspNetCore.Mvc;
using ResourceAPI.Models;

namespace ResourceAPI.Controllers
{
    [Route("api/v1/Subjects/{subjectId}/Exercises/{exerciseId}/Answers")]
    [ApiController]
    public class AnswersController : ControllerBase
    {
        public readonly AppDbContext Context;

        public AnswersController(AppDbContext context)
        {
            Context = context;
        }

        [HttpGet]
        public ActionResult GetAll(int subjectId, int exerciseId)
        {
            var elements = Context.Answers.ToList();
            return StatusCode(200, elements);
        }

        [HttpGet]
        [Route("{answerId}")]
        public ActionResult Get(int subjectId, int exerciseId, int answerId)
        {
            var element = Context.Answers.First(x => x.Id == answerId);
            return StatusCode(200, element);
        }

        [HttpPost]
        public ActionResult Create(int subjectId, int exerciseId, Answer element)
        {
            Context.Answers.Add(element);
            Context.SaveChanges();
            return StatusCode(204);
        }

        [HttpPut]
        [Route("{answerId}")]
        public ActionResult Update(int subjectId, int exerciseId, Answer element)
        {
            return StatusCode(503);
        }

        [HttpDelete]
        [Route("{answerId}")]
        public ActionResult Delete(int subjectId, int exerciseId, int answerId)
        {
            var element = Context.Answers.First(x => x.Id == answerId);
            Context.Answers.Remove(element);
            Context.SaveChanges();
            return StatusCode(204);
        }
    }
}
using System.Collections.Generic;

namespace ResourceAPI.Models
{
    public class Exercise
    {
        public int Id { get; set; }
        public string Content { get; set; }
        public string Solution { get; set; }
        public List<Answer> Answers { get; set; }
        public Subject ParentSubject { get; set; }
    }
}
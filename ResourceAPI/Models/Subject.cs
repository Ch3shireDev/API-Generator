using System.Collections.Generic;

namespace ResourceAPI.Models
{
    public class Subject
    {
        public int Id { get; set; }
        public string Title { get; set; }
        public string Description { get; set; }
        public List<Exercise> Exercises { get; set; }
    }
}
namespace ResourceAPI.Models
{
    public class Answer
    {
        public int Id { get; set; }
        public string Content { get; set; }
        public bool Correct { get; set; }
        public Exercise ParentExercise { get; set; }
    }
}
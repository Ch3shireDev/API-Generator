using Microsoft.EntityFrameworkCore;
using ResourceAPI.Models;

namespace ResourceAPI
{
    public class AppDbContext : DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
        {
        }

        public DbSet<Subject> Subjects { get; set; }
        public DbSet<Exercise> Exercises { get; set; }
        public DbSet<Answer> Answers { get; set; }
    }
}
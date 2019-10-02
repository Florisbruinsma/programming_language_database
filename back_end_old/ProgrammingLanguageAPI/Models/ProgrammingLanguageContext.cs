
using Microsoft.EntityFrameworkCore;

namespace ProgrammingLanguageAPI.Models
{
    public class ProgrammingLanguageContext : DbContext
    {
        public ProgrammingLanguageContext(DbContextOptions<ProgrammingLanguageContext> options) : base(options)
        {
        }

        public DbSet<ProgrammingLanguage> ProgrammingLanguages { get; set; }
    }
}
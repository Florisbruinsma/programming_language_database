
namespace ProgrammingLanguagesAPIv2.Models
{
    public class ProgrammingLanguageDatabaseSettings : IProgrammingLanguageDatabaseSettings
    {
        public string ProgrammingLanguagesCollectionName { get; set; }
        public string ConnectionString { get; set; }
        public string DatabaseName { get; set; }
    }

    public interface IProgrammingLanguageDatabaseSettings
    {
        string ProgrammingLanguagesCollectionName { get; set; }
        string ConnectionString { get; set; }
        string DatabaseName { get; set; }
    }
}

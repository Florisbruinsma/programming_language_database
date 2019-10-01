using ProgrammingLanguagesAPIv2.Models;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Linq;

namespace ProgrammingLanguagesAPIv2.Services
{
    public class ProgrammingLanguageService
    {
        private readonly IMongoCollection<ProgrammingLanguage> _programmingLanguages;

        public ProgrammingLanguageService(IProgrammingLanguageDatabaseSettings settings)
        {
            var client = new MongoClient(settings.ConnectionString);
            var database = client.GetDatabase(settings.DatabaseName);

            _programmingLanguages = database.GetCollection<ProgrammingLanguage>(settings.ProgrammingLanguagesCollectionName);
        }

        public List<ProgrammingLanguage> Get() =>
            _programmingLanguages.Find(programmingLanguage => true).ToList();

        public ProgrammingLanguage Get(string id) =>
            _programmingLanguages.Find<ProgrammingLanguage>(programmingLanguage => programmingLanguage.Id == id).FirstOrDefault();

        public ProgrammingLanguage Create(ProgrammingLanguage programmingLanguage)
        {
            _programmingLanguages.InsertOne(programmingLanguage);
            return programmingLanguage;
        }

        public void Update(string id, ProgrammingLanguage programmingLanguageIn) =>
            _programmingLanguages.ReplaceOne(programmingLanguage => programmingLanguage.Id == id, programmingLanguageIn);

        public void Remove(ProgrammingLanguage programmingLanguageIn) =>
            _programmingLanguages.DeleteOne(programmaingLanguage => programmaingLanguage.Id == programmingLanguageIn.Id);

        public void Remove(string id) =>
            _programmingLanguages.DeleteOne(programmingLanguage => programmingLanguage.Id == id);
    }
}
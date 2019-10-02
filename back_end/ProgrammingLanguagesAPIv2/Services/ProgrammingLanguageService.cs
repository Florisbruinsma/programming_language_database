using ProgrammingLanguagesAPIv2.Models;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Linq;
using MongoDB.Bson;

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

        public List<ProgrammingLanguage> GetByName(string name) =>
           _programmingLanguages.Find<ProgrammingLanguage>(programmingLanguage => programmingLanguage.name == name).ToList();

        public List<ProgrammingLanguage> GetByApplication(string application) =>
           _programmingLanguages.Find<ProgrammingLanguage>(programmingLanguage => programmingLanguage.application == application).ToList();

        public List<ProgrammingLanguage> GetByFramework(string framework) =>
           _programmingLanguages.Find<ProgrammingLanguage>(programmingLanguage => programmingLanguage.framework == framework).ToList();

        public List<ProgrammingLanguage> GetByCompatible(string compatible) =>
           _programmingLanguages.Find<ProgrammingLanguage>(programmingLanguage => programmingLanguage.compatible == compatible).ToList();

        public List<ProgrammingLanguage> GetByAll(string search)
        {
            var builder = Builders<ProgrammingLanguage>.Filter;
            var filter = builder.Or(builder.Eq("name", search), builder.Eq("application", search), builder.Eq("framework", search), builder.Eq("compatible", search));
            var result = _programmingLanguages.Find(filter).ToList();
            return result;
        }

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
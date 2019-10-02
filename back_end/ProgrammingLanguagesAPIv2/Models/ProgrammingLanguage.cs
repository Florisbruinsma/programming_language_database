using MongoDB.Bson;
using MongoDB.Bson.Serialization.Attributes;

namespace ProgrammingLanguagesAPIv2.Models
{
    public class ProgrammingLanguage
    {
        [BsonId]
        [BsonRepresentation(BsonType.ObjectId)]
        public string Id { get; set; }

        [BsonElement("name")]
        public string name { get; set; }

        public string application { get; set; }

        public string framework{ get; set; }

        public string compatible { get; set; }
    }
}

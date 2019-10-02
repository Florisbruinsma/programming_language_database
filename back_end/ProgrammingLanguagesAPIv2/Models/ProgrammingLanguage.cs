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
        [BsonElement("application")]
        public string application { get; set; }
        [BsonElement("framework")]
        public string framework{ get; set; }
        [BsonElement("compatible")]
        public string compatible { get; set; }
    }
}

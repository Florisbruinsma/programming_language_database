using ProgrammingLanguagesAPIv2.Models;
using ProgrammingLanguagesAPIv2.Services;
using Microsoft.AspNetCore.Mvc;
using System.Collections.Generic;

namespace ProgrammingLanguagesAPIv2.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ProgrammingLanguagesController : ControllerBase
    {
        private readonly ProgrammingLanguageService _programmingLanguageService;

        public ProgrammingLanguagesController(ProgrammingLanguageService programmingLanguageService)
        {
            _programmingLanguageService = programmingLanguageService;
        }

        [HttpGet]
        public ActionResult<List<ProgrammingLanguage>> Get() =>
            _programmingLanguageService.Get();

        [HttpGet("{id:length(24)}", Name = "GetProgrammingLanguage")]
        public ActionResult<ProgrammingLanguage> Get(string id)
        {
            var programmingLanguage = _programmingLanguageService.Get(id);

            if (programmingLanguage == null)
            {
                return NotFound();
            }

            return programmingLanguage;
        }

        [HttpPost]
        public ActionResult<ProgrammingLanguage> Create(ProgrammingLanguage programmingLanguage)
        {
            _programmingLanguageService.Create(programmingLanguage);

            return CreatedAtRoute("GetProgrammingLanguage", new { id = programmingLanguage.Id.ToString() }, programmingLanguage);
        }

        [HttpPut("{id:length(24)}")]
        public IActionResult Update(string id, ProgrammingLanguage programmingLanguageIn)
        {
            var programmingLanguage = _programmingLanguageService.Get(id);

            if (programmingLanguage == null)
            {
                return NotFound();
            }

            _programmingLanguageService.Update(id, programmingLanguageIn);

            return Ok();
        }

        [HttpDelete("{id:length(24)}")]
        public IActionResult Delete(string id)
        {
            var programmingLanguage = _programmingLanguageService.Get(id);

            if (programmingLanguage == null)
            {
                return NotFound();
            }

            _programmingLanguageService.Remove(programmingLanguage.Id);

            return Ok();
        }
    }
}
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using ProgrammingLanguageAPI.Models;

namespace ProgrammingLanguageAPI.Controllers
{
    [Route("api/ProgrammingLanguages")]
    [ApiController]
    public class ProgrammingLanguagesController : ControllerBase
    {
        private readonly ProgrammingLanguageContext _context;

        public ProgrammingLanguagesController(ProgrammingLanguageContext context)
        {
            _context = context;
        }

        // GET: api/ProgrammingLanguages
        [HttpGet]
        public async Task<ActionResult<IEnumerable<ProgrammingLanguage>>> GetProgrammingLanguages()
        {
            return await _context.ProgrammingLanguages.ToListAsync();
        }

        // GET: api/ProgrammingLanguages/5
        [HttpGet("{id}")]
        public async Task<ActionResult<ProgrammingLanguage>> GetProgrammingLanguage(long id)
        {
            var programmingLanguage = await _context.ProgrammingLanguages.FindAsync(id);

            if (programmingLanguage == null)
            {
                return NotFound();
            }

            return programmingLanguage;
        }

        // PUT: api/ProgrammingLanguages/5
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPut("{id}")]
        public async Task<IActionResult> PutProgrammingLanguage(long id, ProgrammingLanguage programmingLanguage)
        {
            if (id != programmingLanguage.id)
            {
                return BadRequest();
            }

            _context.Entry(programmingLanguage).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!ProgrammingLanguageExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/ProgrammingLanguages
        // To protect from overposting attacks, please enable the specific properties you want to bind to, for
        // more details see https://aka.ms/RazorPagesCRUD.
        [HttpPost]
        public async Task<ActionResult<ProgrammingLanguage>> PostProgrammingLanguage(ProgrammingLanguage programmingLanguage)
        {
            _context.ProgrammingLanguages.Add(programmingLanguage);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetProgrammingLanguage), new { id = programmingLanguage.id }, programmingLanguage);
        }

        // DELETE: api/ProgrammingLanguages/5
        [HttpDelete("{id}")]
        public async Task<ActionResult<ProgrammingLanguage>> DeleteProgrammingLanguage(long id)
        {
            var programmingLanguage = await _context.ProgrammingLanguages.FindAsync(id);
            if (programmingLanguage == null)
            {
                return NotFound();
            }

            _context.ProgrammingLanguages.Remove(programmingLanguage);
            await _context.SaveChangesAsync();

            return programmingLanguage;
        }

        private bool ProgrammingLanguageExists(long id)
        {
            return _context.ProgrammingLanguages.Any(e => e.id == id);
        }
    }
}

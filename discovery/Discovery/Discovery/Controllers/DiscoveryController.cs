using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Mvc;
using Discovery.Storage;
using Discovery.Model;

namespace Discovery.Controllers
{
    [Route("discovery")]
    [ApiController]
    public class DiscoveryController : ControllerBase
    {

        // GET: discovery/get
        [HttpGet]
        [Route("get")]
        public IActionResult Get()
        {
            return Ok(DiscoveryStorage.GetStorage());
        }

        // POST: discovery/register
        [HttpPost]
        [Route("register")]
        public IActionResult Post([FromBody] DiscoveryData response)
        {
            DiscoveryStorage.Register(response.service, response.hostname);

            return Ok(ResponseTemplate.Ok200());
        }

        // DELETE: discovery/delete/{serviceName}
        [HttpDelete("delete/{serviceName}")]
        public IActionResult Delete(string serviceName, [FromQuery][Required] string node)
        {
            DiscoveryStorage.Delete(serviceName, node);

            return Ok(ResponseTemplate.Ok200());
        }
    }

    public static class ResponseTemplate
    {
        
        public static Dictionary<string, string> Ok200()
        {
            return new Dictionary<string, string>()
            {
                { "response:", "ok" }
            };
        }
    }
}

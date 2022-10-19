using Microsoft.AspNetCore.Mvc;
using Discovery.Storage;
namespace Discovery.Controllers
{
    [Route("discovery")]
    [ApiController]
    public class DiscoveryController : ControllerBase
    {

        // GET: discovery/get
        [HttpGet]
        [Route("get")]
        public Dictionary<string, List<string>> Get()
        {
            return DiscoveryStorage.GetStorage();
        }

        // POST: discovery/register
        [HttpPost]
        [Route("post")]
        public void Post([FromBody] DiscoveryData response)
        {
            DiscoveryStorage.Register(response.server, response.hostname);
        }

        // DELETE: discovery/delete/{serviceName}
        [HttpDelete("delete/{serviceName}")]
        public void Delete(string serviceName, [FromQuery] string node)
        {
            DiscoveryStorage.Delete(serviceName, node);
        }
    }

    public class DiscoveryData
    {
        public string server { get; set; }
        public string hostname { get; set; }
    }
}

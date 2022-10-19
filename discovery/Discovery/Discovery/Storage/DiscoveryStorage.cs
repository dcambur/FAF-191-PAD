namespace Discovery.Storage;

public static class DiscoveryStorage
{
    private static Dictionary<string, List<string>> _storage = new();

    public static void Register(string serviceName, string node)
    {
        if (_storage.ContainsKey(serviceName))
        {
            var curNodes = _storage[serviceName];

            if (!curNodes.Contains(node))
            {
                curNodes.Add(node);
                _storage[serviceName] = curNodes;
            }
        }
        else
        {
            var nodeList = new List<string> { node };
            _storage.Add(serviceName, nodeList);
        }
    }

    public static Dictionary<string, List<string>> GetStorage()
    {
        return _storage;
    }

    public static void Delete(string serviceName, string nodeName)
    {
        if (_storage.ContainsKey(serviceName))
        {
            var nodes = _storage[serviceName];

            if (nodes.Contains(nodeName))
            {
                nodes.Remove(nodeName);
                _storage[serviceName] = nodes;
            }
        } 
    }
}
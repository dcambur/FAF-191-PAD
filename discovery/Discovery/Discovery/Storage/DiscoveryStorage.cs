namespace Discovery.Storage;

public static class DiscoveryStorage
{
    private static readonly Dictionary<string, List<string>> Storage = new();
    private static readonly ReaderWriterLock Lock = new();
    
    public static void Register(string serviceName, string node)
    {
        Lock.AcquireWriterLock(10);
        if (Storage.ContainsKey(serviceName))
        {
            var curNodes = Storage[serviceName];

            if (!curNodes.Contains(node))
            {
                curNodes.Add(node);
                Storage[serviceName] = curNodes;
            }
        }
        else
        {
            var nodeList = new List<string> { node };
            Storage.Add(serviceName, nodeList);
        }
        Lock.ReleaseWriterLock();
    }

    public static Dictionary<string, List<string>> GetStorage()
    {
        return Storage;
    }

    public static void Delete(string serviceName, string nodeName)
    {
        Lock.AcquireWriterLock(10);
        if (Storage.ContainsKey(serviceName))
        {
            var nodes = Storage[serviceName];

            if (nodes.Contains(nodeName))
            {
                nodes.Remove(nodeName);
                Storage[serviceName] = nodes;
            }
        }
        Lock.ReleaseWriterLock();
    }
}
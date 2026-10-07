using System.Text.Json;
using System.Diagnostics;
using CUE4Parse.FileProvider;
using CUE4Parse.UE4.Objects.Engine;
using CUE4Parse.UE4.Versions;
using CUE4Parse_Conversion;
using CUE4Parse_Conversion.Options;
using Serilog;
using Serilog.Core;
using Serilog.Events;

// Research runner: reports stay private; never starts a game or downloads codecs/keys.
return await Run(args);

static async Task<int> Run(string[] args)
{
    if (args.Length is < 4 or > 5 || args[0] is not ("inventory" or "inspect" or "export"))
    {
        Console.Error.WriteLine("Usage: inventory|inspect|export INPUT_ROOT NEW_OUTPUT_ROOT GAME_UE4_20 [virtual/world.umap]");
        return 2;
    }
    string? output = null;
    try
    {
        if (!Enum.TryParse<EGame>(args[3], out var game) || !Enum.IsDefined(game))
            throw new ArgumentException("Unknown explicit parser version");
        if ((args[0] == "inventory") != (args.Length == 4))
            throw new ArgumentException("Only inspect/export require one virtual world path");
        var input = Path.GetFullPath(args[1]);
        var destination = Path.GetFullPath(args[2]);
        CheckRoots(input, destination);
        Directory.CreateDirectory(destination);
        output = destination;
        using var diagnostics = new StreamWriter(Path.Combine(output, "parser.log"));
        using var logger = new LoggerConfiguration().MinimumLevel.Information()
            .WriteTo.Sink(new PrivateLog(diagnostics)).CreateLogger();
        Log.Logger = logger;
        using var provider = new DefaultFileProvider(input, SearchOption.AllDirectories,
            new VersionContainer(game), StringComparer.OrdinalIgnoreCase);
        provider.Initialize();
        provider.Mount();
        provider.PostMount();
        provider.LoadVirtualPaths();
        var containerCount = Directory.EnumerateFiles(input, "*", SearchOption.AllDirectories)
            .Count(p => p.EndsWith(".pak", StringComparison.OrdinalIgnoreCase));
        var maps = provider.Files.Values.Where(f => f.Extension.Equals("umap", StringComparison.OrdinalIgnoreCase))
            .Select(f => f.Path).OrderBy(p => p, StringComparer.Ordinal).ToArray();
        Write(output, "inventory.json", new {
            parserCommit = "e4ea4ba8ec2b88d08b2066dfb8962863dccb36cc", parserGame = game.ToString(),
            mounted = provider.MountedVfs.Count, unmounted = provider.UnloadedVfs.Count,
            encryptedUnmounted = provider.UnloadedVfs.Count(v => v.IsEncrypted),
            suppliedPakContainers = containerCount,
            files = provider.Files.Count, worlds = maps,
            completeIsland = false, collisionQualified = false
        });
        if (provider.UnloadedVfs.Count != 0 || maps.Length == 0 ||
            containerCount != provider.MountedVfs.Count + provider.UnloadedVfs.Count)
            throw new InvalidDataException("Unmounted containers or no worlds: inventory is incomplete");
        if (args[0] == "inventory") { Console.WriteLine($"Indexed {maps.Length} world packages; no island completeness claim."); return 0; }
        var selected = args[4];
        if (!maps.Contains(selected, StringComparer.OrdinalIgnoreCase) || !SafeVirtual(selected))
            throw new ArgumentException("Select an exact safe virtual .umap path from inventory.json");
        var stem = selected[..^5];
        var world = provider.LoadPackageObject<UWorld>(stem + "." + stem.Split('/')[^1]);
        var level = world.PersistentLevel.Load<ULevel>() ?? throw new InvalidDataException("Missing persistent level");
        var actors = new Dictionary<string, int>();
        var missingActors = 0;
        foreach (var ptr in level.Actors)
        {
            if (ptr == null || ptr.IsNull) continue;
            var actor = ptr.Load();
            if (actor == null) { missingActors++; continue; }
            var type = actor.ExportType;
            actors[type] = actors.GetValueOrDefault(type) + 1;
        }
        var streaming = new List<object>();
        var missingLevels = 0;
        foreach (var ptr in world.StreamingLevels ?? [])
        {
            var entry = ptr.Load<ULevelStreaming>();
            var child = entry?.WorldAsset?.Load<UWorld>();
            if (child == null) missingLevels++;
            streaming.Add(new { loaded = child != null, world = child?.GetPathName() });
        }
        Write(output, "world.json", new { world = world.GetPathName(), actors, missingActors,
            streaming, missingLevels, completeIsland = false, collisionQualified = false });
        if (missingActors != 0 || missingLevels != 0)
            throw new InvalidDataException("Unresolved actor or streaming-world references");
        if (args[0] == "inspect") { Console.WriteLine("Selected world inspected; dependency closure and collision remain unverified."); return 0; }
        // Pinned upstream ResolveOutputPath unconditionally changes '/' to '\\'.
        // Do not silently write malformed paths or pretend POSIX output is validated.
        if (!OperatingSystem.IsWindows())
            throw new PlatformNotSupportedException("Pinned USD exporter requires Windows path handling; use Windows for export");
        if (provider.Files.Keys.Any(p => !SafeVirtual(p)))
            throw new InvalidDataException("Unsafe virtual package path");
        var session = new ExportSession { MaxDegreeOfParallelism = 2 };
        session.Add(world);
        var results = await session.RunAsync(Path.Combine(output, "usd"), new ExportOptions(meshFormat: EMeshFormat.USD));
        Write(output, "export.json", new { completeIsland = false, collisionQualified = false,
            results = results.Select(r => new { r.Success, r.ObjectPath, errorType = r.Error?.GetType().Name }) });
        if (results.Count == 0 || results.Any(r => !r.Success))
            throw new InvalidDataException("One or more USD exports failed; partial output retained");
        Console.WriteLine("USD candidate written; inspect missing layers, dummy meshes, units, transforms and collision before use.");
        return 0;
    }
    catch (Exception e)
    {
        // Detailed reports are private. Console never returns input paths or package data.
        if (output != null) Write(output, "failure.json", new { type = e.GetType().Name, message = e.Message });
        Console.Error.WriteLine($"FAIL: {e.GetType().Name}; private report retained if output was created.");
        return 1;
    }
}

static bool SafeVirtual(string path) => !string.IsNullOrWhiteSpace(path) &&
    !Path.IsPathRooted(path) && !path.Contains('\\') && !path.Contains(':') &&
    path.Split('/').All(p => p is not ("" or "." or ".."));

static void CheckRoots(string input, string output)
{
    if (!Directory.Exists(input) || Directory.Exists(output) || File.Exists(output))
        throw new ArgumentException("Input must exist and output must be new");
    foreach (var root in new[] { input, output })
    {
        for (var d = new DirectoryInfo(root); d != null; d = d.Parent)
            if (d.LinkTarget != null) throw new ArgumentException("Symlink/reparse roots are unsupported");
        // Within any Git checkout only its ignored .private directory may hold data.
        for (var d = new DirectoryInfo(root); d != null; d = d.Parent)
            if (Directory.Exists(Path.Combine(d.FullName, ".git")) || File.Exists(Path.Combine(d.FullName, ".git")))
                if (!Within(root, Path.Combine(d.FullName, ".private")) ||
                    !GitConfirmsIgnoredRoot(d.FullName, root))
                    throw new ArgumentException("Use an ignored, untracked .private root or a root outside source control");
    }
    if (Within(input, output) || Within(output, input))
        throw new ArgumentException("Input and output roots must be separate");
    var pending = new Stack<string>();
    pending.Push(input);
    while (pending.TryPop(out var directory))
        foreach (var path in Directory.EnumerateFileSystemEntries(directory))
        {
            var attributes = File.GetAttributes(path);
            if ((attributes & FileAttributes.ReparsePoint) != 0)
                throw new ArgumentException("Input tree contains links");
            if ((attributes & FileAttributes.Directory) != 0) pending.Push(path);
        }
}
static bool GitConfirmsIgnoredRoot(string repository, string root)
{
    // Directory names alone do not establish privacy. Fail closed if Git is unavailable.
    var ignored = Git("check-ignore", "--quiet", "--", root);
    if (ignored.code != 0) return false;
    var tracked = Git("ls-files", "--", root);
    return tracked.code == 0 && tracked.output.Length == 0;

    (int code, string output) Git(params string[] arguments)
    {
        var start = new ProcessStartInfo("git") {
            UseShellExecute = false, RedirectStandardOutput = true, RedirectStandardError = true
        };
        start.ArgumentList.Add("-C");
        start.ArgumentList.Add(repository);
        foreach (var argument in arguments) start.ArgumentList.Add(argument);
        using var process = Process.Start(start) ?? throw new IOException("Cannot verify ignored root");
        var stdout = process.StandardOutput.ReadToEndAsync();
        var stderr = process.StandardError.ReadToEndAsync();
        if (!process.WaitForExit(10000))
        {
            process.Kill(entireProcessTree: true);
            throw new IOException("Cannot verify ignored root");
        }
        stderr.GetAwaiter().GetResult();
        return (process.ExitCode, stdout.GetAwaiter().GetResult());
    }
}
static bool Within(string path, string root) => path.Equals(root, StringComparison.OrdinalIgnoreCase) ||
    path.StartsWith(Path.TrimEndingDirectorySeparator(root) + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase);
static void Write(string root, string name, object data) =>
    File.WriteAllText(Path.Combine(root, name), JsonSerializer.Serialize(data, new JsonSerializerOptions { WriteIndented = true }));

sealed class PrivateLog(StreamWriter writer) : ILogEventSink
{
    public void Emit(LogEvent e)
    {
        lock (writer) { writer.WriteLine(e.RenderMessage()); writer.WriteLine(e.Exception); writer.Flush(); }
    }
}

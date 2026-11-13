using System.IO;
using UnrealBuildTool;

public class StarTrekRPG : ModuleRules
{
    public StarTrekRPG(ReadOnlyTargetRules Target) : base(Target)
    {
        if (Target.Platform != UnrealTargetPlatform.Win64)
            throw new BuildException("StarTrekRPG HOST integration requires Win64.");

        PCHUsage = PCHUsageMode.NoPCHs;
        PrivateDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "InputCore", "Slate", "SlateCore", "RHI" });

        string ThirdParty = Path.Combine(ProjectDirectory(), "Binaries", "Host");
        string Include = Path.Combine(ThirdParty, "include");
        if (!File.Exists(Path.Combine(Include, "trek", "host", "host_abi.h")))
            throw new BuildException("Prepare the Release HOST dependency with Build/Prepare-Host.ps1 before UBT.");

        PrivateIncludePaths.Add(Include);
        foreach (string Dll in new[] { "TrekF04Bridge.dll", "TrekHost.dll" })
        {
            string Source = Path.Combine(ThirdParty, Dll);
            if (!File.Exists(Source))
                throw new BuildException("Missing HOST dependency: " + Source);
            RuntimeDependencies.Add("$(ProjectDir)/Binaries/Win64/" + Dll, Source, StagedFileType.NonUFS);
        }
    }

    private string ProjectDirectory()
    {
        return Path.GetFullPath(Path.Combine(ModuleDirectory, "../.."));
    }
}

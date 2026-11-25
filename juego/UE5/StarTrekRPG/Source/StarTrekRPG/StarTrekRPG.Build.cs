using System.IO;
using UnrealBuildTool;

public class StarTrekRPG : ModuleRules
{
    public StarTrekRPG(ReadOnlyTargetRules Target) : base(Target)
    {
        if (Target.Platform != UnrealTargetPlatform.Win64)
            throw new BuildException("StarTrekRPG HOST integration requires Win64.");

        PCHUsage = PCHUsageMode.NoPCHs;
        PrivateDependencyModuleNames.AddRange(new[] { "Core", "CoreUObject", "Engine", "InputCore", "Slate", "SlateCore", "RHI", "UMG" });

        if (Target.bBuildEditor)
            PrivateDependencyModuleNames.AddRange(new[] { "UnrealEd", "UMGEditor", "AssetTools", "AssetRegistry", "AudioEditor", "LevelSequence", "MovieScene" });

        string ThirdParty = Path.Combine(ProjectDirectory(), "Binaries", "Host");
        string Include = Path.Combine(ThirdParty, "include");
        foreach (string Header in new[] { "host_abi.h", "academy_abi.h" })
        {
            string Source = Path.Combine(Include, "trek", "host", Header);
            if (!File.Exists(Source))
                throw new BuildException("Missing HOST header: " + Source +
                    ". Run Build/Prepare-Host.ps1 from the repository project with -CoreSource <clean pinned CoreRPG> " +
                    "-BuildRoot <native build output> -ProjectDir \"" + ProjectDirectory() + "\" before UBT. See README.md.");
        }

        PrivateIncludePaths.Add(Include);
        foreach (string Dll in new[] { "TrekF04Bridge.dll", "TrekHost.dll" })
        {
            string Source = Path.Combine(ThirdParty, Dll);
            if (!File.Exists(Source))
                throw new BuildException("Missing HOST dependency: " + Source +
                    ". Run Build/Prepare-Host.ps1 for this ProjectDir before UBT. See README.md.");
            RuntimeDependencies.Add("$(ProjectDir)/Binaries/Win64/" + Dll, Source, StagedFileType.NonUFS);
        }
    }

    private string ProjectDirectory()
    {
        return Path.GetFullPath(Path.Combine(ModuleDirectory, "../.."));
    }
}

using UnrealBuildTool;
using System.IO;
public class F02CoreLab : ModuleRules {
    public F02CoreLab(ReadOnlyTargetRules Target) : base(Target) {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;
        CppStandard = CppStandardVersion.Cpp20;
        bEnableExceptions = false; // DLL catches all C++ exceptions before returning.
        PublicDependencyModuleNames.AddRange(new [] { "Core", "CoreUObject", "Engine" });
        if (Target.Platform != UnrealTargetPlatform.Win64)
            throw new BuildException("F02 UE laboratory has only been validated on Win64");
        string ProjectRoot = Path.GetFullPath(Path.Combine(ModuleDirectory, "../.."));
        string ThirdParty = Path.Combine(ProjectRoot, "ThirdParty");
        PublicIncludePaths.Add(Path.Combine(ThirdParty, "include"));
        PublicAdditionalLibraries.Add(Path.Combine(ThirdParty, "Win64", "TrekF02Bridge.lib"));
        PublicDelayLoadDLLs.Add("TrekF02Bridge.dll");
        RuntimeDependencies.Add("$(ProjectDir)/Binaries/Win64/TrekF02Bridge.dll",
            Path.Combine(ThirdParty, "Win64", "TrekF02Bridge.dll"));
    }
}

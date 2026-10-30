using UnrealBuildTool;
using System.IO;
public class F02CoreLab : ModuleRules {
    public F02CoreLab(ReadOnlyTargetRules Target) : base(Target) {
        PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs; CppStandard=CppStandardVersion.Cpp20; bEnableExceptions=false;
        PublicDependencyModuleNames.AddRange(new [] { "Core","CoreUObject","Engine" });
        if(Target.Platform!=UnrealTargetPlatform.Win64) throw new BuildException("F03 UE validated on Win64 only");
        string ThirdParty=Path.GetFullPath(Path.Combine(ModuleDirectory,"../../ThirdParty"));
        PublicIncludePaths.Add(Path.Combine(ThirdParty,"include"));
        foreach(string Bridge in new [] {"TrekF02Bridge","TrekF03Bridge"}) {
            PublicAdditionalLibraries.Add(Path.Combine(ThirdParty,"Win64",Bridge+".lib"));
            PublicDelayLoadDLLs.Add(Bridge+".dll");
            RuntimeDependencies.Add("$(ProjectDir)/Binaries/Win64/"+Bridge+".dll",Path.Combine(ThirdParty,"Win64",Bridge+".dll"));
        }
    }
}

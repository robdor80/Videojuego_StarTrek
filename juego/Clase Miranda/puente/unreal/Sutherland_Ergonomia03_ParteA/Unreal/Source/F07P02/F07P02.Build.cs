using UnrealBuildTool;
public class F07P02 : ModuleRules {
    public F07P02(ReadOnlyTargetRules Target) : base(Target) {
        PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;
        PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine","InputCore","Json"});
    }
}



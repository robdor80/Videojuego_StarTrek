using UnrealBuildTool;
public class ValhallaComputer : ModuleRules { public ValhallaComputer(ReadOnlyTargetRules Target):base(Target){PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine"});}}

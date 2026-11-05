using UnrealBuildTool;
public class ValhallaDoors:ModuleRules{public ValhallaDoors(ReadOnlyTargetRules Target):base(Target){PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine","Json","InputCore","EnhancedInput","RHI","RenderCore"});}}

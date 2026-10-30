using UnrealBuildTool;
public class STAutomaticDoors : ModuleRules {
 public STAutomaticDoors(ReadOnlyTargetRules Target):base(Target) {
  PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;
  PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine"});
 }
}

using UnrealBuildTool;
public class STAutomaticDoorsEditor:ModuleRules {
 public STAutomaticDoorsEditor(ReadOnlyTargetRules Target):base(Target) {
  PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;
  PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine","STAutomaticDoors"});
  PrivateDependencyModuleNames.AddRange(new string[]{"UnrealEd","Json","JsonUtilities","ProceduralMeshComponent","NavigationSystem"});
 }
}

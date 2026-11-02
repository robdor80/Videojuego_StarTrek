using UnrealBuildTool;
using System.IO;
public class F05OrdersLab : ModuleRules {
 public F05OrdersLab(ReadOnlyTargetRules Target) : base(Target) {
  PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs;CppStandard=CppStandardVersion.Cpp20;
  PublicDependencyModuleNames.AddRange(new[]{"Core","CoreUObject","Engine"});
  if(Target.Platform!=UnrealTargetPlatform.Win64)throw new BuildException("F05 MSI harness requires Win64");
  string ThirdParty=Path.GetFullPath(Path.Combine(ModuleDirectory,"../../ThirdParty"));
  PublicIncludePaths.Add(Path.Combine(ThirdParty,"include"));
  PublicAdditionalLibraries.Add(Path.Combine(ThirdParty,"Win64/TrekF04Bridge.lib"));
  PublicDelayLoadDLLs.Add("TrekF04Bridge.dll");
  RuntimeDependencies.Add("$(ProjectDir)/Binaries/Win64/TrekF04Bridge.dll",Path.Combine(ThirdParty,"Win64/TrekF04Bridge.dll"));
 }
}

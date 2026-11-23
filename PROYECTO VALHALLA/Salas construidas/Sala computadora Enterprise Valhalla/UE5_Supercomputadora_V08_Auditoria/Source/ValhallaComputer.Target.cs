using UnrealBuildTool;
public class ValhallaComputerTarget : TargetRules {
 public ValhallaComputerTarget(TargetInfo Target):base(Target){Type=TargetType.Game;DefaultBuildSettings=BuildSettingsVersion.Latest;IncludeOrderVersion=EngineIncludeOrderVersion.Latest;ExtraModuleNames.Add("ValhallaComputer");}
}

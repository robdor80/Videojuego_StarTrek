using UnrealBuildTool;
public class ValhallaComputerEditorTarget : TargetRules {
 public ValhallaComputerEditorTarget(TargetInfo Target):base(Target){Type=TargetType.Editor;DefaultBuildSettings=BuildSettingsVersion.Latest;IncludeOrderVersion=EngineIncludeOrderVersion.Latest;ExtraModuleNames.Add("ValhallaComputer");}
}

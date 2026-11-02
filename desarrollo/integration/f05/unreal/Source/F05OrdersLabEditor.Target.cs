using UnrealBuildTool;
using System.Collections.Generic;
public class F05OrdersLabEditorTarget : TargetRules {
 public F05OrdersLabEditorTarget(TargetInfo Target) : base(Target) {
  Type=TargetType.Editor;DefaultBuildSettings=BuildSettingsVersion.Latest;
  ExtraModuleNames.Add("F05OrdersLab");
 }
}

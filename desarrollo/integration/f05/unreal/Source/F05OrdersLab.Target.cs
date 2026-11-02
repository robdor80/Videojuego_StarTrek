using UnrealBuildTool;
using System.Collections.Generic;
public class F05OrdersLabTarget : TargetRules {
 public F05OrdersLabTarget(TargetInfo Target) : base(Target) {
  Type=TargetType.Game;DefaultBuildSettings=BuildSettingsVersion.Latest;
  ExtraModuleNames.Add("F05OrdersLab");
 }
}

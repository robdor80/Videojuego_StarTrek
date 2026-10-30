using UnrealBuildTool;
using System.Collections.Generic;
public class F02CoreLabTarget : TargetRules {
    public F02CoreLabTarget(TargetInfo Target) : base(Target) {
        Type = TargetType.Game;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("F02CoreLab");
    }
}

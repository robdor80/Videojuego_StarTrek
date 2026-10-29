using UnrealBuildTool;
using System.Collections.Generic;
public class F02CoreLabEditorTarget : TargetRules {
    public F02CoreLabEditorTarget(TargetInfo Target) : base(Target) {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.Latest;
        IncludeOrderVersion = EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.Add("F02CoreLab");
    }
}

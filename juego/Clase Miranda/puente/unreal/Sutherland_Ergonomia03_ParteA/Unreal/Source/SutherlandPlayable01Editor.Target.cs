using UnrealBuildTool;
public class SutherlandPlayable01EditorTarget : TargetRules {
    public SutherlandPlayable01EditorTarget(TargetInfo Target) : base(Target) {
        Type=TargetType.Editor; DefaultBuildSettings=BuildSettingsVersion.Latest;
        IncludeOrderVersion=EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.AddRange(new string[]{"F07P02","ChairAutoLab","ChairAutoLabEditor"});
    }
}

using UnrealBuildTool;
public class SutherlandPlayable01Target : TargetRules {
    public SutherlandPlayable01Target(TargetInfo Target) : base(Target) {
        Type=TargetType.Game; DefaultBuildSettings=BuildSettingsVersion.Latest;
        IncludeOrderVersion=EngineIncludeOrderVersion.Latest;
        ExtraModuleNames.AddRange(new string[]{"F07P02","ChairAutoLab"});
    }
}

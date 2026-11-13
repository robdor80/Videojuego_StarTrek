using UnrealBuildTool;

public class StarTrekRPGEditorTarget : TargetRules
{
    public StarTrekRPGEditorTarget(TargetInfo Target) : base(Target)
    {
        Type = TargetType.Editor;
        DefaultBuildSettings = BuildSettingsVersion.V7;
        IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8;
        ExtraModuleNames.Add("StarTrekRPG");
    }
}

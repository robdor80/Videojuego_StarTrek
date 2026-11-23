#include "HostDiagnosticMapCommandlet.h"

#if WITH_EDITOR
#include "Engine/World.h"
#include "GameFramework/PlayerStart.h"
#include "HAL/FileManager.h"
#include "Misc/PackageName.h"
#include "UObject/Package.h"
#include "UObject/SavePackage.h"

int32 UHostDiagnosticMapCommandlet::Main(const FString&)
{
    const FString Name = TEXT("/Game/Diagnostics/HostDiagnostic");
    const FString File = FPackageName::LongPackageNameToFilename(Name, FPackageName::GetMapPackageExtension());
    if (IFileManager::Get().FileExists(*File))
    {
        UE_LOG(LogTemp, Display, TEXT("H06 diagnostic map already exists: %s"), *File);
        return 0;
    }

    UPackage* Package = CreatePackage(*Name);
    UWorld* World = UWorld::CreateWorld(EWorldType::Editor, false, TEXT("HostDiagnostic"), Package);
    World->SetFlags(RF_Public | RF_Standalone);
    World->SpawnActor<APlayerStart>();
    FSavePackageArgs SaveArgs;
    SaveArgs.TopLevelFlags = RF_Public | RF_Standalone;
    const bool Saved = UPackage::SavePackage(Package, World, *File, SaveArgs);
    World->DestroyWorld(false);
    UE_CLOG(Saved, LogTemp, Display, TEXT("H06 generated diagnostic map: %s"), *File);
    UE_CLOG(!Saved, LogTemp, Error, TEXT("H06 failed to generate diagnostic map: %s"), *File);
    return Saved ? 0 : 1;
}
#else
int32 UHostDiagnosticMapCommandlet::Main(const FString&)
{
    return 1;
}
#endif

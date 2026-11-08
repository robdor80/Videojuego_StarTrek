#include "VH06Tools.h"
#include "AssetCompilingManager.h"
#include "Components/InstancedStaticMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Editor.h"
#include "Engine/StaticMesh.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "IMessageLogListing.h"
#include "Logging/TokenizedMessage.h"
#include "MaterialShared.h"
#include "Materials/Material.h"
#include "Materials/MaterialExpression.h"
#include "MessageLogModule.h"
#include "Misc/PackageName.h"
#include "Misc/SecureHash.h"
#include "RHI.h"
#include "Serialization/BufferArchive.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/ObjectAndNameAsStringProxyArchive.h"
#include "ShaderCompiler.h"
#include "UObject/SavePackage.h"
#include "UObject/UObjectIterator.h"
#include "VHAutomaticDoor.h"

namespace
{
FString Json06(const TSharedRef<FJsonObject> &O)
{
    FString S;
    auto W = TJsonWriterFactory<>::Create(&S);
    FJsonSerializer::Serialize(O, W);
    return S;
}
TArray<TSharedPtr<FJsonValue>> Vector06(FVector V)
{
    return {MakeShared<FJsonValueNumber>(V.X), MakeShared<FJsonValueNumber>(V.Y), MakeShared<FJsonValueNumber>(V.Z)};
}
TSet<UMaterial *> UsedInstancedMaterials(UWorld *W)
{
    TSet<UMaterial *> Out;
    for (TActorIterator<AActor> It(W); It; ++It)
    {
        TArray<UInstancedStaticMeshComponent *> C;
        It->GetComponents(C);
        for (auto *Part : C)
            for (int32 I = 0; I < Part->GetNumMaterials(); I++)
                if (auto *M = Part->GetMaterial(I))
                    Out.Add(M->GetMaterial());
    }
    return Out;
}
FString GraphDigest(UMaterial *M)
{
    FBufferArchive Bytes;
    FObjectAndNameAsStringProxyArchive Ar(Bytes, false);
    for (auto E : M->GetExpressionCollection().Expressions)
    {
        FString C = E->GetClass()->GetPathName();
        Ar << C;
        E->Serialize(Ar);
    }
    uint8 Hash[20];
    FSHA1::HashBuffer(Bytes.GetData(), Bytes.Num(), Hash);
    return BytesToHex(Hash, 20);
}
bool Save06(UObject *O)
{
    auto *P = O->GetOutermost();
    P->MarkPackageDirty();
    FSavePackageArgs A;
    A.TopLevelFlags = RF_Public | RF_Standalone;
    A.SaveFlags = SAVE_NoError;
    return UPackage::SavePackage(
        P, O, *FPackageName::LongPackageNameToFilename(P->GetName(), FPackageName::GetAssetPackageExtension()), A);
}
} // namespace
FString UVH06Tools::MapCheckSnapshot()
{
    auto O = MakeShared<FJsonObject>();
    UWorld *W = GEditor->GetEditorWorldContext().World();
    auto L = FModuleManager::LoadModuleChecked<FMessageLogModule>(TEXT("MessageLog")).GetLogListing(TEXT("MapCheck"));
    FString InitialMessages = L->GetAllMessagesAsString();
    GEditor->Exec(W, TEXT("MAP CHECK"));
    O->SetStringField(TEXT("messages_before_fresh_check"), InitialMessages);
    TArray<TSharedPtr<FJsonValue>> Messages, Materials;
    int32 Warnings = 0, Errors = 0, UsageWarnings = 0, Unset = 0;
    for (const auto &Message : L->GetFilteredMessages())
    {
        auto R = MakeShared<FJsonObject>();
        FString S = Message->ToText().ToString();
        R->SetStringField(TEXT("message"), S);
        R->SetNumberField(TEXT("severity"), (int)Message->GetSeverity());
        Messages.Add(MakeShared<FJsonValueObject>(R));
        if (Message->GetSeverity() == EMessageSeverity::Error)
            Errors++;
        if (Message->GetSeverity() == EMessageSeverity::Warning ||
            Message->GetSeverity() == EMessageSeverity::PerformanceWarning)
        {
            Warnings++;
            if (S.Contains(TEXT("InstancedStatic")) || S.Contains(TEXT("instanced static"), ESearchCase::IgnoreCase))
                UsageWarnings++;
        }
    }
    for (auto *M : UsedInstancedMaterials(W))
    {
        auto R = MakeShared<FJsonObject>();
        bool Used = M->GetUsageByFlag(MATUSAGE_InstancedStaticMeshes);
        if (!Used)
            Unset++;
        R->SetStringField(TEXT("material"), M->GetPathName());
        R->SetBoolField(TEXT("instanced_usage"), Used);
        R->SetBoolField(TEXT("two_sided"), M->TwoSided);
        R->SetStringField(TEXT("graph_digest"), GraphDigest(M));
        Materials.Add(MakeShared<FJsonValueObject>(R));
    }
    O->SetArrayField(TEXT("messages"), Messages);
    O->SetNumberField(TEXT("warnings"), Warnings);
    O->SetNumberField(TEXT("errors"), Errors);
    O->SetNumberField(TEXT("instanced_usage_warnings"), UsageWarnings);
    O->SetNumberField(TEXT("materials_missing_flag"), Unset);
    O->SetArrayField(TEXT("materials"), Materials);
    return Json06(O);
}
FString UVH06Tools::CorrectInstancedMaterialUsage()
{
    auto O = MakeShared<FJsonObject>();
    TArray<TSharedPtr<FJsonValue>> Changes;
    bool OK = true;
    for (auto *M : UsedInstancedMaterials(GEditor->GetEditorWorldContext().World()))
    {
        FString Before = GraphDigest(M);
        M->SetMaterialUsage(MATUSAGE_InstancedStaticMeshes);
        M->PostEditChange();
        FString After = GraphDigest(M);
        bool Same = Before == After;
        OK &= Same && M->GetUsageByFlag(MATUSAGE_InstancedStaticMeshes) && Save06(M);
        auto R = MakeShared<FJsonObject>();
        R->SetStringField(TEXT("material"), M->GetPathName());
        R->SetStringField(TEXT("before_graph"), Before);
        R->SetStringField(TEXT("after_graph"), After);
        R->SetBoolField(TEXT("graph_unchanged"), Same);
        Changes.Add(MakeShared<FJsonValueObject>(R));
    }
    O->SetBoolField(TEXT("ok"), OK);
    O->SetArrayField(TEXT("changes"), Changes);
    return Json06(O);
}
void UVH06Tools::FinishCompilation()
{
    FAssetCompilingManager::Get().FinishAllCompilation();
    // Material shader-cache DDC requests can still be pending before compile jobs exist.
    for (TObjectIterator<UMaterial> It; It; ++It)
    {
        if (It->HasAnyFlags(RF_ClassDefaultObject))
            continue;
        for (int32 Q = 0; Q <= (int32)EMaterialQualityLevel::Num; Q++)
        {
            auto *R = It->GetMaterialResource(GMaxRHIShaderPlatform, (EMaterialQualityLevel::Type)Q);
            if (R && R->IsCachingShaders())
            {
                R->FinishCacheShaders();
                R->FinishCompilation();
            }
        }
    }
    if (GShaderCompilingManager)
        GShaderCompilingManager->FinishAllCompilation();
}
FString UVH06Tools::SurveyGround(float Radius, float HalfHeight, float Grid)
{
    FinishCompilation();
    auto O = MakeShared<FJsonObject>();
    UWorld *W = GEditor->GetEditorWorldContext().World();
    W->UpdateWorldComponents(true, false);
    for (TActorIterator<AActor> I(W); I; ++I)
    {
        TArray<UStaticMeshComponent *> Cs;
        I->GetComponents(Cs);
        for (auto *C : Cs)
        {
            C->UpdateBounds();
            C->RecreatePhysicsState();
        }
    }
    FBox Bounds(ForceInit);
    TArray<TSharedPtr<FJsonValue>> Cells;
    FCollisionQueryParams Q(SCENE_QUERY_STAT(VH06Ground), false);
    int32 GroundCount = 0, ClearCount = 0;
    TArray<AVHAutomaticDoor *> Doors;
    for (TActorIterator<AVHAutomaticDoor> It(W); It; ++It)
    {
        auto *D = *It;
        Doors.Add(D);
        D->LeftLeaf->SetRelativeLocation(D->LeftClosedLocation + FVector(0, -D->TravelDistance, 0));
        D->RightLeaf->SetRelativeLocation(D->RightClosedLocation + FVector(0, D->TravelDistance, 0));
    }
    for (TActorIterator<AActor> It(W); It; ++It)
    {
        TArray<UInstancedStaticMeshComponent *> Components;
        It->GetComponents(Components);
        for (auto *C : Components)
            Bounds += C->Bounds.GetBox();
    }
    Grid = FMath::Max(10.f, Grid);
    float X0 = FMath::FloorToFloat(Bounds.Min.X / Grid) * Grid, Y0 = FMath::FloorToFloat(Bounds.Min.Y / Grid) * Grid;
    for (float X = X0; X <= Bounds.Max.X + Grid; X += Grid)
        for (float Y = Y0; Y <= Bounds.Max.Y + Grid; Y += Grid)
        {
            FHitResult H;
            if (!W->LineTraceSingleByChannel(H, FVector(X, Y, 200), FVector(X, Y, -300), ECC_Visibility, Q))
                continue;
            if (H.ImpactNormal.Z < .7)
                continue;
            GroundCount++;
            FVector Center = H.ImpactPoint + FVector(0, 0, HalfHeight + 2.15);
            bool Clear = !W->OverlapBlockingTestByChannel(Center, FQuat::Identity, ECC_Pawn,
                                                          FCollisionShape::MakeCapsule(Radius, HalfHeight), Q);
            if (Clear)
                ClearCount++;
            auto R = MakeShared<FJsonObject>();
            R->SetArrayField(TEXT("floor"), Vector06(H.ImpactPoint));
            R->SetBoolField(TEXT("standing_capsule_clear"), Clear);
            R->SetStringField(TEXT("actor"), H.GetActor() ? H.GetActor()->GetActorLabel() : TEXT("None"));
            R->SetStringField(TEXT("component"), H.GetComponent() ? H.GetComponent()->GetName() : TEXT("None"));
            Cells.Add(MakeShared<FJsonValueObject>(R));
        }
    for (auto *D : Doors)
        D->ResetClosed();
    O->SetArrayField(TEXT("bounds_min"), Vector06(Bounds.Min));
    O->SetArrayField(TEXT("bounds_max"), Vector06(Bounds.Max));
    O->SetNumberField(TEXT("grid_cm"), Grid);
    O->SetNumberField(TEXT("radius_cm"), Radius);
    O->SetNumberField(TEXT("half_height_cm"), HalfHeight);
    O->SetNumberField(TEXT("ground_samples"), GroundCount);
    O->SetNumberField(TEXT("clear_standing_samples"), ClearCount);
    O->SetArrayField(TEXT("cells"), Cells);
    O->SetStringField(TEXT("method"),
                      TEXT("Real static-world downward visibility trace from Z200 to -300 cm; standing pawn capsule at "
                           "floor + native floor distance. Door poses opened temporarily for spatial survey only."));
    return Json06(O);
}

FString UVH06Tools::ProbeSegments(const FString &Json)
{
    TSharedPtr<FJsonObject> In;
    FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(Json), In);
    TArray<TSharedPtr<FJsonValue>> Out;
    UWorld *W = GEditor->GetEditorWorldContext().World();
    FinishCompilation();
    W->UpdateWorldComponents(true, false);
    for (TActorIterator<AActor> I(W); I; ++I)
    {
        TArray<UStaticMeshComponent *> Cs;
        I->GetComponents(Cs);
        for (auto *C : Cs)
        {
            C->UpdateBounds();
            C->RecreatePhysicsState();
        }
    }
    for (auto &V : In->GetArrayField(TEXT("segments")))
    {
        auto O = V->AsObject();
        auto A = O->GetArrayField(TEXT("start"));
        auto B = O->GetArrayField(TEXT("end"));
        FVector S(A[0]->AsNumber(), A[1]->AsNumber(), A[2]->AsNumber()),
            E(B[0]->AsNumber(), B[1]->AsNumber(), B[2]->AsNumber());
        FHitResult H;
        FCollisionQueryParams Q;
        Q.bTraceComplex = true;
        bool Hit = W->SweepSingleByChannel(H, S + FVector(0, 0, 92.15), E + FVector(0, 0, 92.15), FQuat::Identity,
                                           ECC_Pawn, FCollisionShape::MakeCapsule(35, 90), Q);
        O->SetBoolField(TEXT("blocked"), Hit);
        if (Hit)
        {
            O->SetStringField(TEXT("actor"), GetNameSafe(H.GetActor()));
            O->SetStringField(TEXT("component"), GetNameSafe(H.GetComponent()));
            O->SetNumberField(TEXT("instance"), H.Item);
            O->SetBoolField(TEXT("penetrating"), H.bStartPenetrating);
            O->SetNumberField(TEXT("time"), H.Time);
            O->SetStringField(TEXT("point"), H.ImpactPoint.ToString());
        }
        FHitResult C;
        if (W->LineTraceSingleByChannel(C, S + FVector(0, 0, 10), S + FVector(0, 0, 1000), ECC_Visibility, Q))
        {
            O->SetNumberField(TEXT("headroom_cm"), C.ImpactPoint.Z - S.Z);
            O->SetStringField(TEXT("ceiling_component"), GetNameSafe(C.GetComponent()));
            O->SetNumberField(TEXT("ceiling_instance"), C.Item);
        }
        Out.Add(MakeShared<FJsonValueObject>(O));
    }
    auto Result = MakeShared<FJsonObject>();
    Result->SetArrayField(TEXT("segments"), Out);
    FString Text;
    FJsonSerializer::Serialize(Result, TJsonWriterFactory<>::Create(&Text));
    return Text;
}

#include "AssetRegistry/AssetRegistryModule.h"
#include "PhysicsEngine/BodySetup.h"
#include "StaticMeshAttributes.h"
FString UVH06Tools::AuditWinding()
{
    TSet<UStaticMesh *> Meshes;
    Meshes.Add(LoadObject<UStaticMesh>(nullptr, TEXT("/Engine/BasicShapes/Cube.Cube")));
    for (TActorIterator<AActor> I(GEditor->GetEditorWorldContext().World()); I; ++I)
    {
        TArray<UStaticMeshComponent *> Cs;
        I->GetComponents(Cs);
        for (auto *C : Cs)
            if (C->GetStaticMesh())
                Meshes.Add(C->GetStaticMesh());
    }
    TArray<TSharedPtr<FJsonValue>> Rows;
    for (auto *M : Meshes)
    {
        auto *MD = M->GetMeshDescription(0);
        if (!MD)
            continue;
        FStaticMeshAttributes A(*MD);
        auto P = A.GetVertexPositions();
        auto N = A.GetVertexInstanceNormals();
        int32 Pos = 0, Neg = 0;
        for (auto T : MD->Triangles().GetElementIDs())
        {
            auto V = MD->GetTriangleVertexInstances(T);
            auto X = P[MD->GetVertexInstanceVertex(V[0])], Y = P[MD->GetVertexInstanceVertex(V[1])],
                 Z = P[MD->GetVertexInstanceVertex(V[2])];
            float Dot = FVector3f::DotProduct(FVector3f::CrossProduct(Y - X, Z - X).GetSafeNormal(),
                                              (N[V[0]] + N[V[1]] + N[V[2]]).GetSafeNormal());
            if (Dot > .5)
                Pos++;
            if (Dot < -.5)
                Neg++;
        }
        auto R = MakeShared<FJsonObject>();
        R->SetStringField(TEXT("mesh"), M->GetPathName());
        R->SetNumberField(TEXT("cross_dot_normal_positive"), Pos);
        R->SetNumberField(TEXT("cross_dot_normal_negative"), Neg);
        Rows.Add(MakeShared<FJsonValueObject>(R));
    }
    auto O = MakeShared<FJsonObject>();
    O->SetArrayField(TEXT("meshes"), Rows);
    return Json06(O);
}
FString UVH06Tools::CorrectWinding()
{
    TSet<UStaticMesh *> Meshes;
    for (TActorIterator<AActor> I(GEditor->GetEditorWorldContext().World()); I; ++I)
    {
        TArray<UStaticMeshComponent *> Cs;
        I->GetComponents(Cs);
        for (auto *C : Cs)
            if (C->GetStaticMesh() && C->GetStaticMesh()->GetPathName().StartsWith(TEXT("/Game/Valhalla/Meshes/")))
                Meshes.Add(C->GetStaticMesh());
    }
    TArray<TSharedPtr<FJsonValue>> Rows;
    bool OK = true;
    auto Attributes = [](FMeshDescription &MD) {
        FStaticMeshAttributes A(MD);
        auto P = A.GetVertexPositions();
        auto N = A.GetVertexInstanceNormals();
        auto UV = A.GetVertexInstanceUVs();
        TArray<FString> Entries;
        for (auto T : MD.Triangles().GetElementIDs())
        {
            TArray<FString> C;
            for (auto VI : MD.GetTriangleVertexInstances(T))
            {
                auto X = P[MD.GetVertexInstanceVertex(VI)];
                auto Y = N[VI];
                auto U = UV.Get(VI, 0);
                C.Add(FString::Printf(TEXT("%.9g,%.9g,%.9g;%.9g,%.9g,%.9g;%.9g,%.9g"), X.X, X.Y, X.Z, Y.X, Y.Y, Y.Z,
                                      U.X, U.Y));
            }
            C.Sort();
            Entries.Add(FString::FromInt(MD.GetTrianglePolygonGroup(T).GetValue()) + TEXT(":") +
                        FString::Join(C, TEXT("|")));
        }
        Entries.Sort();
        FString S = FString::Join(Entries, TEXT("\n"));
        return FMD5::HashAnsiString(*S);
    };
    for (auto *M : Meshes)
    {
        FMeshDescription MD = *M->GetMeshDescription(0);
        FString Before = Attributes(MD);
        FStaticMeshAttributes A(MD);
        auto P = A.GetVertexPositions();
        auto N = A.GetVertexInstanceNormals();
        int32 Changed = 0;
        for (auto T : MD.Triangles().GetElementIDs())
        {
            auto V = MD.GetTriangleVertexInstances(T);
            auto X = P[MD.GetVertexInstanceVertex(V[0])], Y = P[MD.GetVertexInstanceVertex(V[1])],
                 Z = P[MD.GetVertexInstanceVertex(V[2])];
            float Dot = FVector3f::DotProduct(FVector3f::CrossProduct(Y - X, Z - X).GetSafeNormal(),
                                              (N[V[0]] + N[V[1]] + N[V[2]]).GetSafeNormal());
            if (Dot > .5)
            {
                MD.ReverseTriangleFacing(T);
                Changed++;
            }
        }
        FString After = Attributes(MD);
        OK &= Before == After;
        UStaticMesh::FBuildMeshDescriptionsParams Params;
        Params.bBuildSimpleCollision = false;
        M->BuildFromMeshDescriptions({&MD}, Params);
        M->ComplexCollisionMesh = nullptr;
        M->GetBodySetup()->InvalidatePhysicsData();
        M->GetBodySetup()->CreatePhysicsMeshes();
        OK &= Save06(M);
        auto R = MakeShared<FJsonObject>();
        R->SetStringField(TEXT("mesh"), M->GetPathName());
        R->SetNumberField(TEXT("triangles_reoriented"), Changed);
        R->SetBoolField(TEXT("positions_normals_uv_materials_unchanged"), Before == After);
        R->SetStringField(TEXT("attributes_before"), Before);
        R->SetStringField(TEXT("attributes_after"), After);
        Rows.Add(MakeShared<FJsonValueObject>(R));
    }
    auto O = MakeShared<FJsonObject>();
    O->SetBoolField(TEXT("ok"), OK);
    O->SetArrayField(TEXT("meshes"), Rows);
    return Json06(O);
}

FString UVH06Tools::SetStairCollision(UStaticMesh *Mesh)
{
    FBufferArchive BeforeBytes;
    Mesh->GetMeshDescription(0)->Serialize(BeforeBytes);
    FSHAHash BeforeHash;
    FSHA1::HashBuffer(BeforeBytes.GetData(), BeforeBytes.Num(), BeforeHash.Hash);
    auto *MD = Mesh->GetMeshDescription(0);
    FStaticMeshAttributes A(*MD);
    auto Pos = A.GetVertexPositions();
    float MinX = FLT_MAX, MaxX = -FLT_MAX;
    for (auto V : MD->Vertices().GetElementIDs())
    {
        MinX = FMath::Min(MinX, Pos[V].X);
        MaxX = FMath::Max(MaxX, Pos[V].X);
    }
    auto *B = Mesh->GetBodySetup();
    B->AggGeom.EmptyElements();
    for (int32 I = 0; I < 10; I++)
    {
        FKConvexElem C;
        for (float X : {MinX, MaxX})
            for (float Y : {-15.f * (I + 1), -15.f * I})
                for (float Z : {-200.f + 20.f * I, -180.f + 20.f * I})
                    C.VertexData.Add(FVector(X, Y, Z));
        C.UpdateElemBox();
        B->AggGeom.ConvexElems.Add(C);
    }
    B->CollisionTraceFlag = CTF_UseSimpleAndComplex;
    B->InvalidatePhysicsData();
    B->CreatePhysicsMeshes();
    Save06(Mesh);
    auto O = MakeShared<FJsonObject>();
    O->SetStringField(TEXT("mesh"), Mesh->GetPathName());
    O->SetNumberField(TEXT("convex_treads"), 10);
    O->SetNumberField(TEXT("local_riser_cm"), 15);
    O->SetNumberField(TEXT("local_tread_cm"), 20);
    FBufferArchive AfterBytes;
    Mesh->GetMeshDescription(0)->Serialize(AfterBytes);
    FSHAHash AfterHash;
    FSHA1::HashBuffer(AfterBytes.GetData(), AfterBytes.Num(), AfterHash.Hash);
    O->SetBoolField(TEXT("render_mesh_untouched"), BeforeHash == AfterHash);
    O->SetStringField(TEXT("before_surface"), BeforeHash.ToString());
    O->SetStringField(TEXT("after_surface"), AfterHash.ToString());
    return Json06(O);
}

#include "StaticMeshResources.h"
FString UVH06Tools::InspectFloor(float X, float Y)
{
    FinishCompilation();
    TArray<TSharedPtr<FJsonValue>> Rows;
    FVector Point(X, Y, 37);
    for (TActorIterator<AActor> I(GEditor->GetEditorWorldContext().World()); I; ++I)
    {
        TArray<UInstancedStaticMeshComponent *> Cs;
        I->GetComponents(Cs);
        for (auto *C : Cs)
        {
            UStaticMesh *M = C->GetStaticMesh();
            if (!M)
                continue;
            auto &L = M->GetRenderData()->LODResources[0];
            auto Ind = L.IndexBuffer.GetArrayView();
            for (int32 J = 0; J < C->GetInstanceCount(); J++)
            {
                FTransform T;
                C->GetInstanceTransform(J, T, true);
                for (int32 K = 0; K + 2 < Ind.Num(); K += 3)
                {
                    FVector V[3], N[3];
                    for (int32 A = 0; A < 3; A++)
                    {
                        V[A] = T.TransformPosition(
                            FVector(L.VertexBuffers.PositionVertexBuffer.VertexPosition(Ind[K + A])));
                        N[A] = T.TransformVectorNoScale(
                            FVector(L.VertexBuffers.StaticMeshVertexBuffer.VertexTangentZ(Ind[K + A])));
                    }
                    if (FMath::Abs(V[0].Z - 37) > .02 || FMath::Abs(V[1].Z - 37) > .02 || FMath::Abs(V[2].Z - 37) > .02)
                        continue;
                    if (FVector::CrossProduct(V[1] - V[0], V[2] - V[0]).SizeSquared() < 1e-8)
                        continue;
                    auto B = FMath::ComputeBaryCentric2D(Point, V[0], V[1], V[2]);
                    if (B.X < -.0001 || B.Y < -.0001 || B.Z < -.0001)
                        continue;
                    int32 Slot = -1;
                    for (auto &S : L.Sections)
                        if (K >= (int32)S.FirstIndex && K < (int32)(S.FirstIndex + S.NumTriangles * 3))
                            Slot = S.MaterialIndex;
                    auto R = MakeShared<FJsonObject>();
                    R->SetStringField(TEXT("component"), C->GetName());
                    R->SetStringField(TEXT("mesh"), M->GetPathName());
                    R->SetNumberField(TEXT("instance"), J);
                    R->SetNumberField(TEXT("triangle"), K / 3);
                    R->SetNumberField(TEXT("material_slot"), Slot);
                    R->SetStringField(TEXT("material"), GetPathNameSafe(C->GetMaterial(Slot)));
                    R->SetArrayField(TEXT("normal_world"), Vector06((N[0] + N[1] + N[2]) / 3));
                    R->SetArrayField(TEXT("geometric_cross_world"),
                                     Vector06(FVector::CrossProduct(V[1] - V[0], V[2] - V[0]).GetSafeNormal()));
                    Rows.Add(MakeShared<FJsonValueObject>(R));
                }
            }
        }
    }
    auto O = MakeShared<FJsonObject>();
    O->SetArrayField(TEXT("triangles"), Rows);
    return Json06(O);
}

#include "UObject/UObjectGlobals.h"
FString UVH06Tools::CorrectFloorFaces()
{
    FinishCompilation();
    TArray<TSharedPtr<FJsonValue>> Rows;
    auto Signature = [](FMeshDescription &MD) {
        FStaticMeshAttributes A(MD);
        auto P = A.GetVertexPositions();
        auto UV = A.GetVertexInstanceUVs();
        FBufferArchive Bytes;
        for (auto V : MD.Vertices().GetElementIDs())
        {
            auto X = P[V];
            Bytes << X;
        }
        for (auto VI : MD.VertexInstances().GetElementIDs())
        {
            auto U = UV.Get(VI, 0);
            Bytes << U;
        }
        for (auto T : MD.Triangles().GetElementIDs())
        {
            int32 G = MD.GetTrianglePolygonGroup(T).GetValue();
            Bytes << G;
        }
        FSHAHash H;
        FSHA1::HashBuffer(Bytes.GetData(), Bytes.Num(), H.Hash);
        return H.ToString();
    };
    for (TActorIterator<AActor> I(GEditor->GetEditorWorldContext().World()); I; ++I)
    {
        TArray<UInstancedStaticMeshComponent *> Cs;
        I->GetComponents(Cs);
        for (auto *C : Cs)
        {
            UStaticMesh *M = C->GetStaticMesh();
            if (!M || !M->GetPathName().StartsWith(TEXT("/Game/Valhalla/Meshes/")))
                continue;
            FMeshDescription MD = *M->GetMeshDescription(0);
            FStaticMeshAttributes A(MD);
            auto P = A.GetVertexPositions();
            auto N = A.GetVertexInstanceNormals();
            TSet<FTriangleID> Flip;
            for (int32 J = 0; J < C->GetInstanceCount(); J++)
            {
                FTransform Tr;
                C->GetInstanceTransform(J, Tr, true);
                for (auto T : MD.Triangles().GetElementIDs())
                {
                    auto V = MD.GetTriangleVertexInstances(T);
                    bool Ground = true;
                    for (auto VI : V)
                        Ground &=
                            FMath::Abs(Tr.TransformPosition(FVector(P[MD.GetVertexInstanceVertex(VI)])).Z - 37) < .02;
                    FVector Normal = Tr.TransformVectorNoScale(FVector(N[V[0]] + N[V[1]] + N[V[2]]) / 3);
                    if (Ground && Normal.Z < -.99)
                        Flip.Add(T);
                }
            }
            if (Flip.IsEmpty())
                continue;
            FString Before = Signature(MD);
            for (auto T : Flip)
            {
                for (auto VI : MD.GetTriangleVertexInstances(T))
                    N[VI] = -N[VI];
                MD.ReverseTriangleFacing(T);
            }
            FString After = Signature(MD);
            FString Path = TEXT("/Game/ValhallaV06/G/F") +
                           C->GetName().RightChop(FString(TEXT("InstancedStaticMeshComponent_")).Len());
            auto *Copy = DuplicateObject<UStaticMesh>(M, CreatePackage(*Path), *FPaths::GetBaseFilename(Path));
            Copy->SetFlags(RF_Public | RF_Standalone);
            FAssetRegistryModule::AssetCreated(Copy);
            UStaticMesh::FBuildMeshDescriptionsParams Params;
            Params.bBuildSimpleCollision = false;
            Copy->ReleaseResources();
            FlushRenderingCommands();
            Copy->BuildFromMeshDescriptions({&MD}, Params);
            Copy->GetBodySetup()->InvalidatePhysicsData();
            Copy->GetBodySetup()->CreatePhysicsMeshes();
            Save06(Copy);
            C->SetStaticMesh(Copy);
            auto R = MakeShared<FJsonObject>();
            R->SetStringField(TEXT("component"), C->GetName());
            R->SetStringField(TEXT("original_mesh"), M->GetPathName());
            R->SetStringField(TEXT("private_mesh"), Copy->GetPathName());
            R->SetNumberField(TEXT("floor_triangles_normal_and_facing_corrected"), Flip.Num());
            R->SetBoolField(TEXT("positions_uv_materials_unchanged"), Before == After);
            R->SetStringField(TEXT("before_positions_uv_materials"), Before);
            R->SetStringField(TEXT("after_positions_uv_materials"), After);
            Rows.Add(MakeShared<FJsonValueObject>(R));
        }
    }
    auto O = MakeShared<FJsonObject>();
    O->SetArrayField(TEXT("corrections"), Rows);
    return Json06(O);
}

#include "MaterialShared.h"
#include "Materials/MaterialRenderProxy.h"
#include "RHI.h"
#include "RenderingThread.h"
FString UVH06Tools::MaterialResourceSnapshot()
{
    auto O = MakeShared<FJsonObject>();
    O->SetBoolField(TEXT("valid_rhi"), !GUsingNullRHI);
    if (GUsingNullRHI)
        return Json06(O);
    FinishCompilation();
    FlushRenderingCommands();
    UWorld *W = GEditor->GetEditorWorldContext().World();
    auto Set = UsedInstancedMaterials(W);
    for (auto *M : Set)
        M->CacheShaders(EMaterialShaderPrecompileMode::Default);
    FinishCompilation();
    FlushRenderingCommands();
    TArray<UMaterial *> Mats;
    for (auto *M : Set)
        Mats.Add(M);
    TArray<bool> Missing, Defaults, CompleteActive;
    TArray<int32> ShaderCounts;
    ShaderCounts.Init(0, Set.Num());
    TArray<int32> ShaderFlags;
    ShaderFlags.Init(0, Set.Num());
    Missing.Init(false, Mats.Num());
    Defaults.Init(false, Mats.Num());
    CompleteActive.Init(false, Mats.Num());
    auto Feature = GMaxRHIFeatureLevel;
    O->SetNumberField(TEXT("world_feature_level"), (int32)W->GetFeatureLevel());
    O->SetNumberField(TEXT("active_rhi_feature_level"), (int32)Feature);
    O->SetNumberField(TEXT("active_shader_platform"), (int32)GMaxRHIShaderPlatform);
    ENQUEUE_RENDER_COMMAND(VH06MaterialResources)([Mats, Feature, &Missing, &Defaults, &CompleteActive, &ShaderFlags,
                                                   &ShaderCounts](FRHICommandListImmediate &Cmd) {
        for (int32 I = 0; I < Mats.Num(); I++)
        {
            auto *R = Mats[I]->GetRenderProxy()->GetMaterialNoFallback(Feature);
            Missing[I] = R == nullptr;
            Defaults[I] = R && R->IsDefaultMaterial();
            auto *ShaderMap = R ? R->GetRenderingThreadShaderMap() : nullptr;
            ShaderFlags[I] = (R ? 1 : 0) | (ShaderMap ? 2 : 0);
            if (ShaderMap)
                ShaderFlags[I] |= (ShaderMap->IsCompilationFinalized() ? 4 : 0) |
                                  (ShaderMap->CompiledSuccessfully() ? 8 : 0) |
                                  (ShaderMap->IsValidForRendering() ? 16 : 0);
            ShaderCounts[I] = ShaderMap ? ShaderMap->GetShaderNum() : 0;
            CompleteActive[I] = ShaderMap && ShaderMap->IsValidForRendering() && ShaderCounts[I] > 0;
        }
    });
    FlushRenderingCommands();
    TArray<TSharedPtr<FJsonValue>> Rows;
    bool Pending = GShaderCompilingManager && GShaderCompilingManager->IsCompiling();
    O->SetBoolField(TEXT("pending_shader_jobs"), Pending);
    bool OK = !Pending;
    for (int32 I = 0; I < Mats.Num(); I++)
    {
        auto *M = Mats[I];
        bool Complete = CompleteActive[I];
        auto R = MakeShared<FJsonObject>();
        R->SetStringField(TEXT("material"), M->GetPathName());
        R->SetBoolField(TEXT("shader_ready"), Complete);
        R->SetNumberField(TEXT("shader_count"), ShaderCounts[I]);
        R->SetNumberField(TEXT("shader_diagnostic_flags"), ShaderFlags[I]);
        R->SetBoolField(TEXT("render_resource_missing"), Missing[I]);
        R->SetBoolField(TEXT("render_resource_is_default"), Defaults[I]);
        OK &= Complete && !Missing[I] && !Defaults[I];
        Rows.Add(MakeShared<FJsonValueObject>(R));
    }
    O->SetBoolField(TEXT("ok"), OK);
    O->SetArrayField(TEXT("materials"), Rows);
    return Json06(O);
}

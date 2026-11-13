#include "HostSessionSubsystem.h"

#include "HostRuntime.h"
#include "Containers/StringConv.h"
#include "Engine/GameInstance.h"
#include "Engine/World.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformProcess.h"
#include "Misc/CommandLine.h"
#include "Misc/Parse.h"
#include "Misc/Paths.h"

namespace
{
TrekHostRequest Request(uint32 Operation, uint64 Generation = 0)
{
    TrekHostRequest Result{};
    Result.size = sizeof(Result);
    Result.operation = Operation;
    Result.generation = Generation;
    return Result;
}

TrekHostText Bytes(const FTCHARToUTF8& Text)
{
    return {Text.Get(), static_cast<uint32>(Text.Length()), 0};
}

bool IsTransition(uint32 Operation)
{
    return Operation == TREK_HOST_OPEN || Operation == TREK_HOST_RESTORE || Operation == TREK_HOST_CLOSE;
}

const TCHAR* OperationName(uint32 Operation)
{
    switch (Operation)
    {
    case TREK_HOST_OPEN: return TEXT("OPEN");
    case TREK_HOST_CLOSE: return TEXT("CLOSE");
    case TREK_HOST_QUERY_VIEW: return TEXT("VIEW");
    case TREK_HOST_SAVE: return TEXT("SAVE");
    case TREK_HOST_RESTORE: return TEXT("RESTORE");
    default: return TEXT("HOST");
    }
}
}

bool UHostWorldProjection::DoesSupportWorldType(EWorldType::Type Type) const
{
    return Type == EWorldType::Game || Type == EWorldType::PIE;
}

void UHostWorldProjection::OnWorldBeginPlay(UWorld& World)
{
    Super::OnWorldBeginPlay(World);
    if (UGameInstance* Game = World.GetGameInstance())
    {
        if (UHostSessionSubsystem* Host = Game->GetSubsystem<UHostSessionSubsystem>())
        {
            Host->Attach(*this);
        }
    }
}

void UHostWorldProjection::OnWorldEndPlay(UWorld& World)
{
    Detach();
    Super::OnWorldEndPlay(World);
}

void UHostWorldProjection::PreDeinitialize()
{
    Detach();
    Super::PreDeinitialize();
}

void UHostWorldProjection::Detach()
{
    if (UHostSessionSubsystem* Host = Session.Get())
    {
        Host->Detach(*this);
    }
    Invalidate();
}

void UHostWorldProjection::Invalidate()
{
    check(IsInGameThread());
    View.Reset();
    Completion.Reset();
    Message.Reset();
}

void UHostWorldProjection::Accept(const TrekHostCompletion& Result)
{
    check(IsInGameThread());
    Completion = Result;
    if (Result.operation == TREK_HOST_QUERY_VIEW)
    {
        View.Reset();
        if (Result.code == TREK_HOST_OK)
        {
            View = Result.output.view;
        }
    }
    Message = FString::Printf(TEXT("%s  %s"), OperationName(Result.operation), HostCodeName(Result.code));
}

void UHostSessionSubsystem::Initialize(FSubsystemCollectionBase& Collection)
{
    Super::Initialize(Collection);
    check(IsInGameThread());

    Api = FStarTrekRPGModule::Get().GetHostApi();
    if (!Api)
    {
        return;
    }

    // Normal game sessions use the current user's application data.
    // Unreal's process-level UserDir also lets automated runs isolate storage.
    FString UserDirOption;
    const FString UserDirectory = !FParse::Value(FCommandLine::Get(), TEXT("-UserDir="), UserDirOption)
        ? FPaths::Combine(FPlatformProcess::UserSettingsDir(), TEXT("StarTrekRPG"), TEXT("Saved"))
        : FPaths::ProjectSavedDir();
    FString Root = FPaths::ConvertRelativePathToFull(FPaths::Combine(UserDirectory, TEXT("HostSlots")));
    FPaths::MakePlatformFilename(Root);
    if (!IFileManager::Get().MakeDirectory(*Root, true) && !IFileManager::Get().DirectoryExists(*Root))
    {
        return;
    }

    const FTCHARToUTF8 RootUtf8(*Root);
    if (Api->Create(TREK_HOST_ABI_VERSION, RootUtf8.Get(), RootUtf8.Length(), &Client) == TREK_HOST_OK)
    {
        TickHandle = FTSTicker::GetCoreTicker().AddTicker(
            FTickerDelegate::CreateUObject(this, &UHostSessionSubsystem::Tick));
    }
}

void UHostSessionSubsystem::Deinitialize()
{
    check(IsInGameThread());
    if (TickHandle.IsValid())
    {
        FTSTicker::GetCoreTicker().RemoveTicker(TickHandle);
        TickHandle.Reset();
    }
    DiscardObservations();
    InvalidateProjections();
    for (const TWeakObjectPtr<UHostWorldProjection>& World : Worlds)
    {
        if (UHostWorldProjection* Projection = World.Get())
        {
            Projection->Session.Reset();
        }
    }
    Worlds.Reset();
    if (Client)
    {
        FStarTrekRPGModule::Get().RetireClient(Client);
        Client = nullptr;
    }
    Api = nullptr;
    Super::Deinitialize();
}

void UHostSessionSubsystem::Attach(UHostWorldProjection& World)
{
    check(IsInGameThread() && World.GetWorld()->GetGameInstance() == GetGameInstance());
    Worlds.AddUnique(&World);
    World.Session = this;
}

void UHostSessionSubsystem::Detach(UHostWorldProjection& World)
{
    check(IsInGameThread());
    for (int32 Index = Pending.Num() - 1; Index >= 0; --Index)
    {
        FObservation& Entry = Pending[Index];
        if (Entry.World.Get() == &World)
        {
            if (Entry.Ticket == Transition)
            {
                // The GameInstance retains the lifecycle operation across travel.
                Entry.World.Reset();
            }
            else
            {
                if (!Entry.Ready.IsSet()) Api->Discard(Client, Entry.Ticket);
                Pending.RemoveAtSwap(Index);
            }
        }
    }
    Worlds.Remove(&World);
    World.Session.Reset();
}

void UHostSessionSubsystem::InvalidateProjections()
{
    for (const TWeakObjectPtr<UHostWorldProjection>& World : Worlds)
    {
        if (UHostWorldProjection* Projection = World.Get())
        {
            Projection->Invalidate();
        }
    }
}

void UHostSessionSubsystem::DiscardObservations()
{
    for (const FObservation& Entry : Pending)
    {
        if (!Entry.Ready.IsSet()) Api->Discard(Client, Entry.Ticket);
    }
    Pending.Reset();
    Transition = 0;
}

bool UHostSessionSubsystem::RefreshStatus()
{
    TrekHostStatus Next{sizeof(TrekHostStatus)};
    if (Api->Status(Client, &Next) != TREK_HOST_OK)
    {
        return false;
    }
    if (Status.generation != Next.generation)
    {
        InvalidateProjections();
    }
    Status = Next;
    return true;
}

bool UHostSessionSubsystem::Tick(float)
{
    check(IsInGameThread());
    if (!RefreshStatus())
    {
        return true;
    }

    // Scan at most the ABI's fixed observation capacity per frame.
    for (int32 Index = 0; Index < Pending.Num();)
    {
        FObservation& Entry = Pending[Index];
        if (!Entry.Ready.IsSet())
        {
            TrekHostCompletion Result{};
            Result.size = sizeof(Result);
            const TrekHostCode Code = Api->Poll(Client, Entry.Ticket, &Result);
            if (Code == TREK_HOST_PENDING || Code == TREK_HOST_RETRY)
            {
                ++Index;
                continue;
            }
            if (Code != TREK_HOST_OK)
            {
                Result.code = Code;
            }
            Entry.Ready = Result;
        }

        // Publication can occur between the first status read and poll.
        // Keep the bounded completion until a fresh generation is available.
        if (!RefreshStatus())
        {
            break;
        }
        TrekHostCompletion Result = Entry.Ready.GetValue();
        if (Result.generation && Result.generation != Status.generation)
        {
            Result = {};
            Result.operation = Entry.Ready->operation;
            Result.code = TREK_HOST_GENERATION_EXPIRED;
        }
        if (Entry.Ticket == Transition)
        {
            Transition = 0;
        }
        if (Result.code == TREK_HOST_OK && Result.campaign[0])
        {
            CampaignAddress = UTF8_TO_TCHAR(Result.campaign);
        }
        if (UHostWorldProjection* World = Entry.World.Get(); World && World->Session.Get() == this)
        {
            World->Accept(Result);
        }
        Pending.RemoveAt(Index);
    }
    return true;
}

TrekHostCode UHostSessionSubsystem::Submit(UHostWorldProjection& World, const TrekHostRequest& Command)
{
    check(IsInGameThread());
    const uint32 Operation = Command.operation;
    TrekHostCode Code = TREK_HOST_SERVICE_UNAVAILABLE;
    if (Client && World.Session.Get() == this)
    {
        if (Pending.Num() >= TREK_HOST_ABI_MAX_PENDING && Operation != TREK_HOST_CLOSE)
        {
            Code = TREK_HOST_CAPACITY_LIMIT;
        }
        else if (Transition && Operation != TREK_HOST_CLOSE)
        {
            Code = TREK_HOST_BUSY_STATE;
        }
        else
        {
            uint64 Ticket = 0;
            Code = Api->Submit(Client, &Command, &Ticket);
            if (Code == TREK_HOST_OK)
            {
                if (IsTransition(Operation))
                {
                    DiscardObservations();
                    InvalidateProjections();
                    Transition = Ticket;
                }
                Pending.Add({Ticket, &World});
                World.Completion.Reset();
                World.Message = FString::Printf(TEXT("%s  PENDING"), OperationName(Operation));
                return Code;
            }
        }
    }
    TrekHostCompletion Rejection{};
    Rejection.operation = Operation;
    Rejection.code = Code;
    World.Accept(Rejection);
    return Code;
}

TrekHostCode UHostSessionSubsystem::Open(UHostWorldProjection& World)
{
    TrekHostRequest Command = Request(TREK_HOST_OPEN);
    // Fixed technical population for the diagnostic. H03 leaves it unbound.
    Command.input.population = {{"miranda", 7, 0}, 65001, 404, 8, 2, 1, 16};
    return Submit(World, Command);
}

TrekHostCode UHostSessionSubsystem::Close(UHostWorldProjection& World)
{
    return Submit(World, Request(TREK_HOST_CLOSE));
}

TrekHostCode UHostSessionSubsystem::Query(UHostWorldProjection& World)
{
    return Submit(World, Request(TREK_HOST_QUERY_VIEW, Status.generation));
}

TrekHostCode UHostSessionSubsystem::Save(UHostWorldProjection& World, const FString& Slot)
{
    const FTCHARToUTF8 SlotBytes(*Slot);
    TrekHostRequest Command = Request(TREK_HOST_SAVE, Status.generation);
    Command.input.slot = Bytes(SlotBytes);
    return Submit(World, Command);
}

TrekHostCode UHostSessionSubsystem::Restore(UHostWorldProjection& World, const FString& Campaign, const FString& Slot)
{
    const FTCHARToUTF8 CampaignBytes(*Campaign);
    const FTCHARToUTF8 SlotBytes(*Slot);
    TrekHostRequest Command = Request(TREK_HOST_RESTORE, Status.generation);
    Command.input.restore = {Bytes(CampaignBytes), Bytes(SlotBytes), 0};
    return Submit(World, Command);
}

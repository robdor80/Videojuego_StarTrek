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

#include <thread>

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

TrekHostAcademyRequest AcademyRequest(uint32 Operation, uint64 Generation = 0)
{
    TrekHostAcademyRequest Result{};
    Result.size = sizeof(Result);
    Result.version = TREK_HOST_ACADEMY_VERSION;
    Result.operation = Operation;
    Result.generation = Generation;
    return Result;
}

const TCHAR* AcademyOperationName(uint32 Operation)
{
    switch (Operation)
    {
    case TREK_HOST_ACADEMY_CREATE: return TEXT("ACADEMY CREATE");
    case TREK_HOST_ACADEMY_QUERY: return TEXT("ACADEMY QUERY");
    case TREK_HOST_ACADEMY_SLOTS: return TEXT("ACADEMY SLOTS");
    default: return TEXT("ACADEMY");
    }
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
    AcademyCandidate.Reset();
    AcademyPage.Reset();
    for (auto& Result : AcademyResults)
    {
        Result.Reset();
    }
    Message.Reset();
}

const TOptional<FHostAcademyResult>& UHostWorldProjection::GetAcademyResult(uint32 Operation) const
{
    check(Operation >= TREK_HOST_ACADEMY_CREATE && Operation <= TREK_HOST_ACADEMY_SLOTS);
    return AcademyResults[Operation];
}

void UHostWorldProjection::InvalidateCatalog()
{
    AcademyPage.Reset();
    AcademyResults[TREK_HOST_ACADEMY_SLOTS].Reset();
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

void UHostWorldProjection::Accept(const TrekHostAcademyCompletion& Result)
{
    check(IsInGameThread());
    AcademyResults[Result.operation] = FHostAcademyResult{Result.operation, Result.code, Result.ticket, Result.generation};
    if (Result.operation == TREK_HOST_ACADEMY_SLOTS)
    {
        AcademyPage.Reset();
        if (Result.code == TREK_HOST_OK)
        {
            AcademyPage.Emplace();
            FHostAcademyPage& Page = AcademyPage.GetValue();
            Page.Generation = Result.generation;
            Page.NextCursor = Result.output.slots.next_cursor;
            Page.Rows.Reserve(Result.output.slots.count);
            for (uint32 Index = 0; Index < Result.output.slots.count; ++Index)
            {
                const auto& Row = Result.output.slots.entries[Index];
                Page.Rows.Add({
                    UTF8_TO_TCHAR(Row.campaign), UTF8_TO_TCHAR(Row.slot), Row.version, Row.kind,
                    Row.format, Row.provenance, Row.reason, Row.compatible != 0,
                    Row.recoverable != 0 && Row.compatible != 0 && Row.reason == TREK_HOST_OK
                });
            }
        }
    }
    else
    {
        AcademyCandidate.Reset();
        if (Result.code == TREK_HOST_OK)
        {
            const auto& Candidate = Result.output.candidate;
            AcademyCandidate = FHostAcademyCandidate{
                UTF8_TO_TCHAR(Candidate.campaign), UTF8_TO_TCHAR(Candidate.display_name),
                UTF8_TO_TCHAR(Candidate.source_digest), Candidate.person, Candidate.creation_fact,
                Candidate.revision, Candidate.tick, Result.generation, Candidate.kind, Candidate.candidate_state
            };
        }
    }
    Message = FString::Printf(TEXT("%s  %s"), AcademyOperationName(Result.operation), HostCodeName(Result.code));
}

TrekHostCode UHostWorldProjection::RejectAcademy(uint32 Operation, TrekHostCode Code)
{
    AcademyResults[Operation] = FHostAcademyResult{Operation, Code};
    Message = FString::Printf(TEXT("%s  %s"), AcademyOperationName(Operation), HostCodeName(Code));
    return Code;
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
    TPromise<TrekHostClient*> Initialized;
    Creating = Initialized.GetFuture();
    std::thread([Native = Api, Root = MoveTemp(Root), Initialized = MoveTemp(Initialized)]() mutable
    {
        TrekHostClient* Result = nullptr;
        if (IFileManager::Get().MakeDirectory(*Root, true) || IFileManager::Get().DirectoryExists(*Root))
        {
            const FTCHARToUTF8 RootUtf8(*Root);
            if (Native->Create(TREK_HOST_ABI_VERSION, RootUtf8.Get(), RootUtf8.Length(), &Result) != TREK_HOST_OK)
            {
                Result = nullptr;
            }
        }
        Initialized.SetValue(Result);
    }).detach();
    TickHandle = FTSTicker::GetCoreTicker().AddTicker(
        FTickerDelegate::CreateUObject(this, &UHostSessionSubsystem::Tick));
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
    if (Client || Creating.IsValid())
    {
        FStarTrekRPGModule::RetireClient(MoveTemp(Api), Client, MoveTemp(Creating));
        Client = nullptr;
    }
    Api.Reset();
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
                Discard(Entry);
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

void UHostSessionSubsystem::InvalidateCatalog()
{
    for (const auto& World : Worlds)
    {
        if (UHostWorldProjection* Projection = World.Get())
        {
            Projection->InvalidateCatalog();
        }
    }
    for (int32 Index = Pending.Num() - 1; Index >= 0; --Index)
    {
        const FObservation& Entry = Pending[Index];
        if (Entry.IsCatalog())
        {
            if (UHostWorldProjection* Projection = Entry.World.Get(); Projection && Projection->Session.Get() == this)
            {
                TrekHostAcademyCompletion Expired{};
                Expired.operation = Entry.Operation;
                Expired.ticket = Entry.Ticket;
                Expired.code = TREK_HOST_GENERATION_EXPIRED;
                Projection->Accept(Expired);
            }
            Discard(Entry);
            Pending.RemoveAt(Index);
        }
    }
}

void UHostSessionSubsystem::Discard(const FObservation& Entry)
{
    if (!Entry.IsReady())
    {
        Api->Discard(Client, Entry.Ticket);
    }
}

void UHostSessionSubsystem::DiscardObservations()
{
    for (const FObservation& Entry : Pending)
    {
        Discard(Entry);
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

bool UHostSessionSubsystem::Poll(FObservation& Entry)
{
    if (Entry.IsReady())
    {
        return true;
    }
    TrekHostCode Code;
    if (Entry.bAcademy)
    {
        TrekHostAcademyCompletion Result{};
        Result.size = sizeof(Result);
        Code = Api->Academy.Poll(Client, Entry.Ticket, &Result);
        if (Code == TREK_HOST_OK)
        {
            if (Result.size != sizeof(Result) || Result.operation != Entry.Operation || Result.ticket != Entry.Ticket)
            {
                Result = {};
                Result.code = TREK_HOST_ABI_MISMATCH;
                Result.operation = Entry.Operation;
                Result.ticket = Entry.Ticket;
            }
            Entry.AcademyNativeResult = MakeUnique<TrekHostAcademyCompletion>(Result);
            return true;
        }
    }
    else
    {
        TrekHostCompletion Result{};
        Result.size = sizeof(Result);
        Code = Api->Poll(Client, Entry.Ticket, &Result);
        if (Code == TREK_HOST_OK)
        {
            Entry.NativeResult = Result;
            return true;
        }
    }

    if (Code == TREK_HOST_PENDING || Code == TREK_HOST_RETRY)
    {
        return false;
    }

    // Only transport OK consumes the observation. Release it on any terminal
    // transport failure and report the original ticket and operation.
    Discard(Entry);
    if (Entry.bAcademy)
    {
        Entry.AcademyNativeResult = MakeUnique<TrekHostAcademyCompletion>();
        Entry.AcademyNativeResult->code = Code;
        Entry.AcademyNativeResult->operation = Entry.Operation;
        Entry.AcademyNativeResult->ticket = Entry.Ticket;
    }
    else
    {
        TrekHostCompletion Result{};
        Result.code = Code;
        Result.operation = Entry.Operation;
        Result.ticket = Entry.Ticket;
        Entry.NativeResult = Result;
    }
    return true;
}

void UHostSessionSubsystem::Publish(FObservation& Entry)
{
    const bool bTransition = Entry.Ticket == Transition;
    if (bTransition)
    {
        Transition = 0;
    }

    UHostWorldProjection* World = Entry.World.Get();
    if (World && World->Session.Get() != this)
    {
        World = nullptr;
    }
    if (Entry.bAcademy)
    {
        auto& Result = *Entry.AcademyNativeResult;
        const uint64 Expected = Result.code == TREK_HOST_OK ? Result.generation : Entry.Generation;
        if ((!bTransition || Result.code == TREK_HOST_OK) && Expected != Status.generation)
        {
            Result.code = TREK_HOST_GENERATION_EXPIRED;
            Result.generation = 0;
        }
        if (Result.code == TREK_HOST_OK)
        {
            if (Entry.IsCatalog() && Result.output.slots.count > TREK_HOST_ACADEMY_MAX_SLOTS)
            {
                Result.code = TREK_HOST_ABI_MISMATCH;
                Result.generation = 0;
            }
            else if (Entry.Operation == TREK_HOST_ACADEMY_CREATE)
            {
                CampaignAddress = UTF8_TO_TCHAR(Result.output.candidate.campaign);
            }
        }
        if (World)
        {
            World->Accept(Result);
        }
        return;
    }
    auto& Result = Entry.NativeResult.GetValue();
    if ((Result.code == TREK_HOST_OK && Result.generation != Status.generation) ||
        (!bTransition && Entry.Generation != Status.generation))
    {
        Result = {};
        Result.operation = Entry.Operation;
        Result.ticket = Entry.Ticket;
        Result.code = TREK_HOST_GENERATION_EXPIRED;
    }
    if (Result.code == TREK_HOST_OK && Result.campaign[0])
    {
        CampaignAddress = UTF8_TO_TCHAR(Result.campaign);
        RetryCreationName.Reset();
    }
    if (World)
    {
        World->Accept(Result);
    }
}

bool UHostSessionSubsystem::Tick(float)
{
    check(IsInGameThread());
    if (Creating.IsValid())
    {
        if (!Creating.IsReady())
        {
            return true;
        }
        Client = Creating.Get();
        Creating = {};
    }
    if (!Client)
    {
        return false;
    }
    if (!RefreshStatus())
    {
        return true;
    }

    // Scan at most the ABI's fixed observation capacity per frame.
    for (int32 Index = 0; Index < Pending.Num();)
    {
        FObservation& Entry = Pending[Index];
        if (!Poll(Entry))
        {
            ++Index;
            continue;
        }

        // Publication can occur between the first status read and poll.
        // Keep the bounded completion until a fresh generation is available.
        if (!RefreshStatus())
        {
            break;
        }
        Publish(Entry);
        Pending.RemoveAt(Index);
    }
    return true;
}

TrekHostCode UHostSessionSubsystem::GetAcademyAvailability() const
{
    return Client ? Api->Academy.Availability : TREK_HOST_SERVICE_UNAVAILABLE;
}

TrekHostCode UHostSessionSubsystem::CheckAdmission(const UHostWorldProjection& World, bool bClosing) const
{
    check(IsInGameThread());
    if (!Client || World.Session.Get() != this)
    {
        return TREK_HOST_SERVICE_UNAVAILABLE;
    }
    if (!bClosing && Pending.Num() >= TREK_HOST_ABI_MAX_PENDING)
    {
        return TREK_HOST_CAPACITY_LIMIT;
    }
    if (Transition && !bClosing)
    {
        return TREK_HOST_BUSY_STATE;
    }
    return TREK_HOST_OK;
}

void UHostSessionSubsystem::Observe(UHostWorldProjection& World, uint64 Ticket, uint32 Operation,
                                   uint64 Generation, bool bAcademy, bool bTransition)
{
    if (bTransition)
    {
        DiscardObservations();
        InvalidateProjections();
        Transition = Ticket;
    }
    Pending.Add({Ticket, &World, Operation, Generation, bAcademy});
    if (bAcademy)
    {
        World.AcademyResults[Operation].Reset();
    }
    else
    {
        World.Completion.Reset();
    }
    World.Message = FString::Printf(TEXT("%s  PENDING"),
        bAcademy ? AcademyOperationName(Operation) : OperationName(Operation));
}

TrekHostCode UHostSessionSubsystem::Reject(UHostWorldProjection& World, uint32 Operation, TrekHostCode Code)
{
    if (World.Session.Get() == this)
    {
        TrekHostCompletion Rejection{};
        Rejection.operation = Operation;
        Rejection.code = Code;
        World.Accept(Rejection);
    }
    return Code;
}

TrekHostCode UHostSessionSubsystem::Submit(UHostWorldProjection& World, const TrekHostRequest& Command)
{
    const uint32 Operation = Command.operation;
    const TrekHostCode Admission = CheckAdmission(World, Operation == TREK_HOST_CLOSE);
    if (Admission != TREK_HOST_OK)
    {
        return Reject(World, Operation, Admission);
    }
    uint64 Ticket = 0;
    const TrekHostCode Code = Api->Submit(Client, &Command, &Ticket);
    if (Code != TREK_HOST_OK)
    {
        return Reject(World, Operation, Code);
    }
    if (Operation == TREK_HOST_CLOSE ||
        ((Operation == TREK_HOST_OPEN || Operation == TREK_HOST_RESTORE) && Status.generation == 0))
    {
        RetryCreationName.Reset();
    }
    if (Operation == TREK_HOST_SAVE)
    {
        InvalidateCatalog();
    }
    Observe(World, Ticket, Operation, Command.generation, false, IsTransition(Operation));
    return Code;
}

TrekHostCode UHostSessionSubsystem::Submit(UHostWorldProjection& World, const TrekHostAcademyRequest& Command)
{
    const uint32 Operation = Command.operation;
    if (World.Session.Get() != this)
    {
        return TREK_HOST_SERVICE_UNAVAILABLE;
    }
    TrekHostCode Code = GetAcademyAvailability();
    if (Code == TREK_HOST_OK)
    {
        Code = CheckAdmission(World, false);
        if (Code == TREK_HOST_OK && Pending.ContainsByPredicate([&](const FObservation& Entry)
            { return Entry.bAcademy && Entry.Operation == Operation && Entry.World.Get() == &World; }))
        {
            Code = TREK_HOST_BUSY_STATE;
        }
    }
    if (Code != TREK_HOST_OK)
    {
        return World.RejectAcademy(Operation, Code);
    }
    uint64 Ticket = 0;
    Code = Api->Academy.Submit(Client, &Command, &Ticket);
    if (Code != TREK_HOST_OK)
    {
        if (Operation == TREK_HOST_ACADEMY_SLOTS && Code == TREK_HOST_GENERATION_EXPIRED)
        {
            World.InvalidateCatalog();
        }
        return World.RejectAcademy(Operation, Code);
    }
    if (Operation == TREK_HOST_ACADEMY_SLOTS)
    {
        World.AcademyPage.Reset();
    }
    Observe(World, Ticket, Operation, Command.generation, true, Operation == TREK_HOST_ACADEMY_CREATE);
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
    return Restore(World, Campaign, Slot, 0);
}

TrekHostCode UHostSessionSubsystem::Restore(UHostWorldProjection& World, const FString& Campaign,
                                           const FString& Slot, uint64 Version)
{
    const FTCHARToUTF8 CampaignBytes(*Campaign);
    const FTCHARToUTF8 SlotBytes(*Slot);
    TrekHostRequest Command = Request(TREK_HOST_RESTORE, Status.generation);
    Command.input.restore = {Bytes(CampaignBytes), Bytes(SlotBytes), Version};
    return Submit(World, Command);
}

TrekHostCode UHostSessionSubsystem::CreateAcademy(UHostWorldProjection& World, const FString& Name)
{
    check(IsInGameThread());
    if (World.Session.Get() != this)
    {
        return TREK_HOST_SERVICE_UNAVAILABLE;
    }
    if (Name.IsEmpty() || Name.Len() > static_cast<int32>(TREK_HOST_ACADEMY_NAME_BYTES))
    {
        return World.RejectAcademy(TREK_HOST_ACADEMY_CREATE, TREK_HOST_INVALID_ARGUMENT);
    }
    const bool bReplay = !RetryCreationName.IsEmpty();
    if (bReplay && !RetryCreationName.Equals(Name, ESearchCase::CaseSensitive))
    {
        return World.RejectAcademy(TREK_HOST_ACADEMY_CREATE, TREK_HOST_IDEMPOTENCY_CONFLICT);
    }
    if (!bReplay && LastCreationKey == MAX_uint64)
    {
        return World.RejectAcademy(TREK_HOST_ACADEMY_CREATE, TREK_HOST_CAPACITY_LIMIT);
    }

    // A caller may pass a name from a projection that admission invalidates.
    FString SubmittedName = Name;
    const FTCHARToUTF8 NameBytes(*SubmittedName, SubmittedName.Len());
    TrekHostAcademyRequest Command = AcademyRequest(TREK_HOST_ACADEMY_CREATE);
    Command.creation_key = bReplay ? LastCreationKey : LastCreationKey + 1;
    Command.display_name = Bytes(NameBytes);
    const TrekHostCode Code = Submit(World, Command);
    if (Code == TREK_HOST_OK && !bReplay)
    {
        LastCreationKey = Command.creation_key;
        RetryCreationName = MoveTemp(SubmittedName);
    }
    return Code;
}

TrekHostCode UHostSessionSubsystem::QueryAcademy(UHostWorldProjection& World)
{
    return Submit(World, AcademyRequest(TREK_HOST_ACADEMY_QUERY, Status.generation));
}

TrekHostCode UHostSessionSubsystem::ListAcademySlots(UHostWorldProjection& World, uint32 Cursor)
{
    check(IsInGameThread());
    if (World.Session.Get() != this)
    {
        return TREK_HOST_SERVICE_UNAVAILABLE;
    }
    if (Cursor && (!World.AcademyPage.IsSet() || World.AcademyPage->NextCursor != Cursor ||
                   World.AcademyPage->Generation != Status.generation))
    {
        return World.RejectAcademy(TREK_HOST_ACADEMY_SLOTS, TREK_HOST_GENERATION_EXPIRED);
    }
    TrekHostAcademyRequest Command = AcademyRequest(TREK_HOST_ACADEMY_SLOTS, Status.generation);
    Command.slot_cursor = Cursor;
    return Submit(World, Command);
}

TrekHostCode UHostSessionSubsystem::RestoreAcademy(UHostWorldProjection& World, const FHostAcademySlot& Version)
{
    check(IsInGameThread());
    const TrekHostCode Availability = GetAcademyAvailability();
    if (Availability != TREK_HOST_OK)
    {
        return Reject(World, TREK_HOST_RESTORE, Availability);
    }
    if (Version.Reason != TREK_HOST_OK)
    {
        return Reject(World, TREK_HOST_RESTORE, Version.Reason);
    }
    if (Version.Kind != TREK_HOST_KIND_ACADEMY || !Version.Version || !Version.bCompatible || !Version.bRecoverable)
    {
        return Reject(World, TREK_HOST_RESTORE, TREK_HOST_SAVE_INCOMPATIBLE);
    }
    if (Status.state != TREK_HOST_CLOSED)
    {
        return Reject(World, TREK_HOST_RESTORE, TREK_HOST_BUSY_STATE);
    }
    // The row is a read projection. H04 validates this exact address afresh.
    return Restore(World, Version.Campaign, Version.Slot, Version.Version);
}

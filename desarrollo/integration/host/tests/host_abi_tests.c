#include "trek/host/host_abi.h"

#include <inttypes.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
# include <windows.h>
static void pause_poll(void) { Sleep(1); }
#else
# include <time.h>
static void pause_poll(void)
{
    const struct timespec pause = {0, 1000000};
    nanosleep(&pause, NULL);
}
#endif

_Static_assert(sizeof(TrekHostRequest) == 80, "Request layout");
_Static_assert(sizeof(TrekHostCompletion) == 120, "Completion layout");
_Static_assert(sizeof(TrekHostStatus) == 24, "Status layout");
_Static_assert(offsetof(TrekHostCompletion, output) == 72, "Payload offset");

static void check(int condition, const char* message)
{
    if (!condition) {
        fprintf(stderr, "FAIL: %s\n", message);
        exit(EXIT_FAILURE);
    }
}

static void expect(TrekHostCode code, TrekHostCode expected, const char* action)
{
    if (code != expected) {
        fprintf(stderr, "FAIL: %s returned %" PRIu32 ", expected %" PRIu32 "\n", action, code, expected);
        exit(EXIT_FAILURE);
    }
}

static TrekHostText text(const char* value)
{
    return (TrekHostText){value, (uint32_t)strlen(value), 0};
}

static TrekHostRequest request(uint32_t op, uint64_t generation)
{
    return (TrekHostRequest){.size = sizeof(TrekHostRequest), .operation = op, .generation = generation};
}

static TrekHostClient* create(const char* root)
{
    TrekHostClient* client = NULL;
    expect(trek_host_create(TREK_HOST_ABI_VERSION, root, (uint32_t)strlen(root), &client),
           TREK_HOST_OK, "create");
    check(client != NULL, "client not allocated");
    return client;
}

static TrekHostStatus status(TrekHostClient* client)
{
    TrekHostStatus out = {.size = sizeof(out)};
    for (int i = 0; i < 10000; ++i) {
        TrekHostCode code = trek_host_status(client, &out);
        if (code == TREK_HOST_RETRY) {
            pause_poll();
            continue;
        }
        expect(code, TREK_HOST_OK, "status");
        return out;
    }
    check(0, "status timed out");
    return out;
}

static TrekHostCode submit(TrekHostClient* client, TrekHostRequest req, uint64_t* ticket)
{
    for (int i = 0; i < 10000; ++i) {
        const TrekHostCode code = trek_host_submit(client, &req, ticket);
        if (code != TREK_HOST_RETRY) return code;
        check(*ticket == 0, "retry admitted a ticket");
        pause_poll();
    }
    check(0, "submit timed out");
    return TREK_HOST_INTERNAL_ERROR;
}

static uint64_t enqueue(TrekHostClient* client, TrekHostRequest req)
{
    uint64_t ticket = 0;
    expect(submit(client, req, &ticket), TREK_HOST_OK, "submit");
    check(ticket != 0, "missing ticket");
    return ticket;
}

static TrekHostCompletion finish(TrekHostClient* client, uint64_t ticket, TrekHostCode expected)
{
    TrekHostCompletion out = {.size = sizeof(out)};
    for (int i = 0; i < 10000; ++i) {
        const TrekHostCode code = trek_host_poll(client, ticket, &out);
        if (code == TREK_HOST_RETRY || code == TREK_HOST_PENDING) {
            check(out.ticket == 0, "pending poll modified output");
            pause_poll();
            continue;
        }
        expect(code, TREK_HOST_OK, "poll");
        expect(out.code, expected, "completion");
        check(out.ticket == ticket && out.size == sizeof(out), "completion metadata");
        if (expected != TREK_HOST_OK) {
            const unsigned char zero[sizeof(out.output)] = {0};
            check(!out.generation && !out.campaign[0] &&
                  memcmp(&out.output, zero, sizeof(zero)) == 0, "failed operation exposed payload");
        }
        expect(trek_host_poll(client, ticket, &out), TREK_HOST_UNKNOWN_TICKET, "poll twice");
        return out;
    }
    check(0, "poll timed out");
    return out;
}

static TrekHostCompletion run(TrekHostClient* client, TrekHostRequest req, TrekHostCode expected)
{
    TrekHostCompletion out = finish(client, enqueue(client, req), expected);
    check(out.operation == req.operation, "lost operation");
    return out;
}

static TrekHostRequest open_request(const char* class_id)
{
    TrekHostRequest req = request(TREK_HOST_OPEN, 0);
    req.input.population = (TrekHostPopulation){text(class_id), 65001, 404, 8, 2, 1, 16};
    return req;
}

static void lifecycle(void)
{
    TrekHostClient* client = NULL;
    expect(trek_host_abi_version(), TREK_HOST_ABI_VERSION, "version");
    expect(trek_host_create(2, NULL, 0, &client), TREK_HOST_ABI_MISMATCH, "wrong version");
    check(!client, "failed create published handle");
    expect(trek_host_create(1, NULL, 1, &client), TREK_HOST_INVALID_ARGUMENT, "missing path bytes");
    client = create("");
    TrekHostClient* other = create("");
    TrekHostStatus wrong_size = {.size = sizeof(wrong_size) - 1};
    expect(trek_host_status(client, &wrong_size), TREK_HOST_ABI_MISMATCH, "status size");
    uint64_t ticket = UINT64_MAX;
    TrekHostRequest open = open_request("miranda");
    open.size--;
    expect(trek_host_submit(client, &open, &ticket), TREK_HOST_ABI_MISMATCH, "request size");
    check(!ticket, "invalid request admitted");
    open = open_request("miranda");
    open.input.population.class_id = (TrekHostText){"mir\0anda", 8, 0};
    expect(trek_host_submit(client, &open, &ticket), TREK_HOST_INVALID_ARGUMENT, "embedded NUL");

    char temporary[] = {'m','i','r','a','n','d','a'};
    open.input.population.class_id = (TrekHostText){temporary, sizeof(temporary), 0};
    ticket = enqueue(client, open);
    memset(temporary, 'x', sizeof(temporary));
    TrekHostCompletion wrong_output = {.size = sizeof(wrong_output) - 1};
    expect(trek_host_poll(client, ticket, &wrong_output), TREK_HOST_ABI_MISMATCH, "poll size");
    const TrekHostCompletion opened = finish(client, ticket, TREK_HOST_OK);
    check(opened.generation && strlen(opened.campaign) == 32, "OPEN identity missing");
    const TrekHostStatus active = status(client);
    check(active.state == TREK_HOST_ACTIVE && active.generation == opened.generation, "OPEN not active");
    expect(active.principal, TREK_HOST_PRINCIPAL_UNBOUND, "no bootstrap");
    expect(active.institutional, TREK_HOST_SERVICE_UNAVAILABLE, "F11 capability");

    open = open_request("miranda");
    run(client, open, TREK_HOST_BUSY_STATE);
    run(other, open, TREK_HOST_BUSY_STATE);
    TrekHostRequest view = request(TREK_HOST_QUERY_VIEW, opened.generation);
    expect(submit(other, view, &ticket), TREK_HOST_GENERATION_EXPIRED, "foreign generation");
    run(client, view, TREK_HOST_PRINCIPAL_UNBOUND);
    run(client, request(TREK_HOST_SUBMIT_SCAN, opened.generation), TREK_HOST_PRINCIPAL_UNBOUND);
    TrekHostRequest save = request(TREK_HOST_SAVE, opened.generation);
    save.input.slot = text("alpha");
    run(client, save, TREK_HOST_PRINCIPAL_UNBOUND);

    uint64_t pending[TREK_HOST_ABI_MAX_PENDING];
    for (size_t i = 0; i < TREK_HOST_ABI_MAX_PENDING; ++i) pending[i] = enqueue(client, view);
    expect(submit(client, view, &ticket), TREK_HOST_CAPACITY_LIMIT, "poll capacity");
    expect(trek_host_discard(client, pending[0]), TREK_HOST_OK, "discard");
    TrekHostCompletion out = {.size = sizeof(out)};
    expect(trek_host_poll(client, pending[0], &out), TREK_HOST_UNKNOWN_TICKET, "discard revoked delivery");
    pending[0] = enqueue(client, view);
    run(client, request(TREK_HOST_CLOSE, 0), TREK_HOST_OK);
    for (size_t i = 0; i < TREK_HOST_ABI_MAX_PENDING; ++i)
        finish(client, pending[i], TREK_HOST_GENERATION_EXPIRED);
    expect(submit(client, view, &ticket), TREK_HOST_GENERATION_EXPIRED, "old token after close");
    check(status(client).state == TREK_HOST_CLOSED, "close failed");
    const TrekHostCompletion reopened = run(other, open, TREK_HOST_OK);
    check(reopened.generation != opened.generation, "generation reused across clients");
    trek_host_destroy(other); /* Non-Game Thread, active worker cleanup. */
    run(client, open, TREK_HOST_OK);
    run(client, request(TREK_HOST_CLOSE, 0), TREK_HOST_OK);
    trek_host_destroy(client);
    puts("PASS ABI lifecycle, product exclusivity, unbound, capacity and late results after CLOSE");
}

static TrekHostRequest restore(uint64_t generation, const char* campaign, const char* slot)
{
    TrekHostRequest req = request(TREK_HOST_RESTORE, generation);
    req.input.restore = (TrekHostSlot){text(campaign), text(slot), 0};
    return req;
}

static void roundtrip(int argc, char** argv)
{
    check(argc == 12, "fixture arguments");
    const char* root = argv[2];
    const char* campaign = argv[3];
    const uint64_t order = strtoull(argv[4], NULL, 10);
    const uint64_t person = strtoull(argv[5], NULL, 10);
    TrekHostScan scan = {0};
    scan.recipient = strtoull(argv[6], NULL, 10);
    scan.station = strtoull(argv[7], NULL, 10);
    scan.key = strtoull(argv[8], NULL, 10);
    scan.expected_revision = strtoull(argv[9], NULL, 10);
    scan.deadline = strtoull(argv[10], NULL, 10);
    scan.cause = strtoull(argv[11], NULL, 10);

    TrekHostClient* client = create(root);
    const TrekHostCompletion loaded = run(client, restore(0, campaign, "alpha"), TREK_HOST_OK);
    const uint64_t generation = loaded.generation;
    check(generation && strcmp(loaded.campaign, campaign) == 0, "RESTORE wrong campaign");
    expect(status(client).principal, TREK_HOST_OK, "H04 restored binding");
    TrekHostRequest view = request(TREK_HOST_QUERY_VIEW, generation);
    const TrekHostCampaignView before = run(client, view, TREK_HOST_OK).output.view;
    check(before.person == person && before.ship && before.revision && before.tick == 28800,
          "wrong authorized campaign view");
    TrekHostRequest query = request(TREK_HOST_QUERY_ORDER, generation);
    query.input.order.id = order;
    const TrekHostOrderView completed = run(client, query, TREK_HOST_OK).output.order;
    check(completed.order == order && completed.state == TREK_HOST_COMPLETED &&
          completed.result && completed.performed && completed.value >= 1 && completed.value <= 100,
          "fixture Core result not recovered");

    TrekHostRequest action = request(TREK_HOST_SUBMIT_SCAN, generation);
    action.input.scan = scan;
    const TrekHostOrderView replay = run(client, action, TREK_HOST_OK).output.order;
    check(replay.order == order && replay.key == scan.key, "replay duplicated fixture order");
    TrekHostCampaignView repeated = run(client, view, TREK_HOST_OK).output.view;
    check(memcmp(&before, &repeated, sizeof(before)) == 0, "query/replay changed projection");

    action.input.scan.key++;
    action.input.scan.expected_revision = before.revision - 1;
    run(client, action, TREK_HOST_REVISION_STALE);
    {
        action.input.scan.key++;
        action.input.scan.expected_revision = run(client, view, TREK_HOST_OK).output.view.revision;
        const TrekHostOrderView issued = run(client, action, TREK_HOST_OK).output.order;
        check(issued.order && issued.order != order && issued.key == action.input.scan.key &&
              issued.state == TREK_HOST_ISSUED && !issued.result && !issued.performed,
              "scan issuance did not return genuine ISSUED");
        query.input.order.id = issued.order;
        TrekHostRequest cancel = request(TREK_HOST_CANCEL_ORDER, generation);
        cancel.input.order = (TrekHostOrderRef){issued.order, issued.revision};
        const TrekHostOrderView cancelled = run(client, cancel, TREK_HOST_OK).output.order;
        check(cancelled.order == issued.order && cancelled.state == TREK_HOST_CANCELLED &&
              cancelled.key == 0, "cancel receipt mismatch");
        check(run(client, query, TREK_HOST_OK).output.order.state == TREK_HOST_CANCELLED, "cancel not persisted in Core");
    }

    TrekHostRequest save = request(TREK_HOST_SAVE, generation);
    save.input.slot = text("../alpha");
    run(client, save, TREK_HOST_PATH_REJECTED);
    run(client, restore(generation, campaign, "missing"), TREK_HOST_PATH_REJECTED);
    check(status(client).generation == generation, "failed LOAD changed generation");
    save.input.slot = text("h06");
    run(client, save, TREK_HOST_OK);
    const TrekHostCampaignView saved = run(client, view, TREK_HOST_OK).output.view;
    query.input.order.id = order;
    const TrekHostOrderView saved_order = run(client, query, TREK_HOST_OK).output.order;
    check(saved_order.result == completed.result && saved_order.value == completed.value,
          "unrelated mutations changed the completed result");
    const uint64_t late = enqueue(client, view);
    const TrekHostCompletion reloaded = run(client, restore(generation, campaign, "h06"), TREK_HOST_OK);
    check(reloaded.generation != generation, "LOAD did not renew generation");
    finish(client, late, TREK_HOST_GENERATION_EXPIRED);
    uint64_t rejected = UINT64_MAX;
    expect(submit(client, view, &rejected), TREK_HOST_GENERATION_EXPIRED, "old query after LOAD");
    expect(submit(client, action, &rejected), TREK_HOST_GENERATION_EXPIRED, "old mutation after LOAD");
    view.generation = reloaded.generation;
    const TrekHostCampaignView after = run(client, view, TREK_HOST_OK).output.view;
    check(memcmp(&saved, &after, sizeof(saved)) == 0, "SAVE/RESTORE lost identity, clock or revision");
    query.generation = reloaded.generation;
    query.input.order.id = order;
    const TrekHostOrderView restored = run(client, query, TREK_HOST_OK).output.order;
    check(memcmp(&saved_order, &restored, sizeof(restored)) == 0, "SAVE/RESTORE lost Core result");
    const uint64_t late_close = enqueue(client, query);
    run(client, request(TREK_HOST_CLOSE, 0), TREK_HOST_OK);
    finish(client, late_close, TREK_HOST_GENERATION_EXPIRED);
    trek_host_destroy(client);
    printf("PASS ABI H04/F05 FIXTURE, person=%" PRIu64 ", Core result=%" PRIu64 "\n", person, restored.result);
}

int main(int argc, char** argv)
{
    if (argc == 1) lifecycle();
    else roundtrip(argc, argv);
    return EXIT_SUCCESS;
}

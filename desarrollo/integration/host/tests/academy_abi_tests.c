#include "trek/host/academy_abi.h"

#include <inttypes.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#include <windows.h>
static void pause_poll(void) { Sleep(1); }
#else
#include <time.h>
static void pause_poll(void) { const struct timespec t = {0, 1000000}; nanosleep(&t, NULL); }
#endif

_Static_assert(sizeof(TrekHostRequest) == 80 && sizeof(TrekHostCompletion) == 120, "v1 frozen");
_Static_assert(sizeof(TrekHostAcademyRequest) == 48, "extension request");
_Static_assert(sizeof(TrekHostAcademyCompletion) == 6696, "extension completion");
_Static_assert(offsetof(TrekHostAcademyCompletion, output) == 32, "extension output");

static void check(int ok, const char* message)
{
    if (!ok) { fprintf(stderr, "FAIL: %s\n", message); exit(1); }
}
static void expect(TrekHostCode actual, TrekHostCode expected)
{
    if (actual != expected) { fprintf(stderr, "Code %u, expected %u\n", actual, expected); exit(1); }
}
static TrekHostText text(const char* s) { return (TrekHostText){s, (uint32_t)strlen(s), 0}; }
static TrekHostClient* client(const char* root)
{
    TrekHostClient* c = NULL;
    expect(trek_host_create(1, root, (uint32_t)strlen(root), &c), TREK_HOST_OK);
    return c;
}
static TrekHostAcademyRequest req(uint32_t op, uint64_t generation)
{
    return (TrekHostAcademyRequest){.size=sizeof(TrekHostAcademyRequest), .version=1,
                                  .operation=op, .generation=generation};
}
static TrekHostAcademyRequest creation(uint64_t key, const char* name)
{
    TrekHostAcademyRequest r = req(TREK_HOST_ACADEMY_CREATE, 0);
    r.creation_key = key; r.display_name = text(name); return r;
}
static TrekHostCode submit(TrekHostClient* c, TrekHostAcademyRequest r, uint64_t* ticket)
{
    for (int i=0; i<30000; ++i) {
        TrekHostCode code = trek_host_academy_submit(c, &r, ticket);
        if (code != TREK_HOST_RETRY) return code;
        check(*ticket == 0, "RETRY admitted ticket"); pause_poll();
    }
    check(0, "submit timeout"); return TREK_HOST_INTERNAL_ERROR;
}
static uint64_t enqueue(TrekHostClient* c, TrekHostAcademyRequest r)
{
    uint64_t ticket=0; expect(submit(c,r,&ticket),TREK_HOST_OK); check(ticket!=0,"ticket"); return ticket;
}
static TrekHostAcademyCompletion finish(TrekHostClient* c, uint64_t ticket, TrekHostCode expected)
{
    TrekHostAcademyCompletion out = {.size=sizeof(out)};
    for (int i=0; i<30000; ++i) {
        TrekHostCode code = trek_host_academy_poll(c,ticket,&out);
        if (code==TREK_HOST_PENDING || code==TREK_HOST_RETRY) { check(!out.ticket,"pending output"); pause_poll(); continue; }
        expect(code,TREK_HOST_OK); expect(out.code,expected);
        check(out.ticket==ticket,"ticket correlation");
        if (expected!=TREK_HOST_OK) {
            const unsigned char zero[sizeof(out.output)]={0};
            check(!out.generation && !memcmp(&out.output,zero,sizeof(zero)),"error leaked payload");
        }
        expect(trek_host_academy_poll(c,ticket,&out),TREK_HOST_UNKNOWN_TICKET);
        return out;
    }
    check(0,"poll timeout"); return out;
}
static TrekHostAcademyCompletion run(TrekHostClient* c,TrekHostAcademyRequest r,TrekHostCode expected)
{ return finish(c,enqueue(c,r),expected); }
static uint64_t old_enqueue(TrekHostClient* c,TrekHostRequest r)
{
    uint64_t ticket=0;
    for(int i=0;i<30000;++i) {
        TrekHostCode code=trek_host_submit(c,&r,&ticket);
        if(code==TREK_HOST_RETRY){pause_poll();continue;}
        expect(code,TREK_HOST_OK);return ticket;
    }
    check(0,"v1 submit timeout"); return 0;
}
static TrekHostCompletion old_finish(TrekHostClient* c,uint64_t ticket,TrekHostCode expected)
{
    TrekHostCompletion out={.size=sizeof(out)};
    for(int i=0;i<30000;++i) {
        TrekHostCode code=trek_host_poll(c,ticket,&out);
        if(code==TREK_HOST_PENDING || code==TREK_HOST_RETRY){pause_poll();continue;}
        expect(code,TREK_HOST_OK);expect(out.code,expected);return out;
    }
    check(0,"v1 poll timeout");return out;
}
static TrekHostRequest old_req(uint32_t op,uint64_t gen)
{ return (TrekHostRequest){.size=sizeof(TrekHostRequest),.operation=op,.generation=gen}; }
static void close_session(TrekHostClient* c)
{ old_finish(c,old_enqueue(c,old_req(TREK_HOST_CLOSE,0)),TREK_HOST_OK); }
static TrekHostStatus status(TrekHostClient* c)
{
    TrekHostStatus s={.size=sizeof(s)};
    for(int i=0;i<30000;++i) {
        TrekHostCode code=trek_host_status(c,&s);
        if(code==TREK_HOST_RETRY){pause_poll();continue;}
        expect(code,TREK_HOST_OK);return s;
    }
    check(0,"status timeout");return s;
}
static void same(const TrekHostAcademyView* a,const TrekHostAcademyView* b)
{
    check(!memcmp(a,b,sizeof(*a)),"identity or Core state changed");
    check(a->person && a->creation_fact && a->kind==TREK_HOST_KIND_ACADEMY &&
          a->candidate_state==TREK_HOST_CANDIDATE,"real candidate projection");
}
static void deny_naval(TrekHostClient* c,uint64_t gen)
{
    const uint32_t ops[]={TREK_HOST_QUERY_VIEW,TREK_HOST_SUBMIT_SCAN,TREK_HOST_QUERY_ORDER,TREK_HOST_CANCEL_ORDER};
    for(unsigned i=0;i<sizeof(ops)/sizeof(ops[0]);++i)
        old_finish(c,old_enqueue(c,old_req(ops[i],gen)),TREK_HOST_ACCESS_DENIED);
}
static void lifecycle(void)
{
    expect(trek_host_abi_version(),1);expect(trek_host_academy_version(),1);
    TrekHostClient* c=client(""); uint64_t ticket=0;
    TrekHostAcademyRequest bad=creation(1,"Aren");bad.version=2;
    expect(submit(c,bad,&ticket),TREK_HOST_ABI_MISMATCH);check(!ticket,"bad version ticket");
    bad=creation(1,"Aren");bad.size--;
    expect(submit(c,bad,&ticket),TREK_HOST_ABI_MISMATCH);
    bad=creation(1,"Aren");bad.reserved=1;
    expect(submit(c,bad,&ticket),TREK_HOST_INVALID_ARGUMENT);
    bad=creation(1,"Aren");bad.display_name.reserved=1;
    expect(submit(c,bad,&ticket),TREK_HOST_INVALID_ARGUMENT);
    bad=creation(0,"Aren");expect(submit(c,bad,&ticket),TREK_HOST_INVALID_ARGUMENT);
    const char* invalid[]={""," ","A\nB","\xc0\xaf","\xed\xa0\x80","\xf4\x90\x80\x80","\xe2\x80\xae"};
    for(unsigned i=0;i<sizeof(invalid)/sizeof(invalid[0]);++i)
        expect(submit(c,creation(1,invalid[i]),&ticket),TREK_HOST_INVALID_ARGUMENT);
    bad=creation(1,"Aren");bad.display_name=(TrekHostText){"A\0ren",5,0};
    expect(submit(c,bad,&ticket),TREK_HOST_INVALID_ARGUMENT);
    char long_name[98];memset(long_name,'A',97);long_name[97]=0;
    expect(submit(c,creation(1,long_name),&ticket),TREK_HOST_INVALID_ARGUMENT);
    check(status(c).state==TREK_HOST_CLOSED,"invalid created a campaign");
    char copied[]="T'Var \xc3\x81ren";
    ticket=enqueue(c,creation(1,copied));memset(copied,'x',strlen(copied));
    const uint64_t duplicate=enqueue(c,creation(1,"T'Var \xc3\x81ren"));
    TrekHostCompletion wrong={.size=sizeof(wrong)};
    expect(trek_host_poll(c,ticket,&wrong),TREK_HOST_ABI_MISMATCH);
    TrekHostAcademyCompletion first=finish(c,ticket,TREK_HOST_OK);
    TrekHostAcademyCompletion concurrent=finish(c,duplicate,TREK_HOST_OK);
    same(&first.output.candidate,&concurrent.output.candidate);
    check(!strcmp(first.output.candidate.display_name,"T'Var \xc3\x81ren"),"input not copied");
    TrekHostStatus bound=status(c);expect(bound.principal,TREK_HOST_OK);
    check(bound.generation==first.generation,"H03 generation");
    TrekHostAcademyCompletion retry=run(c,creation(1,"T'Var \xc3\x81ren"),TREK_HOST_OK);
    same(&first.output.candidate,&retry.output.candidate);
    run(c,creation(1,"Other"),TREK_HOST_IDEMPOTENCY_CONFLICT);
    run(c,creation(2,"Other"),TREK_HOST_BUSY_STATE);
    TrekHostAcademyCompletion view=run(c,req(TREK_HOST_ACADEMY_QUERY,first.generation),TREK_HOST_OK);
    same(&first.output.candidate,&view.output.candidate);
    deny_naval(c,first.generation);
    TrekHostClient* foreign=client("");
    expect(submit(foreign,req(TREK_HOST_ACADEMY_QUERY,first.generation),&ticket),TREK_HOST_GENERATION_EXPIRED);
    trek_host_destroy(foreign);
    expect(submit(c,req(TREK_HOST_ACADEMY_QUERY,first.generation+1),&ticket),TREK_HOST_GENERATION_EXPIRED);
    uint64_t tickets[8];
    for(unsigned i=0;i<8;++i)tickets[i]=enqueue(c,req(TREK_HOST_ACADEMY_QUERY,first.generation));
    expect(submit(c,req(TREK_HOST_ACADEMY_QUERY,first.generation),&ticket),TREK_HOST_CAPACITY_LIMIT);
    close_session(c);
    for(unsigned i=0;i<8;++i)finish(c,tickets[i],TREK_HOST_GENERATION_EXPIRED);
    run(c,creation(1,"T'Var \xc3\x81ren"),TREK_HOST_GENERATION_EXPIRED);
    retry=run(c,creation(2,"Next"),TREK_HOST_OK);
    check(retry.generation!=first.generation,"reopened generation");
    close_session(c);
    // Discard must not cancel CREATE or strand an unbound campaign.
    ticket=enqueue(c,creation(3,"Discarded"));expect(trek_host_discard(c,ticket),TREK_HOST_OK);
    retry=run(c,creation(3,"Discarded"),TREK_HOST_OK);expect(status(c).principal,TREK_HOST_OK);
    close_session(c);
    for(unsigned i=0;i<32;++i) {
        ticket=enqueue(c,creation(4+i,"Race"));close_session(c);
        TrekHostAcademyCompletion out={.size=sizeof(out)};
        TrekHostCode code;
        do {code=trek_host_academy_poll(c,ticket,&out);if(code==TREK_HOST_PENDING || code==TREK_HOST_RETRY)pause_poll();}
        while(code==TREK_HOST_PENDING || code==TREK_HOST_RETRY);
        expect(code,TREK_HOST_OK);check(out.code!=TREK_HOST_OK && !out.generation,"late creation reactivated");
        check(status(c).state==TREK_HOST_CLOSED,"close race state");
        run(c,creation(4+i,"Race"),TREK_HOST_GENERATION_EXPIRED);
    }
    trek_host_destroy(c);
    // Teardown joins native work without requiring observation.
    for(unsigned i=0;i<8;++i){c=client("");enqueue(c,creation(1,"Shutdown"));trek_host_destroy(c);}
}
static void save(TrekHostClient* c,uint64_t gen)
{
    TrekHostRequest r=old_req(TREK_HOST_SAVE,gen);r.input.slot=text("alpha");
    old_finish(c,old_enqueue(c,r),TREK_HOST_OK);
}
static void print_candidate(const TrekHostAcademyCompletion* out)
{
    const TrekHostAcademyView* v=&out->output.candidate;
    printf("%s\n%" PRIu64 "\n%" PRIu64 "\n%" PRIu64 "\n%s\n%s\n",v->campaign,out->generation,
           v->person,v->creation_fact,v->display_name,v->source_digest);
}
int main(int argc,char** argv)
{
    if(argc==1){lifecycle();puts("Academy C extension lifecycle PASS");return 0;}
    check(argc>=3,"mode/root");TrekHostClient* c=client(argv[2]);
    if(!strcmp(argv[1],"write")) {
        TrekHostAcademyCompletion out=run(c,creation(1,"Aren"),TREK_HOST_OK);
        save(c,out.generation);print_candidate(&out);
    } else if(!strcmp(argv[1],"read")) {
        check(argc==4,"campaign");
        TrekHostAcademyCompletion catalog=run(c,req(TREK_HOST_ACADEMY_SLOTS,0),TREK_HOST_OK);
        unsigned naval=0,academy=0;
        for(unsigned i=0;i<catalog.output.slots.count;++i) {
            TrekHostSlotMetadata* row=&catalog.output.slots.entries[i];
            check(row->compatible && row->recoverable && row->reason==TREK_HOST_OK &&
                  row->provenance==TREK_HOST_KNOWN_LOCAL && row->version,"H04 verified metadata");
            if(row->kind==TREK_HOST_KIND_NAVAL){check(row->format==1,"naval format");++naval;}
            if(row->kind==TREK_HOST_KIND_ACADEMY){check(row->format==2,"academy format");++academy;}
        }
        check(naval==1 && academy==1,"mixed family catalog");
        TrekHostRequest r=old_req(TREK_HOST_RESTORE,0);
        r.input.restore=(TrekHostSlot){text(argv[3]),text("alpha"),0};
        const uint64_t late_catalog=enqueue(c,req(TREK_HOST_ACADEMY_SLOTS,0));
        uint64_t restore_ticket=old_enqueue(c,r);
        TrekHostAcademyCompletion wrong={.size=sizeof(wrong)};
        expect(trek_host_academy_poll(c,restore_ticket,&wrong),TREK_HOST_ABI_MISMATCH);
        TrekHostCompletion restored=old_finish(c,restore_ticket,TREK_HOST_OK);
        finish(c,late_catalog,TREK_HOST_GENERATION_EXPIRED);
        expect(status(c).principal,TREK_HOST_OK);
        TrekHostAcademyCompletion out=run(c,req(TREK_HOST_ACADEMY_QUERY,restored.generation),TREK_HOST_OK);
        deny_naval(c,out.generation);save(c,out.generation);print_candidate(&out);
    } else if(!strcmp(argv[1],"catalog")) {
        TrekHostAcademyCompletion out=run(c,req(TREK_HOST_ACADEMY_SLOTS,0),TREK_HOST_OK);
        for(unsigned i=0;i<out.output.slots.count;++i) {
            const TrekHostSlotMetadata* row=&out.output.slots.entries[i];
            printf("%s %u %u %u %u %u %u\n",row->campaign,row->kind,row->format,row->reason,
                   row->compatible,row->recoverable,row->provenance);
        }
    } else if(!strcmp(argv[1],"reject")) {
        check(argc==5,"campaign/error");
        TrekHostRequest r=old_req(TREK_HOST_RESTORE,0);
        r.input.restore=(TrekHostSlot){text(argv[3]),text("alpha"),0};
        old_finish(c,old_enqueue(c,r),(TrekHostCode)strtoul(argv[4],NULL,10));
        check(status(c).state==TREK_HOST_CLOSED && !status(c).generation,"rejected load activated");
    } else if(!strcmp(argv[1],"overflow")) {
        TrekHostAcademyCompletion out=run(c,creation(1,"Aren"),TREK_HOST_OK);
        for(unsigned i=0;i<65;++i)save(c,out.generation);
        run(c,req(TREK_HOST_ACADEMY_SLOTS,out.generation),TREK_HOST_CAPACITY_LIMIT);
    } else check(0,"unknown mode");
    close_session(c);trek_host_destroy(c);return 0;
}

/* Real consumer of the additive extension and the tests-OFF-compatible C ABI. */
#include "trek/host/institutional_abi.h"
#include "trek/host/academy_abi.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#ifdef _WIN32
#include <windows.h>
static void pause_poll(void) { Sleep(1); }
#else
#include <time.h>
static void pause_poll(void) { const struct timespec t={0,1000000}; nanosleep(&t,NULL); }
#endif
_Static_assert(sizeof(TrekHostInstitutionalRequest)==40, "request layout");
_Static_assert(sizeof(TrekHostInstitutionalCompletion)==96, "completion layout");
static void check_at(int ok,int line,const char* expression) { if (!ok) { fprintf(stderr,"FAIL institutional ABI line %d: %s\n",line,expression); exit(1); } }
#define check(ok) check_at((ok),__LINE__,#ok)
static TrekHostText text(const char* s) { return (TrekHostText){s,(uint32_t)strlen(s),0}; }
static TrekHostCode retry_status(TrekHostClient* c,TrekHostStatus* s) {
    for(int i=0;i<10000;i++) { TrekHostCode r=trek_host_status(c,s); if(r!=TREK_HOST_RETRY)return r; pause_poll(); } return 999;
}
static TrekHostCompletion lifecycle(TrekHostClient* c,TrekHostRequest q) {
    uint64_t t=0; TrekHostCode r=0;
    for(int i=0;i<10000;i++){ r=trek_host_submit(c,&q,&t); if(r!=TREK_HOST_RETRY)break;pause_poll(); }
    check(r==0 && t);
    TrekHostCompletion o={.size=sizeof(o)};
    for(int i=0;i<10000;i++){ r=trek_host_poll(c,t,&o);if(r!=TREK_HOST_RETRY&&r!=TREK_HOST_PENDING)break;pause_poll(); }
    if(r||o.code) fprintf(stderr,"lifecycle op=%u generation=%" PRIu64 " transport=%u code=%u\n",q.operation,q.generation,r,o.code);check(r==0&&o.code==0);return o;
}
static uint64_t query(TrekHostClient* c,uint64_t g,uint32_t op,uint64_t event) {
    TrekHostInstitutionalRequest q={sizeof(q),1,op,0,g,4711,event};uint64_t t=0;TrekHostCode r=0;
    for(int i=0;i<10000;i++){r=trek_host_institutional_submit(c,&q,&t);if(r!=TREK_HOST_RETRY)break;pause_poll();}
    check(r==0&&t);return t;
}
static TrekHostInstitutionalCompletion finish(TrekHostClient* c,uint64_t t,TrekHostCode expected) {
    TrekHostInstitutionalCompletion o={.size=sizeof(o)};TrekHostCode r=0;
    for(int i=0;i<10000;i++){r=trek_host_institutional_poll(c,t,&o);if(r!=TREK_HOST_RETRY&&r!=TREK_HOST_PENDING)break;pause_poll();}
    check(r==0&&o.code==expected&&o.ticket==t&&o.correlation==4711);
    if(expected) check(!o.generation&&!o.epoch&&!o.world_revision&&!o.event_id&&!o.rank&&!o.service_status&&
        !o.effective_tick&&!o.original_revision&&!o.from_rank&&!o.to_rank);
    check(trek_host_institutional_poll(c,t,&o)==TREK_HOST_UNKNOWN_TICKET);return o;
}
static TrekHostCode current(TrekHostClient* c,TrekHostInstitutionalCompletion o) {
    for(int i=0;i<10000;i++){TrekHostCode r=trek_host_institutional_current(c,o.generation,o.epoch);if(r!=TREK_HOST_RETRY)return r;pause_poll();}return 999;
}
int main(int argc,char** argv) {
    check(argc==2);char metadata[16384];snprintf(metadata,sizeof(metadata),"%s/career-fixture.txt",argv[1]);
    FILE* f=fopen(metadata,"r");check(f!=NULL);char campaign[33]={0};uint64_t event=0,revision=0;
    check(fscanf(f,"%32s %" SCNu64 " %" SCNu64,campaign,&event,&revision)==3);fclose(f);
    TrekHostClient* c=NULL;check(trek_host_create(1,argv[1],(uint32_t)strlen(argv[1]),&c)==0);
    check(trek_host_institutional_version()==1);
    finish(c,query(c,0,TREK_HOST_CAREER,0),TREK_HOST_SESSION_CLOSED);
    TrekHostRequest restore={.size=sizeof(restore),.operation=TREK_HOST_RESTORE};
    restore.input.restore.campaign=text(campaign);restore.input.restore.slot=text("career");
    uint64_t g=lifecycle(c,restore).generation;
    uint64_t t=query(c,g,TREK_HOST_CAREER,0);
    TrekHostCompletion wrong={.size=sizeof(wrong)};check(trek_host_poll(c,t,&wrong)==TREK_HOST_ABI_MISMATCH);
    TrekHostAcademyCompletion wrong_academy={.size=sizeof(wrong_academy)};
    check(trek_host_academy_poll(c,t,&wrong_academy)==TREK_HOST_ABI_MISMATCH);
    TrekHostInstitutionalCompletion career=finish(c,t,0);
    check(career.rank==1102&&career.service_status&&career.event_id==event&&current(c,career)==0);
    TrekHostInstitutionalCompletion promotion=finish(c,query(c,g,TREK_HOST_PROMOTION,event),0);
    check(promotion.event_id==event&&promotion.original_revision==revision&&promotion.from_rank==1101&&promotion.to_rank==1102);
    for(int i=0;i<8;i++) check(finish(c,query(c,g,TREK_HOST_CAREER,0),0).world_revision==career.world_revision);
    finish(c,query(c,g,TREK_HOST_PROMOTION,event+1000),TREK_HOST_ACCESS_DENIED);
    uint64_t late=query(c,g,TREK_HOST_CAREER,0);
    TrekHostRequest save={.size=sizeof(save),.operation=TREK_HOST_SAVE,.generation=g};save.input.slot=text("abi_query");
    lifecycle(c,save);check(current(c,career)==TREK_HOST_GENERATION_EXPIRED);
    finish(c,late,TREK_HOST_GENERATION_EXPIRED);
    career=finish(c,query(c,g,TREK_HOST_CAREER,0),0);check(current(c,career)==0);
    restore.generation=g;uint64_t next=lifecycle(c,restore).generation;check(next&&next!=g&&current(c,career)==TREK_HOST_GENERATION_EXPIRED);
    TrekHostInstitutionalRequest stale={sizeof(stale),1,TREK_HOST_CAREER,0,g,1,0};t=99;
    check(trek_host_institutional_submit(c,&stale,&t)==TREK_HOST_GENERATION_EXPIRED&&!t);
    finish(c,query(c,next,TREK_HOST_PROMOTION,event),0);
    TrekHostStatus status={.size=sizeof(status)};check(retry_status(c,&status)==0&&status.institutional==TREK_HOST_SERVICE_UNAVAILABLE);
    TrekHostRequest close={.size=sizeof(close),.operation=TREK_HOST_CLOSE};lifecycle(c,close);
    finish(c,query(c,0,TREK_HOST_CAREER,0),TREK_HOST_SESSION_CLOSED);
    trek_host_destroy(c);puts("PASS H07 ABI: canonical facts, correlation, typed denial, wrong poll, repeat, late SAVE, RESTORE, CLOSE; issuer unavailable");return 0;
}

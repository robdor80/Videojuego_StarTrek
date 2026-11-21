#include "slot_store.h"
#include <algorithm>
#include <charconv>
#include <fstream>
#include <iomanip>
#include <limits>
#include <random>
#include <sstream>
#include <system_error>
#ifdef _WIN32
#define NOMINMAX
#include <windows.h>
#else
#include <cerrno>
#include <fcntl.h>
#include <sys/file.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <unistd.h>
#endif

namespace trek::host::detail {
namespace fs=std::filesystem;
namespace {
constexpr std::uint64_t max_file=64ULL*1024*1024, max_tree=512ULL*1024*1024;
void need(bool ok,Error error=Error::PERSISTENCE_FAILED) { if(!ok)throw StorageFailure{error}; }
#if defined(TREK_HOST_PERSISTENCE_TESTING) || defined(TREK_HOST_ACADEMY_TESTING)
std::function<void(const char*)> test_hook;
void point(const char* name) { if(test_hook)test_hook(name); }
#else
void point(const char*) {}
#endif
fs::path utf8(const std::string& s) { return fs::path(reinterpret_cast<const char8_t*>(s.c_str())); }
void mkdir(const fs::path& p) {
#ifdef _WIN32
    need(fs::create_directory(p));
#else
    need(::mkdir(p.c_str(),0700)==0);
#endif
}
void ensure_dir(const fs::path& p) {
    if(!fs::exists(fs::symlink_status(p)))mkdir(p);
    PinnedDirectory checked(p);
}
// Every file is opened without following links, and must have a unique name/link.
class File {
public:
#ifdef _WIN32
    HANDLE fd=INVALID_HANDLE_VALUE;
    File(const fs::path& p,bool write,bool lock=false,bool existing_write=false) {
        fd=CreateFileW(p.c_str(),GENERIC_READ|((write || existing_write)?GENERIC_WRITE:0),lock?0:FILE_SHARE_READ,
                       nullptr,write?(lock?OPEN_ALWAYS:CREATE_NEW):OPEN_EXISTING,
                       FILE_FLAG_OPEN_REPARSE_POINT|FILE_FLAG_WRITE_THROUGH,nullptr);
        need(fd!=INVALID_HANDLE_VALUE);
        BY_HANDLE_FILE_INFORMATION info{};
        if(!GetFileInformationByHandle(fd,&info) || (info.dwFileAttributes&(FILE_ATTRIBUTE_REPARSE_POINT|FILE_ATTRIBUTE_DIRECTORY)) || info.nNumberOfLinks!=1) {
            CloseHandle(fd);fd=INVALID_HANDLE_VALUE;throw StorageFailure{Error::PATH_REJECTED};
        }
    }
    ~File(){if(fd!=INVALID_HANDLE_VALUE)CloseHandle(fd);}
    std::uint64_t size(){LARGE_INTEGER n{};need(GetFileSizeEx(fd,&n));return static_cast<std::uint64_t>(n.QuadPart);}
    void read(char* p,std::size_t n){DWORD got=0;need(ReadFile(fd,p,static_cast<DWORD>(n),&got,nullptr) && got==n);}
    void write(const char* p,std::size_t n){DWORD got=0;need(WriteFile(fd,p,static_cast<DWORD>(n),&got,nullptr) && got==n);}
    void sync(){need(FlushFileBuffers(fd)!=0);}
    void close_checked(){auto held=fd;fd=INVALID_HANDLE_VALUE;need(CloseHandle(held)!=0);}
#else
    int fd=-1;
    File(const fs::path& p,bool write,bool lock=false,bool existing_write=false) {
        fd=::open(p.c_str(),O_CLOEXEC|O_NOFOLLOW|(write?(O_RDWR|O_CREAT|(lock?0:O_EXCL)):(existing_write?O_RDWR:O_RDONLY)),0600);
        need(fd>=0);struct stat st{};
        if(::fstat(fd,&st)!=0 || !S_ISREG(st.st_mode) || st.st_nlink!=1) {
            ::close(fd);fd=-1;throw StorageFailure{Error::PATH_REJECTED};
        }
        if(lock && ::flock(fd,LOCK_EX|LOCK_NB)!=0){::close(fd);fd=-1;throw StorageFailure{Error::BUSY_STATE};}
    }
    ~File(){if(fd>=0)::close(fd);}
    std::uint64_t size(){struct stat s{};need(::fstat(fd,&s)==0);return static_cast<std::uint64_t>(s.st_size);}
    void read(char* p,std::size_t n){while(n){auto k=::read(fd,p,n);if(k<0 && errno==EINTR)continue;need(k>0);p+=k;n-=static_cast<std::size_t>(k);}}
    void write(const char* p,std::size_t n){while(n){auto k=::write(fd,p,n);if(k<0 && errno==EINTR)continue;need(k>0);p+=k;n-=static_cast<std::size_t>(k);}}
    void sync(){need(::fsync(fd)==0);}
    void close_checked(){auto held=fd;fd=-1;need(::close(held)==0);}
#endif
    void finish(){point("file_sync");sync();close_checked();}
    File(const File&)=delete;
};
void sync_dir(const fs::path& p) {
#ifndef _WIN32
    PinnedDirectory dir(p);int fd=::open(dir.path().c_str(),O_RDONLY|O_DIRECTORY|O_CLOEXEC);
    need(fd>=0);bool ok=::fsync(fd)==0;bool closed=::close(fd)==0;need(ok && closed);
#else
    // Namespace publication on Windows uses MoveFileExW WRITE_THROUGH below.
    (void)p;
#endif
}
std::string read(const fs::path& p,std::uint64_t limit=4096) {
    File f(p,false);auto n=f.size();need(n<=limit,Error::CAPACITY_LIMIT);
    std::string s(static_cast<std::size_t>(n),'\0');f.read(s.data(),s.size());need(f.size()==n,Error::SAVE_CORRUPT);return s;
}
void write(const fs::path& p,const std::string& s) {
    File f(p,true);auto half=s.size()/2;f.write(s.data(),half);point("partial_write");f.write(s.data()+half,s.size()-half);f.finish();sync_dir(p.parent_path());
}
std::uint64_t number(const std::string& s) {
    std::uint64_t n=0;auto r=std::from_chars(s.data(),s.data()+s.size(),n);
    need(!s.empty() && r.ec==std::errc{} && r.ptr==s.data()+s.size(),Error::SAVE_CORRUPT);return n;
}
std::string identity_text(PersistentIdentity i) {
    return std::to_string(i.person)+" "+std::to_string(i.record)+" "+std::to_string(i.revision)+" "+std::to_string(i.tick);
}
PersistentIdentity parse_identity(const std::string& s) {
    std::istringstream in(s);std::string a,b,c,d,extra;need(bool(in>>a>>b>>c>>d) && !(in>>extra),Error::SAVE_CORRUPT);
    PersistentIdentity i{number(a),number(b),number(c),number(d)};need(i.person && i.record,Error::IDENTITY_MISMATCH);return i;
}
constexpr std::string_view academy_magic = "TREKHOST4 2";
constexpr std::string_view academy_prefix = "TREKHOST4 2\nACADEMY\n";

bool digest(const std::string& value) {
    return value.size()==64 && value.find_first_not_of("0123456789abcdef")==std::string::npos;
}
void validate_anchor(const AcademyAnchor& a) {
    (void)decode_campaign(a.profile);
    need(a.person && a.creation_fact && a.person!=a.creation_fact &&
         digest(a.source_digest) && digest(a.catalog_digest) && digest(a.name_digest),Error::IDENTITY_MISMATCH);
}
std::string anchor_text(const AcademyAnchor& a) {
    return std::string(academy_catalog_version)+" "+a.catalog_digest+"\n"+
           std::string(academy_source_version)+" "+a.source_digest+"\n"+
           std::to_string(a.person)+" "+std::to_string(a.creation_fact)+" "+a.profile+" "+a.name_digest+"\n";
}
struct Envelope {
    std::string campaign,slot;
    std::uint64_t version;
    SlotIdentity identity;
    std::string history_digest;
    CampaignKind kind() const {
        return std::holds_alternative<AcademySnapshotIdentity>(identity) ? CampaignKind::ACADEMY : CampaignKind::NAVAL;
    }
};
std::string registry_text(const Envelope& e) {
    if (const auto* academy=std::get_if<AcademySnapshotIdentity>(&e.identity))
        return "TREKHOST4 ACADEMY REGISTRY 1\n"+e.campaign+"\n"+anchor_text(academy->anchor);
    return identity_text(std::get<PersistentIdentity>(e.identity));
}
bool registry_matches(const Envelope& e,const std::string& text) {
    if (const auto* naval=std::get_if<PersistentIdentity>(&e.identity))
        return !text.starts_with("TREKHOST4 ACADEMY ") && parse_identity(text)==*naval;
    return text==registry_text(e);
}
std::string encode(const Envelope& e) {
    const auto address=std::string(TREK_HOST_CORE_SHA)+"\n"+e.campaign+"\n"+e.slot+"\n"+std::to_string(e.version)+"\n";
    if (const auto* academy=std::get_if<AcademySnapshotIdentity>(&e.identity))
        return std::string(academy_prefix)+address+anchor_text(academy->anchor)+
               std::to_string(academy->revision)+" "+std::to_string(academy->clock)+"\n"+e.history_digest+"\n";
    return "TREKHOST4 1\n"+address+identity_text(std::get<PersistentIdentity>(e.identity))+"\n";
}
Envelope decode(const std::string& s) {
    std::istringstream in(s);std::string magic,sha,campaign,slot,ver,id,extra;
    need(bool(std::getline(in,magic)),Error::SAVE_CORRUPT);
    const bool academy=magic==academy_magic;
    need(academy || magic=="TREKHOST4 1",Error::SAVE_INCOMPATIBLE);
    if (academy) need(bool(std::getline(in,id)) && id=="ACADEMY",Error::SAVE_INCOMPATIBLE);
    need(bool(std::getline(in,sha)) && sha==TREK_HOST_CORE_SHA,Error::SAVE_INCOMPATIBLE);
    need(bool(std::getline(in,campaign)) && bool(std::getline(in,slot)) && bool(std::getline(in,ver)),Error::SAVE_CORRUPT);
    (void)decode_campaign(campaign);need(valid_slot(slot),Error::PATH_REJECTED);auto version=number(ver);need(version>0,Error::SAVE_CORRUPT);
    if (!academy) {
        need(bool(std::getline(in,id)) && !std::getline(in,extra),Error::SAVE_CORRUPT);
        return {campaign,slot,version,parse_identity(id),{}};
    }

    std::string catalog,source,anchor,progress,history;
    need(bool(std::getline(in,catalog) && std::getline(in,source) && std::getline(in,anchor) &&
              std::getline(in,progress) && std::getline(in,history)) && !std::getline(in,extra),Error::SAVE_CORRUPT);
    need(catalog.starts_with(std::string(academy_catalog_version)+" ") &&
         source.starts_with(std::string(academy_source_version)+" "),Error::SAVE_INCOMPATIBLE);
    AcademySnapshotIdentity snapshot;
    auto& a=snapshot.anchor;
    a.catalog_digest=catalog.substr(academy_catalog_version.size()+1);
    a.source_digest=source.substr(academy_source_version.size()+1);
    std::istringstream anchor_fields(anchor),progress_fields(progress);
    std::string person,fact,revision,clock;
    need(bool(anchor_fields>>person>>fact>>a.profile>>a.name_digest) && !(anchor_fields>>extra) &&
         bool(progress_fields>>revision>>clock) && !(progress_fields>>extra) && digest(history),Error::SAVE_CORRUPT);
    a.person=number(person);a.creation_fact=number(fact);
    snapshot.revision=number(revision);snapshot.clock=number(clock);
    validate_anchor(a);
    Envelope result{campaign,slot,version,std::move(snapshot),std::move(history)};
    need(encode(result)==s,Error::SAVE_CORRUPT);
    return result;
}
bool object_name(const std::string& n) {
    return n=="CURRENT" || (n.size()==68 && n.substr(64)==".obj" && n.substr(0,64).find_first_not_of("0123456789abcdef")==std::string::npos);
}
// Complete bounded flat tree. No recursive traversal or raw content diagnostics.
void tree(const fs::path& source,const fs::path& destination={},bool durable=false) {
    PinnedDirectory pin(source);std::uint64_t count=0,total=0;bool current=false;
    for(const auto& e:fs::directory_iterator(pin.path())) {
        auto name=e.path().filename().string();need(++count<=4096,Error::CAPACITY_LIMIT);
        need(object_name(name) || name=="writer.lock",Error::SAVE_CORRUPT);
        File f(e.path(),false,false,durable);auto n=f.size();need(n<=max_file && total<=max_tree-n,Error::CAPACITY_LIMIT);total+=n;
        if(name=="writer.lock")continue;
        current=current || name=="CURRENT";
        if(!destination.empty()) {
            File out(destination/name,true);std::array<char,65536> buffer{};auto left=n;
            point("copy_file");
            while(left){auto take=static_cast<std::size_t>(std::min<std::uint64_t>(left,buffer.size()));f.read(buffer.data(),take);out.write(buffer.data(),take);left-=take;}
            need(f.size()==n,Error::SAVE_CORRUPT);out.finish();
        } else if(durable) f.finish();
    }
    need(current,Error::SAVE_CORRUPT);if(!destination.empty())sync_dir(destination);
}
std::string history_digest(const fs::path& history) {
    return academy_digest_hex(read(history/"CURRENT",128));
}
std::uint64_t version_number(const std::string& n) {
    if(n.size()<2 || n[0]!='v')return 0;
    return number(n.substr(1));
}
std::vector<std::uint64_t> versions(const fs::path& slot) {
    std::vector<std::uint64_t> out;std::size_t entries=0;
    for(const auto& e:fs::directory_iterator(slot)) {
        need(++entries<=10000,Error::CAPACITY_LIMIT);
        auto name=e.path().filename().string();if(name.starts_with("v")){auto n=version_number(name);if(n){need(out.size()<10000,Error::CAPACITY_LIMIT);out.push_back(n);}}
    }
    need(out.size()<=10000,Error::CAPACITY_LIMIT);std::sort(out.begin(),out.end());return out;
}
void publish(const fs::path& from,const fs::path& to) {
    point("publish_rename");
#ifdef _WIN32
    need(MoveFileExW(from.c_str(),to.c_str(),MOVEFILE_WRITE_THROUGH)!=0);
#else
    need(::rename(from.c_str(),to.c_str())==0);
#endif
}
}

struct PinnedDirectory::Impl {
    fs::path original;
#ifdef _WIN32
    std::vector<HANDLE> handles;
    ~Impl(){for(auto h:handles)CloseHandle(h);}
#else
    std::vector<int> handles;
    ~Impl(){for(auto h:handles)::close(h);}
#endif
};
PinnedDirectory::PinnedDirectory(const fs::path& path):impl_(std::make_unique<Impl>()) {
    need(path.is_absolute() && path.native().size()<=4096,Error::PATH_REJECTED);
    impl_->original=path;
#ifdef _WIN32
    auto current=path.root_path();
    for(const auto& part:path.relative_path()) {
        need(part!=".." && part!=".",Error::PATH_REJECTED);current/=part;
        auto h=CreateFileW(current.c_str(),GENERIC_READ,FILE_SHARE_READ|FILE_SHARE_WRITE,nullptr,OPEN_EXISTING,FILE_FLAG_BACKUP_SEMANTICS|FILE_FLAG_OPEN_REPARSE_POINT,nullptr);
        need(h!=INVALID_HANDLE_VALUE,Error::PATH_REJECTED);impl_->handles.push_back(h);
        BY_HANDLE_FILE_INFORMATION info{};need(GetFileInformationByHandle(h,&info) && (info.dwFileAttributes&FILE_ATTRIBUTE_DIRECTORY) && !(info.dwFileAttributes&FILE_ATTRIBUTE_REPARSE_POINT),Error::PATH_REJECTED);
    }
#else
    fs::path relative=path.relative_path();int fd=-1;
    const auto text=path.string();
    if(text.starts_with("/proc/self/fd/")) {
        const auto tail=text.substr(14);const auto slash=tail.find('/');const auto descriptor=tail.substr(0,slash);
        const auto original=number(descriptor);need(original<=static_cast<unsigned>(std::numeric_limits<int>::max()),Error::PATH_REJECTED);
        fd=::fcntl(static_cast<int>(original),F_DUPFD_CLOEXEC,3);
        relative=slash==std::string::npos?fs::path{}:fs::path(tail.substr(slash+1));
    } else fd=::open("/",O_RDONLY|O_DIRECTORY|O_CLOEXEC);
    need(fd>=0);impl_->handles.push_back(fd);
    for(const auto& part:relative) {
        need(part!=".." && part!=".",Error::PATH_REJECTED);
        fd=::openat(fd,part.c_str(),O_RDONLY|O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC);need(fd>=0,Error::PATH_REJECTED);impl_->handles.push_back(fd);
    }
#endif
}
PinnedDirectory::~PinnedDirectory()=default;
fs::path PinnedDirectory::path() const {
#ifdef _WIN32
    return impl_->original;
#else
    return fs::path("/proc/self/fd")/std::to_string(impl_->handles.back());
#endif
}
std::string new_campaign_id() {
    std::random_device rng;std::ostringstream out;out<<std::hex<<std::setfill('0');
    for(int i=0;i<16;++i)out<<std::setw(2)<<(rng()&255U);return out.str();
}
CampaignId decode_campaign(const std::string& s) {
    need(s.size()==32 && s.find_first_not_of("0123456789abcdef")==std::string::npos && s!=std::string(32,'0'),Error::PATH_REJECTED);
    CampaignId id{};for(std::size_t i=0;i<16;++i){unsigned x=0;std::from_chars(s.data()+i*2,s.data()+i*2+2,x,16);id[i]=static_cast<std::uint8_t>(x);}return id;
}
bool valid_slot(const std::string& s) {
    return !s.empty() && s.size()<=32 && s.find_first_not_of("abcdefghijklmnopqrstuvwxyz0123456789_")==std::string::npos && s!="con" && s!="prn" && s!="aux" && s!="nul" && !(s.size()==4 && (s.starts_with("com") || s.starts_with("lpt")) && s[3]>='0' && s[3]<='9');
}
void copy_history(const fs::path& source,const fs::path& destination) {
    mkdir(destination);
    PinnedDirectory pinned(destination);
    tree(source,pinned.path());
}
namespace {
std::shared_ptr<PinnedDirectory> root(const StorageConfig& config) {
    need(!config.root.empty() && config.root.find('\0')==std::string::npos && !config.root.starts_with("/proc/"),Error::PATH_REJECTED);
    auto configured=utf8(config.root);
#ifdef _WIN32
    need(configured.is_absolute() && configured.root_name().native().size()==2 && configured.root_name().native()[1]==L':',Error::PATH_REJECTED);
    // Local volumes only. Extended paths keep the same bounded path policy and
    // avoid MAX_PATH failures for nested generations on supported Windows.
    configured=fs::path(std::wstring(L"\\\\?\\")+configured.native());
#endif
    auto pin=std::make_shared<PinnedDirectory>(configured);
#ifndef _WIN32
    struct stat info{};need(::stat(pin->path().c_str(),&info)==0 && info.st_uid==::getuid() && !(info.st_mode&0022),Error::PATH_REJECTED);
#endif
    return pin;
}
Envelope validate(const fs::path& local,const fs::path& generation,const SlotAddress& address) {
    auto e=decode(read(generation/"manifest"));
    need(e.campaign==address.campaign && e.slot==address.slot && e.version==address.version,Error::SAVE_CORRUPT);
    need(address.kind==CampaignKind::AUTO || address.kind==e.kind(),Error::SAVE_INCOMPATIBLE);
    need(read(generation/"COMMITTED")==encode(e),Error::SAVE_CORRUPT);
    need(fs::exists(fs::symlink_status(local)),Error::SAVE_UNTRUSTED);
    PinnedDirectory registry(local.parent_path());
    need(registry_matches(e,read(registry.path()/local.filename())),Error::IDENTITY_MISMATCH);
    tree(generation/"history");
    if (e.kind()==CampaignKind::ACADEMY) {
        for (const auto& entry : fs::directory_iterator(generation)) {
            const auto name=entry.path().filename();
            need(name=="manifest" || name=="COMMITTED" || name=="history",Error::SAVE_CORRUPT);
        }
        PinnedDirectory history(generation/"history");
        need(history_digest(history.path())==e.history_digest,Error::SAVE_CORRUPT);
    }
    return e;
}
}
Error SlotStore::save(const std::string& campaign_id,const std::string& slot,SlotIdentity identity,
                     const std::function<Error(const fs::path&)>& snapshot,
                     const std::function<Error(const PreparedSlot&)>& verify) const {
    bool publication_started=false;
    try {
        (void)decode_campaign(campaign_id);need(valid_slot(slot),Error::PATH_REJECTED);
        Envelope e{campaign_id,slot,0,std::move(identity),{}};
        if (const auto* naval=std::get_if<PersistentIdentity>(&e.identity))
            need(naval->person && naval->record,Error::PRINCIPAL_UNBOUND);
        else validate_anchor(std::get<AcademySnapshotIdentity>(e.identity).anchor);
        auto r=root(config_);File lock(r->path()/"host.lock",true,true);
        ensure_dir(r->path()/"campaigns");PinnedDirectory campaigns(r->path()/"campaigns");
        ensure_dir(campaigns.path()/campaign_id);PinnedDirectory campaign(campaigns.path()/campaign_id);
        ensure_dir(r->path()/"registry");PinnedDirectory registry(r->path()/"registry");
        if(!fs::exists(fs::symlink_status(registry.path()/campaign_id))) {
            const auto temporary=registry.path()/("pending-"+new_campaign_id());
            write(temporary,registry_text(e)); // checked flush + close; partial files are never registry entries
            point("registry_before_publish");publication_started=true;
#ifdef _WIN32
            const auto moved=MoveFileExW(temporary.c_str(),(registry.path()/campaign_id).c_str(),MOVEFILE_WRITE_THROUGH);
            if(!moved) {const auto error=GetLastError();if(error==ERROR_ALREADY_EXISTS || error==ERROR_FILE_EXISTS)publication_started=false;}
            need(moved!=0);
#else
            // Linux atomic no-replace publication. Never fall back to replacing rename.
            const auto moved=::syscall(SYS_renameat2,AT_FDCWD,temporary.c_str(),AT_FDCWD,
                           (registry.path()/campaign_id).c_str(),1 /* RENAME_NOREPLACE */);
            if(moved!=0 && errno==EEXIST)publication_started=false;
            need(moved==0);
#endif
            point("registry_after_publish");sync_dir(registry.path());
            need(read(registry.path()/campaign_id)==registry_text(e));
            publication_started=false;
        }
        need(registry_matches(e,read(registry.path()/campaign_id)),Error::IDENTITY_MISMATCH);
        sync_dir(registry.path());
        ensure_dir(campaign.path()/"slots");PinnedDirectory slots(campaign.path()/"slots");
        ensure_dir(slots.path()/slot);PinnedDirectory selected(slots.path()/slot);
        auto prior=versions(selected.path());auto version=prior.empty()?1:prior.back()+1;need(version && version<=10000,Error::CAPACITY_LIMIT);
        const auto name="v"+std::to_string(version);mkdir(selected.path()/name);PinnedDirectory staging(selected.path()/name);
        point("before_snapshot");
        const auto status=snapshot(staging.path()/"history");
        need(status==Error::OK,e.kind()==CampaignKind::ACADEMY?status:Error::PERSISTENCE_FAILED);
        point("after_snapshot");tree(staging.path()/"history",{},true);sync_dir(staging.path()/"history");
        auto history=std::make_shared<PinnedDirectory>(staging.path()/"history");
        if (e.kind()==CampaignKind::ACADEMY) e.history_digest=history_digest(history->path());
        const auto verified=verify({history,e.identity,campaign_id});
        need(verified==Error::OK,e.kind()==CampaignKind::ACADEMY?verified:Error::IDENTITY_MISMATCH);
        e.version=version;
        write(staging.path()/"manifest",encode(e));
        point("after_manifest");write(staging.path()/"prepared",encode(e));
        sync_dir(staging.path());sync_dir(selected.path());sync_dir(slots.path());sync_dir(campaign.path());sync_dir(campaigns.path());sync_dir(r->path());
        point("before_publish");publication_started=true;
        publish(staging.path()/"prepared",staging.path()/"COMMITTED");
        point("after_publish");sync_dir(staging.path());sync_dir(selected.path());
        need(read(staging.path()/"COMMITTED")==encode(e));
        point("before_ack");return Error::OK;
    } catch(const StorageFailure& e) { return publication_started?Error::PUBLICATION_UNCERTAIN:e.error; }
      catch(...) { return publication_started?Error::PUBLICATION_UNCERTAIN:Error::PERSISTENCE_FAILED; }
}
PreparedSlot SlotStore::prepare(SlotAddress address) const {
    (void)decode_campaign(address.campaign);need(valid_slot(address.slot),Error::PATH_REJECTED);
    auto r=root(config_);File lock(r->path()/"host.lock",true,true);
    PinnedDirectory campaign(r->path()/"campaigns"/address.campaign);
    PinnedDirectory slot(campaign.path()/"slots"/address.slot);
    if(!address.version) {
        auto all=versions(slot.path());
        for(auto it=all.rbegin();it!=all.rend();++it) {
            PinnedDirectory candidate(slot.path()/("v"+std::to_string(*it)));
            if(fs::exists(fs::symlink_status(candidate.path()/"COMMITTED"))){address.version=*it;break;}
        }
    }
    need(address.version>0 && address.version<=10000,Error::SAVE_CORRUPT);
    PinnedDirectory generation(slot.path()/("v"+std::to_string(address.version)));
    auto e=validate(r->path()/"registry"/address.campaign,generation.path(),address);
    ensure_dir(r->path()/"work");PinnedDirectory work(r->path()/"work");
    const auto id=new_campaign_id();mkdir(work.path()/id);PinnedDirectory copy(work.path()/id);
    mkdir(copy.path()/"history");auto history=std::make_shared<PinnedDirectory>(copy.path()/"history");
    tree(generation.path()/"history",history->path());
    if (e.kind()==CampaignKind::ACADEMY) need(history_digest(history->path())==e.history_digest,Error::SAVE_CORRUPT);
    point("after_copy");
    return {std::move(history),std::move(e.identity),std::move(e.campaign)};
}
InspectionResult SlotStore::inspect(const std::function<Error(const PreparedSlot&)>& verify) const {
    InspectionResult result;
    try {
        auto r=root(config_);
        if(!fs::exists(fs::symlink_status(r->path()/"campaigns")))return result;
        PinnedDirectory campaigns(r->path()/"campaigns");std::size_t count=0;
        for(const auto& c:fs::directory_iterator(campaigns.path())) {
            need(++count<=10000,Error::CAPACITY_LIMIT);auto campaign_id=c.path().filename().string();(void)decode_campaign(campaign_id);PinnedDirectory campaign(c.path());
            PinnedDirectory slots(campaign.path()/"slots");
            for(const auto& s:fs::directory_iterator(slots.path())) {
                need(++count<=10000,Error::CAPACITY_LIMIT);auto name=s.path().filename().string();need(valid_slot(name),Error::PATH_REJECTED);PinnedDirectory slot(s.path());
                for(auto version:versions(slot.path())) {
                    need(++count<=10000,Error::CAPACITY_LIMIT);SlotInspection info;info.address={campaign_id,name,version};
                    try {
                        PinnedDirectory generation(slot.path()/("v"+std::to_string(version)));
                        auto manifest=read(generation.path()/"manifest");
                        if (manifest.starts_with(academy_prefix)) {
                            info.format=2;info.address.kind=CampaignKind::ACADEMY;
                        }
                        auto e=decode(manifest);
                        info.format=e.kind()==CampaignKind::ACADEMY?2:1;
                        info.address.kind=e.kind();info.compatible=true;
                        auto admitted=validate(r->path()/"registry"/campaign_id,generation.path(),info.address);
                        if(verify) {
                            auto history=std::make_shared<PinnedDirectory>(generation.path()/"history");
                            auto error=verify({history,admitted.identity,campaign_id});
                            if (info.format==2 && error==Error::SAVE_INCOMPATIBLE) info.compatible=false;
                            need(error==Error::OK,error);
                        }
                        info.provenance=Provenance::KNOWN_LOCAL;info.reason=Error::OK;info.recoverable=true;
                    } catch(const StorageFailure& e) {
                        info.reason=e.error;if(e.error==Error::SAVE_UNTRUSTED)info.provenance=Provenance::IMPORTED_UNVERIFIED;
                    } catch(...) { info.reason=Error::PERSISTENCE_FAILED; }
                    result.slots.push_back(std::move(info));
                }
            }
        }
    } catch(const StorageFailure& e) { result.error=e.error; } catch(...) { result.error=Error::PERSISTENCE_FAILED; }
    return result;
}
#if defined(TREK_HOST_PERSISTENCE_TESTING) || defined(TREK_HOST_ACADEMY_TESTING)
void storage_test_event(const char* name) {point(name);}
void storage_test_hook(std::function<void(const char*)> hook) { test_hook=std::move(hook); }
#endif
} // namespace trek::host::detail

#pragma once
#include "f05_ai.h"
#include <cstddef>
#include <cstdint>
#include <string>
#include <utility>
namespace trek::ai {
struct Proposal {
 uint64_t version=0,actor=0,request=0,projection=0,revision=0,issued=0,expires=0;
 uint32_t intent=0;bool clarification=false,insufficient=false,scan=false;
 std::string explanation,trace;
};
bool parse(const char*,size_t,Proposal&) noexcept;
struct Input { F05AiContext context{};std::string text,model; };
struct Reply { bool pending=false;uint32_t error=F05_AI_NONE;std::string body; };
/* Implementations MUST enqueue/poll/cancel without blocking the owner thread.
 * A transport may use a worker/service and external config; it has no Core API.
 * No URLs, commercial models, keys or automatic remote calls are supplied. */
class Provider {
public:
 virtual ~Provider()=default;
 virtual void start(const Input&)=0;
 virtual Reply poll(uint64_t request)=0;
 virtual void cancel(uint64_t request) noexcept=0;
};
/* One controllable provider per test/job: delays are poll counts, no sleeping. */
class SimulatedProvider final:public Provider {
public:
 Input received{};Reply reply{};unsigned delay=0,starts=0,polls=0,cancels=0;
 bool throw_start=false,throw_poll=false;
 void start(const Input&) override;
 Reply poll(uint64_t) override;
 void cancel(uint64_t) noexcept override {++cancels;}
};
enum class Purpose { routine, language, analysis };
uint32_t route_for(Purpose,bool provider_available) noexcept;
std::string message(const F05AiView&);
struct Config {std::string fast_model,reasoning_model;uint64_t timeout_ms=1500;};
/* Host-owned job. poll never advances gameplay time or runs P03. Caller may
 * run deterministic initiative at any time and explicitly apply a valid result.
 * monotonic_ms is Host transport time, distinct from authoritative Core ticks. */
class Job {
 F04Session* session_;F04Ref actor_;Provider* provider_;F05AiContext context_{};
 uint64_t deadline_=0;bool done_=false;
public:
 Job(F04Session*,F04Ref,Provider*);
 uint32_t start(const F05AiRequest&,std::string text,const Config&,uint64_t monotonic_ms);
 uint32_t poll(uint64_t monotonic_ms,F05AiView&);
 const F05AiContext& context() const {return context_;}
};
std::string response(const F05AiContext&,uint32_t intent=F05_AI_SCAN);
} // namespace trek::ai

#include "f05_ai_provider.h"
#include <jsoncons/json.hpp>
#include <limits>
#include <stdexcept>
namespace trek::ai {
using json=jsoncons::json;
uint32_t route_for(Purpose purpose,bool available) noexcept {
 if(!available || purpose==Purpose::routine)return F05_AI_DETERMINISTIC;
 return purpose==Purpose::analysis?F05_AI_REASONING:F05_AI_FAST;
}
std::string message(const F05AiView& v) {
 switch(v.status) {
 case F05_AI_PENDING:return "Análisis opcional pendiente. La tripulación continúa su servicio.";
 case F05_AI_VALID:return "Propuesta disponible para revisión. Aún no es un resultado operativo.";
 case F05_AI_APPROVAL:return "Se requiere una decisión o aprobación explícita de la persona autorizada.";
 case F05_AI_CLARIFICATION:return "Se necesita aclarar la petición antes de proponer una acción.";
 case F05_AI_INSUFFICIENT:return "Información autorizada insuficiente. Solicite un informe válido.";
 case F05_AI_APPLIED:return "Propuesta tramitada por el controlador. Consulte el resultado autoritativo de Core.";
 default:return "Análisis no disponible. Continúan los procedimientos deterministas autorizados.";
 }
}
void SimulatedProvider::start(const Input& i){++starts;if(throw_start)throw std::runtime_error("simulated network");received=i;}
Reply SimulatedProvider::poll(uint64_t){++polls;if(throw_poll)throw std::runtime_error("simulated network");if(delay){--delay;return {true,0,{}};}return reply;}
Job::Job(F04Session* s,F04Ref a,Provider* p):session_(s),actor_(a),provider_(p){}
uint32_t Job::start(const F05AiRequest& q,std::string text,const Config& cfg,uint64_t now) {
 if(context_.request || q.actor.id!=actor_.id || q.actor.scope!=actor_.scope || text.size()>2048 || !cfg.timeout_ms || cfg.timeout_ms>60000 || now>std::numeric_limits<uint64_t>::max()-cfg.timeout_ms)return F04_ARGUMENT;
 auto code=f05_ai_begin(session_,&q,&context_);if(code)return code;
 deadline_=now+cfg.timeout_ms;
 if(q.route==F05_AI_DETERMINISTIC || !context_.complete || !provider_)return F04_OK;
 try{provider_->start({context_,std::move(text),q.route==F05_AI_FAST?cfg.fast_model:cfg.reasoning_model});}
 catch(...){F05AiView v{};done_=true;return f05_ai_finish(session_,actor_,context_.request,nullptr,0,F05_AI_NETWORK,&v);}return F04_OK;
}
uint32_t Job::poll(uint64_t now,F05AiView& v) {
 if(!context_.request)return F04_ARGUMENT;
 if(done_)return f05_ai_view(session_,actor_,context_.request,&v);
 Reply r;
 if(!provider_ || context_.route==F05_AI_DETERMINISTIC)r.error=F05_AI_NOT_CONFIGURED;
 else if(!context_.complete){r.body=response(context_,F05_AI_UNKNOWN);}
 else if(now>=deadline_){provider_->cancel(context_.request);r.error=F05_AI_TIMEOUT;}
 else try{r=provider_->poll(context_.request);}catch(...){r.error=F05_AI_NETWORK;}
 if(r.pending)return f05_ai_view(session_,actor_,context_.request,&v);
 const auto code=f05_ai_finish(session_,actor_,context_.request,r.body.data(),r.body.size(),r.error,&v);
 if(code==F04_OK)done_=true;return code;
}
std::string response(const F05AiContext& c,uint32_t intent) {
 json j=json::object();j["version"]=1;j["actor"]=c.actor;j["request"]=c.request;j["projection"]=c.projection;j["revision"]=c.revision;j["issued_at"]=c.issued_at;j["expires"]=c.expires;
 j["intent"]=intent==F05_AI_SCAN?"scan":intent==F05_AI_ASK?"clarify":intent==F05_AI_UNKNOWN?"insufficient":"advise";
 j["needs_clarification"]=intent==F05_AI_ASK;j["insufficient_data"]=intent==F05_AI_UNKNOWN;
 j["actions"]=json::array();if(intent==F05_AI_SCAN){json a=json::object();a["operation"]="F04_SCAN";a["parameters"]=json::object();j["actions"].push_back(a);}
 j["explanation"]="Propuesta no autoritativa; consultar resultado Core.";j["trace"]="simulated-1";return j.to_string();
}
} // namespace trek::ai

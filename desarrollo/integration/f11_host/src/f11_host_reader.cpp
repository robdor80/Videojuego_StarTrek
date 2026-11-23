#include "f11_host_reader.h"

namespace trek::f11_host {
namespace {
bool same(F11CharacterId a,F11CharacterId b) noexcept {
  return a.high48==b.high48 && a.mid48==b.mid48 &&
         a.low32==b.low32 && a.reserved==0 && b.reserved==0;
}
}

std::uint32_t career(F04Session* session,F04Ref subject,Career* out) noexcept {
  if(!out)return F04_ARGUMENT;
  *out={};
  F11PersonnelView view{};
  const auto code=f11_personnel(session,subject,&view);
  if(code!=F04_OK)return code;
  if(view.person!=subject.id || view.character.reserved ||
     !view.commission || !view.rank_event)return F11_IDENTITY;
  *out={view.character,view.person,view.commission,view.rank_event,
        view.ship,view.billet,view.department,view.revision,
        view.rank,view.service_status};
  return F04_OK;
}

std::uint32_t promotion(F04Session* session,F04Ref subject,
                        std::uint64_t event,Promotion* out) noexcept {
  if(!out)return F04_ARGUMENT;
  *out={};
  // The Core query denies other subjects. Never reconstruct from a client
  // supplied receipt, local UI state or an untrusted JSON service record.
  F11PromotionView record{};
  const auto code=f11_promotion(session,subject,event,&record);
  if(code!=F04_OK)return code;
  F11PersonnelView person{};
  const auto pcode=f11_personnel(session,subject,&person);
  if(pcode!=F04_OK)return pcode;
  if(record.person!=person.person || record.receipt.promotion_event_id!=event ||
     !same(record.receipt.character,person.character) ||
     record.visibility!=F11_SUBJECT_AND_PERSONNEL ||
     record.receipt.status!=F04_OK)return F11_IDENTITY;
  *out={record.receipt.character,event,record.receipt.personnel_order_id,
        record.receipt.original_commit_revision,record.receipt.effective_at,
        record.person,record.ship,record.billet,record.department,
        record.receipt.from_rank,record.receipt.to_rank,record.visibility};
  return F04_OK;
}
} // namespace trek::f11_host

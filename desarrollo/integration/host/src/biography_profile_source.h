#pragma once
#include "f10/biography_validation.h"
#include "trek/host/session_owner.h"

namespace trek::host::detail {
// Private pre-PERSON local profile projection. Only SessionOwner can issue its
// activation. No nickname, profile ID, campaign ID or generation comes from UI.
class BiographyProfileSource final {
public:
    static std::shared_ptr<const BiographyProfileSource> begin(SessionOwner&);
    const f10::BiographyContext& context() const noexcept { return context_; }
    bool current(const f10::BiographyContext& context) const noexcept {
        return !activation_.expired() && context == context_;
    }
private:
    BiographyProfileSource(f10::BiographyContext context, std::weak_ptr<const int> activation)
        : context_(std::move(context)), activation_(std::move(activation)) {}
    const f10::BiographyContext context_;
    const std::weak_ptr<const int> activation_;
};
}

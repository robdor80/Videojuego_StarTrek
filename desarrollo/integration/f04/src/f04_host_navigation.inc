namespace trek::host::nav_bridge {

std::uint32_t create(const char* cls, const F04PopulationConfig& config,
                     const NavalBootstrap& bootstrap, F04Session** out) noexcept {
    auto result = f04_create_population(1, cls, &config, out);
    if (result != F04_OK) return result;
    auto* session = *out;
    F04Handles handles{};
    result = f04_handles(session, &handles);
    if (result == F04_OK) {
        result = call(session, [&] {
            nav_bootstrap(*session->c, *session->content.catalog(), handles.ship.id, config.crew, bootstrap);
            need(schema(*session->c), F04_INTERNAL);
            return F04_OK;
        });
    }
    if (result != F04_OK) {
        f04_destroy(session);
        *out = nullptr;
    }
    return result;
}

std::uint32_t read(F04Session* session, F04Ref principal, NavigationView& out) noexcept {
    out = {};
    F04Handles handles{};
    const auto status = f04_handles(session, &handles);
    if (status != F04_OK) return status;
    return call(session, [&] {
        need(principal.scope == handles.ship.scope, F04_SCOPE);
        need(observer(session, principal), F04_DENIED);
        const auto& campaign = *session->c;
        const auto& world = campaign.world;
        const EntityId ship{handles.ship.id};
        const auto known = Visibility::project(world, EntityId{principal.id});
        const auto knows = [&](EntityId subject) {
            return nav_granted(world, principal.id, NAV_KNOWS, subject) && known.knows(subject);
        };
        const auto origin = world.container_of(ship).container;
        const auto* location = known.find({ship, FactKind::containment});
        const bool knows_origin = location && location->present && location->reference == origin &&
                                 nav_granted(world, principal.id, NAV_OWN_ORIGIN, ship) && knows(origin);
        const auto publications = all(world, "nav_chart");
        const bool knows_chart = !publications.empty() && knows(EntityId{publications.front()});

        const auto revision = world.revision();
        NavigationView view;
        // The pinned Core has one WorldState revision, including containment and knowledge.
        view.revision = {revision, revision, revision, campaign.time.now(),
                         knows_chart ? chart_data::publication : ""};
        std::set<std::string_view> visible_places;
        for (const auto& place : chart_data::places) {
            const auto records = all(world, nav_definition(place).c_str());
            if (records.empty()) continue;
            const EntityId id{records.front()};
            if (knows_origin && id == origin) view.location = place;
            if (knows_chart && knows(id)) {
                visible_places.insert(place.id);
                view.places.push_back(place);
            }
        }
        for (const auto& entry : chart_data::edges) {
            if (!visible_places.contains(entry.origin) || !visible_places.contains(entry.destination)) continue;
            const auto records = all(world, nav_definition(entry).c_str());
            if (!records.empty() && knows(EntityId{records.front()})) view.edges.push_back(entry);
        }
        out = std::move(view);
        return F04_OK;
    });
}

#ifdef F04_HOST_NAVIGATION_TESTING
std::uint32_t revoke_chart(F04Session* session, F04Ref principal) noexcept {
    return call(session, [&] {
        need(observer(session, principal), F04_DENIED);
        const auto publications = all(session->c->world, "nav_chart");
        need(!publications.empty());
        need(session->c->world.revoke_fact(EntityId{principal.id}, {EntityId{publications.front()}})
             == KnowledgeChange::applied);
        return F04_OK;
    });
}
#endif

} // namespace trek::host::nav_bridge

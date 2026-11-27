// Included only by the HOST composition, inside the F04 domain namespace.
using namespace trek::host;
constexpr std::array<Field, 6> chart_stamp_fields{
    NAV_STAMP_0, NAV_STAMP_1, NAV_STAMP_2, NAV_STAMP_3, NAV_STAMP_4, NAV_STAMP_5
};

std::string nav_definition(const ChartPlace& place) { return "nav_place_" + place.id; }
std::string nav_definition(const ChartEdge& edge) { return "nav_edge_" + edge.id; }

void nav_catalog(std::vector<ContentDefinitionInput>& definitions) {
    const auto add = [&](const std::string& name) {
        definitions.emplace_back(ResourceDefinition{*DefinitionId::parse("trek.f04:" + name),
                                                     *ResourceKind::parse("structural")});
    };
    add("nav_chart");
    for (const auto& place : chart_data::places) add(nav_definition(place));
    for (const auto& edge : chart_data::edges) add(nav_definition(edge));
}

bool nav_resource(const WorldState& world, U id) {
    const auto* definition = world.definition_of(EntityId{id});
    return definition && definition->value().starts_with("trek.f04:nav_");
}

bool nav_shape(const WorldState& world, U id, std::set<U>& fields) {
    if (!nav_resource(world, id)) return false;
    if (type(world, id, "nav_chart")) fields.insert(chart_stamp_fields.begin(), chart_stamp_fields.end());
    return true;
}

bool nav_granted(const WorldState& world, U person, U kind, EntityId subject) {
    const auto relations = world.relations_from(EntityId{person});
    return std::any_of(relations.begin(), relations.end(), [&](const auto& relation) {
        return relation.kind == RelationKind{kind} && relation.target == subject;
    });
}

bool nav_knowledge(const WorldState& world, U person, const KnownFact& fact) {
    if (!fact.present) return false;
    const auto subject = fact.key.subject;
    if (fact.key.kind == FactKind::existence &&
        nav_granted(world, person, NAV_KNOWS, subject)) return true;
    if (!nav_granted(world, person, NAV_OWN_ORIGIN, subject)) return false;
    return fact.key.kind == FactKind::existence ||
        (fact.key.kind == FactKind::containment &&
         world.container_of(subject).container == fact.reference &&
         nav_granted(world, person, NAV_KNOWS, fact.reference));
}

void nav_revoke_departing_observer(Campaign& campaign, U person) {
    const EntityId observer_id{person};
    std::vector<EntityRelation> grants;
    for (const auto& relation : campaign.world.relations_from(observer_id))
        if (relation.kind == RelationKind{NAV_KNOWS} || relation.kind == RelationKind{NAV_OWN_ORIGIN})
            grants.push_back(relation);
    for (const auto& grant : grants) {
        const auto result = campaign.world.revoke_fact(observer_id, {grant.target});
        need(result == KnowledgeChange::applied || result == KnowledgeChange::no_change, F04_INTERNAL);
        erase(campaign, grant);
    }
}

bool nav_schema(const WorldState& world, U ship) {
    const EntityId ship_id{ship};
    const auto origin = world.container_of(ship_id).container;
    const auto publications = all(world, "nav_chart");
    if (publications.size() > 1) return false;
    const bool published = !publications.empty();
    if (published) {
        for (std::size_t i = 0; i < chart_stamp_fields.size(); ++i)
            if (val(world, publications.front(), chart_stamp_fields[i]) != chart_data::stamp[i]) return false;
    }
    bool found_origin = !origin.is_valid();
    for (const auto& place : chart_data::places) {
        const auto ids = all(world, nav_definition(place).c_str());
        if (ids.size() > 1 || (published && ids.empty())) return false;
        if (!ids.empty()) {
            const EntityId id{ids.front()};
            if (!published && id != origin) return false;
            found_origin |= id == origin;
        }
    }
    for (const auto& edge : chart_data::edges)
        if (all(world, nav_definition(edge).c_str()).size() != static_cast<std::size_t>(published)) return false;
    if (!found_origin) return false;
    return true;
}

void nav_bootstrap(Campaign& campaign, const ContentCatalog& catalog, U ship, U crew,
                   const NavalBootstrap& bootstrap) {
    if (!bootstrap.origin && !bootstrap.chart_publication && bootstrap.observers.empty()) return;
    auto& world = campaign.world;
    const bool published = bootstrap.chart_publication.has_value();
    need(!published || *bootstrap.chart_publication == chart_data::publication);
    std::map<std::string_view, U> places, edges;
    U chart = 0;
    if (published) {
        chart = make(campaign, catalog, "nav_chart");
        for (std::size_t i = 0; i < chart_stamp_fields.size(); ++i)
            set(campaign, chart, chart_stamp_fields[i], chart_data::stamp[i]);
    }
    for (const auto& place : chart_data::places) {
        if (published || (bootstrap.origin && place.id == *bootstrap.origin))
            places.emplace(place.id, make(campaign, catalog, nav_definition(place).c_str()));
    }
    U origin = 0;
    if (bootstrap.origin) {
        const auto place = places.find(*bootstrap.origin);
        need(place != places.end());
        origin = place->second;
        action(campaign, ship, PlaceEntityAction{EntityId{ship}, EntityId{origin}});
    }
    if (published) {
        for (const auto& entry : chart_data::edges)
            edges.emplace(entry.id, make(campaign, catalog, nav_definition(entry).c_str()));
    }

    std::vector<U> crew_people;
    for (const U p : all(world, "person"))
        if (member(world, p) && val(world, p, CATEGORY) == 1) crew_people.push_back(p);
    need(crew_people.size() == crew, F04_INTERNAL);
    std::set<U> observers;
    for (const auto& grant : bootstrap.observers) {
        need(grant.crew_ordinal < crew_people.size() && observers.insert(grant.crew_ordinal).second);
        need(grant.knows_chart ? chart != 0 : grant.places.empty() && grant.edges.empty());
        need(!grant.knows_own_location || origin != 0);
        need(grant.places.size() <= places.size() && grant.edges.size() <= edges.size());
        const U person = crew_people[static_cast<std::size_t>(grant.crew_ordinal)];
        const auto learn = [&](U subject, FactKind kind = FactKind::existence) {
            const auto result = world.learn_fact(EntityId{person}, {EntityId{subject}, kind});
            need(result == KnowledgeChange::applied || result == KnowledgeChange::no_change, F04_INTERNAL);
        };
        const auto authorize = [&](U subject) {
            edge(campaign, person, NAV_KNOWS, subject);
            learn(subject);
        };
        if (grant.knows_chart) authorize(chart);
        for (const auto& id : grant.places) {
            const auto place = places.find(id);
            need(place != places.end());
            authorize(place->second);
        }
        for (const auto& id : grant.edges) {
            const auto entry = edges.find(id);
            need(entry != edges.end());
            authorize(entry->second);
        }
        if (grant.knows_own_location) {
            authorize(origin);
            edge(campaign, person, NAV_OWN_ORIGIN, ship);
            learn(ship);
            learn(ship, FactKind::containment);
        }
    }
}

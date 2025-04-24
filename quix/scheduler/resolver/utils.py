from quix.scheduler.blueprint import Blueprint
from quix.scheduler.owner import Owner


def isolate_related_groups(blueprints: list[Blueprint]) -> list[set[Blueprint]]:
    groups: dict[Owner, set[Owner]] = {}
    roots: set[Owner] = set()
    owner2blueprint: dict[Owner, Blueprint] = {}

    for blueprint in blueprints:
        sub_owners, root = blueprint.get_owners(), blueprint.root

        owner2blueprint[root] = blueprint
        roots.difference_update(sub_owners)
        roots.add(root)

        if existing_set := groups.get(root, None):
            for owner in sub_owners.difference(existing_set):
                groups[owner] = existing_set

            existing_set.update(sub_owners)
            continue

        for owner in sub_owners:
            groups[owner] = sub_owners

    return [{owner2blueprint[owner] for owner in groups[root]} for root in roots]

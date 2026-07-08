from django import template

register = template.Library()

GAME_GROUPS = {
    'sound_games': [
        ('Giggle Generators', ['microchallenge']),
        ('Choice Chaos', ['wyrquestion']),
        ('Mimic Mayhem', ['soundfx']),
        ('Lip-Sync Legends', ['lipsyncsound']),
    ],
    'creative_games': [
        ('Tale Twisters', ['storytwist', 'storyending', 'storysession']),
        ('Funny Face Factory', ['faceprompt']),
        ('Doodle Dash', ['doodlesubject', 'doodleemotion', 'doodleaccessory', 'doodledrawing']),
    ],
    'active_games': [
        ('Wild Roles', ['rolecharacter', 'rolesetting', 'roleactivity']),
        ('Highway Hijinks', ['cargame', 'tripsession']),
    ],
}


@register.filter
def game_groups(app):
    groups = []
    raw = GAME_GROUPS.get(app['app_label'], [])
    name_map = {m['object_name'].lower(): m for m in app['models']}
    used = set()
    for group_name, model_names in raw:
        models_in_group = []
        for mn in model_names:
            if mn in name_map:
                models_in_group.append(name_map[mn])
                used.add(mn)
        if models_in_group:
            groups.append((group_name, models_in_group))
    remaining = [m for m in app['models'] if m['object_name'].lower() not in used]
    if remaining:
        groups.append((None, remaining))
    return groups

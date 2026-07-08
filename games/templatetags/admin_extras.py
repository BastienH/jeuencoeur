from django import template

register = template.Library()

MODEL_MOVES = {
    'userprofile': {'from_app': 'games', 'to_app': 'auth'},
    'prompt': {'from_app': 'games', 'to_app': 'sound_games'},
    'storyseed': {'from_app': 'games', 'to_app': 'creative_games'},
    'soundeffect': {'from_app': 'games', 'to_app': 'sound_games'},
}

APP_RENAME = {
    'auth': 'User Management',
}

GAME_GROUPS = {
    'games': [
        (None, ['genre', 'favorite', 'analyticsevent']),
        ('Communications', ['contactmessage', 'gamesuggestion']),
    ],
    'sound_games': [
        ('Giggle Generators', ['microchallenge', 'prompt']),
        ('Choice Chaos', ['wyrquestion']),
        ('Mimic Mayhem', ['soundfx']),
        ('Lip-Sync Legends', ['lipsyncsound', 'soundeffect']),
    ],
    'creative_games': [
        ('Tale Twisters', ['storytwist', 'storyending', 'storysession', 'storyseed']),
        ('Funny Face Factory', ['faceprompt']),
        ('Doodle Dash', ['doodlesubject', 'doodleemotion', 'doodleaccessory', 'doodledrawing']),
    ],
    'active_games': [
        ('Wild Roles', ['rolecharacter', 'rolesetting', 'roleactivity']),
        ('Highway Hijinks', ['cargame', 'tripsession']),
    ],
}


@register.filter
def reorganize_app_list(app_list):
    app_list = list(app_list)

    for model_lower, move in MODEL_MOVES.items():
        found_model = None
        src_idx = None
        model_idx = None

        for ai, app in enumerate(app_list):
            if app['app_label'] == move['from_app']:
                for mi, m in enumerate(app['models']):
                    if m['object_name'].lower() == model_lower:
                        found_model = m
                        src_idx = ai
                        model_idx = mi
                        break
            if found_model:
                break

        if found_model:
            app_list[src_idx]['models'].pop(model_idx)
            for ai, app in enumerate(app_list):
                if app['app_label'] == move['to_app']:
                    app_list[ai]['models'].append(found_model)
                    break

    for app in app_list:
        if app['app_label'] in APP_RENAME:
            app['name'] = APP_RENAME[app['app_label']]

    return app_list


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

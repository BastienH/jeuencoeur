---
name: game-pattern
description: End-to-end structure for adding/modifying a game in coeuretjeu
---

## Anatomy of a game

Each game spans 4 layers:

### 1. View (`games/urls.py` + app views)
- URL pattern is defined in `games/urls.py` (single central urls file).
- View imports from the appropriate app: `sound_games.views`, `creative_games.views`, `active_games.views`.
- Each view calls `activate(lang)`, gets `Genre` via `get_object_or_404(Genre, slug='...')`, and renders a template.
- Game-specific models reside in the app's `models.py` (e.g. `CarGame`, `TripSession` in `active_games.models`).

### 2. Template (`templates/<app>/<game>.html`)
- Extends `base.html`.
- Loads `{% load i18n static genre_tags %}`.
- Links game JS via `{% block extra_js %}`.
- Uses `{% trans %}` for all user-facing strings.
- Genre name rendered with `{{ genre|genre_name:lang }}`.

### 3. JS (`static/<app>/<game>.js`)
- IIFE-wrapped, defines `promptCount = 0`.
- Calls `checkPlayLimit('game_module')` after each action.
- Sets `window.resetCurrentGameCounter`.
- All `fetch()` calls have `showError()` in catch.
- Uses `document.documentElement.lang` for inline translations.

### 4. Context processor (`games/context_processors.py`)
- `all_genres_data` serializes all non-empty Genre objects for the suggestion overlay.
- Registered in `jeuencoeur/settings.py` `TEMPLATES.OPTIONS.context_processors`.

## Adding a new game
1. Create model(s) in the appropriate app.
2. Add view(s) in the app's `views.py`.
3. Add URL pattern(s) in `games/urls.py`.
4. Create template in `templates/<app>/`.
5. Create JS file in `static/<app>/` following game-js patterns.
6. Create a Genre entry with `game_module` set to the app module string.
7. Add tests in the app's `tests.py`.
8. Run `python manage.py test` and verify all pass.
9. Update `FEATURES.md` game table if the game is new.
10. Append to `.opencode/skills/game-pattern/features/<game>.md` if the game has unique architecture.

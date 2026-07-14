# Features

Developer reference for app capabilities and architecture decisions.
For user-facing descriptions, see `templates/about.html`.

## Games

9 games across 3 categories, all following the Genre + model pattern.

| Game | Category | Module | Description |
|------|----------|--------|-------------|
| Giggle Generators | Sound | `giggle_generators` | Random silly sound challenges |
| Choice Chaos | Sound | `choice_chaos` | Would-you-rather debates |
| Mimic Mayhem | Sound | `mimic_mayhem` | Imitate sounds from prompts |
| Lip-Sync Legends | Sound | `lip_sync_legends` | Act out sounds without speaking |
| Tale Twisters | Creative | `tale_twisters` | Collaborative story building |
| Funny Face Factory | Creative | `funny_face_factory` | Silly face drawing prompts |
| Doodle Dash | Creative | `doodle_dash` | Draw prompts with accessories |
| Wild Roles | Active | `wild_roles` | Spin random character + setting + activity |
| Highway Hijinks | Active | `highway_hijinks` | Backseat road trip games |

**Architecture:** Each game has a Genre entry, a view, a template, and a JS file. Models live in their respective app (`sound_games`, `creative_games`, `active_games`). See `game-pattern` skill for the full recipe.

## PWA

Installable Progressive Web App with offline support.

- **Manifest:** `static/manifest.json` — teal theme (#26A69A), cream background
- **Service worker:** `static/sw.js` — vanilla SW, no Workbox. Network-first for HTML, cache-first for static assets. Precaches icons and manifest on install.
- **Install prompt:** `static/pwa.js` — platform-adaptive. Chromium uses `beforeinstallprompt`. iOS shows share-sheet instructions. Android shows menu instructions. State tracked in localStorage.
- **Offline fallback:** `templates/offline.html` — served when no cache is available

**Decision:** Vanilla SW over Workbox to keep the tooling footprint zero. No build step required. Cache versioning via `CACHE_VERSION` constant in `sw.js`.

## Vendor Bundling

Tailwind CSS and htmx are bundled locally in `static/vendor/`.

- `static/vendor/tailwind.js` — Tailwind play build (~400KB)
- `static/vendor/htmx.min.js` — htmx 2.0.3 (~14KB)

**Decision:** Removed CDN dependency to enable full offline support. Both files are cached by the service worker on first visit.

## i18n

3 languages: English, French, Spanish.

- URL pattern: `/{lang}/...` (e.g. `/en/games/`, `/fr/games/`)
- Language activation: `activate(lang)` in every view
- Template strings: `{% trans "..." %}` and `{{ var|filter:lang }}`
- Model fields: `text_en`, `text_fr`, `text_es` (or `name_en`, `name_fr`, `name_es`)
- Context helper: `get_<field>(lang)` method on models, falls back to English
- Language switcher: dropdown in header, preserves current page path

**Decision:** Field-per-language over Django's built-in i18n because game content is user-facing and needs per-language editing in admin. Adding a language = adding a field, no code changes.

## Auth

Simple username/password authentication via Django's built-in `UserCreationForm` and `AuthenticationForm`.

- Login: `/{lang}/login/`
- Signup: `/{lang}/signup/`
- Logout: `/{lang}/logout/`
- Profile: `/{lang}/profile/` (favorites list)

**Decision:** No social auth, no email verification. Low friction per app-spirit. Favorites are tied to authenticated users.

## Analytics

Lightweight event tracking via `navigator.sendBeacon`.

- Events tracked: `page_view`, `genre_enter`, `genre_abandon`, `prompt_reroll`
- Endpoint: `/{lang}/analytics/track/`
- Model: `AnalyticsEvent` in `games/models.py`
- JS: `trackEvent()` in `templates/base.html` inline script

**Decision:** No third-party analytics SDK. sendBeacon is fire-and-forget, doesn't block page navigation. Respects Do Not Track.

## Admin

Django admin with custom model grouping.

- Custom `app_list.html` template groups models by game category
- Grouping defined in `games/templatetags/admin_extras.py` `GAME_GROUPS`
- Registration uses `@admin.register()` decorator

## About Page

Public feature discovery page at `/{lang}/about/`.

- View: `games/views.py` `about()` — passes active genres
- Template: `templates/about.html` — shows game grid, capability cards (offline, i18n, install), and contribute link
- No JS needed, purely static content + genre data

## Offline Page

Standalone fallback at `/offline/` for when no cache is available.

- Route: `jeuencoeur/urls.py` (root level, no lang prefix)
- Template: `templates/offline.html` — self-contained with inline CSS
- Served by the service worker when navigation fetch fails

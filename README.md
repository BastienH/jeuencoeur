# Jeu en coeur

A playful, family-oriented web app with 9 games designed to spark laughter and connection between parents and kids. Built with Django 6 + HTMX + TailwindCSS.

## Games

| Game | Category | Description |
|------|----------|-------------|
| **Giggle Generator** | Sound | Quick silly prompts — waddle like a penguin, act like a judge. |
| **Choice Chaos** | Sound | "Would You Rather" questions with confetti and auto-advance. |
| **Tale Twister** | Creative | Collaborative story building: seed → twist → ending. |
| **Funny Face Factory** | Creative | Silent selfie challenges with camera capture & PNG download. |
| **Doodle Party** | Creative | Random art prompts with a digital whiteboard. |
| **Mimic Mania** | Sound | Noise challenges with a visual volume meter. |
| **Lip Sync Battle** | Sound | Act out sound effects in normal or reverse mode. |
| **Wild Roles** | Active | Physical charades: random character + setting + activity with rerolls. |
| **Highway Hijinks** | Active | 13+ car games for road trips, GPS trip tracking. |

## Quick start

```bash
cp .env.example .env
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed
python manage.py runserver
```

Open http://localhost:8000.

## Architecture

- **Django apps:** `games/` (core: genres, auth, analytics, hub, print decks), `sound_games/`, `creative_games/`, `active_games/`
- **Frontend:** Server-rendered Django templates with vanilla JS per game, HTMX for partial swaps
- **i18n:** English / French / Spanish via `django.middleware.locale.LocaleMiddleware`
- **Static files:** Whitenoise with manifest compression; project-level `static/` directory
- **Media (prod):** Optional S3 via django-storages

## Language support

Change language via the dropdown in the top-right corner of the hub. Translation `.po`/`.mo` files live in `locale/{fr,es}/LC_MESSAGES/`.

## Deployment

Set `DEBUG=False`, configure `DATABASE_URL`, `SECRET_KEY`, and `ALLOWED_HOSTS` in `.env`. Enable S3 with `USE_S3=True` and the corresponding AWS vars.

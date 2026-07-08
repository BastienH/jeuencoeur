---
name: pending-admin-moves
description: Planned admin reorganization — move models between app groups in the Django admin
---

## What to do

In `games/templatetags/admin_extras.py`:

1. Add a `reorganize_app_list` filter that moves models between apps:
   - `userprofile` → from `games` to `auth` (rename `auth` app to "User Management")
   - `prompt` → from `games` to `sound_games`
   - `storyseed` → from `games` to `creative_games`
   - `soundeffect` → from `games` to `sound_games`

2. Update `GAME_GROUPS`:
   - Add `'games': [(None, ['genre', 'favorite', 'analyticsevent'])]`
   - Giggle Generators: `['microchallenge', 'prompt']`
   - Lip-Sync Legends: `['lipsyncsound', 'soundeffect']`
   - Tale Twisters: `['storytwist', 'storyending', 'storysession', 'storyseed']`

3. In `templates/admin/app_list.html`, change:
   ```django
   {% for app in app_list %}
   ```
   to:
   ```django
   {% for app in app_list|reorganize_app_list %}
   ```

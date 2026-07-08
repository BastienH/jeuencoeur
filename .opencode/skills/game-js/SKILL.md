---
name: game-js
description: Shared JavaScript patterns used across all game JS files in coeuretjeu
---

## Shared functions (defined in `static/shared.js`)

### `window.showError(msg)`
Creates a red toast at the bottom of the screen that auto-removes after 3s.

### `window.showSuggestionOverlay(currentModule)`
Shows a full-screen overlay suggesting 3 random other games after 7 prompts.
- Reads genre data from `<script id="genres-data">` JSON.
- Filters out the current game module.
- Has "Keep playing" (resets counter) and "Stop playing" (links to hub) buttons.

### `window.resetCurrentGameCounter()`
Resets `promptCount` to 0 (each game sets its own implementation).

## Per-game pattern

Each game JS file (e.g. `static/sound_games/giggle.js`):
1. Wraps in IIFE: `(function() { ... })();`
2. Defines local `promptCount = 0`.
3. On each action (next, spin, save, etc.): `promptCount++; checkPlayLimit('game_module');`
4. Implements `window.resetCurrentGameCounter = function() { promptCount = 0; };`
5. Uses `checkPlayLimit(currentModule)` — at 7 prompts, shows suggestion overlay.
6. All `fetch().catch()` must call `showError()` — never silent.

## Translations in JS

```javascript
var lang = document.documentElement.lang || 'en';
var msg = lang === 'fr' ? 'Texte français'
       : lang === 'es' ? 'Texto español'
       : 'English text';
```

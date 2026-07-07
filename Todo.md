# Functional Test Findings

All Critical and High items fixed. Remaining Medium/Low items:

## 🟡 Medium (edge cases & polish)

### 1. All games — silent fetch failures
- Every `.catch(() => {})` swallows network errors. User gets no feedback.

### 2. Highway Hijinks — `trip_active` never passed to template
- View doesn't set `trip_active`, so `{% if not trip_active %}` is always True.

### 3. Highway Hijinks — no validation on progress input
- User can enter negative numbers, >100, or non-numeric with no feedback.

### 4. Wild Roles — timer never triggers action at 0
- Countdown just shows "0" forever once it reaches 0.

### 5. Funny Face Factory — `<a download>` with data URL may fail on iOS Safari
- Mobile Safari may open in new tab instead of downloading.

### 6. Giggle Generator — "Go!" button doesn't increment prompt count
- Counter only increments on Skip/Next, not on completing a full countdown.

## 🟢 Low (minor / cosmetic)

### 7. Mimic Mayhem — mic meter runs forever until "Next Sound" clicked
- AudioContext animation frame never stops except on htmx swap.

### 8. Wild Roles — "Switch Roles" uses `spinBtn.click()` instead of API call
- Poor abstraction; triggers full "Spinning..." delay.

### 9. Doodle Dash — "Reroll" triggers full page reload
- `window.location.reload()` loses current drawing with no confirmation.

### 10. Tale Twister — save title is always empty
- `{ title: '' }` hardcoded in JS.

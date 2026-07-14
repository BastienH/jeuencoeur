---
name: feature-log
description: Keep FEATURES.md and the about page in sync with app capabilities
---

Use this skill after implementing a feature that adds or changes a user-visible capability or architectural decision.

## What to update

### User-visible features
Update `templates/about.html` if the new feature should be discoverable by users (e.g., a new game category, a new capability like "works offline").

### Architecture decisions
Update `FEATURES.md` if the feature introduces a new pattern, changes an existing one, or involves non-obvious tradeoffs. Describe **what exists and why**, not what changed.

### Games
When adding or modifying a game, also update the game table in `FEATURES.md` and append a note to `.opencode/skills/game-pattern/features/<game>.md` if the game has unique architectural details.

## What NOT to update

- Don't duplicate git history. Commit messages already capture what changed and when.
- Don't update for bug fixes, minor tweaks, or content changes.
- Don't update for changes that don't affect the app's capabilities or architecture.

## Template

For `FEATURES.md` entries, use this structure:

```markdown
## Feature Name

What it does. Key files. Why this approach was chosen.
```

Keep it concise — a few sentences per feature. Link to skills for full details.

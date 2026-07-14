---
name: app-spirit
description: The overall spirit, values, and design philosophy of Jeu en Coeur — guides development decisions, content tone, and feature scoping
---

## What this app is

Jeu en Coeur is a playful, family-oriented web app with games designed to
spark laughter and connection between parents and kids. The app is a
CATALYST for off-screen play — the screen starts the fun, then families
put the device down and play together.

## Who it's for

- Parents looking for low-pressure, fun ways to connect with their kids
- Kids ages 3-10+ (age-inclusive)
- Multilingual families worldwide — not limited to any set of languages

## Core values

### 1. App as prop, not play

The screen is the starter, not the activity. A game should get families
laughing, then they put the device down. If the app IS the activity,
it's not aligned with the spirit.

### 2. Low friction

One tap and you're playing. Zero decision fatigue. No sign-up walls,
no complex menus, no loading screens. The path from "I'm bored" to
"we're playing" must be as short as possible.

### 3. Language-agnostic by design

3 languages at launch (EN/FR/ES), but the architecture must support
adding any language with zero code changes. Models use `text_<lang>`
fields. The i18n system is built to scale — adding a 4th or 20th
language is a content task, not a dev task.

### 4. Playful over polished

Silly, goofy, absurd is the default tone. The app should feel
handmade and warm, never corporate or sterile. Rounded corners,
pastel colors, emoji icons — whimsy over perfection.

### 5. Gamified but non-competitive

Confetti, emoji reactions, silly awards, surprise overlays — YES.
Real scoring, leaderboards, head-to-head competition — NO.
Gamification should feel like a celebration, not a contest.

### 6. Age-inclusive

Every game must work for a 3-year-old AND a 10-year-old. Simple
language, large touch targets (44px+), graceful degradation.

### 7. Offline-first

The app should work as much as possible without a connection.
Prompt data can be cached client-side. Core gameplay must never
require a network request. Graceful fallbacks when offline.

## Visual design philosophy

From Design.md:

- Whimsical, playful, family-oriented
- Soft color palette: teal, pastel yellow, muted coral, pale pink, cream
- Bold, rounded, chunky sans-serif typography
- Flat, vector-style illustrations with hand-drawn elements
- Highly rounded corners on everything
- Clean but soft, approachable, "fun" — never corporate

## Development guidelines

- "Does this get families OFF the screen, or keep them ON it?"
- Prefer simple, server-rendered patterns over complex JS
- HTMX for partial swaps, vanilla JS for device APIs
- Mobile-first, touch-friendly (44px+ buttons)
- Every game must work without camera/mic/permissions
- No third-party JS libraries unless absolutely necessary
- All user-facing strings use `{% trans %}` — no hardcoded text
- Dynamic content uses model fields with `get_<field>(lang)` pattern
- New content types should follow the Genre + model pattern

## Content tone guide

- Silly, absurd, playful — never serious or preachy
- Short, punchy prompts — kids have short attention spans
- Encouraging, not competitive
- Translations must be culturally curated, not machine-translated
- Each language version should feel natural, not translated

## Scope boundaries

- In: Off-screen play, physical activity, conversation, creativity
- Out: Monetization, social login, complex gamification, screen-heavy mechanics
- Grey zone: PDFs, timers, audio — allowed if they support off-screen play

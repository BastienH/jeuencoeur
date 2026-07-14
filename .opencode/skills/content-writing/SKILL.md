---
name: content-writing
description: How to write, format, and import game content (prompts, questions, challenges) for any game in coeuretjeu
---

Use this skill when creating, editing, or bulk-importing game content for any game in coeuretjeu. Also use when asked about content strategy, translation guidelines, or CSV import format for game data.

## Style brief

### Voice

Direct and punchy. Gets to the choice fast. No filler words.

- **Good:** "Spaghetti hair or pickle fingers?"
- **Bad:** "If you could have one of the following magical transformations, which would you prefer: having spaghetti as hair or having fingers made of pickles?"

### Humor

Mix of two modes, chosen per category:

- **Absurdist/surreal:** "Sneeze glitter" / "Your farts smell like roses"
- **Relatable kid scenarios:** "Have homework forever or clean your room forever"

### Age tiering

Content MUST be clearly tiered by language complexity:

| Age group | Language rules | Example |
|-----------|---------------|---------|
| **3-6** | Simple words, concrete concepts, very silly. Max 8 words per option. | "Eat only chocolate 🍫" / "Eat only pizza 🍕" |
| **7-10** | Can be wittier, more imaginative. Max 12 words per option. | "Have a chef who makes you breakfast every morning 👨‍🍳" |
| **11+** | Slightly more nuanced, funnier. Max 15 words per option. | "Always be 10 minutes late but never miss anything ⏳" |
| **all** | Universal appeal, simple enough for kids, fun for adults. Max 10 words per option. | "Fly like a bird ✈️" / "Swim like a fish 🐠" |

### Cultural adaptation

Translations must be **fully culturally adapted**, not literal:

- Food references become local favorites (croissants, churros, tortilla)
- Names and places change per culture
- Jokes should land natively in each language
- Idioms get replaced, not translated
- Each language version should feel natural, not translated

### Emoji

Light and occasional. Adds personality without cluttering. One emoji per option max, only when it adds visual context. Never emoji-only communication.

## Model catalog

### Genre-linked models (have `genre` FK)

| Model | App | Text fields | Metadata fields |
|-------|-----|-------------|-----------------|
| **Prompt** | games | `text_en`, `text_fr`, `text_es` | `category` (nullable) |
| **StorySeed** | games | `text_en`, `text_fr`, `text_es` | `category` (nullable) |
| **MicroChallenge** | sound_games | `text_en`, `text_fr`, `text_es` | `age_group`, `energy_level` (calm/wild), `duration_seconds` |
| **WYRQuestion** | sound_games | `option_a_en`, `option_a_fr`, `option_a_es`, `option_b_en`, `option_b_fr`, `option_b_es` | `category`, `age_group` |
| **SoundFX** | sound_games | `name` | `category`, `audio_file` |
| **LipSyncSound** | sound_games | `description_en`, `description_fr`, `description_es` | `name`, `audio_file` |
| **StoryTwist** | creative_games | `text_en`, `text_fr`, `text_es` | — |
| **StoryEnding** | creative_games | `text_en`, `text_fr`, `text_es` | — |
| **FacePrompt** | creative_games | `text_en`, `text_fr`, `text_es` | `category`, `age_group` |
| **CarGame** | active_games | `name_en`, `name_fr`, `name_es`, `instructions_en`, `instructions_fr`, `instructions_es` | `min_age` |

### Standalone models (no genre FK — combinatorial/shared)

| Model | App | Fields |
|-------|-----|--------|
| **DoodleSubject** | creative_games | `text_en`, `text_fr`, `text_es` |
| **DoodleEmotion** | creative_games | `text_en`, `text_fr`, `text_es` |
| **DoodleAccessory** | creative_games | `text_en`, `text_fr`, `text_es` |
| **RoleCharacter** | active_games | `text_en`, `text_fr`, `text_es` |
| **RoleSetting** | active_games | `text_en`, `text_fr`, `text_es` |
| **RoleActivity** | active_games | `text_en`, `text_fr`, `text_es` |

## CSV format templates

The `genre` column uses `Genre.name` (e.g., `"Choice Chaos"`), NOT the slug. The `GenreForeignKeyWidget` in `games/resources.py` looks up by `name`.

### Simple text models (Prompt, StorySeed, StoryTwist, StoryEnding)

```csv
genre,category,text_en,text_fr,text_es
Giggle Generators,Mealtime,Make a funny food face,Fais une tête de nourriture drôle,Haz una cara graciosa de comida
```

### WYRQuestion (Choice Chaos)

```csv
genre,category,age_group,option_a_en,option_b_en,option_a_fr,option_b_fr,option_a_es,option_b_es
Choice Chaos,silly,3-6,Have spaghetti hair 🍝,Have pickle fingers,Avoir des cheveux en spaghetti 🍝,Avoir des doigts en cornichon,Tener cabello de espaguetis 🍝,Tener dedos de pepinillo
```

### MicroChallenge (Giggle Generators)

```csv
genre,age_group,energy_level,duration_seconds,text_en,text_fr,text_es
Giggle Generators,3-6,calm,20,Make a quiet mouse sound,Fais un bruit de souris tout doux,Haz un sonido de ratón muy suave
```

### FacePrompt (Funny Face Factory)

```csv
genre,age_group,category,text_en,text_fr,text_es
Funny Face Factory,3-6,silly,A dinosaur who just ate a lemon,Un dinosaure qui vient de manger un citron,Un dinosaurio que acaba de comer un limón
```

### CarGame (Highway Hijinks)

```csv
genre,min_age,name_en,name_fr,name_es,instructions_en,instructions_fr,instructions_es
Highway Hijinks,all,I-Spy,Je vois je vois,Yo veo veo,Look out the window and find something blue,Regarde par la fenêtre et trouve quelque chose de bleu,Mira por la ventana y encuentra algo azul
```

## Import workflow

1. Write content to a CSV file in the app directory (e.g., `sound_games/choice_chaos_content.csv`)
2. Go to Django Admin → App → Model → **Import**
3. Upload the CSV
4. Confirm column mapping and start import
5. Bulk-edit `genre` if needed (or include it in CSV)

**Important:** `_BaseResource` excludes `id` and `created_at`. The `import_id_fields` is empty, so re-importing the same CSV will create duplicates. Delete old rows first or use "Update" mode with a unique field.

## Content strategy

### Volume targets

| Target | Description |
|--------|-------------|
| **MVP minimum** | 15-20 items per model |
| **Good** | 30-50 items per model |
| **Rich** | 80-100+ items per model |

### Age group distribution

When a model has `age_group`:
- **Roughly equal** across `3-6`, `7-10`, `11+`
- Plus ~15% as `all` (universal appeal)
- Example for 112 items: 32 + 32 + 32 + 16

### Category distribution

When a model has `category`:
- **Roughly equal** across categories
- Aim for 3-5 items per category per age group
- Example: 8 categories × 14 each = 112 total

## Quality checklist

Every content item should pass ALL of these:

- [ ] **Under 15 words** per text field (shorter is better)
- [ ] **Uses an action verb** — "Fly", "Eat", "Build", "Explore"
- [ ] **Makes sense to a 3-year-old** — even if targeted at older kids
- [ ] **Would make someone laugh** — if it's not funny, rewrite it
- [ ] **Works in all 3 languages** — test the concept, not just the translation
- [ ] **No preaching** — never teaches a lesson, never moralizes
- [ ] **No screen references** — content should work offline
- [ ] **Gender-neutral** — avoid gendered language unless the model requires it

### Bad → Good examples

| Bad | Why | Good |
|-----|-----|------|
| "Would you rather be able to fly or be invisible?" | Too long, formal | "Fly or be invisible?" |
| "Have a pet that can talk" | Vague | "Have a talking parrot 🦜" |
| "Only eat vegetables forever" | Preachy (vegetables are good!) | "Only eat broccoli forever 🥦" |
| "Read minds or see the future?" | Fine but bland | "Read minds 🧠 or see the future 🔮?" |

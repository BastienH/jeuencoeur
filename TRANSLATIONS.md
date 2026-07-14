# Translations Guide

This project supports three languages: **English** (en), **French** (fr), and **Spanish** (es).

There are three distinct translation layers:

1. **Django i18n** — templates and Python code (gettext `.po`/`.mo` files)
2. **JavaScript inline** — hardcoded ternary chains per language
3. **Database content** — column-per-language (`text_en` / `text_fr` / `text_es`)

---

## 1. Django i18n (Templates + Python)

### How it works

User-facing strings are wrapped in translation tags/functions. Django extracts them into `.po` files, you translate the `.po` files, then compile them to `.mo` files.

### Adding a new translatable string

**In templates:**

```django
{% load i18n %}

<p>{% trans "Hello!" %}</p>
<p>{% blocktranslate count counter=items|length %}
  You have {{ counter }} item.
{% endblocktranslate %}</p>
```

**In Python (model fields, choices, form labels):**

```python
from django.utils.translation import gettext_lazy as _

class MyModel(models.Model):
    status = models.CharField(max_length=20, choices=[
        ('draft', _('Draft')),
        ('published', _('Published')),
    ], verbose_name=_('Status'))
```

**In Python (views, runtime messages):**

```python
from django.utils.translation import gettext as _
from django.contrib import messages

messages.success(request, _('Your changes were saved!'))
```

Use `gettext_lazy` (`_`) for model/form definitions (evaluated at import time).
Use `gettext` for runtime strings in views (evaluated at call time).

### Updating translation files

After adding or changing translatable strings, regenerate the `.po` files:

```bash
python manage.py makemessages -l fr
python manage.py makemessages -l es
python manage.py makemessages -l en
```

Then translate the new/changed `msgstr` entries in each `.po` file and compile:

```bash
python manage.py compilemessages
```

### What NOT to wrap in `_()`

- Template variable expressions: `{{ user.username }}`
- CSS class names, IDs, HTML attributes that aren't user-facing
- Technical strings (URLs, field names used in code)
- Model field `name` (only `verbose_name` and `help_text` need translation)

### Common pitfalls

- **Forgetting `{% load i18n %}`** — the `{% trans %}` tag won't work without it
- **Using `gettext` instead of `gettext_lazy`** in models/forms — causes `ImproperlyConfigured` errors at import time
- **Fuzzy entries** — `#, fuzzy` in `.po` files means the entry was auto-matched but may be wrong. Review and either fix or remove the fuzzy flag. Fuzzy entries are **not compiled** into `.mo` files.
- **Stale `.po` files** — run `makemessages` whenever you add/change `{% trans %}` or `_()` strings

---

## 2. JavaScript Translations

### Current approach

JavaScript files use inline ternary chains based on `document.documentElement.lang`:

```javascript
const lang = document.documentElement.lang;
btn.textContent = lang === 'fr' ? 'Tourner!' : lang === 'es' ? '¡Girar!' : 'Spin!';
```

There is **no Django `jsi18n` catalog** in this project.

### Adding a new JS string

Follow the existing ternary pattern:

```javascript
const lang = document.documentElement.lang;
const myString = lang === 'fr' ? 'Texte francais' : lang === 'es' ? 'Texto en espanol' : 'English text';
```

### Limitations

- Adding a new language requires editing **every ternary chain** in every JS file
- No central dictionary (except `funny_face.js`'s `getMsg()` helper)
- Duplicated translations across files (e.g., "Connection error" appears 14 times)

### Recommendation

For new strings, prefer adding to a shared dictionary in `shared.js`:

```javascript
const translations = {
  connection_error: { fr: 'Erreur de connexion', es: 'Error de conexion', en: 'Connection error' },
  saving: { fr: 'Enregistrement...', es: 'Guardando...', en: 'Saving...' },
};

function getMsg(key) {
  const lang = document.documentElement.lang;
  return translations[key]?.[lang] || translations[key]?.en || key;
}
```

This makes adding a new language a single-file change.

---

## 3. Database Content Translation

### How it works

Game content (prompts, challenges, questions, story elements) is stored with separate columns per language:

```python
class Prompt(models.Model):
    text_en = models.TextField()
    text_fr = models.TextField(blank=True)
    text_es = models.TextField(blank=True)
```

Each model has a `get_text(lang)` method that returns the appropriate column with fallback to English:

```python
def get_text(self, lang):
    return getattr(self, f'text_{lang}', None) or self.text_en
```

### Adding content

When creating or editing game content via the admin, always fill in all three language columns. Leave blank only if the content is language-independent (e.g., a numeric value).

### Fallback behavior

If `text_fr` or `text_es` is empty/null, `get_text()` falls back to `text_en`. This means missing translations won't crash the app — they'll just show English instead.

---

## 4. Language Switching

The app uses URL-based language prefixes (`/en/...`, `/fr/...`, `/es/...`).

Language is activated manually in every view via:

```python
from django.utils.translation import activate

activate(lang)  # lang extracted from URL prefix
```

The language switcher in `base.html` redirects to the same page with a different prefix.

---

## 5. File Reference

| File | Purpose |
|------|---------|
| `locale/fr/LC_MESSAGES/django.po` | French translations (template + Python strings) |
| `locale/es/LC_MESSAGES/django.po` | Spanish translations |
| `locale/en/LC_MESSAGES/django.po` | English translations (mostly empty — source language) |
| `locale/*/LC_MESSAGES/django.mo` | Compiled binary translations (generated by `compilemessages`) |
| `static/shared.js` | Shared JS translations (suggestion overlay) |
| `static/pwa.js` | PWA install prompt translations (currently English-only) |
| `static/active_games/*.js` | Game-specific JS translations |
| `static/sound_games/*.js` | Game-specific JS translations |
| `static/creative_games/*.js` | Game-specific JS translations |

---

## 6. Checklist for New User-Facing Strings

When adding any new user-facing text:

- [ ] Template string wrapped in `{% trans "..." %}` or `{% blocktranslate %}`
- [ ] Python string wrapped in `gettext_lazy` (`_`) for models/forms, `gettext` for views
- [ ] Model `verbose_name` and `help_text` wrapped in `_()`
- [ ] JavaScript string added to ternary chain (or `shared.js` dictionary) with all 3 languages
- [ ] Database content has all 3 `text_*` columns filled
- [ ] Run `makemessages` + `compilemessages` after template/Python changes
- [ ] Verify new strings appear in `.po` files and are translated

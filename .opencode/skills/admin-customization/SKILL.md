---
name: admin-customization
description: How the Django admin is customized in coeuretjeu (app naming, model grouping)
---

## App naming

Each app's `apps.py` can set `verbose_name` to control admin display:

```python
class GamesConfig(AppConfig):
    name = 'games'
    verbose_name = 'General'   # appears in admin sidebar
```

## Model naming

Set `verbose_name` / `verbose_name_plural` in `Meta`:

```python
class WYRQuestion(models.Model):
    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
```

## Model grouping within an app

Defined in `games/templatetags/admin_extras.py`:

```python
GAME_GROUPS = {
    'sound_games': [
        ('Giggle Generators', ['microchallenge']),
        ('Choice Chaos', ['wyrquestion']),
        ...
    ],
}
```

The `game_groups` template filter maps `app['app_label']` + `model['object_name'].lower()` to group names.
The override template `templates/admin/app_list.html` renders sub-headers for each group.

## Template overrides

- Place in `templates/admin/` (project-level templates dir registered in settings).
- Override Django's `admin/app_list.html` for grouped model listing.
- Override `admin/index.html` if needed (currently inherits default via `{% include %}`).

## Registration

Models are registered via `@admin.register(Model)` decorator in `games/admin.py`.
No custom `AdminSite` — all registrations remain with the default `admin.site`.

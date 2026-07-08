---
name: django-test
description: How to run tests and write tests for the coeuretjeu project
---

## Running tests

```bash
python manage.py test          # all 48 tests
python manage.py test games    # games app only
```

## Test patterns

- Uses `django.test.TestCase` and `Client`.
- Each app has its own `tests.py` (e.g. `games/tests.py`, `sound_games/tests.py`).
- DB is reset between tests.
- Use `setUp()` to create Genre, Prompt, etc. fixtures.
- Test views by instantiating `Client` and calling `client.get()` / `client.post()`.
- Check `response.status_code`, `response.context`, and `response.content`.
- For AJAX views, set `HTTP_X_REQUESTED_WITH='XMLHttpRequest'` header.

## Example

```python
class MyTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.client = Client()

    def test_view_returns_200(self):
        response = self.client.get(f'/{lang}/test/')
        self.assertEqual(response.status_code, 200)
```

import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from .models import (AnalyticsEvent, Favorite, Genre, Prompt, SoundEffect,
                     StorySeed, UserProfile)


class PromptManagerTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test Genre', slug='test-genre', icon='🎯')
        self.prompt = Prompt.objects.create(
            genre=self.genre,
            text_en='English text',
            text_fr='Texte français',
            text_es='Texto español',
        )

    def test_get_random_returns_prompt_with_display_text(self):
        prompt = Prompt.objects.get_random(self.genre, 'fr')
        self.assertIsNotNone(prompt)
        self.assertEqual(prompt.display_text, 'Texte français')

    def test_get_random_fallback_to_english(self):
        prompt = Prompt.objects.get_random(self.genre, 'de')
        self.assertIsNotNone(prompt)
        self.assertEqual(prompt.display_text, 'English text')

    def test_get_random_empty_genre_returns_none(self):
        other = Genre.objects.create(name='Empty', slug='empty', icon='❌')
        prompt = Prompt.objects.get_random(other, 'en')
        self.assertIsNone(prompt)


class StorySeedTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.seed = StorySeed.objects.create(
            genre=self.genre,
            text_en='Story seed EN',
            text_fr='Story seed FR',
            text_es='Story seed ES',
        )

    def test_get_text(self):
        self.assertEqual(self.seed.get_text('fr'), 'Story seed FR')

    def test_get_random(self):
        seed = StorySeed.objects.get_random(self.genre, 'es')
        self.assertIsNotNone(seed)
        self.assertEqual(seed.display_text, 'Story seed ES')


class SoundEffectTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.effect = SoundEffect.objects.create(
            name='Test sound',
            audio_file='sounds/test.mp3',
        )
        self.effect.genres.add(self.genre)

    def test_string(self):
        self.assertEqual(str(self.effect), 'Test sound')

    def test_genre_tagged(self):
        self.assertIn(self.genre, self.effect.genres.all())


class UserProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')

    def test_profile_auto_created_on_signup(self):
        profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.assertTrue(created)
        self.assertEqual(profile.settings, {})


class FavoriteTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.prompt = Prompt.objects.create(
            genre=self.genre,
            text_en='EN', text_fr='FR', text_es='ES',
        )

    def test_favorite_unique_together(self):
        Favorite.objects.create(user=self.user, prompt=self.prompt)
        with self.assertRaises(Exception):
            Favorite.objects.create(user=self.user, prompt=self.prompt)


class AnalyticsEventTest(TestCase):
    def test_create_event(self):
        event = AnalyticsEvent.objects.create(
            event_type='page_view',
            session_key='abc123',
            language='en',
        )
        self.assertEqual(event.event_type, 'page_view')
        self.assertEqual(event.language, 'en')


class ContributePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Test Genre', slug='test-genre', icon='🎯')

    def test_contribute_page_returns_200(self):
        response = self.client.get('/en/contribute/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Contribute')
        self.assertContains(response, 'Suggest a Prompt')
        self.assertContains(response, 'Contact the Developer')

    def test_contribute_page_pre_selects_game(self):
        response = self.client.get('/en/contribute/', {'game': 'test-genre'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'selected')

    def test_suggestion_form_creates_gamesuggestion(self):
        from .models import GameSuggestion
        response = self.client.post('/en/contribute/', {
            'suggestion_submit': '1',
            'genre_id': self.genre.id,
            'suggestion_text': 'My awesome prompt idea',
            'email': 'user@example.com',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(GameSuggestion.objects.count(), 1)
        suggestion = GameSuggestion.objects.first()
        self.assertEqual(suggestion.suggestion_text, 'My awesome prompt idea')
        self.assertEqual(suggestion.email, 'user@example.com')
        self.assertEqual(suggestion.genre, self.genre)
        self.assertEqual(suggestion.status, 'pending')

    def test_suggestion_form_redirects_post(self):
        from .models import GameSuggestion
        response = self.client.post('/en/contribute/', {
            'suggestion_submit': '1',
            'genre_id': self.genre.id,
            'suggestion_text': 'Some idea',
            'email': '',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/en/contribute/', response.url)
        self.assertEqual(GameSuggestion.objects.count(), 1)

    def test_contact_form_creates_contactmessage(self):
        from .models import ContactMessage
        response = self.client.post('/en/contribute/', {
            'contact_submit': '1',
            'email': 'user@example.com',
            'message': 'Hello, I love this site!',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 1)
        msg = ContactMessage.objects.first()
        self.assertEqual(msg.message, 'Hello, I love this site!')
        self.assertEqual(msg.email, 'user@example.com')
        self.assertFalse(msg.dealt_with)

    def test_contact_form_redirects_post(self):
        from .models import ContactMessage
        response = self.client.post('/en/contribute/', {
            'contact_submit': '1',
            'email': 'test@example.com',
            'message': 'Hi there',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('/en/contribute/', response.url)
        self.assertEqual(ContactMessage.objects.count(), 1)


class ViewStatusTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test Genre', slug='test-genre', icon='🎯')
        Prompt.objects.create(
            genre=self.genre,
            text_en='English text',
            text_fr='Texte français',
            text_es='Texto español',
        )
        self.client = Client()

    def test_hub_returns_200(self):
        response = self.client.get('/en/')
        self.assertEqual(response.status_code, 200)

    def test_detail_returns_200(self):
        response = self.client.get('/en/test-genre/')
        self.assertEqual(response.status_code, 200)

    def test_detail_returns_404_for_unknown_genre(self):
        response = self.client.get('/en/unknown/')
        self.assertEqual(response.status_code, 404)

    def test_next_prompt_returns_partial(self):
        response = self.client.get('/en/next-prompt/', {'genre_slug': 'test-genre'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'English text')

    def test_root_redirects_to_en(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/en/')

    def test_french_hub(self):
        response = self.client.get('/fr/')
        self.assertEqual(response.status_code, 200)

    def test_signup_page_returns_200(self):
        response = self.client.get('/en/signup/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_returns_200(self):
        response = self.client.get('/en/login/')
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get('/en/profile/')
        self.assertIn(response.status_code, [302, 404])

    def test_track_event_endpoint(self):
        response = self.client.post(
            '/en/analytics/track/',
            json.dumps({'event_type': 'page_view'}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(AnalyticsEvent.objects.count(), 1)


class AuthFlowTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.prompt = Prompt.objects.create(
            genre=self.genre, text_en='EN', text_fr='FR', text_es='ES',
        )

    def test_signup_creates_user_and_profile(self):
        response = self.client.post('/en/signup/', {
            'username': 'newuser',
            'password1': 'ComplexPass123!',
            'password2': 'ComplexPass123!',
        })
        self.assertIn(response.status_code, [200, 302])
        self.assertTrue(User.objects.filter(username='newuser').exists())
        user = User.objects.get(username='newuser')
        self.assertTrue(UserProfile.objects.filter(user=user).exists())

    def test_login_and_favorite(self):
        User.objects.create_user(username='testuser', password='pass123')
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(f'/en/toggle-favorite/{self.prompt.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(user__username='testuser', prompt=self.prompt).exists())
        response = self.client.post(f'/en/toggle-favorite/{self.prompt.id}/')
        self.assertFalse(Favorite.objects.filter(user__username='testuser', prompt=self.prompt).exists())

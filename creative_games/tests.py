import json

from django.contrib.auth.models import User
from django.test import Client, TestCase

from games.models import Genre
from creative_games.models import (DoodleAccessory, DoodleDrawing,
                                   DoodleEmotion, DoodleSubject, FacePrompt,
                                   StorySession, StoryTwist)


class StoryTwistTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.t = StoryTwist.objects.create(
            genre=self.genre, text_en='EN', text_fr='FR', text_es='ES',
        )

    def test_get_text(self):
        self.assertEqual(self.t.get_text('fr'), 'FR')

    def test_get_random(self):
        t = StoryTwist.get_random('en')
        self.assertEqual(t.display_text, 'EN')


class FacePromptTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        FacePrompt.objects.create(genre=self.genre, text_en='EN', text_fr='FR', text_es='ES', age_group='all', category='silly')

    def test_get_random(self):
        p = FacePrompt.get_random('en')
        self.assertEqual(p.display_text, 'EN')

    def test_get_random_age_filter(self):
        p = FacePrompt.get_random('en', age_group='3-6')
        self.assertIsNotNone(p)
        self.assertEqual(p.display_text, 'EN')

    def test_get_random_category_filter(self):
        p = FacePrompt.get_random('en', category='silly')
        self.assertIsNotNone(p)
        self.assertEqual(p.display_text, 'EN')


class DoodleModelTest(TestCase):
    def setUp(self):
        DoodleSubject.objects.create(text_en='Cat', text_fr='Chat', text_es='Gato')
        DoodleEmotion.objects.create(text_en='Happy', text_fr='Heureux', text_es='Feliz')
        DoodleAccessory.objects.create(text_en='Hat', text_fr='Chapeau', text_es='Sombrero')

    def test_subject_get_text(self):
        s = DoodleSubject.objects.first()
        self.assertEqual(s.get_text('fr'), 'Chat')


class CreativeGameViewTest(TestCase):
    def setUp(self):
        Genre.objects.create(name='TT', slug='tale-twisters', game_module='tale_twisters')
        Genre.objects.create(name='FFF', slug='funny-face-factory', game_module='funny_face_factory')
        Genre.objects.create(name='DD', slug='doodle-dash', game_module='doodle_dash')
        g = Genre.objects.get(slug='tale-twisters')
        StoryTwist.objects.create(genre=g, text_en='twist', text_fr='twist', text_es='twist')
        FacePrompt.objects.create(genre=Genre.objects.get(slug='funny-face-factory'),
                                   text_en='face', text_fr='face', text_es='face',
                                   age_group='all', category='silly')
        DoodleSubject.objects.create(text_en='subj', text_fr='subj', text_es='subj')
        DoodleEmotion.objects.create(text_en='emo', text_fr='emo', text_es='emo')
        DoodleAccessory.objects.create(text_en='acc', text_fr='acc', text_es='acc')
        self.client = Client()

    def test_tale_play(self):
        r = self.client.get('/en/tale-twisters/')
        self.assertEqual(r.status_code, 200)

    def test_funny_face_play(self):
        r = self.client.get('/en/funny-face-factory/')
        self.assertEqual(r.status_code, 200)

    def test_doodle_play(self):
        r = self.client.get('/en/doodle-dash/')
        self.assertEqual(r.status_code, 200)

    def test_tale_save_anonymous_returns_login_required(self):
        r = self.client.post('/en/tale-twisters/save/',
                             json.dumps({'content': 'story', 'title': 'Test'}),
                             content_type='application/json')
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data['status'], 'login_required')
        self.assertIn('/en/login/', data['login_url'])
        self.assertIn('/en/tale-twisters/claim-story/', data['login_url'])

    def test_tale_save_authenticated(self):
        User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')
        r = self.client.post('/en/tale-twisters/save/',
                             json.dumps({'content': 'story', 'title': 'Test'}),
                             content_type='application/json')
        self.assertEqual(r.status_code, 200)
        data = json.loads(r.content)
        self.assertEqual(data['status'], 'ok')
        self.assertTrue(StorySession.objects.filter(user__username='testuser', title='Test').exists())

    def test_tale_claim_story(self):
        User.objects.create_user(username='testuser', password='pass')
        session = self.client.session
        session['pending_story'] = {
            'title': 'My Saved Story',
            'content': 'Once upon a time...',
            'duration_seconds': 0,
            'language': 'en',
        }
        session.save()
        self.client.login(username='testuser', password='pass')
        r = self.client.get('/en/tale-twisters/claim-story/')
        self.assertRedirects(r, '/en/tale-twisters/chest/')
        self.assertTrue(StorySession.objects.filter(user__username='testuser', title='My Saved Story').exists())
        # pending_story should be cleared
        session = self.client.session
        self.assertNotIn('pending_story', session)

    def test_tale_claim_story_no_pending(self):
        User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')
        r = self.client.get('/en/tale-twisters/claim-story/')
        self.assertRedirects(r, '/en/tale-twisters/chest/')
        self.assertEqual(StorySession.objects.count(), 0)

    def test_tale_chest_redirects_anonymous(self):
        r = self.client.get('/en/tale-twisters/chest/')
        self.assertRedirects(r, '/en/login/?next=/en/tale-twisters/chest/')

    def test_tale_chest_authenticated(self):
        User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')
        r = self.client.get('/en/tale-twisters/chest/')
        self.assertEqual(r.status_code, 200)

    def test_tale_save_strips_html_from_title(self):
        User.objects.create_user(username='testuser', password='pass')
        self.client.login(username='testuser', password='pass')
        r = self.client.post('/en/tale-twisters/save/',
                             json.dumps({'content': 'story', 'title': '<script>alert("xss")</script>My Story'}),
                             content_type='application/json')
        self.assertEqual(r.status_code, 200)
        session = StorySession.objects.get(user__username='testuser')
        self.assertNotIn('<script>', session.title)
        self.assertIn('My Story', session.title)

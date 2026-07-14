from django.test import Client, TestCase

from games.models import Genre
from sound_games.models import LipSyncSound, MicroChallenge, SoundFX, WYRQuestion


class MicroChallengeTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.c = MicroChallenge.objects.create(
            genre=self.genre, text_en='EN', text_fr='FR', text_es='ES',
            age_group='3-6', energy_level='calm',
        )

    def test_get_text(self):
        self.assertEqual(self.c.get_text('fr'), 'FR')
        self.assertEqual(self.c.get_text('de'), 'EN')

    def test_get_random(self):
        c = MicroChallenge.get_random('en')
        self.assertEqual(c.display_text, 'EN')

    def test_get_random_age_filter(self):
        MicroChallenge.objects.create(
            genre=self.genre, text_en='Wild', text_fr='', text_es='',
            age_group='7-10', energy_level='wild',
        )
        c = MicroChallenge.get_random('en', age_group='3-6')
        self.assertEqual(c.age_group, '3-6')


class WYRQuestionTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        self.q = WYRQuestion.objects.create(
            genre=self.genre, category='silly', age_group='3-6',
            option_a_en='A_en', option_a_fr='A_fr', option_a_es='A_es',
            option_b_en='B_en', option_b_fr='B_fr', option_b_es='B_es',
        )

    def test_get_option(self):
        self.assertEqual(self.q.get_option_a('fr'), 'A_fr')
        self.assertEqual(self.q.get_option_b('de'), 'B_en')

    def test_get_random(self):
        q = WYRQuestion.get_random('en')
        self.assertIsNotNone(q)
        self.assertEqual(q.display_a, 'A_en')

    def test_get_random_age_filter(self):
        WYRQuestion.objects.create(
            genre=self.genre, category='deep', age_group='7-10',
            option_a_en='Older', option_a_fr='', option_a_es='',
            option_b_en='Also', option_b_fr='', option_b_es='',
        )
        q = WYRQuestion.get_random('en', age_group='3-6')
        self.assertEqual(q.age_group, '3-6')

    def test_get_random_category_and_age_filter(self):
        WYRQuestion.objects.create(
            genre=self.genre, category='food', age_group='3-6',
            option_a_en='Food', option_a_fr='', option_a_es='',
            option_b_en='Yum', option_b_fr='', option_b_es='',
        )
        q = WYRQuestion.get_random('en', category='food', age_group='3-6')
        self.assertEqual(q.category, 'food')
        self.assertEqual(q.age_group, '3-6')

    def test_default_age_group_is_all(self):
        q = WYRQuestion.objects.create(
            genre=self.genre, category='silly',
            option_a_en='X', option_a_fr='', option_a_es='',
            option_b_en='Y', option_b_fr='', option_b_es='',
        )
        self.assertEqual(q.age_group, 'all')


class SoundFXTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        SoundFX.objects.create(genre=self.genre, name='Laugh', category='funny')

    def test_get_random(self):
        s = SoundFX.get_random()
        self.assertIsNotNone(s)
        self.assertEqual(s.name, 'Laugh')


class LipSyncSoundTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        LipSyncSound.objects.create(genre=self.genre, name='Robot', description_en='Beep')

    def test_get_description(self):
        self.assertEqual(LipSyncSound.get_random().name, 'Robot')


class SoundGameViewTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='GG', slug='giggle-generators', game_module='giggle_generators')
        Genre.objects.create(name='CC', slug='choice-chaos', game_module='choice_chaos')
        Genre.objects.create(name='MM', slug='mimic-mayhem', game_module='mimic_mayhem')
        Genre.objects.create(name='LL', slug='lip-sync-legends', game_module='lip_sync_legends')
        MicroChallenge.objects.create(genre=self.genre, text_en='test', text_fr='test', text_es='test',
                                        age_group='3-6', energy_level='calm')
        WYRQuestion.objects.create(genre=Genre.objects.get(slug='choice-chaos'), category='silly', age_group='all',
                                    option_a_en='a', option_a_fr='a', option_a_es='a',
                                    option_b_en='b', option_b_fr='b', option_b_es='b')
        SoundFX.objects.create(genre=Genre.objects.get(slug='mimic-mayhem'), name='Test')
        LipSyncSound.objects.create(genre=Genre.objects.get(slug='lip-sync-legends'), name='Test')
        self.client = Client()

    def test_giggle_play(self):
        r = self.client.get('/en/giggle-generators/')
        self.assertEqual(r.status_code, 200)

    def test_choice_play(self):
        r = self.client.get('/en/choice-chaos/')
        self.assertEqual(r.status_code, 200)

    def test_mimic_play(self):
        r = self.client.get('/en/mimic-mayhem/')
        self.assertEqual(r.status_code, 200)

    def test_lip_sync_play(self):
        r = self.client.get('/en/lip-sync-legends/')
        self.assertEqual(r.status_code, 200)

    def test_choice_vote_post(self):
        r = self.client.post('/en/choice-chaos/vote/',
                             {'question_id': '1', 'vote': 'a'},
                             content_type='application/json')
        self.assertEqual(r.status_code, 200)

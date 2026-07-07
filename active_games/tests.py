from django.test import Client, TestCase

from games.models import Genre
from active_games.models import (CarGame, RoleActivity, RoleCharacter,
                                 RoleSetting, TripSession)


class RoleModelTest(TestCase):
    def setUp(self):
        RoleCharacter.objects.create(text_en='Wizard', text_fr='Sorcier', text_es='Mago')
        RoleSetting.objects.create(text_en='Castle', text_fr='Château', text_es='Castillo')
        RoleActivity.objects.create(text_en='Dance', text_fr='Danser', text_es='Bailar')

    def test_get_text(self):
        c = RoleCharacter.objects.first()
        self.assertEqual(c.get_text('fr'), 'Sorcier')
        s = RoleSetting.objects.first()
        self.assertEqual(s.get_text('es'), 'Castillo')
        a = RoleActivity.objects.first()
        self.assertEqual(a.get_text('en'), 'Dance')


class CarGameTest(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name='Test', slug='test', icon='🎯')
        CarGame.objects.create(
            genre=self.genre, name_en='I Spy',
            instructions_en='Look out the window',
        )

    def test_str(self):
        g = CarGame.objects.first()
        self.assertEqual(str(g), 'I Spy')


class ActiveGameViewTest(TestCase):
    def setUp(self):
        Genre.objects.create(name='WR', slug='wild-roles', game_module='wild_roles')
        Genre.objects.create(name='HH', slug='highway-hijinks', game_module='highway_hijinks')
        RoleCharacter.objects.create(text_en='char', text_fr='char', text_es='char')
        RoleSetting.objects.create(text_en='set', text_fr='set', text_es='set')
        RoleActivity.objects.create(text_en='act', text_fr='act', text_es='act')
        CarGame.objects.create(genre=Genre.objects.get(slug='highway-hijinks'),
                                name_en='Game', instructions_en='Play')
        self.client = Client()

    def test_wild_play(self):
        r = self.client.get('/en/wild-roles/')
        self.assertEqual(r.status_code, 200)

    def test_highway_play(self):
        r = self.client.get('/en/highway-hijinks/')
        self.assertEqual(r.status_code, 200)

    def test_wild_spin(self):
        r = self.client.get('/en/wild-roles/spin/')
        self.assertEqual(r.status_code, 200)

    def test_highway_boredom_buster(self):
        r = self.client.get('/en/highway-hijinks/boredom-buster/')
        self.assertEqual(r.status_code, 200)

    def test_highway_start_trip(self):
        r = self.client.post('/en/highway-hijinks/start-trip/',
                             {'distance': '100'},
                             content_type='application/json')
        self.assertEqual(r.status_code, 200)

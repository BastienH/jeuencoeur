from django.db import models

import random

from sound_games.models import MicroChallenge, WYRQuestion, SoundFX, LipSyncSound


def seed_micro_challenges(genre, stdout):
    challenges = [
        {'age_group': '3-6', 'energy_level': 'calm', 'text_en': 'Make a quiet mouse sound', 'text_fr': 'Fais un bruit de souris tout doux', 'text_es': 'Haz un sonido de ratón muy suave'},
        {'age_group': '3-6', 'energy_level': 'wild', 'text_en': 'Roar like a tiny dinosaur!', 'text_fr': 'Rugis comme un tout petit dinosaure!', 'text_es': 'Ruge como un dinosaurio pequeño!'},
        {'age_group': '3-6', 'energy_level': 'calm', 'text_en': 'Whisper a secret to the wind', 'text_fr': 'Chuchote un secret au vent', 'text_es': 'Susurra un secreto al viento'},
        {'age_group': '3-6', 'energy_level': 'wild', 'text_en': 'Make the loudest animal sound you can', 'text_fr': 'Fais le bruit d\'animal le plus fort possible', 'text_es': 'Haz el sonido de animal más fuerte que puedas'},
        {'age_group': '7-10', 'energy_level': 'calm', 'text_en': 'Hum a tune and have others guess it', 'text_fr': 'Chante une mélodie en fredonnant et laisse les autres deviner', 'text_es': 'Tararea una melodía y deja que los demás adivinen'},
        {'age_group': '7-10', 'energy_level': 'wild', 'text_en': 'Imitate a machine sound for 10 seconds', 'text_fr': 'Imite le bruit d\'une machine pendant 10 secondes', 'text_es': 'Imita el sonido de una máquina durante 10 segundos'},
    ]
    count = 0
    for c in challenges:
        MicroChallenge.objects.get_or_create(
            genre=genre, text_en=c['text_en'],
            defaults={'age_group': c['age_group'], 'energy_level': c['energy_level'],
                      'text_fr': c['text_fr'], 'text_es': c['text_es']}
        )
        count += 1
    stdout.write(f'  Seeded {count} micro challenges')


def seed_wyr_questions(genre, stdout):
    questions = [
        {'category': 'silly', 'option_a_en': 'Eat only sweet food forever', 'option_a_fr': 'Manger seulement sucré pour toujours', 'option_a_es': 'Comer solo dulce para siempre',
         'option_b_en': 'Eat only savory food forever', 'option_b_fr': 'Manger seulement salé pour toujours', 'option_b_es': 'Comer solo salado para siempre'},
        {'category': 'silly', 'option_a_en': 'Have a pet elephant', 'option_a_fr': 'Avoir un éléphant comme animal de compagnie', 'option_a_es': 'Tener un elefante como mascota',
         'option_b_en': 'Have a pet penguin', 'option_b_fr': 'Avoir un pingouin comme animal de compagnie', 'option_b_es': 'Tener un pingüino como mascota'},
        {'category': 'deep', 'option_a_en': 'Be able to fly', 'option_a_fr': 'Pouvoir voler', 'option_a_es': 'Poder volar',
         'option_b_en': 'Be invisible', 'option_b_fr': 'Être invisible', 'option_b_es': 'Ser invisible'},
        {'category': 'deep', 'option_a_en': 'Live in a treehouse', 'option_a_fr': 'Vivre dans une cabane dans un arbre', 'option_a_es': 'Vivir en una casa en un árbol',
         'option_b_en': 'Live in a castle', 'option_b_fr': 'Vivre dans un château', 'option_b_es': 'Vivir en un castillo'},
        {'category': 'food', 'option_a_en': 'Pizza for breakfast every day', 'option_a_fr': 'Pizza au petit-déjeuner tous les jours', 'option_a_es': 'Pizza en el desayuno todos los días',
         'option_b_en': 'Ice cream for dinner every day', 'option_b_fr': 'Glace au dîner tous les jours', 'option_b_es': 'Helado en la cena todos los días'},
        {'category': 'food', 'option_a_en': 'Never eat vegetables again', 'option_a_fr': 'Ne plus jamais manger de légumes', 'option_a_es': 'No volver a comer verduras',
         'option_b_en': 'Only eat vegetables forever', 'option_b_fr': 'Manger seulement des légumes pour toujours', 'option_b_es': 'Comer solo verduras para siempre'},
    ]
    count = 0
    for q in questions:
        WYRQuestion.objects.get_or_create(
            genre=genre, option_a_en=q['option_a_en'],
            defaults={'category': q['category'],
                      'option_a_fr': q['option_a_fr'], 'option_a_es': q['option_a_es'],
                      'option_b_en': q['option_b_en'], 'option_b_fr': q['option_b_fr'], 'option_b_es': q['option_b_es']}
        )
        count += 1
    stdout.write(f'  Seeded {count} WYR questions')


def seed_sound_fx(genre, stdout):
    sounds = [
        {'name': 'Laugh', 'category': 'funny'},
        {'name': 'Boo', 'category': 'funny'},
        {'name': 'Applause', 'category': 'funny'},
        {'name': 'Drum Roll', 'category': 'dramatic'},
        {'name': 'Crickets', 'category': 'dramatic'},
    ]
    count = 0
    for s in sounds:
        SoundFX.objects.get_or_create(genre=genre, name=s['name'], defaults={'category': s['category']})
        count += 1
    stdout.write(f'  Seeded {count} sound FX (placeholders — no audio files)')


def seed_lip_sync_sounds(genre, stdout):
    sounds = [
        {'name': 'Happy Birthday', 'description_en': 'Sing it like a rock star'},
        {'name': 'Thunderstorm', 'description_en': 'Sound like rain and thunder'},
        {'name': 'Robot Voice', 'description_en': 'Talk like a robot'},
    ]
    count = 0
    for s in sounds:
        LipSyncSound.objects.get_or_create(
            genre=genre, name=s['name'],
            defaults={'description_en': s['description_en'], 'description_fr': '', 'description_es': ''}
        )
        count += 1
    stdout.write(f'  Seeded {count} lip-sync sounds (placeholders — no audio files)')

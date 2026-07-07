from creative_games.models import StoryEnding, StoryTwist, FacePrompt, DoodleSubject, DoodleEmotion, DoodleAccessory


def seed_story_twists(genre, stdout):
    twists = [
        {'text_en': '...but then a dragon appeared!', 'text_fr': '...mais alors un dragon est apparu!', 'text_es': '...¡pero entonces apareció un dragón!'},
        {'text_en': '...and suddenly everything turned upside down!', 'text_fr': '...et soudain tout s\'est retourné!', 'text_es': '...¡y de repente todo se puso al revés!'},
        {'text_en': '...when a mysterious letter arrived...', 'text_fr': '...quand une lettre mystérieuse est arrivée...', 'text_es': '...cuando llegó una carta misteriosa...'},
        {'text_en': '...but the surprise was waiting inside...', 'text_fr': '...mais la surprise attendait à l\'intérieur...', 'text_es': '...pero la sorpresa esperaba dentro...'},
        {'text_en': '...and that is when the magic began!', 'text_fr': '...et c\'est là que la magie a commencé!', 'text_es': '...¡y entonces comenzó la magia!'},
        {'text_en': '...but the ground started shaking!', 'text_fr': '...mais le sol s\'est mis à trembler!', 'text_es': '...¡pero el suelo empezó a temblar!'},
        {'text_en': '...when they found a hidden door...', 'text_fr': '...quand ils ont trouvé une porte cachée...', 'text_es': '...cuando encontraron una puerta escondida...'},
        {'text_en': '...and the animals started talking!', 'text_fr': '...et les animaux se sont mis à parler!', 'text_es': '...¡y los animales empezaron a hablar!'},
        {'text_en': '...but someone had eaten all the cookies...', 'text_fr': '...mais quelqu\'un avait mangé tous les biscuits...', 'text_es': '...pero alguien se había comido todas las galletas...'},
        {'text_en': '...when a rainbow appeared out of nowhere!', 'text_fr': '...quand un arc-en-ciel est apparu de nulle part!', 'text_es': '...¡cuando apareció un arcoíris de la nada!'},
        {'text_en': '...but the character shrank to the size of a mouse!', 'text_fr': '...mais le personnage a rétréci à la taille d\'une souris!', 'text_es': '...¡pero el personaje se encogió al tamaño de un ratón!'},
        {'text_en': '...and the weather changed instantly!', 'text_fr': '...et le temps a changé instantanément!', 'text_es': '...¡y el clima cambió instantáneamente!'},
        {'text_en': '...when a friendly alien landed nearby...', 'text_fr': '...quand un extraterrestre amical a atterri près d\'ici...', 'text_es': '...cuando un extraterrestre amigable aterrizó cerca...'},
        {'text_en': '...but the treasure was not what it seemed!', 'text_fr': '...mais le trésor n\'était pas ce qu\'il semblait être!', 'text_es': '...¡pero el tesoro no era lo que parecía!'},
        {'text_en': '...and they discovered they could fly!', 'text_fr': '...et ils ont découvert qu\'ils pouvaient voler!', 'text_es': '...¡y descubrieron que podían volar!'},
    ]
    count = 0
    for t in twists:
        _, created = StoryTwist.objects.get_or_create(genre=genre, text_en=t['text_en'],
                                          defaults={'text_fr': t['text_fr'], 'text_es': t['text_es']})
        if created:
            count += 1
    stdout.write(f'  Seeded {count} story twists (new)')


def seed_story_endings(genre, stdout):
    endings = [
        {'text_en': 'And they all lived happily ever after.', 'text_fr': 'Et ils vécurent tous heureux pour toujours.', 'text_es': 'Y todos vivieron felices para siempre.'},
        {'text_en': 'It was the best adventure they ever had.', 'text_fr': 'C\'était la meilleure aventure qu\'ils aient jamais eue.', 'text_es': 'Fue la mejor aventura que jamás tuvieron.'},
        {'text_en': 'From that day on, nothing was the same.', 'text_fr': 'À partir de ce jour, plus rien ne fut pareil.', 'text_es': 'Desde ese día, nada fue igual.'},
        {'text_en': 'And they promised to always explore together.', 'text_fr': 'Et ils promirent de toujours explorer ensemble.', 'text_es': 'Y prometieron explorar siempre juntos.'},
        {'text_en': 'The journey taught them more than any treasure could.', 'text_fr': 'Le voyage leur a appris plus qu\'aucun trésor ne pourrait.', 'text_es': 'El viaje les enseñó más de lo que cualquier tesoro podría.'},
        {'text_en': 'And so the story became a legend in their town.', 'text_fr': 'Et ainsi l\'histoire devint une légende dans leur ville.', 'text_es': 'Y así la historia se convirtió en una leyenda en su pueblo.'},
        {'text_en': 'They made a new friend that day.', 'text_fr': 'Ils se sont fait un nouvel ami ce jour-là.', 'text_es': 'Hicieron un nuevo amigo ese día.'},
        {'text_en': 'The mystery was solved, but new questions remained.', 'text_fr': 'Le mystère était résolu, mais de nouvelles questions demeuraient.', 'text_es': 'El misterio se resolvió, pero quedaron nuevas preguntas.'},
        {'text_en': 'And they knew this was only the beginning.', 'text_fr': 'Et ils savaient que ce n\'était que le début.', 'text_es': 'Y sabían que esto era solo el comienzo.'},
        {'text_en': 'The whole family laughed about it for years.', 'text_fr': 'Toute la famille en a ri pendant des années.', 'text_es': 'Toda la familia se rió de eso durante años.'},
        {'text_en': 'And they finally made it home just in time for dinner.', 'text_fr': 'Et ils sont finalement rentrés juste à l\'heure pour le dîner.', 'text_es': 'Y finalmente llegaron a casa justo a tiempo para la cena.'},
        {'text_en': 'The secret was safer with them than anywhere else.', 'text_fr': 'Le secret était plus en sécurité avec eux que partout ailleurs.', 'text_es': 'El secreto estaba más seguro con ellos que en cualquier otro lugar.'},
        {'text_en': 'They decided to write a book about their adventure.', 'text_fr': 'Ils décidèrent d\'écrire un livre sur leur aventure.', 'text_es': 'Decidieron escribir un libro sobre su aventura.'},
        {'text_en': 'And the magic stayed with them forever after.', 'text_fr': 'Et la magie est restée avec eux pour toujours.', 'text_es': 'Y la magia se quedó con ellos para siempre.'},
        {'text_en': 'It turned out to be the best day ever.', 'text_fr': 'Cela s\'est avéré être le meilleur jour de tous.', 'text_es': 'Resultó ser el mejor día de todos.'},
    ]
    count = 0
    for e in endings:
        _, created = StoryEnding.objects.get_or_create(genre=genre, text_en=e['text_en'],
                                          defaults={'text_fr': e['text_fr'], 'text_es': e['text_es']})
        if created:
            count += 1
    stdout.write(f'  Seeded {count} story endings (new)')


def seed_face_prompts(genre, stdout):
    prompts = [
        {'text_en': 'Make your silliest face!', 'text_fr': 'Fais la grimace la plus idiote!', 'text_es': '¡Haz la cara más tonta!'},
        {'text_en': 'Pretend you just ate something sour', 'text_fr': 'Fais comme si tu venais de manger quelque chose d\'acide', 'text_es': 'Imagina que acabas de comer algo agrio'},
        {'text_en': 'Show your happiest smile', 'text_fr': 'Montre ton plus beau sourire', 'text_es': 'Muestra tu sonrisa más feliz'},
        {'text_en': 'Look surprised!', 'text_fr': 'Aie l\'air surpris!', 'text_es': '¡Parece sorprendido!'},
    ]
    count = 0
    for p in prompts:
        FacePrompt.objects.get_or_create(genre=genre, text_en=p['text_en'],
                                          defaults={'text_fr': p['text_fr'], 'text_es': p['text_es']})
        count += 1
    stdout.write(f'  Seeded {count} face prompts')


def seed_doodle_data(stdout):
    subjects = [
        {'text_en': 'A happy cat', 'text_fr': 'Un chat heureux', 'text_es': 'Un gato feliz'},
        {'text_en': 'A silly monster', 'text_fr': 'Un monstre idiot', 'text_es': 'Un monstruo tonto'},
        {'text_en': 'A flying car', 'text_fr': 'Une voiture volante', 'text_es': 'Un coche volador'},
        {'text_en': 'A treehouse', 'text_fr': 'Une cabane dans un arbre', 'text_es': 'Una casa en un árbol'},
        {'text_en': 'A rainbow pizza', 'text_fr': 'Une pizza arc-en-ciel', 'text_es': 'Una pizza arcoíris'},
    ]
    for s in subjects:
        DoodleSubject.objects.get_or_create(text_en=s['text_en'],
                                             defaults={'text_fr': s['text_fr'], 'text_es': s['text_es']})
    stdout.write(f'  Seeded {len(subjects)} doodle subjects')

    emotions = [
        {'text_en': 'happy', 'text_fr': 'heureux', 'text_es': 'feliz'},
        {'text_en': 'silly', 'text_fr': 'idiot', 'text_es': 'tonto'},
        {'text_en': 'brave', 'text_fr': 'courageux', 'text_es': 'valiente'},
        {'text_en': 'sleepy', 'text_fr': 'fatigué', 'text_es': 'soñoliento'},
    ]
    for e in emotions:
        DoodleEmotion.objects.get_or_create(text_en=e['text_en'],
                                             defaults={'text_fr': e['text_fr'], 'text_es': e['text_es']})
    stdout.write(f'  Seeded {len(emotions)} doodle emotions')

    accessories = [
        {'text_en': 'wearing a crown', 'text_fr': 'portant une couronne', 'text_es': 'usando una corona'},
        {'text_en': 'with sunglasses', 'text_fr': 'avec des lunettes de soleil', 'text_es': 'con gafas de sol'},
        {'text_en': 'holding a balloon', 'text_fr': 'tenant un ballon', 'text_es': 'sosteniendo un globo'},
        {'text_en': 'with butterfly wings', 'text_fr': 'avec des ailes de papillon', 'text_es': 'con alas de mariposa'},
    ]
    for a in accessories:
        DoodleAccessory.objects.get_or_create(text_en=a['text_en'],
                                               defaults={'text_fr': a['text_fr'], 'text_es': a['text_es']})
    stdout.write(f'  Seeded {len(accessories)} doodle accessories')

from active_games.models import RoleCharacter, RoleSetting, RoleActivity, CarGame


def seed_role_data(genre, stdout):
    characters = [
        {'text_en': 'A clumsy wizard', 'text_fr': 'Un sorcier maladroit', 'text_es': 'Un mago torpe'},
        {'text_en': 'A singing pirate', 'text_fr': 'Un pirate qui chante', 'text_es': 'Un pirata cantante'},
        {'text_en': 'A shy superhero', 'text_fr': 'Un super-héros timide', 'text_es': 'Un superhéroe tímido'},
        {'text_en': 'A dancing robot', 'text_fr': 'Un robot qui danse', 'text_es': 'Un robot bailarín'},
        {'text_en': 'A detective duck', 'text_fr': 'Un canard détective', 'text_es': 'Un pato detective'},
    ]
    for c in characters:
        RoleCharacter.objects.get_or_create(text_en=c['text_en'],
                                             defaults={'text_fr': c['text_fr'], 'text_es': c['text_es']})
    stdout.write(f'  Seeded {len(characters)} role characters')

    settings = [
        {'text_en': 'On a pirate ship', 'text_fr': 'Sur un bateau pirate', 'text_es': 'En un barco pirata'},
        {'text_en': 'In a haunted house', 'text_fr': 'Dans une maison hantée', 'text_es': 'En una casa encantada'},
        {'text_en': 'At the North Pole', 'text_fr': 'Au pôle Nord', 'text_es': 'En el Polo Norte'},
        {'text_en': 'Inside a video game', 'text_fr': 'Dans un jeu vidéo', 'text_es': 'Dentro de un videojuego'},
    ]
    for s in settings:
        RoleSetting.objects.get_or_create(text_en=s['text_en'],
                                           defaults={'text_fr': s['text_fr'], 'text_es': s['text_es']})
    stdout.write(f'  Seeded {len(settings)} role settings')

    activities = [
        {'text_en': 'Look for treasure', 'text_fr': 'Chercher un trésor', 'text_es': 'Buscar un tesoro'},
        {'text_en': 'Escape from something', 'text_fr': 'Échapper à quelque chose', 'text_es': 'Escapar de algo'},
        {'text_en': 'Cook a magical meal', 'text_fr': 'Cuisiner un repas magique', 'text_es': 'Cocinar una comida mágica'},
        {'text_en': 'Put on a show', 'text_fr': 'Organiser un spectacle', 'text_es': 'Organizar un espectáculo'},
    ]
    for a in activities:
        RoleActivity.objects.get_or_create(text_en=a['text_en'],
                                            defaults={'text_fr': a['text_fr'], 'text_es': a['text_es']})
    stdout.write(f'  Seeded {len(activities)} role activities')


def seed_car_games(genre, stdout):
    games = [
        {'name_en': 'I Spy', 'name_fr': 'Je vois', 'name_es': 'Veo veo',
         'instructions_en': 'Take turns spotting things outside the window. First to find something wins!',
         'instructions_fr': 'À tour de rôle, repérez des choses par la fenêtre. Le premier à trouver gagne!',
         'instructions_es': 'Por turnos, encuentren cosas fuera de la ventana. ¡El primero en encontrar gana!'},
        {'name_en': 'License Plate Bingo', 'name_fr': 'Bingo des plaques', 'name_es': 'Bingo de matrículas',
         'instructions_en': 'Try to spot license plates from different states or countries.',
         'instructions_fr': 'Essayez de repérer des plaques de différents états ou pays.',
         'instructions_es': 'Intenta encontrar matrículas de diferentes estados o países.'},
        {'name_en': 'The Quiet Game', 'name_fr': 'Le jeu du silence', 'name_es': 'El juego del silencio',
         'instructions_en': 'Whoever stays quiet the longest wins!',
         'instructions_fr': 'Celui qui reste silencieux le plus longtemps gagne!',
         'instructions_es': '¡Quien se quede callado más tiempo gana!'},
        {'name_en': '20 Questions', 'name_fr': '20 questions', 'name_es': '20 preguntas',
         'instructions_en': 'Think of an animal, object, or person. Others get 20 yes/no questions to guess it!',
         'instructions_fr': 'Pensez à un animal, un objet ou une personne. Les autres ont 20 questions oui/non pour le deviner!',
         'instructions_es': '¡Piensa en un animal, objeto o persona. Los demás tienen 20 preguntas de sí/no para adivinarlo!'},
        {'name_en': 'Story Chain', 'name_fr': 'Chaîne d\'histoires', 'name_es': 'Cadena de historias',
         'instructions_en': 'Each person adds one sentence to a story. Take turns and see where it goes!',
         'instructions_fr': 'Chaque personne ajoute une phrase à une histoire. À tour de rôle et voyez où cela mène!',
         'instructions_es': 'Cada persona añade una oración a una historia. ¡Túrnense y vean a dónde va!'},
        {'name_en': 'Animal Sounds', 'name_fr': 'Bruits d\'animaux', 'name_es': 'Sonidos de animales',
         'instructions_en': 'One person makes an animal sound, others guess the animal. Silly sounds encouraged!',
         'instructions_fr': 'Une personne imite un animal, les autres devinent. Les sons idiots sont encouragés!',
         'instructions_es': 'Una persona hace el sonido de un animal, los demás adivinan. ¡Se animan sonidos tontos!'},
        {'name_en': 'Alphabet Game', 'name_fr': 'Jeu de l\'alphabet', 'name_es': 'Juego del alfabeto',
         'instructions_en': 'Find words outside starting with each letter from A to Z. First to Z wins!',
         'instructions_fr': 'Trouvez des mots dehors commençant par chaque lettre de A à Z. Le premier à Z gagne!',
         'instructions_es': '¡Encuentra palabras afuera que empiecen con cada letra de la A a la Z. El primero en llegar a la Z gana!'},
        {'name_en': 'Color Hunt', 'name_fr': 'Chasse aux couleurs', 'name_es': 'Caza de colores',
         'instructions_en': 'Pick a color and find as many things of that color outside as you can.',
         'instructions_fr': 'Choisissez une couleur et trouvez autant de choses de cette couleur dehors que possible.',
         'instructions_es': 'Elige un color y encuentra tantas cosas de ese color afuera como puedas.'},
        {'name_en': 'Would You Rather?', 'name_fr': 'Tu préfères?', 'name_es': '¿Qué prefieres?',
         'instructions_en': 'Take turns asking silly would-you-rather questions. No wrong answers!',
         'instructions_fr': 'À tour de rôle, posez des questions tu-préfères idiotes. Pas de mauvaises réponses!',
         'instructions_es': 'Por turnos, hagan preguntas tontas de qué-prefieres. ¡No hay respuestas incorrectas!'},
        {'name_en': 'Count the Cows', 'name_fr': 'Compter les vaches', 'name_es': 'Contar vacas',
         'instructions_en': 'Each person counts cows on their side of the car. Most cows at the destination wins!',
         'instructions_fr': 'Chaque personne compte les vaches de son côté de la voiture. Le plus de vaches à destination gagne!',
         'instructions_es': 'Cada persona cuenta las vacas de su lado del coche. ¡Quien tenga más vacas al llegar gana!'},
        {'name_en': 'Name That Tune', 'name_fr': 'Reconnaître la chanson', 'name_es': 'Adivina la canción',
         'instructions_en': 'Hum or sing a few notes of a song. First person to name the tune gets a point!',
         'instructions_fr': 'Fredonnez ou chantez quelques notes d\'une chanson. Le premier à reconnaître la chanson gagne un point!',
         'instructions_es': 'Tararea o canta unas notas de una canción. ¡El primero en adivinar la canción gana un punto!'},
        {'name_en': 'Memory Game', 'name_fr': 'Jeu de mémoire', 'name_es': 'Juego de memoria',
         'instructions_en': '"I packed my bag and brought..." — each person repeats the list and adds one new item.',
         'instructions_fr': '« J\'ai préparé mon sac et j\'ai apporté... » — chaque personne répète la liste et ajoute un nouvel objet.',
         'instructions_es': '«Empaqué mi maleta y traje...» — cada persona repite la lista y añade un artículo nuevo.'},
        {'name_en': 'Cloud Shapes', 'name_fr': 'Formes de nuages', 'name_es': 'Formas de nubes',
         'instructions_en': 'Look at the clouds and describe what shapes you see. A dragon? An ice cream cone?',
         'instructions_fr': 'Regardez les nuages et décrivez les formes que vous voyez. Un dragon? Une glace?',
         'instructions_es': 'Mira las nubes y describe las formas que ves. ¿Un dragón? ¿Un cono de helado?'},
    ]
    count = 0
    for g in games:
        _, created = CarGame.objects.get_or_create(genre=genre, name_en=g['name_en'],
                                       defaults={'name_fr': g['name_fr'], 'name_es': g['name_es'],
                                                 'instructions_en': g['instructions_en'],
                                                 'instructions_fr': g['instructions_fr'],
                                                 'instructions_es': g['instructions_es']})
        if created:
            count += 1
    stdout.write(f'  Seeded {count} new car games (total {CarGame.objects.filter(genre=genre).count()})')

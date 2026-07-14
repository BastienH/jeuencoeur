"""
Populate Genre descriptions from Games.md content.
Each description includes: 1 paragraph + tip + timeframe.
"""
from django.db import migrations

DESCRIPTIONS = {
    'giggle-generators': {
        'en': (
            "Tap to get an easy, quick, silly moment to share with your kids. "
            "The app acts as a rapid-fire silly prompt generator — with a single tap, "
            "a completely ridiculous 10-second task appears, like \"Waddle like a penguin "
            "while brushing your teeth\" or \"Introduce yourself as a very serious judge.\" "
            "Zero prep, high-impact giggles with a shake-to-refresh feature for when you "
            "need the next prompt immediately.\n\n"
            "**Tip:** Great for spontaneous moments when energy is high but attention spans are short.\n\n"
            "**Timeframe:** Gets hilarious within the first 2 minutes."
        ),
        'fr': (
            "Appuie pour obtenir un moment rapide et silly à partager avec tes enfants. "
            "L'application agit comme un générateur de défis amusants en rafale — en un seul "
            "appuie, une tâche complètement ridicule de 10 secondes apparaît, comme « Fais "
            "le pingouin en te brossant les dents » ou « Présente-toi comme un juge très "
            "sérieux ». Zéro préparation, des rires garantis avec un secouer pour actualiser "
            "quand tu as besoin de la prochaine idée immédiatement.\n\n"
            "**Astuce :** Parfait pour les moments spontanés quand l'énergie est haute mais "
            "la concentration est courte.\n\n"
            "**Durée :** Devient hilarant dans les 2 premières minutes."
        ),
        'es': (
            "Toca para obtener un momento rápido y divertido para compartir con tus hijos. "
            "La aplicación actúa como un generador de desafíos graciosos a toda velocidad — "
            "con un solo toque, aparece una tarea completamente ridícula de 10 segundos, "
            "como « Camina como un pingüino mientras te cepillas los dientes » o "
            "« Preséntate como un juez muy serio ». Cero preparación, risas garantizadas "
            "con una función agitar para actualizar cuando necesites la siguiente idea "
            "inmediatamente.\n\n"
            "**Consejo:** Ideal para momentos espontáneos cuando la energía es alta pero "
            "la atención es corta.\n\n"
            "**Tiempo:** Se vuelve hilarante en los primeros 2 minutos."
        ),
    },
    'choice-chaos': {
        'en': (
            "Silly either-or questions to build connection through conversation. "
            "The app provides age-appropriate \"Would You Rather\" questions with a voice "
            "changer toggle — hear the question read aloud in a goofy robot voice, helium "
            "voice, or scary monster voice. Features a \"Reroll\" button if a question flops, "
            "ensuring the conversation never stalls.\n\n"
            "**Tip:** Perfect for car rides, dinner table, or any time you want to spark "
            "laughter through conversation.\n\n"
            "**Timeframe:** Gets fun after 5-6 questions when everyone loosens up."
        ),
        'fr': (
            "Des questions amusantes du type « Tu préfères » pour créer des liens par la "
            "conversation. L'application fournit des questions adaptées à l'âge avec un "
            "changeur de voix — écoute la question lue à voix haute en voix de robot, "
            "voix d'hélium ou voix de monstre effrayant. Bouton « Nouvelle question » si "
            "une question ne fonctionne pas, pour que la conversation ne stagne jamais.\n\n"
            "**Astuce :** Parfait pour les trajets en voiture, à table, ou quand tu veux "
            "déclencher des rires par la conversation.\n\n"
            "**Durée :** Devient amusant après 5-6 questions quand tout le monde se détend."
        ),
        'es': (
            "Preguntas graciosas del tipo «¿Qué prefieres?» para crear conexiones a través "
            "de la conversación. La aplicación proporciona preguntas apropiadas para la edad "
            "con un cambio de voz — escucha la pregunta leída en voz alta con voz de robot, "
            "voz de helio o voz de monstruo aterrador. Botón « Siguiente » si una pregunta "
            "no funciona, para que la conversación nunca se estanque.\n\n"
            "**Consejo:** Perfecto para viajes en auto, la cena, o cuando quieras provocar "
            "risas a través de la conversación.\n\n"
            "**Tiempo:** Se vuelve divertido después de 5-6 preguntas cuando todos se relajan."
        ),
    },
    'tale-twisters': {
        'en': (
            "Create a family story together with title prompts, twists, and an easy way "
            "to record and save the magic. The app provides the opening line and a "
            "\"Random Plot Device\" button. Every time a family member adds a sentence, "
            "they hit a \"Twist!\" button, which inserts a chaotic, unexpected element "
            "into the narrative. The app records the entire unscripted family story session, "
            "saving it as an audio file for parents to treasure forever.\n\n"
            "**Tip:** Best for quiet evenings or rainy days when you have 15-20 minutes to "
            "build a story together.\n\n"
            "**Timeframe:** The magic happens after the first twist — usually around 5 minutes in."
        ),
        'fr': (
            "Crée une histoire en famille avec des idées de titres, des rebondissements, "
            "et un moyen facile d'enregistrer et de sauvegarder la magie. L'application "
            "fournit la première phrase et un bouton « Aléatoire ». Chaque fois qu'un "
            "membre de la famille ajoute une phrase, il appuie sur le bouton « "
            "Rebondissement ! », qui insère un élément chaotique et inattendu dans le "
            "récit. L'application enregistre toute la session d'histoire familiale, la "
            "sauvegardant comme fichier audio pour que les parents la chérissent à jamais.\n\n"
            "**Astuce :** Idéal pour les soirées calmes ou les jours de pluie quand tu as "
            "15-20 minutes pour construire une histoire ensemble.\n\n"
            "**Durée :** La magie se produit après le premier rebondissement — généralement "
            "vers la 5ème minute."
        ),
        'es': (
            "Crea una historia familiar con ideas de giros, giros argumentales, y una forma "
            "fácil de grabar y guardar la magia. La aplicación proporciona la primera línea "
            "y un botón « Aleatorio ». Cada vez que un miembro de la familia agrega una "
            "oración, presiona el botón « ¡Giro! », que inserta un elemento caótico e "
            "inesperado en la narrativa. La aplicación graba toda la sesión de historia "
            "familiar, guardándola como archivo audio para que los padres la atesoren para "
            "siempre.\n\n"
            "**Consejo:** Mejor para tardes tranquilas o días lluviosos cuando tienes 15-20 "
            "minutos para construir una historia juntos.\n\n"
            "**Tiempo:** La magia sucede después del primer giro — generalmente a los 5 minutos."
        ),
    },
    'mimic-mayhem': {
        'en': (
            "Fun, random noise prompts that redirect loud kiddo energy into lighthearted "
            "play. The app acts as a soundboard that fires off random, goofy audio clips — "
            "a honking goose, a popping bubble, a drill, or a crying baby. A visual volume "
            "meter fills up as the child mimics the sound as loudly as possible, then plays "
            "a gentle \"Shush\" sound that turns winding down from a loud moment into a game "
            "in itself.\n\n"
            "**Tip:** Ideal for burning off energy indoors or transitioning from loud play to "
            "quiet time.\n\n"
            "**Timeframe:** Gets hilarious immediately — watch their face when the shush sound plays."
        ),
        'fr': (
            "Des bruits aléatoires amusants qui redirigent l'énergie des enfants vers un "
            "jeu léger. L'agit comme une table de mixage qui lance des clips audio "
            "aléatoires et rigolos — un oie qui klaxonne, une bulle qui éclate, une perceuse, "
            "ou un bébé qui pleure. Un compteur de volume visuel se remplit tandis que l'enfant "
            "imite le son aussi fort que possible, puis joue un doux « Chut » qui transforme "
            "le passage du bruit au calme en un jeu en soi.\n\n"
            "**Astuce :** Idéal pour dépenser de l'énergie à l'intérieur ou pour passer du "
            "jeu bruyant au moment calme.\n\n"
            "**Durée :** Devient hilarant immédiatement — regarde leur visage quand le chut joue."
        ),
        'es': (
            "Sonidos aleatorios divertidos que redirigen la energía de los niños hacia un "
            "juego ligero. La aplicación actúa como una mesa de mezclas que lanza clips de "
            "audio aleatorios y graciosos — un ganso que toca la bocina, una burbuja que "
            "revienta, un taladro, o un bebé llorando. Un medidor de volumen visual se llena "
            "mientras el niño imita el sonido lo más fuerte posible, luego reproduce un suave "
            "« ¡Shh! » que convierte el paso del ruido al silencio en un juego.\n\n"
            "**Consejo:** Ideal para gastar energía adentro o para pasar del juego ruidoso al "
            "momento tranquilo.\n\n"
            "**Tiempo:** Se vuelve hilarante inmediatamente — mira su cara cuando suena el shh."
        ),
    },
    'wild-roles': {
        'en': (
            "Spin, act, and laugh! The app randomly combines a character, a setting, and an "
            "activity — like \"You are a very clumsy ninja trying to make a sandwich\" or "
            "\"You are a tired dinosaur at a dance party.\" Features a 30-second countdown "
            "timer to add silly pressure, and emoji vote buttons where family members can "
            "tap a laughing face or a star to score the best performance.\n\n"
            "**Tip:** Great for group play with 3+ people — the more dramatic the acting, the "
            "better.\n\n"
            "**Timeframe:** Peaks after 10-15 minutes when everyone gets into character."
        ),
        'fr': (
            "Tourne, joue, et ris ! L'application combine aléatoirement un personnage, un "
            "cadre, et une activité — comme « Tu es un ninja très maladroit qui essaie de "
            "faire un sandwich » ou « Tu es un dinosaure fatigué à une soirée dansante ». "
            "Minuteur de 30 secondes pour ajouter une pression amusante, et des boutons "
            "de vote emoji où les membres de la famille peuvent appuyer sur un visage "
            "qui rit ou une étoile pour noter la meilleure performance.\n\n"
            "**Astuce :** Parfait pour jouer à 3+ personnes — plus le jeu est dramatique, "
            "mieux c'est.\n\n"
            "**Durée :** Atint son apogée après 10-15 minutes quand tout le monde entre "
            "dans son personnage."
        ),
        'es': (
            "¡Gira, actúa, y ríe! La aplicación combina aleatoriamente un personaje, un "
            "escenario, y una actividad — como « Eres un ninja muy torpe tratando de hacer "
            "un sándwich » o « Eres un dinosaurio cansado en una fiesta de baile ». Temporizador "
            "de 30 segundos para añadir presión divertida, y botones de voto emoji donde los "
            "miembros de la familia pueden tocar una cara riendo o una estrella para puntuar "
            "la mejor actuación.\n\n"
            "**Consejo:** Genial para jugar en grupo con 3+ personas — cuanto más dramática "
            "la actuación, mejor.\n\n"
            "**Tiempo:** Alcanza su punto máximo después de 10-15 minutos cuando todos entran "
            "en personaje."
        ),
    },
    'funny-face-factory': {
        'en': (
            "Facial expression challenges that turn quiet play into a hilarious reveal party. "
            "The app shows a prompt for a specific, difficult expression — like \"A dinosaur "
            "who just ate a lemon\" or \"A robot who smells toast burning.\" After the kid "
            "makes the face, a surprise digital filter (rainbow barf, bunny ears, funny "
            "mustache) is applied to the photo, turning the quiet activity into a laughing "
            "fit.\n\n"
            "**Tip:** Perfect for quiet time — great when you need calm play that's still "
            "silly.\n\n"
            "**Timeframe:** Gets funny immediately, especially with the filter reveal."
        ),
        'fr': (
            "Des défis d'expressions faciales qui transforment un jeu calme en une fête "
            "drôle. L'application montre un défi pour une expression spécifique et difficile "
            "— comme « Un dinosaure qui vient de manger un citron » ou « Un robot qui sent "
            "le pain grillé brûler ». Après que l'enfant a fait la tête, un filtre numérique "
            "surpris (vomissement arc-en-ciel, oreilles de lapin, moustache drôle) est "
            "appliqué à la photo, transformant l'activité calme en un fou rire.\n\n"
            "**Astuce :** Parfait pour le temps calme — idéal quand tu as besoin d'un jeu "
            "tranquille mais drôle.\n\n"
            "**Durée :** Devient drôle immédiatement, surtout avec la révélation du filtre."
        ),
        'es': (
            "Desafíos de expresiones faciales que convierten el juego tranquilo en una fiesta "
            "divertida. La aplicación muestra un desafío para una expresión específica y difícil "
            "— como « Un dinosaurio que acaba de comer un limón » o « Un robot que huele tostado "
            "quemándose ». Después de que el niño hace la cara, un filtro digital sorpresa "
            "(vómito arcoíris, orejas de conejo, bigote divertido) se aplica a la foto, "
            "convirtiendo la actividad tranquila en una carcajada.\n\n"
            "**Consejo:** Perfecto para el tiempo tranquilo — ideal cuando necesitas un juego "
            "calmo pero divertido.\n\n"
            "**Tiempo:** Se vuelve divertido inmediatamente, especialmente con la revelación del filtro."
        ),
    },
    'lip-sync-legends': {
        'en': (
            "Surprise sound effects to lip sync and act out for a little dose of silly fun. "
            "One player reads the sound prompt aloud or makes the noise, while the other "
            "player silently acts it out using only their face and body — no talking or "
            "mouthing words, just sounds and movement! Features a \"How to play\" guide and "
            "tips for bringing sounds to life.\n\n"
            "**Tip:** Best with exactly 2 players — great for parent-child bonding moments.\n\n"
            "**Timeframe:** Gets competitive and hilarious around the 5-minute mark."
        ),
        'fr': (
            "Des effets sonores surprise à lip sync et à jouer pour une dose de fun. "
            "Un joueur lit le défi sonore à voix haute ou fait le bruit, tandis que l'autre "
            "joueur le joue silencieusement en utilisant seulement son visage et son corps — "
            "pas de paroles, juste des sons et du mouvement ! Guide « Comment jouer » et "
            "astuces pour donner vie aux sons.\n\n"
            "**Astuce :** Idéal avec exactement 2 joueurs — parfait pour les moments de "
            "complicité parent-enfant.\n\n"
            "**Durée :** Devient compétitif et hilarant vers la 5ème minute."
        ),
        'es': (
            "Efectos de sonido sorpresa para lip sync y actuar para una dosis de diversión. "
            "Un jugador lee el desafío de sonido en voz alta o hace el ruido, mientras el "
            "otro jugador lo actúa silenciosamente usando solo su cara y cuerpo — ¡sin hablar, "
            "solo sonidos y movimiento! Guía «Cómo jugar» y consejos para dar vida a los sonidos.\n\n"
            "**Consejo:** Mejor con exactamente 2 jugadores — ideal para momentos de unión "
            "padre-hijo.\n\n"
            "**Tiempo:** Se vuelve competitivo e hilarante alrededor del minuto 5."
        ),
    },
    'highway-hijinks': {
        'en': (
            "Beat backseat boredom with 20+ car games for connection. The app suggests "
            "games based on your surroundings — \"Spot 5 blue cars,\" \"Next time you see "
            "a round sign, yell YIPPEE!\" Features a prominent \"Boredom Buster\" button "
            "that instantly shuffles to a new screen-free car game like \"I-Spy,\" "
            "\"20 Questions,\" or \"The License Plate Game.\"\n\n"
            "**Tip:** Start the trip with it and let passengers take turns picking games.\n\n"
            "**Timeframe:** Gets fun after 10 minutes when everyone's engaged — perfect for "
            "trips over 30 minutes."
        ),
        'fr': (
            "Fini l'ennui sur la banquette arrière avec 20+ jeux de voiture pour créer des "
            "liens. L'application suggère des jeux selon vos alentours — « Repère 5 voitures "
            "bleues », « La prochaine fois que tu vois un panneau rond, crie YIPPEE ! ». "
            "Bouton « Anti-Ennui » qui mélange instantanément un nouveau jeu sans écran "
            "comme « Je vois, je vois », « 20 Questions », ou « Le jeu des plaques "
            "d'immatriculation ».\n\n"
            "**Astuce :** Commence le voyage avec et laisse les passagers tourner pour choisir "
            "les jeux.\n\n"
            "**Durée :** Devient amusant après 10 minutes quand tout le monde est engagé — "
            "parfait pour les voyages de plus de 30 minutes."
        ),
        'es': (
            "Adiós al aburrimiento en el asiento trasero con 20+ juegos de auto para crear "
            "conexiones. La aplicación sugiere juegos según tu entorno — « Encuentra 5 autos "
            "azules », « La próxima vez que veas una señal redonda, grita ¡YIPPEE! ». Botón "
            "« Anti-Aburrimiento » que mezcla instantáneamente un nuevo juego sin pantalla "
            "como « Veo, veo », « 20 Preguntas », o « El juego de las placas ».\n\n"
            "**Consejo:** Empieza el viaje con ella y deja que los pasajeros turnen para elegir "
            "los juegos.\n\n"
            "**Tiempo:** Se vuelve divertido después de 10 minutos cuando todos están参与 — "
            "perfecto para viajes de más de 30 minutos."
        ),
    },
    'doodle-dash': {
        'en': (
            "Mix and match silly prompts for hilarious family doodling fun. The app generates "
            "prompts by randomly combining a subject, an emotion, and a color palette — like "
            "\"Doodle a confused squirrel wearing pink shoes.\" Choose between guided mode "
            "with prompts or free draw mode, with an optional timer to add playful pressure. "
            "Save your masterpieces to the gallery or print them.\n\n"
            "**Tip:** Great for rainy days, quiet time, or when siblings need a cooperative "
            "activity.\n\n"
            "**Timeframe:** Gets creative and funny after 3-4 prompts when the silly combos pile up."
        ),
        'fr': (
            "Mélange et combine des idées drôles pour un dessin en famille hilarant. "
            "L'application génère des idées en combinant aléatoirement un sujet, une émotion, "
            "et une palette de couleurs — comme « Dessine un écureuil confus portant des "
            "chaussures roses ». Choisis entre le mode guidé avec des idées ou le mode "
            "dessin libre, avec un timer optionnel pour ajouter une pression ludique. "
            "Sauvegarde tes chefs-d'œuvre dans la galerie ou imprime-les.\n\n"
            "**Astuce :** Parfait pour les jours de pluie, le temps calme, ou quand les "
            "frères et sœurs ont besoin d'une activité coopérative.\n\n"
            "**Durée :** Devient créatif et drôle après 3-4 idées quand les combinaisons "
            "s'accumulent."
        ),
        'es': (
            "Mezcla y combina ideas graciosas para dibujar en familia de forma hilarante. "
            "La aplicación genera ideas combinando aleatoriamente un sujeto, una emoción, "
            "y una paleta de colores — como « Dibuja una ardilla confusa usando zapatos "
            "rosa ». Elige entre modo guiado con ideas o modo dibujo libre, con un temporizador "
            "opcional para añadir presión juguetona. Guarda tus obras maestras en la galería "
            "o imprímelas.\n\n"
            "**Consejo:** Genial para días lluviosos, tiempo tranquilo, o cuando los hermanos "
            "necesitan una actividad cooperativa.\n\n"
            "**Tiempo:** Se vuelve creativo y divertido después de 3-4 ideas cuando las "
            "combinaciones graciosas se acumulan."
        ),
    },
}


def populate_descriptions(apps, schema_editor):
    Genre = apps.get_model('games', 'Genre')
    for slug, descriptions in DESCRIPTIONS.items():
        try:
            genre = Genre.objects.get(slug=slug)
        except Genre.DoesNotExist:
            continue
        genre.description = descriptions['en']
        genre.description_fr = descriptions['fr']
        genre.description_es = descriptions['es']
        genre.save(update_fields=['description', 'description_fr', 'description_es'])


def reverse_descriptions(apps, schema_editor):
    Genre = apps.get_model('games', 'Genre')
    Genre.objects.update(description='', description_fr='', description_es='')


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0011_add_genre_descriptions'),
    ]

    operations = [
        migrations.RunPython(populate_descriptions, reverse_descriptions),
    ]

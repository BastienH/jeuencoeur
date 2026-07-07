import csv

from django.core.management.base import BaseCommand

from games.models import Genre, Prompt, StorySeed

GENRES = [
    {'name': 'Giggle Generators', 'slug': 'giggle-generators', 'icon': '😂', 'tagline': 'Tap for instant laughs!', 'game_module': 'giggle_generators'},
    {'name': 'Choice Chaos', 'slug': 'choice-chaos', 'icon': '🤔', 'tagline': 'Silly debates for everyone!', 'game_module': 'choice_chaos'},
    {'name': 'Tale Twisters', 'slug': 'tale-twisters', 'icon': '📖', 'tagline': 'Collaborative story fun', 'game_module': 'tale_twisters'},
    {'name': 'Mimic Mayhem', 'slug': 'mimic-mayhem', 'icon': '🔊', 'tagline': 'Imitate the sound!', 'game_module': 'mimic_mayhem'},
    {'name': 'Wild Roles', 'slug': 'wild-roles', 'icon': '🎭', 'tagline': 'Spin, act, and laugh!', 'game_module': 'wild_roles'},
    {'name': 'Funny Face Factory', 'slug': 'funny-face-factory', 'icon': '📸', 'tagline': 'Make your silliest face!', 'game_module': 'funny_face_factory'},
    {'name': 'Lip-Sync Legends', 'slug': 'lip-sync-legends', 'icon': '🎤', 'tagline': 'Act out that sound!', 'game_module': 'lip_sync_legends'},
    {'name': 'Highway Hijinks', 'slug': 'highway-hijinks', 'icon': '🚗', 'tagline': 'Beat backseat boredom!', 'game_module': 'highway_hijinks'},
    {'name': 'Doodle Dash', 'slug': 'doodle-dash', 'icon': '🎨', 'tagline': 'Draw what you imagine!', 'game_module': 'doodle_dash'},
]

PROMPTS_CSV = """genre_slug,category,text_en,text_fr,text_es
giggle-generators,Mealtime,What is the silliest face you can make with your food?,Quelle est la grimace la plus idiote que tu puisses faire avec ta nourriture?,¿Cuál es la cara más tonta que puedes hacer con tu comida?
giggle-generators,Mealtime,If your spoon could talk what would it say?,Si ta cuillère pouvait parler que dirait-elle?,Si tu cuchara pudiera hablar ¿qué diría?
giggle-generators,Mealtime,Pretend your drink is a magical potion. What does it do?,Fais comme si ta boisson était une potion magique. Que fait-elle?,Imagina que tu bebida es una poción mágica. ¿Qué hace?
giggle-generators,Bedtime,What color is the sound of silence?,De quelle couleur est le bruit du silence?,¿De qué color es el sonido del silencio?
giggle-generators,Bedtime,If your pillow could tell stories what would it say?,Si ton oreiller pouvait raconter des histoires que dirait-il?,Si tu almohada pudiera contar historias ¿qué diría?
giggle-generators,Bedtime,What do your dreams taste like?,À quoi ressemblent tes rêves?,¿A qué saben tus sueños?
giggle-generators,Car rides,How many cows do you think we will see today?,Combien de vaches penses-tu qu'on va voir aujourd'hui?,¿Cuántas vacas crees que veremos hoy?
giggle-generators,Car rides,If the clouds were made of cotton candy which one would you eat?,Si les nuages étaient faits de barbe à papa lequel mangerais-tu?,Si las nubes fueran de algodón de azúcar ¿cuál te comerías?
giggle-generators,Car rides,Make up a song about the car in front of us,Invente une chanson sur la voiture devant nous,Inventa una canción sobre el coche que está delante de nosotros
giggle-generators,Bath time,If your bath toys threw a party what would it look like?,Si tes jouets de bain organisaient une fête à quoi ressemblerait-elle?,Si tus juguetes de baño hicieran una fiesta ¿cómo sería?
giggle-generators,Bath time,What superpower does your rubber duck have?,Quel super-pouvoir a ton canard en caoutchouc?,¿Qué superpoder tiene tu patito de goma?
giggle-generators,Bath time,Pretend the bubbles are clouds. Where are you flying?,Fais comme si les bulles étaient des nuages. Où voles-tu?,Imagina que las burbujas son nubes. ¿Dónde estás volando?
giggle-generators,Playtime,If your toys had a secret meeting what would they talk about?,Si tes jouets avaient une réunion secrète de quoi parleraient-ils?,Si tus juguetes tuvieran una reunión secreta ¿de qué hablarían?
giggle-generators,Playtime,What game would you invent if you could make any rules?,Quel jeu inventerais-tu si tu pouvais créer n'importe quelles règles?,¿Qué juego inventarías si pudieras crear cualquier regla?
giggle-generators,Playtime,If you could trade places with your favorite toy for a day what would you do?,Si tu pouvais échanger ta place avec ton jouet préféré pour un jour que ferais-tu?,Si pudieras intercambiar lugares con tu juguete favorito por un día ¿qué harías?
giggle-generators,Outdoor,What would you name every tree in the yard?,Quel nom donnerais-tu à chaque arbre du jardin?,¿Qué nombre le pondrías a cada árbol del jardín?
giggle-generators,Outdoor,If the wind could whisper secrets what would it tell you?,Si le vent pouvait chuchoter des secrets que te dirait-il?,Si el viento pudiera susurrar secretos ¿qué te diría?
giggle-generators,Outdoor,What kind of bug would you want to be for a day?,Quel genre d'insecte voudrais-tu être pour un jour?,¿Qué tipo de insecto te gustaría ser por un día?
giggle-generators,Quiet time,Tell me about a dream you remember,Raconte-moi un rêve dont tu te souviens,Cuéntame un sueño que recuerdes
giggle-generators,Quiet time,What is the most beautiful thing you have ever seen?,Quelle est la plus belle chose que tu aies jamais vue?,¿Cuál es la cosa más hermosa que has visto?
choice-chaos,,What is the funniest word you know?,Quel est le mot le plus drôle que tu connaisses?,¿Cuál es la palabra más divertida que conoces?
choice-chaos,,Can you laugh without opening your mouth?,Peux-tu rire sans ouvrir la bouche?,¿Puedes reírte sin abrir la boca?
choice-chaos,,Make a funny face and hold it for 10 seconds,Fais une grimace et tiens-la pendant 10 secondes,Haz una cara graciosa y mantenla por 10 segundos
choice-chaos,,What sound does a happy hippo make?,Quel son fait un hippopotame heureux?,¿Qué sonido hace un hipopótamo feliz?
choice-chaos,,Tell a joke in three words,Raconte une blague en trois mots,Cuenta un chiste en tres palabras
choice-chaos,,Imitate your parents' voice saying something silly,Imite la voix de tes parents disant quelque chose de drôle,Imita la voz de tus padres diciendo algo gracioso
choice-chaos,,What would a chicken say if it could talk?,'Que dirait un poulet s''il pouvait parler?',¿Qué diría un pollo si pudiera hablar?
choice-chaos,,Make up a silly dance move and name it,Invente un pas de danse idiot et donne-lui un nom,Inventa un movimiento de baile tonto y ponle nombre
choice-chaos,,What is the most ridiculous outfit you can imagine?,Quelle est la tenue la plus ridicule que tu puisses imaginer?,¿Cuál es el atuendo más ridículo que puedas imaginar?
choice-chaos,,Pretend your hand is a talking animal. Introduce yourself,Fais comme si ta main était un animal qui parle. Présente-toi,Imagina que tu mano es un animal que habla. Preséntate
choice-chaos,,What would make a robot laugh?,Qu'est-ce qui ferait rire un robot?,¿Qué haría reír a un robot?
choice-chaos,,Sing a sentence like an opera singer,Chante une phrase comme un chanteur d'opéra,Canta una frase como un cantante de ópera
choice-chaos,,Make the silliest face possible,Fais la grimace la plus idiote possible,Haz la cara más tonta posible
choice-chaos,,What if animals could talk? Which one would be the funniest?,Et si les animaux pouvaient parler? Lequel serait le plus drôle?,¿Y si los animales pudieran hablar? ¿Cuál sería el más divertido?
choice-chaos,,Try to say the alphabet backwards as fast as you can,Essaie de dire l'alphabet à l'envers le plus vite possible,Intenta decir el alfabeto al revés lo más rápido posible
choice-chaos,,Make a sound effect for every action you do for one minute,Fais un bruitage pour chaque action que tu fais pendant une minute,Haz un efecto de sonido para cada acción que hagas durante un minuto
choice-chaos,,What is the weirdest food combination you can think of?,Quelle est la combinaison d'aliments la plus étrange à laquelle tu puisses penser?,¿Cuál es la combinación de alimentos más extraña que se te ocurra?
choice-chaos,,Tell a story using only sounds,Raconte une histoire en utilisant seulement des sons,Cuenta una historia usando solo sonidos
choice-chaos,,Draw a monster with your eyes closed,Dessine un monstre les yeux fermés,Dibuja un monstruo con los ojos cerrados
choice-chaos,,What would a laughing tree sound like?,À quoi ressemblerait le rire d'un arbre?,¿Cómo sonaría un árbol riendo?
tale-twisters,,Once upon a time there was a purple elephant who...,Il était une fois un éléphant violet qui...,Érase una vez un elefante violeta que...
tale-twisters,,If you found a magic key what door would it open?,Si tu trouvais une clé magique quelle porte ouvrirait-elle?,Si encontraras una llave mágica ¿qué puerta abriría?
tale-twisters,,Tell a story about a brave little raindrop,Raconte une histoire sur une petite goutte de pluie courageuse,Cuenta una historia sobre una valiente gotita de lluvia
tale-twisters,,What happened when the sun forgot to rise?,Que s'est-il passé quand le soleil a oublié de se lever?,¿Qué pasó cuando el sol olvidó salir?
tale-twisters,,Describe a world where everything is made of marshmallows,Décris un monde où tout est fait de guimauves,Describe un mundo donde todo está hecho de malvaviscos
tale-twisters,,Tell the story of a pirate who was afraid of water,Raconte l'histoire d'un pirate qui avait peur de l'eau,Cuenta la historia de un pirata que le tenía miedo al agua
tale-twisters,,What if your shadow had its own adventures?,Et si ton ombre avait ses propres aventures?,¿Y si tu sombra tuviera sus propias aventuras?
tale-twisters,,Create a story about a flying bicycle,Crée une histoire sur un vélo volant,Crea una historia sobre una bicicleta voladora
tale-twisters,,Tell me about the day the toys took over the house,Raconte-moi le jour où les jouets ont pris le contrôle de la maison,Cuéntame sobre el día en que los juguetes tomaron la casa
tale-twisters,,What is at the top of the tallest mountain in the world?,Qu'y a-t-il au sommet de la plus haute montagne du monde?,¿Qué hay en la cima de la montaña más alta del mundo?
tale-twisters,,Imagine you could talk to animals. What would you ask?,Imagine que tu peux parler aux animaux. Que demanderais-tu?,Imagina que puedes hablar con los animales. ¿Qué les preguntarías?
tale-twisters,,Write a story about a star that fell to Earth,Écris une histoire sur une étoile tombée sur Terre,Escribe una historia sobre una estrella que cayó a la Tierra
tale-twisters,,What would a day in the life of a cloud look like?,À quoi ressemblerait une journée dans la vie d'un nuage?,¿Cómo sería un día en la vida de una nube?
tale-twisters,,Tell a story from the perspective of your pet,Raconte une histoire du point de vue de ton animal,Cuenta una historia desde la perspectiva de tu mascota
tale-twisters,,If you built a city in the clouds what would it have?,Si tu construisais une ville dans les nuages qu'aurait-elle?,Si construyeras una ciudad en las nubes ¿qué tendría?
tale-twisters,,What secret message would you put in a bottle?,Quel message secret mettrais-tu dans une bouteille?,¿Qué mensaje secreto pondrías en una botella?
tale-twisters,,Tell the story of a caterpillar who did not want to become a butterfly,Raconte l'histoire d'une chenille qui ne voulait pas devenir papillon,Cuenta la historia de una oruga que no quería convertirse en mariposa
tale-twisters,,Describe a magical forest where plants sing,Décris une forêt magique où les plantes chantent,Describe un bosque mágico donde las plantas cantan
tale-twisters,,What would you do if you found a genie lamp?,Que ferais-tu si tu trouvais une lampe à génie?,¿Qué harías si encontraras una lámpara de genio?
tale-twisters,,Make up a legend about how the moon was created,Invente une légende sur la création de la lune,Inventa una leyenda sobre cómo se creó la luna
mimic-mayhem,,Walk backward for 30 seconds,Marche à reculons pendant 30 secondes,Camina hacia atrás durante 30 segundos
mimic-mayhem,,Speak in a robot voice for the next minute,Parle avec une voix de robot pendant la prochaine minute,Habla con voz de robot durante el próximo minuto
mimic-mayhem,,Hop on one foot around the room,Saute à cloche-pied autour de la pièce,Salta en un pie alrededor de la habitación
mimic-mayhem,,Do your best animal impression for 15 seconds,Fais ta meilleure imitation d'animal pendant 15 secondes,Haz tu mejor imitación de animal durante 15 segundos
mimic-mayhem,,Spin around 5 times and try to walk in a straight line,Tourne sur toi-même 5 fois et essaie de marcher en ligne droite,Gira 5 veces y trata de caminar en línea recta
mimic-mayhem,,Sing everything you say for the next minute,Chante tout ce que tu dis pendant la minute suivante,Canta todo lo que digas durante el próximo minuto
mimic-mayhem,,Balance a book on your head for 30 seconds,Garde un livre en équilibre sur ta tête pendant 30 secondes,Equilibra un libro sobre tu cabeza durante 30 segundos
mimic-mayhem,,Talk without moving your lips,Parle sans bouger les lèvres,Habla sin mover los labios
mimic-mayhem,,Do 10 silly jumping jacks,Fais 10 jumping jacks idiots,Haz 10 jumping jacks tontos
mimic-mayhem,,Keep a straight face while everyone tries to make you laugh,Garde ton sérieux pendant que tout le monde essaie de te faire rire,Mantén la cara seria mientras todos intentan hacerte reír
mimic-mayhem,,Walk like a penguin to the next room,Marche comme un pingouin jusqu'à la pièce suivante,Camina como un pingüino hasta la próxima habitación
mimic-mayhem,,Make a tower using only your body,Construis une tour en utilisant seulement ton corps,Construye una torre usando solo tu cuerpo
mimic-mayhem,,Eat something using only your non-dominant hand,Mange quelque chose en utilisant seulement ta main non dominante,Come algo usando solo tu mano no dominante
mimic-mayhem,,Whisper everything for 2 minutes,Chuchote tout pendant 2 minutes,Di todo en susurros durante 2 minutos
mimic-mayhem,,Keep a balloon in the air for 30 seconds without using your hands,Garde un ballon en l'air pendant 30 secondes sans utiliser tes mains,Mantén un globo en el aire durante 30 segundos sin usar las manos
mimic-mayhem,,Do a dramatic slow-motion walk across the room,Fais une traversée dramatique au ralenti de la pièce,Haz un cruce dramático en cámara lenta por la habitación
mimic-mayhem,,Imitate a news reporter describing what is happening in the room,Imite un journaliste décrivant ce qui se passe dans la pièce,Imita a un reportero describiendo lo que sucede en la habitación
mimic-mayhem,,Close your eyes and describe the room from memory,Ferme les yeux et décris la pièce de mémoire,Cierra los ojos y describe la habitación de memoria
mimic-mayhem,,Stand on one leg and count to 20,Tiens-toi sur une jambe et compte jusqu'à 20,Párate en una pierna y cuenta hasta 20
mimic-mayhem,,Crawl like a baby to the nearest chair,Rampe comme un bébé jusqu'à la chaise la plus proche,Gatea como un bebé hasta la silla más cercana
wild-roles,,What has keys but cannot open doors? (A piano),Qu'est-ce qui a des touches mais ne peut pas ouvrir de portes? (Un piano),¿Qué tiene llaves pero no puede abrir puertas? (Un piano)
wild-roles,,I follow you all day but you never catch me. What am I? (Your shadow),Je te suis toute la journée mais tu ne peux jamais m'attraper. Que suis-je? (Ton ombre),Te sigo todo el día pero nunca me atrapas. ¿Qué soy? (Tu sombra)
wild-roles,,What gets wetter the more it dries? (A towel),Qu'est-ce qui devient plus mouillé plus il sèche? (Une serviette),¿Qué se moja más cuanto más seca? (Una toalla)
wild-roles,,What has a head and a tail but no body? (A coin),Qu'est-ce qui a une tête et une queue mais pas de corps? (Une pièce),¿Qué tiene cabeza y cola pero no cuerpo? (Una moneda)
wild-roles,,What building has the most stories? (The library),Quel bâtiment a le plus d'histoires? (La bibliothèque),¿Qué edificio tiene más historias? (La biblioteca)
wild-roles,,What can travel around the world while staying in a corner? (A stamp),Qu'est-ce qui peut voyager autour du monde tout en restant dans un coin? (Un timbre),¿Qué puede viajar alrededor del mundo mientras se queda en una esquina? (Un sello)
wild-roles,,What has many teeth but cannot bite? (A comb),Qu'est-ce qui a beaucoup de dents mais ne peut pas mordre? (Un peigne),¿Qué tiene muchos dientes pero no puede morder? (Un peine)
wild-roles,,What runs but never walks? (Water),Qu'est-ce qui court mais ne marche jamais? (L'eau),¿Qué corre pero nunca camina? (El agua)
wild-roles,,What has one eye but cannot see? (A needle),Qu'est-ce qui a un œil mais ne peut pas voir? (Une aiguille),¿Qué tiene un ojo pero no puede ver? (Una aguja)
wild-roles,,What can you hold in your left hand but not in your right? (Your right elbow),Que peux-tu tenir dans ta main gauche mais pas dans ta droite? (Ton coude droit),¿Qué puedes sostener en tu mano izquierda pero no en la derecha? (Tu codo derecho)
wild-roles,,What grows when it eats but dies when it drinks? (Fire),Qu'est-ce qui grandit quand il mange mais meurt quand il boit? (Le feu),¿Qué crece cuando come pero muere cuando bebe? (El fuego)
wild-roles,,What has hands but cannot wave? (A clock),Qu'est-ce qui a des mains mais ne peut pas faire coucou? (Une horloge),¿Qué tiene manecillas pero no puede saludar? (Un reloj)
wild-roles,,What can fill a room without taking up any space? (Light),Qu'est-ce qui peut remplir une pièce sans prendre de place? (La lumière),¿Qué puede llenar una habitación sin ocupar espacio? (La luz)
wild-roles,,The more you take the more you leave behind. What am I? (Footsteps),Plus tu en prends plus tu en laisses. Que suis-je? (Des pas),Cuanto más tomas más dejas atrás. ¿Qué soy? (Huellas)
wild-roles,,What goes up but never comes down? (Your age),Qu'est-ce qui monte mais ne redescend jamais? (Ton âge),¿Qué sube pero nunca baja? (Tu edad)
wild-roles,,What begins with T ends with T and has T in it? (A teapot),Qu'est-ce qui commence par T finit par T et contient du T? (Une théière),¿Qué empieza con T termina con T y tiene T dentro? (Una tetera)
wild-roles,,What has four legs but cannot walk? (A table),Qu'est-ce qui a quatre pattes mais ne peut pas marcher? (Une table),¿Qué tiene cuatro patas pero no puede caminar? (Una mesa)
wild-roles,,What can you break even if you never touch it? (A promise),Que peux-tu briser même si tu ne le touches jamais? (Une promesse),¿Qué puedes romper incluso si nunca lo tocas? (Una promesa)
wild-roles,,What is always in front of you but cannot be seen? (The future),Qu'est-ce qui est toujours devant toi mais ne peut pas être vu? (L'avenir),¿Qué está siempre frente a ti pero no puede ser visto? (El futuro)
wild-roles,,What is full of holes but still holds water? (A sponge),Qu'est-ce qui est plein de trous mais retient encore l'eau? (Une éponge),¿Qué está lleno de agujeros pero aún retiene agua? (Una esponja)
funny-face-factory,,Name a time you felt really proud,Nomme un moment où tu t'es senti vraiment fier,Nombra una vez que te sentiste realmente orgulloso
funny-face-factory,,What makes you feel safe?,Qu'est-ce qui te fait sentir en sécurité?,¿Qué te hace sentir seguro?
funny-face-factory,,Draw how you are feeling right now,Dessine comment tu te sens en ce moment,Dibuja cómo te sientes ahora mismo
funny-face-factory,,What is something that made you smile today?,Qu'est-ce qui t'a fait sourire aujourd'hui?,¿Qué te hizo sonreír hoy?
funny-face-factory,,If your feeling were a color what color would it be?,Si ton sentiment était une couleur de quelle couleur serait-il?,Si tu sentimiento fuera un color ¿de qué color sería?
funny-face-factory,,What do you do when you feel scared?,Que fais-tu quand tu as peur?,¿Qué haces cuando tienes miedo?
funny-face-factory,,Tell me about a time you helped someone,Raconte-moi une fois où tu as aidé quelqu'un,Cuéntame sobre una vez que ayudaste a alguien
funny-face-factory,,What is the kindest thing someone has done for you?,Quelle est la chose la plus gentille que quelqu'un ait faite pour toi?,¿Cuál es la cosa más amable que alguien ha hecho por ti?
funny-face-factory,,How do you show love to your family?,Comment montres-tu l'amour à ta famille?,¿Cómo demuestras amor a tu familia?
funny-face-factory,,What does happiness feel like in your body?,À quoi ressemble le bonheur dans ton corps?,¿Cómo se siente la felicidad en tu cuerpo?
funny-face-factory,,What makes you feel frustrated and how do you handle it?,Qu'est-ce qui te frustre et comment gères-tu cela?,¿Qué te frustra y cómo lo manejas?
funny-face-factory,,Describe a moment when you felt really loved,Décris un moment où tu t'es senti vraiment aimé,Describe un momento en que te sentiste realmente amado
funny-face-factory,,What is a worry you have and can we shrink it together?,Qu'est-ce qui t'inquiète et pouvons-nous le réduire ensemble?,¿Qué preocupación tienes y podemos encogerla juntos?
funny-face-factory,,Who is someone you look up to and why?,Qui est quelqu'un que tu admires et pourquoi?,¿Quién es alguien a quien admiras y por qué?
funny-face-factory,,What sound calms you down?,Quel son te calme?,¿Qué sonido te calma?
funny-face-factory,,If your feelings could talk what would they say right now?,Si tes sentiments pouvaient parler que diraient-ils en ce moment?,Si tus sentimientos pudieran hablar ¿qué dirían ahora mismo?
funny-face-factory,,What is the bravest thing you have ever done?,Quelle est la chose la plus courageuse que tu aies jamais faite?,¿Cuál es la cosa más valiente que has hecho?
funny-face-factory,,How do you know when someone loves you?,Comment sais-tu quand quelqu'un t'aime?,¿Cómo sabes cuando alguien te ama?
funny-face-factory,,Finish this sentence: I feel happiest when...,Termine cette phrase: Je suis le plus heureux quand...,Termina esta frase: Me siento más feliz cuando...
funny-face-factory,,What does friendship mean to you?,Que signifie l'amitié pour toi?,¿Qué significa la amistad para ti?
lip-sync-legends,,Stomp your feet like a giant,Piétine comme un géant,Pisa fuerte como un gigante
lip-sync-legends,,Flap your arms like a bird,Bat(tre) des bras comme un oiseau,Aletea como un pájaro
lip-sync-legends,,Roll your shoulders in big circles,Roule tes épaules en faisant de grands cercles,Gira los hombros en círculos grandes
lip-sync-legends,,Shake your whole body for 10 seconds,Secoue tout ton corps pendant 10 secondes,Sacude todo tu cuerpo durante 10 segundos
lip-sync-legends,,Waddle like a duck,Marche comme un canard,Camina como un pato
lip-sync-legends,,Reach up high like you are grabbing a star,Tends les bras vers le haut comme pour attraper une étoile,Estírate hacia arriba como si agarraras una estrella
lip-sync-legends,,Crawl through an imaginary tunnel,Traverse un tunnel imaginaire en rampant,Atraviesa un túnel imaginario gateando
lip-sync-legends,,Jump like a frog across the room,Saute comme une grenouille à travers la pièce,Salta como una rana por la habitación
lip-sync-legends,,Spin slowly like a falling leaf,Tourne lentement comme une feuille qui tombe,Gira lentamente como una hoja que cae
lip-sync-legends,,March like you are in a parade,Marche comme si tu étais dans un défilé,Marcha como si estuvieras en un desfile
lip-sync-legends,,Stretch your arms and legs like a waking cat,Étire tes bras et tes jambes comme un chat qui se réveille,Estira tus brazos y piernas como un gato que se despierta
lip-sync-legends,,Tiptoe as quietly as you can,Marche sur la pointe des pieds aussi silencieusement que possible,Camina de puntillas lo más silenciosamente posible
lip-sync-legends,,Pretend to climb a very tall ladder,Fais comme si tu grimpais à une très grande échelle,Imagina que trepas una escalera muy alta
lip-sync-legends,,Gallop like a horse around the room,Galope comme un cheval autour de la pièce,Galopa como un caballo alrededor de la habitación
lip-sync-legends,,Roll your head gently from side to side,Roule doucement ta tête d'un côté à l'autre,Mueve suavemente la cabeza de un lado a otro
lip-sync-legends,,Dance like no one is watching,Danse comme si personne ne regardait,Baila como si nadie estuviera mirando
lip-sync-legends,,Freeze in a silly pose and hold it for 5 seconds,Figé dans une pose idiote et tiens-la 5 secondes,Inmovilízate en una pose tonta y mantenla por 5 segundos
lip-sync-legends,,Swim through the air like you are in a pool,Nage dans l'air comme si tu étais dans une piscine,Nada en el aire como si estuvieras en una piscina
lip-sync-legends,,Move like your favorite animal,Bouge comme ton animal préféré,Muévete como tu animal favorito
lip-sync-legends,,Do a slow-motion happy dance,Fais une danse de la joie au ralenti,Haz un baile feliz en cámara lenta
highway-hijinks,,Make the loudest roar you can,Fais le rugissement le plus fort possible,Haz el rugido más fuerte que puedas
highway-hijinks,,Whistle a tune you make up yourself,Siffle un air que tu inventes,Siliba una melodía que inventes tú mismo
highway-hijinks,,Imitate a car engine starting,Imit(e) le bruit d'un moteur de voiture qui démarre,Imita el motor de un coche arrancando
highway-hijinks,,Make sounds like it is raining,Fais des bruits comme s'il pleuvait,Haz sonidos como si estuviera lloviendo
highway-hijinks,,Buzz like a bee near a flower,Bourdonne comme une abeille près d'une fleur,Zumba como una abeja cerca de una flor
highway-hijinks,,Imitate a squeaky door,Imit(e) une porte qui grince,Imita una puerta que chirría
highway-hijinks,,Make the sound of a spaceship taking off,Fais le bruit d'un vaisseau spatial qui décolle,Haz el sonido de una nave espacial despegando
highway-hijinks,,Click your tongue like a horse,Claque ta langue comme un cheval,Chasquea la lengua como un caballo
highway-hijinks,,Hum a lullaby and pass it to the next person,Chanton(ne) une berceuse et passe-la à la personne suivante,Entona una canción de cuna y pásala a la siguiente persona
highway-hijinks,,Make popping sounds with your cheeks,Fais des bruits de claquement avec tes joues,Haz sonidos de pop con tus mejillas
highway-hijinks,,Copy the sound of a cat drinking water,Imit(e) le bruit d'un chat qui boit de l'eau,Imita el sonido de un gato bebiendo agua
highway-hijinks,,Growl like a bear then roar like a lion,Grogne comme un ours puis rugis comme un lion,Gruñe como un oso luego ruge como un león
highway-hijinks,,Make the sound of footsteps in crunchy snow,Fais le bruit de pas dans la neige craquante,Haz el sonido de pasos en la nieve crujiente
highway-hijinks,,Imitate a baby laughing,Imit(e) le rire d'un bébé,Imita la risa de un bebé
highway-hijinks,,Blow air through your lips to make a horse sound,Souffle entre tes lèvres pour faire le bruit d'un cheval,Sopla a través de tus labios para hacer el sonido de un caballo
highway-hijinks,,Moo like a cow in different tones,Meugle comme une vache sur différents tons,Muge como una vaca en diferentes tonos
highway-hijinks,,Make a sound like a balloon deflating,Fais le bruit d'un ballon qui se dégonfle,Haz el sonido de un globo desinflándose
highway-hijinks,,Imitate the wind blowing through trees,Imit(e) le vent qui souffle dans les arbres,Imita el viento soplando entre los árboles
highway-hijinks,,Create a beatbox pattern with your mouth,Crée un rythme beatbox avec ta bouche,Crea un ritmo beatbox con tu boca
highway-hijinks,,Make a sound that represents the color blue,Fais un son qui représente la couleur bleue,Haz un sonido que represente el color azul
doodle-dash,,What was the best part of your day?,Quelle a été la meilleure partie de ta journée?,¿Cuál fue la mejor parte de tu día?
doodle-dash,,If you could dream about anything tonight what would it be?,Si tu pouvais rêver de n'importe quoi cette nuit de quoi rêverais-tu?,Si pudieras soñar con cualquier cosa esta noche ¿qué sería?
doodle-dash,,Describe your perfect cozy place,Décris ton endroit douillet parfait,Describe tu lugar acogedor perfecto
doodle-dash,,What made you feel grateful today?,Qu'est-ce qui t'a rendu reconnaissant aujourd'hui?,¿Qué te hizo sentir agradecido hoy?
doodle-dash,,If your bed were a cloud where would it float to?,Si ton lit était un nuage où flotterait-il?,Si tu cama fuera una nube ¿hacia dónde flotaría?
doodle-dash,,Tell me three good things that happened today,Raconte-moi trois bonnes choses qui sont arrivées aujourd'hui,Cuéntame tres cosas buenas que pasaron hoy
doodle-dash,,What superpower would help you fall asleep?,Quel super-pouvoir t'aiderait à t'endormir?,¿Qué superpoder te ayudaría a dormirte?
doodle-dash,,If stars could speak what would they whisper?,Si les étoiles pouvaient parler que chuchoteraient-elles?,Si las estrellas pudieran hablar ¿qué susurrarían?
doodle-dash,,Describe a peaceful place in your imagination,Décris un endroit paisible dans ton imagination,Describe un lugar tranquilo en tu imaginación
doodle-dash,,What is something nice you can say about yourself?,Qu'est-ce que tu peux dire de gentil sur toi-même?,¿Qué cosa agradable puedes decir sobre ti mismo?
doodle-dash,,If you had a magic blanket when would you use it?,Si tu avais une couverture magique quand l'utiliserais-tu?,Si tuvieras una manta mágica ¿cuándo la usarías?
doodle-dash,,What animal would be the best bedtime buddy?,Quel animal serait le meilleur compagnon de lit?,¿Qué animal sería el mejor compañero para dormir?
doodle-dash,,Count your blessings instead of sheep,Compte tes bénédictions au lieu de compter les moutons,Cuenta tus bendiciones en lugar de ovejas
doodle-dash,,What is a question you have about the world?,Quelle question te poses-tu sur le monde?,¿Qué pregunta tienes sobre el mundo?
doodle-dash,,Imagine a gentle wave washing away your worries,Imagine une douce vague emportant tes soucis,Imagina una ola suave que se lleva tus preocupaciones
doodle-dash,,What kind of dream is the most fun?,Quel genre de rêve est le plus amusant?,¿Qué tipo de sueño es el más divertido?
doodle-dash,,Tell a one-sentence bedtime story,Raconte une histoire du soir en une phrase,Cuenta una historia para dormir en una oración
doodle-dash,,What color is peace and why?,De quelle couleur est la paix et pourquoi?,¿De qué color es la paz y por qué?
doodle-dash,,If you could thank the moon what would you say?,Si tu pouvais remercier la lune que dirais-tu?,Si pudieras agradecer a la luna ¿qué dirías?
doodle-dash,,Take three deep breaths together,Prenez trois grandes respirations ensemble,Tomen tres respiraciones profundas juntos
"""

STORY_SEEDS_CSV = """genre_slug,text_en,text_fr,text_es
tale-twisters,A mysterious door appears in your backyard. Where does it lead?,Une porte mystérieuse apparaît dans ton jardin. Où mène-t-elle?,Una puerta misteriosa aparece en tu jardín. ¿A dónde lleva?
tale-twisters,You find a message in a bottle. What does it say?,Tu trouves un message dans une bouteille. Que dit-il?,Encuentras un mensaje en una botella. ¿Qué dice?
tale-twisters,A tiny dragon moves into your garage. What happens next?,Un petit dragon emménage dans ton garage. Que se passe-t-il ensuite?,Un pequeño dragón se muda a tu garaje. ¿Qué sucede después?
tale-twisters,Your shadow starts moving on its own. Where does it go?,Ton ombre commence à bouger toute seule. Où va-t-elle?,Tu sombra comienza a moverse sola. ¿A dónde va?
tale-twisters,You discover a hidden room in your house. What is inside?,Tu découvres une pièce cachée dans ta maison. Qu'y a-t-il à l'intérieur?,Descubres una habitación escondida en tu casa. ¿Qué hay dentro?
tale-twisters,A friendly alien lands in your school playground. What happens?,Un extraterrestre amical atterrit dans la cour de ton école. Que se passe-t-il?,Un alienígena amigable aterriza en el patio de tu escuela. ¿Qué pasa?
tale-twisters,You wake up and can talk to animals. What do you ask first?,Tu te réveilles et tu peux parler aux animaux. Que demandes-tu d'abord?,Te despiertas y puedes hablar con los animales. ¿Qué preguntas primero?
tale-twisters,A magical seed grows into something amazing overnight. What?,Une graine magique donne quelque chose d'incroyable du jour au lendemain. Quoi?,Una semilla mágica crece y se convierte en algo increíble durante la noche. ¿Qué?
tale-twisters,You find a pair of glasses that let you see invisible things. What do you see?,Tu trouves des lunettes qui te permettent de voir les choses invisibles. Que vois-tu?,Encuentras unos lentes que te permiten ver cosas invisibles. ¿Qué ves?
tale-twisters,Time freezes for everyone except you. What do you do?,Le temps s'arrête pour tout le monde sauf toi. Que fais-tu?,El tiempo se congela para todos excepto para ti. ¿Qué haces?
tale-twisters,You build a machine that lets you visit any storybook world. Which one do you choose?,Tu construis une machine qui te permet de visiter n'importe quel monde de livre d'histoires. Lequel choisis-tu?,Construyes una máquina que te permite visitar cualquier mundo de cuentos. ¿Cuál eliges?
tale-twisters,The moon sends you a letter. What does it say?,La lune t'envoie une lettre. Que dit-elle?,La luna te envía una carta. ¿Qué dice?
tale-twisters,You become the captain of a pirate ship. Where do you sail?,Tu deviens le capitaine d'un bateau pirate. Où navigues-tu?,Te conviertes en el capitán de un barco pirata. ¿A dónde navegas?
tale-twisters,Paintings in a museum come to life at night. What do they do?,Les tableaux d'un musée prennent vie la nuit. Que font-ils?,Las pinturas de un museo cobran vida por la noche. ¿Qué hacen?
tale-twisters,You find a compass that points to the nearest adventure. Where does it lead?,Tu trouves une boussole qui pointe vers l'aventure la plus proche. Où mène-t-elle?,Encuentras una brújula que apunta hacia la aventura más cercana. ¿A dónde lleva?
"""

class Command(BaseCommand):
    help = 'Seed the database with genres and prompts'

    def handle(self, *args, **options):
        self.stdout.write('Seeding genres...')
        genre_map = {}
        for g in GENRES:
            genre, created = Genre.objects.get_or_create(
                slug=g['slug'],
                defaults={'name': g['name'], 'icon': g['icon'], 'tagline': g['tagline'], 'game_module': g['game_module']},
            )
            if created:
                self.stdout.write(f'  Created genre: {genre.name}')
            else:
                genre.name = g['name']
                genre.icon = g['icon']
                genre.tagline = g['tagline']
                genre.game_module = g['game_module']
                genre.save()
            genre_map[g['slug']] = genre

        self.stdout.write('Seeding prompts...')
        reader = csv.DictReader(PROMPTS_CSV.strip().splitlines())
        count = 0
        for row in reader:
            genre_slug = row['genre_slug'].strip()
            category = row['category'].strip() if row['category'].strip() else None
            text_en = row['text_en'].strip()
            text_fr = row['text_fr'].strip()
            text_es = row['text_es'].strip()
            genre = genre_map.get(genre_slug)
            if not genre:
                self.stdout.write(f'  Skipping unknown genre: {genre_slug}')
                continue
            Prompt.objects.get_or_create(
                genre=genre,
                text_en=text_en,
                defaults={
                    'category': category,
                    'text_fr': text_fr,
                    'text_es': text_es,
                },
            )
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Done! {count} prompts seeded.'))

        self.stdout.write('Seeding story seeds...')
        seed_count = 0
        for row in csv.DictReader(STORY_SEEDS_CSV.strip().splitlines()):
            genre_slug = row['genre_slug'].strip()
            text_en = row['text_en'].strip()
            text_fr = row['text_fr'].strip()
            text_es = row['text_es'].strip()
            genre = genre_map.get(genre_slug)
            if not genre:
                self.stdout.write(f'  Skipping unknown genre: {genre_slug}')
                continue
            StorySeed.objects.get_or_create(
                genre=genre,
                text_en=text_en,
                defaults={'text_fr': text_fr, 'text_es': text_es},
            )
            seed_count += 1
        self.stdout.write(self.style.SUCCESS(f'Done! {seed_count} story seeds seeded.'))

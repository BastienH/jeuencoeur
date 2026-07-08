# Jeu en coeur – Enhanced MVP Requirement Sheet (v2.0)

**Version:** 2.0  
**Date:** 2026-07-07  
**Status:** Approved for Development  

---

## 1. Global i18n Overlay (CORE – Applied to ALL modules)

- **Static UI:** Every button, timer label, category name, and error message must be fully translated into **English (EN), French (FR), and Spanish (ES)**.
- **Dynamic Prompts:** All new `text_en`, `text_fr`, and `text_es` fields are **optional** in the database. 
- **Text-to-Speech (TTS):** The `SpeechSynthesis` API must select the voice corresponding to the app's active language (e.g., `fr-FR` voice for French prompts, `es-ES` for Spanish).
- **Date/Time/Durations:** Use Django's `{% localize %}` and `l10n` filters to display numbers, times, and durations in the user's locale format.
- **Language Persistence:** The chosen language must be stored in a cookie or `localStorage` and persist across sessions and device rotations.

---

## 2. Enhanced Data Models (Django Backend)

### Core Models

```python
class Genre(models.Model):
    name = models.CharField(max_length=50)      # e.g., "Little Moments"
    slug = models.SlugField(unique=True)        # e.g., "little-moments"
    icon = models.CharField(max_length=10)      # Emoji string (e.g., "😂")

class Prompt(models.Model):
    # Relationships
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='prompts')
    
    # Metadata for filtering
    category = models.CharField(max_length=50, db_index=True)   # e.g., "Silly", "Deep", "Calm"
    age_group = models.CharField(
        max_length=20,
        choices=[('toddler', 'Toddler'), ('prek', 'Pre-K'), ('elem', 'Elementary')],
        blank=True
    )
    energy_level = models.CharField(
        max_length=10,
        choices=[('calm', 'Calm'), ('wild', 'Wild')],
        blank=True
    )
    
    # --- i18n Core Text (MANDATORY) ---
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    
    # --- Combinatorial fields for "You Are..." and "Doodle" (optional per prompt) ---
    subject_en = models.CharField(max_length=100, blank=True)
    subject_fr = models.CharField(max_length=100, blank=True)
    subject_es = models.CharField(max_length=100, blank=True)
    
    setting_en = models.CharField(max_length=100, blank=True)
    setting_fr = models.CharField(max_length=100, blank=True)
    setting_es = models.CharField(max_length=100, blank=True)
    
    action_en = models.CharField(max_length=100, blank=True)
    action_fr = models.CharField(max_length=100, blank=True)
    action_es = models.CharField(max_length=100, blank=True)
    
    # --- Helpers ---
    def get_text(self, lang):
        """Return primary translation; fallback to English if missing."""
        return getattr(self, f'text_{lang}', self.text_en) or self.text_en

    def get_subject(self, lang):
        return getattr(self, f'subject_{lang}', self.subject_en) or self.subject_en
    
    def get_setting(self, lang):
        return getattr(self, f'setting_{lang}', self.setting_en) or self.setting_en
    
    def get_action(self, lang):
        return getattr(self, f'action_{lang}', self.action_en) or self.action_en
        
        

       Global Technical Considerations (Backend & Infrastructure)

    Content Management System (CMS): An admin panel for us to continuously upload new prompts, questions, sound effects, and story seeds without pushing app updates.

    User Profiles: Local storage (or optional cloud sync) to save audio stories and favorite game settings.

    Analytics SDK: To track which games are abandoned, which prompts get the most "rerolls", and engagement time to optimize future content.

Game Module 1: "Little Moments for Big Laughs" - The Randomizer

Goal: Deliver a rapid-fire, 10-second challenge with zero decision fatigue for parents.

    Content Database (JSON): A library of 500+ "micro-challenges" (e.g., "Waddle like a penguin", "Speak in a pirate accent"). Tagged by age-group (Toddler, Pre-K, Elementary) and energy level (Calm, Wild).

    The "One-Tap" Engine: The main screen features one large, prominent button. Tapping it fetches a random prompt.

    Shake-to-Refresh (Accelerometer): Integrating the device's gyroscope so that shaking the phone instantly skips to a new prompt without looking at the screen.

    Visual Countdown Timer: A large, circular progress bar visually showing the 20-second limit for the challenge, creating lighthearted urgency.

    Text-to-Speech (TTS) Auditory Mode: A toggleable setting that reads the prompt aloud using a playful, cartoonish voice, accommodating non-readers.

    Haptic Feedback: A subtle vibration to signify the start and end of the challenge.

Game Module 2: "Would You Rather" - The Conversationalist

Goal: Foster conversation. The app is a prop, not the main focus.

    Curated Question Engine: 200+ questions, sorted by "Silly", "Deep", and "Food" categories.

    Reroll Function: An "Go next" button that instantly fetches a new question without resetting the app state.

    Voice-Changer Read-Aloud: Integrated text-to-speech audio player with three distinct voice filters: Deep/Scary, Helium/High-Pitched, and Robot, to make reading prompts hilarious for the kids.

    Voting System (Optional): A prominent white "Vote" button on the left/right of the screen. Tap to record your choice, and the app briefly displays a playful animation (e.g., "Team Pizza!" vs "Team Tacos!") to encourage debate.

Game Module 3: "Plot Twist!" - The Story Architect

Goal: Foster collaborative storytelling and capture spoken family memories as digital keepsakes.

    Story Front-End: A "Mad-Libs" style screen showing a growing text story.

    The "Twist!" Button: A large button on the side that triggers an API call to a pre-set list of chaotic interruptions (e.g., "Suddenly, a giant pickle..." / "But wait, grandma is a spy!"), injecting randomness into the plot.

    Voice Recorder Module (Native API): Requires microphone permissions. Automatically starts a background audio recording the moment the session starts.

    Audio Archiving System: When the story ends, a "Save & Share" button compresses the audio file into an MP4, attaches the written story as metadata, and saves it to a local "Storytime Vault" gallery that families can re-listen to on holidays. 
        

        Game Module 4: "Who Can Sound Like" - The Noise Harness

Goal: Redirect chaotic energy into a controlled, loud, and structured game.

    Audio FX Library: A robust collection of high-fidelity sound effects (mooing, balloon popping, sirens, roaring dinosaurs).

    Decibel/Volume Meter UI: A real-time waveform visualizer on the screen that rises and falls based on the device microphone input.

    "Fill the Bar" Mechanic: The app prompts: "Imitate this sound!" The goal is for the child to shout/mimic loud enough to fill a "Volume Meter" to 100%.

    Dynamic Response Logic: When the meter hits 100%, instead of a harsh noise, the app triggers a gentle, sliding "Shhhh..." sound effect and smoothly animates the volume meter deflating, naturally guiding the child to calm down for the next round.

Game Module 5: "You Are..." - The Physical Chaos Maker

Goal: Transform wild energy into structured, physical improvisation.

    Triple-Spin Wheel: A visual slot-machine UI that randomizes three elements: Character, Setting, and Activity (e.g., A clumsy ninja + in a bakery + trying to tie their shoes).

    Countdown Timer: A 30-second circular timer that begins once the prompt is revealed.

    Active Judging & Scoring: A non-competitive "Reaction" panel at the bottom where the parent or sibling taps an emoji (Laughing Star, Heart, Clapping Hands) to rate the performance without using words.

    Turn-Switching State: After the timer ends, a "Switch Roles" button automatically clears the screen and resets the timer for the next player.

Game Module 6: "Make This Face" - The Quiet Funster

Goal: Enable play in quiet public spaces (restaurants, waiting rooms) through silent expressions.

    Prompt Database: Visual and text prompts for highly specific, absurd facial expressions (e.g., "A dinosaur who bit a lemon," "A robot smelling burnt toast").

    Selfie Camera Integration: Automatically opens the front-facing camera (with a subtle, fun framing border to guide the child's face into view).

    Surprise AR/Filter Engine: When the child presses the "Snap!" button, the app doesn't just take the photo—it applies a random, hilarious augmented reality filter (mustache, rainbow barf, floppy ears, or a goofy hat) to the final photo.

    Comparison Gallery: Shows the filter-applied photo alongside the original prompt. Allows saving to the camera roll for a family "Wall of Silly Faces."

Game Module 7: "Act Out That Sound" - The Silent Dubbing Master

Goal: A spin on silent movies and lip-syncing.

    Sound Deck: Random selection of 50 abstract or situational sound effects (squeaky shoe, haunted door, alien translation).

    "3...2...1... ACTION" Timer: A 3-second countdown plays on screen for the "sound" to start.

    Reverse Mode Logic: A distinct toggle. When "Reverse Mode" is on, the parent acts out a scenario silently while the app provides 4 multiple-choice sound options. The child must tap the correct sound effect on the screen that matches the parent's mime.

    Haptic Feedback for Guesses: The screen lightly buzzes if the child picks the wrong sound, and buzzes strongly + triggers a confetti animation if they get it right.

Game Module 8: "Are We There Yet" - The Road Trip Companion

Goal: Gamify the physical environment to prevent backseat meltdowns while minimizing driving distraction.

    GPS/Location Services Integration: Tracks the car's route. Triggers "Spontaneous Events" based on geolocation (e.g., "Quick! Look out your window! How many blue cars do you see in the next 30 seconds?").

    "Boredom Buster" Button: A massive, low-latency button on the screen. Tapping it instantly draws from a separate list of no-prop car games ("I Spy", "License Plate Game", "20 Questions") and displays the core rule on screen.

    Parent-Centric UX: In "Driving Mode," the screen interface is ultra-high-contrast with large text to be readable in sunlight. Most interactions are based on single-taps rather than swipes, so the parent's eyes stay on the road.

    Tracking Progress: A visual "Miles to Destination" progress bar that can be manually set at the start of a trip.

Game Module 9: "What Should We Doodle?" - The Artist's Assistant

Goal: Spark collaborative creativity with absurd prompts.

    Random Prompt Generator: A mixing database of Subject + Emotion + Attire/Accessory (e.g., An oblivious squirrel + wearing pink roller skates).

    Digital Canvas (In-App): A basic finger-drawing canvas with 3 brush sizes and a color palette. Allows families to draw the prompt directly on the tablet/phone if they don't have paper handy.

    PDF/AirPrint Generator: A clean "Print" button. It renders the prompt as a printable PDF and splits the page into 4 blank squares, allowing the entire family to print it on paper, doodle simultaneously, and compare their physical drawings in the real world.

    "Comparison View": If they draw digitally, a split-screen button allows two family members' drawings to be overlaid side-by-side to see different interpretations.

Supplementary Feature: "Printable Card Decks"

    PDF Export Engine: Transforms the internal game prompt databases into beautifully formatted, printable PDFs with cut-lines.

    Deck Selection: Allows parents to choose which game's deck they want to print (e.g., only print the "Would You Rather" deck) so they can take a physical deck on a camping trip if they prefer zero-phone play.

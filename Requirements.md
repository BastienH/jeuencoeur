Here is the **prioritized MVP requirement sheet**—focused strictly on validating the core concept: *a browsable hub of game genres that instantly delivers random prompts.*

We’ll use a **MoSCoW** framework (Must, Should, Could, Won’t) to rank every feature. Monetization, user accounts, PDFs, and advanced gamification are pushed to later phases.

---

## MVP Priority Matrix

| Priority | Category | Included Features |
| :--- | :--- | :--- |
| **🟢 MUST** | **Core MVP** | Working Hub (9 genres), User can select language (French, English, Spanish to start), Random Prompt generator per genre, Basic UI/UX, Django Admin for content seeding in multiple languages and has mass import option. |
| **🟡 SHOULD** | **Phase 1.5 (Beta)** | Favorites/Bookmarks (local storage only), Basic PWA manifest (installable), Category filtering (for *Little Moments*). |
| **🟠 COULD** | **Phase 2 (Polishing)** | User accounts & cloud sync, Offline caching of prompts, Shuffle animation, Detailed stats counter. |
| **🔴 WON'T (now)** | **Future** | Payment/Monetization, PDF generation, Built-in sketchpad, Voting/Polling, Audio/text-to-speech, Email/Social login. |

---

## Detailed MVP Functional Requirements (MUST HAVE)

### 1. The Hub (Landing Page)
- **Purpose:** A single, visually clean page that lists all 9 "game genres" (apps) as clickable cards/tiles.
- **Display per genre:**
  - Name (e.g., *Little Moments for Big Laughs*)
  - A simple emoji or icon (to reduce design overhead).
  - A short tagline (e.g., *Silly ideas for connecting*).
- **Navigation:** Clicking a tile navigates the user to that genre's dedicated prompt view (without a full page reload if using SPA, or via standard routing if using Django templates).
- **Language** selection, user can select between 3 languages to start with : English, french, Spanish

### 2. Genre-Specific Prompt View
- **Header:** Displays the genre name and a "Back to Hub" button.
- **Primary Action – "Give me a prompt":** A large, tappable button that fetches a **random** prompt from that specific genre's database.
- **Prompt Display:** A clean, highly readable card that shows the full prompt text.
- **Behaviour on load:** The very first time a user enters a genre, a random prompt should be displayed immediately (no empty state).
- **"Next Prompt" / Re-roll:** The same button re-fetches a new random prompt, replacing the current one.

### 3. Content Structure (Data Model)
- **Genres:** 9 fixed entries (you can seed them via Django fixtures).
- **Prompts:** Each prompt belongs to exactly **one** genre.
- **Minimum Content:** Seed at least **15–20 prompts per genre** for the MVP (enough to test variety).
- **Extra field for *Little Moments*:** This genre requires a `category` field (e.g., *Mealtime*, *Bedtime*) so we can later filter. For MVP, just store it; no filtering UI yet.

### 4. Backend Architecture (Python/Django)
- **Project Structure:** A single Django project with **one core `apps` app**. Do not create 9 separate Django apps. Instead, use a single `Prompt` model with a `genre` CharField or ForeignKey.
- **API (if using separate frontend) OR Server-Side Rendering:**
  - *Recommendation for MVP:* Use **Django Templates + minimal vanilla JavaScript** (or **HTMX**) for the simplest maintenance. This avoids setting up a separate Node.js build pipeline.
  - If you strongly prefer a frontend framework, use **Vue.js (CDN)** or **Alpine.js** – both are lightweight and can be embedded directly in Django templates without a complex Webpack setup.
- **Admin Panel:** Leverage Django's built-in Admin interface **as the CMS** for MVP. The admin should allow the product owner to:
  - Add/Edit/Delete prompts.
  - Assign prompts to genres.
  - (For *Little Moments*) Assign categories to prompts.
- **No Authentication:** For MVP, no login, no user accounts. Everyone sees the same prompts.

### 5. Frontend UI/UX (Mobile-First)
- **Responsive:** Must work flawlessly on a smartphone (portrait mode) and tablet.
- **Touch-friendly:** Buttons must be at least 44px tall.
- **Loading states:** A subtle loading spinner while fetching the prompt (even if instant).
- **No external dependencies:** Keep CSS light (e.g., Tailwind CDN or a simple custom CSS file).

---

## SHOULD HAVE (For Beta Testing – Phase 1.5)

Build these right after the MVP is live and you have initial user feedback:
- **Local Favorites:** A "❤️ Save" button that saves prompts to the browser's `localStorage` (no backend sync). A "Favorites" tab on the Hub to view saved ones.
- **Basic PWA Manifest:** Add a `manifest.json` and a Service Worker (just to cache the core assets) so users can "Add to Home Screen". This reinforces the "app" feeling.
- **Category filter for *Little Moments*:** A dropdown or pill buttons above the prompt to filter by category (e.g., *Bedtime*, *Car rides*).

---

## COULD HAVE (Phase 2 – Polishing)

- **User Accounts & Cloud Sync:** Login to save favorites across devices. (Add Django `User` model and JWT or session auth).
- **Offline Prompt Cache:** Store ~50 prompts per genre in IndexedDB so the app works without internet.
- **Smooth transitions:** Animated card flips or fades when fetching a new prompt.
- **Usage Counter:** "You've viewed 42 prompts today!"

---

## WON'T HAVE (Postponed indefinitely for now)

| Feature | Reason to postpone |
| :--- | :--- |
| **Monetization / Payment gateway** | You explicitly said this is not a priority. Validate the concept first. |
| **Printable PDF decks** | Complex rendering and download logic. Not needed for testing engagement. |
| **Built-in sketchpad / drawing tools** | Heavy frontend work. Users can use paper. |
| **Polling/Voting** | Adds backend complexity and real-time DB needs. |
| **Social login / Password reset** | Not needed without user accounts. |
| **Separate mobile apps (iOS/Android)** | PWA is sufficient for MVP. Native can come later. |

---

## Technical Implementation Blueprint (MVP)

| Layer | Choice | Rationale |
| :--- | :--- | :--- |
| **Backend** | Django 5.x + SQLite (or PostgreSQL if hosted) | Built-in admin, ORM, simple routing. SQLite is fine for seeding 180 prompts. |
| **Data Models** | `Genre` (name, slug, icon_emoji) <br> `Prompt` (text, genre_fk, category_nullable) | One model, one table. Filter by `genre__slug` in views. |
| **URLs** | `/` (Hub) <br> `/genre/<slug>/` (Prompt view) | Clean, RESTful, bookmarkable URLs. |
| **Frontend** | Django Templates + **Alpine.js** (or just plain `fetch()` API with a Django view returning JSON) | Alpine is 15kb and gives reactivity for buttons. Simpler: use a Django view that returns a `JsonResponse` and update the DOM with vanilla JS. |
| **Styling** | TailwindCSS via CDN | Utility-first, no CSS file to maintain, mobile-first out of the box. |
| **Deployment** | Single server (e.g., Render, PythonAnywhere, or a $5 VPS) | Cheap and easy. No Docker/K8s needed. |

---

## MVP User Stories (Acceptance Criteria)

| ID | User Story | Acceptance Criteria |
| :--- | :--- | :--- |
| **US-01** | As a parent, I want to open the landing page and see all 9 game options. | Hub renders 9 distinct tiles with icons and names. |
| **US-02** | As a parent, I want to tap a game tile and immediately see a prompt. | On click, page navigates to `/genre/big-laughs/`. A prompt card is visible on load. |
| **US-03** | As a parent, I want to get a new idea without going back to the hub. | Tapping the "Next" button replaces the prompt text with a new random one from the same genre. |
| **US-04** | As the content owner, I want to easily add new prompts. | Logging into `/admin/`, I can add a prompt, select its genre, and save. It appears in the app immediately. |
| **US-05** | As a user on my phone, I want the buttons to be easy to tap. | All interactive elements are >44px and spaced apart. |

---

## Development Roadmap (Suggested Sprint Plan)

| Sprint | Focus | Deliverable |
| :--- | :--- | :--- |
| **Sprint 1 (Week 1)** | Data models + Admin + Seed 9 genres + 20 prompts each. | Django project with populated DB. Admin works. |
| **Sprint 2 (Week 2)** | Hub page + Genre detail page + Random prompt logic + "Next" button. | Functional web app accessible via browser. |
| **Sprint 3 (Week 3)** | Mobile-first CSS polish, deploy to a public URL, share with 5–10 test parents. | Live MVP. Collect qualitative feedback (Do they use it? Do they laugh?). |
| **Post-MVP** | Based on feedback, implement **SHOULD HAVE** items (Favorites, PWA, Category filter). | Beta release for wider testing. |

---

This MVP strips away every distraction and focuses on **the core loop**: *Browse Genre → Read Prompt → Smile/Get Inspired → Next Prompt*. Build this, put it in front of parents within 3 weeks, and validate the concept before investing in the rest.

## Addendum: Internationalization (i18n) – French, English & Spanish

This addendum supersedes the previous prioritization by elevating **multi-language support to a CORE MVP requirement (MUST HAVE)**. The app must be fully functional in **English, French, and Spanish** from the very first release.

---

### 1. Updated MoSCoW Priority (i18n Impact)

| Priority | Category | Updated Inclusion |
| :--- | :--- | :--- |
| **🟢 MUST** | **Core MVP** | _Previous items_ **+** Full i18n support for EN, FR, ES: <br> • Language switcher <br> • Translated prompt content <br> • Translated UI strings (buttons, labels, navigation) <br> • Language-persistent session/cookie |
| **🟡 SHOULD** | **Phase 1.5** | Auto-detection of browser language on first visit (fallback to English). |
| **🟠 COULD** | **Phase 2** | Right-to-left (RTL) support (not needed for these languages). |
| **🔴 WON'T (now)** | **Future** | Machine-translation fallback for missing content (must be manually curated). |

---

### 2. Functional Requirements (i18n-Specific)

#### 2.1. Language Selection & Persistence
- **Language Switcher:** A visible, intuitive selector (e.g., flag icons or language codes: **EN / FR / ES**) must be present on the **Hub page** and **every genre detail page** (e.g., in the header or footer).
- **Persistence:** The selected language must be remembered across sessions using a **cookie** or **localStorage**. When a user returns, they see the app in their last chosen language.
- **Browser Detection (Nice-to-have for MVP but recommended):** On first visit, the app should read the browser's `Accept-Language` header and default to the closest match (EN, FR, or ES). If none match, fallback to **English**.

#### 2.2. User-Facing UI Translation (Static Strings)
All static interface elements must be translated into the three languages:
- **Hub:** "Jeu en coeur" / title, each genre's name and tagline.
- **Navigation:** "Back to Hub", "Give me a prompt", "Next", "Save" (if added later).
- **Placeholders / Empty states:** "No prompts found in this category".
- **Admin (optional but recommended):** Django admin labels can remain in English for the content manager, but the front-end must be fully localized.

#### 2.3. Prompt Content Translation (Dynamic Data)
- **Requirement:** Every single prompt stored in the database must have **three versions**: one in English, one in French, and one in Spanish.
- **Fallback logic:** If a prompt is missing a translation for the current language (e.g., a newly added prompt has only English), the app must **gracefully fallback to English** (or display a placeholder like `[Translation missing]`) – but the admin should be prevented from publishing a prompt without all three translations via admin validation.

#### 2.4. URL Structure (Optional but Recommended)
To enable bookmarking and sharing in different languages, use **URL language prefixes**:
- `/en/` → Hub in English
- `/fr/` → Hub in French
- `/es/` → Hub in Spanish
- Example: `/en/genre/big-laughs/` vs `/fr/genre/gros-rire/`

> **Note for MVP:** You may skip translated slugs (keep `big-laughs` for all languages) to reduce complexity, but the prefix (`/en/`, `/fr/`) must be present.

---

### 3. Data Model Adjustments

Replace the single `text` field with **three separate fields** for MVP simplicity:

```python
class Prompt(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    category = models.CharField(max_length=50, null=True, blank=True)  # for Little Moments
    # i18n fields:
    text_en = models.TextField()
    text_fr = models.TextField()
    text_es = models.TextField()
    
    def get_text(self, language):
        # Returns the appropriate translation or falls back to English
        return getattr(self, f'text_{language}', self.text_en)
```

**Alternative (more scalable):** Use `django-modeltranslation` package – but for MVP, three explicit fields are simpler to manage in the Django admin and easier to seed with CSV data.

---

### 4. Backend Implementation (Django)

- **Django's built-in i18n:** Activate `django.middleware.locale.LocaleMiddleware` and set `LANGUAGES = [('en', 'English'), ('fr', 'Français'), ('es', 'Español')]`.
- **Locale folder:** Create `.po` files for static UI translations. Use `{% trans %}` and `{% blocktrans %}` in templates.
- **Session/Cookie:** Use Django's `LANGUAGE_COOKIE_NAME` to persist the choice.
- **Admin validation:** Override the `Prompt` admin form to ensure that `text_en`, `text_fr`, and `text_es` are **all required** before saving – this guarantees content parity across languages.

---

### 5. Frontend Implementation

- **UI Text:** Use Django's `{% trans "Give me a prompt" %}` in templates. For client-side dynamic updates (if you use JavaScript to fetch new prompts), the static button labels must be rendered already translated by Django.
- **API / Fetch logic (if using AJAX):** When the frontend requests a new random prompt, it must send the current language as a parameter (e.g., `GET /api/prompt/?lang=fr`). The backend then returns the correct translation.
- **Language switcher behavior:** Changing the language must **refresh the page** (or re-fetch the current prompt in the new language) so all UI strings update. For an SPA approach, you would need a reactive i18n store – but for MVP simplicity, a full page reload on language change is acceptable.

---

### 6. Content Strategy for MVP

- **Seeding data:** Prepare a spreadsheet with **all prompts in 3 columns** (EN, FR, ES) before development. Use a Django management command (`python manage.py import_prompts`) to load this data.
- **Translation quality:** Do not rely on machine translation (Google Translate) for the MVP. The product owner must provide **curated, playful, culturally appropriate translations** – especially since humor and silliness do not translate well literally. Engage native speakers or use a service like DeepL with human review.
- **Minimum count:** Seed **at least 15 prompts per genre × 3 languages** (i.e., 15 EN + 15 FR + 15 ES per genre). That is 135 prompts per language, 405 total – still manageable for MVP.

---

### 7. Updated Acceptance Criteria (i18n User Stories)

| ID | User Story | Acceptance Criteria |
| :--- | :--- | :--- |
| **US-i18n-01** | As a French-speaking parent, I want to see the entire app in French. | Language switcher shows FR. Tapping it reloads the page with all UI labels and prompts in French. |
| **US-i18n-02** | As a Spanish-speaking parent, I want the app to remember my language preference. | After selecting ES, closing the browser, and reopening the app, the interface remains in Spanish. |
| **US-i18n-03** | As a bilingual parent, I want to switch languages instantly to practice with my kids. | Switching from EN to FR while viewing a prompt changes that prompt's text to French immediately (after page reload or dynamic fetch). |
| **US-i18n-04** | As the content admin, I want to ensure no prompt goes live without all three translations. | The Django admin interface marks `text_fr` and `text_es` as required fields alongside `text_en`. Saving is blocked if any are empty. |

---

### 8. Development Impact & Estimation

| Area | Additional Effort (vs. single-language MVP) |
| :--- | :--- |
| **Data model** | +2 extra fields per Prompt (trivial). |
| **Django setup** | +1 day for configuring `LocaleMiddleware`, creating `.po` files, and marking templates with `{% trans %}`. |
| **Admin** | +2 hours to customize the Prompt admin form with required validation. |
| **Content preparation** | **This is the biggest task** – the product owner must prepare translated prompt lists before development starts. Estimate 3–5 days for professional translation of ~200 prompts. |
| **Frontend** | +1 day to add the language switcher, handle URL prefixes, and implement language persistence. |
| **Testing** | +2 days for QA across all 3 languages (verify UI truncation, special characters like é/ñ, and proper encoding). |

---

### 9. Final Note on "Core"

By making i18n a **MUST HAVE**, you ensure that the MVP can be tested simultaneously with **English-speaking, French-speaking, and Spanish-speaking families** – a strategic move for a parenting app that targets diverse demographics. It also prevents a costly retrofitting later, as adding i18n to an existing codebase is significantly more complex than building it in from day one.

All other features (Favorites, PWA, Offline) remain **SHOULD/COULD** and can be added after initial validation. **Language support is non-negotiable and ships with v1.**

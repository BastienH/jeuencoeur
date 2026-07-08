from django.urls import path

from active_games import views as active_views
from creative_games import views as creative_views
from sound_games import views as sound_views

from . import views

urlpatterns = [
    path('', views.hub, name='hub'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('next-prompt/', views.next_prompt, name='next_prompt'),
    path('toggle-favorite/<int:prompt_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('analytics/track/', views.track_event, name='track_event'),
    path('print-decks/', views.print_deck_list, name='print_deck_list'),
    path('print-decks/<slug:game_module>/', views.print_deck_pdf, name='print_deck_pdf'),

    # Giggle Generators
    path('giggle-generators/', sound_views.giggle_play, name='giggle_generators_play'),
    path('giggle-generators/next/', sound_views.giggle_next, name='giggle_generators_next'),

    # Choice Chaos
    path('choice-chaos/', sound_views.choice_play, name='choice_chaos_play'),
    path('choice-chaos/reroll/', sound_views.choice_reroll, name='choice_chaos_reroll'),
    path('choice-chaos/vote/', sound_views.choice_vote, name='choice_chaos_vote'),

    # Tale Twisters
    path('tale-twisters/', creative_views.tale_play, name='tale_twisters_play'),
    path('tale-twisters/twist/', creative_views.tale_twist, name='tale_twisters_twist'),
    path('tale-twisters/start/', creative_views.tale_start, name='tale_twisters_start'),
    path('tale-twisters/pick-twist/', creative_views.tale_pick_twist, name='tale_twisters_pick_twist'),
    path('tale-twisters/pick-ending/', creative_views.tale_pick_ending, name='tale_twisters_pick_ending'),
    path('tale-twisters/state/', creative_views.tale_state, name='tale_twisters_state'),
    path('tale-twisters/save/', creative_views.tale_save, name='tale_twisters_save'),
    path('tale-twisters/claim-story/', creative_views.tale_claim_story, name='tale_twisters_claim_story'),
    path('tale-twisters/chest/', creative_views.tale_chest, name='tale_twisters_chest'),

    # Mimic Mayhem
    path('mimic-mayhem/', sound_views.mimic_play, name='mimic_mayhem_play'),
    path('mimic-mayhem/next/', sound_views.mimic_next, name='mimic_mayhem_next'),

    # Wild Roles
    path('wild-roles/', active_views.wild_play, name='wild_roles_play'),
    path('wild-roles/spin/', active_views.wild_spin, name='wild_roles_spin'),
    path('wild-roles/spin-character/', active_views.wild_spin_character, name='wild_roles_spin_character'),
    path('wild-roles/spin-setting/', active_views.wild_spin_setting, name='wild_roles_spin_setting'),
    path('wild-roles/spin-activity/', active_views.wild_spin_activity, name='wild_roles_spin_activity'),
    path('wild-roles/react/', active_views.wild_react, name='wild_roles_react'),

    # Funny Face Factory
    path('funny-face-factory/', creative_views.funny_face_play, name='funny_face_factory_play'),
    path('funny-face-factory/next/', creative_views.funny_face_next, name='funny_face_factory_next'),

    # Lip-Sync Legends
    path('lip-sync-legends/', sound_views.lip_sync_play, name='lip_sync_legends_play'),
    path('lip-sync-legends/next/', sound_views.lip_sync_next, name='lip_sync_legends_next'),

    # Highway Hijinks
    path('highway-hijinks/', active_views.highway_play, name='highway_hijinks_play'),
    path('highway-hijinks/boredom-buster/', active_views.highway_boredom_buster, name='highway_hijinks_boredom_buster'),
    path('highway-hijinks/start-trip/', active_views.highway_start_trip, name='highway_hijinks_start_trip'),
    path('highway-hijinks/next-game/', active_views.highway_next_game, name='highway_hijinks_next_game'),
    path('highway-hijinks/update-progress/', active_views.highway_update_progress, name='highway_hijinks_update_progress'),
    path('highway-hijinks/end-trip/', active_views.highway_end_trip, name='highway_hijinks_end_trip'),

    # Doodle Dash
    path('doodle-dash/', creative_views.doodle_play, name='doodle_dash_play'),
    path('doodle-dash/save/', creative_views.doodle_save, name='doodle_dash_save'),
    path('doodle-dash/gallery/', creative_views.doodle_gallery, name='doodle_dash_gallery'),

    # Generic fallback
    path('<slug:genre_slug>/', views.detail, name='detail'),
]

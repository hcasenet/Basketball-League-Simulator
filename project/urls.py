#Hinsley Casenet - U59220930
#project/urls.py - used to provide urls for visiting each of the pages in the application.

from django.urls import path
from . import views
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # home view
    path(r'', views.index, name='index'),

    ##league tabs
    path(r'create_league', CreateLeagueView.as_view(), name='create_league'), 
    path(r'leagues/', LeagueListView.as_view(), name='league_list'),
    path(r'league/<int:pk>/', LeagueDetailView.as_view(), name='league_detail'),
    path(r'league/<int:pk>/management/', LeagueManagementView.as_view(), name='league_management'),
    path(r'league/<int:pk>/management/stats/', LeagueStatsView.as_view(), name='league_stats'),
    path(r'league/<int:pk>/management/teams/', LeagueTeamsView.as_view(), name='league_teams'),
    path(r'league/<int:pk>/simulate/', SimulateLeagueView.as_view(), name='simulate_league'),
    path(r'league/<int:pk>/update/', LeagueUpdateView.as_view(), name='league_update'),
    path(r'league/<int:pk>/delete/', LeagueDeleteView.as_view(), name='league_delete'),

    ##team tabs
    path(r'league/<int:league_pk>/team/<int:pk>/', TeamDetailView.as_view(), name='team_detail'),
    path(r'league/<int:league_pk>/team/<int:pk>/update/', UpdateTeamView.as_view(), name='update_team'),
    path(r'league/<int:league_pk>/team/<int:pk>/roster/', TeamRosterView.as_view(), name='team_roster'),

    ##player tabs
    path(r'league/<int:league_pk>/team/<int:team_pk>/player/<int:pk>/', PlayerDetailView.as_view(), name='player_detail'),
    path(r'league/<int:league_pk>/team/<int:team_pk>/player/<int:pk>/update/', UpdatePlayerView.as_view(), name='update_player'),

    #authentication tabs
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='logged_out'), name="logout"),
    path('logged_out/', views.LoggedOutView.as_view(), name='logged_out'),
    path('create_user/', RegisterUserView.as_view(), name='create_user'), #new
]

#debugging step added in order to make sure media was properly loading
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

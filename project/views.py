#Hinsley Casenet - U59220930
#project/views.py - core functionality of the page, return to user requests

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, DeleteView, FormView
import random
from .models import *
from .forms import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse_lazy
from django.utils import timezone
import datetime

# Create your views here.

def index(request):
    """displays the home page for the application"""
    
    if request.user.is_authenticated:
        return redirect('league_list')  #redirect authenticated users to the league list page

    return render(request, 'project/index.html')


class LeagueUpdateView(LoginRequiredMixin, UpdateView):
    '''manages updating the league, makes usage of a form'''

    model = League
    form_class = UpdateLeagueForm
    template_name = 'project/update_league_form.html'
    success_url = reverse_lazy('league_list')

    def get_queryset(self):
        #only the user can update the league

        queryset = super().get_queryset()
        return queryset.filter(user_league=self.request.user)


class LeagueDeleteView(LoginRequiredMixin, DeleteView):
    '''manages deleting a league - redirects to a confirmation page'''

    model = League
    template_name = 'project/league_confirm_delete.html'
    success_url = reverse_lazy('league_list')

    def get_queryset(self):
        # Only allow the league owner to delete the league
        queryset = super().get_queryset()
        return queryset.filter(user_league=self.request.user)

from django.contrib import messages
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect

class CreateLeagueView(LoginRequiredMixin, CreateView):
    """manages league creation - randomly generates teams and players, uses simulateview
    to randomly generate games as well"""

    form_class = CreateLeagueForm
    template_name = "project/create_league_form.html"

    def form_valid(self, form):
        """handles the form submission to create a new League object tied to the current user"""

        form.instance.user_league = self.request.user  #association with logged-in user
        response = super().form_valid(form)

        #random generation method
        self.generate_teams_and_players(self.object)
        
        #simulation method
        self.simulate_games(self.object)

        #flash message on successful league creation
        messages.success(self.request, 'League successfully created!')

        return response

    def form_invalid(self, form):
        """handles invalid form submission and adds error messages"""

        #general error message
        messages.error(self.request, "There were errors in the form. Please check below.")

        #if form has non-field errors, add them to messages
        for error in form.non_field_errors():
            messages.error(self.request, error)

        #for each field with errors, display them as messages
        for field in form:
            for error in field.errors:
                messages.error(self.request, f"{field.label}: {error}")

        return self.render_to_response({'form': form})

    def simulate_games(self, league):
        """simulates games for the league after it is created - simulateview is the subroutine"""
        SimulateLeagueView().post(self.request, pk=league.pk)

    def generate_teams_and_players(self, league):
        """randomly generates teams and players for a league upon creation"""

        team_names = [
            "Hawks", "Fighters", "Giants", "Foxes", "Spinners", 
            "Lions", "Panthers", "Wolves", "Dragons", "Tide",
            "Dinos", "Eagles", "65ers", "Barons", "Newmans",
            "Wileys", "Blaze", "Tigers", "Kings", "Chuckers",
            "Ardrats", "Gladiators", "Rexes", "Brewers",
            "Brave", "Stars", "Racers", "Menaces", "Thieves",
            "Maimers", "Flight", "Muse", "Legends", "Glory"
        ]
        american_cities = [
            "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
            "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose",
            "Newark", "Boston", "New Orleans", "Las Vegas", "Honolulu", 
            "Detroit", "Anaheim", "Milwaukee", "Philadelphia", "Seattle",
            "Indianapolis", "San Francisco", "Austin", "Portland", 
            "Nashville", "El Paso", "Denver", "Fort Worth", "Jacksonville",
            "Charlotte", "Oklahoma City", "Washington", "D.C.",
            "Sacramento", "Baltimore", "Atlanta", "Memphis", "Orlando", "Miami"
        ]
        player_first_names = [
            "John", "Mikey", "Chris", "Jared", "Alex", "Arnold", "Robert", "Anthony", "Marko", "David",
            "Michael", "James", "Daniel", "Matthew", "Joseph", "Joshua", "Andrew", "Justin", "Kevin", "Ryan",
            "Jacob", "Ethan", "Tyler", "Brandon", "Nicholas", "Zachary", "Adam", "Nathan", "Eric", "Sean",
            "Cameron", "Aaron", "Kyle", "Jason", "Brian", "Logan", "Jeffrey", "Samuel", "Austin", "Jonathan",
            "Christian", "Gregory", "Patrick", "Peter", "Scott", "Lucas", "Dylan", "Paul", "Evan", "Trevor",
            "Steven", "Blake", "Shane", "Colin", "Bradley", "Mitchell", "Cody", "Hunter", "Jordan", "Spencer",
            "Luke", "Gavin", "Tyson", "Elijah", "Isaac", "Chase", "Vincent", "Marcus", "Tristan", "Grant",
            "Cole", "Dominic", "Brent", "Wesley", "Maxwell", "Jack", "Phillip", "Owen", "Damian", "Tanner"
        ]
        player_last_names = [
            "White", "Johnson", "Brown", "Taylor", "Anderson", "Lee", "Clark", "Walker", "Robinson", "Lewis",
            "Harris", "Young", "Allen", "King", "Wright", "Scott", "Green", "Baker", "Adams", "Nelson",
            "Carter", "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans", "Edwards",
            "Collins", "Stewart", "Morris", "Rodriguez", "Reed", "Cook", "Morgan", "Bell", "Murphy", "Bailey",
            "Rivera", "Cooper", "Richardson", "Cox", "Howard", "Ward", "Torres", "Peterson", "Gray", "Ramirez",
            "James", "Watson", "Brooks", "Kelly", "Sanders", "Price", "Bennett", "Wood", "Barnes", "Ross",
            "Henderson", "Coleman", "Jenkins", "Perry", "Powell", "Long", "Patterson", "Hughes", "Flores", "Washington",
            "Butler", "Simmons", "Foster", "Gonzalez", "Bryant", "Alexander", "Russell", "Griffin", "Diaz", "Hayes"
        ]

        positions = ["Forward", "Guard", "Center"]

        random.shuffle(team_names)
        random.shuffle(american_cities)
        used_team_names = set()
        used_player_names = set()

        for i in range(min(league.num_teams, len(team_names))):
            #ensures no duplicate team names - teams can share location but not a name

            team_name = team_names[i]
            if team_name in used_team_names:
                continue
            used_team_names.add(team_name)

            #team creation logic
            team = Team.objects.create(
                league=league,
                name=team_name,
                city=american_cities[i % len(american_cities)], 
                #default values for teams
                place_in_standings=0,
                wins=0,
                losses=0,
                star_mult=0
            )

            #default value for number of star players
            star_player_count = 0

            #player generation for the team
            for _ in range(5):  #each team has a roster of 5 players
                is_star = random.random() < 0.2  # 20% chance for a player to be a star
                if is_star:
                    star_player_count += 1

                #no duplicate FULL player name combinations
                first_name, last_name = None, None
                while True:
                    first_name = random.choice(player_first_names)
                    last_name = random.choice(player_last_names)
                    if (first_name, last_name) not in used_player_names:
                        used_player_names.add((first_name, last_name))
                        break

                Player.objects.create(
                    team=team,
                    first_name=first_name,
                    last_name=last_name,
                    position=random.choice(positions),
                    star=is_star,
                    dob=f"{random.randint(1985, 2005)}-{random.randint(1, 12):02}-{random.randint(1, 28):02}",
                )

            #update the star multiplier based on the number of star players
            team.star_mult = int(star_player_count * 1.02 * 100)
            team.save()

    def get_success_url(self):
        '''returns a url to redirect to upon successful creation'''

        return reverse('league_detail', kwargs={'pk': self.object.pk})


 
    
class LeagueDetailView(LoginRequiredMixin, DetailView):
    '''detail view about a specific league in the db'''

    model = League
    template_name = 'project/league.html'
    context_object_name = 'league'

    def get_context_data(self, **kwargs):
        #sends the context data regarding the league

        context = super().get_context_data(**kwargs)
        league = self.object
        context['league_name'] = league.name

        #display nothing in case there is no logo for the league
        if(league.logo == None):
            context['league_logo'] = ""
        context['league_logo'] = league.logo.url
        context['league_num_teams'] = league.num_teams
        context['league_num_games'] = league.num_games

        return context
    
class LeagueListView(LoginRequiredMixin, ListView):
    '''list of leagues that the user can view'''

    model = League
    template_name = 'league_list.html'
    context_object_name = 'leagues'

    def get_queryset(self):
        #only return leagues created by the logged-in user

        return League.objects.filter(user_league=self.request.user)
    

class LeagueManagementView(LoginRequiredMixin, TemplateView):
    '''view handling the core management functionality of the league simulator'''

    template_name = "project/league_management.html"

    def get_context_data(self, **kwargs):
        #returns necessary context regarding the league

        context = super().get_context_data(**kwargs)
        league = get_object_or_404(League, pk=self.kwargs['pk'])
        context['league'] = league

        #counts the number of games simulated
        num_games_simulated = Game.objects.filter(team1__league=league).count()
        context['num_games_simulated'] = num_games_simulated

        return context

    def post(self, request, *args, **kwargs):
        '''method to update the league specifically after simulating games OR resimulating games'''

        league = get_object_or_404(League, pk=self.kwargs['pk'])
        #teams = Team.objects.filter(league=league)

        #clear existing games for re-simulation
        deleted_games, _ = Game.objects.filter(team1__league=league).delete()
        print(f"Deleted games count in post: {deleted_games}")

        #simulate games using SimulateLeagueView logic
        SimulateLeagueView().post(request, pk=league.pk)

        messages.success(request, f"Games simulated successfully!")
        return redirect('league_management', pk=league.pk)




class LeagueTeamsView(ListView):
    """view all teams in a league"""

    model = Team
    template_name = 'league_teams.html'
    context_object_name = 'teams'

    def get_queryset(self):
        #return teams which belong to a league

        league_id = self.kwargs['pk']
        return Team.objects.filter(league_id=league_id)
    

class TeamPlayersView(ListView):
    """view all players on a team"""

    model = Player
    template_name = 'team_players.html'
    context_object_name = 'players'

    def get_queryset(self):
        #return players which belong to a team

        team_id = self.kwargs['pk']
        return Player.objects.filter(team_id=team_id)
    


class SimulateLeagueView(View):
    def post(self, request, pk, *args, **kwargs):
        '''method to update the league and resimulate games'''

        league = get_object_or_404(League, pk=pk)

        #delete existing games before resimulation
        deleted_games, _ = Game.objects.filter(team1__league=league).delete()
        print(f"Deleted games count: {deleted_games}")

        #restores original number of games from the league - did this step explicitly bc i was having
        #issues with the simulation logic
        original_num_games = league.num_games

        teams = list(league.team_set.all())
        num_teams = len(teams)
        max_games = original_num_games
        games_played = {team.id: 0 for team in teams}

        #date assignment logic
        next_available_date = {team.id: timezone.now().date() for team in teams}

        #this should not be a problem because the league form error checks for this
        if num_teams < 2:
            messages.error(request, "Not enough teams to simulate games.")
            return HttpResponseRedirect(reverse('league_management', args=[pk]))

        #same as above
        if max_games < num_teams - 1:
            messages.error(request, f"Number of games per team must be at least {num_teams - 1} to ensure each team plays every other team at least once.")
            return HttpResponseRedirect(reverse('league_management', args=[pk]))

        #default information for each team
        for team in teams:
            team.wins = 0
            team.losses = 0
            team.place_in_standings = 0
            team.save()

        def schedule_game(team1, team2):
            #method which takes care of scheduling a game - makes sure that the gap is between 2 or 3 days for each team

            game_date = max(next_available_date[team1.id], next_available_date[team2.id]) #assigns a next date from the 
            #highest avaiable date between the two teams
            game = Game.objects.create(team1=team1, team2=team2, date=game_date) #creates a game on the date found next available
            next_game_gap = random.randint(2, 3)
            next_available_date[team1.id] = game_date + datetime.timedelta(days=next_game_gap)
            next_available_date[team2.id] = game_date + datetime.timedelta(days=next_game_gap)
            game.points_scored()

            #checks to see if a team won or lost on a particular day and saves the result
            if game.points_scored_team1 > game.points_scored_team2:
                winner, loser = team1, team2
            else:
                winner, loser = team2, team1

            winner.wins += 1
            loser.losses += 1
            winner.save()
            loser.save()

            games_played[team1.id] += 1
            games_played[team2.id] += 1

        def can_schedule_game(team1, team2):
            #checks to see if two teams are available to play on a particular day

            return team1 != team2 and games_played[team1.id] < max_games and games_played[team2.id] < max_games

        #ensure each team plays exactly num_games (max_games) games
        for _ in range(max_games):
            for team1 in teams:
                for team2 in teams:
                    if can_schedule_game(team1, team2):
                        schedule_game(team1, team2)

        #sorts the teams for the standings based on wins to losses
        sorted_teams = sorted(teams, key=lambda t: (-t.wins, t.losses))

        #assigns standings based on record
        for index, team in enumerate(sorted_teams):
            team.place_in_standings = index + 1
            team.save()

        league.update_league_stats()

        #verify the number of game objects created - debugging purposes
        total_games_created = Game.objects.filter(team1__league=league).count()
        print(f"Total games created: {total_games_created}")
        print(f"Number of games per team should be: {original_num_games}")

        for team in teams:
            print(f"Games played by {team.name}: {games_played[team.id]}")

        messages.success(request, "League games have been simulated successfully!")
        return HttpResponseRedirect(reverse('league_management', args=[pk]))





class LoggedOutView(TemplateView):
    '''custom logout page using template view'''

    template_name = "project/logged_out.html"

class RegisterUserView(FormView):
    '''view to handle user registration using Django's UserCreationForm'''

    template_name = "project/create_user.html"
    form_class = UserCreationForm
    success_url = reverse_lazy('login')  # redirect to login page after successful registration

    def form_valid(self, form):
        '''save user and handle the form submission'''

        form.save()  # Create a new user in the database
        return super().form_valid(form)
    


class LeagueStatsView(LoginRequiredMixin, DetailView):
    '''view to manage displaying stats and provides filtering support'''

    model = League
    template_name = "project/league_stats.html"
    context_object_name = "league"

    def get_context_data(self, **kwargs):
        #method to handle context data
        context = super().get_context_data(**kwargs)
        league = self.get_object()
        
        team_name = self.request.GET.get('team_name', '')

        #filtering logic for teams
        if team_name:
            teams = Team.objects.filter(league=league, name__icontains=team_name)
            games = Game.objects.filter(team1__in=teams) | Game.objects.filter(team2__in=teams)
        else:
            games = Game.objects.filter(team1__league=league).order_by('-id')

        context['games'] = games
        context['teams'] = Team.objects.filter(league=league).order_by('place_in_standings', '-wins', 'losses')
        context['team_name'] = team_name

        return context


    
class LeagueTeamsView(LoginRequiredMixin, DetailView):
    '''a view to see the teams in the league'''

    model = League
    template_name = "project/league_teams.html"
    context_object_name = "league"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.filter(league=self.object)
        return context


class TeamRosterView(LoginRequiredMixin, DetailView):
    '''a view to see the roster for a specifc team'''

    model = Team
    template_name = "project/team_roster.html"

    def get_queryset(self):
        return Team.objects.filter(league_id=self.kwargs['league_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = Player.objects.filter(team=self.object)
        return context
    

class PlayerDetailView(LoginRequiredMixin, DetailView):
    '''a view to see details about a specific player'''

    model = Player
    template_name = "project/player_detail.html"

    def get_queryset(self):
        return Player.objects.filter(
            team_id=self.kwargs['team_pk'], team__league_id=self.kwargs['league_pk']
        )


class TeamDetailView(LoginRequiredMixin, DetailView):
    '''a view to see information about a specific team'''

    model = Team
    template_name = "project/team_detail.html"

    def get_queryset(self):
        return Team.objects.filter(league_id=self.kwargs['league_pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['roster'] = self.object.roster()
        context['team'] = Team.objects.get(pk=self.object.pk)
        context['all_teams'] = Team.objects.filter(league_id=self.kwargs['league_pk']).order_by('-wins', 'losses') #acquires all teams - debugging reasons
        return context



class UpdateTeamView(LoginRequiredMixin, UpdateView):
    """update a team's details"""

    model = Team
    fields = ['name', 'city', 'place_in_standings', 'wins', 'losses', 'star_mult']
    template_name = "project/update_team_form.html"

    def get_success_url(self):
        """return back to the league detail page"""

        return reverse_lazy('league_detail', kwargs={'pk': self.object.league.pk})
    

class UpdatePlayerView(LoginRequiredMixin, UpdateView):
    """update a player's attributes"""

    model = Player
    fields = ['first_name', 'last_name', 'position', 'star', 'dob']
    template_name = "project/update_player_form.html"

    def get_success_url(self):
        """return back to the team detail page"""

        team = self.object.team
        return reverse_lazy('team_detail', kwargs={
            'league_pk': team.league.pk,
            'pk': team.pk
        })
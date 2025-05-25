#Hinsley Casenet - U59220930
#project/models.py - used to encapsulate the model representations of different objects for the league simulator

from django.db import models
import time, random
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class League(models.Model):
    '''Represents a sports league containing multiple teams'''

    name = models.TextField(blank=False)
    logo = models.ImageField(blank=False)
    num_teams = models.IntegerField(default=0)
    num_games = models.IntegerField(default=0)
    user_league = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        '''Return a representation of this model'''

        return f'{self.name}'

    def update_league_stats(self):
        '''Updates the number of teams in the league'''

        self.num_teams = Team.objects.filter(league=self).count()
        self.save()

    def get_absolute_url(self):
        '''Returns a url for the object'''

        return reverse('league_detail', kwargs={'pk': self.pk})


    

class Team(models.Model):
    '''Model to represent a sports team'''

    name = models.TextField(blank=False)
    city = models.TextField(blank=False)
    place_in_standings = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    league = models.ForeignKey(League, on_delete=models.CASCADE)
    star_mult = models.IntegerField(blank=False)

    def team_schedule(self):
        '''Returns all games this team is involved in'''

        return Game.objects.filter(models.Q(team1=self) | models.Q(team2=self))

    def roster(self):
        '''Returns the list of players associated with this team'''

        return Player.objects.filter(team=self)

    def win_chance_modifier(self):
        '''Calculates a boosted win% chance per star player on the roster'''

        star_count = self.roster().filter(star=True).count()
        self.star_mult = star_count * 1.02
        return star_count
    
    def __str__(self):
        '''Returns a string representation of the team'''
        return f'{self.city} {self.name}'


class Player(models.Model):
    '''Model created to represent the different players on different teams'''

    # every player has one team
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    first_name = models.TextField(blank=False)
    last_name = models.TextField(blank=False)
    position = models.TextField(blank=False)
    star = models.BooleanField(default=False)
    dob = models.TextField(blank=False)

    ###########################################################################
    def __str__(self):
        '''returns a string representation of the player'''

        return f'{self.last_name}, {self.first_name} - {self.team}' 


class Game(models.Model):
    '''Model to encapsulate a game played between two teams'''

    team1 = models.ForeignKey(Team, related_name='home', on_delete=models.CASCADE)
    team2 = models.ForeignKey(Team, related_name='away', on_delete=models.CASCADE)
    points_scored_team1 = models.IntegerField(default=0)
    points_scored_team2 = models.IntegerField(default=0)
    winner = models.TextField(blank=True)
    date = models.DateField(default=timezone.now)  #date included for date logic (12/1)

    # def star_bonuses(self):
    #     '''original method to get and return star bonuses, not used'''

    #     team1_star_bonus = self.team1.win_chance_modifier
    #     team2_star_bonus = self.team2.win_chance_modifier
    #     return team1_star_bonus, team2_star_bonus

    def points_scored(self, *args, **kwargs):
        '''Using the win modifiers to calculate the points scored'''

        team1_star_bonus = self.team1.win_chance_modifier()
        team2_star_bonus = self.team2.win_chance_modifier()

        #defines the range for possible points scored for each team affected by the star bonus!
        team1_min_points = 70 + int(team1_star_bonus)
        team1_max_points = 140 + int(team1_star_bonus)
        team2_min_points = 70 + int(team2_star_bonus)
        team2_max_points = 140 + int(team2_star_bonus)

        #randomly assign each team points given that there are no points for the game yet
        if self.points_scored_team1 == 0 and self.points_scored_team2 == 0:
            self.points_scored_team1 = random.randint(team1_min_points, team1_max_points)
            self.points_scored_team2 = random.randint(team2_min_points, team2_max_points)

        #anti tie logic - randomly give one of the teams one more point, possibly code for overtime logic later!
        if self.points_scored_team1 == self.points_scored_team2:
            if random.choice([True, False]):
                self.points_scored_team1 += 1
            else:
                self.points_scored_team2 += 1

        #logic to assign a winner
        if not self.winner:
            if self.points_scored_team1 > self.points_scored_team2:
                self.winner = str(self.team1)
            else:
                self.winner = str(self.team2)

        self.save()

    def __str__(self):
        '''String representation of a game'''

        return f'{self.team1} vs {self.team2} - Winner: {self.winner}'

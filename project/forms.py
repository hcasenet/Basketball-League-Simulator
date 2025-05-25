#Hinsley Casenet - U59220930
#project/forms.py

from django import forms
from .models import League #model that we created

class CreateLeagueForm(forms.ModelForm):
    """A form to add league to the existing database with validation."""

    class Meta:
        model = League
        fields = ['name', 'logo', 'num_teams', 'num_games'] #values that should appear on form

    def clean(self):
        cleaned_data = super().clean()
        num_teams = cleaned_data.get('num_teams')
        num_games = cleaned_data.get('num_games')

        #check to make sure that there is a valid ratio of games to teams

        if num_teams < 2:
            raise forms.ValidationError("A league must have at least 2 teams.")

        min_games_required = num_teams - 1
        if num_games < min_games_required:
            raise forms.ValidationError(
                f'A league with {num_teams} teams must have at least {min_games_required} games to ensure each team plays every other team at least once.'
            )

        return cleaned_data


class UpdateLeagueForm(forms.ModelForm):
    '''A form to update an existing league, also with validation'''

    class Meta:
        model = League
        fields = ['name', 'logo', 'num_teams', 'num_games']  #values that should appear on form

    def clean(self):
        cleaned_data = super().clean()
        num_teams = cleaned_data.get('num_teams')
        num_games = cleaned_data.get('num_games')

        #same validation logic as before
        
        if num_teams < 2:
            raise forms.ValidationError("A league must have at least 2 teams.")

        min_games_required = num_teams - 1
        if num_games < min_games_required:
            raise forms.ValidationError(
                f'A league with {num_teams} teams must have at least {min_games_required} games to ensure each team plays every other team at least once.'
            )

        return cleaned_data



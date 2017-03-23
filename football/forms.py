from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class CreateTeamForm(forms.Form):
    team_name = forms.CharField(max_length=250, label='Team name',  help_text='Enter a team name')

    def clean_team_name(self):
        data = self.cleaned_data['team_name']

        # Always return the cleaned data!
        return data

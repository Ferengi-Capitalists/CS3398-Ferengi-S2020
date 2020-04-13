from django import forms
from .models import GoalType

class GoalForm(forms.ModelForm):
	class Meta: 
		model = GoalType
		fields = ['goal_objective', 'goal_choice_type', 'goal_accomplished']
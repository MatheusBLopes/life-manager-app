# habit_tracker/forms.py
from django import forms
from .models import Habit, HabitCompletion, DayOfWeek


class HabitForm(forms.ModelForm):
    days_of_week = forms.MultipleChoiceField(choices=DayOfWeek.DAY_CHOICES, widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Habit
        fields = ['user', 'name', 'days_of_week']
    
    def clean_days_of_week(self):
        selected_days = self.cleaned_data['days_of_week']

        mapping = {
            'Sun': 1,
            'Mon': 2,
            'Tue': 3,
            'Wed': 4,
            'Thu': 6,
            'Fri': 5,
            'Sat': 7,
        }

        cleaned_values = [mapping[day] for day in selected_days]

        return cleaned_values
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(HabitForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user
            self.fields['user'].widget = forms.HiddenInput()

class HabitCompletionForm(forms.ModelForm):
    class Meta:
        model = HabitCompletion
        fields = ['habit', 'date_completed']

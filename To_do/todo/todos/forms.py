from django.forms import ModelForm
from .models import Todo
from django import forms


class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ['category','title','memo','important']

class categoryForm(forms.Form):
    choices=[('Delivery 1Q23','Delivery 1Q23'),
    ('2H Reflections','2H Reflections'),
    ('Personal Todos' ,'Personal Todos'),
    ('Staff Meetings','Staff Meetings'),
    ('WBA staff meetings' ,'WBA staff meetings'),
    ('Iteration RPA' ,'Iteration RPA'),
    ('Iteration WBA','Iteration WBA'),
    ('1on1 Fran','1on1 Fran'),
    ('Daily Todos','Daily Todos')]

    category = forms.ChoiceField(label="",choices=choices,
        widget=forms.Select(
            attrs={
                'class':'form-control',

            }
        )
    )
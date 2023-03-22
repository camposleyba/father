from django.forms import ModelForm
from .models import Todo
from django import forms


class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ['category','title','memo','important']

class categoryForm(forms.Form):
    choices=[('Delivery 1Q23','Delivery 1Q23'),
    ('Delivery 2Q23','Delivery 2Q23'),
    ('Delivery 3Q23','Delivery 3Q23'),
    ('Delivery 4Q23','Delivery 4Q23'),
    ('2H Reflections','2H Reflections'),
    ('Personal Todos' ,'Personal Todos'),
    ('Staff Meetings','Staff Meetings'),
    ('WBA staff meetings' ,'WBA staff meetings'),
    ('IBM RPA' ,'IBM RPA'),
    ('Iteration RPA' ,'Iteration RPA'),
    ('Iteration WBA','Iteration WBA'),
    ('1on1 Fran','1on1 Fran'),
    ('Daily Todos','Daily Todos'),
    ('1on1 Chris','1on1 Chris'),
    ('Must Watch Series','Must Watch Series')]

    category = forms.ChoiceField(label="",choices=choices,
        widget=forms.Select(
            attrs={
                'class':'form-control',

            }
        )
    )
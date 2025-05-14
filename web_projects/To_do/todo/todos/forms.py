from django.forms import ModelForm
from .models import Todo
from django import forms


class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ['category','title','memo','important']

class categoryForm(forms.Form):
    choices=[
	('Delivery 1Q24','Delivery 1Q24'),
	('Delivery 2Q24','Delivery 2Q24'),
	('Delivery 3Q24','Delivery 3Q24'),
	('Delivery 4Q24','Delivery 4Q24'),
    ('Personal Todos' ,'Personal Todos'),
    ('Staff Meetings','Staff Meetings'),
    ('Iteration RPA' ,'Iteration RPA'),
    ('Iteration WBA','Iteration WBA'),
	('CRAFT Documentation','CRAFT Documentation'),
    ('1on1 Fran','1on1 Fran'),
    ('1on1 Chris','1on1 Chris'),
    ('1on1 Melissa','1on1 Melissa'),
	('1on1 Gabe','1on1 Gabe'),
	('1on1 Colleen','1on1 Colleen'),
	('1on1 Pablo','1on1 Pablo'),
    ('Daily Todos','Daily Todos'),
    ('Must Watch Series','Must Watch Series'),
    ('Juana','Juana')]

    category = forms.ChoiceField(label="",choices=choices,
        widget=forms.Select(
            attrs={
                'class':'form-control',

            }
        )
    )

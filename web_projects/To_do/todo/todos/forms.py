from django.forms import ModelForm
from .models import Todo
from django import forms


class TodoForm(ModelForm):
	class Meta:
		model = Todo
		fields = ['category','title','memo','important']

class categoryForm(forms.Form):
    choices=[('Chatbot','Chatbot'),
    ('SAP4HANA','SAP4HANA'),
    ('Presentación Usina Arte','Presentación Usina Arte'),
    ('Delivery 1Q23','Delivery 1Q23'),
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
    ('1on1 Chris','1on1 Chris'),
    ('1on1 Melissa','1on1 Melissa'),
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
from django import forms


class addDaysForm(forms.Form):
    choices=[('Pablo Iacovone','Pablo Iacovone'),
    ('Santiago Kitashima','Santiago Kitashima'),
    ('Bruno Secchiari' ,'Bruno Secchiari'),
    ('Ezequiel Ferlauto','Ezequiel Ferlauto'),
    ('Andres Grosman' ,'Andres Grosman'),
    ('Laura Bisaccia' ,'Laura Bisaccia'),
    ('Dario Atach','Dario Atach'),
    ('Martin Spadoni' ,'Martin Spadoni'),
    ('Martin Williner' ,'Martin Williner'),
    ('Martin Laguna' ,'Martin Laguna')]

    choiceadd = forms.ChoiceField(label="",choices=choices, 
        widget=forms.Select(
            attrs={
                'class':'form-control',

            }
        )
    )

    days = forms.DecimalField(label="",max_digits=20,decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control'

            }
            )
        )
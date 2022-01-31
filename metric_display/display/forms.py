from django import forms

class inputf(forms.Form):
    inputfile = forms.FileField(label="",
         widget=forms.FileInput(
            attrs={
                'class':'form-control'
            }
        )
    )

class inputfspec(forms.Form):
    inputfile = forms.FileField(label="",
         widget=forms.FileInput(
            attrs={
                'class':'form-control'
            }
        )
    )

class inputfval(forms.Form):
    inputfile = forms.FileField(label="",
         widget=forms.FileInput(
            attrs={
                'class':'form-control'
            }
        )
    )

class awardform(forms.Form):
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

    choiceaward = forms.ChoiceField(label="",choices=choices, 
        widget=forms.Select(
            attrs={
                'class':'form-control',

            }
        )
    )


    goalamount = forms.DecimalField(label="",max_digits=20,decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control'

            }
            )
        )

    wizardamount = forms.DecimalField(label="",max_digits=20,decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class':'form-control'

            }
            )
        )


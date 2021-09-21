from django import forms

class inputf(forms.Form):
    inputfile = forms.FileField(label="",
         widget=forms.FileInput(
            attrs={
                'class':'form-control'
            }
        )
    )


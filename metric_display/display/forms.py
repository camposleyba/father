from django import forms

class inputf(forms.Form):
    input_file = forms.FileField(label="", widget=forms.FileInput(
            attrs={
                'class':'form-control'


            }
        )
    )
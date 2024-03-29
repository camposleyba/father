from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class ContactForm(forms.Form):
	fullname = forms.CharField(widget=forms.TextInput(
		attrs={'class':'form-control','id':'form_fullname', 'placeholder':'Name'
	 		})
		)
	email = forms.EmailField(widget=forms.EmailInput(
		attrs={'class':'form-control','id':'form_email', 'placeholder':'Email'

			})
		)
	content = forms.CharField(widget=forms.Textarea(
		attrs={'class':'form-control','id':'form_content', 'placeholder':'Your message'

			})
		)

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if not 'gmail.com' in email:
			raise forms.ValidationError('Email has to be gmail.com')
		return email


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'form-control', 'id':'form-password', 'placeholder':'Password'

			})
		)

class RegisterForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField(widget=forms.EmailInput(
		attrs={'class':'form-control','id':'form_email', 'placeholder':'Email'

			})
		)
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'form-control', 'id':'form-password', 'placeholder':'Password'

			})
		)
	password2 = forms.CharField(widget=forms.PasswordInput(
		attrs={'class':'form-control', 'id':'form-password', 'placeholder':'Confirm Password'

			})
		)

	def clean_username(self):
		username = self.cleaned_data.get('username')
		qs = User.objects.filter(username=username)
		if qs.exists:
			raise forms.ValidationError("Username is taken, pick a new one please.")
		return username


	def clean(self):
		data = self.cleaned_data
		password = data.get('password')
		password2 = data.get('password2')
		if password2 != password:
			raise forms.ValidationError("Passwords must match")
		return data
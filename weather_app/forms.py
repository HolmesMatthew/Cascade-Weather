from django import forms


class NewUser(forms.Form):
    username = forms.CharField(label='Username', max_length=10)
    password = forms.CharField(
        widget=forms.PasswordInput, label='Password', max_length=10)
    first_name = forms.CharField(
        label='First Name', max_length=15, required=False)
    last_name = forms.CharField(
        label='Last Name', max_length=15, required=False)
    email = forms.EmailField(label='Email')


class LoginUser(forms.Form):
    username = forms.CharField(label='Username', max_length=10)
    password = forms.CharField(
        widget=forms.PasswordInput, label='Password', max_length=10)


class SearchWeather(forms.Form):
    search = forms.CharField(label='search', max_length=25)

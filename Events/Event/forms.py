from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Event

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'

        for fieldname in ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']:
            self.fields[fieldname].label = ''
            self.fields[fieldname].help_text = ''

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'

        for fieldname in ['username', 'password']:
            self.fields[fieldname].label = ''
            self.fields[fieldname].help_text = ''

class EventForm(forms.ModelForm):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label='From')
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True, label='To')

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'organizer']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Event Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'organizer': forms.Select(attrs={'placeholder': 'Organizer'}),
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        
        self.fields['organizer'].queryset = User.objects.filter(is_superuser=True)

        for fieldname in ['title', 'description', 'location']:
            self.fields[fieldname].label = ''
            self.fields[fieldname].help_text = ''

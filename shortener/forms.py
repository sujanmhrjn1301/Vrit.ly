from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import ShortenedURL

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class ShortenURLForm(forms.ModelForm):
    expiration_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control',
        }),
        label='Expiration date',
        help_text='Optional: Set when this link expires'
    )

    class Meta:
        model = ShortenedURL
        fields = ['original_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['original_url'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Paste your long link here'
        })

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data.get('expiration_date')
        if expiration_date:
            from django.utils import timezone
            today = timezone.now().date()
            if expiration_date <= today:
                raise ValidationError("Expiration date must be in the future.")
        return expiration_date

class CustomShortForm(forms.ModelForm):
    class Meta:
        model = ShortenedURL
        fields = ['custom_key']

    def clean_custom_key(self):
        custom_key = self.cleaned_data.get('custom_key')

        if custom_key:
            existing = ShortenedURL.objects.filter(
                custom_key=custom_key
            ).exclude(pk=self.instance.pk)

            if existing.exists():
                raise ValidationError("This custom short code is already taken.")

            if len(custom_key) < 3:
                raise ValidationError("Custom short code must be at least 3 characters.")

        return custom_key

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['custom_key'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter custom short code (optional)'
        })

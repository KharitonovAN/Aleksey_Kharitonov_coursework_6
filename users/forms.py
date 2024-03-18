from main_app.forms import CrispyFormMixin
from users.models import User
from django import forms
from django.forms import HiddenInput
from django.contrib.auth.forms import (
    UserChangeForm,
    UserCreationForm,
    PasswordResetForm,
    SetPasswordForm
)


class UserForm(CrispyFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'


class RegisterForm(CrispyFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(CrispyFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'phone', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = HiddenInput()


class UserForgotPasswordForm(PasswordResetForm):
    pass


class UserSetNewPasswordForm(SetPasswordForm):
    pass


class ModeratorForm(CrispyFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_active']

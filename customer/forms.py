from urllib import request
from django import forms
from django.contrib.auth.models import User
from . import models


class CustomerForm(forms.ModelForm):
    class Meta:
        model = models.Customer
        fields = '__all__'
        exclude = ('user',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação de Senha',
    )

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data

        validation_error_messages = {}

        user_data = cleaned.get('username')
        pass_data = cleaned.get('password')
        pass2_data = cleaned.get('password2')
        email_data = cleaned.get('email')

        user_db = User.objects.filter(username=user_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_passwd_not_match = 'Senhas não conferem'
        error_passwd_short = 'Senha precisa ter pelo menos 6 caracteres'
        error_passwd_required_field = 'A senha é obrigatória'

        # Update customer validation
        if self.user:
            if user_db:
                if user_data != self.user.username:
                    validation_error_messages['username'] = error_msg_user_exists

            if email_db:
                if email_data != self.user.email:
                    validation_error_messages['email'] = error_msg_email_exists

            if pass_data:
                if pass_data != pass2_data:
                    validation_error_messages['password'] = error_passwd_not_match
                    validation_error_messages['password2'] = error_passwd_not_match
                if len(pass_data) < 6:
                    validation_error_messages['password'] = error_passwd_short

        # Create User validation
        else:
            if user_db:
                validation_error_messages['username'] = error_msg_user_exists

            if email_db:
                validation_error_messages['email'] = error_msg_email_exists

            if not pass_data:
                validation_error_messages['password'] = error_passwd_required_field
            if not pass2_data:
                validation_error_messages['password2'] = error_passwd_required_field
            
            if pass_data != pass2_data:
                validation_error_messages['password'] = error_passwd_not_match
                validation_error_messages['password2'] = error_passwd_not_match

            if len(pass_data) < 6:
                validation_error_messages['password'] = error_passwd_short
        
        if validation_error_messages:
            raise(forms.ValidationError(validation_error_messages))
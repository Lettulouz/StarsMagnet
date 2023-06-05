from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from api.models import Companies
User = get_user_model()

class CustomUserForm(UserCreationForm):

    def clean(self):
        cln_data = super().clean()
        username = cln_data.get('username')
        email = cln_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "Email already taken")

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error("username", "Username already taken")

    class Meta:
         model = User
         fields = ('email',)

class CustomUserChanger(UserChangeForm):
    def clean(self):
        cln_data = super().clean()
        username = cln_data.get('username')
        email = cln_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "Email already taken")

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error("username", "Username already taken")

    class Meta:
        model = User
        fields = ('email',)

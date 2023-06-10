from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from api.models import Companies
User = get_user_model()


class CustomUserForm(UserCreationForm):

    """
    Form to add new user by admin, inherited from UserCreationForm.
    """
    def clean(self):
        """
        Method to validate added user,
        checks if username or email already exists,
        adds an error if so
        """
        cln_data = super().clean()
        username = cln_data.get('username')
        email = cln_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "Email already taken")

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error("username", "Username already taken")

    class Meta:
         """
          Metadata for CustomUserForm,
          contains used model and fields
         """
         model = User
         fields = ('email',)

class CustomUserChanger(UserChangeForm):

    """
    Form to edit user by admin, inherited from UserChangeForm.
    """

    def clean(self):
        """
        Method to validate edited user,
        checks if username or email already exists,
        and belong to another user
        adds an error if so
        """
        cln_data = super().clean()
        username = cln_data.get('username')
        email = cln_data.get('email')

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "Email already taken")

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error("username", "Username already taken")

    class Meta:
        """
          Metadata for UserChangeForm,
          contains used model and fields
        """
        model = User
        fields = ('email',)

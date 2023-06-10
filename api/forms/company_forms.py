from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from api.models import Companies
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanyForm(forms.ModelForm):
    """
    Form to edit Company by admin.
    Modify password field and add confirm_password field.
    """

    password = forms.CharField(
        required=False,
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(
       required=False,
       label="Password confirmation",
       widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
       strip=False,
       help_text="Enter the same password as before, for verification.",
    )
    class Meta:
        """
          Metadata for CustomUserForm,
          contains used model and fields.
        """
        model = Companies
        fields = ('name', 'site',  'token', 'email', 'username', 'password', 'confirm_password', 'status')

    def clean(self):
        """
        Method to validate edited Company,
        checks if username or email already exists
        and if passwords are equal or empty,
        adds an error if unique data already exist or passwords aren't the same.
        """
        cln_data = super().clean()
        password = cln_data.get('password')
        username = cln_data.get('username')
        email = cln_data.get('email')
        confirm_password = cln_data.get('confirm_password')

        if password is not None or confirm_password is not None:
            if password != confirm_password:
                self.add_error('confirm_password', "The two password fields didn’t match.")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "Email already taken")

        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error("username", "Username already taken")

    def save(self, commit=True):
        """
        Method to save changes for company.
        :param commit: autosave
        :return: Companies object
        """
        company = super().save(commit=False)

        company = Companies.objects.get(pk=self.instance.pk)
        company.name=self.cleaned_data['name']
        company.site=self.cleaned_data['site']
        company.username=self.cleaned_data['username']
        if self.cleaned_data['password']:
            company.password=make_password(self.cleaned_data['password'])
        company.token=self.cleaned_data['token']
        company.email=self.cleaned_data['email']
        company.status=self.cleaned_data['status']

        company.save()
        return company


class AddCompanyForm(forms.ModelForm):
    """
    Form to add new Company by admin.
    Modify password field and add confirm_password field.
    """
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        validators=[validate_password]
    )
    confirm_password = forms.CharField(required=True,
                                       label="Password confirmation",
                                       widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
                                       strip=False,
                                       help_text="Enter the same password as before, for verification.",
                                       )
    class Meta:
        """
          Metadata for CustomUserForm,
          contains used model and fields.
        """
        model = Companies
        fields = ('name', 'site',  'token', 'email', 'username', 'password', 'confirm_password', 'status')

    def clean(self):
        """
        Method to validate added Company,
        checks if username or email already exists
        and if passwords are equal,
        adds an error if unique data already exist or passwords aren't the same.
        """
        cln_data = super().clean()
        password = cln_data.get('password')
        username = cln_data.get('username')
        email = cln_data.get('email')
        confirm_password = cln_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "The two password fields didn’t match.")

        if User.objects.filter(email=email).exists() or Companies.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "Email already taken")

        if User.objects.filter(username=username).exists() or Companies.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            self.add_error("username", "Username already taken")

    def save(self, commit=True):
        """
        Method to save added company.
        :param commit: autosave
        :return: Companies object
        """
        company = super().save(commit=False)

        company = Companies.objects.create(
            name=self.cleaned_data['name'],
            site=self.cleaned_data['site'],
            username=self.cleaned_data['username'],
            password=make_password(self.cleaned_data['password']),
            token=self.cleaned_data['token'],
            email=self.cleaned_data['email'],
            status=self.cleaned_data['status']
        )

        company.save()
        return company
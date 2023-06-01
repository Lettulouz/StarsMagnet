from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from api.models import Companies
from django.contrib.auth import get_user_model

User = get_user_model()

class CompanyForm(forms.ModelForm):


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
        model = Companies
        fields = ('name', 'site',  'token', 'email', 'login', 'password', 'confirm_password', 'status')

    def clean(self):
        cln_data = super().clean()
        password = cln_data.get('password')
        login = cln_data.get('login')
        email = cln_data.get('email')
        confirm_password = cln_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "The two password fields didn’t match.")

        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            self.add_error("email", "Email already taken")

        if User.objects.filter(username=login).exclude(pk=self.instance.pk).exists() or Companies.objects.filter(login=login).exclude(pk=self.instance.pk).exists():
            self.add_error("login", "Username already taken")

    def save(self, commit=True):
        company = super().save(commit=False)

        company = Companies.objects.create(
            name=self.cleaned_data['name'],
            site=self.cleaned_data['site'],
            login=self.cleaned_data['login'],
            password=make_password(self.cleaned_data['password']),
            token=self.cleaned_data['token'],
            email=self.cleaned_data['email'],
            status=self.cleaned_data['status']
        )

        company.save()
        return company




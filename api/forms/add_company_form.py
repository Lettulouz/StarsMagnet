from django import forms
from django.contrib.auth.hashers import make_password
from api.models import Companies


class CompanyForm(forms.ModelForm):

    confirm_password = forms.CharField(required=True)
    class Meta:
        model = Companies
        fields = ('name', 'site',  'token', 'email', 'login', 'password', 'confirm_password', 'status')

    def clean(self):
        cln_data = super().clean()
        password = cln_data.get('password')
        confirm_password = cln_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("The two password fields didn’t match.")

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




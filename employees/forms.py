from django import forms
from accounts.models import User
from .models import Employee

class EmployeeCreateForm(forms.ModelForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Employee
        fields = ['department', 'designation', 'date_of_joining', 'basic_salary']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
            'designation': forms.Select(attrs={'class': 'form-control'}),
            'date_of_joining': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'basic_salary': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean_password(self):
        password = self.cleaned_data['password']
        if not password.strip():
            raise forms.ValidationError("Password cannot be empty")
        return password


from .models import EmployeeProfile

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = [
            "photo", "phone", "personal_email", "address",
            "date_of_birth", "emergency_contact",
            "bank_name", "account_number", "ifsc_code"
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

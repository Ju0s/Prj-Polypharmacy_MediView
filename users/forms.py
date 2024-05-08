from django import forms
from django.core.exceptions import ValidationError
from users.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        widget=forms.TextInput(
            attrs={'placeholder':'사용자명(3자리 이상)'},
        ),
        )
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(
            attrs={'placeholder':'비밀번호 (8자리 이상)'},
        ),
        )
    
class SignupForm(forms.Form):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError(f'입력한 사용자명({username})은 이미 사용 중입니다.')
        return username
    
    def clean(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            self.add_error('password2','비밀번호가 서로 다릅니다.')
            
    def save(self):
        username = self.cleaned_data['username']
        password1 = self.cleaned_data['password1']
        user = User.objects.create_user(
            username=username,
            password=password1,
        )
        return user 
    
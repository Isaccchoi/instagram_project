from django import forms
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()


class UserForm(forms.Form):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError('이미 존재하는 계정입니다!')
        return data

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('비밀번호가 같지 않습니다.')
        return password2

    def clean(self):
        # clean은 is_valid하건 is_valid하지 않건 무조건 실행
        if self.is_valid():
            setattr(self, 'signup', self._signup)
        return self.cleaned_data

    def _signup(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=username, password=password)
        if user is not None:
            login(request, user)


class LoginForm(forms.Form):
    """
    is_valid()에서 주어진 username/password를 사용한 authenticate실행 성공시 login(request)메서드를 사용할 수 있음
    """
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        self.user = authenticate(username=username, password=password)
        if not self.user:
            raise forms.ValidationError("계정 이름 또는 암호가 맞지 않습니다.")
        else:
            # clean에서 user를 넣었을때만 self._login을 self.login으로 사용할 수 있도록 지
            setattr(self, 'login', self._login)
        return cleaned_data

    def _login(self, request):
        if self.user is not None:
            login(request, self.user)

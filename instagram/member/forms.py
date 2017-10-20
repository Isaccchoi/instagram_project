from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class SignupForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        class_update_fields = ('password1', 'password2')
        for field in class_update_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            'username',
            'password1',
            'password2',
            'img_profile',
            'age',
        )
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'age': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }


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

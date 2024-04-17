from django import forms
from . models import User, UserProfile
from .validators import allow_only_images_validator
from django.core.validators import RegexValidator, EmailValidator

# Custom validator for password
password_validator = RegexValidator(
    regex=r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
    message="Password must be at least 8 characters long and include at least one number and one special character."
)

first_name_validator = RegexValidator(
    regex=r'^[A-Za-z]{2,}$',
    message="First name must be at least 2 characters long and include only letters."
)

last_name_validator = RegexValidator(
    regex=r'^[A-Za-z]{2,}$',
    message="last name must be at least 2 characters long and include only letters."
)

# Custom email validator if you need specific criteria
email_validator = EmailValidator(
    message="Enter a valid email address."
)
class UserForm(forms.ModelForm):
    first_name = forms.CharField(validators=[first_name_validator])
    last_name = forms.CharField(validators=[last_name_validator])
    email = forms.EmailField(validators=[email_validator])  # Using the custom or Django's built-in EmailValidator
    password = forms.CharField(widget=forms.PasswordInput(), validators=[password_validator])
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'address', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude']
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
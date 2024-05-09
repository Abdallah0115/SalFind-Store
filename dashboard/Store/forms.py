from django import forms
from .models import Cust , CustGroup
from django.contrib.auth.models import User
from django.contrib.auth.models import Group 
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import get_user_model

class CustForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=255)
    username = forms.EmailField(max_length=255)
    name_prefix = forms.CharField(max_length=10, required=False)
    middle_initial = forms.CharField(max_length=1, required=False)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    age = forms.IntegerField()
    ssn = forms.CharField(max_length=255)
    phone_no = forms.CharField(max_length=20)
    place_name = forms.CharField(max_length=255)
    county = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    zip_code = forms.CharField(max_length=20)
    region = forms.ChoiceField(choices = [('South','South'),('East','East'),('West','West'),('North','North')])
    state = forms.ChoiceField(choices=[('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
                                        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'),
                                        ('DE', 'Delaware'), ('DC', 'District Of Columbia'), ('FL', 'Florida'),
                                        ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
                                        ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'),
                                        ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'), ('MA', 'Massachusetts'),
                                        ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'), ('MO', 'Missouri'),
                                        ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
                                        ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
                                        ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
                                        ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
                                        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
                                        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
                                        ('WI', 'Wisconsin'), ('WY', 'Wyoming')])


    class Meta:
        model = Cust
        fields = ['full_name', 'name_prefix','first_name' ,'middle_initial','username' ,'last_name', 'gender', 'age', 'email',  'ssn', 'phone_no',
                    'place_name', 'county', 'city', 'state', 'zip_code', 'region','image','password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2

    def save(self, commit=True):
        instance = super(CustForm, self).save(commit=False)
        user = User.objects.create_user(first_name=self.cleaned_data['first_name'],last_name=self.cleaned_data['last_name'],email=self.cleaned_data['email'],username= self.cleaned_data['email'],password= self.cleaned_data['password1'])
        default_group = Group.objects.get(name='customers')
        instance.user = user

        if commit:
            instance.save()
            CustGroup.objects.create(cust=instance, group=default_group)
        return instance

class searchForm(forms.Form):

    Custmail = forms.EmailField(label='Custmail')

class editCustForm(forms.ModelForm):
    class Meta:
        model = Cust
        fields = ['full_name', 'name_prefix', 'middle_initial', 'gender', 'age', 'ssn', 'phone_no',
                    'place_name', 'county', 'city', 'state', 'zip_code', 'region', 'image']

    def __init__(self, *args, **kwargs):
        super(editCustForm, self).__init__(*args, **kwargs)
        # Exclude the user field from being edited


    def clean_user(self):
        # Ensure the user field cannot be changed
        return self.instance.user

User = get_user_model()

class UserPasswordUpdateForm(forms.Form):
    current_password = forms.CharField(label='Current Password', widget=forms.PasswordInput)
    new_password = forms.CharField(label='New Password', widget=forms.PasswordInput)
    confirm_new_password = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError('Invalid current password')
        return current_password

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise forms.ValidationError('New passwords do not match')
        return confirm_new_password

    def save(self):
        new_password = self.cleaned_data.get('new_password')
        self.user.password = make_password(new_password)
        self.user.save()

User = get_user_model()

class UserPasswordResetForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(user, *args, **kwargs)

    def save(self, commit=True):
        # Save the new password for the user
        self.user.set_password(self.cleaned_data["new_password1"])
        if commit:
            self.user.save()
        return self.user
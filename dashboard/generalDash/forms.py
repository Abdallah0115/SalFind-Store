from django.contrib.auth.models import User 
from django.contrib.auth.models import Group
from django import forms
from .models import guest, guestGroup, sess

class searchForm(forms.Form):

    Custmail = forms.EmailField(label='Custmail')

class CustForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    full_name = forms.CharField(max_length=255)
    username = forms.EmailField(max_length=255)
    


    class Meta:
        model = guest
        fields = ['full_name','first_name','username' ,'last_name', 'email','password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2

    def save(self, commit=True):
        instance = super(CustForm, self).save(commit=False)
        user = User.objects.create_user(first_name=self.cleaned_data['first_name'],last_name=self.cleaned_data['last_name'],email=self.cleaned_data['email'],username= self.cleaned_data['email'],password= self.cleaned_data['password1'])
        default_group = Group.objects.get(name='guest')
        instance.user = user

        if commit:
            instance.save()
            guestGroup.objects.create(guest = instance, group = default_group)
        return instance

class sessForm(forms.ModelForm):

    name = forms.CharField(required=True)

    description = forms.CharField(max_length=100 ,required=True)

class sessForm(forms.ModelForm):
    gues = guest
    class Meta:
        model = sess
        fields = ['name','description','csv_file','gues']
        widgets = {
            'last_used': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea()
        }
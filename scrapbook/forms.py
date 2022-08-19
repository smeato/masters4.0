from django.contrib.auth.models import User
from django.forms import ClearableFileInput, FileField, ImageField, ModelForm, TextInput, URLInput
from django import forms
from django.contrib.auth.forms import UserCreationForm
from pyparsing import Char


from scrapbook.models import Page

ROLES =[('owner', 'I want to make a scrapbook'),
        ( 'contributor', 'I want to help someone with their scrapbook'), 
        ('own/contrib', 'I want to do both'),]

RELATIONSHIPS =[ ('own', 'Me'),
                ('partner/spouse', 'Partner/Spouse'), 
                ('child', 'Child'), 
                ('friend', 'Friend'), 
                ('carer', 'Carer/Assistant')]

class RegForm(UserCreationForm):

        recovery_email = forms.EmailField(label='If you need to reset your password, what email should we send the reset link to?')
        recovery_relationship = forms.CharField(label='Who does this email belong to?', widget=forms.Select(choices=RELATIONSHIPS))
        role = forms.CharField(label='What would you like to use Scrapbook for?', widget=forms.Select(choices=ROLES))
        
        class Meta:
                model = User
                fields = ['username', 'password1', 'password2', 'first_name', 'recovery_email', 'recovery_relationship', 'role',]
        
        def save(self, commit=False):
                user = super(RegForm, self).save(commit=False)
                if commit:
                        user.set_password(user.password)
                        user.save() 
                return user

class PageForm(forms.ModelForm):
        class Meta:
                model = Page 
                fields = ('title', 'video_file', 'image_file')
                widgets = {
                        'title': forms.TextInput(attrs={'class': 'form-group', 'label':'Give your page a title'}),
                        'video_file': forms.FileInput(attrs={'class': 'form-group', 'label':'Upload a video here or use YouTube in a later step'}), 
                        'image_file': forms.FileInput(attrs={'class': 'form-group', 'label':'Upload a picture'}),
                }
                labels = {
                        'title': 'Give Your Page a Title',
                        'video_file': 'Upload a Video Here or Use YouTube in a Later Step',
                        'image_file': 'Upload a Picture'
                }

        
# class UserForm(ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput())
    
    
#     class Meta:
#         model = User
#         fields = ('username', 'email', 'password', 'first_name')
        









# class PageForm(ModelForm):
#     class Meta:
#         model = Page
#         fields = ['title', 'video_url', 'video_file', 'song_id']
        
#         widgets = {
#             'title': TextInput(attrs={
#                 'class' : 'form-control', 
#                 'style': 'max-width: 300px;', 
#                 'placeholder': 'Enter a title...'
#                 }),
#             'video_url': URLInput(attrs={
#                 'class': "form-control",
#                 'style': 'max-width: 300px;', 
#                 'placeholder': 'Copy a YouTube link here...' 
#             }),
#             'video_file': ClearableFileInput(attrs={
#                 'class' : 'form-control'
                
#             }), 
#             'song_id': TextInput(attrs={
#                 'class' : 'form-control',
                
#             })
#         }
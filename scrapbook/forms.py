from django.contrib.auth.models import User
from django.forms import ClearableFileInput, FileField, ImageField, ModelForm, TextInput, URLInput
from django import forms
from pyparsing import Char


from scrapbook.models import Page

class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name')
        









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
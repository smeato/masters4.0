from distutils.command.upload import upload
from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.forms import SlugField 
from django.template.defaultfilters import slugify
from django.urls import reverse
#from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
import subprocess
from base64 import b64encode, b32encode
import uuid
from os import urandom
from django.db.models.signals import post_save
from django.dispatch import receiver


USERNAME_MAX = 15
PASSWORD_MIN = 4
PASSWORD_MAX = 12
TITLE_LENGTH = 50

# user account model where a user can have the role of scrapbook owner, scrapbook contributor or both
class Account(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE, primary_key=True)
    id = models.IntegerField() 
    has_scrapbook = models.BooleanField(default=True)
    shares_scrapbook = models.BooleanField(default=False)
    recovery_email = models.EmailField(blank=True)
    recovery_relationship = models.CharField(max_length=20)
    
    def save(self, *args, **kwargs):
        self.id = self.user.id
        self.user.email = self.recovery_email
        super(Account, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username 
    
@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)
    instance.account.save()
        
    
class Scrapbook(models.Model):
    owner = models.OneToOneField(User, related_name='owner', on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, related_name='collaborators', blank=True)
    share_code = models.CharField(max_length=20) 

    def __str__(self):
        return self.owner.username 
    
    def save(self, *args, **kwargs):
        code = uuid.uuid4().hex[:6].upper()
        
        if "'" in code:
            self.share_code = code.replace("'", "")
        else:
            self.share_code = code
        while Scrapbook.objects.filter(share_code=self.share_code):
            code = uuid.uuid4().hex[:6].upper()
            if "'" in code:
                self.share_code = code.replace("'", "")
            else:
                self.share_code = code
        super(Scrapbook, self).save(*args, **kwargs)
        
class Page(models.Model):
    title = models.CharField(max_length=50)
    creator = models.ForeignKey(User, related_name='creator', on_delete=models.CASCADE)
    scrapbook = models.ForeignKey('Scrapbook', on_delete=models.CASCADE)
    vid_src = models.CharField(max_length=22, blank=True)
    song_embed = models.CharField(max_length=24, blank=True)
    video_file = models.FileField(blank=True, upload_to='page_videos')
    image_file = models.FileField(blank=True, upload_to='page_images')
    title_slug = models.SlugField()
    
    def get_absolute_url(self):
        return reverse('scrapbook:page_view', kwargs={'page_pk': self.id})
    
    def save(self, *args, **kwargs):
        self.title_slug = slugify(self.title)
        
        
        super(Page, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title
    
    

class Image(models.Model):
    gallery = models.ForeignKey(Page, on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to='page_images', blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    
    
class TextNote(models.Model):
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    text = models.TextField(max_length=10000)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    
    def __str__(self):
        return self.title
    
    
class VoiceNote(models.Model):
    title = models.CharField(max_length=100)
    page = models.ForeignKey('Page', on_delete=models.CASCADE)
    audio = models.FileField(blank=True, upload_to='page_audio_files')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title
    
class Activity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    uploads = models.FileField(blank=True, upload_to='activity_uploads')
    
    class Meta:
        verbose_name_plural = 'Activities'
        
    def __str__(self):
        return self.title
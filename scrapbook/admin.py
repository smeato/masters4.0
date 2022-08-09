from django.contrib import admin
from .models import Activity, Scrapbook, Page, Image, TextNote, Account, VoiceNote

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'title_slug':('title',)}
    
# Register your models here.
admin.site.register(Scrapbook)
admin.site.register(Image)
admin.site.register(TextNote)
admin.site.register(VoiceNote)
admin.site.register(Activity)
admin.site.register(Page, PageAdmin)
admin.site.register(Account)
#from typing_extensions import Required
from asyncio import subprocess
import os
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect 
from .models import Image, Page, Scrapbook, User, TextNote
from scrapbook.forms import UserForm 
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect 
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.http import JsonResponse
import json 
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date

from pathlib import Path


# Create your views here.
def index(request): 
    context = {}
    
    if request.user.is_authenticated:
        user = request.user
        context['books'] = []
        scrapbooks = Scrapbook.objects.filter(collaborators__username=user.username)
        for book in scrapbooks: 
            print(book)
            context['books'].append(book)
        
    return render(request, 'scrapbook/index.html', context)

# class based view for listing all pages in the given scrapbook
class ScrapbookView(ListView):
    model = Page 
    
    template_name = 'scrapbook/scrapbook_view.html'
    
    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        self.scrapbook = get_object_or_404(Scrapbook, owner=self.user)
        
        self.viewable = False
        
        if self.user == self.request.user:
            self.viewable = True 
        else:
            self.current_collaborator = self.scrapbook.collaborators.filter(username=self.request.user.username)
            if self.current_collaborator:
                self.viewable = True
            else:
                self.viewable = False
        
        if not self.viewable:
            return reverse_lazy('scrapbook:no_access')
        return Page.objects.filter(scrapbook=self.scrapbook)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.username 
        context['viewable'] = self.viewable 
        return context


class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    fields = ['title', 'video_file', 'image_file']
    
    def get_success_url(self) -> str:
        return reverse_lazy('scrapbook:complete_page', kwargs={'page_pk': self.object.pk})
    
    def form_valid(self, form): 
        form.instance.creator = self.request.user 
        form.instance.scrapbook = get_object_or_404(Scrapbook, owner=get_object_or_404(User, username=self.kwargs['username']))
        
        return super().form_valid(form)



@login_required
def song_search(request):
    if is_ajax(request):
        spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        data = json.load(request)
        artist = data['artist']
        title = data['song_title']
        
        q = " track:" + title 
        print(q)
        if artist: 
            q = q + " artist:" + artist
            
        q.replace(" ", "%20")
        print(q)
        result = spotify.search(q, 5, 0, "track")
        response = {}
        no_of_results = len(result['tracks']['items'])
        
        
        embedPre = "https://open.spotify.com/embed/track/"
        embedPost = "?utm_source=generator"
        
        if no_of_results >= 1:
            embed1 = embedPre + result['tracks']['items'][0]['id'] + embedPost
            response['result 1'] = embed1
        if no_of_results >= 2:
            embed2 = embedPre + result['tracks']['items'][1]['id'] + embedPost
            response['result 2'] = embed2
        if no_of_results >= 3:
            embed3 = embedPre + result['tracks']['items'][2]['id'] + embedPost
            response['result 3'] = embed3
        if no_of_results >= 4:
            embed4 = embedPre + result['tracks']['items'][3]['id'] + embedPost
            response['result 4'] = embed4
      
            
        return JsonResponse(response)
    
@login_required
def song_save(request):
    if is_ajax(request):
        data = json.load(request)
        print(data['embed'])
        print(data['page_id'])
        page = get_object_or_404(Page, id=data['page_id'])
        page.song_embed = data['embed']
        page.save()
        vid_required = False
        if bool(page.video_file) == False:
            vid_required = True
        response = {}
        response['vid_required'] =  vid_required
        print(response['vid_required'])
     
        return JsonResponse(response)
    
    return 

@login_required
def youtube_search(request):
    if is_ajax(request):
        data = json.load(request)
        page = get_object_or_404(Page, id=data['page_id'])
        page.vid_src = data['src']
        print('got to views ajax ')
        page.save()
        context = {}
        context['page'] = page
        context['user'] = request.user
        return JsonResponse(data)
    
        
@login_required
def complete_page(request, page_pk):
    page = get_object_or_404(Page, id=page_pk)
    context = {}
    
    current_user = request.user 
    
    if current_user != page.creator:
        return redirect(reverse('scrapbook:no_access'))

    context['user'] = current_user
    context['page'] = page
    return render(request,'scrapbook/complete_page.html', context)
            



@login_required
def page_view(request, page_pk):
    context = {}
    context['page'] = get_object_or_404(Page, pk=page_pk)
    context['scrapbook'] = context['page'].scrapbook
    today = date.today()
    context['day'] = today.strftime("%d %B, %Y")
    weekday = today.weekday() 
    if weekday == 1: 
        day = "Monday"
    elif weekday == 2:
        day = "Tuesday"
    elif weekday == 3:
        day = "Wednesday"
    elif weekday == 4:
        day = "Thursday"
    elif weekday == 5:
        day = "Friday"
    elif weekday == 6:
        day = "Saturday"
    elif weekday == 7:
        day = "Sunday"
        
    context['weekday'] = day  
    return render(request, 'scrapbook/page_view.html', context)

def no_access(request):
    return render(request, 'scrapbook/no_access.html')
    
def activities(request):
    context = {}
    return render(request, 'scrapbook/activities.html', context)

def help_page(request):
    context = {}
    return render(request, 'scrapbook/help_page.html', context)

def user_login(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            
                login(request, user)
                return redirect(reverse('scrapbook:index'))
           
        else:
            context['message'] = "Log in details incorrect"
            return render(request, 'scrapbook/login.html', context)
        
        
    return render(request, 'scrapbook/index.html', context)

@login_required
def add_note(request):
    if is_ajax(request):
        data = json.load(request)
        page = get_object_or_404(Page, id=data['page_pk'])
        new_note = TextNote(page=page, text=data['note'], creator=request.user)
        new_note.save()
        return JsonResponse(data)

@login_required
def view_notes(request, page_pk):
    page = get_object_or_404(Page, id=page_pk)
    
    
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('scrapbook:index'))
    
    
def account_recovery(request):
    context = {}
    return render(request, 'scrapbook/account_recovery.html', context)

def register(request):
    context = {}
    
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered = True
            
            if user is not None:
                login(request, user)
                return redirect(reverse('scrapbook:index'))

        else:
            print(user_form.errors)
    
    else:
        user_form = UserForm()
        
    context['user_form'] = user_form
    context['registered'] = registered      
    return render(request, 'scrapbook/register.html', context)


class AjaxTest(View):
    def get(self, request):
        return render(request, 'scrapbook/ajax_test.html')
    
def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'


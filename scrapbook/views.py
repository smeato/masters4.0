#from typing_extensions import Required
from asyncio import subprocess
from cgitb import reset
import os
from django.contrib.auth.decorators import login_required 
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

from masters.settings import SESSION_EXPIRE_AT_BROWSER_CLOSE 
from .models import Image, Page, Scrapbook, User, TextNote, Account
from scrapbook.forms import PageForm, RegForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect 
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, View
from django.views.generic.edit import CreateView, UpdateView
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.http import JsonResponse
import json 
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date
import random
from pathlib import Path
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q 
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib.auth import authenticate


# Create your views here.
def index(request): 
    context = {}

    
    if request.user.is_authenticated:
        user = request.user
        account = Account.objects.get(user=user)
        context['account'] = account
        
        context['books'] = []
        scrapbooks = Scrapbook.objects.filter(collaborators__id=user.id)
        if account.shares_scrapbook:
            for book in scrapbooks: 
                print(book)
                context['books'].append(book)
        
    return render(request, 'scrapbook/index.html', context)

# class based view for listing all pages in the given scrapbook
class ScrapbookView(LoginRequiredMixin, ListView):
    model = Page 
    
    template_name = 'scrapbook/scrapbook_view.html'
    
    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs['username'])
        self.scrapbook = get_object_or_404(Scrapbook, owner=self.user)
        
        self.viewable = False
        self.is_owner = False 
        
        if self.user == self.request.user:
            self.viewable = True 
            self.is_owner = True
        else:
            self.current_collaborator = self.scrapbook.collaborators.filter(username=self.request.user.username)
            if self.current_collaborator:
                self.viewable = True
                self.is_owner = False
            else:
                self.viewable = False
                return reverse_lazy('scrapbook:index')
        
        if not self.viewable:
            return reverse_lazy('scrapbook:no_access')
        return Page.objects.filter(scrapbook=self.scrapbook)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.username 
        context['scrapbook'] = self.scrapbook
        context['viewable'] = self.viewable 
        context['is_owner'] = self.is_owner
            
        return context

@login_required
def manage_sharing(request, username):
    owner = get_object_or_404(User, username=username)
    scrapbook = get_object_or_404(Scrapbook, owner=owner)
    if request.user != scrapbook.owner: 
        return redirect(reverse('scrapbook:index'))
    
    collaborators = []
    for c in scrapbook.collaborators.all():
        collaborators.append(c)
            
    context = {}
    context['collaborators'] = collaborators
    context['scrapbook'] = scrapbook
    
    
    return render(request,'scrapbook/manage_sharing.html', context)

@login_required
def delete_collaborator(request, username):
    owner = get_object_or_404(User, username=username)
    scrapbook = get_object_or_404(Scrapbook, owner=owner)
    if request.user != scrapbook.owner: 
        return redirect(reverse('scrapbook:index'))
    
    if is_ajax(request):
        data = json.load(request)
        user = User.objects.get(username=data['removed_collab'])
        print(user)
        print(scrapbook)
        scrapbook.collaborators.remove(user)
        scrapbook.save()
        return JsonResponse(data)
    return

@login_required
def add_collaborator(request, username):
    owner = get_object_or_404(User, username=username)
    scrapbook = get_object_or_404(Scrapbook, owner=owner)
    if request.user != scrapbook.owner: 
        return redirect(reverse('scrapbook:index'))
    
    if is_ajax(request):
        data = json.load(request)
        user = User.objects.get(username=data['add_collab'])
        if not user:
            error = {'message': "no user"}
            return JsonResponse(error)
        scrapbook.collaborators.add(user)
        scrapbook.save()
        return JsonResponse(data)
    
    
def add_scrapbook(request):
    context = {}
    context['user'] = request.user 
    context['account'] = Account.objects.get(user=context['user'])
    return render(request,'scrapbook/add_scrapbook.html', context)
    
    
def add_with_code(request):
    if is_ajax(request):
        response = {}
        data = json.load(request)
        code = data['code']
        
        try:
            scrapbook = Scrapbook.objects.get(share_code=code)
            response['user'] = scrapbook.owner.username
            scrapbook.collaborators.add(request.user)
            
        except Scrapbook.DoesNotExist:
            response['user'] = 'none'
            
        print(response['user'])
        return JsonResponse(response)

            

@login_required
def random_page(request, username):
    owner = User.objects.get(username=username)
    scrapbook = Scrapbook.objects.get(owner=owner)
    pages = Page.objects.filter(scrapbook=scrapbook)
    rand_page = random.choice(pages) 
    return redirect('scrapbook:page_view', page_pk=rand_page.id)



#                   PAGE CREATION 
##############################################################

class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    form_class = PageForm
    template_name = 'scrapbook/create_page.html'
    
    def get_success_url(self) -> str:
        return reverse_lazy('scrapbook:complete_page', kwargs={'page_pk': self.object.pk})
    
    def get_context_data(self, **kwargs):
        context = super(PageCreateView, self).get_context_data(**kwargs)
        context['username'] = self.request.user.username
        return context
    
    def form_valid(self, form): 
        form.instance.creator = self.request.user 
        form.instance.scrapbook = get_object_or_404(Scrapbook, owner=get_object_or_404(User, username=self.kwargs['username']))
        
        return super().form_valid(form)

        
@login_required
def complete_page(request, page_pk):
    page = get_object_or_404(Page, id=page_pk)
    context = {}
    
    current_user = request.user 
    
    if current_user != page.creator:
        return redirect(reverse('scrapbook:index'))

    context['user'] = current_user
    context['page'] = page
    return render(request,'scrapbook/complete_page.html', context)



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
        print(no_of_results)
        
        
        embedPre = "https://open.spotify.com/embed/track/"
        embedPost = "?utm_source=generator"
        
        response['resultsNum'] = no_of_results
        
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
    




#                   PAGE RELATED VIEWS
##################################################################

@login_required
def page_view(request, page_pk):
    page = get_object_or_404(Page, id=page_pk)
    scrapbook = page.scrapbook
    owner = scrapbook.owner

    # get list of scrapbooks this user has access to
    available = Scrapbook.objects.filter(collaborators__id=request.user.id) 
    
    # if user is not onwer or collaborator send to index
    if owner == request.user:
        pass
    elif scrapbook in available:
        pass
    else:
        return redirect(reverse('scrapbook:index'))
    
    context = {}
    context['page'] = get_object_or_404(Page, pk=page_pk)
    context['scrapbook'] = context['page'].scrapbook
    context['notes'] = []
    notes = TextNote.objects.filter(page = page)
    for note in notes:
        context['notes'].append(note)
  
    return render(request, 'scrapbook/page_view.html', context)


@login_required
def add_note(request):
    if is_ajax(request):
        data = json.load(request)
        page = get_object_or_404(Page, id=data['page_pk'])
        print(data['title'])
        new_note = TextNote(page=page, text=data['note'], creator=request.user, title=data['title'])
        new_note.save()
        return JsonResponse(data)


@login_required
def view_notes(request, page_pk):
    page = get_object_or_404(Page, id=page_pk)
    print(page_pk)
    context= {}
    context['notes'] = []
    notes = TextNote.objects.filter(page = page)
    for note in notes:
        context['notes'].append(note)
    context['page'] = page
    return render(request, 'scrapbook/view_notes.html', context)


class PageVideoUpdateView(UpdateView):
    model = Page 
    fields = ['video_file']
    template_name_suffix = '_video_update_form'
    
    def get_object(self, queryset= None):
        return Page.objects.get(id=self.kwargs['page_pk'])
    
    def get_context_data(self, **kwargs):
        context = super(PageVideoUpdateView, self).get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, id=self.kwargs['page_pk'])
        context['username'] = self.request.user.username
        return context
    
    def form_valid(self, form): 
        form.instance.page = get_object_or_404(Page, id=self.kwargs['page_pk'])
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('scrapbook:page_view', kwargs={'page_pk': self.object.id})
    
    
class PageImageUpdateView(UpdateView):
    model = Page 
    fields = ['image_file']
    template_name_suffix = '_image_update_form'
    
    def get_object(self, queryset= None):
        return Page.objects.get(id=self.kwargs['page_pk'])
    
    def get_context_data(self, **kwargs):
        context = super(PageImageUpdateView, self).get_context_data(**kwargs)
        context['page'] = get_object_or_404(Page, id=self.kwargs['page_pk'])
        context['username'] = self.request.user.username
        return context
    
    def form_valid(self, form): 
        form.instance.page = get_object_or_404(Page, id=self.kwargs['page_pk'])
        return super().form_valid(form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('scrapbook:page_view', kwargs={'page_pk': self.object.id})
    
    
    
#                       GENERAL SITE VIEWS (NOT USER SPECIFIC)
#####################################################################

def activities(request):
    context = {}
    return render(request, 'scrapbook/activities.html', context)


def help_page(request):
    context = {}
    return render(request, 'scrapbook/help_page.html', context)








#                      ACCOUNT REGISTRATION/LOGIN/RECOVERY VIEWS
#########################################################################
     
     

def register(request):
    context = {}
    
    registered = False
    
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        
        if reg_form.is_valid():
            user = reg_form.save()
            account = Account(user=user)
            user.set_password(user.password)
            #stores email in lowercase
            account.recovery_email = reg_form.cleaned_data['recovery_email']
            account.recovery_relationship = reg_form.cleaned_data['recovery_relationship']
            if reg_form.cleaned_data['role'] == 'owner':
                account.has_scrapbook = True
                account.shares_scrapbook = False
            elif reg_form.cleaned_data['role'] == 'contributor':
                account.has_scrapbook = False
                account.shares_scrapbook = True
            elif reg_form.cleaned_data['role'] == 'own/contrib':
                account.has_scrapbook = True
                account.shares_scrapbook = True
            
            account.save()
            new_scrapbook = Scrapbook(owner=user)
            new_scrapbook.save()
            user.save()
            
            registered = True
            
            if user is not None:
                login(request, user)
                return redirect(reverse('scrapbook:index'))

        else:
            context['errors'] = reg_form.errors
    
    else:
        reg_form = RegForm()
        
    context['form'] = reg_form
    context['registered'] = registered 
    if registered or request.user.is_authenticated:
        return redirect(reverse('scrapbook:index'))
    return render(request, 'scrapbook/register.html', context)
                                              

def user_login(request):
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
                login(request, user)
                if request.POST.get('remember_me'):
                    request.session.set_expiry(31536000)
                else:
                    request.session.set_expiry(0)
                return redirect(reverse('scrapbook:index'))
           
        else:
            context['message'] = "Log in details incorrect"
            return render(request, 'scrapbook/login.html', context)
    
        
    return render(request, 'scrapbook/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('scrapbook:index'))
    
    
def account_recovery(request):
    context = {}
    return render(request, 'scrapbook/account_recovery.html', context)

def check_username(request):
    if is_ajax(request):
        data = json.load(request)
        response = {}
        try:
            user = User.objects.get(username=data['username'])
            account = Account.objects.get(user=user)
            print(data['username'])
            response['relationship'] = account.recovery_relationship
        except User.DoesNotExist:
            response['relationship'] = 'none'
       
        print(response['relationship'])    
        return JsonResponse(response)


def password_reset_request(request):
    if request.method == "POST":
        reset_form = PasswordResetForm(request.POST)
        if reset_form.is_valid():
            # checks email in lowercase to be case insensitive
            data = reset_form.cleaned_data['email']
            users = User.objects.filter(Q(email=data))
            if users.exists():
                for user in users:
                    subject = "Password Reset for Scrapbook"
                    email_template_name = 'accounts/password_reset_email.txt'
                    info = {
                        'email': user.email, 
                        'domain': '192.168.1.103:8000',
                        'site_name': 'Scrapbook', 
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)), 
                        'user': user, 
                        'token': default_token_generator.make_token(user), 
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, info)
                    try: 
                        send_mail(subject, email, '2263320s@student.gla.ac.uk', [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
            return redirect(reverse('password_reset_done'))
    reset_form = PasswordResetForm() 
    return render(request, 'accounts/password_reset.html', context={'reset_form': reset_form})            
          
  




######## HELPER  ########## 
def is_ajax(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'



def no_access(request):
    return render(request, 'scrapbook/no_access.html')
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect

from .models import *

def index(request):
    sortlist = []
    for song in Song.objects.all():
        sortlist.append(song.id)
    if request.method == "POST":
        sort2 = []

        fav = request.POST.get('fav', False)
        title = request.POST["title"]
        singer = request.POST["singer"]
        genre = request.POST["genre"]

        if fav:
            for i in sortlist:
                if request.user in Song.objects.filter(id=i)[0].favorite.all():
                    sort2.append(i)
            sortlist = sort2
            sort2 = []

        if title:
                for i in sortlist:
                    if title.lower() in Song.objects.filter(id=i)[0].name.lower():
                        sort2.append(i)
                sortlist = sort2
                sort2 = []
        
        if singer:
            for i in sortlist:
                if singer == Song.objects.filter(id=i)[0].singer1 or singer == Song.objects.filter(id=i)[0].singer2:
                    sort2.append(i)
            sortlist = sort2
            sort2 = []

        if genre:
            for i in sortlist:
                if genre == Song.objects.filter(id=i)[0].genre:
                    sort2.append(i)
            sortlist = sort2
            sort2 = []

        return render(request, "songs_lyrics/index.html", {
            "currentUser": request.user,
            "sortlist": sortlist,
            "users": User.objects.count(),
            "songs": Song.objects.order_by('name')
        })

    return render(request, "songs_lyrics/index.html", {
            "currentUser": request.user,
            "sortlist": sortlist,
            "users": User.objects.count(),
            "songs": Song.objects.order_by('-favorite')
    })

def lyrics(request, song):
    if not Song.objects.filter(id=song):
        return HttpResponse("Song not found")

    if request.method == "POST":
        if request.POST.get('like'):
           mod = Song.objects.filter(id=song)[0]
           mod.favorite.add(request.user)
           mod.save()
           return render(request, "songs_lyrics/lyrics.html", {
                "currentUser": request.user,
                "song": Song.objects.filter(id=song)[0]
            })
        if request.POST.get('unlike'):
           mod = Song.objects.filter(id=song)[0]
           mod.favorite.remove(request.user)
           mod.save()
           return render(request, "songs_lyrics/lyrics.html", {
                "currentUser": request.user,
                "song": Song.objects.filter(id=song)[0]
            })

    if Song.objects.filter(id=song):
        return render(request, "songs_lyrics/lyrics.html", {
            "currentUser": request.user,
            "song": Song.objects.filter(id=song)[0]
        })

@csrf_protect
def add(request):#done
    if request.method == "POST":
        name = request.POST["name"]
        singer1 = request.POST["singer1"]
        singer2 = request.POST["singer2"]
        album = request.POST["album"]
        genre = request.POST["genre"]
        lang = request.POST["lang"]
        topic = request.POST["topic"]
        taal = request.POST["taal"]
        link = request.POST["link"]
        lyrics = request.POST["lyrics"]

        newsong = Song(
            creator = request.user,
            name=name,
            lyrics = lyrics,
            singer1 = singer1,
            singer2 = singer2,
            genre = genre,
            taal = taal,
            link = link[32:43],
            album = album,
            language = lang,
            topic = topic
        )
        newsong.save()
        return HttpResponseRedirect("/")
    return render(request, "songs_lyrics/add.html", {
        "currentUser": request.user
    })

@csrf_protect
def edit(request, song):
    if request.method == "POST":
        name = request.POST["name"]
        singer1 = request.POST["singer1"]
        singer2 = request.POST["singer2"]
        album = request.POST["album"]
        genre = request.POST["genre"]
        lang = request.POST["lang"]
        topic = request.POST["topic"]
        taal = request.POST["taal"]
        link = request.POST["link"]
        lyrics = request.POST["lyrics"]

        mod = Song.objects.filter(id=song)[0]
        mod.name=name
        mod.lyrics = lyrics
        mod.singer1 = singer1
        mod.singer2 = singer2
        mod.genre = genre
        mod.taal = taal
        mod.link = link[32:43]
        mod.album = album
        mod.language = lang
        mod.topic = topic
        mod.save()
        return HttpResponseRedirect(f"/{song}")
    return render(request, "songs_lyrics/edit.html", {
        "currentUser": request.user,
        "song": Song.objects.filter(id=song)[0]
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "songs_lyrics/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "songs_lyrics/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "songs_lyrics/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "songs_lyrics/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "songs_lyrics/register.html")

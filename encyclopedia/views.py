import re
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from . import util

from random import choice
from markdown2 import Markdown
md = Markdown()

entry_map = {i.lower():i for i in util.list_entries()}
list_entries = list(entry_map.keys())

def index(request):
    print(util.list_entries())
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title.lower() in list_entries:
        return render(request, 'encyclopedia/entry.html', {
            "title":entry_map[title.lower()],
            "entry":util.get_entry(title),
            "viewer_entry":md.convert(util.get_entry(title))
        })
    else:
        return render(request, 'encyclopedia/notfound.html')

def search(request):
    query = request.GET['q'].lower()
    
    if query in list_entries:
        return entry(request, query)

    matches = []
    for entry_title in list_entries:
        if re.search(query, entry_title) != None:
            matches.append(entry_map[entry_title])

    return results(request, matches)

def results(request, matches):
    return render(request, 'encyclopedia/results.html', {
        "matches":matches
    })

def newpage(request):
    return render(request, 'encyclopedia/newpage.html')

def show_newpage(request):
    global entry_map
    global list_entries
    if request.method == "POST":
        if request.POST['page-title'].lower() in list_entries:
            return render(request, 'encyclopedia/alreadyexists.html')
        else:
            print(type(request.POST['page-title']))
            util.save_entry(request.POST['page-title'],request.POST['page-content'])
            entry_map = {i.lower():i for i in util.list_entries()}
            list_entries = list(entry_map.keys())
            return entry(request, request.POST['page-title'])

def edit(request, title):
    return render(request, 'encyclopedia/edit.html', {
        "title":title,
        "entry":util.get_entry(title)
    })

def save_edit(request):
    if request.method == "POST":
        util.save_entry(request.POST['page-title'],request.POST['page-content'])
        entry_map = {i.lower():i for i in util.list_entries()}
        list_entries = list(entry_map.keys())
        return entry(request, request.POST['page-title'])

def random(request):
    title = choice(util.list_entries())
    return entry(request, title)
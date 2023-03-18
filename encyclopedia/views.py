import random
from django.shortcuts import render
import markdown2
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def convert_to_html(entry_name):
    md = markdown2.Markdown()
    entry = util.get_entry(entry_name)
    html = md.convert(entry) if entry else None
    return html

def entry(request, entry_name):
    html = convert_to_html(entry_name)
    if html is None:
        return render(request, "encyclopedia/wrong_entry.html", {
            "entryTitle": entry_name
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "entryTitle": entry_name
        })

def search(request):
    if request.method == 'POST':
        input = request.POST['q']
        html = convert_to_html(input)

        entries = util.list_entries()
        if input in entries:
            return render(request, "encyclopedia/entry.html", {
                "entry": html,
                "entryTitle": input
            })
        else:
            search_pages = []
            for entry in entries:
                if input.upper() in entry.upper():
                    search_pages.append(entry)
            return render(request, "encyclopedia/search.html", {
                "entries": search_pages,
            })

def create(request):
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        entries = util.list_entries()
        if title in entries:
            return render(request, "encyclopedia/already_exist.html", {
                "error": "Page already exists!"
            })
        elif title=="" or text=="":
            return render(request, "encyclopedia/already_exist.html", {
                "error": "Title and Text can't be empty!"
            })
        else :
            util.save_entry(title, text)
            html = convert_to_html(title)
            return render(request, "encyclopedia/entry.html", {
                "entry": html,
                "entryTitle": title
            })
    return render(request, "encyclopedia/create.html")

def edit(request, title):
    if request.method == 'POST':
        title = request.POST["title"]
        text = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "entry": text,
            "entryTitle": title
        })
    
def save_edit(request):
    if request.method == 'POST':
        input_title = request.POST['title']
        input_text = request.POST['text']
        util.save_entry(input_title, input_text)
        html = convert_to_html(input_title)
        return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "entryTitle": input_title
        })
    
def rand(request):
    arr = util.list_entries()
    entry_title = random.choice(arr)
    html = convert_to_html(entry_title)
    return render(request, "encyclopedia/entry.html", {
            "entry": html,
            "entryTitle": entry_title
        })

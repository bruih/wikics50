from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from . import util
from django import forms
from markdown2 import Markdown
import secrets



class whenCreatingNewForm(forms.Form):
    title = forms.CharField(label = "Title")
    text = forms.CharField(label = "", widget=forms.Textarea)
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newPage(request):
    if request.method == "POST":
        form = whenCreatingNewForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            edit = form.cleaned_data["edit"]
            listsOfTitles = util.list_entries()
            if edit is False and title in listsOfTitles:
                    return render(request,"alreadyExist.html", {
                        "form": whenCreatingNewForm(), 
                            })
            else:
                util.save_entry(title,text)
                return HttpResponseRedirect(reverse("entry", kwargs={"entry": title}))
        else:
            return render(request, "encyclopedia/entry.html", {
            "form": form,
                })
    else:
        return render(request, "encyclopedia/newPage.html", {
        "form": whenCreatingNewForm(),
            
        })  
def searchPage(request):
    title = request.GET.get('Q','')
    if util.get_entry(title) != None:
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': title })) 
    else:
        entries = []
        for entry in util.list_entries():
            if title.upper() in entry.upper():
                entries.append(entry)

        return render(request, "encyclopedia/search.html", {
        "entries": entries,
        "search": True,
        "title": title,

    })

def entryPage(request, entry ):
    getEntry = util.get_entry(entry)
    if getEntry == None:
        return render(request, "encyclopedia/noEntry.html", {
            "title" : entry,
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": Markdown().convert(getEntry),
            "title" : entry,
        })

def editPage(request, entry):
    if request.method == "GET":
        getEntry = util.get_entry(entry)
        if getEntry == None:
            return render(request, "encyclopedia/noEntry.html", {
            "title" : entry,
        })
        else:
            editForm = whenCreatingNewForm()
            editForm.fields["title"].initial = entry
            editForm.fields["title"].widget = forms.HiddenInput()
            editForm.fields["text"].initial = getEntry
            editForm.fields["edit"].initial = True
            return render(request, "encyclopedia/edit.html", {
                "form": editForm,
                "edit": editForm.fields["edit"].initial,
                "entryTitle": editForm.fields["title"]. initial,
        })
    else:
        editForm = whenCreatingNewForm(request.POST)
        if editForm.is_valid():
            text = editForm.cleaned_data["text"]
            util.save_entry(entry, text)
            getEntry = util.get_entry(entry)
            return render(request, "encyclopedia/entry.html", {
                "title": entry,
                "form": whenCreatingNewForm(),
                "entry": Markdown().convert(getEntry)
            })

def randomPage(request):
    listOfTitles = util.list_entries()
    random = secrets.choice(listOfTitles)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': random}))




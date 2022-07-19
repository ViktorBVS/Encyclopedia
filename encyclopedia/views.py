from django.shortcuts import render, redirect
from markdown2 import markdown
from django import forms
from random import choice
from . import util


class TextForm(forms.Form):
    f_page_name =  forms.CharField(label = 'Название', widget=forms.TextInput(attrs={'placeholder': 'Введите название', 'class':'form-control'}))
    f_page_content = forms.CharField(label = 'Содержание', widget=forms.Textarea(attrs={'placeholder': 'Заполните содержимое раздела', 'rows':'20', 'class':'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "header": "Содержание:"
    })

def viewpage(request, entry):
    page_content = util.get_entry(entry)
    if page_content == None:
       page_content = f"Страница {entry} не найдена." 
    else:
        return render(request, "encyclopedia/viewpage.html", {
        "page_name": entry,
        "page_content": markdown(page_content)
    })

def editpage(request):
     if request.method == "POST":
        title = request.POST.get('page_name')
        form = TextForm()
        form.fields['f_page_name'].initial = title
        form.fields['f_page_content'].initial = util.get_entry(title)
        return render(request, "encyclopedia/editpage.html", {
            "form": form,
            "edit": True 
        })

def savepage(request):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['f_page_name']
            body = form.cleaned_data['f_page_content'].encode('utf-8')
            edit = request.POST.get('edit')
            if edit == "True":
                util.save_entry(title, body)
        return render(request, "encyclopedia/viewpage.html", {
            "page_name": title,
            "page_content": markdown(body)
            })

def newpage(request):
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['f_page_name']
            body = form.cleaned_data['f_page_content'].encode('utf-8')
            edit = request.POST.get('edit')
            if edit != "True":
                entries = util.list_entries()
                for entry in entries:
                    if entry.lower() == title.lower():
                        return render(request, "encyclopedia/viewpage.html", {
                        "page_content": f"Страница {entry} уже существует.",
                        "page_name": entry
                        })
            util.save_entry(title, body)
            return render(request, "encyclopedia/viewpage.html", {
                "page_content": markdown(body),
                "page_name": title
                })
    return render(request, "encyclopedia/newpage.html", {
        "form": TextForm()
    })

def randompage(request):
    entry = choice(util.list_entries())
    return redirect(f"viewpage/{entry}/")

def searchpage(request):
    q = request.GET.get("q")
    entry_text = util.get_entry(q)
    if entry_text == None:
        entries = util.list_entries()
        search_entries = []
        for i in entries:
            if i.lower().find(q.lower()) != -1:
                search_entries.append(i)
        if len(search_entries) == 0:
            page_header = "Ничего не найдено"
        else:
            page_header = "Результат поиска"
        return render(request, "encyclopedia/index.html", {
            "entries": search_entries,
            "header": page_header
            })
    else:
        return render(request, "encyclopedia/viewpage.html", {
            "page_content": markdown(entry_text),
            "page_name": q,
            "edit": True
            })

def deletepage(request):
    if request.method == "POST":
        title = request.POST.get('page_name')
        util.delete_entry(title)
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "header": "Содержание:"
        })
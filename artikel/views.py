from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect,  get_object_or_404

from .forms import UserEditForm
from django import forms

from artikel.models import Kategori, Artikel
from artikel.forms import KategoriForms, ArtikelForms

from django.contrib.auth.models import Group
import requests

from rest_framework import viewsets
from artikel.models import Artikel
from .serializers import ArtikelSerializer

class ArtikelViewSet(viewsets.ModelViewSet):
    queryset = Artikel.objects.all()
    serializer_class = ArtikelSerializer

###############API#############
def artikel_external(request):
    response = requests.get("https://jsonplaceholder.typicode.com/posts")
    data = response.json()
    return render(request, 'external_list.html', {'artikel_list': data})

def artikel_external_detail(request, id):
    response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{id}")
    artikel = response.json()
    return render(request, 'external_detail.html', {'artikel': artikel})

# Create your views here.


def in_operator(user):
    get_user = user.groups.filter(name='Operator').count()
    if get_user > 0:
        return True
    else:
        return False

def in_author(user):
    get_user = user.groups.filter(name='Author').count()
    if get_user > 0:
        return True
    else:
        return False
    
def in_Contributor(user):
    get_user = user.groups.filter(name='Contributor').count()
    if get_user > 0:
        return True
    else:
        return False

################ user biasa ##################
@login_required( login_url='/auth-login')
def artikel_list(request):
    template_name = "dashboard/pengguna/artikel_list.html"
    artikel = Artikel.objects.filter(created_by=request.user)
    context = {
        "artikel":artikel,
    }
    return render(request, template_name, context)


@login_required( login_url='/auth-login')
def artikel_tambah(request):
    template_name = "dashboard/admin/artikel_forms.html"
    if request.method =="POST":
       forms = ArtikelForms(request.POST, request.FILES)
       if forms.is_valid():
           pub = forms.save(commit=False)
           pub.created_by = request.user
           pub.save()
           messages.success(request, 'berhasil tambah artikel')
           return redirect("artikel_list")   
    forms = ArtikelForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required( login_url='/auth-login')
def artikel_update(request, id_artikel):
    template_name = "dashboard/admin/artikel_forms.html"
    try:
        artikel = Artikel.objects.get(id=id_artikel, created_by=request.user)
    except:
        messages.success(request, "halaman yang minta tidak di temukan")
        return redirect("/dashboard")
    
    if request.method =="POST":
       forms = ArtikelForms(request.POST,  request.FILES, instance=artikel)
       if forms.is_valid():
           pub = forms.save(commit=False)
           pub.created_by = request.user
           pub.save()
           messages.success(request, 'berhasil melakukan update artikel')
           return redirect("artikel_list")
    
    forms = ArtikelForms(instance=artikel)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required( login_url='/auth-login')
def artikel_delete(request, id_artikel):
    artikel = get_object_or_404(Artikel, id=id_artikel, created_by=request.user)
    artikel.delete()
    return redirect("artikel_list")


################## admin ################
@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_list(request):
    template_name = "dashboard/admin/kategori_list.html"
    kategori = Kategori.objects.all()
    context = {
        "kategori":kategori

    }
    return render(request, template_name, context)

@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_tambah(request):
    template_name = "dashboard/admin/kategori_forms.html"
    if request.method =="POST":
       forms = KategoriForms(request.POST)
       if forms.is_valid():
           pub = forms.save(commit=False)
           pub.created_by = request.user
           pub.save()
           messages.success(request, "Berhasil tambah kategori")
           return redirect("admin_kategori_list")
    
    forms = KategoriForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_update(request, id_kategori):
    template_name = "dashboard/admin/kategori_forms.html"
    kategori = Kategori.objects.get(id=id_kategori)
    
    if request.method =="POST":
       forms = KategoriForms(request.POST, instance=kategori)
       if forms.is_valid():
           pub = forms.save(commit=False)
           pub.created_by = request.user
           pub.save()
           messages.success(request, "Berhasil melakukan update kategori")
           return redirect("admin_kategori_list")
    
    forms = KategoriForms(instance=kategori)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)


@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_kategori_delete(request, id_kategori):
    kategori = get_object_or_404(Kategori, id=id_kategori)
    kategori.delete()
    return redirect("admin_kategori_list")


#############Artikel#######

@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_list(request):
    template_name = "dashboard/admin/artikel_list.html"
    artikel = Artikel.objects.all()  
    context = {
        "artikel": artikel  
    }
    return render(request, template_name, context)

@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_tambah(request):
    template_name = "dashboard/admin/artikel_forms.html"
    if request.method =="POST":
       forms = ArtikelForms(request.POST, request.FILES)
       if forms.is_valid():
           pub = forms.save(commit=False)
           pub.created_by = request.user
           pub.save()
           messages.success(request, "Berhasil tambah artikel")
           return redirect("admin_artikel_list")   
    forms = ArtikelForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_update(request, id_artikel):
    template_name = "dashboard/admin/artikel_forms.html"
    artikel = Artikel.objects.get(id=id_artikel)
    
    if request.method =="POST":
       forms = ArtikelForms(request.POST,  request.FILES, instance=artikel)
       if forms.is_valid():
           pub = forms.save(commit=False)
           pub.created_by = request.user
           pub.save()
           messages.success(request, "Berhasil update artikel")
           return redirect("admin_artikel_list")
    
    forms = ArtikelForms(instance=artikel)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required( login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_delete(request, id_artikel):
    artikel = get_object_or_404(Artikel, id=id_artikel)
    artikel.delete()
    return redirect("admin_artikel_list")



################################ Managemet User Oleh Operator ################################ 

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_list(request):
    template_name ="dashboard/admin/artikel_list.html"
    artikel = Artikel.objects.all()
    context = {
        "artikel":artikel
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_tambah(request):
    template_name = "dashboard/admin/artikel_forms.html"
    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil tambah artikel')
        return redirect(admin_artikel_list)
    forms = ArtikelForms()
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_update(request, id_artikel):
    template_name = "dashboard/admin/artikel_forms.html"
    artikel = Artikel.objects.get(id=id_artikel)
    
    if request.method == "POST":
        forms = ArtikelForms(request.POST, request.FILES, instance=artikel)
        if forms.is_valid():
            pub = forms.save(commit=False)
            pub.created_by = request.user
            pub.save()
            messages.success(request, 'berhasil melakukan update artikel')
        return redirect(admin_artikel_list)
    
    forms = ArtikelForms(instance=artikel)
    context = {
        "forms":forms
    }
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_artikel_delete(request, id_artikel):
    try:
        Kategori.objects.get(id=id_artikel).delete()
    except:
        pass
    
    return redirect(admin_artikel_list)


##################################### Management User Oleh Operator ##########################################

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_management_user_list(request):
    template_name = "dashboard/admin/user_list.html"
    daftar_user = User.objects.all()
    context = {
        "daftar_user":daftar_user
    } 
    return render(request, template_name, context)

@login_required(login_url='/auth-login')
@user_passes_test(in_operator, login_url='/')
def admin_management_user_edit(request, user_id):
    template_name = 'dashboard/admin/user_edit.html'
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        is_staff = request.POST.get("is_staff")
        groups_checked = request.POST.getlist("groups")

        user.first_name = first_name
        user.last_name = last_name
        user.is_staff = True if is_staff == "on" else False
        user.groups.set(Group.objects.filter(id__in=groups_checked))
        user.save()

        messages.success(request, f"Berhasil update user {user.username}")
        return redirect('admin_management_user_list')

    all_groups = Group.objects.all()
    group_user = [group.name for group in user.groups.all()]

    context = {
        'user': user,
        'all_groups': all_groups,
        'group_user': group_user,
    }
    return render(request, template_name, context)
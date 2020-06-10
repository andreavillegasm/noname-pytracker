from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserForm, ProfileForm, CommentRawProduction, CommentForm
from .models import Invoices, Projects, Clients, Tasks, Timers, Comments,Profile

# for import date and time
from _datetime import datetime
from django.utils import timezone
from django.template import defaultfilters
from django.utils.dateparse import parse_date



@login_required
def home(request):
    return render(request, 'PyTraker/index.html')


def sign_up(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile_form = profile_form.save(commit=False)
            profile_form.user = user
            profile_form.save()
            userN = user_form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + userN)
            return redirect('login')
    else:
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
    return render(request, 'PyTraker/sign_up.html', {'user_form': user_form, 'profile_form': profile_form})


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}

    return render(request, 'PyTracker/login.html', context)


def log_out(request):
    if request.method == "POST":
        logout(request)

    messages.info(request, "Logged out successfully!")
    return redirect('login')


# Invoice View

def invoice(request, invoices_id):
    obj = Invoices.objects.get(id=invoices_id)
    tasks = Tasks.objects.filter(projectID_id=obj.projectID)
    context = {
        'invoice_id': obj.id,
        'client_name': obj.projectID.clientID.name,
        'client_email': obj.projectID.clientID.email,
        'client_phone': obj.projectID.clientID.phone,
        'user_fname': obj.userID.firstname,
        'user_lname': obj.userID.lastname,
        'user_email': obj.userID.email,
        'user_phone': obj.userID.phonenumber,
        'date_created': obj.dateCreated,
        'date_due': obj.dueDate,
        'hourly_rate': obj.projectID.payRate,
        'tasks_list': tasks,
    }
    return render(request, "PyTraker/invoice.html", context)


#comment page
def comment_view(request):
    obj = Comments.objects.all()
    context ={
        'object': obj
    }
    return render(request, "PyTraker/comment_form.html",context)

def comment_detail_view(request, comment_id):
    obj = Comments.objects.get(id=comment_id)
    context = {
        'comment': obj
    }
    return render(request, "PyTraker/comment_detail.html", context)

def comment_create_view(request):
    if request.method == "POST":
        # new_comment = CommentForm()
        new_comment_user = request.POST.get('user')
        new_comment_comment = request.POST.get('comment')
        new_comment_comment_date = parse_date(request.POST.get('comment_date'))
        # print(parse_date(request.POST.get('comment_date')))
        Comments.objects.create(user=new_comment_user,comment=new_comment_comment,comment_date=new_comment_comment_date)
    comments = Comments.objects.all()
    date = datetime.now()
    userid = Profile.objects.all()
    m = User.objects.all()
    i = m.user_id
    context = {
        'i':i,
        'userid': userid,
        'object': comments,
        'time' : defaultfilters.date(date, "Y-m-d")
    }
    return render(request, "PyTraker/comment_form.html", context)

def comment_delete(request, comment_id):
    obj = get_object_or_404(Comments, id=comment_id)
    if request.method == "POST":
        obj.delete()
        return redirect('../../')
    context = {
        "object":obj
    }
    return render(request, "PyTraker/comment_delete.html", context)
#Task Views
def tasklist(request):
    all_task_list = Tasks.objects.order_by("name")
    context = {"all_task_list": all_task_list}
    return render(request, "PyTraker/tasklist.html", context)


def task_detail(request, tasks_id):
    tasks = get_object_or_404(Tasks, pk=tasks_id)
    return render(request, 'PyTraker/task_detail.html', {'tasks': tasks})

#Project Views
def projects(request):
    all_projects = Projects.objects.order_by("name")
    context = {"all_projects": all_projects}
    return render(request, "PyTraker/projects.html", context)


def project_detail(request, projects_id):
    project = get_object_or_404(Projects, pk=projects_id)
    return render(request, 'PyTraker/project_detail.html', project)


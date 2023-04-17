from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.utils import timezone
from .forms import TaskForms
from .models import Task

# Create your views here.


def home(request):
    return render(request, 'home.html', {
        'title': 'HOME'
    })


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'title': 'SIGNUP',
            'form': UserCreationForm
        })
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe en la base de datos.'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                'error': 'Las contraseñas no iguales.'
            })

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {
        'title': 'TASKS',
        'tasks': tasks
    })

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'title': 'TASKS',
        'tasks': tasks
    })

@login_required
def createTask(request):
    if request.method == 'GET':
        return render(request, 'task_create.html', {
            'form': TaskForms
        })
    else:
        try:
            form = TaskForms(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': form,
                'error': 'Algo esta pasando por el backend'
            })

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        # task = Task.objects.get(pk=task_id) si buscamos un id que no esta el server cae. Hay otra forma mejor.
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForms(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else: 
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForms(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
            'task': task,
            'form': form,
            'error': 'ERROR - La tarea no se pudo actualizar.'
        })

@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

@login_required    
def singout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta.'
            })
        else:
            login(request, user)
            return redirect('tasks')

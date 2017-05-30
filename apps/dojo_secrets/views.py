from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Secret
from django.db.models import Count
def index(request):
    return render(request, 'index.html')

def register(request):
    postData = {
    'f_n': request.POST['f_n'],
    'l_n': request.POST['l_n'],
    'eml': request.POST['eml'],
    'pw': request.POST['pw'],
    'c_pw': request.POST['c_pw'],
    }
    result = User.objects.register(postData)
    if result[0] == False:
        for error in User.objects.register(postData)[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/')
    else:
        request.session['user_id'] = result[1]
        return redirect('/secrets')
def login(request):
    postData = {
    'eml': request.POST['eml'],
    'pw': request.POST['pw'],
    }
    if User.objects.login(postData)[0] == False:
        for error in User.objects.login(postData)[1]:
            messages.add_message(request, messages.INFO, error)
        return redirect('/')
    else:
        request.session['user_id'] = User.objects.login(postData)[1]
        return redirect('/secrets')
def logout(request):
    request.session['user_id'] = None
    return redirect('/')

def secrets(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        messages.add_message(request, messages.INFO, 'Please login first!')
        return redirect('/')
    secrets = Secret.objects.annotate(num_likes=Count('likes')).order_by('-id')[0:5]
    context = {
    'user' : User.objects.get(id=user_id),
    'secrets': secrets
    }
    return render(request, 'secrets.html', context)

def post(request):
    content=request.POST.get('secret', False)
    user_id = request.session.get('user_id', False)
    result = Secret.objects.validate(content, user_id)
    for info in result[1]:
        messages.add_message(request, messages.INFO, info)
    return redirect('/secrets')

def like(request, secret_id, fromurl):
    user_id = request.session.get('user_id', False)
    result = Secret.objects.like(secret_id, user_id)
    for info in result[1]:
        messages.add_message(request, messages.INFO, info)
    if fromurl == 'sec' :
        return redirect('/secrets')
    else:
        return redirect('/secrets/')

def delete(request, secret_id, fromurl):
    user_id = request.session.get('user_id', False)
    result = Secret.objects.delete(secret_id, user_id)
    for info in result[1]:
        messages.add_message(request, messages.INFO, info)
    if fromurl == 'sec' :
        return redirect('/secrets')
    else:
        return redirect('/secrets/')

def pop_secrets(request):
    user_id = request.session.get('user_id', False)
    if not user_id:
        messages.add_message(request, messages.INFO, 'Please login first!')
        return redirect('/')
    secrets = Secret.objects.annotate(num_likes=Count('likes')).order_by('num_likes')
    context = {
    'user' : User.objects.get(id=user_id),
    'secrets': secrets
    }   
    return render(request, 'pop_secrets.html', context)








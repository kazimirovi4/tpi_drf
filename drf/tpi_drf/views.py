from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message, ChatList, UserProfile
from .forms import MessageForm, UserRegistrationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages
from datetime import datetime

from django.http import Http404


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user, name=user.username)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Аккаунт для {username} успешно создан!')
            return redirect('chat_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def user_chat_list(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    chats = Chat.objects.filter(user=user_profile)

    if not chats.exists():

        return render(request, 'user_chat_list.html', {'chats': chats, 'no_chats': True})

    return render(request, 'user_chat_list.html', {'chats': chats, 'no_chats': False})

@login_required
def chat_detail(request, chat_uuid):
    try:
        chat = get_object_or_404(Chat, uuid=chat_uuid)
        if request.user.is_staff or chat.user.user == request.user:
            messages = Message.objects.filter(chat=chat).order_by('timestamp')
            form = MessageForm(request.POST or None)
            if request.method == 'POST':
                if form.is_valid():
                    try:
                        message = form.save(commit=False)
                        message.chat = chat
                        message.sender = UserProfile.objects.get(user=request.user)
                        message.timestamp = datetime.now()
                        message.save()
                        messages.success(request, "Сообщение успешно отправлено.")
                        return redirect('chat_detail', chat_uuid=chat.uuid)
                    except Exception as e:
                        messages.error(request, f"Ошибка отправки сообщения: {str(e)}")
                else:
                    messages.error(request, "Форма сообщения недействительна.")
            return render(request, 'chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})
        else:
            messages.error(request, "Ошибка подключения к чату. Нет доступа.")
            return redirect('chat_list')
    except Http404:
        messages.error(request, "Чат не найден.")
        return redirect('chat_list')
    except Exception as e:
        messages.error(request, f"Ошибка загрузки истории сообщений: {str(e)}")
        return redirect('chat_list')

@login_required
def admin_chat_list(request):
    if not request.user.is_staff:
        return redirect('chat_list')
    chat_lists = ChatList.objects.filter(admin=request.user)
    return render(request, 'admin_chat_list.html', {'chat_lists': chat_lists})

@login_required
def admin_chat_detail(request, chat_uuid):
    if not request.user.is_staff:
        messages.error(request, "Ошибка авторизации. Доступ запрещен.")
        return redirect('user:user_chat_list')

    try:
        chat = get_object_or_404(Chat, uuid=chat_uuid)
        messages = Message.objects.filter(chat=chat).order_by('timestamp')
        form = MessageForm(request.POST or None)
        if request.method == 'POST':
            if form.is_valid():
                try:
                    message = form.save(commit=False)
                    message.chat = chat
                    message.sender = UserProfile.objects.get(user=request.user)
                    message.timestamp = datetime.now()
                    message.save()
                    messages.success(request, "Сообщение успешно отправлено.")
                    return redirect('admin_chat_detail', chat_uuid=chat.uuid)
                except Exception as e:
                    messages.error(request, f"Ошибка отправки сообщения: {str(e)}")
            else:
                messages.error(request, "Форма сообщения недействительна.")
        return render(request, 'admin_chat_detail.html', {'chat': chat, 'messages': messages, 'form': form})
    except Http404:
        messages.error(request, "Чат не найден.")
        return redirect('admin_chat_list')
    except Exception as e:
        messages.error(request, f"Ошибка загрузки истории сообщений: {str(e)}")
        return redirect('admin_chat_list')


@login_required
def create_chat(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)

    open_chat = Chat.objects.filter(user=user_profile, status='open').first()

    if open_chat:
        return redirect('chat_detail', chat_uuid=open_chat.uuid)

    new_chat = Chat.objects.create(user=user_profile, status='open', created=datetime.now())

    admin_user = User.objects.filter(is_staff=True).first()
    if admin_user:
        ChatList.objects.create(chat=new_chat, admin=admin_user)

    return redirect('chat_detail', chat_uuid=new_chat.uuid)


@login_required
def close_chat(request, chat_uuid):
    chat = get_object_or_404(Chat, uuid=chat_uuid)
    if request.user.is_staff or chat.user.user == request.user:
        chat.status = 'closed'
        chat.closed = datetime.now()
        chat.save()
        return redirect('chat_list' if not request.user.is_staff else 'admin_chat_list')
    return redirect('chat_detail', chat_uuid=chat_uuid)


@login_required
def update_status(request, status):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if status == 'online':
        user_profile.is_online = True
    elif status == 'offline':
        user_profile.is_online = False
    user_profile.save()
    return redirect('home')


def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)
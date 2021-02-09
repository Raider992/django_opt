from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView

from django.core.mail import send_mail
from django.conf import settings

from authapp.models import User
from cartapp.models import Cart


def send_verify_email(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    subject = f'Подтверждение регистрации {user.username}'
    message = f'Для подтверждения регистрации пройдите по ссылке: {settings.DOMAIN}{verify_link}'

    return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
    try:
        user = User.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verify.html')
    except Exception as ex:
        return HttpResponseRedirect(reverse('main'))


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True
    success_url = 'main'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs)
        context.update({'title': 'авторизация'})
        context.update({'style_link': 'css/auth-admin.css'})
        context.update({'script_link': 'js/auth-admin.js'})
        return context


# Не вижу смысла ради двух строчек создавать класс, который съест больше памяти, чем функция
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


class UserSignUpView(CreateView):
    model = User
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')
    form_class = UserRegisterForm

    def form_valid(self, form, **kwargs):
        super().form_valid(form)
        user = form.save()
        send_verify_email(user)

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UserSignUpView, self).get_context_data(**kwargs)
        context.update({'title': 'регистрация'})
        return context


# class UserProfileView(UpdateView):
#     model = User
#     template_name = 'authapp/profile.html'
#     success_url = reverse_lazy('auth:profile')
#     form_class = UserProfileForm
#
#
#     def get_context_data(self, request, **kwargs):
#         context = super(UserProfileView, self).get_context_data(**kwargs)
#         context.update({'title': 'профиль'})
#         context.update({'style_link': 'css/profile.css'})
#
#         carts = Cart.objects.filter(user=request.user)
#         context.update({'carts': carts})
#         return context

def profile(request):
    if request.method == "POST":
        form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
        profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))

    else:
        form = UserProfileForm(instance=request.user)
        profile_form = UserProfileEditForm(instance=request.user.userprofile)

    carts = Cart.objects.filter(user=request.user)

    context = {
        'title': 'профиль',
        'style_link': 'css/profile.css',

        'carts': carts,

        'form': form,

        'profile_form': profile_form
    }

    return render(request, 'authapp/profile.html', context)

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('main'))
#
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'title': 'авторизация',
#         'style_link': 'css/auth-admin.css',
#         'script_link': 'js/auth-admin.js',
#
#         'form': form
#     }
#
#     return render(request, 'authapp/login.html', context)


# def register(request):
#     if request.method == "POST":
#         reg_form = UserRegisterForm(data=request.POST)
#         if reg_form.is_valid():
#             reg_form.save()
#             messages.success(request, 'Вы успешно зарегистрировались')
#             return HttpResponseRedirect(reverse('authapp:login'))
#     else:
#         reg_form = UserRegisterForm()
#
#     context = {
#         'title': 'регистрация',
#         'style_link': 'css/auth-admin.css',
#         'script_link': 'js/auth-admin.js',
#
#         'form': reg_form
#     }
#
#     return render(request, 'authapp/register.html', context)

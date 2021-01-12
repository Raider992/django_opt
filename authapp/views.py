from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import UserLoginForm, UserRegisterForm, UserProfileForm
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView

from authapp.models import User
from cartapp.models import Cart


class UserLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'authapp/login.html'
    redirect_authenticated_user = True
    success_url = 'main'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data(**kwargs);
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
    success_url = reverse_lazy('authapp:login')
    form_class = UserRegisterForm

    def get_context_data(self, **kwargs):
        context = super(UserSignUpView, self).get_context_data(**kwargs)
        context.update({'title': 'регистрация'})
        context.update({'style_link': 'css/auth-admin.css'})
        context.update({'script_link': 'js/auth-admin.js'})
        return context


class UserProfileView(UpdateView):
    model = User
    template_name = 'authapp/profile.html'
    success_url = reverse_lazy('auth:profile')
    form_class = UserProfileForm

    def get_context_data(self, request, **kwargs):
        context = super(UserProfileView, self).get_context_data(**kwargs)
        context.update({'title': 'профиль'})
        context.update({'style_link': 'css/profile.css'})

        carts = Cart.objects.filter(user=request.user)
        context.update({'carts': carts})
        return context

# def profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(data=request.POST, files=request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     carts = Cart.objects.filter(user=request.user)
#
#     context = {
#         'title': 'профиль',
#         'style_link': 'css/profile.css',
#
#         'carts': carts,
#
#         'form': form
#     }
#
#     return render(request, 'authapp/profile.html', context)

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

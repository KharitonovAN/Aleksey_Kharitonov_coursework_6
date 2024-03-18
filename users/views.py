from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib.auth.views import (
    LoginView as
    BaseLoginView,
    PasswordResetView,
    PasswordResetConfirmView
)
from users.models import User
from users.services import send_verify_email
from users.forms import (
    RegisterForm,
    UserForgotPasswordForm,
    UserSetNewPasswordForm,
    UserProfileForm,
    ModeratorForm
)


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


def logout_user(request):
    logout(request)
    return redirect('main_app:home')


class RegisterUserView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('main_app:home')

    def form_valid(self, form):
        if form.is_valid():
            user = form.save()
            send_verify_email(user)
        return super().form_valid(form)


class ConfirmVerifyUser(View):
    def get(self, request, uuid):
        try:
            user = User.objects.get(field_uuid=uuid)
            user.is_active = True
            user.save()
            users_group, created = Group.objects.get_or_create(name='Users')
            if created:
                permissions = Permission.objects.filter(
                    codename__in=['add_client', 'change_client', 'view_client', 'delete_client',
                                  'view_mailingsettings', 'add_mailingsettings', 'change_mailingsettings',
                                  'delete_mailingsettings',
                                  'add_mailingmessage', 'change_mailingmessage', 'view_mailingmessage',
                                  'delete_mailingmessage',
                                  'view_newsletter', 'change_user', 'delete_user']
                )
                users_group.permissions.set(permissions)
            user.groups.add(users_group)
            user.save()
            return render(request, 'users/confirm_register.html')
        except User.DoesNotExist:
            return render(request, 'users/error_register.html')


class UserForgotPasswordView(PasswordResetView):
    form_class = UserForgotPasswordForm
    template_name = 'users/user_password_reset.html'
    success_url = reverse_lazy('main_app:home')
    success_message = 'Письмо для восстановления пароля отправлено на ваш email'
    subject_template_name = 'users/password_subject_reset_mail.txt'
    email_template_name = 'users/password_reset_mail.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetNewPasswordForm
    template_name = 'users/user_password_set_new.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Пароль успешно изменен'


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile_user')
    form_class = UserProfileForm

    def get_object(self, queryset=None):
        return self.request.user


@login_required
def get_user_profile(request):
    user = User.objects.get(id=request.user.pk)
    return render(request, 'users/user_profile.html', {"user": user})


@login_required
def delete_self_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect('main_app:home')


class ModeratorListView(LoginRequiredMixin, ListView):
    model = User

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.groups.filter(name='Moderator').exists():
            queryset = queryset.filter(groups__name='Users')
            return queryset
        if self.request.user.is_superuser:
            return queryset.all()


class ModeratorUpdateUserView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = User
    form_class = ModeratorForm
    permission_required = 'users.set_active'

    def get_object(self, *args, **kwargs):
        user = super().get_object(*args, **kwargs)
        if (self.request.user.has_perm(self.permission_required) and self.request.user.is_staff) \
                or self.request.user.is_superuser:
            return user
        raise PermissionError

    def form_valid(self, form):
        if form.has_changed():
            user = self.get_object()
            if user.is_active:
                user.is_active = False
            user.is_active = True
            user.save()
            form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('users:all_user')

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    UpdateView,
    DetailView,
    DeleteView
)
from blogpost.models import BlogPost
from config import settings
from main_app.forms import (
    MailingMessageForm,
    MailingSettingsForm,
    ClientForm,
    ModeratorMailingSettingsForm
)
from main_app.models import (
    Client,
    MailingSettings,
    MailingMessage,
    MailingLog
)
from main_app.services import get_client_cache, get_mailingsettings_cache


class IndexView(TemplateView):
    template_name = 'main_app/home.html'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['count_mailing'] = MailingSettings.objects.count()  # кол-во рассылок
        context_data['active_mailing'] = MailingSettings.objects.filter(is_active=True).count()  # кол-во активных рассылок
        context_data['uniqe_clients'] = Client.objects.distinct().count()  # кол-во уникальных клиентов
        context_data['blog_content'] = BlogPost.objects.all().order_by('?')[:3]  # случайные статьи из блога
        return context_data


class ClientListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Client
    permission_required = 'main_app.view_client'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if settings.CACHE_ENABLED:
            context_data['client_list'] = get_client_cache(user=self.request.user)
        else:
            context_data['client_list'] = Client.objects.filter(owners=self.request.user)
        return context_data


class ClientCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    permission_required = 'main_app.add_client'

    def get_success_url(self):
        return reverse('main_app:client_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owners = self.request.user  # владелец
            self.object.save()
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    permission_required = 'main_app.change_client'

    def get_success_url(self):
        return reverse('main_app:client_list')

    def get_object(self, *args, **kwargs):
        client = super().get_object(*args, **kwargs)
        if client.owners == self.request.user:  # проверка на владельца
            return client
        return reverse('main_app:client_list')

    def form_valid(self, form):
        if self.object.owners == self.request.user:
            self.object.owners = self.request.user
            self.object.save()
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Client
    permission_required = 'main_app.view_client'


class ClientDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main_app:client_list')
    permission_required = 'main_app.delete_client'


class MailingSettingsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingSettings
    permission_required = 'main_app.view_mailingsettings'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if settings.CACHE_ENABLED:
            context_data['mailingsettings_list'] = get_mailingsettings_cache(user=self.request.user)
        else:
            if self.request.user.groups.filter(name='Moderator').exists() or self.request.user.is_superuser:
                context_data['mailingsettings_list'] = MailingSettings.objects.all()
            else:
                context_data['mailingsettings_list'] = MailingSettings.objects.filter(owners=self.request.user)
        return context_data


class MailingSettingsDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingSettings
    permission_required = 'main_app.view_mailingsettings'

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        clients = MailingSettings.objects.get(id=self.kwargs.get('pk')).client.all()
        context_data['clients'] = clients
        return context_data


class MailingSettingsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    permission_required = 'main_app.add_mailingsettings'

    def get_success_url(self):
        return reverse('main_app:mails_list')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owners = self.request.user
            self.object.save()
        return super().form_valid(form)


class MailingSettingsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingSettings
    permission_required = 'main_app.change_mailingsettings'

    def get_success_url(self):
        return reverse('main_app:mails_list')

    def get_form_class(self):
        if (self.request.user.has_perm('main_app.set_active') and self.request.user.is_staff) \
                or self.request.user.is_superuser:
            return ModeratorMailingSettingsForm
        return MailingSettingsForm

    def form_valid(self, form):
        if self.object.owners == self.request.user:
            self.object.owners = self.request.user
            self.object.save()
            if form.is_valid():
                self.object = form.save()
                self.object.save()
        return super().form_valid(form)


class MailingSettingsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingSettings
    success_url = reverse_lazy('main_app:mails_list')
    permission_required = 'main_app.view_mailingsettings'


class PersonalAreaView(LoginRequiredMixin, TemplateView):
    template_name = 'main_app/personal_area.html'


class MailingMessageCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = MailingMessage
    form_class = MailingMessageForm
    permission_required = 'main_app.add_mailingmessage'

    def get_success_url(self):
        return reverse('main_app:personal_area')

    def form_valid(self, form):
        if form.is_valid():
            self.object = form.save()
            self.object.owners = self.request.user
            self.object.save()
            return super().form_valid(form)


class MailingMessageUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = MailingMessage
    form_class = MailingMessageForm
    permission_required = 'main_app.change_mailingmessage'

    def get_success_url(self):
        return reverse('main_app:personal_area')

    def form_valid(self, form):
        if self.object.owners == self.request.user:
            self.object.owners = self.request.user
            self.object.save()
        if form.is_valid():
            self.object = form.save()
            self.object.save()
        return super().form_valid(form)


class MailingMessageListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = MailingMessage
    permission_required = 'main_app.view_mailingmessage'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(owners=self.request.user)  # владелец
        return queryset


class MailingMessageDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = MailingMessage
    permission_required = 'main_app.view_mailingmessage'


class MailingMessageDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = MailingMessage
    success_url = reverse_lazy('main_app:list_messages')
    permission_required = 'main_app.delete_mailingmessage'


class MailingLogListView(LoginRequiredMixin, ListView):
    model = MailingLog


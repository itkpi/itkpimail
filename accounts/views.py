from accounts.forms import UserForm
from customauth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView, DetailView, UpdateView


class HomeView(TemplateView):
    template_name = 'home.html'


class AccountView(DetailView):
    template_name = 'accounts/account.html'
    model = User

    def get_object(self, queryset=None):
      return self.model.objects.get(pk=self.request.user.pk)


class AccountEditView(UpdateView):
    form_class = UserForm
    template_name = 'accounts/account_edit.html'
    model = User

    def get_object(self, queryset=None):
      return self.model.objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse('account')

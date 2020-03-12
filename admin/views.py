from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Domain, Invoice, Transfer
from users.models import CustomUser
import whois
import socket
from django.urls import reverse
from .forms import DeleteForm
from django.contrib.auth.hashers import check_password
# Create your views here.


class AdminView(TemplateView, LoginRequiredMixin):
    template_name = "admin/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domains = Domain.objects.filter(user=self.request.user)
        invoices = Invoice.objects.filter(user=self.request.user)
        context["invoices"] = invoices
        context["active"] = domains.filter(status='active')
        context["pending"] = domains.filter(status='pending')
        context["expired"] = domains.filter(status='expired')
        context["transferred"] = domains.filter(status='transferred')

class InvoiceView(ListView, LoginRequiredMixin):
    template_name = Invoice
    template = "admin/pages/invoices.html"
    object_name = "invoices"

    def get_queryset(self, **kwargs):
        return Invoice.objects.filter(user=self.request.user)

class ListView(ListView, LoginRequiredMixin):
    model = Domain
    template_name = "admin/pages/domainlist.html"
    object_name = "domains"

    def get_queryset(self, **kwargs):
        domains = Domain.objects.filter(user=self.request.user)
        return domains.filter(status=self.kwargs['category'])

class RegisteredDomainView(ListView, LoginRequiredMixin):
    model = Domain
    template_name = "admin/pages/registered.html"
    object_name = "domains"

    def get_queryset(self, **kwargs):
        domains = Domain.objects.filter(user=self.request.user)
        return domains

class TransferDomainView(CreateView, LoginRequiredMixin):
    model = Transfer
    fields = ['domain_name', 'note']
    template_name = "admin/pages/transfer.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TransferDomainView, self).form_valid(form)


class UpdateAccountView(UpdateView, LoginRequiredMixin):
    model = CustomUser
    template_name = "admin/pages/account_edit.html"
    fields = ['first_name', 'last_name', 'email']
    redirect = "/account/"

    def get_success_url(self):
        return reverse('index')


def SearchDomain(request):
    if request.method == 'POST':
        domain = request.POST['domain']
        if domain:
            if domain.find(".zw"):
                try:
                    if socket.gethostbyname(domain) == None:
                        return render(request,'admin/pages/search.html', {'av': 'true', 'dom': domain})
                    else:
                        return render(request, 'admin/pages/search.html', {'av': 'false', 'dom': domain})
                except:
                    return render(request, 'admin/pages/search.html', {'av': 'true', 'dom': domain})
            else:
                w = whois.whois(domain)
                if w['status'] == None:
                    return render(request, 'admin/pages/search.html', {'av': 'true', 'dom': domain})
                else:
                    return render(request, 'admin/pages/search.html', {'av': 'false', 'dom': domain})
        else:
            return render(request, 'admin/pages/search.html')
    else:
        return render(request, 'admin/pages/search.html')

def delete_user(request):
    if request.method == "POST":
        form = DeleteForm()
    else:
        form = DeleteForm(request.POST)
        if form.is_valid():
            user = request.user
            r_pass = user.password
            password = form.cleaned_data['password']
            match = check_password(password, r_pass)
            if match:
                context = {}
                try:
                    user = request.user
                    user.is_active = False
                    user.save()
                    return reverse('home')
                except User.DoesNotExist:
                    context['msg'] = 'Sorry the account does not exist'
                    return reverse('home')
            else:
                context['msg'] = 'Wrong Password, Account cannot be deleted'
                return render(request, 'account/delete_account.html', context=context)
    return render(request, "account/delete_account.html", {'form': form})



class PaymentView(TemplateView):
    template_name = 'admin/pages/payments.html'

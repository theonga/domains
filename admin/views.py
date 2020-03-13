from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Domain, Invoice, Transfer, Price, Payment
from users.models import CustomUser
import whois
import socket
from paynow import Paynow
from django.urls import reverse
from .forms import DeleteForm
from django.contrib.auth.hashers import check_password
# Create your views here.


class AdminView(LoginRequiredMixin, TemplateView):
    template_name = "siteadmin/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domains = Domain.objects.filter(user=self.request.user)
        context["active"] = domains.filter(status='active')
        context["pending"] = domains.filter(status='pending')
        context["expired"] = domains.filter(status='expired')
        context["transferred"] = domains.filter(status='transferred')
        return context

class MakePayment(LoginRequiredMixin, CreateView):
    model = Payment
    fields = ['phone']
    template_name = "siteadmin/pages/makepayment.html"

    def form_valid(self, form):
        domain = Domain.objects.get(name=self.kwargs['domain'])
        form.instance.domain = domain
        if domain.name.find(".zw"):
            form.instance.amount = 55
        else:
            form.instance.amount = 600
        return super(MakePayment, self).form_valid(form)

class InvoiceView(LoginRequiredMixin, ListView):
    template_name = Invoice
    template = "siteadmin/pages/invoices.html"
    context_object_name = "invoices"

    def get_queryset(self, **kwargs):
        return invoices

class DomainListView(LoginRequiredMixin, ListView):
    model = Domain
    template_name = "siteadmin/pages/domainlist.html"
    context_object_name = "domains"

    def get_queryset(self, **kwargs):
        domains = Domain.objects.filter(user=self.request.user)
        return domains.filter(status=self.kwargs['status'])

class RegisteredDomainView(ListView, LoginRequiredMixin):
    model = Domain
    template_name = "siteadmin/pages/registered.html"
    context_object_name = "domains"

    def get_queryset(self, **kwargs):
        domains = Domain.objects.filter(user=self.request.user)
        return domains

class TransferDomainView(LoginRequiredMixin, CreateView):
    model = Transfer
    fields = ['domain_name', 'note']
    template_name = "siteadmin/pages/transfer.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TransferDomainView, self).form_valid(form)


class UpdateAccountView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "siteadmin/pages/account_edit.html"
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
                        price = Price.objects.get(domain_type="loc")
                        return render(request,'siteadmin/pages/search.html', {'av': 'true', 'dom': domain, 'price': price.price})
                    else:
                        price = Price.objects.get(domain_type="loc")
                        return render(request, 'siteadmin/pages/search.html', {'av': 'false', 'dom': domain, 'price': price.price})
                except:
                    price = Price.objects.get(domain_type="loc")
                    return render(request, 'siteadmin/pages/search.html', {'av': 'true', 'dom': domain, 'price': price.price})
            else:
                w = whois.whois(domain)
                if w['status'] == None:
                    price = Price.objects.get(domain_type="int")
                    return render(request, 'siteadmin/pages/search.html', {'av': 'true', 'dom': domain, 'price': price.price})
                else:
                    price = Price.objects.get(domain_type="int")
                    return render(request, 'siteadmin/pages/search.html', {'av': 'false', 'dom': domain, 'price': price.price})
        else:
            return render(request, 'siteadmin/pages/search.html')
    else:
        return render(request, 'siteadmin/pages/search.html')

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

class PaymentView(LoginRequiredMixin, TemplateView):
    template_name = 'siteadmin/pages/payments.html'


class Manage(UpdateView, LoginRequiredMixin):
    model = Domain
    fields = ('nameserver1', 'nameserver2', 'nameserver3', 'nameserver4', 'nameserver5')
    context_object_name = 'domain'
    template_name = "siteadmin/pages/manage.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        domain = Domain.objects.get(pk=self.kwargs['pk'])
        context["domain"] = domain
        return context

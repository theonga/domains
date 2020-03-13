from django.shortcuts import render
from django.urls import reverse
from main.models import Domain, Price
from .forms import ContactForm
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
import whois
import socket

# Create your views here.
def HomePageView(request):
    if request.method == 'POST':
        domain = request.POST['domain']
        if domain:
            if domain.find(".zw"):
                try:
                    if socket.gethostbyname(domain) == None:
                        price = Price.objects.get(domain_type="loc")
                        return render(request,'home.html', {'av': 'true', 'dom': domain, 'price': price.price})
                    else:
                        price = Price.objects.get(domain_type="loc")
                        return render(request, 'home.html', {'av': 'false', 'dom': domain, 'price': price.price})
                except:
                    price = Price.objects.get(domain_type="loc")
                    return render(request, 'home.html', {'av': 'true', 'dom': domain, 'price': price.price})
            else:
                w = whois.whois(domain)
                if w['status'] == None:
                    return render(request, 'home.html', {'av': 'true', 'dom': domain, 'price': Price.objects.get(domain_type="int").price})
                else:
                    return render(request, 'home.html', {'av': 'false', 'dom': domain, 'price': Price.objects.get(domain_type="int").price})
        else:
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')


def Contact(request):
    if request.method == 'GET':
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            phone_number = form.cleaned_data['phone_number']
            message = form.cleaned_data['message']
            content = "Phone: {} \n Message: {}".format(phone_number, message)
            try:
                send_mail(subject, content, from_email, ['brandonsimango2@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect('contact')
    return render(request, "pages/contact.html", {'form': form})

class AboutPageView(TemplateView): # new
    template_name = 'pages/about.html'

class Register(LoginRequiredMixin, CreateView):
    model = Domain
    fields = ['first_name', 'last_name', 'business', 'org_name', 'nameserver1', 'nameserver2', 'nameserver3', 'nameserver4', 'nameserver5', 'address', 'email', 'phone']
    template_name = "siteadmin/pages/registerdom.html"

    def get_success_url(self):
        return reverse('payments')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        name = self.kwargs['domain']
        form.instance.name = name
        return super(Register, self).form_valid(form)

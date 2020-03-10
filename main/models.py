from django.db import models
from users.models import CustomUser
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import send_mail
from django.shortcuts import redirect

domain_status = (
    ('pn', 'Pending'),
    ('ac', 'Active'),
    ('ex', 'Expired'),
    ('tf', 'Transferred')
)

payment_status = (
    ('S', 'Success'),
    ('F', 'Failed'),
)

class Domain(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=("user"), on_delete=models.CASCADE)
    name = models.CharField(help_text="Domain name", max_length=50)
    status = models.CharField(help_text="Status", choices=domain_status, default='pn', max_length=50)
    first_name = models.CharField(help_text="Owner first name", max_length=50)
    last_name = models.CharField(help_text="Owner last name", max_length=50)
    business = models.CharField(help_text="Domain business", max_length=100)
    org_name = models.CharField(help_text="Organisation name", null=True, blank=True, max_length=50)
    address = models.TextField(help_text="Physical Address", max_length=200)
    email = models.CharField(help_text="Registrant Email Address", max_length=100)
    phone = models.CharField(help_text="Registrant Phone Number", max_length=50)
    nameserver1 = models.CharField(help_text="Nameserver 1", max_length=50)
    nameserver2 = models.CharField(help_text="Nameserver 2", max_length=50)
    nameserver3 = models.CharField(help_text="Nameserver 3", blank=True, null=True, max_length=50)
    nameserver4 = models.CharField(help_text="Nameserver 4", blank=True, null=True, max_length=50)
    nameserver5 = models.CharField(help_text="Nameserver 5", blank=True, null=True, max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dashboard")

    class Meta:
        db_table = "dm_domains"
        verbose_name = "Domain"
        verbose_name_plural = "Domains"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        sender = self.user.email
        subject = "Domain Registration"
        full_message = "Nameserver: <br> Domain name: {}, <br> Nameserver 1: {}, <br> Nameserver 2: {}, <br> Nameserver 3: {}, <br> Nameserver 4: {}, <br> Nameserver 5: {}".format(self.name, self.nameserver1, self.nameserver2, self.nameserver3, self.nameserver4, self.nameserver5)
        try:
            send_mail(subject, full_message, sender, ['clouditate@gmail.com'])
        except BadHeaderError:
                return HttpResponse('Email not valid')
        return redirect('dashboard')
        super(Domain, self).save(*args, **kwargs)

class Payment(models.Model):
    domain = models.ForeignKey(Domain, help_text="Domain name", on_delete=models.CASCADE)
    amount = models.FloatField(help_text="Amount")
    phone = models.CharField(help_text="Ecocash phone", max_length=50)
    status = models.CharField(help_text="Payment status", choices=payment_status, max_length=50)
    date = models.DateField(help_text="date", auto_now_add=True)

    def __str__(self):
        return self.domain.name

    def get_absolute_url(self):
        return reverse('dashboard')
    class Meta:
        db_table = "dm_payments"

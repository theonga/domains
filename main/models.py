from django.db import models
from users.models import CustomUser
from django.urls import reverse
from django.utils.text import slugify
from django.core.mail import BadHeaderError, send_mail
from django.shortcuts import redirect
from django.utils import timezone
from paynow import Paynow
from datetime import datetime, timedelta

domain_status = (
    ('pending', 'Pending'),
    ('active', 'Active'),
    ('expired', 'Expired'),
    ('transferred', 'Transferred')
)

payment_status = (
    ('S', 'Success'),
    ('F', 'Failed'),
)

class Price(models.Model):
    tld = (
        ('int',  'International Domain'),
        ('loc', 'Local Domains')
    )
    domain_type = models.CharField(help_text="Domain type", choices=tld, max_length=30)
    price = models.FloatField(help_text="Domain price")

    def __str__(self):
        return self.domain_type


class Domain(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=("user"), on_delete=models.CASCADE)
    name = models.CharField(help_text="Domain name", max_length=50, unique=True)
    status = models.CharField(help_text="Status", choices=domain_status, default='pending', max_length=50)
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
    registered_date = models.DateTimeField(default=timezone.now())
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=365))
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("index")

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
            send_mail(subject, full_message, sender, ['support@zimbabwedomainregistration.com'])
        except BadHeaderError:
                return HttpResponse('Email not valid')
        super(Domain, self).save(*args, **kwargs)


class Transfer(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=("user"), on_delete=models.CASCADE)
    domain_name = models.CharField(help_text="Domain name", max_length=50)
    note = models.TextField(help_text="Release note from your current registra")

    class Meta:
        db_table = "dm_transfer"

    def get_absolute_url(self):
        return reverse("index")


    def save(self, *args, **kwargs):
        sender = self.user.email
        subject = "Domain Registration Transfer"
        full_message = "Domain name: {}, <br> note: {}".format(self.domain_name, self.note)
        try:
            send_mail(subject, full_message, sender, ['support@zimbabwedomainregistration.com'])
        except BadHeaderError:
                return HttpResponse('Email not valid')
        super(Transfer, self).save(*args, **kwargs)



class Payment(models.Model):
    domain = models.ForeignKey(Domain, help_text="Domain name", on_delete=models.CASCADE)
    amount = models.FloatField(help_text="Amount")
    phone = models.CharField(help_text="Ecocash phone", max_length=50)
    status = models.CharField(help_text="Payment status", choices=payment_status, default='F', max_length=50)
    date = models.DateField(help_text="date", auto_now_add=True)

    def __str__(self):
        return self.domain.name

    def get_absolute_url(self):
        return reverse('index')

    class Meta:
        db_table = "dm_payments"

    def save(self, *args, **kwargs):
        paynow = Paynow(
            '6668',
            'b0b170e0-c950-4800-b56c-9ce4e4e02e14',
            'https://zimbabwedomainregistry.co.zw',
            'https://zimbabwedomainregistry.co.zw',
        )
        payment = paynow.create_payment(self.domain.name, self.domain.user.email)
        if self.domain.name.find(".zw"):
            payment.add(self.domain.name, 55)
            self.amount = 55
        else:
            payment.add(self.domain.name, 600)
            self.amount = 600
        response = paynow.send_mobile(payment, self.phone, 'ecocash')
        if response.success:
            status = paynow.check_transaction_status('https://zimbabwedomainregistry.co.zw')
            time.sleep(30)
            if status.paid:
                self.status = 'S'
                self.domain.status = 'active'
            else:
                self.status = 'F'
                self.domain.status = 'pending'
        else:
            self.status = 'F'
            self.domain.status = 'pending'
        super(Payment, self).save(*args, **kwargs)



class Invoice(models.Model):
     in_status = (
        ('paid', 'Paid'),
        ('unpaid', 'Not Paid')
     )
     domain = models.ForeignKey(Domain, on_delete=models.CASCADE, related_name="invoices")
     amount = models.FloatField(help_text="Amount Due")
     status = models.CharField(help_text="Invoice Status", max_length=20, choices=in_status, default="unpaid")

     def __str__(self):
         return self.domain.name

     def get_absolute_url(self):
         return reverse('index')

     class Meta:
         db_table = "dm_invoices"

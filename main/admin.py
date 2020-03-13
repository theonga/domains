from django.contrib import admin
from main.models import Domain, Transfer, Invoice, Payment, Price
models = [Domain, Transfer, Invoice, Payment, Price]
# Register your models here.
for model in models:
    admin.site.register(model)

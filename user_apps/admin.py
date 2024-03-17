from django.contrib import admin
from .models import App, Plan, Subscription

# Register your models here.
admin.site.register(App)
admin.site.register(Plan)
admin.site.register(Subscription)

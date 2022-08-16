from django.contrib import admin
from .models import Router, Deployment, Script

# Register your models here.
admin.site.register(Router)
admin.site.register(Script)
admin.site.register(Deployment)

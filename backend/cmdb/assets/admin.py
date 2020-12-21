from django.contrib import admin
from assets import models


# Register your models here.


for i in models.__all__:
    admin.site.register(getattr(models,i))


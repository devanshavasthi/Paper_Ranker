from django.contrib import admin

# Register your models here.
from .models import FrequentPaper,NewPaper

admin.site.register(FrequentPaper)
admin.site.register(NewPaper)
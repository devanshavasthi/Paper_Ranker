from django.contrib import admin

# Register your models here.
from .models import FrequentPaper,NewPaper,fetchinfo,conferencedata

admin.site.register(FrequentPaper)
admin.site.register(NewPaper)
admin.site.register(fetchinfo)
admin.site.register(conferencedata)


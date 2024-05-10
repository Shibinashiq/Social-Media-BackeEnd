from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Story)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(SavedPost)
admin.site.register(Report)
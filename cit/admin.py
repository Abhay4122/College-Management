from django.contrib import admin
from .models import inquery, course, std_registration, std_exm_marks, std_fee

# Register your models here.
admin.site.register(inquery)
admin.site.register(course)
admin.site.register(std_registration)
admin.site.register(std_exm_marks)
admin.site.register(std_fee)
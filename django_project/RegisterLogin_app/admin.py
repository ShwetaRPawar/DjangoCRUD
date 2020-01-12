from django.contrib import admin
from .models import Register
# Register your models here.
#admin.site.register(register)

#define admin class
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'email', 'password' ,'confirm_pass', 'status')
#register the admin class with associated model
admin.site.register(Register,RegisterAdmin)



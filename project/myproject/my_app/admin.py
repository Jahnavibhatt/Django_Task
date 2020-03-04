from django.contrib import admin
# from . import models
# from .models import UserProfile
from django.contrib import admin
from .models import *


admin.site.register(UserProfile)

admin.site.register(Menu)
admin.site.register(MenuPdf)
admin.site.register(Order)

from django.contrib import admin
from django.contrib.auth.models import Group

from .models import ReferalCode, ReferalHistory

admin.site.register(ReferalHistory)
admin.site.register(ReferalCode)
admin.site.unregister(Group)
 
from django.contrib import admin

# Register your models here.

from .models import Keeper
from .models import Apiary
from .models import Hive
from .models import Event

admin.site.register(Keeper)
admin.site.register(Apiary)
admin.site.register(Hive)
admin.site.register(Event)

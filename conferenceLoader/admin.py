from django.contrib import admin

# Register your models here.
from .models import Conference
from .models import Team
from .models import Stream
from .models import Person

admin.site.register(Conference)
admin.site.register(Team)
admin.site.register(Stream)
admin.site.register(Person)
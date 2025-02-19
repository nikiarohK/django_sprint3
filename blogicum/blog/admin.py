from django.contrib import admin
from .models import Category, Location, Post

admin.site.register({Category, Location, Post})

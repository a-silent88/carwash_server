from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db import models
from django.core.paginator import Paginator
from django.db.models import Q

# Create your views here.
class CommentView(View):
    def get(self, request):
        return render(request, 'comments.html')
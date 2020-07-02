from django.shortcuts import HttpResponse
from django.views.generic import View
from .tasks import celery_task


class MyView(View):

    def get(self, request):
        result = celery_task(1)
        return HttpResponse(result)
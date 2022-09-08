from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView
from django.urls import reverse_lazy

from .models import Mail
from .forms import MailForm

import smtplib, ssl, random, praw, re
from bs4 import BeautifulSoup

# Create your views here.
class MailView(FormView):
    template_name = 'script/email.html'
    form_class = MailForm
    success_url = reverse_lazy('script:success')

    def form_valid(self, form):
        # Calls the custom send method
        form.send()
        return super().form_valid(form)

class MailSuccessView(TemplateView):
    template_name = 'script/success.html'

def something(request):
    if request.method == "POST":
        form = MailForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return render(request, 'script/email.html', {})
    else:
        form = MailForm()
    return render(request, 'script/email.html', {'form':form})

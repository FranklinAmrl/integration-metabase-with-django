from django.http import HttpResponse
from django.shortcuts import render
import jwt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from config.settings import METABASE_SECRET_KEY, METABASE_SITE_URL

class LoginRequiredClass(LoginRequiredMixin):
    login_url = "/login/"

def get_token(payload):
    return jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

def index(request):
    return render(request,
                  'user_stats/index.html',
                  {})

def public_dashboard(request):
    payload = {
        "resource": {"dashboard": 1},
        "params": {
        }
    }
    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + get_token(payload) + "#bordered=true"
    return render(request,
                  'user_stats/public_dashboard.html',
                  {'iframeUrl': iframeUrl}) 
@login_required
def private_chart(request):
    payload = {
        "resource": {"question": 8},
        "params": {
        }
    }

    iframeUrl = METABASE_SITE_URL + "/embed/question/" + get_token(payload) + "#bordered=true"

    # always show admins user stats
    return render(request,
                    'user_stats/private_chart.html',
                    {'iframeUrl': iframeUrl})

@login_required
def private_dashboard(request):
    payload = {
        "resource": {"dashboard": 5},
        "params": {
        }
    }

    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + get_token(payload) + "#bordered=true"

    return render(request,
                    'user_stats/private_dashboard.html',
                    {'iframeUrl': iframeUrl})
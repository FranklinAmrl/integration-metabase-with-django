from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
import requests
import jwt
from django.contrib.auth.decorators import login_required
from django.views import View

from django.views.generic import TemplateView

from config.settings import METABASE_SECRET_KEY, METABASE_SITE_URL


def get_token(payload):     
    return jwt.encode(payload, METABASE_SECRET_KEY, algorithm="HS256")

def get_session(username,password):
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(METABASE_SITE_URL + "/api/session",json = payload)
    session = response.json().get("id")
    return session

class IndexView(TemplateView):

    template_name = 'user_stats/index.html'


def get_dashboard(request,id):
    payload = {
        "resource": {"dashboard": id},
        "params": {
             
        }
    }
    questionUrl = METABASE_SITE_URL + f"/api/dashboard/{id}"
    session_id = get_session("franklinteste00@gmail.com","Nilknarf-0")
    response = requests.get(questionUrl, headers={'X-Metabase-Session':session_id})
    card_data = [{"id" : data.get('card_id'),"name":data.get('card').get('name')}
                     for data in response.json()['ordered_cards']]
    iframeUrl = METABASE_SITE_URL + "/embed/dashboard/" + get_token(payload) + "#bordered=true"
    return render(request,
                  'user_stats/public_dashboard.html',
                  {'iframeUrl': iframeUrl,'card_data':card_data})

class CardView(View):

    previous_url = reverse_lazy('index')

    def get(self,request,id):
        payload = {
            "resource": {"question": id},
            "params": {
                
            }
        }
        iframeUrl = METABASE_SITE_URL + "/embed/question/" + get_token(payload) + "#bordered=true"
        response = requests.get(iframeUrl)
        print(iframeUrl)
        #print(response.text)
        html = response.text
        html = html.replace("<body>","")
        html = html.replace("</body>","")
        #print(html[:1000])
        return render(request,
                    'user_stats/public_dashboard.html',
                    {'iframeUrl': iframeUrl,'previous_url':self.previous_url}) 


class PublicDashboardView(View):
    previous_url = reverse_lazy('index')
    def get(self,request):
        dashboardUrl = METABASE_SITE_URL + "/api/dashboard"
        session_id = get_session("franklinteste00@gmail.com","Nilknarf-0")
        response = requests.get(dashboardUrl,headers={'X-Metabase-Session':session_id})
        data = []
        for dashboard in response.json():
            data.append({'id':dashboard['id'],'name':dashboard['name']})


        return render(request,
                    'user_stats/public_dashboard.html',
                    {'data':data,'previous_url':self.previous_url}) 


# def public_dashboard(request):
    
#     dashboardUrl = METABASE_SITE_URL + "/api/dashboard"
#     session_id = get_session("franklinteste00@gmail.com","Nilknarf-0")
#     response = requests.get(dashboardUrl,headers={'X-Metabase-Session':session_id})
#     data = []
#     for dashboard in response.json():
#         data.append({'id':dashboard['id'],'name':dashboard['name']})


#     return render(request,
#                   'user_stats/public_dashboard.html',
#                   {'data':data}) 
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
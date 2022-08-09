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

class DocumentationView(TemplateView):
    template_name = 'user_stats/documentation.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['url_doc'] = "https://drive.google.com/drive/folders/1SdDHygsMDUrOPITFLpv6r8xtkw2QOY4N"
        return context

class ShowDashboardView(View):
    def get(self,request,id):
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
                    'user_stats/show_dashboard.html',
                    {'iframeUrl': iframeUrl,'card_data':card_data})

class CardView(View):
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
                    'user_stats/show_chart.html',
                    {'iframeUrl': iframeUrl}) 


class ListDashboardView(View):
    previous_url = reverse_lazy('index')
    def get(self,request):
        dashboardUrl = METABASE_SITE_URL + "/api/dashboard"
        session_id = get_session("franklinteste00@gmail.com","Nilknarf-0")
        response = requests.get(dashboardUrl,headers={'X-Metabase-Session':session_id})
        dashboard_data = []
        for dashboard in response.json():
            dashboard_data.append({'id':dashboard['id'],'name':dashboard['name']})

        return render(request,
                    'user_stats/list_dashboard.html',
                    {'dashboard_data':dashboard_data,'previous_url':self.previous_url})


class ListCardiew(View):
    def get(self,request):
        card_url = METABASE_SITE_URL + "/api/card"
        session_id = get_session("franklinteste00@gmail.com","Nilknarf-0")
        response = requests.get(card_url,headers={'X-Metabase-Session':session_id})
        card_data = []
        for card in response.json():
            card_data.append({'id':card.get('id'),'name':card.get('name')})

        return render(request,
                    'user_stats/list_card.html',
                    {'card_data':card_data})

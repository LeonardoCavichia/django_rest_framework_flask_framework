"""eventos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from rest_framework import routers

from api_eventos.viewsets.eventos_viewsets import events_view, event_details, search_event_viewset
from api_eventos.viewsets.eventos_tipo_viewsets import evento_tipo
from api_eventos.viewsets.mensagem_viewsets import mensagem_view, mensagem_details
from api_eventos.viewsets.participant_viewsets import participant_view, participant_details
from api_eventos.viewsets.user_viewset import user_details, user_view, user_login

router = routers.DefaultRouter()

urlpatterns = [
    path('user/login', user_login),
    path('user/login/', user_login),
    path('user/<slug:id>', user_details),
    path('user/<slug:id>/', user_details),
    path('user', user_view),
    path('user/', user_view),

    path('event', events_view),
    path('event/', events_view),
    path('event/search', search_event_viewset),
    path('event/<slug:id>', event_details),
    path('event/<slug:id>/', event_details),

    path('participant/', participant_view),
    path('participant', participant_view),
    path('participant/<slug:id>', participant_details),
    path('participant/<slug:id>/', participant_details),

    path('mensagem/', mensagem_view),
    path('mensagem', mensagem_view),
    path('mensagem/<slug:id>', mensagem_details),
    path('mensagem/<slug:id>/', mensagem_details),
    path('mensagem/evento/<slug:id>', mensagem_details),
    path('mensagem/evento/<slug:id>/', mensagem_details),

    path('tipoEvento/', evento_tipo),
    path('tipoEvento', evento_tipo),
    path('tipoevento/', evento_tipo),
    path('tipoevento', evento_tipo),

    path('', include(router.urls)),
    path('admin/', admin.site.urls)

]

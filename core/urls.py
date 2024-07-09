# Importando as bibliotecas necessárias
from django.contrib import admin
from django.urls import path, include
from core.views import home, detail, save, update, delete
from django.views.generic.base import RedirectView

# Definindo os padrões de URL para a aplicação Django
urlpatterns = [
    # Rotas
    path('', home, name='home'),
    path('save/', save, name="save"),
    path('detail/<int:id>', detail, name='detail'),
    path('update/<int:id>', update, name='update'),
    path('delete/<int:id>', delete, name='delete'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico'))
]

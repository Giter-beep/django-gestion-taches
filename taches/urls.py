from django.urls import path
from . import views




urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('stats/pdf/', views.stats_pdf, name='stats_pdf'),



    # Intervenants
    path('intervenants/', views.intervenant_list, name='intervenant_list'),
    path('intervenants/add/', views.intervenant_add, name='intervenant_add'),
    path('intervenants/delete/<int:pk>/', views.intervenant_delete, name='intervenant_delete'),

    # Clients
    path('clients/', views.client_list, name='client_list'),
    path('clients/add/', views.client_add, name='client_add'),
    path('clients/delete/<int:pk>/', views.client_delete, name='client_delete'),

    # Interventions
path('interventions/', views.intervention_list, name='intervention_list'),
path('interventions/add/', views.intervention_add, name='intervention_add'),
path('interventions/delete/<int:pk>/', views.intervention_delete, name='intervention_delete'),


    # Statistiques
    path('stats/', views.stats, name='stats'),
]

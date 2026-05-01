from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update-stock/', views.update_stock, name='update_stock'),
    path('save-transaction/', views.save_transaction, name='save_transaction'),
    path('report/', views.report, name='report'),
    path('manifest.json', TemplateView.as_view(template_name='billing/manifest.json', content_type='application/json'), name='manifest'),
    path('sw.js', TemplateView.as_view(template_name='billing/sw.js', content_type='application/javascript'), name='sw'),
]

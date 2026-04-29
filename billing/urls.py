from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('update-stock/', views.update_stock, name='update_stock'),
    path('save-transaction/', views.save_transaction, name='save_transaction'),
    path('report/', views.report, name='report'),
]

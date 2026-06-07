from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create/', views.create_short_url, name='create_url'),
    path('result/<int:pk>/', views.url_detail_public, name='url_detail_public'),
    path('url/<int:pk>/', views.url_detail, name='url_detail'),
    path('url/<int:pk>/edit/', views.edit_url, name='edit_url'),
    path('url/<int:pk>/delete/', views.delete_url, name='delete_url'),
    path('url/<int:pk>/qr/', views.get_qr_code, name='get_qr_code'),
    path('s/<str:short_code>/', views.redirect_to_url, name='redirect_url'),
]

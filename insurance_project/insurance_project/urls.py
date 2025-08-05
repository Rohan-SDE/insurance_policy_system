from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views
from insurance import views

router = DefaultRouter()
router.register(r'policies', views.PolicyViewSet)
router.register(r'claims', views.ClaimViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('policies/', views.policy_list, name='policy_list'),
    path('feedback/', views.feedback_view, name='feedback'),
]

from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Import auth views for login
from django.contrib import admin
from django.urls import path, include

# def home(request):
#     return render(request, 'insurance/index.html')
from django.contrib.auth.views import LoginView

class MyLoginView(LoginView):
    template_name = "insurance/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return "https://ai-medical-soumyadip.onrender.com/"

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('policies/', views.policy_list, name='policy_list'),
    path('feedback/', views.feedback_view, name='feedback'),
    # path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    # path('admin/', admin.site.urls),
    # path('', include('insurance.urls')),
    path('login/', views.login_user, name='login_user'),
    path('signup/', views.signup_user, name='signup_user'),
    # path('', home, name='home'), 
    path('', views.home, name='home'),
    path("login/", MyLoginView.as_view(), name="login"),

]
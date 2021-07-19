"""donMaxsulot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from home import views
from home.views import base, editItem, agentTake, editAgent, delete, deleteHome, editHome, payToAgent, deleteBase

from django.views.static import serve
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('delete/<int:home_id>', deleteHome, name='deleteHome'),
    path('<int:home_id>', editHome, name='editHome'),
    # Note Auth
    path('signup/', views.signup_user, name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login'),
    # Note base
    path('base/', base, name='base'),
    path('base/<int:product_id>', editItem, name='editItem'),
    path('base/delete/<int:product_id>', deleteBase, name='deleteBase'),
    # Savdo tochkasi
    path('savdo/', agentTake, name='agentTake'),
    path('savdo/<int:agent_id>', editAgent, name='editAgent'),
    path('savdo/delete/<int:agent_id>', delete, name='delete'),
    path('savdo/payToAgent', payToAgent, name='payToAgent'),
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root':       settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

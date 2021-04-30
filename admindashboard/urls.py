from admindashboard import views
from django.urls import path, include
"""dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

urlpatterns = [
    path('add_program/', views.add_program, name = 'add_program'),
    path('add_module/', views.add_module, name = 'add_module'),
    path('add_content/', views.add_content, name = 'add_content'),
    path('add_ivr_prompt/', views.add_ivr_prompt, name = "add_ivr_prompt"),
    path('program_format/', views.program_format, name = 'program_format'),
    path('module_format/', views.module_format, name = 'module_format'),
    path('content_format/', views.content_format, name = 'content_format'),
    # path('program_insert_sample/', views.export_program_insert_sample, name = "export_program_insert_sample"),
    # path('program_update_sample/', views.export_program_update_sample, name = "export_program_update_sample"),
    # path('module_insert_sample/', views.export_module_insert_sample, name = "export_module_insert_sample"),
    # path('module_update_sample/', views.export_module_update_sample, name = "export_module_update_sample"),
    # path('content_sample_without_module/', views.export_content_sample_wihtout_module, name = "export_content_sample"),
    # path('content_sample_with_module/', views.export_content_sample_with_module, name = "export_content_sample"),
    path('ivrprompt_format/', views.ivrprompt_format, name = 'ivrprompt_format'),
    # path('ivrprompt_insert_sample/', views.export_ivrprompt_insert_sample, name = "export_ivrprompt_insert_sample"),
    # path('ivrprompt_update_sample/', views.export_ivrprompt_update_sample, name = "export_ivrprompt_update_sample")
]

admin.site.site_header = "Dost Admin"
admin.site.site_title = "Dost Admin Portal"
admin.site.index_title = "Welcome to Dost Admin Portal"
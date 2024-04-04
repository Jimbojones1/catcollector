from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
	# django's convention is to use a trailing / for 
	# the routE
	path('about/', views.about, name='about'),
	path('cats/', views.cats_index, name="index"),
	path('cats/<int:cat_id>/', views.cats_detail, name='detail'),
	path('cats/create/', views.CatCreate.as_view(), name='cats_create'),
]
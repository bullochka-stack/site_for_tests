from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('category/<int:category_id>/', get_category, name='category'),
    path('test/<int:test_id>/<int:number_question>/', test_page, name='test_page'),
    path('test/<int:test_id>/results/', show_results, name='show_results'),
    path('login/', user_login, name='login'),
    path('registration/', registration, name='registration'),
    path('logout/', user_logout, name='user_logout'),
    path('profile/', user_profile, name='user_profile'),

]
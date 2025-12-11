from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 🔐 Autenticación
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),  # La raíz ahora es siempre el login

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    
    # 🏠 Páginas principales
    path('welcome/', views.welcome, name='welcome'),
    path('home/', views.home, name='home'),
    path('start-quiz/', views.start_quiz, name='start_quiz'),
    path('play/', views.play_quiz, name='play_quiz'),
    path('results/', views.quiz_results, name='quiz_results'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile_user'),
    path('discover/', views.discover, name='discover'),

    # 🛠 Debug
    path('debug/', views.debug_quiz, name='debug_quiz'),
]

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import JsonResponse
from .models import (
    Category, Question, Answer, UserProfile, Badge, 
    UserBadge, Quiz, QuizAttempt, QuizResponse, Friend
)
import random


def welcome(request):
    """Pantalla de bienvenida"""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'quizz/welcome.html')


def register(request):
    """Registro de nuevo usuario"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil automáticamente
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def home(request):
    """Pantalla principal - Discover"""
    # Obtener o crear perfil del usuario
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Quizzes disponibles
    quizzes = Quiz.objects.filter(is_live=True)[:5]
    
    # Categorías
    categories = Category.objects.all()[:4]
    
    # Amigos
    friends = Friend.objects.filter(user=request.user).select_related('friend', 'friend__profile')[:5]
    
    # Quiz reciente del usuario
    recent_quiz = QuizAttempt.objects.filter(user=request.user).first()
    
    context = {
        'profile': profile,
        'quizzes': quizzes,
        'categories': categories,
        'friends': friends,
        'recent_quiz': recent_quiz,
    }
    return render(request, 'quizz/home.html', context)


@login_required
def start_quiz(request):
    """Iniciar un nuevo quiz - VERSIÓN MEJORADA"""
    # Limpiar sesión anterior
    for key in ['quiz_questions', 'current_question', 'score', 'correct_answers']:
        if key in request.session:
            del request.session[key]
    
    # Obtener preguntas aleatorias
    all_questions = list(Question.objects.filter(is_active=True))
    
    if len(all_questions) < 20:
        # Si hay menos de 20 preguntas, tomar todas las que hay
        questions = all_questions
    else:
        # Seleccionar 20 aleatorias
        questions = random.sample(all_questions, 20)
    
    if not questions:
        # No hay preguntas, mostrar mensaje
        return render(request, 'quizz/no_questions.html')
    
    # Guardar IDs de preguntas en sesión
    request.session['quiz_questions'] = [q.id for q in questions]
    request.session['current_question'] = 0
    request.session['score'] = 0
    request.session['correct_answers'] = 0
    request.session.modified = True
    
    # Redirigir directamente a la primera pregunta
    return redirect('play_quiz')


@login_required
def play_quiz(request):
    """Jugar el quiz - VERSIÓN MEJORADA"""
    # Obtener datos de la sesión
    question_ids = request.session.get('quiz_questions', [])
    current_index = request.session.get('current_question', 0)
    score = request.session.get('score', 0)
    correct_answers = request.session.get('correct_answers', 0)
    
    # Verificar si hay preguntas en la sesión
    if not question_ids:
        return redirect('start_quiz')
    
    # Verificar si terminó el quiz
    if current_index >= len(question_ids):
        return redirect('quiz_results')
    
    # Obtener la pregunta actual
    try:
        question = Question.objects.get(id=question_ids[current_index])
    except Question.DoesNotExist:
        # Si la pregunta no existe, limpiar sesión y empezar de nuevo
        for key in ['quiz_questions', 'current_question', 'score', 'correct_answers']:
            if key in request.session:
                del request.session[key]
        return redirect('start_quiz')
    
    # Obtener respuestas de la pregunta
    answers = list(question.answers.all())
    
    # Calcular progreso
    progress = ((current_index + 1) / len(question_ids)) * 100
    
    # Procesar respuesta si es POST
    if request.method == 'POST':
        selected_answer_id = request.POST.get('answer')
        
        if selected_answer_id:
            try:
                selected_answer = Answer.objects.get(id=selected_answer_id)
                
                # Verificar si es correcta
                if selected_answer.is_correct:
                    request.session['score'] = score + question.points
                    request.session['correct_answers'] = correct_answers + 1
                
                # Avanzar a la siguiente pregunta
                request.session['current_question'] = current_index + 1
                request.session.modified = True
                
                # Redirigir a la siguiente pregunta o resultados
                return redirect('play_quiz')
                
            except Answer.DoesNotExist:
                pass
    
    context = {
        'question': question,
        'answers': answers,
        'question_number': current_index + 1,
        'total_questions': len(question_ids),
        'progress': progress,
        'score': score,
    }
    return render(request, 'quizz/play_quiz.html', context)


@login_required
def quiz_results(request):
    """Mostrar resultados del quiz - VERSIÓN MEJORADA"""
    # Obtener datos de la sesión
    score = request.session.get('score', 0)
    correct_answers = request.session.get('correct_answers', 0)
    question_ids = request.session.get('quiz_questions', [])
    total_questions = len(question_ids) if question_ids else 0
    
    # Si no hay datos de quiz, redirigir al home
    if total_questions == 0:
        return redirect('home')
    
    # Obtener o crear perfil
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Guardar el intento en la base de datos
    attempt = QuizAttempt.objects.create(
        user=request.user,
        score=score,
        correct_answers=correct_answers,
        total_questions=total_questions
    )
    
    # Actualizar perfil del usuario
    profile.total_points += score
    profile.quizzes_played += 1
    profile.save()
    
    # Verificar y otorgar badges
    check_and_award_badges(request.user, profile)
    
    # Obtener ranking
    rank = profile.get_rank()
    
    # Calcular porcentaje
    percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Limpiar sesión
    for key in ['quiz_questions', 'current_question', 'score', 'correct_answers']:
        if key in request.session:
            del request.session[key]
    
    context = {
        'attempt': attempt,
        'rank': rank,
        'profile': profile,
        'score': score,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'percentage': percentage,
    }
    return render(request, 'quizz/quiz_results.html', context)


def check_and_award_badges(user, profile):
    """Verificar y otorgar badges según logros"""
    badges = Badge.objects.all()
    
    for badge in badges:
        # Verificar si ya tiene el badge
        if UserBadge.objects.filter(user=user, badge=badge).exists():
            continue
        
        # Verificar requisitos según tipo
        awarded = False
        if badge.badge_type == 'beginner' and profile.quizzes_played >= badge.requirement:
            awarded = True
        elif badge.badge_type in ['intermediate', 'expert', 'master'] and profile.total_points >= badge.requirement:
            awarded = True
        
        if awarded:
            UserBadge.objects.create(user=user, badge=badge)


@login_required
def leaderboard(request):
    """Tabla de clasificación"""
    tab = request.GET.get('tab', 'weekly')
    
    if tab == 'weekly':
        # Leaderboard semanal
        week_ago = timezone.now() - timezone.timedelta(days=7)
        
        # Calcular puntos semanales para cada usuario
        users_with_points = []
        all_profiles = UserProfile.objects.select_related('user').all()
        
        for profile in all_profiles:
            weekly_points = QuizAttempt.objects.filter(
                user=profile.user,
                completed_at__gte=week_ago
            ).aggregate(total=Sum('score'))['total'] or 0
            
            if weekly_points > 0:
                users_with_points.append({
                    'user': profile.user,
                    'profile': profile,
                    'points': weekly_points
                })
        
        # Ordenar por puntos
        leaderboard_data = sorted(users_with_points, key=lambda x: x['points'], reverse=True)[:10]
    else:
        # Leaderboard all-time
        leaderboard_data = []
        top_profiles = UserProfile.objects.select_related('user').order_by('-total_points')[:10]
        
        for profile in top_profiles:
            leaderboard_data.append({
                'user': profile.user,
                'profile': profile,
                'points': profile.total_points
            })
    
    # Obtener posición del usuario actual
    current_user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if tab == 'weekly':
        current_user_points = current_user_profile.get_weekly_points()
        higher_count = len([u for u in users_with_points if u['points'] > current_user_points])
        user_rank = higher_count + 1
    else:
        user_rank = current_user_profile.get_rank()
        current_user_points = current_user_profile.total_points
    
    # Top 3 para el podio
    top_3 = leaderboard_data[:3] if len(leaderboard_data) >= 3 else leaderboard_data
    
    context = {
        'leaderboard': leaderboard_data,
        'top_3': top_3,
        'tab': tab,
        'user_rank': user_rank,
        'current_user_points': current_user_points,
    }
    return render(request, 'quizz/leaderboard.html', context)


@login_required
def profile(request, username=None):
    """Perfil de usuario"""
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Badges del usuario
    user_badges = UserBadge.objects.filter(user=user).select_related('badge')
    
    # Estadísticas
    rank = profile.get_rank()
    monthly_quizzes = profile.get_monthly_quizzes()
    
    # Quizzes ganados (con más del 70% de aciertos)
    quizzes_won = QuizAttempt.objects.filter(
        user=user,
        correct_answers__gte=14  # Al menos 14 de 20 correctas
    ).count()
    
    # Quizzes creados
    quizzes_created = profile.quizzes_created
    
    context = {
        'profile': profile,
        'user_badges': user_badges,
        'rank': rank,
        'monthly_quizzes': monthly_quizzes,
        'quizzes_won': quizzes_won,
        'quizzes_created': quizzes_created,
        'is_own_profile': user == request.user,
    }
    return render(request, 'quizz/profile.html', context)


@login_required
def discover(request):
    """Página de descubrimiento"""
    # Buscar quizzes y categorías
    search_query = request.GET.get('search', '')
    
    if search_query:
        quizzes = Quiz.objects.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query),
            is_live=True
        )
        categories = Category.objects.filter(name__icontains=search_query)
    else:
        quizzes = Quiz.objects.filter(is_live=True)[:10]
        categories = Category.objects.all()[:8]
    
    # Amigos
    friends = Friend.objects.filter(user=request.user).select_related('friend', 'friend__profile')[:5]
    
    context = {
        'quizzes': quizzes,
        'categories': categories,
        'friends': friends,
        'search_query': search_query,
    }
    return render(request, 'quizz/discover.html', context)


@login_required
def debug_quiz(request):
    """Página de debug para verificar el estado del quiz"""
    from django.db.models import Count
    
    total_questions = Question.objects.count()
    active_questions = Question.objects.filter(is_active=True).count()
    total_categories = Category.objects.count()
    sample_questions = Question.objects.filter(is_active=True).prefetch_related('answers')[:5]
    
    context = {
        'total_questions': total_questions,
        'active_questions': active_questions,
        'total_categories': total_categories,
        'sample_questions': sample_questions,
    }
    return render(request, 'quizz/debug_quiz.html', context)

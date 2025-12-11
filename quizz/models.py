from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone


class Category(models.Model):
    """Categoría de preguntas"""
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Question(models.Model):
    """Pregunta del quiz"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    points = models.IntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['?']  # Random ordering
    
    def __str__(self):
        return self.question_text[:50]


class Answer(models.Model):
    """Respuesta de una pregunta"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return self.answer_text


class UserProfile(models.Model):
    """Perfil extendido del usuario"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    total_points = models.IntegerField(default=0)
    quizzes_played = models.IntegerField(default=0)
    quizzes_created = models.IntegerField(default=0)
    country_flag = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"
    
    def get_rank(self):
        """Obtener ranking del usuario"""
        return UserProfile.objects.filter(total_points__gt=self.total_points).count() + 1
    
    def get_weekly_points(self):
        """Obtener puntos de la semana"""
        week_ago = timezone.now() - timezone.timedelta(days=7)
        weekly_points = QuizAttempt.objects.filter(
            user=self.user,
            completed_at__gte=week_ago
        ).aggregate(total=Sum('score'))['total'] or 0
        return weekly_points
    
    def get_monthly_quizzes(self):
        """Obtener quizzes jugados este mes"""
        month_ago = timezone.now() - timezone.timedelta(days=30)
        return QuizAttempt.objects.filter(
            user=self.user,
            completed_at__gte=month_ago
        ).count()


class Badge(models.Model):
    """Insignias/Logros"""
    BADGE_TYPES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('expert', 'Expert'),
        ('master', 'Master'),
        ('special', 'Special'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default='beginner')
    icon = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=20, default='#7C3AED')
    requirement = models.IntegerField(help_text="Puntos o quizzes requeridos")
    
    def __str__(self):
        return self.name


class UserBadge(models.Model):
    """Insignias obtenidas por usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'badge']
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"


class Quiz(models.Model):
    """Quiz/Sesión de juego"""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_quizzes')
    total_questions = models.IntegerField(default=20)
    is_live = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Quizzes"
    
    def __str__(self):
        return self.title


class QuizAttempt(models.Model):
    """Intento de quiz por un usuario"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quiz_attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts', null=True, blank=True)
    score = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=20)
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-completed_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.score} points"
    
    def get_percentage(self):
        """Obtener porcentaje de acierto"""
        if self.total_questions > 0:
            return (self.correct_answers / self.total_questions) * 100
        return 0


class QuizResponse(models.Model):
    """Respuesta individual del usuario en un quiz"""
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.attempt.user.username} - Q{self.question.id}"


class Friend(models.Model):
    """Relación de amistad entre usuarios"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'friend']
    
    def __str__(self):
        return f"{self.user.username} - {self.friend.username}"

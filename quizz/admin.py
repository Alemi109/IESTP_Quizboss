from django.contrib import admin
from .models import (
    Category, Question, Answer, UserProfile, Badge, 
    UserBadge, Quiz, QuizAttempt, QuizResponse, Friend
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'created_at']
    search_fields = ['name']


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    max_num = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'category', 'points', 'is_active', 'created_at']
    list_filter = ['category', 'is_active']
    search_fields = ['question_text']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['answer_text', 'question', 'is_correct']
    list_filter = ['is_correct']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_points', 'quizzes_played', 'created_at']
    search_fields = ['user__username', 'user__email']
    list_filter = ['created_at']


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'badge_type', 'requirement', 'color']
    list_filter = ['badge_type']


@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']
    list_filter = ['badge', 'earned_at']
    search_fields = ['user__username']


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'created_by', 'total_questions', 'is_live', 'created_at']
    list_filter = ['category', 'is_live', 'created_at']
    search_fields = ['title', 'description']


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'correct_answers', 'total_questions', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['user__username']


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    list_display = ['attempt', 'question', 'selected_answer', 'is_correct', 'answered_at']
    list_filter = ['is_correct', 'answered_at']


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ['user', 'friend', 'created_at']
    search_fields = ['user__username', 'friend__username']

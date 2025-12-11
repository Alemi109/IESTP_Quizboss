from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from quizz.models import Category, Question, Answer, Badge, UserProfile, Quiz
import random


class Command(BaseCommand):
    help = 'Cargar datos de ejemplo en la base de datos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Cargando datos de ejemplo...')

        # Crear categorías
        categories_data = [
            {'name': 'Cultura General', 'icon': '🌍'},
            {'name': 'Matemáticas', 'icon': '🧮'},
            {'name': 'Historia del Perú', 'icon': '🇵🇪'},
            {'name': 'Ciencias Naturales', 'icon': '🔬'},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(**cat_data)
            categories[cat.name] = cat
            if created:
                self.stdout.write(f'✓ Categoría creada: {cat.name}')

        # Crear preguntas con sus respuestas
        questions_data = [
            # Cultura General (6 preguntas)
            {
                'category': 'Cultura General',
                'text': '¿Cuál es la capital de Francia?',
                'answers': [
                    {'text': 'París', 'correct': True},
                    {'text': 'Londres', 'correct': False},
                    {'text': 'Madrid', 'correct': False},
                    {'text': 'Roma', 'correct': False},
                ]
            },
            {
                'category': 'Cultura General',
                'text': '¿Quién pintó la Mona Lisa?',
                'answers': [
                    {'text': 'Leonardo da Vinci', 'correct': True},
                    {'text': 'Pablo Picasso', 'correct': False},
                    {'text': 'Vincent van Gogh', 'correct': False},
                    {'text': 'Michelangelo', 'correct': False},
                ]
            },
            {
                'category': 'Cultura General',
                'text': '¿Cuál es el océano más grande del mundo?',
                'answers': [
                    {'text': 'Océano Pacífico', 'correct': True},
                    {'text': 'Océano Atlántico', 'correct': False},
                    {'text': 'Océano Índico', 'correct': False},
                    {'text': 'Océano Ártico', 'correct': False},
                ]
            },
            {
                'category': 'Cultura General',
                'text': '¿En qué año llegó el hombre a la Luna?',
                'answers': [
                    {'text': '1969', 'correct': True},
                    {'text': '1959', 'correct': False},
                    {'text': '1979', 'correct': False},
                    {'text': '1989', 'correct': False},
                ]
            },
            {
                'category': 'Cultura General',
                'text': '¿Cuál es el animal terrestre más rápido?',
                'answers': [
                    {'text': 'Guepardo', 'correct': True},
                    {'text': 'León', 'correct': False},
                    {'text': 'Caballo', 'correct': False},
                    {'text': 'Tigre', 'correct': False},
                ]
            },
            {
                'category': 'Cultura General',
                'text': '¿Cuál es el idioma más hablado en el mundo?',
                'answers': [
                    {'text': 'Chino Mandarín', 'correct': True},
                    {'text': 'Español', 'correct': False},
                    {'text': 'Inglés', 'correct': False},
                    {'text': 'Hindi', 'correct': False},
                ]
            },
            # Matemáticas (7 preguntas)
            {
                'category': 'Matemáticas',
                'text': '¿Cuánto es 7 x 8?',
                'answers': [
                    {'text': '56', 'correct': True},
                    {'text': '54', 'correct': False},
                    {'text': '48', 'correct': False},
                    {'text': '64', 'correct': False},
                ]
            },
            {
                'category': 'Matemáticas',
                'text': '¿Cuál es la raíz cuadrada de 144?',
                'answers': [
                    {'text': '12', 'correct': True},
                    {'text': '14', 'correct': False},
                    {'text': '10', 'correct': False},
                    {'text': '16', 'correct': False},
                ]
            },
            {
                'category': 'Matemáticas',
                'text': '¿Cuánto es 25% de 200?',
                'answers': [
                    {'text': '50', 'correct': True},
                    {'text': '25', 'correct': False},
                    {'text': '75', 'correct': False},
                    {'text': '100', 'correct': False},
                ]
            },
            {
                'category': 'Matemáticas',
                'text': 'Si un triángulo tiene ángulos de 60°, 60° y 60°, ¿qué tipo de triángulo es?',
                'answers': [
                    {'text': 'Equilátero', 'correct': True},
                    {'text': 'Isósceles', 'correct': False},
                    {'text': 'Escaleno', 'correct': False},
                    {'text': 'Rectángulo', 'correct': False},
                ]
            },
            {
                'category': 'Matemáticas',
                'text': '¿Cuánto es 15 + 23 x 2?',
                'answers': [
                    {'text': '61', 'correct': True},
                    {'text': '76', 'correct': False},
                    {'text': '53', 'correct': False},
                    {'text': '46', 'correct': False},
                ]
            },
            {
                'category': 'Matemáticas',
                'text': '¿Cuál es el valor de π (pi) aproximadamente?',
                'answers': [
                    {'text': '3.14', 'correct': True},
                    {'text': '3.41', 'correct': False},
                    {'text': '2.14', 'correct': False},
                    {'text': '4.13', 'correct': False},
                ]
            },
            {
                'category': 'Matemáticas',
                'text': '¿Cuántos lados tiene un hexágono?',
                'answers': [
                    {'text': '6', 'correct': True},
                    {'text': '5', 'correct': False},
                    {'text': '7', 'correct': False},
                    {'text': '8', 'correct': False},
                ]
            },
            # Historia del Perú (7 preguntas)
            {
                'category': 'Historia del Perú',
                'text': '¿Quién fue el primer presidente del Perú?',
                'answers': [
                    {'text': 'José de la Riva Agüero', 'correct': True},
                    {'text': 'Simón Bolívar', 'correct': False},
                    {'text': 'Ramón Castilla', 'correct': False},
                    {'text': 'José de San Martín', 'correct': False},
                ]
            },
            {
                'category': 'Historia del Perú',
                'text': '¿En qué año se declaró la independencia del Perú?',
                'answers': [
                    {'text': '1821', 'correct': True},
                    {'text': '1810', 'correct': False},
                    {'text': '1824', 'correct': False},
                    {'text': '1815', 'correct': False},
                ]
            },
            {
                'category': 'Historia del Perú',
                'text': '¿Cuál fue la capital del Imperio Inca?',
                'answers': [
                    {'text': 'Cusco', 'correct': True},
                    {'text': 'Lima', 'correct': False},
                    {'text': 'Arequipa', 'correct': False},
                    {'text': 'Trujillo', 'correct': False},
                ]
            },
            {
                'category': 'Historia del Perú',
                'text': '¿Quién fue el último emperador inca?',
                'answers': [
                    {'text': 'Atahualpa', 'correct': True},
                    {'text': 'Huáscar', 'correct': False},
                    {'text': 'Pachacútec', 'correct': False},
                    {'text': 'Túpac Yupanqui', 'correct': False},
                ]
            },
            {
                'category': 'Historia del Perú',
                'text': '¿En qué batalla se selló la independencia del Perú?',
                'answers': [
                    {'text': 'Batalla de Ayacucho', 'correct': True},
                    {'text': 'Batalla de Junín', 'correct': False},
                    {'text': 'Batalla de Arica', 'correct': False},
                    {'text': 'Batalla de Angamos', 'correct': False},
                ]
            },
            {
                'category': 'Historia del Perú',
                'text': '¿Quién descubrió Machu Picchu para el mundo occidental?',
                'answers': [
                    {'text': 'Hiram Bingham', 'correct': True},
                    {'text': 'Francisco Pizarro', 'correct': False},
                    {'text': 'Antonio Raimondi', 'correct': False},
                    {'text': 'Julio C. Tello', 'correct': False},
                ]
            },
            {
                'category': 'Historia del Perú',
                'text': '¿En qué guerra participó el Perú contra Chile?',
                'answers': [
                    {'text': 'Guerra del Pacífico', 'correct': True},
                    {'text': 'Guerra de la Independencia', 'correct': False},
                    {'text': 'Guerra del Guano', 'correct': False},
                    {'text': 'Guerra Civil', 'correct': False},
                ]
            },
            # Ciencias Naturales (6 preguntas)
            {
                'category': 'Ciencias Naturales',
                'text': '¿Cuál es el planeta más cercano al Sol?',
                'answers': [
                    {'text': 'Mercurio', 'correct': True},
                    {'text': 'Venus', 'correct': False},
                    {'text': 'Tierra', 'correct': False},
                    {'text': 'Marte', 'correct': False},
                ]
            },
            {
                'category': 'Ciencias Naturales',
                'text': '¿Qué órgano del cuerpo humano bombea la sangre?',
                'answers': [
                    {'text': 'El corazón', 'correct': True},
                    {'text': 'Los pulmones', 'correct': False},
                    {'text': 'El hígado', 'correct': False},
                    {'text': 'Los riñones', 'correct': False},
                ]
            },
            {
                'category': 'Ciencias Naturales',
                'text': '¿Cuál es el gas más abundante en la atmósfera terrestre?',
                'answers': [
                    {'text': 'Nitrógeno', 'correct': True},
                    {'text': 'Oxígeno', 'correct': False},
                    {'text': 'Dióxido de carbono', 'correct': False},
                    {'text': 'Hidrógeno', 'correct': False},
                ]
            },
            {
                'category': 'Ciencias Naturales',
                'text': '¿Qué proceso realizan las plantas para producir su alimento?',
                'answers': [
                    {'text': 'Fotosíntesis', 'correct': True},
                    {'text': 'Respiración', 'correct': False},
                    {'text': 'Transpiración', 'correct': False},
                    {'text': 'Fermentación', 'correct': False},
                ]
            },
            {
                'category': 'Ciencias Naturales',
                'text': '¿Cuántos huesos tiene el cuerpo humano adulto?',
                'answers': [
                    {'text': '206', 'correct': True},
                    {'text': '198', 'correct': False},
                    {'text': '214', 'correct': False},
                    {'text': '220', 'correct': False},
                ]
            },
            {
                'category': 'Ciencias Naturales',
                'text': '¿Cuál es el animal más grande del mundo?',
                'answers': [
                    {'text': 'Ballena azul', 'correct': True},
                    {'text': 'Elefante africano', 'correct': False},
                    {'text': 'Tiburón ballena', 'correct': False},
                    {'text': 'Jirafa', 'correct': False},
                ]
            },
        ]

        # Crear preguntas y respuestas
        for q_data in questions_data:
            question, created = Question.objects.get_or_create(
                question_text=q_data['text'],
                category=categories[q_data['category']],
                defaults={'points': 10}
            )
            
            if created:
                for ans_data in q_data['answers']:
                    Answer.objects.create(
                        question=question,
                        answer_text=ans_data['text'],
                        is_correct=ans_data['correct']
                    )
                self.stdout.write(f'✓ Pregunta creada: {q_data["text"][:50]}...')

        # Crear badges
        badges_data = [
            {'name': 'Primer Quiz', 'badge_type': 'beginner', 'requirement': 1, 'description': 'Completa tu primer quiz', 'color': '#06B6D4'},
            {'name': 'Principiante', 'badge_type': 'beginner', 'requirement': 5, 'description': 'Completa 5 quizzes', 'color': '#22C55E'},
            {'name': 'Aficionado', 'badge_type': 'intermediate', 'requirement': 100, 'description': 'Alcanza 100 puntos', 'color': '#FFD700'},
            {'name': 'Experto', 'badge_type': 'expert', 'requirement': 500, 'description': 'Alcanza 500 puntos', 'color': '#A855F7'},
            {'name': 'Maestro', 'badge_type': 'master', 'requirement': 1000, 'description': 'Alcanza 1000 puntos', 'color': '#FF6B9D'},
            {'name': 'Leyenda', 'badge_type': 'master', 'requirement': 5000, 'description': 'Alcanza 5000 puntos', 'color': '#7C3AED'},
        ]

        for badge_data in badges_data:
            badge, created = Badge.objects.get_or_create(**badge_data)
            if created:
                self.stdout.write(f'✓ Badge creado: {badge.name}')

        # Crear usuario de prueba
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@quizboss.com',
                password='admin123',
                first_name='Karina',
                last_name='Quispe'
            )
            self.stdout.write(f'✓ Usuario admin creado (password: admin123)')

        # Crear quiz de ejemplo
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            quiz, created = Quiz.objects.get_or_create(
                title='Quiz de Cultura General',
                defaults={
                    'description': 'Quiz completo de cultura general con 20 preguntas',
                    'created_by': admin_user,
                    'total_questions': 20,
                    'is_live': True
                }
            )
            if created:
                self.stdout.write(f'✓ Quiz creado: {quiz.title}')

        self.stdout.write(self.style.SUCCESS('\n¡Datos de ejemplo cargados exitosamente!'))
        self.stdout.write(f'Total de preguntas: {Question.objects.count()}')
        self.stdout.write(f'Total de categorías: {Category.objects.count()}')
        self.stdout.write(f'Total de badges: {Badge.objects.count()}')

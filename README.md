# 🎯 IESTP QuizBoss - Versión Simple (SIN Google OAuth)

Aplicación web completa de quizzes educativos desarrollada con Django 6.0.

## ✨ Características

- ✅ **Sistema de autenticación simple** (login/registro Django)
- ✅ **26 preguntas** de cultura general
- ✅ **4 categorías** temáticas
- ✅ **6 badges** desbloqueables
- ✅ **Sistema de puntos** y rankings
- ✅ **Leaderboard** (semanal y all-time)
- ✅ **8 pantallas** completas
- ✅ **Diseño responsive**

## 🚀 Instalación Rápida

```bash
# 1. Crear entorno virtual
python -m venv venv

# 2. Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones (ya están creadas)
python manage.py migrate

# 5. Cargar datos de ejemplo
python manage.py load_sample_data

# 6. Iniciar servidor
python manage.py runserver
```

## 🔑 Credenciales

**Usuario Admin:**
- Username: `admin`
- Password: `admin123`

## 📱 URLs

- Inicio: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
- Login: http://127.0.0.1:8000/login/
- Registro: http://127.0.0.1:8000/register/

## 📦 Tecnologías

- Django 6.0
- Python 3.12
- SQLite
- HTML5, CSS3, JavaScript

## ✅ Diferencias con la Versión Completa

Esta versión NO incluye:
- ❌ Google OAuth
- ❌ django-allauth
- ❌ Dependencias adicionales

En su lugar usa:
- ✅ Sistema de autenticación Django nativo
- ✅ Login/Registro simple
- ✅ UserCreationForm de Django

## 🎮 Uso

1. Regístrate en /register/
2. Inicia sesión en /login/
3. Juega quizzes desde /home/
4. Compite en el leaderboard
5. Gana badges por logros

---

**Desarrollado para IESTP**

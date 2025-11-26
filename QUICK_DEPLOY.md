# ⚡ Быстрый деплой на Railway

Скопируйте и выполните команды по порядку.

## 1. Подготовка Git (в терминале проекта)

```bash
cd c:\Users\Hp\OneDrive\Desktop\algoritm
git init
git add .
git commit -m "Initial commit - Algoritmi"
```

## 2. GitHub (создайте репозиторий на GitHub.com)

Затем:
```bash
git remote add origin https://github.com/ВАШ_USERNAME/algoritmi.git
git branch -M main
git push -u origin main
```

## 3. Railway Setup

1. **Сайт:** https://railway.app/
2. **New Project** → **Deploy from GitHub repo**
3. **Выберите:** `algoritmi`
4. **+ New** → **Database** → **PostgreSQL**

## 4. Переменные окружения (Railway Variables)

### Сгенерируйте SECRET_KEY:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Добавьте в Railway:
```env
SECRET_KEY=ваш-сгенерированный-ключ
DEBUG=False
ALLOWED_HOSTS=*.railway.app
GEMINI_API_KEY=ваш-gemini-key
```

### Gemini API:
https://aistudio.google.com/app/apikey

## 5. После деплоя

### Суперпользователь:
```bash
railway run python manage.py createsuperuser
```

### Синхронизация:
```bash
railway run python manage.py sync_arena_scores --all-time
railway run python manage.py create_missing_profiles
```

## ✅ Готово!

Ваш сайт: `https://algoritmi-production-XXXX.up.railway.app`

---

**Проблемы?** См. [DEPLOYMENT.md](DEPLOYMENT.md)

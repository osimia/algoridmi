"""
Утилиты для работы с базой данных
Парсинг DATABASE_URL без внешних зависимостей
"""

from urllib.parse import urlparse, parse_qs


def parse_database_url(url):
    """
    Парсит DATABASE_URL в формат Django DATABASES
    
    Поддерживает форматы:
    - postgresql://user:password@host:port/database
    - postgres://user:password@host:port/database
    
    Args:
        url: строка подключения к БД
    
    Returns:
        dict: конфигурация для Django DATABASES
    """
    if not url:
        return None
    
    # Парсим URL
    parsed = urlparse(url)
    
    # Определяем движок БД
    scheme_map = {
        'postgres': 'django.db.backends.postgresql',
        'postgresql': 'django.db.backends.postgresql',
        'mysql': 'django.db.backends.mysql',
        'sqlite': 'django.db.backends.sqlite3',
    }
    
    scheme = parsed.scheme.split('+')[0]  # Убираем возможные суффиксы
    engine = scheme_map.get(scheme)
    
    if not engine:
        raise ValueError(f"Неподдерживаемая схема БД: {scheme}")
    
    # Базовая конфигурация
    config = {
        'ENGINE': engine,
    }
    
    # Для SQLite путь в netloc или path
    if scheme == 'sqlite':
        config['NAME'] = parsed.path.lstrip('/')
        return config
    
    # Для остальных БД
    config.update({
        'NAME': parsed.path.lstrip('/'),
        'USER': parsed.username or '',
        'PASSWORD': parsed.password or '',
        'HOST': parsed.hostname or 'localhost',
        'PORT': parsed.port or '',
    })
    
    # Дополнительные параметры из query string
    options = {}
    if parsed.query:
        query_params = parse_qs(parsed.query)
        
        for key, value in query_params.items():
            # Берем первое значение из списка
            options[key] = value[0] if isinstance(value, list) else value
    
    # Добавляем настройки для PostgreSQL для улучшения стабильности
    if engine == 'django.db.backends.postgresql':
        options.update({
            'connect_timeout': 10,  # Таймаут подключения 10 секунд
            'options': '-c statement_timeout=30000',  # Таймаут запроса 30 секунд
        })
    
    if options:
        config['OPTIONS'] = options
    
    # Добавляем настройки пула соединений
    config['CONN_MAX_AGE'] = 600  # Держать соединение 10 минут
    
    return config

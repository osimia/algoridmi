"""
Скрипт для создания иконок PWA разных размеров из логотипа
"""
from PIL import Image
import os

# Размеры иконок для PWA
ICON_SIZES = [72, 96, 128, 144, 152, 192, 384, 512]

def generate_icons():
    """Генерирует иконки разных размеров из логотипа"""
    
    # Путь к исходному логотипу
    logo_path = 'static/images/logo.png'
    icons_dir = 'static/icons'
    
    # Проверяем существование логотипа
    if not os.path.exists(logo_path):
        print(f"❌ Логотип не найден: {logo_path}")
        return
    
    # Создаем папку для иконок если её нет
    os.makedirs(icons_dir, exist_ok=True)
    
    # Открываем логотип
    try:
        logo = Image.open(logo_path)
        print(f"✅ Логотип загружен: {logo.size}")
        
        # Конвертируем в RGBA если нужно
        if logo.mode != 'RGBA':
            logo = logo.convert('RGBA')
        
        # Генерируем иконки для каждого размера
        for size in ICON_SIZES:
            # Создаем квадратную иконку
            icon = logo.resize((size, size), Image.Resampling.LANCZOS)
            
            # Сохраняем
            icon_path = os.path.join(icons_dir, f'icon-{size}x{size}.png')
            icon.save(icon_path, 'PNG', optimize=True)
            print(f"✅ Создана иконка: {size}x{size}px")
        
        print(f"\n🎉 Все иконки успешно созданы в папке {icons_dir}/")
        print(f"📱 Теперь приложение будет отображать логотип при установке!")
        
    except Exception as e:
        print(f"❌ Ошибка при создании иконок: {e}")

if __name__ == '__main__':
    generate_icons()

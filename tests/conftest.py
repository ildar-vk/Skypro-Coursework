import os
import sys

# Добавляем src в путь импортов для ВСЕХ тестов
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

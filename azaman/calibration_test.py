import sys
import os
from datetime import datetime, timedelta

# Добавляем папку в пути поиска, чтобы импортировать наш движок
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортируем функцию расчета из нашего основного файла
from test_time import calculate_times, time_to_string

def run_calibration():
    print("=== КАЛИБРОВКА AZAMAN ===")
    # Задаем период для теста (с 12 по 18 ноября 2026)
    start_date = datetime(2026, 11, 12)
    
    for i in range(7):
        current_date = start_date + timedelta(days=i)
        res = calculate_times(current_date.year, current_date.month, current_date.day)
        
        # Выводим в формате, удобном для сравнения с таблицей
        print(f"\nДата: {current_date.strftime('%d.%m.%Y')}")
        print(f"Фаджр: {time_to_string(res['fajr'])} | Восход: {time_to_string(res['sunrise'])} | Зухр: {time_to_string(res['dhuhr'])}")
        print(f"Аср:   {time_to_string(res['asr'])} | Магриб: {time_to_string(res['maghrib'])} | Иша:   {time_to_string(res['isha'])}")

if __name__ == "__main__":
    run_calibration()

def hasl():
    print("=== КАЛЬКУЛЯТОР 'ХАСЛ' ===")
    
    task = input("Введите задачу (нахаслить...)")
    
    if not task.lower().startswith("нахаслить"):
        print("\nОшибка: команда должна начинаться с 'нахаслить...'")
        return

    target = task[9:].strip()
    
    try:
        need = float(input(f"Сколько нужно нахаслить на '{target}' (в рублях)? "))
        have = float(input("Сколько ты уже нахаслил (в рублях)? "))
    except ValueError:
        print("Ошибка: введи числа!")
        return

    remaining = need - have

    print("\n" + "="*40)
    print(f"Цель: {target}")
    print("Результат команды 'хасл':")
    
    if remaining > 0:
        print(f"Тебе осталось нахаслить: {remaining:.2f} рублей.")
        print("Статус: процесс не завершен. Хасль дальше!")
    elif remaining == 0:
        print("Ты нахаслил ровно столько, сколько нужно! Красавчик.")
        print("Статус: выполнено.")
    else:
        print(f"Ты нахаслил даже больше на {-remaining:.2f} рублей!")
        print("Статус: перевыполнение плана. Берем с тебя пример!")

    print("="*40)

hasl()

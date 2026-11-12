import math
from datetime import datetime

# ==========================================
# НАСТРОЙКИ
# ==========================================
LAT = 55.93
LON = 37.51
TIMEZONE_OFFSET = 3.0 

ANGLE_FAJR = 18.0 
ANGLE_ISHA = 17.0 

# Тонкая настройка (подгоняем под табличку)
TUNE = {
    'fajr': -1,     
    'sunrise': 0,   
    'dhuhr': 2,     
    'asr': 0,       
    'maghrib': 0,   
    'isha': 0       
}

# ==========================================
# МАТЕМАТИКА
# ==========================================
def rad(deg): return deg * math.pi / 180.0
def deg(rad): return rad * 180.0 / math.pi

def get_julian_date(year, month, day):
    if month <= 2:
        year -= 1
        month += 12
    A = math.floor(year / 100)
    B = 2 - A + math.floor(A / 4)
    return math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + B - 1524.5

def get_sun_declination_and_eqt(jd):
    d = jd - 2451545.0
    L = (280.460 + 0.9856474 * d) % 360
    g = (357.528 + 0.9856003 * d) % 360
    lambda_sun = L + 1.915 * math.sin(rad(g)) + 0.020 * math.sin(rad(2 * g))
    epsilon = 23.439 - 0.0000004 * d 
    decl = deg(math.asin(math.sin(rad(epsilon)) * math.sin(rad(lambda_sun))))
    alpha = deg(math.atan2(math.cos(rad(epsilon)) * math.sin(rad(lambda_sun)), math.cos(rad(lambda_sun))))
    alpha = (alpha + 360) % 360
    eqt = (L - alpha) * 4 
    if eqt > 20: eqt -= 1440
    if eqt < -20: eqt += 1440
    return decl, eqt

def time_to_string(time_float):
    if time_float == "-----":
        return "-----"
    time_float = time_float % 24.0
    h = int(time_float)
    m = int(round((time_float - h) * 60))
    if m == 60:
        h += 1
        m = 0
    return f"{h:02d}:{m:02d}"

def calc_hour_angle(angle, decl):
    cos_H = (math.sin(rad(angle)) - math.sin(rad(LAT)) * math.sin(rad(decl))) / (math.cos(rad(LAT)) * math.cos(rad(decl)))
    if cos_H > 1.0 or cos_H < -1.0:
        return "-----"
    return deg(math.acos(cos_H)) / 15.0

def calculate_times(year, month, day):
    jd = get_julian_date(year, month, day)
    decl, eqt = get_sun_declination_and_eqt(jd)
    
    times = {}
    
    # 1. Зухр
    dhuhr_utc = 12.0 - (eqt / 60.0)
    dhuhr_local = dhuhr_utc + TIMEZONE_OFFSET - (LON / 15.0)
    times['dhuhr'] = dhuhr_local
    
    # 2. Восход и Магриб
    H_sunrise = calc_hour_angle(-0.833, decl)
    times['sunrise'] = (dhuhr_local - H_sunrise) if H_sunrise != "-----" else "-----"
    times['maghrib'] = (dhuhr_local + H_sunrise) if H_sunrise != "-----" else "-----"

    # 3. Фаджр и Иша
    H_fajr = calc_hour_angle(-ANGLE_FAJR, decl)
    H_isha = calc_hour_angle(-ANGLE_ISHA, decl)
    
    if H_fajr == "-----" or H_isha == "-----":
        if H_sunrise != "-----":
            night_duration = 24.0 - (H_sunrise * 2)
            one_seventh = night_duration / 7.0
            times['fajr'] = times['maghrib'] + one_seventh
            isha_time = times['sunrise'] - one_seventh
            times['isha'] = isha_time + 24.0 if isha_time < 0 else isha_time
        else:
            times['fajr'] = "-----"
            times['isha'] = "-----"
    else:
        times['fajr'] = (dhuhr_local - H_fajr) if H_fajr != "-----" else "-----"
        times['isha'] = (dhuhr_local + H_isha) if H_isha != "-----" else "-----"
    
    # 4. Аср (Ханафитский)
    angle_asr = deg(math.atan(1.0 / (2.0 + math.tan(rad(abs(LAT - decl))))))
    H_asr = calc_hour_angle(angle_asr, decl)
    times['asr'] = (dhuhr_local + H_asr) if H_asr != "-----" else "-----"
    
    # Применяем поправки
    for k in times:
        if times[k] != "-----":
            times[k] += TUNE[k] / 60.0
            
    return times

# ==========================================
# ИНТЕРАКТИВНЫЙ ВВОД ДАТЫ
# ==========================================
if __name__ == "__main__":
    print("\n=== КАЛЬКУЛЯТОР ВРЕМЕНИ НАМАЗА (AZAMAN) ===")
    print("Введите дату в формате ДД.ММ.ГГГГ (например, 12.11.2026).")
    print("Или нажмите Enter, чтобы рассчитать на сегодня.")

    user_input = input("Ваша дата: ").strip()

    if user_input == "":
        target_date = datetime.now()
        print(f"\nБерем текущую дату: {target_date.strftime('%d.%m.%Y')}")
    else:
        try:
            day, month, year = map(int, user_input.split('.'))
            target_date = datetime(year, month, day)
            print(f"\nРасчет для даты: {target_date.strftime('%d.%m.%Y')}")
        except ValueError:
            print("\n[ОШИБКА] Неверный формат даты! Попробуйте еще раз (ДД.ММ.ГГГГ).")
            exit()

    res = calculate_times(target_date.year, target_date.month, target_date.day)

    print("-" * 30)
    for k in ['fajr', 'sunrise', 'dhuhr', 'asr', 'maghrib', 'isha']:
        names = {
            'fajr': 'Фаджр   ', 'sunrise': 'Восход  ', 'dhuhr': 'Зухр    ', 
            'asr': 'Аср     ', 'maghrib': 'Магриб  ', 'isha': 'Иша     '
        }
        print(f"{names[k]}: {time_to_string(res[k])}")
    print("-" * 30)

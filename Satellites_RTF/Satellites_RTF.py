# Импортируем библиотеки
# Штатная библиотека для работы со временем
from datetime import datetime, date, time, timedelta
# Собственно клиент для space-track
# Набор операторов для управления запросами. Отсюда нам понадобится время
import spacetrack.operators as op
# Главный класс для работы с space-track
from spacetrack import SpaceTrackClient

# Штатная библиотека для работы со временем
from datetime import datetime, date
# Ключевой класс библиотеки pyorbital
from pyorbital.orbital import Orbital

import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import ttk

import math

import urllib.request
 
# Имя пользователя и пароль сейчас опишем как константы
USERNAME = 'okuvshinov@inbox.ru'
PASSWORD = 'irit-rtf_satellite_IVM'
LIGHTSPEED = 3e8

EarthRadius = 6371.0088
CenterAngle = 0

utc_shift = 5

CurrentFRQ = 0
CurrentPt = 0
CurrentGt = 0

CurrentSens = -90
CurrentGr = 13

lat_array = []
long_array = []
alt_array = []

az_array = []
elev_array = []

dist_array = []

NeedyInfo = []

recieve_pwr_array = []
 
# Для примера реализуем всё в виде одной простой функции
# На вход она потребует идентификатор спутника, диапазон дат, имя пользователя и пароль. Опциональный флаг для последних данных tle
def get_spacetrack_tle (sat_id, start_date, end_date, username, password, latest=False):
    # Реализуем экземпляр класса SpaceTrackClient, инициализируя его именем пользователя и паролем
    st = SpaceTrackClient(identity=username, password=password)
    # Выполнение запроса для диапазона дат:
    if not latest:
        # Определяем диапазон дат через оператор библиотеки
        daterange = op.inclusive_range(start_date, end_date)
        # Собственно выполняем запрос через st.tle
        data = st.tle(norad_cat_id=sat_id, orderby='epoch desc', limit=1, format='tle', epoch = daterange)
    # Выполнение запроса для актуального состояния
    else:
        # Выполняем запрос через st.tle_latest
        data = st.tle_latest(norad_cat_id=sat_id, orderby='epoch desc', limit=1, format='tle')
 
    # Если данные недоступны
    if not data:
        return 0, 0
 
    # Иначе возвращаем две строки
    tle_1 = data[0:69]
    tle_2 = data[70:139]
    return tle_1, tle_2

wndw = tk.Tk()
wndw.title('Расчет расстояния до спутника')

wndw_w = int(1366/2)
wndw_h = int(768/2)
wndw.geometry(f"{wndw_w}x{wndw_h}+{int(wndw_w/2)}+{int(wndw_h/2)}")

# здесь будем писать день наблюдения
tk.Label(wndw, text="Дата наблюдения (дд.мм.гггг): ").grid(row=0, column=0)

date_track = tk.Entry(wndw)
date_track.insert(0, "09.04.2022")
date_track.grid(row=0, column=1)

# время начала наблюдения
tk.Label(wndw, text="Время начала наблюдения (чч:мм:сс): ").grid(row=1, column=0)

time_start = tk.Entry(wndw)
time_start.insert(0, "20:03:30")
time_start.grid(row=1, column=1)

# время конца наблюдения
tk.Label(text="Время конца наблюдения (чч:мм:сс): ").grid(row=2, column=0)

time_stop = tk.Entry(wndw)
time_stop.insert(0, "20:10:30")
time_stop.grid(row=2, column=1)

# шаг в секундах
tk.Label(text="Шаг времени (с): ").grid(row=3, column=0)

step_sec = tk.Entry(wndw)
step_sec.insert(0, 30)
step_sec.grid(row=3, column=1)

# наша позиция
# широта
tk.Label(text="Наша широта (град): ").grid(row=4, column=0)

our_lat = tk.Entry(wndw)
our_lat.insert(0, 56.8411)
our_lat.grid(row=4, column=1)

# долгота
tk.Label(text="Наша долгота (град): ").grid(row=5, column=0)

our_lon = tk.Entry(wndw)
our_lon.insert(0, 60.6498)
our_lon.grid(row=5, column=1)

# высота подвеса антенны
tk.Label(text="Высота подвеса антенны (м): ").grid(row=6, column=0)

antenna_height = tk.Entry(wndw)
antenna_height.insert(0, 1.5)
antenna_height.grid(row=6, column=1)

# чувствительность приемника
tk.Label(text="Чувствительность приемника (дБм): ").grid(row=7, column=0)

Sens_line = tk.Entry(wndw)
Sens_line.insert(0, CurrentSens)
Sens_line.grid(row=7, column=1)

# КУ антенны
tk.Label(text="КУ антенны (дБ): ").grid(row=8, column=0)

Gr_line = tk.Entry(wndw)
Gr_line.insert(0, CurrentGr)
Gr_line.grid(row=8, column=1)



SatList = ttk.Combobox(wndw)

# имя выбранного спутника
tk.Label(text="Имя выбранного спутника: ").grid(row=10, column=0)

chosen_name_line = tk.Entry(wndw)
chosen_name_line.grid(row=10, column=1)

# статус
tk.Label(text="Статус: ").grid(row=11, column=0)

Status_line = tk.Entry(wndw)
Status_line.grid(row=11, column=1)

# частота сигнала (МГц)
tk.Label(text="Частота: ").grid(row=12, column=0)

frq_line = tk.Entry(wndw)
frq_line.grid(row=12, column=1)

# способ модуляции
tk.Label(text="Модуляция: ").grid(row=13, column=0)

Mod_line = tk.Entry(wndw)
Mod_line.grid(row=13, column=1)

# мощность передатчика
tk.Label(text="Мощность передатчика (мВт): ").grid(row=14, column=0)

Pt_line = tk.Entry(wndw)
Pt_line.grid(row=14, column=1)

# КУ антенны
tk.Label(text="КУ антенны (дБ): ").grid(row=15, column=0)

Gt_line = tk.Entry(wndw)
Gt_line.grid(row=15, column=1)

# На вход будем требовать идентификатор спутника, день (в формате date (y,m,d))
# шаг в минутах для определения положения спутника, путь для результирующего файла
def create_orbital_track_for_day():

    #sat_id=43937
    track_date=datetime.strptime(date_track.get(), "%d.%m.%Y")
    track_time_start=datetime.strptime(time_start.get(), "%H:%M:%S")
    track_time_stop=datetime.strptime(time_stop.get(), "%H:%M:%S")
    time_step=int(step_sec.get())

    # Для начала получаем TLE    
    # Запрашиваем самые последний набор TLE 
    # tle_1, tle_2 = get_spacetrack_tle(sat_id, None, None, USERNAME, PASSWORD, True)

    CurrentTle_1 = tle1_array[SatList.current() + 226]
    CurrentTle_2 = tle2_array[SatList.current() + 226]
 
    # Если не получилось добыть    
    #if not tle_1 or not tle_2:
    #    print('Impossible to retrieve TLE')     
    #    return

    # Создаём экземляр класса Orbital
    orb = Orbital("N", line1=CurrentTle_1, line2=CurrentTle_2)
 
    # Поскольку нам нужен подробный график, расстояние и бюджет канала будем считать с шагом по секундам
    # Для этого зададим начальную и конечную секунду, а также шаг
    start_sec = (track_time_start.hour - utc_shift) * 60 * 60 + track_time_start.minute * 60 + track_time_start.second
    stop_sec = (track_time_stop.hour - utc_shift) * 60 * 60 + track_time_stop.minute * 60 + track_time_stop.second
    current_sec = start_sec
 
    while current_sec <= stop_sec:
        # Часы, минуты и секунды, которые будем подставлять в формулу для рассчета положения спутника в это время
        utc_hour = int((current_sec // 60) // 60)

        utc_minutes = int((current_sec - utc_hour * 60 * 60) // 60)

        utc_seconds = int((current_sec - utc_hour * 60 * 60) - utc_minutes * 60)

        # И переменную с временем текущего шага в формате datetime
        utc_time = datetime(track_date.year, track_date.month, track_date.day, utc_hour, utc_minutes, utc_seconds)
 
        # Считаем положение спутника

        lon, lat, alt = orb.get_lonlatalt(utc_time)
        az, elev = orb.get_observer_look(utc_time, float(our_lon.get()), float(our_lat.get()), float(antenna_height.get())/1000)

        long_array.append(lon)
        lat_array.append(lat)
        alt_array.append(alt)

        az_array.append(az)
        elev_array.append(elev)
 
        current_sec += time_step

    if len(elev_array) > 0:
        tk.messagebox.showinfo(title='Внимание', message='Значения углов места получены')
    else:
        tk.messagebox.showerror(title='Внимание', message='Значения углов места не получены')
    
def count_recieve_pwr():

    CurrentFRQ = 433.456

    CurrentPt = 100

    CurrentGt = 13

    for i in range(len(dist_array)):
        if dist_array[i] > 0:
            recieve_pwr_array.append((CurrentPt/1000) * 10**(CurrentGt/10) * 10**(CurrentGr/10) * (LIGHTSPEED/(CurrentFRQ*1e6*4*math.pi*dist_array[i]*1000))**2)
            recieve_pwr_array[i] = 10 * math.log10(recieve_pwr_array[i]/(1e-3))
        else:
            recieve_pwr_array.append(0)

def count_distance():
    our_lon_pos =  float(our_lon.get())*math.pi/180
    our_lat_pos =  float(our_lat.get())*math.pi/180

    for i in range(len(elev_array)):
        # считаем только если уол места больше нуля
        if elev_array[i] > 0:
            # точка 1 - мы, точка 2 - спутник
            sat_lon_pos = long_array[i]*math.pi/180
            sat_lat_pos = lat_array[i]*math.pi/180

            delX = math.cos(sat_lat_pos)*math.cos(sat_lon_pos)-math.cos(our_lat_pos)*math.cos(our_lon_pos)
            delY = math.cos(sat_lat_pos)*math.sin(sat_lon_pos)-math.cos(our_lat_pos)*math.sin(our_lon_pos)
            delZ = math.sin(sat_lat_pos)-math.sin(our_lat_pos)

            Chord = math.sqrt(delX*delX + delY*delY + delZ*delZ)
            CenterAngle = 2*math.asin(Chord/2)*(180/math.pi)
            Chord *= EarthRadius

            FirstTerm = 2 * Chord * math.cos((CenterAngle/2 + elev_array[i])*math.pi/180)
            SecondTerm = 4 * Chord * Chord * math.cos((CenterAngle/2 + elev_array[i])*math.pi/180) * math.cos((CenterAngle/2 + elev_array[i])*math.pi/180)
            ThirdTerm = 4 * (Chord * Chord - alt_array[i] * alt_array[i])

            dist_array.append((FirstTerm + math.sqrt(SecondTerm - ThirdTerm))/2)
        else:
            dist_array.append(-1)

    count_recieve_pwr()

    plt.plot(range(len(recieve_pwr_array)), recieve_pwr_array)
    plt.hlines(float(Sens_line.get()), 0, len(recieve_pwr_array), color='red')
    plt.show()

def test1():
    print(int(step_sec.get()))

sat_names_array = []
tle1_array = []
tle2_array = []


def tle_db():
    FileDb = open("sts.txt", "r")

    LineCounters = 0
    for line in FileDb:
        if LineCounters % 3 == 0:
            sat_names_array.append(line)
            SatList['values'] = tuple(list(SatList['values']) + [str(line)])
        elif (LineCounters - 1) % 3 == 0:
            tle1_array.append(line)
        else:
            tle2_array.append(line)
        LineCounters += 1
    FileDb.close()

    SatList.grid(row=9, column=0)

def fill_entries(event):
    chosen_name_line.insert(0, SatList.get())

    FileInfo = open("sts_data.txt", "r")

    LineCounters = 0
    ReadNextAndLeft = 0

    for line in FileInfo:
        if ReadNextAndLeft == 1:
            NeedyInfo = line.split(" ")
            break
        if line == chosen_name_line.get():
            ReadNextAndLeft = 1
    
    Status_line.insert(0, NeedyInfo[0])

    frq_line.insert(0, NeedyInfo[1])

    Mod_line.insert(0, NeedyInfo[2])

    Pt_line.insert(0, NeedyInfo[3])

    Gt_line.insert(0, NeedyInfo[4])

def updateTLE():
    destination = 'sts.txt'
    url = 'http://r4uab.ru/satonline.txt'
    urllib.request.urlretrieve(url, destination)

TrackButton = tk.Button(wndw, text = 'Получить координаты', bg = 'yellow', command=create_orbital_track_for_day)
TrackButton.grid(row=0, column=3)

DistanceButton = tk.Button(wndw, text = 'Посчитать мощность', bg = 'yellow', command=count_distance)
DistanceButton.grid(row=1, column=3)

UploadTLEdb = tk.Button(wndw, text = 'Загрузить список спутников', command=tle_db)
UploadTLEdb.grid(row=2, column=3)

SatList.bind("<<ComboboxSelected>>", fill_entries)

UpdateTLEdb = tk.Button(wndw, text = 'Обновить TLE', command=updateTLE)
UpdateTLEdb.grid(row=3, column=3)

test = tk.Button(wndw, command=test1)
test.grid(row=1, column=4)

wndw.mainloop()

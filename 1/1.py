import csv
your_folder = '/home/han/test/weather_and_email_register/1'
path = your_folder + '/34300.01.01.2016.01.01.2017.1.0.0.ru.csv'
path_days_data = your_folder + '/days_data.csv'
lines = open(path, 'r').readlines()
days, mons, line_d = [], [], []
day_temp, mon_temp = [], []
day_windy, mon_windy = [], []
day_rrr, week_rrr = [], []
day_temp_dict, mon_temp_dict, mon_windy_dict, week_rrr_dict = {}, {}, {}, {}
week_counter = 0
with open(path_days_data, "w", newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=';')
    writer.writerow(['day', 'daily average temperature', 'average daily wind speed', 'daily rainfall'])
    for line in lines[7:]:
        cell = line.replace('"', '').split(';')
        day = cell[0].split(' ')[0]
        r_i = 23 if len(cell) == 30 else 24
        if day not in days:
            if len(day_temp):
                line_d.append(days[-1])
                line_d.append(sum(day_temp)/len(day_temp))
            if len(day_windy): line_d.append(sum(day_windy)/len(day_windy))
            if len(day_rrr): line_d.append(sum(day_rrr))
            if len(line_d):
                writer.writerow(line_d)
                line_d = []
            days.append(day)
            day_temp, day_windy, day_rrr = [], [], []
            day_temp.append(float(cell[1]))
            day_windy.append(float(cell[7]))
            if cell[r_i]:
                rrr = 0 if cell[r_i] == 'Следы осадков' else cell[r_i]
                day_rrr.append(float(rrr))
        else:
            day_temp.append(float(cell[1]))
            day_windy.append(float(cell[7]))
            if cell[r_i]:
                rrr = 0 if cell[r_i] == 'Следы осадков' else cell[r_i]
                day_rrr.append(float(rrr))
    writer.writerow([day, sum(day_temp)/len(day_temp), sum(day_windy)/len(day_windy), sum(day_rrr)])

with open(path_days_data, "r") as csv_file_day:
    lines_from_day = csv_file_day.readlines()
    for line_day in lines_from_day[1:]:
        cell_day = line_day.replace('\n', '').split(';')
        day_temp_dict.setdefault(cell_day[0], round(float(cell_day[1]), 3))
        if week_counter == 0:
            week_counter +=1
            fin_week = cell_day[0]
            if len(cell_day) == 4: week_rrr.append(float(cell_day[3]))
        else:
            week_counter +=1
            if len(cell_day) == 4: week_rrr.append(float(cell_day[3]))
            if week_counter == 7:
                start_week = cell_day[0]
                if len(cell_day) == 4: week_rrr.append(float(cell_day[3]))
                if len(week_rrr): week_rrr_dict.setdefault((start_week +' - ' + fin_week), sum(week_rrr))
                week_rrr = []
                week_counter = 0
        if not '2017' in cell_day[0]:
            mon = cell_day[0].split('.')[1]
            if mon not in mons:
                if len(mon_temp): mon_temp_dict.setdefault(mons[-1], round(sum(mon_temp)/len(mon_temp), 3))
                if len(mon_windy): mon_windy_dict.setdefault(mons[-1], round(sum(mon_windy)/len(mon_windy), 3))
                mons.append(mon)
                mon_temp, mon_windy = [], []
                mon_temp.append(float(cell_day[1]))
                mon_windy.append(float(cell_day[2]))
            else:
                mon_temp.append(float(cell_day[1]))
                mon_windy.append(float(cell_day[2]))
    mon_temp_dict.setdefault(mon, round((sum(mon_temp)/len(mon_temp)), 3))
    mon_windy_dict.setdefault(mon, round((sum(mon_windy)/len(mon_windy)), 3))

    list_d = list(day_temp_dict.items())
    list_d.sort(key=lambda i: i[1])
        
    list_m = list(mon_temp_dict.items())
    list_m.sort(key=lambda i: i[1])

    list_m_w = list(mon_windy_dict.items())
    list_m_w.sort(key=lambda i: i[1])

    list_w_r = list(week_rrr_dict.items())
    list_w_r.sort(key=lambda i: i[1])
    
    print('самый ветреный месяц - (месяц и средняя скорость ветра)-', list_m_w[-1])
    print('самый холодный месяц - (месяц и средняя температура) -', '\t', list_m[0])
    print('самый холодный день - (день и средняя температура) -', '\t', list_d[0])
    print('самый тёплый месяц - (месяц и средняя температура) -', '\t', list_m[-1])
    print('самый тёплый день - (день и средняя температура) -', '\t', list_d[-1])
    print('самая дождливая неделя - (период и количество осадков) -', list_w_r[-1])
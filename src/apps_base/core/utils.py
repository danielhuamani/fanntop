from datetime import datetime, date, timedelta
import math

def range_month():
    anio_hoy = create_from.year
    mes_initial = (datetime.now() - timedelta(days=5*30)).month
    anio_actual = (datetime.now() - timedelta(days=5*30)).year
    anio_today = anio_actual
    for mes in range(mes_initial, mes_initial+6, 1):
        mes_final = mes + 1
        if mes_final > 12:
            if mes == 12:
                mes_final = 1
            else:
                mes_final = mes_final - 12
                mes = mes - 12
            anio_hoy = anio_actual + 1
        mes_start = date(anio_today, mes, 1)
        mes_end = date(anio_hoy, mes_final, 1)
        anio_today = anio_hoy
        dic = {
            'mes_start': mes_start,
            'mes_end': mes_end
        }
        yield dic


def format_date(my_date):
    return datetime.strptime(my_date, '%d/%m/%Y')

def range_start_end():
    anio_hoy = datetime.now().year
    mes_end = datetime.now()
    mes_start = (datetime.now() - timedelta(days=5*30))
    return mes_end, mes_start

def month_initial():
    today = datetime.now()
    today_month = date(today.year, today.month, 1)
    return today_month

def today_date():
    today = datetime.now()
    return today.date()

def daterange(start_initial_date, end_initial_date):
    start_initial_date = format_date(start_initial_date)
    end_initial_date = format_date(end_initial_date)
    rest_date = end_initial_date - start_initial_date
    month = int(math.ceil(rest_date.days / 30))
    for n in range(1, month + 2):
        if n == 1:
            print('entroooo', start_initial_date)
            start_date = start_initial_date
            end_date = start_date + timedelta(31*n)
            print(end_date)
            yield {
                'mes_start': start_date,
                'mes_end':  datetime(end_date.year, end_date.month, 1)
            }
        elif n == (month):
            start_date = start_initial_date + timedelta(31*(n-1))
            start_date = datetime(start_date.year, start_date.month, 1)
            end_date = start_initial_date + timedelta(31*n)
            end_date = datetime(end_date.year, end_date.month, 1)
            yield {
                'mes_start': start_date,
                'mes_end':  end_initial_date
            }
        elif n == (month + 1):
            start_date = start_initial_date + timedelta(31*(n-1))
            end_date = end_initial_date
            yield {
                'mes_start': end_date,
                'mes_end':  ''
            }
        else:
            start_date = start_initial_date + timedelta(31*(n-1))
            end_date = start_initial_date + timedelta(31*n)
            start_date = datetime(start_date.year, start_date.month, 1)
            end_date = datetime(end_date.year, end_date.month, 1)
            yield {
                'mes_start': start_date,
                'mes_end': end_date
            }

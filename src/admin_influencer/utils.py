from datetime import datetime, date, timedelta

def range_month():
    anio_hoy = datetime.now().year
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

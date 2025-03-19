import requests  # Libreria para hacer requests HTTP, la uso con APIs
from datetime import date  # Liberaria para usar cosas de dates


# Recibe un a;o y retorna la url formada para ese a;o
def get_url(year):
    return f"https://nolaborables.com.ar/api/v2/feriados/{year}"


months = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]
days = ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]


# Funcion para obtener el dia de la semana
def day_of_week(day, month, year):
    return days[date(year, month, day).weekday()]


# Busca y presenta el proximo feriado
class NextHoliday:
    def __init__(self):
        # A;o actual
        self.year = date.today().year
        # self.loading == True  <==> self.holiday = None
        # self.loading == False <==> self.holiday = <Algo>
        # Creo, self loading significa que se esta buscando un dato
        self.loading = True
        # Inicialmente no hay ningun dato asignado
        self.holiday = None

    # Busca el siguiente feriado desde hoy
    def set_next(self, holidays):
        # Dia de hoy
        now = date.today()
        # Saco el dia y mes actual de hoy y lo guardo en today
        today = {"day": now.day, "month": now.month}

        # El siguiente feriado es
        holiday = next(
            # Se itera sobre todos los holidays y se busca el primero que
            # (A)  holiday['mes'] == today['mes'] && holiday['dia'] > toda['dia']
            #               || (or)
            # (B) holiday['mes'] > today['month']
            # Basicamente,
            # A -> El primer feriado de este mes posterior al dia de hoy
            # B -> El primer feriado del siguient mes (usado si el mes actual
            (
                h
                for h in holidays
                if h["mes"] == today["month"]
                and h["dia"] > today["day"]
                or h["mes"] > today["month"]
            ),
            # Fallback en caso de no encontrar el holiday
            holidays[0],
        )

        # Ya encontre feriado
        self.loading = False
        # Y es el que acabo de calcular
        self.holiday = holiday

    # Funcion para obtener todos los feriados de un a;o
    # Hago un HTTP request a
    # https://nolaborables.com.ar/api/v2/feriados/{year}
    # Con el year agarrado de self.year (year actual)
    def fetch_and_set_holidays(self):
        # Guardo la response
        response = requests.get(get_url(self.year))
        # response como json en data
        data = response.json()
        # Busco el feriado desde el json
        self.set_next(data)

    def render(self):
        if self.loading:
            print("Buscando...")
        else:
            print("Próximo feriado")
            print(self.holiday["motivo"])  ## Dia nacional de ...
            print("Fecha:")  ## Domingo X de Y
            print(day_of_week(self.holiday["dia"], self.holiday["mes"] - 1, self.year))
            print(self.holiday["dia"])
            print(months[self.holiday["mes"] - 1])
            print("Tipo:")
            print(self.holiday["tipo"])

    # La idea es que fetchee todo el json del a;o y nosotros hagamos cosas con
    # eso
    def fetch_holidays_by_type(self, type):
        if (  ## El type es uno valido hago lo mio
            type
            == "inamovible" | type
            == "trasladable" | type
            == "nolaborable" | type
            == "puente"
        ):
            # Guardo la response
            response = requests.get(get_url(self.year))
            # response como json en data
            data = response.json()
            return data
        else:  ## Salgo con error
            exit(1)


# Seteo el objeto next_holiday
next_holiday = NextHoliday()
## Lo comento por ahora
# next_holiday.fetch_and_set_holidays()
# next_holiday.render()

# Printeo el json obtenido, es de todo el a;o
print(next_holiday.fetch_holidays_by_type(type))

from flask import Flask, jsonify, request
import random       # Para trabajar las sugerencias aleatorias de películas
import unicodedata  # Para normalizar los géneros y títulos de películas
from proximo_feriado import NextHoliday

app = Flask(__name__)

peliculas = [
    {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
    {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'},
    {'id': 3, 'titulo': 'Interstellar', 'genero': 'Ciencia ficción'},
    {'id': 4, 'titulo': 'Jurassic Park', 'genero': 'Aventura'},
    {'id': 5, 'titulo': 'The Avengers', 'genero': 'Acción'},
    {'id': 6, 'titulo': 'Back to the Future', 'genero': 'Ciencia ficción'},
    {'id': 7, 'titulo': 'The Lord of the Rings', 'genero': 'Fantasía'},
    {'id': 8, 'titulo': 'The Dark Knight', 'genero': 'Acción'},
    {'id': 9, 'titulo': 'Inception', 'genero': 'Ciencia ficción'},
    {'id': 10, 'titulo': 'The Shawshank Redemption', 'genero': 'Drama'},
    {'id': 11, 'titulo': 'Pulp Fiction', 'genero': 'Crimen'},
    {'id': 12, 'titulo': 'Fight Club', 'genero': 'Drama'}
]


# --------------------------- FUNCIONES AUXILIARES ---------------------------
# def obtener_nuevo_id():
#     if len(peliculas) > 0:
#         ultimo_id = peliculas[-1]['id']
#         return ultimo_id + 1
#     else:
#         return 1

# Nueva versión de obtener_nuevo_id() que surge del siguiente problema: al eli-
# minar una película, por ejemplo aquella con el ID 5, deja ese espacio vacío.
# Cuando se busca incorporar un nuevo film a la DB, esta tomará el IDfinal+1,
# dejando la lista con IDs 1,2,3,4,6,...,12,13 en este caso. De esta manera,
# ese espacio libre es ocupado al instante, y solo agrega una al final cuando
# la secuencia de IDs de películas es continua 
def obtener_nuevo_id():
    ids_existentes = {pelicula['id'] for pelicula in peliculas}
    nuevo_id = 1
    while nuevo_id in ids_existentes:
        nuevo_id += 1
    return nuevo_id


def normalizar_texto(texto):
    # Convierte el texto a minúsculas
    texto = texto.lower()

    # NFKD separa las tildes de las letras. Por ejemplo 'á' => 'a' + '´'
    # Se codifica el texto en ASCII, descartando caracteres especiales y se
    # decodifica en UTF-8 para tener la cadena normalizada
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('utf-8')
    return texto


# Coloca la primera letra de un 'texto' en mayúscula, si es que existe
def capitalizar_primer_letra(texto):
    return texto[0].upper() + texto[1:] if texto else texto

# --------------------------- FUNCIONES PRINCIPALES ---------------------------
@app.get("/")
def obtener_peliculas():
    return peliculas


@app.get("/peliculas/<int:id>")
def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles

    # Se asegura que el ID sea positivo
    if id == 0:
        return jsonify({'error': 'Se debe un ingresar un número positivo '
                        'como ID'}), 400 # HTTP Bad Request

    # Busca la película por su ID en la DB
    for pelicula in peliculas:
        if pelicula['id'] == id:
            pelicula_encontrada = pelicula
            return jsonify(pelicula_encontrada), 200 # HTTP OK

    # Si la película no está en la DB, envía el siguiente mensaje
    return jsonify({'mensaje': 'Película no encontrada'}), 404 # HTTP Not Found


@app.post("/peliculas")
def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        # De esta forma todos los títulos y géneros añadidos iniciarán con ma-
        # yúsculas, el resto todo minúsculas y se eliminarán las tildes.
        # Soluciona un posible caso particular donde se ingresa:
        # '{"titulo": "dÉADṔOol", "genero": "cÓmeDiá"}'
        # Transformándolo a:
        # '{"titulo": "Deadpool", "genero": "Comedia"}'
        'titulo': capitalizar_primer_letra(normalizar_texto(request.json['titulo'])),
        'genero': capitalizar_primer_letra(normalizar_texto(request.json['genero']))
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula), 201  # HTTP Created


@app.put("/peliculas/<int:id>")
def actualizar_pelicula(id):
    # Se asegura que el ID sea positivo
    if id == 0:
        return jsonify({'error': 'Se debe ingresar un número positivo como ID'}), 400

    # Busca la película por su ID y actualiza su título y género
    for pelicula_a_actualizar in peliculas:
        if pelicula_a_actualizar['id'] == id:
            # Se conserva el título tal como se recibe (solo se capitaliza la primera letra)
            # No normalizo para pasar el test
            titulo = capitalizar_primer_letra(request.json['titulo'])
            # Normalizo el genero porque puedo buscar por genero
            genero = capitalizar_primer_letra(normalizar_texto(request.json['genero']))

            pelicula_a_actualizar['titulo'] = titulo
            pelicula_a_actualizar['genero'] = genero

            # Retorna la película actualizada
            return jsonify(pelicula_a_actualizar), 200
    
    # En caso de que la película no esté en la DB, envía el siguiente mensaje
    return jsonify({'mensaje': 'Película no encontrada'}), 404


@app.delete("/peliculas/<int:id>")
def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla
    
    # Se asegura que el ID sea positivo
    if id == 0:
        return jsonify({'error': 'Se debe un ingresar número positivo '
                        'como ID'}), 400 # HTTP Bad Request

    # Busca la película por su ID y la remueve de la DB
    for pelicula_a_eliminar in peliculas:
        if pelicula_a_eliminar['id'] == id:
            peliculas.remove(pelicula_a_eliminar)
            return jsonify({'mensaje': 'Película eliminada '
                            'correctamente'}), 200 # HTTP OK
    
    # En caso de fallo, devuelve la siguiente advertencia
    return jsonify({'mensaje': 'No se pudo eliminar la película '
                    'correctamente'}), 404 # HTTP Not Found

    
@app.get("/peliculas/genero/<string:genero>")
def obtener_pelicula_por_genero(genero):
    # Creo una lista con las películas del género indicado
    filtradas = [
        p for p in peliculas 
        if normalizar_texto(p['genero']) == normalizar_texto(genero)
    ]
    if not filtradas:
        return jsonify({'mensaje': 'No se encontraron películas del '
                        'género seleccionado'}), 404 # HTTP Not Found
    
    return jsonify(filtradas), 200 # HTTP OK


@app.get("/peliculas/titulo/<string:titulo>")
def buscar_peliculas_por_titulo(titulo):
    # Creo una lista con las películas que contengan el string en el título
    filtradas = [
        p for p in peliculas 
        if normalizar_texto(titulo) in normalizar_texto(p['titulo'])
    ]
    if not filtradas:
        return jsonify({'mensaje': 'No se encontraron películas '
                        'relacionadas'}), 404 # HTTP Not Found
    
    return jsonify(filtradas), 200 # HTTP OK


@app.get("/peliculas/recomendacion")
def sugerir_pelicula_aleatoria():
    # random escoge una película cualquiera del json de películas
    pelicula_aleatoria = random.choice(peliculas)
    return jsonify(pelicula_aleatoria), 200 # HTTP OK


@app.get("/peliculas/recomendacion/<string:genero>")
def sugerir_pelicula_aleatoria_por_genero(genero):
    # En caso de haber mandado 'ciencia_ficcion' o 'thriller-policial' como 
    # género, por ejemplo
    genero = genero.replace("-", " ")
    genero = genero.replace("_", " ")

    # Normalizamos el género para aceptar varias posibilidades como: 
    #   - ACCION
    #   - accion
    #   - cÍÉncÍÁ%20fÍccÍÓn
    #   - aVeNtUrA
    # y otras posibles combinaciones bizarras de caracteres...
    genero = normalizar_texto(genero) 

    # Arma una lista compuesta únicamente con las películas del género dado.
    # Vale aclarar que compara ambos géneros ya normalizados, tanto el ingresa-
    # do por el usuario como el del json
    peliculas_filtradas = [
        p for p in peliculas if normalizar_texto(p['genero']) == genero
    ]

    # Si la lista está vacía, significa que no hay películas de tal género y se
    # envía una advertencia. Caso contrario, random escoge una película cual-
    # quiera de la lista previamente creada
    if peliculas_filtradas:
        pelicula_elegida = random.choice(peliculas_filtradas)
        return jsonify(pelicula_elegida), 200 # HTTP OK
    else:
        return jsonify({'error': 'No se encontraron películas del género '
                        'seleccionado'}), 404 # HTTP Not Found
        

"""
    Aca abajo esta lo necesario para la parte b) del modulo 2
"""

@app.get("/peliculas/recomendacion/feriado")
def recomendar():
    # Capturo el valor de la key json (ej: Crimen)
    genero = request.json['genero']
    # Genero el json de películas 
    json_pelis = obtener_peliculas()
    # Me da una lista de jsons de pelis h que cumplen con h['genero'] == genero
    filtered_list = list(filter(lambda h: h['genero'] == genero, json_pelis))
    # Elijo un elemento aleatorio de la lista
    peli_elegida = random.choice(filtered_list)
    # Capturo el próximo feriado
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    holiday = next_holiday.holiday

    # Genero el json de output
    output = { 'holiday' : holiday ,'pelicula' : peli_elegida }

    return jsonify(output)


if __name__ == '__main__':
    app.run()

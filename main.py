from flask import Flask, jsonify, request
import random
from proximo_feriado import NextHoliday



app = Flask(__name__)

peliculas = [ ## Esto es un json <-- ???
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


# @app.get("/") # Usamos esto en vez de la linea 23
def obtener_peliculas():
    return peliculas


#@app.get("/peliculas/<int:id>")
def obtener_pelicula(id):
    # Lógica para buscar la película por su ID y devolver sus detalles

    # Busca la película por su ID en la DB
    for pelicula in peliculas:
        if pelicula['id'] == id:
            pelicula_encontrada = pelicula
            return jsonify(pelicula_encontrada)

    # Si la película no está en la DB, envía el siguiente mensaje
    return jsonify({'mensaje': 'Película no encontrada'}), 404 # Error 404


# @app.post("/peliculas")
def agregar_pelicula():
    nueva_pelicula = {
        'id': obtener_nuevo_id(),
        'titulo': request.json['titulo'],
        'genero': request.json['genero']
    }
    peliculas.append(nueva_pelicula)
    print(peliculas)
    return jsonify(nueva_pelicula)


# @app.put("/peliculas/<int:id>")
def actualizar_pelicula(id):
    # Lógica para buscar la película por su ID y actualizar sus detalles

    # Busca la película por su ID y actualiza su título y género
    for pelicula_a_actualizar in peliculas:
        if pelicula_a_actualizar['id'] == id:
            pelicula_a_actualizar['titulo'] = request.json["titulo"]
            pelicula_a_actualizar['genero'] = request.json["genero"]

            # Si la encuentra, la película se actualiza
            pelicula_actualizada = pelicula_a_actualizar
            return jsonify(pelicula_actualizada)
    
    # En caso de que la película no esté en la DB, envía el siguiente mensaje
    return jsonify({'mensaje': 'Película no encontrada'}), 404


# @app.delete("/peliculas/<int:id>")
def eliminar_pelicula(id):
    # Lógica para buscar la película por su ID y eliminarla

    # Busca la película por su ID y la remueve de la DB
    for pelicula_a_eliminar in peliculas:
        if pelicula_a_eliminar['id'] == id:
            peliculas.remove(pelicula_a_eliminar)
            return jsonify({'mensaje': 'Película eliminada correctamente'})
    
    # En caso de fallo, devuelve la siguiente advertencia
    return jsonify({'mensaje': 'No se pudo eliminar la película correctamente'}), 404


def obtener_nuevo_id():
    if len(peliculas) > 0:
        ultimo_id = peliculas[-1]['id']
        return ultimo_id + 1
    else:
        return 1


"""
    Aca abajo esta lo necesario para la parte b) del modulo 2
"""

# @app.get("/recomendacion")
def recomendar():
    # Capturo el valor de la key json (ej: Crimen)
    genero = request.json['genero']
    # Genero el json de peliculas 
    json_pelis = obtener_peliculas()
    # Me da una lista de jsons de pelis h que cumplen con h['genero'] == genero
    filtered_list = list(filter(lambda h: h['genero'] == genero, json_pelis))
    # Elijo un elemento aleatorio de la lista
    peli_elegida = random.choice(filtered_list)
    # Capturo el proximo feriado
    next_holiday = NextHoliday()
    next_holiday.fetch_holidays()
    holiday = next_holiday.holiday

    # Genero el json de output
    output = { 'holiday' : holiday ,'pelicula' : peli_elegida }

    return jsonify(output)


app.add_url_rule('/peliculas', 'obtener_peliculas', obtener_peliculas, methods=['GET'])
app.add_url_rule('/peliculas/<int:id>', 'obtener_pelicula', obtener_pelicula, methods=['GET'])
app.add_url_rule('/peliculas', 'agregar_pelicula', agregar_pelicula, methods=['POST'])
app.add_url_rule('/peliculas/<int:id>', 'actualizar_pelicula', actualizar_pelicula, methods=['PUT'])
app.add_url_rule('/peliculas/<int:id>', 'eliminar_pelicula', eliminar_pelicula, methods=['DELETE'])

if __name__ == '__main__':
    app.run()

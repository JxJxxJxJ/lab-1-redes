import requests

# Obtener todas las películas
response = requests.get('http://localhost:5000/')
peliculas = response.json()
print("Películas existentes:")
for pelicula in peliculas:
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
print()

# Agregar una nueva película
nueva_pelicula = {
    'titulo': 'Pelicula de prueba',
    'genero': 'Acción'
}
response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
if response.status_code == 201:
    pelicula_agregada = response.json()
    print("Película agregada:")
    print(f"ID: {pelicula_agregada['id']}, Título: {pelicula_agregada['titulo']}, Género: {pelicula_agregada['genero']}")
else:
    print("Error al agregar la película.")
print()

# Obtener detalles de una película específica
id_pelicula = 1  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
else:
    print("Error al obtener los detalles de la película.")
print()

# Actualizar los detalles de una película
id_pelicula = 1  # ID de la película a actualizar
datos_actualizados = {
    'titulo': 'Nuevo título',
    'genero': 'Comedia'
}
response = requests.put(f'http://localhost:5000/peliculas/{id_pelicula}', json=datos_actualizados)
if response.status_code == 200:
    pelicula_actualizada = response.json()
    print("Película actualizada:")
    print(f"ID: {pelicula_actualizada['id']}, Título: {pelicula_actualizada['titulo']}, Género: {pelicula_actualizada['genero']}")
else:
    print("Error al actualizar la película.")
print()

# Eliminar una película
id_pelicula = 1  # ID de la película a eliminar
response = requests.delete(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 200:
    print("Película eliminada correctamente.")
else:
    print("Error al eliminar la película.")
print()

# Obtener todas las películas de un género
genero = "CIénCia fÍcCion" # Genero a obtener y testeamos la normalización del género
response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
if response.status_code == 200:
    obtener_pelicula_por_genero = response.json()
    print("Películas por género:")
    for pelicula in obtener_pelicula_por_genero:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, " 
              f"Género: {pelicula['genero']}")
else:
    print(f"Error al obtener películas del género '{genero}'.")
print()

# Buscar peliculas que contengan en el título el string ingresado
titulo = "tHé" # String a buscar entre los títulos existentes 
               # y testeamos la normalización del título
response = requests.get(f'http://localhost:5000/peliculas/titulo/{titulo}')
if response.status_code == 200:
    buscar_peliculas_por_titulo = response.json()
    print("Películas por título sugerido:")
    for pelicula in buscar_peliculas_por_titulo:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, " 
              f"Género: {pelicula['genero']}")
else:
    print(f"Error al obtener películas con el titulo '{titulo}'.")
print()

# Sugerir una película aleatoria
response = requests.get('http://localhost:5000/peliculas/recomendacion')
if response.status_code == 200:
    pelicula_sugerida = response.json()
    print("Película sugerida:")
    print(f"ID: {pelicula_sugerida['id']}, Título: {pelicula_sugerida['titulo']}, Género: {pelicula_sugerida['genero']}")
else:
    print("Error al escoger una película aleatoria.")
print()

# Sugerir una película aleatoria por género (género existente en la DB)
genero = "aCcÍón"  # Para testear también la normalización del género
response = requests.get(f'http://localhost:5000/peliculas/recomendacion/{genero}')
if response.status_code == 200:
    pelicula_sugerida_genero = response.json()
    print("Película sugerida del género seleccionado:")
    print(f"ID: {pelicula_sugerida_genero['id']}, Título: {pelicula_sugerida_genero['titulo']}, Género: {pelicula_sugerida_genero['genero']}")
    print("Test aprobado.")
else:
    print(f'Error al escoger una película del género {genero}. Test no aprobado')
print()

# Sugerir una película aleatoria por género (género inexistente en la DB)
genero = "terror"  # Para testear también la normalización del género
response = requests.get(f'http://localhost:5000/peliculas/recomendacion/{genero}')
if response.status_code == 200:
    pelicula_sugerida_genero = response.json()
    print("Película sugerida del género seleccionado:")
    print(f"ID: {pelicula_sugerida_genero['id']}, Título: {pelicula_sugerida_genero['titulo']}, Género: {pelicula_sugerida_genero['genero']}")
    print("Test no aprobado.")
else:
    print(f'Error al escoger una película del género {genero}. Test aprobado.')
print()

# Obtener detalles de una película específica cuyo ID es 0
id_pelicula = 0  # ID de la película a obtener
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 400:
    print("Error al escoger un ID igual a 0. Test aprobado.")
else:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
    print("Test no aprobado.")
print()

# Obtener detalles de una película específica que no existe en la DB
id_pelicula = 253  # ID de la película a obtener (la cual no existe)
response = requests.get(f'http://localhost:5000/peliculas/{id_pelicula}')
if response.status_code == 404:
    print("Error al buscar la película (no existe). Test aprobado.")
else:
    pelicula = response.json()
    print("Detalles de la película:")
    print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
    print("Test no aprobado.")
print()

# Obtener todas las películas de un género (género existente en la DB)
genero = "romance"  
response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
if response.status_code == 200:
    peliculas_obtenidas_por_genero = response.json()
    print("Películas encontradas del género seleccionado:")
    for pelicula in peliculas_obtenidas_por_genero:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
    print("Test no aprobado.")
else:
    print(f"Error al obtener las películas del género '{genero}'. Test aprobado.")
print()


# Buscar peliculas que contengan en el título el string ingresado (título inexistente)
titulo = "viernes"  
response = requests.get(f'http://localhost:5000/peliculas/titulo/{titulo}')
if response.status_code == 200:
    peliculas_por_titulo = response.json()
    print("Películas con el título seleccionado:")
    for pelicula in peliculas_por_titulo:
        print(f"ID: {pelicula['id']}, Título: {pelicula['titulo']}, Género: {pelicula['genero']}")
    print("Test no aprobado.")
else:
    print(f"Error al encontrar las películas con '{titulo}' en su título. Test aprobado.")
print()

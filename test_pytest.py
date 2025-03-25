import requests
import pytest
import requests_mock

@pytest.fixture
def mock_response():
    with requests_mock.Mocker() as m:
        # Simulamos la respuesta para obtener todas las películas
        m.get('http://localhost:5000/', json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para agregar una nueva película
        m.post('http://localhost:5000/peliculas', status_code=201, json={'id': 3, 'titulo': 'Pelicula de prueba', 'genero': 'Acción'})

        # Simulamos la respuesta para obtener detalles de una película específica
        m.get('http://localhost:5000/peliculas/1', json={'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'})

        # Simulamos la respuesta para actualizar los detalles de una película
        m.put('http://localhost:5000/peliculas/1', status_code=200, json={'id': 1, 'titulo': 'Nuevo título', 'genero': 'Comedia'})

        # Simulamos la respuesta para actualizar los detalles de una 
        # película con ID = 0
        m.put('http://localhost:5000/peliculas/0', status_code=400, json=
              {'error': 'Se debe ingresar un número positivo como ID'})

        # Simulamos la respuesta para actualizar los detalles de una 
        # película no encontrada
        m.put('http://localhost:5000/peliculas/999', status_code=404, json=
              {'mensaje': 'Película no encontrada'})

        # Simulamos la respuesta para eliminar una película
        m.delete('http://localhost:5000/peliculas/1', status_code=200)

        # Simulamos la respuesta para eliminar una película con ID = 0
        m.delete('http://localhost:5000/peliculas/0', status_code=400, json=
                 {'error': 'Se debe un ingresar número positivo como ID'})
        # Simulamos la respuesta para eliminar una película con ID = 0
        m.delete('http://localhost:5000/peliculas/999', status_code=404, json=
                 {'mensaje': 'No se pudo eliminar la película correctamente'})
        
        # Simulamos la respuesta para obtener películas por género
        m.get('http://localhost:5000/peliculas/genero/dRámA', status_code=200, json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulados la respuesta para obtener películas por género con fallo
        m.get('http://localhost:5000/peliculas/genero/romance', status_code=404)


        # Simulamos la respuesta para buscar películas por título
        m.get('http://localhost:5000/peliculas/titulo/loRd of THE', status_code=200, json=[
            {'id': 1, 'titulo': 'Indiana Jones', 'genero': 'Acción'},
            {'id': 2, 'titulo': 'Star Wars', 'genero': 'Acción'}
        ])

        # Simulamos la respuesta para buscar películas por título con fallo
        m.get('http://localhost:5000/peliculas/titulo/viernes', status_code=404)

        # Simulamos la respuesta al sugerir una película aleatoria
        m.get('http://localhost:5000/peliculas/recomendacion', status_code=200)

        # Simulamos la respuesta al sugerir una película aleatoria de acción
        m.get('http://localhost:5000/peliculas/recomendacion/aCcÍón', status_code=200)

        # Simulamos la respuesta al sugerir una película aleatoria de terror, género inexistente en la DB
        m.get('http://localhost:5000/peliculas/recomendacion/terror', status_code=404)

        # Simulamos la respuesta para obtener detalles de una película ingresando el ID 0 (Bad Request)
        m.get('http://localhost:5000/peliculas/0', status_code=400)

        # Simulamos la respuesta para obtener detalles de una película inexistente en la DB
        m.get('http://localhost:5000/peliculas/253', status_code=404)

        yield m

def test_obtener_peliculas(mock_response):
    response = requests.get('http://localhost:5000/')
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_agregar_pelicula(mock_response):
    nueva_pelicula = {'titulo': 'Pelicula de prueba', 'genero': 'Acción'}
    response = requests.post('http://localhost:5000/peliculas', json=nueva_pelicula)
    assert response.status_code == 201
    assert response.json()['id'] == 3

def test_obtener_detalle_pelicula(mock_response):
    response = requests.get('http://localhost:5000/peliculas/1')
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Indiana Jones'

def test_actualizar_detalle_pelicula(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/1', json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()['titulo'] == 'Nuevo título'

def test_actualizar_detalle_pelicula_fallo_id(mock_response):
    response = requests.put('http://localhost:5000/peliculas/0', json={'titulo': 'Título inválido', 'genero': 'Acción'})
    assert response.status_code == 400

def test_actualizar_detalle_pelicula_no_encontrada(mock_response):
    datos_actualizados = {'titulo': 'Nuevo título', 'genero': 'Comedia'}
    response = requests.put('http://localhost:5000/peliculas/999', json=datos_actualizados)
    assert response.status_code == 404

def test_eliminar_pelicula(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/1')
    assert response.status_code == 200

def test_eliminar_pelicula_fallo_id(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/0')
    assert response.status_code == 400

def test_eliminar_pelicula_no_encontrada(mock_response):
    response = requests.delete('http://localhost:5000/peliculas/999')
    assert response.status_code == 404

def test_obtener_pelicula_por_genero_exito(mock_response):
    genero = "dRámA"
    response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
    assert response.status_code == 200


def test_obtener_pelicula_por_genero_fallo(mock_response):
    genero = "romance"
    response = requests.get(f'http://localhost:5000/peliculas/genero/{genero}')
    assert response.status_code == 404

def test_buscar_peliculas_por_titulo_exito(mock_response):
    titulo = "loRd of THE"
    response = requests.get(f'http://localhost:5000/peliculas/titulo/{titulo}')
    assert response.status_code == 200

def test_buscar_peliculas_por_titulo_fallo(mock_response):
    titulo = "viernes"
    response = requests.get(f'http://localhost:5000/peliculas/titulo/{titulo}')
    assert response.status_code == 404

def test_sugerir_pelicula_aleatoria(mock_response):
    response = requests.get('http://localhost:5000/peliculas/recomendacion')
    assert response.status_code == 200

def test_sugerir_pelicula_aleatoria_por_genero_exito(mock_response):
    genero = "aCcÍón"
    response = requests.get(f'http://localhost:5000/peliculas/recomendacion/{genero}')
    assert response.status_code == 200

def test_sugerir_pelicula_aleatoria_por_genero_fallo(mock_response):
    genero = "terror"
    response = requests.get(f'http://localhost:5000/peliculas/recomendacion/{genero}')
    assert response.status_code == 404

def test_obtener_detalle_pelicula_id0(mock_response):
    response = requests.get('http://localhost:5000/peliculas/0')
    assert response.status_code == 400

def test_obtener_detalle_pelicula_inexistente(mock_response):
    response = requests.get('http://localhost:5000/peliculas/253')
    assert response.status_code == 404
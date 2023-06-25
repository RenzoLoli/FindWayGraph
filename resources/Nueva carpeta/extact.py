import pandas as pd
import requests


# Leer el archivo CSV existente
df = pd.read_csv('datos_originales.csv', delimiter=';')

# Crear columnas vacías para los campos de respuesta de la API
df['osmid'] = ''
df['oneway'] = ''
df['lanes'] = ''
df['name'] = ''
df['highway'] = ''
df['maxspeed'] = ''
df['reversed'] = ''
df['length'] = ''
df['geometry'] = ''
df['bridge'] = ''
df['ref'] = ''
df['junction'] = ''
df['tunnel'] = ''
df['access'] = ''

# URL de la API de OpenStreetMap
url = 'https://nominatim.openstreetmap.org/search'

# Iterar sobre las filas del DataFrame
for index, row in df.iterrows():
    # Obtener los valores de la fila
    lugar = row['name']

    # Parámetros de la solicitud
    params = {
    'q': 'Lima, Perú',  # Ciudad y país que deseas buscar
    'format': 'json'  # Formato de la respuesta
    }
    # Realizar la solicitud GET a la API
    response = requests.get(url, params=params)

    # Verificar el estado de la respuesta
    if response.status_code == 200:
        # La solicitud fue exitosa
        data = response.json()  # Convertir la respuesta a JSON

        # Extraer los campos relevantes de la respuesta y asignarlos a las columnas correspondientes
        if data:
            result = data[0]
            df.at[index, 'osmid'] = result.get('osm_id', '')
            df.at[index, 'oneway'] = result.get('oneway', '')
            df.at[index, 'lanes'] = result.get('lanes', '')
            df.at[index, 'name'] = result.get('display_name', '')
            df.at[index, 'highway'] = result.get('highway', '')
            df.at[index, 'maxspeed'] = result.get('maxspeed', '')
            df.at[index, 'reversed'] = result.get('reversed', '')
            df.at[index, 'length'] = result.get('length', '')
            df.at[index, 'geometry'] = result.get('geometry', '')
            df.at[index, 'bridge'] = result.get('bridge', '')
            df.at[index, 'ref'] = result.get('ref', '')
            df.at[index, 'junction'] = result.get('junction', '')
            df.at[index, 'tunnel'] = result.get('tunnel', '')
            df.at[index, 'access'] = result.get('access', '')

    else:
        # La solicitud no fue exitosa
        print('Error en la solicitud:', response.status_code)

# Guardar el DataFrame en un nuevo archivo CSV
df.to_csv('datos_actualizados.csv', index=False, sep=';')
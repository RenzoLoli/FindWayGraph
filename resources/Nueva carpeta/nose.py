import csv
import requests

def obtener_datos_zona():
    # URL de la API Overpass
    url = 'https://overpass-api.de/api/interpreter'

    # Consulta Overpass para obtener los datos de una zona específica (área rectangular)
    query = '''
    [out:json];
    area["name"="Lima Metropolitana"]->.a;
    (
      node(area.a);
      way(area.a);
      relation(area.a);
    );
    out body;
    >;
    out skel qt;
    '''

    parametros = {
        'data': query
    }

    try:
        response = requests.get(url, params=parametros)

        # Verifica el estado de la respuesta
        if response.status_code == 200:
            datos_zona = response.json()  # Convierte la respuesta JSON en un diccionario o lista de Python
            return datos_zona
        else:
            print('La solicitud no fue exitosa. Código de estado:', response.status_code)
    except requests.exceptions.RequestException as e:
        print('Error de conexión:', e)

    return None

# Llamada a la función para obtener los datos de la zona
datos_zona = obtener_datos_zona()
if datos_zona is not None:
    # Verificar si los datos están en formato de lista o diccionario
    if isinstance(datos_zona, list):
        datos = datos_zona
    elif isinstance(datos_zona, dict):
        datos = datos_zona.get('elements', [])

    # Verificar si existen datos
    if datos:
        # Ruta del archivo CSV de salida
        archivo_csv = 'datos_zona.csv'

        # Abrir el archivo CSV en modo escritura
        with open(archivo_csv, 'w', newline='') as archivo:
            # Crear el escritor CSV
            escritor_csv = csv.DictWriter(archivo, fieldnames=datos[0].keys())

            # Escribir la cabecera
            escritor_csv.writeheader()

            # Escribir los datos
            escritor_csv.writerows(datos)

        print(f"Los datos se han exportado correctamente en el archivo '{archivo_csv}'.")
    else:
        print("No se encontraron datos para exportar.")

import requests

# Definir el nombre del lugar de interés
nombre_lugar = "Lima Peru"

# Codificar el nombre del lugar para incluirlo en la URL de la solicitud
nombre_lugar_codificado = requests.utils.quote(nombre_lugar)

# Construir la URL de la API de búsqueda de OpenStreetMap (Nominatim)
url = f"https://nominatim.openstreetmap.org/search?format=json&q={nombre_lugar_codificado}"
print(url)
# Realizar la solicitud a la API de búsqueda
# response = requests.get(url)

# # Verificar el estado de la respuesta
# if response.status_code == 200:
#     # Obtener los datos JSON de la respuesta
#     data = response.json()
    
#     if data:
#         # Obtener la primera coincidencia (lugar) de la lista de resultados
#         primer_lugar = data[0]
        
#         # Procesar los datos como desees
#         # Por ejemplo, imprimir el resultado completo
#         print(primer_lugar)
#     else:
#         print("No se encontraron resultados para el lugar especificado.")
# else:
#     print("Error al realizar la solicitud:", response.status_code)
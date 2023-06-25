import overpy
from overpy import Overpass
api = overpy.Overpass()

# Definir el nombre del lugar específico
place_name = "San Miguel Lima Peru"

# Definir la consulta Overpass con el filtro de nombre
query = """
    way(around:1000, lat, lon)["name"="{place_name}"];
    out body;
""".format(place_name=place_name)

# Ejecutar la consulta
result = api.query(query)

# Obtener los campos deseados de los elementos encontrados
for way in result.ways:
    u = way.u  # ID único del elemento
    v = way.v  # Versión del elemento
    key = way.tags.get("key")  # Valor de la etiqueta "key"
    osmid = way.tags.get("osmid")  # Valor de la etiqueta "osmid"
    oneway = way.tags.get("oneway")  # Valor de la etiqueta "oneway"
    lanes = way.tags.get("lanes")  # Valor de la etiqueta "lanes"
    name = way.tags.get("name")  # Valor de la etiqueta "name"
    highway = way.tags.get("highway")  # Valor de la etiqueta "highway"
    maxspeed = way.tags.get("maxspeed")  # Valor de la etiqueta "maxspeed"
    reversed = way.tags.get("reversed")  # Valor de la etiqueta "reversed"
    length = way.tags.get("length")  # Valor de la etiqueta "length"
    geometry = way.geometry  # Geometría del elemento
    bridge = way.tags.get("bridge")  # Valor de la etiqueta "bridge"
    ref = way.tags.get("ref")  # Valor de la etiqueta "ref"
    junction = way.tags.get("junction")  # Valor de la etiqueta "junction"
    tunnel = way.tags.get("tunnel")  # Valor de la etiqueta "tunnel"
    access = way.tags.get("access")  # Valor de la etiqueta "access"
    
    # Realizar las operaciones necesarias con los campos obtenidos
    # ...

    # Imprimir los campos obtenidos
    print(u, v, key, osmid, oneway, lanes, name, highway, maxspeed, reversed, length, geometry, bridge, ref, junction, tunnel, access)
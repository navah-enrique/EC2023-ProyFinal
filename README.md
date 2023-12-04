# EC2023-ProyFinal
Repositorio del proyecto final de la clase de Estadistica Computacional 2023

# Proyecto Final:
Establecimientos populares de la CDMX y similitudes por colonias

# Integrantes del equipo:
| Nombre                              | CU     | Mail                  | Usuario Gh    |
| ----------------------------------- | ------ | --------------------- | ------------- |
| Héctor Vilchis Peralta              | 214557 | hvilchis@itam.mx      | hectorvil     |
| Enrique Nava Hernández              | 108807 | enavaher@itam.mx      | navah-enrique |
| Cecilia Avilés Robles               | 197817 | cavilesr@itam.mx      | cecyar        |
| Leonardo Ceja Pérez                 | 197818 | lcejaper@itam.mx      | lecepe00      |


# Explicación del problema de negocio:
Para conocer la competitividad que tenga algún establecimiento utilizamos la API de foursquare para tener información de los negocios de la Ciudad de México. Estos datos utilizados fueron tipo de negocio, coordenadas geográficas, nombre y colonia a la que pertenece.
Con base en esta data, se creó una API que segmentara a todas las colonias de la ciudad por medio de un algoritmo k-means. Los datos resultantes de la segmentación se grafican en Shiny, con lo cual se puede conocer qué colonias son más parecidas entre sí, lo que da una ventaja competitiva, ya que si se consulta algún tipo de restaurante podremos observar si existe alguna colonia aledaña con un giro comercial parecido y además cuál es la actividad comercial predominante de la colonia a la que pertenece el establecimiento.

# Base de datos:
La base de datos inicial se encuentra en un csv ya existente dentro de la carpeta app/data dentro de este repositorio.

# Ejecución:
1. Clonar el repositorio en el equipo.
2. Abrir una terminal, ir a la carpeta "app" del repositorio clonado.
3. Construir la imagen de docker: docker-compose build y docker-compose up.

# ¿Qué hace el producto?:
1. Se crean los contenedores de la api, postgress, y shiny (y dash que fue un primer intento para nuestro mapa).
2. API: se crea y configura la conexion a postgres
3. API: lee la data venues_cdmx_completa (esta desde el inicio en la carpeta de data)
4. API: procesa el csv: one-hot encoding, crea los top 10 venues, y hace clustering de k-means sobre colonias similares.
5. API: guarda nuevo csv
6. Shiny app: lee los csvs
7. Shiny app: crea mapas para poder ver los venues por tipo de venue (establecimiento) y por tipo de cluster.

from flask import Flask, request
from flask_cors import CORS
import pusher
import mysql.connector
from mysql.connector import Error


app = Flask(__name__)
CORS(app)

# Configuración de la base de datos MySQL
db_config = {
    'host': 'mysql-haruand.alwaysdata.net',         # Dirección de tu servidor MySQL
    'user': 'haruand',              # Usuario de MySQL
    'password': 'Haru_and8', # Contraseña de MySQL
    'database': 'haruand_pusher_db'      # Nombre de tu base de datos
}
# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None


@app.route("/", methods=["POST"])
def hola_mundo():
    data = request.get_json()

    guardar_mensaje(data["message"],"anonimo")
    pusher_client = pusher.Pusher(
        app_id = "2062326",
        key = "8991fbde10313380964c",
        secret = "57b5781a85767841a9c8",
        cluster = "ap3",
        ssl= True
    )

    pusher_client.trigger('my-channel','my-event', {'message':data["message"]})
    return ".."

def guardar_mensaje(mensaje, usuario):

    if not mensaje or not usuario:
        return None

    # Obtener la conexión a la base de datos
    connection = get_db_connection()
    if connection is None:
        return None
    
    try:
        # Guardar el mensaje en la base de datos
        cursor = connection.cursor()
        query = 'INSERT INTO mensajes (mensaje, usuario) VALUES (%s, %s)'
        cursor.execute(query, (mensaje, usuario))
        connection.commit()

     
        cursor.close()
        return True
    except Error as e:
        print(f"Error al guardar el mensaje: {e}")
        return None
    finally:
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)

    

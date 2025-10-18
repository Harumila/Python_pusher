from flask import Flask, request
from flask_cors import CORS
import pusher

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["POST"])
def hola_mundo():
    data = request.get_json()


    pusher_client = pusher.Pusher(
        app_id = "2062326",
        key = "8991fbde10313380964c",
        secret = "57b5781a85767841a9c8",
        cluster = "ap3",
        ssl= True
    )

    pusher_client.trigger('my-channel','my-event', {'message':data["message"]})
    return ".."

if __name__ == "__main__":
    app.run(debug=True)

    

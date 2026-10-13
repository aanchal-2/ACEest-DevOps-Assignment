
import os

from flask import Flask, jsonify, render_template, request

from sqlite3 import IntegrityError
 
import storage
 
 
FITNESS_PROGRAMS = {

    "Fat Loss": {

        "workouts": [

            "Monday: Cardio - 30 minutes",

            "Tuesday: Full-body strength training",

            "Wednesday: Walking and mobility",

            "Thursday: Cardio intervals",

            "Friday: Strength and core",

            "Saturday: Light activity",

            "Sunday: Rest"

        ],

        "nutrition": [

            "Eat balanced meals with vegetables and protein",

            "Include whole grains and fiber-rich foods",

            "Drink water regularly",

            "Choose portions appropriate to your needs"

        ]

    },

    "Muscle Gain": {

        "workouts": [

            "Monday: Chest and triceps",

            "Tuesday: Back and biceps",

            "Wednesday: Recovery and mobility",

            "Thursday: Legs",

            "Friday: Shoulders and core",

            "Saturday: Full-body training",

            "Sunday: Rest"

        ],

        "nutrition": [

            "Include protein-rich foods in balanced meals",

            "Eat sufficient carbohydrates for training",

            "Include healthy fat sources",

            "Stay hydrated and recover adequately"

        ]

    },

    "Beginner": {

        "workouts": [

            "Monday: Full-body introductory workout",

            "Tuesday: Walking",

            "Wednesday: Rest or gentle mobility",

            "Thursday: Basic strength exercises",

            "Friday: Light cardio",

            "Saturday: Stretching and mobility",

            "Sunday: Rest"

        ],

        "nutrition": [

            "Eat a varied and balanced diet",

            "Include vegetables and fruit",

            "Include protein sources in meals",

            "Drink water throughout the day"

        ]

    }

}
 
 
def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(

        SECRET_KEY=os.environ.get("SECRET_KEY", "local-development-only"),

        DATABASE=os.environ.get(

            "ACEEST_DB_PATH", os.path.join(app.instance_path, "aceest.db")

        )

    )

    if test_config:

        app.config.update(test_config)
 
    os.makedirs(os.path.dirname(app.config["DATABASE"]), exist_ok=True)

    storage.init_db(app.config["DATABASE"])
 
    @app.get("/")

    def home():

        return render_template("index.html", programs=list(FITNESS_PROGRAMS))
 
    @app.get("/health")

    def health():

        return jsonify(application="ACEest Fitness & Gym", status="running"), 200
 
    @app.get("/program/<path:program_name>")

    def get_program(program_name):

        program = FITNESS_PROGRAMS.get(program_name)

        if program is None:

            return jsonify(error="Fitness program not found"), 404

        return jsonify(

            name=program_name,

            workouts=program["workouts"],

            nutrition=program["nutrition"]

        ), 200
 
    @app.get("/clients")

    def get_clients():

        return jsonify(storage.list_clients(app.config["DATABASE"])), 200
 
    @app.post("/clients")

    def create_client():

        data = request.get_json(silent=True)

        if not isinstance(data, dict):

            return jsonify(error="A JSON object is required"), 400

        name = data.get("name")

        if not isinstance(name, str) or not name.strip():

            return jsonify(error="Client name is required"), 400

        try:

            client_id = storage.add_client(name.strip(), app.config["DATABASE"])

        except IntegrityError:

            return jsonify(error="Client already exists"), 409

        return jsonify(

            message="Client created successfully",

            client_id=client_id

        ), 201
 
    @app.patch("/clients/<int:client_id>/membership")

    def change_membership(client_id):

        data = request.get_json(silent=True)

        if not isinstance(data, dict):

            return jsonify(error="A JSON object is required"), 400

        status = data.get("status")

        if status not in ("Active", "Inactive"):

            return jsonify(error="Status must be Active or Inactive"), 400

        updated = storage.update_membership(

            client_id, status, app.config["DATABASE"]

        )

        if not updated:

            return jsonify(error="Client not found"), 404

        return jsonify(message="Membership updated", status=status), 200
 
    @app.get("/workouts")

    def get_workouts():

        return jsonify(storage.list_workouts(app.config["DATABASE"])), 200
 
    @app.post("/workouts")

    def create_workout():

        data = request.get_json(silent=True)

        if not isinstance(data, dict):

            return jsonify(error="A JSON object is required"), 400

        client_id = data.get("client_id")

        workout_type = data.get("workout_type")

        duration = data.get("duration_min")

        if (

            type(client_id) is not int

            or not isinstance(workout_type, str)

            or not workout_type.strip()

            or type(duration) is not int

            or duration <= 0

        ):

            return jsonify(error="Invalid workout data"), 400

        workout_id = storage.add_workout(

            client_id, workout_type, duration, app.config["DATABASE"]

        )

        if workout_id is None:

            return jsonify(error="Client not found"), 404

        return jsonify(

            message="Workout added successfully",

            workout_id=workout_id

        ), 201
 
    return app
 
 
app = create_app()
 
if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=False)


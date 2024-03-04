from emp import db, Employee
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from werkzeug.exceptions import BadRequestKeyError

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:pass123@127.0.0.1:3306/employee"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


employee = Employee()


@app.route("/")
def hello_world():
    return jsonify({"200": "Success"})


@app.route("/employee", methods=["GET"])
@cross_origin(allow_headers=["Content-Type"])
def get_all():
    return employee.get_all()


@app.route("/employee/detail/<id>", methods=["GET"])
@cross_origin(allow_headers=["Content-Type"])
def get_by_id(id):
    return employee.get_by_id(id)


@app.route("/employee/add", methods=["POST"])
@cross_origin(allow_headers=["Content-Type"])
def create_employee():
    try:
        if request.data:
            data = request.get_json()
            # print(data)
            # print(str(data['firstname']).isalpha())
            return employee.create(data)
        raise BadRequestKeyError
    except BadRequestKeyError:
        return jsonify({"Error": "Data does not exist"})


@app.route("/employee/update/<id>", methods=["PUT"])
@cross_origin(allow_headers=["Content-Type"])
def update_image(id):
    try:
        if request.data:
            data = request.get_json()
            # print(str(data['firstname']).isalpha())
            return employee.update(id, data)
        raise BadRequestKeyError
    except BadRequestKeyError:
        return jsonify({"Error": "No data present"})


@app.route("/employee/delete/<id>", methods=["DELETE"])
@cross_origin()
def delete_emp(id):
    return employee.remove(id)


if __name__ == "__main__":
    app.run()

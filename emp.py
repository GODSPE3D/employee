import base64
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import NoResultFound
from sqlalchemy.dialects.mysql import LONGBLOB

db = SQLAlchemy()


class Employee(db.Model):
    emp_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    age = db.Column(db.Integer)
    image = db.Column(LONGBLOB)

    @property
    def serialize(self):
        image = base64.b64encode(self.image).decode('utf-8')

        return {
            "emp_id": self.emp_id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
            "age": self.age,
            "image": image,
        }

    def get_all(self):
        try:
            empAll = Employee.query.all()
            if empAll != []:
                return jsonify(
                    [
                        {
                            "emp_id": emp.emp_id,
                            "firstname": emp.firstname,
                            "lastname": emp.lastname,
                            "email": emp.email,
                            "age": emp.age,
                        }
                        for emp in empAll
                    ]
                )
            raise NoResultFound
        except NoResultFound:
            return jsonify({"Error": "No data exists"})

    def get_by_id(self, id):
        print(id)
        try:
            emp = db.session.query(Employee).filter_by(emp_id=id).first()

            if emp == None:
                raise NoResultFound

            if emp.image == None:
                emp.image = "null"
            else:
                # image = base64.b64encode(emp.image).decode('utf-8')
                image = bytes(emp.image).decode('utf-8')
                emp.image = image

            return jsonify(
                {
                    "emp_id": emp.emp_id,
                    "firstname": emp.firstname,
                    "lastname": emp.lastname,
                    "email": emp.email,
                    "age": emp.age,
                    "image": emp.image
                }
            )
        except NoResultFound:
            return jsonify({"Error": "No such ID exists"})

    def create(self, data):
        try:
            new_emp = Employee()

            # "firstname" not in data and str(data['firstname']).isalpha() == True
                # and "lastname" not in data and str(data['lastname']).isalpha() == True
                # and "email" not in data and str(data['email']).isalnum() == True
                # and "age" not in data and str(data['age']).isnumeric() == True
                # and "image" not in data

            # if (
            #     "firstname" not in data or str(data['firstname']).isalpha() == False or
            #     "lastname" not in data or str(data['lastname']).isalpha() == False or
            #     "email" not in data and str(data['email']).isalnum() == False or
            #     "age" not in data and str(data['age']).isnumeric() == False or
            #     "image" not in data
                
            #     # or str(data['firstname']).isalpha() == False
            #     # and "lastname"  in data and str(data['lastname']).isalpha() == False
            # ):
            #     raise ValueError

            if "firstname" in data:
                new_emp.firstname = data["firstname"]
            if "lastname" in data:
                new_emp.lastname = data["lastname"]
            if "email" in data:
                new_emp.email = data["email"]
            if "age" in data:
                new_emp.age = data["age"]
            if "image" in data:
                new_emp.image = bytes(data['image'], encoding='utf-8')

            db.session.add(new_emp)
            db.session.commit()
            
            return new_emp.get_by_id(new_emp.emp_id)
        except ValueError:
            return jsonify({"Error": "Please enter valid value"})

    def update(self, id, data):
        try:
            emp = db.session.get(Employee, id)
            print(data)

            if emp == None:
                raise NoResultFound
            if "firstname" in data and str(data['firstname']).isalpha() == True:
                emp.firstname = data["firstname"]
            if "lastname" in data and str(data['lastname']).isalpha() == True:
                emp.lastname = data["lastname"]
            if "age" in data and str(data['age']).isnumeric() == True:
                emp.age = data["age"]
            if "image" in data:
                emp.image = bytes(data['image'], encoding='utf-8')
            else:
                raise ValueError

            db.session.commit()

            return emp.get_by_id(emp.emp_id)
        except NoResultFound:
            return jsonify({"Error": "No such ID exists"})
        except ValueError:
            return jsonify({"Error": "Please enter valid value"})

    def remove(self, id):
        try:
            emp = Employee.query.filter_by(emp_id=id).first()

            if emp == None:
                raise NoResultFound

            db.session.delete(emp)
            db.session.commit()

            return jsonify({"Success": "Data deleted successfully!"})

        except NoResultFound:
            return jsonify({"Error": "No such ID exists!"})
        

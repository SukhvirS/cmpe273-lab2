from flask import Flask, escape, request

app = Flask(__name__)

studentID = 1
classID = 1

DB = {
    "students": {},
    "classes": {},
}

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'

@app.route('/students/', methods=['POST'])
def create_student():
    global studentID
    req = request.json
    currentID = studentID
    DB['students'][currentID] = {
        'id': currentID,
        'name': req['name'],
    }
    studentID += 1
    return DB['students'][currentID], 201

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    id = int(id)
    if id >= studentID or id < 1:
        return f"No student with id {id}"
    return DB['students'][id], 201

@app.route('/classes/', methods=['POST'])
def create_class():
    global classID
    req = request.json
    currentID = classID
    DB['classes'][currentID] = {
        'id': currentID,
        'name': req['name'],
        'students': [],
    }
    classID += 1
    return DB['classes'][currentID], 201

@app.route('/classes/<id>', methods=['GET'])
def get_class(id):
    id = int(id)
    if id >= classID or id < 1:
        return f"No class with id {id}"
    return DB['classes'][id], 201

@app.route('/classes/<id>', methods=['PATCH'])
def add_student_to_class(id):
    id = int(id)
    req = request.json
    DB['classes'][id]['students'].append(
        DB['students'][req['student_id']]
    )
    return DB['classes'][id]
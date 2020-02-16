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
def createStudent():
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
def getStudent(id):
    id = int(id)
    if id >= studentID or id < 1:
        return f"No student with id {id}"
    return DB['students'][id]

@app.route('/classes/', methods=['POST'])
def createClass():
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
def getClass(id):
    id = int(id)
    if id >= classID or id < 1:
        return f"No class with id {id}"
    return DB['classes'][id]

@app.route('/classes/<id>', methods=['PATCH'])
def addStudentToClass(id):
    cID = int(id)
    req = request.json
    sID = req['student_id']

    if cID >= classID:
        return f"No class with id {cID}"

    if sID >= studentID:
        return f"No student with id {sID}"
    
    if not studentAlreadyInClass(cID, sID):        
        DB['classes'][cID]['students'].append(
            DB['students'][sID]
        )
        print(f"Student with id {sID} is already in this class.")
    return DB['classes'][cID], 201

def studentAlreadyInClass(cID, sID):
    students = DB['classes'][cID]['students']
    for student in students:
        if student['id'] == sID:
            return True
    return False
    
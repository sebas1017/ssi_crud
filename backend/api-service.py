from flask import Flask, jsonify, request
from flask_bootstrap import Bootstrap
from flask import Flask, render_template
from dotenv import dotenv_values
from models.models_db import db, Patient
from datetime import datetime

app = Flask(__name__)


config_db = dotenv_values(".env")
# Configurar la conexión a la base de datos desde el archivo .env
app.config['SQLALCHEMY_DATABASE_URI'] = config_db.get('DATABASE_URL')
db.init_app(app)

with app.app_context():
    db.create_all()

bootstrap = Bootstrap(app)



def get_all_patients_data():
    patients = Patient.query.all()
    patient_list = []

    for patient in patients:
        patient_data = {
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),
            'gender': patient.gender,
            'address': patient.address,
            'phone': patient.phone,
            'email': patient.email
        }
        patient_list.append(patient_data)
    return patient_list


@app.route('/')
def index():
    patient_list =get_all_patients_data()
    return render_template('index.html', patients = patient_list)


@app.route('/patients', methods=['GET'])
def get_all_patients():
    patient_list = get_all_patients_data()
    return jsonify({'patients': patient_list})

# Ruta para agregar un nuevo paciente
@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.form
    valid_data = {}
    for k , v in data.items():
        if v is not None:
            valid_data[k] = v

    if "date_of_birth" in valid_data:
        valid_data["date_of_birth"] = datetime.strptime(data['date_of_birth'], '%Y-%m-%d')

    new_patient = Patient(
        **valid_data
    )
    db.session.add(new_patient)
    db.session.commit()
    
    response_data = {'message': 'Paciente creado correctamente', 'id': new_patient.id}
    return jsonify(response_data), 201

# Ruta para ver los detalles de un paciente por ID
@app.route('/patient_details/<int:id>', methods=['GET'])
def get_patient(id):
    patient = db.session.get(Patient, id)
    if patient is None:
        return jsonify({'error': 'El ID a consultar no existe'}), 404
    
    patient_data = {
        'id': patient.id,
        'first_name': patient.first_name,
        'last_name': patient.last_name,
        'date_of_birth': patient.date_of_birth.strftime('%Y-%m-%d'),
        'gender': patient.gender,
        'address': patient.address,
        'phone': patient.phone,
        'email': patient.email
    }
    return jsonify(patient_data)

@app.route('/patients/<int:id>', methods=['PUT','POST'])
def update_patient(id):
    print(request.get_json())
    data = {}
    if request.is_json:
        data = request.get_json()
    patient = db.session.get(Patient, id)
    if patient is None:
        return jsonify({'error': 'El ID a actualizar no existe'}), 404

    if data is None:
        data = request.json
    updated_fields = {}  # Almacenar los campos actualizados aquí


    print(data)
    # Definir los campos permitidos para actualización
    allowed_fields = ['first_name', 'last_name', 'date_of_birth', 'gender', 'address', 'phone', 'email']

    # Iterar sobre las claves en data y actualizar los campos correspondientes
    for field in allowed_fields:
        if field in data:
            if field == 'date_of_birth':
                setattr(patient, field, datetime.strptime(data[field], '%Y-%m-%d'))
            else:
                setattr(patient, field, data[field])
            updated_fields[field] = data[field]

    db.session.commit()
    return jsonify({'message': 'Paciente actualizado correctamente', 'updated_fields': updated_fields})


# Ruta para eliminar un paciente por ID
@app.route('/patients/<int:id>', methods=['DELETE', 'GET'])
def delete_patient(id):
    print("SIII", id)
    patient = db.session.get(Patient, id)
    
    if patient is None:
        return jsonify({'error': 'El ID a eliminar no existe'}), 404
    db.session.delete(patient)
    db.session.commit()
    return jsonify({'message': 'Paciente eliminado correctamente'})

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5001, debug=True)
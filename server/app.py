import os
from typing import Dict, List, Any, Optional
from flask import Flask, jsonify, request, Response
from models import init_db, db, Dog, Breed
from models.dog import AdoptionStatus

# Get the server directory path
base_dir: str = os.path.abspath(os.path.dirname(__file__))

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(base_dir, "dogshelter.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
init_db(app)

@app.route('/api/dogs', methods=['GET'])
def get_dogs() -> Response:
    QUERY = db.session.query(
        Dog.id, 
        Dog.name, 
        Breed.name.label('breed'),
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id)
    
    # Filter by breed if breed_id query parameter is provided
    BREED_ID = request.args.get('breed_id', type=int)
    if BREED_ID is not None:
        QUERY = QUERY.filter(Dog.breed_id == BREED_ID)
    
    # Filter by availability if available query parameter is provided
    AVAILABLE = request.args.get('available', type=str)
    if AVAILABLE and AVAILABLE.lower() == 'true':
        QUERY = QUERY.filter(Dog.status == AdoptionStatus.AVAILABLE)
    
    DOGS_QUERY = QUERY.all()
    
    # Convert the result to a list of dictionaries
    DOGS_LIST: List[Dict[str, Any]] = [
        {
            'id': DOG.id,
            'name': DOG.name,
            'breed': DOG.breed,
            'status': DOG.status.name if DOG.status else 'UNKNOWN'
        }
        for DOG in DOGS_QUERY
    ]
    
    return jsonify(DOGS_LIST)

@app.route('/api/dogs/<int:id>', methods=['GET'])
def get_dog(id: int) -> tuple[Response, int] | Response:
    # Query the specific dog by ID and join with breed to get breed name
    dog_query = db.session.query(
        Dog.id,
        Dog.name,
        Breed.name.label('breed'),
        Dog.age,
        Dog.description,
        Dog.gender,
        Dog.status
    ).join(Breed, Dog.breed_id == Breed.id).filter(Dog.id == id).first()
    
    # Return 404 if dog not found
    if not dog_query:
        return jsonify({"error": "Dog not found"}), 404
    
    # Convert the result to a dictionary
    dog: Dict[str, Any] = {
        'id': dog_query.id,
        'name': dog_query.name,
        'breed': dog_query.breed,
        'age': dog_query.age,
        'description': dog_query.description,
        'gender': dog_query.gender,
        'status': dog_query.status.name
    }
    
    return jsonify(dog)

@app.route('/api/breeds', methods=['GET'])
def get_breeds() -> Response:
    """
    Retrieve all dog breeds from the database.
    Queries the Breed table and returns all breed records as JSON.
    Each breed object contains its unique identifier and name.
    Returns:
        Response: A Flask response object containing a JSON array of breeds.
                 Each breed is a dictionary with 'id' and 'name' keys.
    """
    breeds_query = Breed.query.all()
    
    # Convert the result to a list of dictionaries
    breeds_list: List[Dict[str, Any]] = [
        {
            'id': breed.id,
            'name': breed.name
        }
        for breed in breeds_query
    ]
    
    return jsonify(breeds_list)

if __name__ == '__main__':
    app.run(debug=True, port=5100) # Port 5100 to avoid macOS conflicts
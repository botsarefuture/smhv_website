from flask import Blueprint, jsonify, request
from bson import ObjectId

# Create an API blueprint
api_bp = Blueprint('api', __name__)

# Admin API for creating a signup
@api_bp.route('/signups', methods=['POST'])
def admin_api_create_signup():
    signup_data = request.get_json()
    
    # Perform validation on signup_data as needed
    
    signup_id = signups_collection.insert_one(signup_data).inserted_id
    
    return jsonify({'signup_id': str(signup_id)}), 201

# Admin API for updating a signup
@api_bp.route('/signups/<signup_id>', methods=['PUT'])
def admin_api_update_signup(signup_id):
    signup_data = request.get_json()
    
    # Perform validation on signup_data as needed
    
    result = signups_collection.update_one(
        {'_id': ObjectId(signup_id)},
        {'$set': signup_data}
    )
    
    if result.modified_count == 1:
        return jsonify({'message': 'Signup updated successfully'})
    else:
        return jsonify({'error': 'Signup not found'}), 404

# Admin API for deleting a signup
@api_bp.route('/signups/<signup_id>', methods=['DELETE'])
def admin_api_delete_signup(signup_id):
    result = signups_collection.delete_one({'_id': ObjectId(signup_id)})
    
    if result.deleted_count == 1:
        return jsonify({'message': 'Signup deleted successfully'})
    else:
        return jsonify({'error': 'Signup not found'}), 404

# Admin API for getting all signups
@api_bp.route('/signups', methods=['GET'])
def admin_api_get_signups():
    signups_data = signups_collection.find()
    signup_list = []

    for signup in signups_data:
        signup_list.append({
            'signup_id': str(signup['_id']),
            'name': signup['name'],
            'email': signup['email'],
            # Add other signup fields as needed
        })

    return jsonify(signup_list)

# Admin API for creating an event
@api_bp.route('/events', methods=['POST'])
def admin_api_create_event():
    event_data = request.get_json()
    
    # Perform validation on event_data as needed
    
    event_id = events_collection.insert_one(event_data).inserted_id
    
    return jsonify({'event_id': str(event_id)}), 201

# Admin API for updating an event
@api_bp.route('/events/<event_id>', methods=['PUT'])
def admin_api_update_event(event_id):
    event_data = request.get_json()
    
    # Perform validation on event_data as needed
    
    result = events_collection.update_one(
        {'_id': ObjectId(event_id)},
        {'$set': event_data}
    )
    
    if result.modified_count == 1:
        return jsonify({'message': 'Event updated successfully'})
    else:
        return jsonify({'error': 'Event not found'}), 404

# Admin API for deleting an event
@api_bp.route('/events/<event_id>', methods=['DELETE'])
def admin_api_delete_event(event_id):
    result = events_collection.delete_one({'_id': ObjectId(event_id)})
    
    if result.deleted_count == 1:
        return jsonify({'message': 'Event deleted successfully'})
    else:
        return jsonify({'error': 'Event not found'}), 404

# Admin API for getting all events
@api_bp.route('/events', methods=['GET'])
def admin_api_get_events():
    events_data = events_collection.find()
    event_list = []

    for event in events_data:
        event_list.append({
            'event_id': str(event['_id']),
            'name': event['name'],
            'date': event['date'],
            # Add other event fields as needed
        })

    return jsonify(event_list)

# Admin API for creating a join
@api_bp.route('/joins', methods=['POST'])
def admin_api_create_join():
    join_data = request.get_json()
    
    # Perform validation on join_data as needed
    
    join_id = joins_collection.insert_one(join_data).inserted_id
    
    return jsonify({'join_id': str(join_id)}), 201

# Admin API for updating a join
@api_bp.route('/joins/<join_id>', methods=['PUT'])
def admin_api_update_join(join_id):
    join_data = request.get_json()
    
    # Perform validation on join_data as needed
    
    result = joins_collection.update_one(
        {'_id': ObjectId(join_id)},
        {'$set': join_data}
    )
    
    if result.modified_count == 1:
        return jsonify({'message': 'Join updated successfully'})
    else:
        return jsonify({'error': 'Join not found'}), 404

# Admin API for deleting a join
@api_bp.route('/joins/<join_id>', methods=['DELETE'])
def admin_api_delete_join(join_id):
    result = joins_collection.delete_one({'_id': ObjectId(join_id)})
    
    if result.deleted_count == 1:
        return jsonify({'message': 'Join deleted successfully'})
    else:
        return jsonify({'error': 'Join not found'}), 404

# Admin API for getting all joins
@api_bp.route('/joins', methods=['GET'])
def admin_api_get_joins():
    joins_data = joins_collection.find()
    join_list = []

    for join in joins_data:
        join_list.append({
            'join_id': str(join['_id']),
            'name': join['name'],
            'email': join['email'],
            # Add other join fields as needed
        })

    return jsonify(join_list)

# Admin API for creating a contaction
@api_bp.route('/contactions', methods=['POST'])
def admin_api_create_contaction():
    contaction_data = request.get_json()
    
    # Perform validation on contaction_data as needed
    
    contaction_id = contactions_collection.insert_one(contaction_data).inserted_id
    
    return jsonify({'contaction_id': str(contaction_id)}), 201

# Admin API for updating a contaction
@api_bp.route('/contactions/<contaction_id>', methods=['PUT'])
def admin_api_update_contaction(contaction_id):
    contaction_data = request.get_json()
    
    # Perform validation on contaction_data as needed
    
    result = contactions_collection.update_one(
        {'_id': ObjectId(contaction_id)},
        {'$set': contaction_data}
    )
    
    if result.modified_count == 1:
        return jsonify({'message': 'Contaction updated successfully'})
    else:
        return jsonify({'error': 'Contaction not found'}), 404

# Admin API for deleting a contaction
@api_bp.route('/contactions/<contaction_id>', methods=['DELETE'])
def admin_api_delete_contaction(contaction_id):
    result = contactions_collection.delete_one({'_id': ObjectId(contaction_id)})
    
    if result.deleted_count == 1:
        return jsonify({'message': 'Contaction deleted successfully'})
    else:
        return jsonify({'error': 'Contaction not found'}), 404

# Admin API for getting all contactions
@api_bp.route('/contactions', methods=['GET'])
def admin_api_get_contactions():
    contactions_data = contactions_collection.find()
    contaction_list = []

    for contaction in contactions_data:
        contaction_list.append({
            'contaction_id': str(contaction['_id']),
            'name': contaction['name'],
            'email': contaction['email'],
            # Add other contaction fields as needed
        })

    return jsonify(contaction_list)

# ... (remaining code)

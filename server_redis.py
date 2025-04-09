from flask import Flask, request, jsonify, Response
import redis
import json

app_dk = Flask(__name__)
app_dk.config.update(
    JSON_AS_ASCII=False,
    JSONIFY_PRETTYPRINT_REGULAR=True  # Красивое форматирование
)
r = redis.Redis(host='localhost', port=6379, db=0)
rooms_n_users = {} 

def manage_room(data):
    if data['room'] not in rooms_n_users:
        rooms_n_users[data['room']] = []
        print(f"New room {data['room']} added")

    if data['user'] not in rooms_n_users[data['room']]:
        rooms_n_users[data['room']].append(data['user'])
        print(f"New user {data['user']} in room {data['room']} added")

def push_to_reddis(data):
    room = data['room']
    user = data['user']
    list_name = f'like_{room}_{user}'
    r.lpush(list_name, data['film'])
    print(f"Film {data['film']} added to {list_name}")

def look_for_matches(data):
    for user in rooms_n_users[data['room']]:
        liked_films = []
        if user is not data['user']:
            room = data['room']
            list_name = f'like_{room}_{user}'
            liked_films = r.lrange(list_name, 0, -1)

            liked_films = [film.decode('utf-8') for film in liked_films]

            if data['film'] in liked_films:
                print("We found a match!")
                return True
    return False


@app_dk.route('/push', methods=['POST'])
def proceed_data():
    try:
        data = request.json  
        if not data:
            return jsonify({"error": "No data provided"}), 400

        manage_room(data)
        
        is_match = False
        if data['status'] == 'like':
            push_to_reddis(data)
            is_match = look_for_matches(data)
        if is_match:
            output = {"status": "Match found", "matched film": data['film']}
            json_str = json.dumps(output, ensure_ascii=False, indent=2)
            return Response(json_str, mimetype='application/json')
            # return jsonify({"status": "Match found", "matched film": data['film']}), 200
        
        return jsonify({"status": "Data proceeded, matches not found"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app_dk.run(host='0.0.0.0', port=5000) 
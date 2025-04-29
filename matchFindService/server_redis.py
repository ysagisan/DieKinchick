from flask import Flask, request, jsonify, Response
import redis
import json

app_dk = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)
rooms_n_users = {}


def add_new_room(data):
    rooms_n_users[data['room']] = data['users']
    print(f"New room {data['room']} with users {data['users']} added")


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
            if data['film'] not in liked_films:
                return False
    print("We found a match!")
    return True


def delete_data(data):
    room = data['room']
    for user in rooms_n_users[data['room']]:
        list_name = f'like_{room}_{user}'
        res = r.delete(list_name)
        print(f'List {list_name} deleted')
    del rooms_n_users[data['room']]
    print(f'Room {room} deleted')


@app_dk.route('/push', methods=['POST'])
def proceed_data():
    try:
        data = request.json

        if not data:
            return jsonify({"error": "No data provided"}), 400

        if data['status'] == 'new room':
            add_new_room(data)
            return jsonify({"status": "New room added", "room": data['room']}), 200

        elif data['status'] == 'film message':

            if data['film_status'] == 'like':
                push_to_reddis(data)
                is_match = True
                is_match = look_for_matches(data)

                if is_match:
                    output = {"room": data['room'], "status": "Match found", "matched film": data['film']}
                    json_str = json.dumps(output, ensure_ascii=False, indent=2)
                    return Response(json_str, mimetype='application/json')

                output = {"room": data['room'], "user": data['user'],
                          "status": "Film added to redis, matches not found",
                          "Added film": data['film']}
                json_str = json.dumps(output, ensure_ascii=False, indent=2)
                return Response(json_str, mimetype='application/json')

            output = {"room": data['room'], "user": data['user'], "status": "Film skipped",
                      "Disliked film": data['film']}
            json_str = json.dumps(output, ensure_ascii=False, indent=2)
            return Response(json_str, mimetype='application/json')

        elif data['status'] == 'end of session':
            delete_data(data)
            return jsonify({"status": "Room deleted", "room": data['room']}), 200

        else:
            return jsonify({"error": "Invalid format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app_dk.run(host='0.0.0.0', port=4450)
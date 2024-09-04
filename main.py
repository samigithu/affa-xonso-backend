from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL

app = Flask(__name__)
CORS(app)  
# MySQL Configuration
# Configure database connection
app.config['MYSQL_HOST'] = 'sql12.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql12729214'
app.config['MYSQL_PASSWORD'] = '9ql3Lh6nyT'
app.config['MYSQL_DB'] = 'sql12729214'
app.config['MYSQL_PORT'] = 3306

mysql = MySQL(app)

@app.route('/api')
def hello_world():
    return "hello world"
@app.route('/api/data', methods=['GET'])
def get_data():
    data = {'message': 'Hello from Python backend!'}
    return jsonify(data)


@app.route("/albums", methods=["GET"])
def get_all_albums():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM album_table")
    albums = cur.fetchall()
    output = []
    for album in albums:
        output.append({"album_id": album[0], "album_title": album[1], "album_image": album[2], "album_description": album[3]})
    cur.close()
    return jsonify({"albums": output})

@app.route("/albums/<int:album_id>", methods=["GET"])
def get_album(album_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM album_table WHERE album_id = %s", (album_id,))
    album = cur.fetchone()
    if album is None:
        return jsonify({"message": "Album not found"}), 404
    output = {"album_id": album[0], "album_title": album[1], "album_image": album[2], "album_description": album[3]}
    cur.close()
    return jsonify({"album": output})

@app.route("/albums", methods=["POST"])
def create_album():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO album_table (album_title, album_image, album_description) VALUES (%s, %s, %s)", (data["album_title"], data["album_image"], data.get("album_description")))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Album created successfully"})

@app.route("/albums/<int:album_id>", methods=["PUT"])
def update_album(album_id):
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM album_table WHERE album_id = %s", (album_id,))
    album = cur.fetchone()
    if album is None:
        return jsonify({"message": "Album not found"}), 404
    cur.execute("UPDATE album_table SET album_title = %s, album_image = %s, album_description = %s WHERE album_id = %s", (data.get("album_title", album[1]), data.get("album_image", album[2]), data.get("album_description", album[3]), album_id))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Album updated successfully"})

@app.route("/albums/<int:album_id>", methods=["DELETE"])
def delete_album(album_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM album_table WHERE album_id = %s", (album_id,))
    album = cur.fetchone()
    if album is None:
        return jsonify({"message": "Album not found"}), 404
    cur.execute("DELETE FROM album_table WHERE album_id = %s", (album_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({"message": "Album deleted successfully"})
    
    
  
# 1. Get all singers
@app.route('/singers', methods=['GET'])
def get_all_singers():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM singers_table")
    singers = cur.fetchall()
    return jsonify([{"id": singer[0], "name": singer[1], "profile": singer[2]} for singer in singers])

# 2. Get a singer by ID
@app.route('/singers/<int:singer_id>', methods=['GET'])
def get_singer_by_id(singer_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM singers_table WHERE singer_id = %s", (singer_id,))
    singer = cur.fetchone()
    if singer:
        return jsonify({"id": singer[0], "name": singer[1], "profile": singer[2]})
    else:
        return jsonify({"error": "Singer not found"}), 404

# 3. Create a new singer
@app.route('/singers', methods=['POST'])
def create_singer():
    cur = mysql.connection.cursor()
    data = request.get_json()
    name = data["name"]
    profile = data["profile"]
    cur.execute("INSERT INTO singers_table (singer_name, singer_profile) VALUES (%s, %s)", (name, profile))
    db.commit()
    return jsonify({"message": "Singer created successfully"}), 201

# 4. Update a singer
@app.route('/singers/<int:singer_id>', methods=['PUT'])
def update_singer(singer_id):
    cur = mysql.connection.cursor()
    data = request.get_json()
    name = data["name"]
    profile = data["profile"]
    cur.execute("UPDATE singers_table SET singer_name = %s, singer_profile = %s WHERE singer_id = %s", (name, profile, singer_id))
    db.commit()
    return jsonify({"message": "Singer updated successfully"})

# 5. Delete a singer
@app.route('/singers/<int:singer_id>', methods=['DELETE'])
def delete_singer(singer_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM singers_table WHERE singer_id = %s", (singer_id,))
    db.commit()
    return jsonify({"message": "Singer deleted successfully"}), 204
    
@app.route("/songs", methods=["GET"])
def get_songs():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM songs_table")
    songs = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    return jsonify([dict(zip(columns, song)) for song in songs])

@app.route("/songs", methods=["POST"])
def create_song():
    cur = mysql.connection.cursor()
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO songs_table (song_title, category_id, singer_id, album_id, song_description, is_favorite) VALUES (%s, %s, %s, %s, %s, %s)",
                 (data["title"], data["category_id"], data["singer_id"], data["album_id"], data["description"], data["is_favorite"]))
    mysql.connection.commit()
    return jsonify({"message": "Song created"}), 201

@app.route("/songs/<int:song_id>", methods=["GET"])
def get_song(song_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM songs_table WHERE song_id = %s", (song_id,))
    song = cur.fetchone()
    if song is None:
        return jsonify({"error": "Song not found"}), 404
    column_names = [desc[0] for desc in cur.description]
    return jsonify(dict(zip(column_names, song)))

@app.route("/songs/<int:song_id>", methods=["PUT"])
def update_song(song_id):
    cur = mysql.connection.cursor()
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("UPDATE songs_table SET song_title = %s, category_id = %s, singer_id = %s, album_id = %s, song_description = %s, is_favorite = %s WHERE song_id = %s",
                 (data["title"], data["category_id"], data["singer_id"], data["album_id"], data["description"], data["is_favorite"], song_id))
    mysql.connection.commit()
    return jsonify({"message": "Song updated"})

@app.route("/songs/<int:song_id>", methods=["DELETE"])
def delete_song(song_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM songs_table WHERE song_id = %s", (song_id,))
    mysql.connection.commit()
    return jsonify({"message": "Song deleted"})
    

# Create a new category
@app.route('/category', methods=['POST'])
def create_category():
    try:
        data = request.json
        category_id = data['category_id']
        category_name = data['category_name']
        category_description = data['category_description']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO song_category_table(category_id, category_name, category_description) VALUES(%s, %s, %s)", (category_id, category_name, category_description))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Category created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM song_category_table")
        categories = cur.fetchall()
        cur.close()
        return jsonify([{'category_id': category[0], 'category_name': category[1], 'category_description': category[2]} for category in categories]), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Get a category by ID
@app.route('/category/<int:category_id>', methods=['GET'])
def get_category(category_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM song_category_table WHERE category_id = %s", (category_id,))
        category = cur.fetchone()
        cur.close()
        if category:
            return jsonify({'category_id': category[0], 'category_name': category[1], 'category_description': category[2]}), 200
        else:
            return jsonify({'message': 'Category not found'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Update a category
@app.route('/category/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    try:
        data = request.json
        category_name = data['category_name']
        category_description = data['category_description']

        cur = mysql.connection.cursor()
        cur.execute("UPDATE song_category_table SET category_name = %s, category_description = %s WHERE category_id = %s", (category_name, category_description, category_id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Category updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

# Delete a category
@app.route('/category/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM song_category_table WHERE category_id = %s", (category_id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': 'Category deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500
        
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
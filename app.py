from flask import Flask, jsonify, request
from flask_cors import CORS
from mysql.connector import connect, Error
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
def create_connection():
    """Create a database connection."""
    try:
        connection = connect(
            host="localhost",
            user="root",
            password="Ste12248",
            database="music360"
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
@app.route('/events', methods=['GET'])
def get_events():
    """Fetch events by genre."""
    genre_id = request.args.get('genre_id')
    if not genre_id:
        return jsonify({"error": "genre_id is required"}), 400

    connection = create_connection()
    if not connection:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT event_name, event_date, description
            FROM MusicEvents
            WHERE genre_id = %s
            ORDER BY event_date ASC
        """
        cursor.execute(query, (genre_id,))
        events = cursor.fetchall()
        print(events)
        return jsonify(events)  # Return data in JSON format
    except Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to fetch events"}), 500
    finally:
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)

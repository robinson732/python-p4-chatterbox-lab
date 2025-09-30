from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)

# --- Config ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # or Postgres if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Init DB & Migrate ---
db.init_app(app)
migrate = Migrate(app, db)

# ---------- ROUTES ----------

# GET /messages
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return jsonify([m.to_dict() for m in messages]), 200

# POST /messages
@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()

    if not data.get("body") or not data.get("username"):
        return {"error": "body and username required"}, 400

    new_message = Message(body=data["body"], username=data["username"])
    db.session.add(new_message)
    db.session.commit()

    return jsonify(new_message.to_dict()), 201

# PATCH /messages/<id>
@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    data = request.get_json()
    if "body" in data:
        message.body = data["body"]

    db.session.commit()
    return jsonify(message.to_dict()), 200

# DELETE /messages/<id>
@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get(id)
    if not message:
        return {"error": "Message not found"}, 404

    db.session.delete(message)
    db.session.commit()
    return {"message": "Deleted successfully"}, 200


if __name__ == '__main__':
    app.run(port=5555, debug=True)

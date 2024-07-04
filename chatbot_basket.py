from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot_basket.db'
db = SQLAlchemy(app)

class Basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(80), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Basket {self.item}>'

def init_db():
    # Crée la base de données et les tables
    db.create_all()
    # Importer les données depuis le fichier SQL
    with open('/mnt/data/chatbot_basket.sql', 'r') as f:
        sql_commands = f.read().split(';')
        for command in sql_commands:
            if command.strip():
                db.session.execute(command)
        db.session.commit()

@app.route('/')
def home():
    return "Chatbot is running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response_message = generate_response(user_message)
    return jsonify({"response": response_message})

def generate_response(user_message):
    # Exemple de traitement simple
    if "basket" in user_message.lower():
        items = Basket.query.all()
        response = "Here are the items in your basket:\n"
        for item in items:
            response += f"{item.quantity} x {item.item}\n"
        return response
    return "I don't understand your message."

if __name__ == '__main__':
    # Vérifiez si la base de données existe déjà
    if not os.path.exists('chatbot_basket.db'):
        init_db()
    app.run(debug=True)
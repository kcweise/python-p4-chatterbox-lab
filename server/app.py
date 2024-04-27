from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods = ['GET', 'POST'])
def messages():
    if request.method == 'GET':
        m = []
        for message in Message.query.order_by(Message.created_at.asc()).all():
            m_dict = message.to_dict()
            m.append(m_dict)
            
        return jsonify(m)
        
    elif request.method == 'POST':
        new_message = Message(
            body = request.json['body'],
            username = request.json['username'])
            
        db.session.add(new_message)
        db.session.commit()
        
        new_message_dict = new_message.to_dict()
                
        return jsonify(new_message_dict)

@app.route('/messages/<int:id>', methods = ['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    
    if request.method =='PATCH':
        for attr in request.json:
            setattr(message, attr, request.json.get(attr))
            
        db.session.add(message)
        db.session.commit()
        
        message_dict = message.to_dict()
        
        return jsonify(message_dict)
    
    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        
        response = make_response(
            {}, 200
        )
        return response
if __name__ == '__main__':
    app.run(port=5555)

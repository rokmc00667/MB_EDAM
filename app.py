from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Configure the PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/mediabox_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define a model for recordingsclass Recording(db.Model):
id = db.Column(db.Integer, primary_key=True)
channel = db.Column(db.String(100), nullable=False)
start_time = db.Column(db.DateTime, default=datetime.utcnow)
end_time = db.Column(db.DateTime, nullable=True)
file_path = db.Column(db.String(200), nullable=True)

def __repr__(self):
    return f"<Recording {self.channel} at {self.start_time}>"

# Initialize the databasewith app.app_context():
db.create_all()

@app.route('/')def home():
return "Welcome to mediabox!"

@app.route('/recordings', methods=['GET'])def get_recordings():
recordings = Recording.query.all()
return jsonify([{
    "id": r.id,
    "channel": r.channel,
    "start_time": r.start_time.strftime("%Y-%m-%d %H:%M:%S"),
    "end_time": r.end_time.strftime("%Y-%m-%d %H:%M:%S") if r.end_time else None,
    "file_path": r.file_path
} for r in recordings])

@app.route('/recordings', methods=['POST'])def add_recording():
data = request.get_json()
new_recording = Recording(
    channel=data['channel'],
    start_time=datetime.fromisoformat(data['start_time']),
    end_time=datetime.fromisoformat(data['end_time']) if 'end_time' in data else None,
    file_path=data.get('file_path', '')
)
db.session.add(new_recording)
db.session.commit()
return jsonify({"message": "Recording added"}), 201

if __name__ == '__main__':
app.run(debug=True)
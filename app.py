from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)
# Remplace par tes informations de connexion à la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://344595:3u1J93mjDC@mysql-photobooth.alwaysdata.net/photobooth_projetfinal'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration de Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'azertyuiopqsdfghjklmwxcvbn'  # Changez cela pour votre propre clé secrète
jwt = JWTManager(app)

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(45), nullable=False)
    prenom = db.Column(db.String(45), nullable=False)
    identifiant = db.Column(db.String(45), nullable=False)
    password = db.Column(db.String(45), nullable=False)
    droit = db.Column(db.String(45), nullable=False)

class Evenement(db.Model):
    __tablename__ = 'evenement'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(45), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('evenements', lazy=True))

class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2000), nullable=False)
    nom = db.Column(db.String(45))
    evenement_id = db.Column(db.Integer, db.ForeignKey('evenement.id'), nullable=False)
    evenement = db.relationship('Evenement', backref=db.backref('photos', lazy=True))

class Video(db.Model):
    __tablename__ = 'video'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2000), nullable=False)
    nom = db.Column(db.String(45))
    evenement_id = db.Column(db.Integer, db.ForeignKey('evenement.id'), nullable=False)
    evenement = db.relationship('Evenement', backref=db.backref('videos', lazy=True))

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # Ici, vous devriez vérifier les identifiants de l'utilisateur avec votre base de données
    # Pour simplifier, nous allons juste simuler une authentification réussie
    if username == "admin" and password == "secret":  # Remplacez ceci par une véritable vérification
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    return jsonify({"msg": "Mauvais nom d'utilisateur ou mot de passe"}), 401

@app.route('/evenements', methods=['GET'])
@jwt_required()
def get_evenements():
    evenements_list = Evenement.query.all()
    return jsonify([{'id': ev.id, 'nom': ev.nom, 'date': ev.date, 'description': ev.description, 'user_id': ev.user_id} for ev in evenements_list])

@app.route('/photos', methods=['GET'])
@jwt_required()
def get_photos():
    photos_list = Photo.query.all()
    return jsonify([{'id': p.id, 'url': p.url, 'nom': p.nom, 'evenement_id': p.evenement_id} for p in photos_list])

@app.route('/videos', methods=['GET'])
@jwt_required()
def get_videos():
    videos_list = Video.query.all()
    return jsonify([{'id': v.id, 'url': v.url, 'nom': v.nom, 'evenement_id': v.evenement_id} for v in videos_list])


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
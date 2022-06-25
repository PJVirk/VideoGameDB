from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class GameModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    progress = db.Column(db.Integer, nullable=False)
    difficulty = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Game(name = {name}, progress = {progress}, difficulty = {difficulty})"


game_put_args = reqparse.RequestParser()
game_put_args.add_argument("name", type=str, help="Name of the Game", required=True)
game_put_args.add_argument("progress", type=int, help="Progress Towards Completion", required=True)
game_put_args.add_argument("difficulty", type=str, help="Difficulty of the Game", required=True)

game_update_args = reqparse.RequestParser()
game_update_args.add_argument("name", type=str, help="Name of the Game")
game_update_args.add_argument("progress", type=int, help="Progress Towards Completion")
game_update_args.add_argument("difficulty", type=str, help="Difficulty of the Game")


resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'progress': fields.Integer,
    'difficulty': fields.String
}

class Game(Resource):
    @marshal_with(resource_fields)
    def get(self, game_id):
        result = GameModel.query.filter_by(id=game_id).first()
        if not result:
            abort(404, message="Game ID does not exist")
        return result, 200

    @marshal_with(resource_fields)
    def put(self, game_id):
        args = game_put_args.parse_args()
        result = GameModel.query.filter_by(id=game_id).first()
        if result:
            abort(409, message="Game ID already exists")
        game = GameModel(id=game_id, name=args['name'], progress=args['progress'], difficulty=args['difficulty'])
        db.session.add(game)
        db.session.commit()
        return '', 201

    @marshal_with(resource_fields)
    def patch(self, game_id):
        args = game_update_args.parse_args()
        result = GameModel.query.filter_by(id=game_id).first()
        if not result:
            abort(404, message="Game ID does not exist")

        if args['name']:
            result.name = args['name']
        if args['progress']:
            result.progress = args['progress']
        if args['difficulty']:
            result.difficulty = args['difficulty']

        db.session.commit()

        return '', 200

    @marshal_with(resource_fields)
    def delete(self, game_id):
        result = GameModel.query.filter_by(id=game_id).first()
        if not result:
            abort(404, message="Game ID does not exist")

        game = GameModel(id=game_id, name=args['name'], progress=args['progress'], difficulty=args['difficulty'])
        db.session.delete(game)
        db.session.commit()
        return '', 204


api.add_resource(Game, "/videogame/<int:game_id>")

if __name__ == "__main__":
    app.run(debug=True)

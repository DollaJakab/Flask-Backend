import os
import logging
from flask import Flask, jsonify
from flask_restful import Api, Resource, marshal_with, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

# Load environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/articles")
FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app, origins=[FRONTEND_ORIGIN])
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 10
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 5

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app, db)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    author = db.Column(db.String(50), nullable=False)

resource_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'content': fields.String,
    'author': fields.String,
}

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, help='Title required', location='json', required=True)
parser.add_argument('content', type=str, help='Content required', location='json', required=True)
parser.add_argument('author', type=str, help='Author required', location='json', default="Guest")

class CreateArticle(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        try:
            article = Article(title=args['title'], content=args['content'], author=args['author'])
            db.session.add(article)
            db.session.commit()
            return article, 201
        except Exception as e:
            logging.error(f"Error creating article: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500

class Articles(Resource):
    @marshal_with(resource_fields)
    def get(self):
        try:
            articles = Article.query.all()
            return articles, 200
        except Exception as e:
            logging.error(f"Error fetching articles: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500

class IndividualArticle(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        try:
            article = Article.query.get(id)
            if not article:
                return jsonify({"error": "Article not found"}), 404
            return article, 200
        except Exception as e:
            logging.error(f"Error fetching article: {str(e)}")
            return jsonify({"error": "Internal Server Error"}), 500

api.add_resource(CreateArticle, '/article')
api.add_resource(Articles, '/articles')
api.add_resource(IndividualArticle, '/articles/<int:id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
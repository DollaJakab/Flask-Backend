from flask import Flask
from flask_restful import Api, Resource, marshal_with, fields, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jakabdolla:5518@localhost/articles'
db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app,db)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    author = db.Column(db.String(50), nullable=False)

class ArticleTest(db.Model):
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
parser.add_argument('id', type=int, help='ID required', location='json')
parser.add_argument('title', type=str, help='Title required',location='json', required=True)
parser.add_argument('content', type=str, help='Content required',location='json', required=True)
parser.add_argument('author', type=str, help='Author required',location='json', default="Guest")


class CreateArticle(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        article = Article(title=args['title'], content=args['content'], author=args['author'])
        db.session.add(article)
        db.session.commit()
        return article, 201
    
class Articles(Resource):
    @marshal_with(resource_fields)
    def get(self):
        articles = Article.query.all()
        return articles, 200
    
class IndividualArticle(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        article = Article.query.get(id)
        return article, 200
    
class CreateArticleTest(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = parser.parse_args()
        article = ArticleTest(title=args['title'], content=args['content'], author=args['author'])
        db.session.add(article)
        db.session.commit()
        return article, 201

class ArticlesTest(Resource):
    @marshal_with(resource_fields)
    def get(self):
        articles = ArticleTest.query.all()
        return articles, 200
    
class IndividualArticleTest(Resource):
    @marshal_with(resource_fields)
    def get(self, id):
        article = ArticleTest.query.get(id)
        return article, 200

api.add_resource(CreateArticle, '/article')
api.add_resource(Articles, '/articles')
api.add_resource(IndividualArticle, '/articles/<int:id>')
api.add_resource(CreateArticleTest, '/test/article')
api.add_resource(ArticlesTest, '/test/articles')
api.add_resource(IndividualArticleTest, '/test/articles/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)
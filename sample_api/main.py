from flask import Flask 
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    views = db.Column(db.Integer, nullable = False)
    likes = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Video(name = {name}, views={views}, likes={likes})"


#db.create_all()

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'views': fields.Integer,
    'likes': fields.Integer

}

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type = str, help = "name of the video", required = True)
video_put_args.add_argument("likes", type = int, help = "likes of the video", required = True)
video_put_args.add_argument("views", type = int, help = "views of the video", required = True)

#videos = {}

# def abort_if_video_id_doesnt_exist(video_id):
#     if video_id not in videos:
#         abort(404, message = "video id is not valid...")
# def abort_if_video_id_exists(video_id):
#     if video_id in videos:
#         abort(409, message="the video already exists...")

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        # abort_if_video_id_doesnt_exist(video_id)
        # return videos[video_id] #will get information of any video id you put here
        result = VideoModel.query.get(id=video_id)
        return result
    def put(self, video_id):
        abort_if_video_id_exists(video_id)
        args = video_put_args.parse_args()
        videos[video_id] = args
        return args, 201 #201 stands for it was created, 200 stands for everything is okay
    def delete(self, video_id):
        abort_if_video_id_doesnt_exist(video_id)
        del videos[video_id]
        return '', 204

api.add_resource(Video, "/video/<int:video_id>")
 

if __name__ == "__main__":
    app.run(debug = True)

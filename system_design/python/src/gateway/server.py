import os, gridfs, pika, json
from flask import Flask, request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util
from bson.objectid import ObjectId

server = Flask(__name__)
server.config["MONGO_URI"] = "mongodb://host.minikube.internal:27017/microservice_converter"

mongo = PyMongo(server)

fs_videos = gridfs.GridFS(mongo.db, collection="videos")
fs_mp3s = gridfs.GridFS(mongo.db, collection="mp3s")

connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()

@server.route("/login", methods=["POST"])
def login():
    token, err = access.login(request)

    if not err:
        return token
    else:
        return err
    
@server.route('/upload', methods=['POST'])
def upload():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    try:
        if access["admin"]:
            if len(request.files)>1 or len(request.files)<1:
                return "exactly 1 file required", 400
            
            for _, f in request.files.items():
                err = util.upload(f, fs_videos, channel, access)

                if err:
                    return err
            return "Success!", 200
        else:
            return "not authorized", 401
    except Exception as err:
        print(err)
    
@server.route('/download', methods=['GET'])
def download():
    access, err = validate.token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required", 400
        
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out, download_name=f'{fid_string}.mp3', as_attachment=True)
        except Exception as err:
            print(err)
            return "internal server error"

    return "not authorized", 401

if __name__=="__main__":
    server.run(host="0.0.0.0", port=8080)
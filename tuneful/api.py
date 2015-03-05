import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

import models
import decorators
from tuneful import app
from database import session
from utils import upload_path

song_schema = {
  "properties": {
    "file": {
      "filename" : {"type" : "string" }
    }
  }
}

@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def get_songs():
  """Get a list of songs"""
  
  songs = session.query(models.Song)
  songs = songs.all()
  
  data = json.dumps([song.as_dictionary()for song in songs])
  return Response(data, 200, mimetype="application/json")

@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def post_song():
  data = request.json
  
  fileid = data["file"]["id"]
  
  try:
    validate(data, song_schema)
  except ValidationError as error:
    data = {"message": error.message}
    return Response(json.dumps(data), 422, mimetype="application/json")
  
  file = session.query(models.File)
  file = file.filter(models.File.id == fileid).first()
  
  file = models.File(filename=file.filename)
  song = models.Song(song=file)
  session.merge(song)
  session.commit()
  
  data = json.dumps(song.as_dictionary())
  return Response(data, 201, mimetype="application/json")

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)

@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    file = request.files.get("file")

    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    db_file = models.File(filename=filename)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))

    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")
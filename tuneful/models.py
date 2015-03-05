import os.path

from flask import url_for
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship

from tuneful import app
from database import Base, engine

class Song(Base):
  __tablename__ = "songs"
  
  id = Column(Integer, primary_key=True)
  file_id = Column(Integer, ForeignKey('files.id'), nullable=False)
  
  def as_dictionary(self):
    song = {
      "id": self.id,
      "file": {
        "id": self.song.id,
        "filename": self.song.filename
      }
    }
    return song
    
class File(Base):
  __tablename__ = "files"
  
  id = Column(Integer, primary_key=True)
  filename = Column(String, nullable=False)
  songs = relationship('Song', backref='song')
  
  def as_dictionary(self):
    file = {
      "id": self.id,
      "filename": self.filename
    }
    return file
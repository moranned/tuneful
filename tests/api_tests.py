import unittest
import os
import shutil
import json
from urlparse import urlparse
from StringIO import StringIO

import sys; print sys.modules.keys()
# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.utils import upload_path
from tuneful.database import Base, engine, session

class TestAPI(unittest.TestCase):
    """ Tests for the tuneful API """

    def setUp(self):
        """ Test setup """
        self.client = app.test_client()

        # Set up the tables in the database
        Base.metadata.create_all(engine)

        # Create folder for test uploads
        os.mkdir(upload_path())

    def tearDown(self):
        """ Test teardown """
        session.close()
        # Remove the tables and their data from the database
        Base.metadata.drop_all(engine)

        # Delete test upload folder
        shutil.rmtree(upload_path())

    def testGetSong(self):
      """ Getting a single post from a populated database """
      file1 = models.File(filename="Riders_on_the_Storm.mp3")
      song1 = models.Song(song=file1)

      session.add_all([file1, song1])
      session.commit()

      response = self.client.get("/api/songs", headers=[("Accept", "application/json")])

      self.assertEqual(response.status_code, 200)
      self.assertEqual(response.mimetype, "application/json")

      songs = json.loads(response.data)
      for song in songs:
        self.assertEqual(song["file"]["filename"], "Riders_on_the_Storm.mp3")
   
    def testPostSong(self):
      """Posting a new song"""
      song = {"file":{"filename": "LA_Woman.mp3"}}
      
      response = self.client.post("/api/songs", data=json.dumps(song), content_type="application/json", headers=[("Accept", "application/json")])
      
      self.assertEqual(response.status_code, 201)
      self.assertEqual(response.mimetype, "application/json")
      
      #file_data = json.loads(file_response.data)

      
      
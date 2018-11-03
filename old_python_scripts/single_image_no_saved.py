#!/usr/bin/env python

# Copyright 2015 Google, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Draws squares around detected faces in the given image."""

import argparse

# [START vision_face_detection_tutorial_imports]
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
# [END vision_face_detection_tutorial_imports]

import cv2



# [START vision_face_detection_tutorial_send_request]
def detect_face(content, max_results=4):
    """Uses the Vision API to detect faces in the given file.

    Args:
        face_file: A file-like object containing an image with faces.

    Returns:
        An array of Face objects with information about the picture.
    """
    # [START vision_face_detection_tutorial_client]
    client = vision.ImageAnnotatorClient()
    # [END vision_face_detection_tutorial_client]

    # content = face_file.read()
    image = types.Image(content=content)

    return client.face_detection(image=image).face_annotations
# [END vision_face_detection_tutorial_send_request]


# [START vision_face_detection_tutorial_process_response]
def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)

    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save(output_filename)
# [END vision_face_detection_tutorial_process_response]


def explicit():
    from google.cloud import storage
    import os, sys

    # Explicitly use service account credentials by specifying the private key
    # file.
    print('Credendtials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    test = open(os.path.join(__location__, 'SibbSquadV2-8e1c8113e39c.json'), 'r');
    loc = sys.path[0] + '/SibbSquadV2-8e1c8113e39c.json'
    storage_client = storage.Client.from_service_account_json('SibbSquadV2-8e1c8113e39c.json')
    # print(test)
    test.read()
    # print(sys.path[0])
    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)

def cvImage():

    cam = cv2.VideoCapture(1)

    cv2.namedWindow("test")

    img_counter = 0
    max_results = 4
    output_filename = "test2.png"

    # while True:
    ret, frame = cam.read()
    cv2.imshow("test", frame)


    cam.release()

    cv2.destroyAllWindows()

    faces = detect_face(frame, max_results)
    print('Found {} face{}'.format(
        len(faces), '' if len(faces) == 1 else 's'))

    print('Writing to file {}'.format(output_filename))
    # Reset the file pointer, so we can read the file again
    frame.seek(0)
    highlight_faces(frame, faces, output_filename)
    return


if __name__ == '__main__':
    explicit()
    cvImage()

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
import time
import io
import os

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
    # print("1")
    test.read()
    # print(sys.path[0])
    # print("2")
    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    # print(buckets)


def highlight_objects(image, faces, output_filename):
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
        if (face.name in["Person", "Man", "Woman", "Girl", "Boy"]) and (face.score > 0.65):
            box = [(vertex.x*im.width, vertex.y*im.height)
                   for vertex in face.bounding_poly.normalized_vertices]
            draw.line(box + [box[0]], width=5, fill='#00ff00')

    im.save("output_filename.png")

def label_finding(name, out):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(name, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    # draw = ImageDraw.Draw(image)

    objects = client.object_localization(image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
        for vertex in object_.bounding_poly.vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))

    highlight_objects(name, objects, out)


def cvImage():
    curr = 0
    cam = cv2.VideoCapture(1)
    cv2.namedWindow("test")
    img_counter = 0

    for x in range(0, 20):
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        # time.sleep(1) #sleep is in seconds.
        if (x%20 == 0): #select 1 in 20 images to analyze
            temp = curr % 10
            string ="test" + str(temp) + ".png" #LIMITS MAX NUMBER OF PICTURES WE WILL SAVE
            img_name = string.format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1

            # curr_image = "test1.png"
            img_out_name = "test" + str(temp) + "out.png"
            out = "test2out.png"
            max_results = 10
            label_finding(img_name, out)
            curr += 1
        time.sleep(0.05)
    cam.release()
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    explicit()
    cvImage()

#!/usr/bin/env python

"""Draws squares around detected faces in the given image."""

import argparse
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw
import cv2
import time
import io
import os
from roomba_tracking import *

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
    test.read()
    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())


def highlight_objects(image, faces, output_filename, verbosity):
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
    num_peeps = 0

    for face in faces:
        if (face.name in["Person", "Man", "Woman", "Girl", "Boy"]) and (face.score > 0.65):
            if (verbosity > 0):
                box = [(vertex.x*im.width, vertex.y*im.height)
                       for vertex in face.bounding_poly.normalized_vertices]
                draw.line(box + [box[0]], width=5, fill='#00ff00')
            num_peeps+=1

    if(verbosity > 1):
        im.save(output_filename)
    return num_peeps

def label_finding(name, out, verbosity):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    client = vision.ImageAnnotatorClient()

    with open(name, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    objects = client.object_localization(image=image).localized_object_annotations
    if(verbosity > 1):
        print('Number of objects found: {}'.format(len(objects)))
        for object_ in objects:
            print('\n{} (confidence: {})'.format(object_.name, object_.score))
            print('Normalized bounding polygon vertices: ')
            for vertex in object_.bounding_poly.normalized_vertices:
                print(' - ({}, {})'.format(vertex.x, vertex.y))

    peep_num = highlight_objects(name, objects, out, verbosity)
    return peep_num


def cvImage(verbosity):
    curr = 0
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0
    last_peepcount = 0
    peep_num = 0

    for x in range(0, 20):
        ret, frame = cam.read()
        cv2.imshow("test", frame)
        k = cv2.waitKey(1)
        if (x%20 == 0): #select 1 in 20 images to analyze
            last_peepcount = peep_num
            temp = curr % 10
            string ="test" + str(temp) + ".png" #LIMITS MAX NUMBER OF PICTURES WE WILL SAVE
            img_name = string.format(img_counter)
            cv2.imwrite(img_name, frame)
            if (verbosity > 0):
                print("{} written!".format(img_name))
            img_counter += 1
            img_out_name = "test" + str(temp) + "out.png"
            max_results = 10
            peep_num = label_finding(img_name, img_out_name, verbosity)
            curr += 1
        # Peep_num logic, where we save if there's 1 person and remembers when it drops to 0
        if(peep_num == 0 & last_peepcount > 0):
            #Take sweet, sweet revenge if the light is on
            follow_person()
        time.sleep(0.05)
    cam.release()
    cv2.destroyAllWindows()
    return


if __name__ == '__main__':
    verbosity = 2
    explicit()
    cvImage(verbosity)

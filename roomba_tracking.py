#! /usr/bin/env python

from room_checking_threaded import *
from pycreate2 import Create2
from time import sleep
import time
import random

from Arduino_Shoot import take_shot, wait_for_shadow
from mqtt_lib import Communicator


def bounding_boxes(name, out_name, verbosity):
    """
	Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    print("starting")
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

    im = Image.open(name)
    draw = ImageDraw.Draw(im)
    new_list = []
    for item in objects:
        if (item.name in["Person", "Man", "Woman", "Girl", "Boy"]) and (item.score > 0.65):
            if (verbosity > 0):
                box = [(vertex.x*im.width, vertex.y*im.height)
                       for vertex in item.bounding_poly.normalized_vertices]
                draw.line(box + [box[0]], width=5, fill='#00ff00')
            new_list.append(item)
    if(verbosity > 1):
        im.save(out_name)
    image_size = (im.width, im.height)
    # new_list.insert(0,new_tup)
    return new_list, image_size


def calculate_areas(people, height, width):
    """
    Calculates the area of each bounding box a set of bounding boxes.
    Returns the information of the largest.

    people : normalized bounding boxes.
    h, w : image height and width.
    """
    max_area = 0
    max_area_location = 0
    for i in range(len(people)):
        sum = 0
        for vertex in people[i].bounding_poly.normalized_vertices:
            sum += vertex.x * width + vertex.y * height
        sum /= 4
        if (sum > max_area):
            max_area = sum
            max_area_location = i
    return (max_area_location, max_area)


def calculate_center(item, width, height):
    """
    Calculates center of bounding box associated with found object.
    """
    sumx = 0
    sumy = 0
    for vertex in item.bounding_poly.normalized_vertices:
        sumx += vertex.x * width
        sumy += vertex.y * height
    sumx /= 4
    sumy /= 4
    return (sumx, sumy)


def angle_to_turn(width, xcoord):
    FOV = 45
    xfrac = xcoord*1.0/width - 0.5
    return xfrac * FOV

bot = Create2('/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DN026EMT-if00-port0')
bot.start()
bot.full()

cam = cv2.VideoCapture(1)
cv2.namedWindow("test")

def follow_person(communicator, verbosity = 2):
    adjustment_constant = 1.2

    img_counter = 0
    current = 0
    previous_max = None
    current_max = None
    sees_person = False
    x=0

    #Threadpool
    pool = ThreadPool(processes=1)
    async_result = None

    # Three to five seconds
    next_fire = time.time() + 5

    while c.is_armed:
        ret, frame = cam.read()
        if sees_person:
            bot.drive_straight(80)
        else:
            bot.drive_stop()

        if async_result:
            # Steer
            (degree, current_max, sees_person) = async_result.get()

            print("Degree: ", degree)
            bot.turn_angle(-degree*adjustment_constant, speed=40)
            bot.drive_stop()
            async_result = None

            if time.time() > next_fire:
                # FIRE!
                next_fire = time.time() + (2 + 3*random.random())
                take_shot()

        if(x%15 == 0):
            # Send an image to Google
            cv2.imshow("test", frame)
            k = cv2.waitKey(1)
            async_result = pool.apply_async(roomba_threaded, (x, frame, current_max, verbosity, bot)) # tuple of args for foo

        time.sleep(0.05)
        x+=1

    # cam.release()
    # cv2.destroyAllWindows()
    return
	# Find the center of the top of the box
	# Calculate motion necessary to travel towards that point
	# Turn and move wheels towards that point.

def roomba_threaded(x, frame, current_max, verbosity, bot):
    name = "following_test" + str(x % 150) + ".png"
    out_name = "following_test" + str(x % 150) + "_out.png"
    cv2.imwrite(name, frame)
    # Find bounding boxes for every person in the roomba's field of view.
    people, (width, height) = bounding_boxes(name, out_name, verbosity)
    # width = image_size[0]
    # height = image_size[1]
    degree = 0
    if people:
        sees_person = True
        (location, area) = calculate_areas(people, height, width)
        current_max = people[location]
        center = calculate_center(current_max, height, width)

        #TODO: Turn
        degree = angle_to_turn(width, center[0])
    else:
        sees_person = False
    return (degree, current_max, sees_person)

def main(verbosity = 2):
    c = Communicator()
    while True:
        wait_for_shadow()
        if c.is_armed:
            take_shot()
            follow_person(c, verbosity)


if __name__ == '__main__':
    verbosity = 2
    main(verbosity)
    # follow_person(Communicator(), verbosity)

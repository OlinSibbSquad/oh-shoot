#! /usr/bin/env python

from room_checking_threaded import *
from pycreate2 import Create2
from time import sleep


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


def follow_person(verbosity = 2):
    #roombaaaaaa
    bot = Create2('/dev/serial/by-id/usb-FTDI_FT231X_USB_UART_DN026EMT-if00-port0')
    bot.start()
    bot.full()
    sensors = bot.get_sensors()
    # This camera will point to the camera on the Roomba.
    cam = cv2.VideoCapture(1)
    cv2.namedWindow("test")
    img_counter = 0
    current = 0
    previous_max = None
    current_max = None
    # The number of times to search for a person.
    CYCLES = 150
    sees_person = False
    x=0

    #Threadpool
    pool = ThreadPool(processes=1)
    async_result = None
    while True:
        x+=1
        ret, frame = cam.read()
        if sees_person:
            bot.drive_straight(80)
        else:
            bot.drive_stop()

        if(x%15 == 0):
            cv2.imshow("test", frame)
            k = cv2.waitKey(1)
            if async_result:
                (current_max, sees_person) = async_result.get()
            async_result = pool.apply_async(roomba_threaded, (x, frame, current_max, verbosity, bot)) # tuple of args for foo



        time.sleep(0.05)
    cam.release()
    cv2.destroyAllWindows()
    return
	# Find the center of the top of the box
	# Calculate motion necessary to travel towards that point
	# Turn and move wheels towards that point.

def roomba_threaded(x, frame, current_max, verbosity, bot):
    name = "following_test" + str(x) + ".png"
    out_name = "following_test" + str(x) + "_out.png"
    cv2.imwrite(name, frame)
    # Find bounding boxes for every person in the roomba's field of view.
    people, (width, height) = bounding_boxes(name, out_name, verbosity)
    # width = image_size[0]
    # height = image_size[1]
    adjustment_constant = 1.2
    if people:
        sees_person = True
        (location, area) = calculate_areas(people, height, width)
        current_max = people[location]
        center = calculate_center(current_max, height, width)

        #TODO: Turn
        degree = angle_to_turn(width, center[0])
        print("Degree: ", degree)
        bot.turn_angle(-degree*adjustment_constant, speed=40)
        bot.drive_stop()
    else:
        sees_person = False
    return (current_max, sees_person)

if __name__ == '__main__':
    verbosity = 2
    explicit()
    follow_person(verbosity)

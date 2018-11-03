#! /usr/bin/env python

from room_checking import *

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

    for item in objects:
        if (item.name in["Person", "Man", "Woman", "Girl", "Boy"]) and (item.score > 0.65):
            if (verbosity > 0):
                box = [(vertex.x*im.width, vertex.y*im.height)
                       for vertex in item.bounding_poly.normalized_vertices]
                draw.line(box + [box[0]], width=5, fill='#00ff00')
    if(verbosity > 1):
        im.save(out_name)
    return out_name

def follow_person(verbosity):	
	# This camera will point to the camera on the Roomba.
	cam = cv2.VideoCapture(0)
	cv2.namedWindow("test")
	img_counter = 0
	current = 0
	
	# The number of times to search for a person.
	for x in range(0, CYCLES):
		ret, frame = cam.read()
		cv2.imshow("test", frame)
		k = cv2.waitKey(1)
		name = "following_test" + str(x) + ".png"
		out_name = "following_test" + str(x) + "_out.png"
		cv2.imwrite(name, frame)
	# Find bounding boxes for every person in the roomba's field of view.
		bounding_boxes(name, out_name, verbosity)
		time.sleep(0.05)
	cam.release()
	cv2.destroyAllWindows()
	return
	# Find the center of the top of the box
	# Calculate motion necessary to travel towards that point
	# Turn and move wheels towards that point.


if __name__ == '__main__':
    verbosity = 2
    explicit()
    follow_person(verbosity)

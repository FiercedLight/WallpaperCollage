import argparse
import random
import glob
import pickle
from PIL import Image, ImageDraw

def crop(image_obj, coords, saved_location):
    cropped_image = image_obj.crop(coords)
    #cropped_image.save(saved_location)
    #cropped_image.show()

with open("RectangleData", 'rb') as f:
    rectangle_array = pickle.load(f)

with open("SquareData", 'rb') as f:
    square_data = pickle.load(f) 
    # 0 : square_size
    # 1 : square_precision
    # 2 : width_limit_min
    # 3 : width_limit_max
    # 4 : height_limit_min
    # 5 : height_limit_max

image_list = []
for filename in glob.glob('images/*.png'): #assuming gif
    im=Image.open(filename)
    im.convert('RGBA')
    image_list.append(im)

grid_image = Image.open("square.png")
result = Image.new('RGBA', (int(square_data[0]), int(square_data[0])))

for rect in rectangle_array:
    cur_image = image_list[random.randrange(0,len(image_list))]
    while 1:
        (cur_image_width,cur_image_height) = cur_image.size
        if(cur_image_width - rect[2]*square_data[1] < 0 or cur_image_height - rect[3]*square_data[1] < 0):
            cur_image = cur_image.resize((cur_image.size[0]*2,cur_image.size[1]*2))
            continue
        else:
            break
    width_random = int((cur_image_width - rect[2]*square_data[1])*random.random())
    height_random = int((cur_image_height - rect[3]*square_data[1])*random.random())

    #print(str(width_random)+" "+str(height_random))

    cutted_image = Image.new('RGBA', (int(rect[2]*square_data[1]), int(rect[3]*square_data[1])))
    crop_box =  (width_random,height_random,width_random + rect[2]*square_data[1] ,height_random + rect[3]*square_data[1])
    cutted_image = cur_image.crop(crop_box)
       
    #print(str(crop_box))
    #print(str(cur_image.size))
    result.paste(cutted_image, (int(rect[0]*square_data[1]), int(rect[1]*square_data[1])))

result = Image.alpha_composite(result,grid_image) 

filename = "collage.png"
print("Saving {}".format(filename))
result.save(filename)




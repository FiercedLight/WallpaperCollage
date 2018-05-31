import random
import sys
import argparse
from PIL import Image, ImageDraw
import pickle


print(
    "For best results pick square size, width, and height divisible by precision"
)
print("and pick min limits same as precision.")

square_size = int(input('Square size (600): ') or "600")
square_precision = float(input("Square precision (50): ") or "50")
square_step = int(square_size / square_precision)
square_array = [[0 for x in range(square_step)] for y in range(square_step)]
rectangle_array = []

width_limit_max = int(
    int(input('Rectangle width max limit (200): ') or "200") /
    square_precision)
width_limit_min = int(
    int(input('Rectangle width min limit (precision): ') or square_precision) /
    square_precision)
height_limit_max = int(
    int(input('Rectangle height max limit (300): ') or "300") /
    square_precision)
height_limit_min = int(
    int(input('Rectangle height min limit (precision): ') or square_precision)
    / square_precision)
print ("")

square_size = int(square_size / square_precision) * square_precision

random_margin_w = int(width_limit_max - width_limit_min)
random_margin_h = int(height_limit_max - height_limit_min)

curX = 0
curY = 0

limX = 0

gen_w = 0
gen_h = 0

curRect = 1

success = 0
try_number = 5000


def print_square():
    global square_array
    global square_step
    for j in range(0, square_step):
        for i in range(0, square_step):
            sys.stdout.write(str(square_array[j][i]).zfill(2) + " ")
        sys.stdout.write("\n")
    sys.stdout.flush()
    pass


def find_next_limit_x():
    global curX
    global curY
    global limX
    limX = curX
    while limX < square_step and square_array[curY][limX] == 0:
        limX += 1
    pass


def find_next_coord():
    global curX
    global curY
    while curY < square_step and square_array[curY][curX] != 0:
        curX += 1
        if (curX >= square_step):
            curX = 0
            curY += 1
    pass

def draw_border():
    
    curX = 0
    curY = 0
    filecode=""
    image = Image.new(mode='RGBA', size=(int(square_size), int(square_size)), color="#00000000")
    draw = ImageDraw.Draw(image)
    for rect in rectangle_array:
        filecode+=str(rect[0])+str(rect[1])
        line_v = ((rect[0]*square_precision, rect[1]*square_precision), (rect[0]*square_precision, (rect[1]+rect[3])*square_precision))
        line_h = ((rect[0]*square_precision, rect[1]*square_precision), ((rect[0]+rect[2])*square_precision, rect[1]*square_precision))
        draw.line(line_v, fill=(255,255,255,255), width=3)
        draw.line(line_h, fill=(255,255,255,255), width=3)
    del draw
    #filename = "square-{}-{}.png".format(filecode,square_size)
    filename = "square.png"
    print("Saving {}".format(filename))
    image.save(filename)

def export_square_data():
    print("Saving SquareData")
    with open("SquareData", 'wb') as f:
        pickle.dump((square_size,square_precision,width_limit_min,width_limit_max,height_limit_min,height_limit_max), f)

def export_rect_data():
    print("Saving RectangleData")
    with open("RectangleData", 'wb') as f:
        pickle.dump(rectangle_array, f)

#gen_w = width_limit_min+random.randint(0,random_margin_w)
#gen_h = height_limit_min+random.randint(0,random_margin_h)

#print("Width: " + str(gen_w)
#        + " Height: " + str(gen_h) + "\n")
#        for j in range(0,gen_h):
#            for i in range(0,gen_w):
#                square_array[curY+j][curX+i]=curRect

for t in range(0, try_number):
    for k in range(1, 400):
        gen_w = 0
        gen_h = 0

        find_next_coord()  # set curX, curY
        #print("Coord: " + str(curX) + ","+str(curY))
        if (curY >= square_step):
            success = 1
            break
        find_next_limit_x()  # set limX
        #print("Limit X: " + str(limX))
        #print("Tile: " + str(k))

        if ((limX - curX) >= width_limit_max):  # can create random rect
            #print("can create random width")
            gen_w = width_limit_min + random.randint(0, random_margin_w)
        elif ((limX - curX) >= width_limit_min):  # must use free space
            #print("must use free space width")
            gen_w = limX - curX
        else:  # can't create rect fitting specs
            #print("fail width")
            break

        if ((square_step - curY) >=
            height_limit_max):  # can create random rect
            gen_h = height_limit_min + random.randint(0, random_margin_h)
            #print("can create random height")
        elif ((square_step - curY) >= height_limit_min):  # must use free space
            gen_h = square_step - curY
            #print("must use free space height")
        else:  # can't create rect fitting specs
            #print("fail height")
            break

        #print("Width: " + str(gen_w) # create rect
        #    + " Height: " + str(gen_h) + "\n")
        rectangle_array.append((curX,curY,gen_w,gen_h))
        for j in range(0, gen_h):
            for i in range(0, gen_w):
                square_array[curY + j][curX + i] = k

        #print_square()

    if (success):
        success = t+1
        break
    #print(t)
    square_array = [[0 for x in range(square_step)] for y in range(square_step)]
    curX = 0
    curY = 0
    limX = 0
    gen_w = 0
    gen_h = 0
    rectangle_array=[]

if (success):
    print("Final Square (Tried " + str(success) + " times)")
    print("")
    #print(str(rectangle_array))
    print_square()
    export_rect_data()
    export_square_data()
    draw_border()
else:
    print("Tried " + str(try_number) +
          " times and couldn't find a valid solution.")
    print("Try setting height or width min limit lower.")


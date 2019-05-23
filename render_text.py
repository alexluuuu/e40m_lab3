from PIL import Image


def render_alpha_num(char, ser):
    my_bmp = Image.open('font.png')
    data = my_bmp.getdata()
    location_x = ord(char) % 256
    location_y = (ord(char) // 256)*8

    pixels = my_bmp.load() # this is not a list, nor is it list()'able
    width, height = my_bmp.size
    #This is to commit

    for x in range(location_x, location_x + 32):
        for y in range(location_y, location_y + 32):
            cpixel = pixels[x, y]
            if (cpixel == (255, 255, 255)):
                print ("", end =" ")
            else:
                print ("0", end =" ")

    # for i,p in enumerate(data):
    #     if (i % 512 == 0): print ()
    #     if (p == (255, 255, 255)):
    #         print ("", end =" ")
    #     else:
    #         print (0, end ="")
	#ser.write(grid_str.encode())

render_alpha_num("c", "c");

#def output_string(str, ser):
	#for char in str:
	#	render_alpha_num(char)
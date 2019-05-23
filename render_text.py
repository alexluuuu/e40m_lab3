from PIL import Image


def render_alpha_num(char, ser):
    grid = [['0' for i in range(8)] for j in range(8)]
    my_bmp = Image.open('font.png')
    data = my_bmp.getdata()
    location_x = (ord(char[0]) % 16) *32
    location_y = (ord(char[0]) % 16) *32

    pixels = my_bmp.load() # this is not a list, nor is it list()'able
    width, height = my_bmp.size
    #This is to commit
    arr_y = 0
    for y in range(location_y, location_y + 32):
        arr_x = 0
        for x in range(location_x, location_x + 32):
            cpixel = pixels[x, y]
            if (cpixel == (255, 255, 255)):
                grid[arr_x//4][arr_y//4] = 1
            else:
                grid[arr_x//4][arr_y//4] = 0
            arr_x += 1
        arr_y += 1
    
    for arr in grid:
        for elem in arr:
            print(elem, end ="")
        print()

render_alpha_num("0", "c")

#def output_string(str, ser):
	#for char in str:
	#	render_alpha_num(char)
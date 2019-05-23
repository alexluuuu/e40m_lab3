from PIL import Image
import time 


def render_alpha_num(char):
    grid = [['0' for i in range(8)] for j in range(8)]
    my_bmp = Image.open('font.png')
    data = my_bmp.getdata()
    char_num = ord(char) - 1 if ord(char) < ord('a') else ord(char)
    location_x = (char_num % 16) *32
    location_y = (char_num // 16) *32

    pixels = my_bmp.load() # this is not a list, nor is it list()'able
    width, height = my_bmp.size
    arr_y = 0
    for y in range(location_y, location_y + 32):
        arr_x = 0
        for x in range(location_x, location_x + 32):
            cpixel = pixels[x, y]
            if (cpixel == (255, 255, 255)):
                grid[arr_y//4][arr_x//4] = '1'
            else:
                grid[arr_y//4][arr_x//4] = '0'
            arr_x += 1
        arr_y += 1
    
    return grid
    # for arr in grid:
    #     for elem in arr:
    #         print("\u25A0" if elem == 1 else " " , end ="")
    #     print()

def render_text(text, ser):
    charsToDisplay = []
    # Build Letter Arrays
    for letter in text:
        charsToDisplay.append(render_alpha_num(letter))
    charsToDisplay.append([['0' for i in range(8)] for j in range(8)])
    totalCols = len(text) * 8
    # Traverse all frames col by col
    frame = [['0' for i in range(8)] for j in range(8)]
    for startCol in range (0,totalCols):
        if startCol % 8 == 0:
            render(charsToDisplay[startCol//8], ser)
        else: 
            idx_in_letter = startCol % 8
            # Portion from first letter
            for col in range(idx_in_letter, 8):
                for row in range(0,8):
                    frame[row][col-idx_in_letter] = charsToDisplay[startCol//8][row][col]
            # Portion from next letter
            for col in range(0, idx_in_letter):
                for row in range(0,8):
                    frame[row][col + 8 - idx_in_letter ] = charsToDisplay[startCol //8 + 1][row][col]
            render(frame, ser)
        time.sleep(0.08)


def render(grid, ser) :
    grid_str = "".join(["".join(row) for row in grid]) + "\n"
    ser.write(grid_str.encode())
    
    for arr in grid:
        for elem in arr:
            print("\u25A0" if elem == 1 else " " , end ="")
        print()

#render_text("Hello World", "")

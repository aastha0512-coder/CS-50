from multiset import *
from pixelsquare import *
def censor(image, forbidden):
    '''

    '''
    for i in range(image._dimension):
            for j in range(image._dimension):
                for k in range(forbidden._first):
                    value = image._colours[i][j]
                    if (forbidden._data.access(k) == value):
                       image._colours[i][j] = "x"

    print(image)
    return image

def mystery(dim, first, second):
    a = PixelSquare(dim)
    print(a)
    for index in range(0, dim // 2):
        number = dim - 2*index-1
        if index % 2 == 0:

            a.rectangle(index, index,number, number, first)
        else:
            a.rectangle(index, index,number, number, second)

    return a

k = mystery(6,"#","+")
a = Multiset()
b = Multiset()
print(a)
a.add("#")
print(a)
a.add("+")
print(a)
print(a._first)
z = censor(k, b)
print(z)
def enlarge(image:PixelSquare,scale:int):
    dim = image.size()
    ps = PixelSquare(dim*scale)

    for row in range(dim):
        for col in range(dim):
            colour = image.get_colour(row,col)
            ps.rectangle(scale*row ,scale*col ,scale , scale, colour)
    return ps
l = enlarge(z, 2)
print(l)


def blur(image, block_size):
    x, y = 0, 0
    while y < image.size():
        while x < image.size():
            b, w = 0, 0
            for j in range(y, y+block_size):
                for i in range(x, x+block_size):
                    if image.get_colour(j,i) == '#':
                        b += 1
                    if image.get_colour(j,i) == '.':
                        w += 1
            if b > w:
                blur_val = '#'
            elif b < w:
                blur_val = '.'
            else:
                blur_val = '-'
            for j in range(y, y+block_size):
                for i in range(x, x+block_size):
                    image.set_colour(j,i,blur_val)
            x += block_size
        x = 0
        y += block_size
    return image

print(k)
p = blur(k,3)
print(p)
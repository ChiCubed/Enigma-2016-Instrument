import math

FOV_HORIZONTAL = math.pi # Full FOV in radians
FOV_VERTICAL = math.pi
IMG_WIDTH = 1920.0
IMG_HEIGHT = 1080.0

MALLET_WIDTH = 2.3 # cm

def circle_to_3D(x, y, r):
    # Given the x and y position of a circle
    # from the edge of an image
    # and the radius of the circle in pixels,
    # calculates the x, y and z position of the
    # corresponding sphere in 3D space.
    # These values are not necessarily accurate in
    # the real world: rather, they are calibrated
    # based on repeated tests of the program.

    horiz_theta = 2*r/IMG_WIDTH*FOV_HORIZONTAL
    vert_theta = 2*r/IMG_HEIGHT*FOV_VERTICAL

    z = MALLET_WIDTH/math.tan(horiz_theta)

    CENTER = (IMG_WIDTH/2,IMG_HEIGHT/2)

    return z*math.tan((x-CENTER[0])/IMG_WIDTH*FOV_HORIZONTAL), \
           z*math.tan((y-CENTER[1])/IMG_HEIGHT*FOV_VERTICAL), \
           z

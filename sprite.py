'''Make creating games with 2D sprites more easy and clean.'''

# This module is designed to be used with the graphics module to make
# creating games with 2D sprite more clean and to help learn objects
# in Python.

import graphics
import math

class Sprite:
    '''Class that represents a moveable 2D image.

    :param float x: The x-coordinate, in pixels, of the center of the sprite.

    :param float y: The y-coordinate, in pixels, of the center of the
        sprite.

    :param str image_name: The file name of the image to draw when
        drawing the sprite.  The image must be a gif file.
    '''

    def __init__(self, x=0, y=0, image_name=None):
        '''Initialize a Sprite.

        :param float x: The x-coordinate, in pixels, of the center of the
            sprite.

        :param float y: The y-coordinate, in pixels, of the center of the
            sprite.

        :param str image_name: The file name of the image to draw when
            drawing the sprite.  The image must be a gif file.
        '''
        self.x = x
        '''The x-coordinate, in pixels, of the center of this sprite.'''
        self.y = y
        '''The y-coordinate, in pixels, of the center of this sprite.'''
        self.image_name = image_name
        '''The name of the image to draw, when drawing this sprite.'''

    def __getattr__(self, name):
        '''Get this Sprite's attribute's

        :param string name: The name of the attribute to get.

        :return: (obj) -- The requested attribute.

        This function adds the synthetic attrbutes top, bottom, left,
        and right, which are the locaitons of the edges of this
        sprite, to the built-in attributes x, y, image, and
        image_size.

        '''
        if name == 'top':
            return self.y - self.height / 2
        elif name == 'bottom':
            return self.y + self.height / 2
        elif name == 'left':
            return self.x - self.width / 2
        elif name == 'right':
            return self.x + self.width / 2
        else:
            return super().__getattr__(name)

    def __setattr__(self, name, value):
        '''Set an attribute of this Sprite.

        :param string name: The name of the attribute to set.

        :param obj value: The value to set the attribute to.

        This function sets the dependent attribute ``image_size`` when
        the ``image_name`` attribute changes.

        '''
        if name == 'width':
            return
        if name == 'height':
            return
        super().__setattr__(name, value)
        if name == 'image_name':
            (width, height) = graphics.image_size(value)
            super().__setattr__('width', width)
            super().__setattr__('height', height)

    def __str__(self):
        '''Returns a string representation of this Sprite.

        :return: (str) -- A string that represents this sprite.
        '''
        string_list = []
        attribute_dictionary = vars(self)
        for attribute_name in attribute_dictionary:
            attribute_value = str(attribute_dictionary[attribute_name])
            attribute_string = '{}={}'.format(attribute_name, attribute_value)
            string_list.append(attribute_string)
        return '[{}]'.format(', '.join(string_list))

    def uncollide(self, other_sprite):
        '''Moves this Sprite so that it does not overlap with another Sprite.

        :param Sprite other_sprite: Another Sprite object.

        Moves this sprite the minimum amount so that it is not
        overlapping with ``other_sprite``.  If there is no overlap, it
        does nothing.

        '''
        if not self.collides(other_sprite):
            return
        top_overlap = other_sprite.bottom - self.top
        bottom_overlap = self.bottom - other_sprite.top
        left_overlap = other_sprite.right - self.left
        right_overlap = self.right - other_sprite.left
        if (top_overlap <= bottom_overlap and
            top_overlap <= left_overlap and
            top_overlap < right_overlap):
            self.y += top_overlap
        elif (bottom_overlap < top_overlap and
              bottom_overlap < left_overlap and
              bottom_overlap <= right_overlap):
            self.y -= bottom_overlap
        elif (left_overlap <= right_overlap and
              left_overlap < top_overlap and
              left_overlap <= bottom_overlap):
            self.x += left_overlap
        elif (right_overlap < left_overlap and
              right_overlap <= top_overlap and
              right_overlap < bottom_overlap):
            self.x -= right_overlap

    def collides(self, other_sprite):
        '''Returns whether this Sprite is colliding with another Sprite.

        :param Sprite other_sprite: Another Sprite object.

        :return: (bool) -- Returns True if this sprite is overlapping
          with ``other_sprite`` and False otherwise.

        '''
        if self.top >= other_sprite.bottom:
            return False
        if self.bottom <= other_sprite.top:
            return False
        if self.left >= other_sprite.right:
            return False
        if self.right <= other_sprite.left:
            return False
        return True

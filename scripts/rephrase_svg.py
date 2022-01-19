# this class helps to insert "hidden" (css) features
# into a svg image.

import os
import pandas as pd
import regex as re

from __init__ import INDEX_DICT

class TightSVG:
    '''This class alows to append a tree svg with notes, etc.
    '''
    def __init__(self, svg_path):
        '''Initialize from svg_file.
        '''
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"File '{svg_path}' does not exist.")
        self.file = svg_path
        self.get_max_length()
        return

    def get_max_length(self):
        '''Return the y axis length of the image in pixels.
        '''
        with open(self.file, "r") as file:
            for line in file.readlines():
                if not line.startswith("<svg") : continue
                self.width = int(re.search('width="([0-9]*)"', line)[1])
                self.height = int(re.search('height="([0-9]*)"', line)[1])
                return
        raise RuntimeError("File is no proper svg.")

    def a_elements(self):
        '''Construct a generator that iterates through all a elements.
        '''
        file = open(self.file, "r")
        a_str_lines = []
        a_str_started = False
        for line in file.readlines():
            if not a_str_started:
                if line.strip().startswith("<a "):
                    a_str_started = True
                    a_str_lines.append(line)
            else:
                a_str_lines.append(line)
                if line.strip().startswith("</a>"):
                    yield "".join(a_str_lines)
                    a_str_lines = []
                    a_str_started = False
        file.close()
        return

    def build_profiles(self):
        '''Make profiles of all birds.
        '''
        for a_str in self.a_elements():
            a_el = ATeam(a_str)


# end TightSVG

class ATeam:
    '''This is a wrapper for a single <a> element.
    '''
    def __init__(self, a_str, language="EN"):
        '''Initialize by a given a element from the svg.
        '''
        self.index = ["a", "g1", "img1", "/g1", "/a"]
        self.str = a_str
        self.split_str()
        
        # store the psoitions of element and image on svg
        self.get_position()
        self.get_img_position()

        # load the alias of the bird
        self.lang = language
        self.get_bird_name()
        self.BIRD_DATA = pd.read_csv(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_INFO"])
        self.data = self.BIRD_DATA[self.BIRD_DATA["CODE"]==self.bird_alias].squeeze()
        return

    def split_str(self):
        '''Split up string into elements.
        '''
        self.lines = {k : ln for ln, k in
                zip(self.str.split("\n"), self.index)}
        return

    def get_position(self):
        '''Obtain the position of the element in the svg.
        '''
        self.x, self.y = [int(v) for v in
                re.search("translate\( ([0-9]*), ([0-9]*)", self.lines["g1"]).groups()]
        return

    def get_img_position(self):
        '''Obtain position and size of image.
        '''
        self.img_x, self.img_y = [int(v) for v in 
                re.search('image x="([\-0-9]*)" y="([\-0-9]*)"', self.lines["img1"]).groups()]
        self.img_dims = {k : int(val) for k, val in zip(["width", "height"], re.search(
            'width="([\-0-9]*)" height="([\-0-9]*)"', self.lines["img1"]).groups())}
        return

    def add_class(self, class_label="bird", element="g1"):
        '''Add a class label to the g element.
        '''
        self.lines[element] = self.lines[element].replace(
                "g transform", f'g class="{class_label}" transform')
        return

    def duplicate_g(self):
        '''Add g2 that is the same as the g1.
        '''
        g2_index = ["g2", "img2", "/g2"]
        g1_end = self.get_key_index("/g1")
        self.index = self.index[:g1_end+1] + g2_index + self.index[g1_end+1:]
        for k1, k2 in zip(["g1", "img1", "/g1"], g2_index):
            self.lines[k2] = str(self.lines[k1])
        return

    def get_key_index(self, key):
        '''Obtain numeric index of a key of the lines dict.
        '''
        indx = [i for i, k in enumerate(self.index) if k==key][0]
        return indx

    def write_str(self):
        '''Write a string to print out.
        '''
        out = "\n".join([self.lines[i] for i in self.index])
        return out

    def change_position(self, new_x, new_y, element_name="g2"):
        '''Change the position of an element.
        '''
        self.lines[element_name] = self.lines[element_name].replace(
                f"translate( {self.x}, {self.y} )",
                f"translate( {new_x}, {new_y} )")
        return

    def get_bird_name(self):
        '''Obtain the alias of the bird of the current a string.
        '''
        self.bird_alias = re.search("([A-Za-z]*).png", self.lines["img1"])[1]
        return

    def scale_image(self, element_name="img2", factor=4):
        '''Scale an image by a given factor.
        '''
        self.lines[element_name] = self.lines[element_name].replace(
                f'width="{self.img_dims["width"]}" height="{self.img_dims["height"]}"',
                f'width="{int(self.img_dims["width"]*factor)}" height="{int(self.img_dims["height"]*factor)}"')
        return

    def thumb_to_image(self, element_name="img2"):
        '''Replace the thubs image by an image with better resolution.
        '''
        self.lines[element_name] = self.lines[element_name].replace("thumbs", "images_std")
        return

    def add_line_after(self, line, foregone_element, new_key, tabbed=True):
        '''Insert a line after a given element.
        '''
        # update index and lines dict
        indx = self.get_key_index(foregone_element)
        self.index = self.index[:indx+1] + [new_key] + self.index[indx+1:]
        # use tabs of foregeone element
        if tabbed : tabs = self.lines[foregone_element].split("<")[0]
        else : tabs = ""
        self.lines[new_key] = f"{tabs}{line}"
        return

    def add_text(self, text, label="LABEL", x=0, y=0, color="black", font_size="12px", foregone_element="img2"):
        '''Add text element with name of the bird.
        '''
        text_str = (
                f'<text x="{x}" y="{y}" fill="{color}" font-size="{font_size}">'
                f'{text}</text>')
        self.add_line_after(text_str, foregone_element, label, tabbed=True) 
        return

    def add_rectangle(self, x=0, y=0, width=100, height=100, edge_radius=20, color="black", stroke_color="grey", opacity=0.95, foregone_element="img2"):
        '''Add a reactangle shape after a given element.
        '''
        rect_str = (f'<rect x="{x}" y="{y}" rx="{edge_radius}" ry="{edge_radius}" width="{width}" height="{height}"'
                f' style="fill:{color};stroke:{stroke_color};stroke-width:5;opacity:{opacity}" />')
        self.add_line_after(rect_str, foregone_element, "rectangle", tabbed=True)
        return



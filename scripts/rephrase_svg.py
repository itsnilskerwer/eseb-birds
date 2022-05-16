# this class helps to insert "hidden" (css) features
# into a svg image.

import os
import pandas as pd
import regex as re

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class TightSVG:
    '''This class alows to append a tree svg with notes, etc.
    '''
    def __init__(self, svg_path, language="EN"):
        '''Initialize from svg_file.
        '''
        if not os.path.exists(svg_path):
            raise FileNotFoundError(f"File '{svg_path}' does not exist.")
        self.file = svg_path
        self.get_max_length()
        self.lang = language
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

    def get_prolog(self):
        '''Return part of svg before a elements.
        '''
        file = open(self.file, "r")
        p_str_lines = []
        for line in file.readlines():
            if line.strip().startswith("<a "): break
            p_str_lines.append(line)
        file.close()
        prolog = "".join(p_str_lines)
        return prolog

    def get_postlog(self):
        '''Return part of svg after a elements.
        '''
        file = open(self.file, "r")
        p_str_lines = []
        a_str_started = False
        a_str_ended = False
        for line in file.readlines():
            if a_str_ended:
                p_str_lines.append(line)
                if line.strip().startswith("<a "):
                    a_str_ended = False
                    a_str_started = True
                    p_str_lines = []
            elif a_str_started:
                a_str_ended = line.strip().startswith("</a>")
            elif line.strip().startswith("<a "): 
                a_str_started = True
        postlog = "".join(p_str_lines)
        return postlog

    def build_profiles(self, image_scale_factor=4, font_size=20, max_character_per_line=40, correction=4):
        '''Build Bird profiles within a given svg image.
        '''
        TOPICS_KEYS = ["Distribution", "Wingspan", "Weight", "Diet", "Genome size"]
        if self.lang == "EN" :
            topics =dict(zip(TOPICS_KEYS, TOPICS_KEYS))
        else :
            TOPICS_GR = ["Κατανομή", "Ανοιγμα φτερών", "Βάρος", "Διατροφή", "Μέγεθος γονιδιώματος"]  # , "Καλό να γνωρίζω"]
            topics = dict(zip(TOPICS_KEYS, TOPICS_GR))
        first_line_correction = len(f'<tspan font-weight="bold">:</tspan>')
        
        profile_elements = []
        for a_el in self.a_elements():
            a_inst = ATeam(a_el, language=self.lang)

            if a_inst.bird_alias == "question" : profile_elements.append(a_inst.write_str())
            # simple element labelling and copying
            a_inst.duplicate_g()
            a_inst.add_class()
            a_inst.add_class(class_label="hide", element="g2")

            # build all the text info for the profile:
            ## we track the position of lines with a growing y coordinate
            y_shift = a_inst.img_y + a_inst.img_dims["height"]*image_scale_factor +int((font_size+5)*1.2)

            ## names are used as header
            bird_name = a_inst.data.loc["Name"]
            a_inst.add_text(f'<tspan font-weight="bold">{bird_name}</tspan>', label="bird_name",
                            x=a_inst.img_x, y=y_shift, color="black", font_size=f"{int(font_size*1.2)}px")
            latin_name = a_inst.data.loc["Latin"]
            a_inst.add_text(latin_name, label="latin_name", x=a_inst.img_x, y=y_shift+int(font_size*1.2),
                        color="black", font_size=f"{int(font_size*1.2)}px", style="italic", 
                        foregone_element="bird_name")
            foregone_label = "latin_name"
            y_shift += +int((font_size+5)*1.2)

            ## tabular data is added line after line
            for i, topic in enumerate(TOPICS_KEYS):
                topic_id = topic.lower().replace(" ", "_")
                header = f'<tspan font-weight="bold">{topics[topic]}:</tspan>'
                topic_str = f"{header}{''.join([' ']*correction)}{a_inst.data.loc[topic_id]}"
                lines = break_line(topic_str, max_character_per_line, correction=correction,
                                   firstline_correction=first_line_correction-correction)
                # sometimes data is too large for the profile box
                for j, line in enumerate(lines):
                    y_shift += font_size+5
                    # we add a tab space for lines that are not the first (headers)
                    if j > 0 : line = f'{"".join([" "]*correction)}{line}'
                    a_inst.add_text(line, label=f"{topic_id}_{j}", x=a_inst.img_x, y=y_shift,
                            color="black", font_size=f"{font_size}px", foregone_element=foregone_label)
                    foregone_label = f"{topic_id}_{j}"
                y_shift += 5
            
            # add sequence
            y_shift += font_size+5
            seq = a_inst.get_sequence(bird_name=a_inst.bird_alias).strip().replace("<dd>","").replace("</dd>", "").replace("span", "tspan")
            if self.lang == "EN" :
                a_inst.add_text(f'<tspan font-weight="bold">DNA fragment:</tspan>  ..{seq}..', label="seq", x=a_inst.img_x, y=y_shift,
                                color="black", font_size=f"{font_size}px", foregone_element=foregone_label)
            else :
                a_inst.add_text(f'<tspan font-weight="bold">κομμάτι του DNA:</tspan>  ..{seq}..', label="seq", x=a_inst.img_x, y=y_shift,
                                color="black", font_size=f"{font_size}px", foregone_element=foregone_label)
            y_shift += int((font_size+5)*1.2)+font_size

            # obtain rectangle coordinates
            rect_dims = adjust_rectangle(
                a_inst.img_x, a_inst.img_y, a_inst.img_dims["width"]*image_scale_factor,
                y_shift, 20)
            new_pos = get_new_position(rect_dims, a_inst.x, a_inst.y, a_inst.img_x, a_inst.img_y, 
                             self.width, self.height, buffer=10)
            
            # add the background rectangle
            a_inst.add_rectangle(foregone_element="g2", color="white", **rect_dims)
            
            # change the position of the image, scale it and change its source
            a_inst.change_position(new_pos["x"], new_pos["y"])
            a_inst.scale_image()
            a_inst.thumb_to_image()

            profile_elements.append(a_inst.write_str())
        return "\n".join(profile_elements)

    def rephrase(self, **kwargs):
        '''Rewrite svg image with bird profiles.
        '''
        parts = [
            self.get_prolog(),
            self.build_profiles(**kwargs),
            self.get_postlog()
                ]
        return "\n".join([p.strip("\n") for p in parts])
# end TightSVG

class ATeam(AbstractPage):
    '''This is a wrapper for a single <a> element.
    '''
    def __init__(self, a_str, language="EN"):
        '''Initialize by a given a element from the svg.
        '''
        super().__init__(language=language, stop_html_init=True)
        self.index = ["a", "g1", "img1", "/g1", "/a"]
        self.ext_index = ["a", "g1", "g2", "img1", "/g2", "/g1", "/a"]
        self.str = a_str
        self.split_str()
        
        # store the psoitions of element and image on svg
        self.get_position()
        self.get_img_position()

        # load the alias of the bird
        self.get_bird_name()
        self.data = self.BIRD_DATA[self.BIRD_DATA["CODE"]==self.bird_alias].squeeze()
        return

    def split_str(self):
        '''Split up string into elements.
        '''
        G2_INDICATOR = "<g>"
        self.lines = {k : ln for ln, k in
                zip(self.str.split("\n"), self.index)}
        if G2_INDICATOR in  self.lines["img1"]:
            self.lines = {k : ln for ln, k in
                    zip(self.str.split("\n"), self.ext_index)}
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

    def add_text(self, text, label="LABEL", x=0, y=0, color="black", font_size="12px", 
            style="normal", foregone_element="img2"):
        '''Add text element with name of the bird.
        '''
        text_str = (
                f'<text x="{x}" y="{y}" fill="{color}" font-size="{font_size}" font-style="{style}">'
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
# end ATeam


# helpers
def adjust_rectangle(x, y, width, height, frame_width):
    '''Define parameters of rectangle by given image/text shape info.
    '''
    rect_dict = {
        "x": int(x - frame_width),
        "y": int(y - frame_width),
        "width": int(width + 2*frame_width),
        "height": int(height + 2*frame_width)
    }
    return rect_dict

def avoid_borders(position, image_length, object_length, correction=0, buffer=0):
    '''Optimize position of object such that object does not go out of borders.

    correction is the relative coordinate value that is set in inner elements
    buffer is a framing area that should not be covered either.
    '''
    available_image_length = image_length - object_length - buffer
    scaling_factor = available_image_length / image_length
    new_position = buffer + (position)*scaling_factor - correction
    return int(new_position)

def get_new_position(rectangle_dict, old_x, old_y, img_x, img_y,
                     total_width, total_height, buffer=10):
    '''Adjust the positions of a g element.
    '''
    X_FACTOR = .2
    pos_dict = {
        "x": int(img_x*X_FACTOR),
        "y": avoid_borders(old_y, total_height, rectangle_dict["height"],
                           correction=img_y, buffer=buffer)
    }
    return pos_dict

def break_line(string, max_line_length, correction=0, firstline_correction=0):
    '''Break a string into mutliple, if it is too long.
    '''
    if len(string) <= max_line_length+correction+firstline_correction : return [string]
    # if the string is too long we start splitting it into words
    words = string.split(" ")
    string_length = 0
    firstline_list = []
    for i, word in enumerate(words):
        string_length += len(word)
        if string_length > max_line_length+correction+firstline_correction:
            if len(firstline_list)==0:
                lines = [word]
                i += 1
            else : lines = [" ".join(firstline_list)]
            remaining_lines = " ".join(words[i:])
            for line in break_line(remaining_lines, max_line_length, correction=correction):
                lines.append(line)
            return lines
        firstline_list.append(word)
        string_length += 1
    raise RuntimeError("There is a coding mistake. One should never reach this.")

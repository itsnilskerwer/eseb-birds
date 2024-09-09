# here we include the class that designs the 
# html pages for successful placements of
# each bird species

import dominate as dm
from dominate.tags import *
import os
import pandas as pd
import yaml

from abstract_page import AbstractPage
from abstract_page import get_placement_species_list
from __init__ import INDEX_DICT

class RightPlacementPage(AbstractPage):
    '''Builder class for a given bird species.
    '''
    def __init__(self, bird_name, language="EN", stop_html_init=False):
        '''Initiaize object with a given name.
        '''
        self.name = bird_name
        
        super().__init__(language=language, stop_html_init=stop_html_init)
        self.get_data()
        return
    
    # helpers
    def check_name(self, bird_name):
        '''Check if bird name is in list.
        '''
        return self.BIRD_DATA["CODE"].str.match(bird_name).any()

    def check_placementname(self, bird_name):
        '''Check if bird name occurs in the list of birds that should be
        phylogenetically placed.
        '''
        return bird_name in get_placement_species_list(language=self.lang)

    def get_data(self):
        '''Select the data of the bird name from the whole `BIRD_DATA`.
        '''
        self.data = self.BIRD_DATA[self.BIRD_DATA["CODE"]==self.name].squeeze()
        return


    def make_title(self):
        '''Build a title for the HTML.
        '''
        file_texts = os.path.join(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_TEXTS"], "success.yml")
        self.texts = yaml.safe_load(open(file_texts, "r"))

        # this can be edited.
        # so far, we simply take the latin name.
        if not hasattr(self, "data"):
            self.get_data()
        title = self.data.loc["Latin"]
        return title
    
    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["PLACEMENT_HTML_DIR"],
                f"{self.name}_success.html")
        return os.path.abspath(file_name)

    def make_tree_img_path(self, bird_name, non_relative=False):
        '''Build name of path for a bird image.
        '''
        assert self.check_name(bird_name), f"{bird_name} is not in list."

        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"],
                f"tree_{bird_name}_answer.svg")
        if non_relative : return os.path.abspath(file_name)
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))

    def make_sequence_div(self): # todo refactor and add to seq info page
        '''Create the sequence div with the lines connecting the character strings.
        '''
        seq1 = "TGTGACAGCC" # TODO edit
        seq2 = "TGTGACAGCCGTCGGT" # TODO edit
        with div(id='sequence'):
            self.add_sequence_with_lines(seq1, seq2)
        return
    
    def add_sequence_with_lines(self, seq1, seq2):
        '''Add sequences with connecting lines to the HTML.
        '''
        table_content = self.generate_sequence_table(seq1, seq2)
        with table():
            for row_index, row in enumerate(table_content):
                with tr():
                    for cell in row:
                        if row_index == 1:
                            if cell == '|':
                                td(cls='line')
                            elif cell == '':
                                td(cls='no-border')
                            else:
                                td(cell, cls='sequence-char')
                        else:
                            if cell == '':
                                td(cls='no-border')
                            else:
                                td(cell, cls='no-box')
                    """ for cell in row:
                        if cell == '|':
                            td(cls='line')
                        elif cell == '':
                            td(cls='no-border')
                        else:
                            td(cell, cls='sequence-char') """

    def generate_sequence_table(self, seq1, seq2):
        '''Generate a table-like structure with sequences and lines.
        '''
        max_len = max(len(seq1), len(seq2))
        seq1 = seq1.ljust(max_len, '-')
        seq2 = seq2.ljust(max_len, '-')
        
        table_content = [[], [], []]  # Three rows: seq1, lines, seq2
        for c1, c2 in zip(seq1, seq2):
            table_content[0].append(c1)
            
            if c1 == c2 or c1 == '-' or c2 == '-':
                table_content[1].append('|')
                table_content[2].append(c2)
            else:
                table_content[1].append('')  # Placeholder for the line
                table_content[2].append(c2)


        return table_content
    
    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        self.define_header()
        with div(cls="row", id="main-content"):
            self.column1()
            self.column2()
        return

    def column1(self):
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column tree"):
            tree_path = self.make_tree_img_path(self.name, non_relative=True)
            self.plot_with_info(tree_path)
        return

    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        # make subtitle
        page_subtitle = self.texts["maintext1"]["FILL_IN"]
        
        
        with div(cls="column"):
            self.add_divider()
            self.make_sequence_div()
            self.add_divider()
            p("Our computer analysis confirms that this bird fits into the marked position.") # TODO text
            h2(page_subtitle)
            # p(self.texts["maintext2"]["FILL_IN"])
            self.define_infopagelink()
            self.define_moreinfolink()
            self.define_startplacmentlink()
        return

    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title with name as species
        page_title = f"{self.texts['header']['FILL_IN']} {self.data.loc['Name']}"
        with div():
            attr(id="header")
            h1(page_title)
        return

    def plot_with_info(self, image_path):
        '''Add image to html document and annotate it with background info.
        '''
        from rephrase_svg import TightSVG
        from io import StringIO
        from dominate.util import raw
        # we use this as image alternativ text
        license_info = self.texts["imgalt"]["FILL_IN"]
        # this is the image caption
        license_link = self.texts["imgtext"]["FILL_IN"]
        
        # it is a tree
        img_content = "tree"
        with div():
            attr_id = "image"
            attr(id=attr_id)
            tsvg = TightSVG(image_path, language=self.lang)
            svg_io = StringIO(tsvg.rephrase())
            self.paste_svg_io(image_path, svg_io)
            if isinstance(license_link, str):
                figcaption(raw(license_link))
            else:  # for missing data
                figcaption("Missing.")
        return

    def add_divider(self):
        '''Add a div-divider element with three centrally aligned dots.'''
        with div(cls="div-divider"):
            span("•")
            span("•")
            span("•")
        return

    def define_infopagelink(self):
        '''Make a small button that brings the user to the info page.
        '''
        from bird_pages import BirdPage
        bp = BirdPage(self.name, language=self.lang, stop_html_init=True)
        bp_path = os.path.relpath(bp.make_page_path(), os.path.dirname(self.make_page_path()))
        with form():
            input_(
                type="button",
                value=self.texts["button1"]["FILL_IN"],
                onclick=f"window.location.href='{bp_path}'")
        return

    def define_moreinfolink(self):
        '''Make a small button that brings the user to a specific web URL for more information.
        '''
        web_url = "https://github.com/pierrebarbera/epa-ng"
        with form():
            input_(
                type="button",
                value=self.texts["button3"]["FILL_IN"],
            onclick=f"window.open('{web_url}', '_blank')")
        return

    def define_startplacmentlink(self):
        '''Make a small button that brings the user back to the start page for PPs.
        '''
        from title_page import TitlePage
        tp = TitlePage(language=self.lang, stop_html_init=True)
        tp_path = os.path.relpath(tp.make_page_path(), os.path.dirname(self.make_page_path()))
        with form():
            input_(
                type="button",
                value=self.texts["button2"]["FILL_IN"],
                onclick=f"window.location.href='{tp_path}'")
        return

# end RightPlacementPage


# helpers

###############
def main():
    for lang in [ln for ln in INDEX_DICT.keys() if len(ln)==2]:
        bird_names = get_placement_species_list(language=lang)
        for bird_name in bird_names:
            bird_name = bird_name.strip()
            rp = RightPlacementPage(bird_name, language=lang)
            rp.build_html()
            rp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


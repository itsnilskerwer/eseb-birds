# here we include the core class that designs the 
# page that initiates the placement game

import dominate as dm
from dominate.tags import *
import os
import pandas as pd
import yaml

from abstract_page import AbstractPage
from abstract_page import get_placement_species_list
from __init__ import INDEX_DICT

class StartPlacementPage(AbstractPage):
    '''Builder class for the start page fro placement game.
    '''
    def make_title(self):
        '''Build a title for the HTML.
        '''
        file_texts = os.path.join(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_TEXTS"], "start_placement.yml")
        self.texts = yaml.safe_load(open(file_texts, "r"))

        # this can be edited.
        # so far we take a simple title.
        title = self.texts["urltitle"]["FILL_IN"]
        return title
    

    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                f"start_placement.html")
        return os.path.abspath(file_name)


    def make_tree_img_path(self, non_relative=False):
        '''Build name of path for the tree image.
        '''
        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"],
                f"tree.svg")
        if non_relative : return os.path.abspath(file_name)
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))

    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        self.define_header()
        with div(cls="row", id="main-content"):
            self.column1()
            self.column2()
        return

    def define_stylesheet(self):
        '''Define the style sheet for the html head.
        '''
        super().define_stylesheet()
        # define path
        css_rawpath = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["CSS_DIR"],
                'two_columns.css')
        css_path = os.path.relpath(os.path.abspath(css_rawpath),
                os.path.dirname(self.make_page_path()))
        # set stylesheet for two columns
        link(rel='stylesheet', href=css_path)
        return

    
    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title with name as species
        page_title = self.texts["header"]["FILL_IN"]
        # page_subtitle = self.texts["subheader"]["FILL_IN"]

        with div():
            attr(id="header")
            h1(page_title)
            # h2(em(page_subtitle))
        return

    def link_phylogenetics_info(self):
        '''Link out to page that informs about phylogenetics.
        '''
        from phylogenetics_page import PhylogeneticsPage
        ip_abspath = PhylogeneticsPage(language=self.lang, stop_html_init=True).make_page_path()
        ip_path = os.path.relpath(ip_abspath, os.path.dirname(self.make_page_path()))
        with form():
            input_(
                type="button",
                value=self.texts["button1"]["FILL_IN"],
                onclick=f"window.location.href='{ip_path}'")
        return

    def start_game_link(self):
        '''Link to start the game.
        '''
        from placement_pages import PlacementPage
        new_birds = get_placement_species_list(language=self.lang)
        pp = PlacementPage(new_birds[1], language=self.lang, stop_html_init=True)
        pp_path = os.path.relpath(pp.make_page_path(), os.path.dirname(self.make_page_path()))
        with form():
            input_(
                type="button",
                value=self.texts["button2"]["FILL_IN"],
                onclick=f"window.location.href='{pp_path}'"
            )
        return
    
    def define_seq_info_link(self):
        '''Link to information page about DNA and sequencing.
        '''
        from sequences_page import SequencesPage
        ip_abspath = SequencesPage(language=self.lang).make_page_path()
        ip_path = os.path.relpath(ip_abspath, os.path.dirname(self.make_page_path()))
        with form():
            input_(
                type="button",
                value=self.texts["button"]["FILL_IN"],
                onclick=f"window.location.href='{ip_path}'")
        return

    def plot_with_info(self, image_path):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
        from io import StringIO
        from rephrase_svg import TightSVG
        # we use this as image alternativ text
        license_info = "These are the birds we already know from greece."
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
            figcaption(raw(license_link))
        return
    
    def add_divider(self):
        '''Add a div-divider element with three centrally aligned dots.'''
        with div(cls="div-divider"):
            span("•")
            span("•")
            span("•")
        return

    def show_sequences(self):
        '''Plot the unknown sequences. Edited to one sequence for dev purpose.
        '''
        from dominate.util import raw
        from placement_pages import PlacementPage
        new_birds = get_placement_species_list(language=self.lang)
        for i, bird in enumerate(new_birds[:1], start=1): # edited to display only one sequence for now
            pp = PlacementPage(bird, language=self.lang, stop_html_init=True)
            pp_path = os.path.relpath(pp.make_page_path(), os.path.dirname(self.make_page_path()))
            with p(href=pp_path): # edited to remove dynamic build and switch to static content
                #p(make_seq(bird))
                sequence = self.get_sequence(bird_name=bird)
                sequence = sequence.replace('<dd><span',
                        '<dd>~~~<span')
                sequence = sequence.replace('</span></dd>',
                        '</span>~~~</dd>')
                raw(f"{sequence}<br>") # raw(f"{i}) {sequence}<br>")
        return

    def column1(self): # todo Move all text convos
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column"):
            with div(cls="text-container"):
                p("Learning about local birds is important information for airport safety staff. They have provided the lab with a small sample from a dead bird to analyze. The lab has analyzed the bird sample and found a short DNA sequence that couldn't be identified.")
            with div(cls="sequence-container"):
                self.show_sequences()
            with div(cls="sequence-container"):
                self.define_seq_info_link()
            self.add_divider()
            with div(cls="text-container"):
                p("Luckily, your lab has developed a special computer program. It can calculate the most likely placement of the unknown bird sequence, amongst its evolutionary relatives (a phylogenetic tree).")
            with div(cls="text-container"):    
                self.link_phylogenetics_info()
            self.add_divider()
            with div(cls="text-container"): 
                p("Help to identify which bird species belongs to the unknown sequence.")
            # p(self.texts["maintext"]["FILL_IN"]) 
            self.add_divider()
            with div(cls="text-container"):
                p("Your colleague says:")
            # self.add_divider()
            with div(cls="text-container"):
                p("I've been looking at bird pictures all week... I really need some rest.")
            self.add_divider()
            
            with div(cls="text-container"):
                self.start_game_link()
        return


    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        # from dominate.util import raw
        return
# end TitlePage

# helpers
def make_seq(bird_name, language="EN"):
    '''Retrieve a random sequence of a bird.
    '''
    from random import choice
    seq = "".join(
             map(lambda x: choice("ATGC"), range(10)))
    return seq

###############
def main():
    for lang in [ln for ln in INDEX_DICT.keys() if len(ln)==2]:
        sp = StartPlacementPage(language=lang)
        sp.build_html()
        sp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


# here we include the class that designs the 
# html pages for successful placements of
# each bird species

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from abstract_page import AbstractPage
from abstract_page import get_placement_species_list
from __init__ import INDEX_DICT

class RightPlacementPage(AbstractPage):
    '''Builder class for a given bird species.
    '''
    def __init__(self, bird_name, language="EN"):
        '''Initiaize object with a given name.
        '''
        self.name = bird_name
        super().__init__(language=language)
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

    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        self.define_header()
        with div(cls="row"):
            self.column1()
            self.column2()
        return

    def column1(self):
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column"):
            tree_path = self.make_tree_img_path(self.name, non_relative=True)
            self.plot_with_info(tree_path)
        return

    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        # make subtitle 
        page_subtitle = ("You are a great researcher. Your dry "
            "lab team approved that this bird fits into the "
            "phylogenetic placement")
        
        with div(cls="column"):
            p(page_subtitle)
            self.define_infopagelink()
        return

    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title with name as species
        page_title = f"Successfully placed: {self.data.loc['Name']}"
        with div():
            attr(id="header")
            h1(page_title)
        return

    def plot_with_info(self, image_path):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
        # we use this as image alternativ text
        license_info = "Right placement in tree."
        # this is the image caption
        license_link = "Our wet lab sent us this data after sequencing of the bird."
        # it is a tree
        img_content = "tree"
        with div():
            attr_id = "image"
            attr(id=attr_id)
            self.paste_svg(image_path)
            if isinstance(license_link, str):
                figcaption(raw(license_link))
            else:  # for missing data
                figcaption("Missing.")
        return

    def define_infopagelink(self):
        '''Make a small button that brings the user to the info page.
        '''
        from bird_pages import BirdPage
        bp = BirdPage(self.name, language=self.lang)
        bp_path = os.path.relpath(bp.make_page_path(), os.path.dirname(self.make_page_path()))
        with form():
            input_(
                    type="button",
                    value="Learn more about this bird...",
                    onclick=f"window.location.href='{bp_path}'")
        return
# end RightPlacementPage


# helpers

###############
def main():
    for lang in ["EN", "GR"]:
        bird_names = get_placement_species_list(language=lang)
        for bird_name in bird_names:
            bird_name = bird_name.strip()
            rp = RightPlacementPage(bird_name, language=lang)
            rp.build_html()
            rp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


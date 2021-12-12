# here we include the class that designs the 
# html pages for successful placements of
# each bird species

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from abstract_page import AbstractPage
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


    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        self.define_header()
        self.plot_with_info()
        return

    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title with name as species
        page_title = f"Successfully placed: {self.data.loc['Name']}"
        # make subtitle of latin name in italics
        page_subtitle = ("You are a great researcher. Your dry "
            "lab team approved that this bird fits into the "
            "phylogenetic placement")
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
            self.define_infopagelink()
        return

    def plot_with_info(self):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
        
        # get image location
        image_file = self.make_img_path()
        # image_file = self.data["Photolink"]
        # get license information
        license_info = self.data["license notice for plain text "]
        # get license link
        license_link = self.data["license notice HTML (https://lizenzhinweisgenerator.de/)"]
        with div():
            attr(id="image")
            with figure():
                attr(id="habitus")
                img(src=image_file,
                        alt=license_info)
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
        bp_path = bp.make_page_path()
        with form():
            input_(
                    type="button",
                    value="Learn more about this bird...",
                    onclick=f"window.location.href='{bp_path}'")
        return
# end RightPlacementPage


# helpers
def get_placement_species_list(language="EN"):
    '''Return a list of bird species that are used for the placement.
    '''
    pm_dir = INDEX_DICT[language]["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"]
    bird_sp_list = [
            fl.replace("tree_","").replace(".svg", "") for fl in 
            os.listdir(pm_dir) if fl.startswith("tree_")]
    return bird_sp_list


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


# here we include the core class that designs the 
# html page which informs about bird phylogeny

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class PhylogeneticsPage(AbstractPage):
    '''Builder class for the info page about phylogenetics.
    '''
    def make_title(self):
        '''Build a title for the HTML.
        '''
        # this can be edited.
        # so far we take a simple title.
        title = f"What is a phylogenetic tree?"
        return title
    

    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                f"phylogenetic_tree.html")
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
        with div(cls="row"):
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
        if self.lang == "EN" :
            page_title = f"Trees that reflect evolutionary history"
        else :
             page_title = f"Δέντρα που αντικατοπτρίζουν την εξελικτική ιστορία"
        # make subtitle of latin name in italics
        if self.lang == "EN" :
            page_subtitle = (
                "Let us tell you some things about phylogenetic trees.")
        else :
            page_subtitle = (
                "Ας σας πούμε μερικά πράγματα για τα φυλογενετικά δέντρα.")
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
        return

    def define_backlink(self):
        '''Make a small button that returns the user to the last page.
        '''
        with form():
            if self.lang == "EN" :
                input_(
                    type="button",
                    value="Go back to the start page.",
                    onclick="history.back()")
            else :
               input_(
                    type="button",
                    value="Επιστρέψτε στην αρχική σελίδα.",
                    onclick="history.back()") 
        return


    def plot_with_info(self, image_path):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
        from io import StringIO
        from rephrase_svg import TightSVG
        # we use this as image alternativ text
        license_info = "Phylogeny of birds with outgroup."
        # this is the image caption
        if self.lang == "EN" :
            license_link = "A tree full of birds."
        else :
            license_link = "Ένα δέντρο γεμάτο πουλιά."
        # it is a tree
        img_content = "tree"
        with div():
            attr_id = "image"
            attr(id=attr_id)
            tsvg = TightSVG(image_path)
            svg_io = StringIO(tsvg.rephrase())
            self.paste_svg_io(image_path, svg_io)
            figcaption(raw(license_link))
        return

    def column1(self):
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column"):
            tree_path = self.make_tree_img_path(non_relative=True)
            self.plot_with_info(tree_path)
        return


    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        with div(cls="column"):
            if self.lang == "EN" :
                p("A phylogenetic tree (also phylogeny or evolutionary tree) is a branching diagram "
                  "or a tree showing the evolutionary relationships among various biological species "
                  "or other entities based upon similarities and differences in their physical or "
                  "genetic characteristics. All life on Earth is part of a single phylogenetic tree, "
                  "indicating common ancestry.")
            else :
                p("Ένα φυλογενετικό δέντρο (επίσης φυλογένεση ή εξελικτικό δέντρο) είναι ένα διάγραμμα "
                  "διακλάδωσης ή ένα δέντρο που δείχνει τις εξελικτικές σχέσεις μεταξύ διαφόρων βιολογικών "
                  "ειδών ή άλλων οντοτήτων με βάση ομοιότητες και διαφορές στα φυσικά ή γενετικά "
                  "χαρακτηριστικά τους. Όλη η ζωή στη Γη είναι μέρος ενός μόνο φυλογενετικού δέντρου, "
                  "που υποδηλώνει κοινή καταγωγή.")
            
            self.define_backlink()

        return
# end TitlePage


###############
def main():
    for lang in ["EN", "GR"]:
        pp = PhylogeneticsPage(language=lang)
        pp.build_html()
        pp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


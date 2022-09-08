# here we include the core class that designs the 
# html page which informs about bird phylogeny

import dominate as dm
from dominate.tags import *
import os
import pandas as pd
import yaml

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class PhylogeneticsPage(AbstractPage):
    '''Builder class for the info page about phylogenetics.
    '''
    def make_title(self):
        '''Build a title for the HTML.
        '''
        file_texts = os.path.join(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_TEXTS"], "phylogenetic_tree.yml")
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
        page_title = self.texts["header"]["FILL_IN"]
        page_subtitle = self.texts["subheader"]["FILL_IN"]
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
        return

    def define_backlink(self):
        '''Make a small button that returns the user to the last page.
        '''
        with form():
            input_(
                type="button",
                value=self.texts["button"]["FILL_IN"],
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
            p(self.texts["maintext"]["FILL_IN"]) 
            self.define_backlink()

        return
# end TitlePage


###############
def main():
    for lang in [ln for ln in INDEX_DICT.keys() if len(ln)==2]:
        pp = PhylogeneticsPage(language=lang)
        pp.build_html()
        pp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


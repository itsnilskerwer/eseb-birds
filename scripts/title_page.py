# here we include the core class that designs the 
# title html page which shows the bird phylogeny

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class TitlePage(AbstractPage):
    '''Builder class for the title page.
    '''
    def make_title(self):
        '''Build a title for the HTML.
        '''
        # this can be edited.
        # so far we take a simple title.
        title = f"Diversity of birds worldwide."
        return title
    

    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                f"title.html")
        return os.path.abspath(file_name)


    def make_tree_img_path(self):
        '''Build name of path for the tree image.
        '''
        file_name = os.path.join(
                INDEX_DICT["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"],
                f"tree.svg")
        # return os.path.abspath(file_name)
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))

    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        with self.doc:
            self.define_header()
            with div(cls="row"):
                self.column1()
                self.column2()
        return

    def define_stylesheet(self):
        '''Define the style sheet for the html head.
        '''
        # define path
        css_rawpath = os.path.join(
                INDEX_DICT["PATHS_FROM_SCRIPTS"]["CSS_DIR"],
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
        page_title = f"Phylogeny of birdso of the world"
        # make subtitle of latin name in italics
        page_subtitle = (
                "Our research team found out, how the birds ",
                "of the world relate to each other.")
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
        return

    def plot_with_info(self, image_path):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
        # we use this as image alternativ text
        license_info = "Phylogeny of birds with outgroup."
        # this is the image caption
        license_link = "A tree full of birds."
        # it is a tree
        img_content = "tree"
        with div():
            attr_id = "image"
            attr(id=attr_id)
            with figure():
                attr(id=img_content)
                img(src=image_path,
                        alt=license_info)
                figcaption(raw(license_link))
        return

    def column1(self):
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column"):
            tree_path = self.make_tree_img_path()
            self.plot_with_info(tree_path)
        return


    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        with div(cls="column"):
            p("Do you see, which birds are closely realted to each other? "
                    "That is pretty fascinating, right? "
                    "Click on the images to find out more about the "
                    "bird on the image.")
        return
# end TitlePage


###############
def main():
    tp = TitlePage()
    tp.build_html()
    tp.save_html(force=True)
    return

if __name__ == "__main__":
    main()

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
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                f"title.html")
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
            # make a large title with name as species
            page_title = f"Aerial Collisions"
            page_subtitle = (
                "A research team found out, how birds ",
                "around the world are related to each other.")
        else :
            page_title = f"Εναέριες Συγκρούσεις"
            page_subtitle = (
                "Μια ερευνητική ομάδα ανακάλυψε πώς σχετίζονται ",
                "μεταξύ τους τα πουλιά σε όλο τον κόσμο.")
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
        return

    def plot_with_info(self, image_path):
        '''Add image to html document and annotate it with background info.
        '''
        from io import StringIO
        from dominate.util import raw
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
            # we rephrease the svg
            tsvg = TightSVG(image_path, language=self.lang)
            svg_io = StringIO(tsvg.rephrase())
            self.paste_svg_io(image_path, svg_io)
            figcaption(raw(license_link))
        return

    def link_phylogenetics_info(self):
        '''Link out to page that informs about phylogenetics.
        '''
        from phylogenetics_page import PhylogeneticsPage
        ip_abspath = PhylogeneticsPage(language=self.lang, stop_html_init=True).make_page_path()
        ip_path = os.path.relpath(ip_abspath, os.path.dirname(self.make_page_path()))
        with form():
            if self.lang == "EN" :
                input_(
                    type="button",
                    value="What is a phylogenetic tree?",
                    onclick=f"window.location.href='{ip_path}'")
            else :
                input_(
                    type="button",
                    value="Τι είναι ένα φυλογενετικό δέντρο;",
                    onclick=f"window.location.href='{ip_path}'")
                
        return

    def start_placement_game(self):
        '''Forward to the start page of the placement game.
        '''
        from start_placement_page import StartPlacementPage
        from dominate.util import raw

        if self.lang == "EN" :
            p("The molecular laboratory received a bird sample from a plane"
              " that should be identified. Can you help them?")
        else :
            p("Το μοριακό εργαστήριο έλαβε δείγμα πουλιού από αεροπλάνο"
              " που πρέπει να αναγνωριστεί. Μπορείτε να τους βοηθήσετε;")
         
        sp_abspath = StartPlacementPage(language=self.lang, stop_html_init=True).make_page_path()
        sp_path = os.path.relpath(sp_abspath, os.path.dirname(self.make_page_path()))
        with form():
            if self.lang == "EN" :
                input_(
                    type="button",
                    value="Become a real bird researcher",                                
                    onclick=f"window.location.href='{sp_path}'")
            else :
               input_(
                    type="button",
                    value="Γίνε ένας πραγματικός ερευνητής πουλιών",                                
                    onclick=f"window.location.href='{sp_path}'") 
                
        # sequence video
        if self.lang == "EN":
            p("Where do the DNA samples come from? Watch this short movie!")
            raw('<iframe width="560" height="315" src="https://www.youtube.com/embed/jXPf-nHdoxo?cc_load_policy=1&cc_lang_pref=en" '
                'title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; '
                'clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
        else:
            p("Από πού προέρχονται τα δείγματα DNA; Δες αυτή τη μικρή ταινία!")            
            raw('<iframe width="560" height="315" src="https://www.youtube.com/embed/jXPf-nHdoxo?cc_load_policy=1&cc_lang_pref=gr" '
                'title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; '
                'clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>')
        return


    def column1(self):
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column"):
            # tree_path = self.make_tree_img_path(non_relative=False)
            tree_path = self.make_tree_img_path(non_relative=True)
            self.plot_with_info(tree_path)
        return


    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        with div(cls="column"):
            if self.lang == "EN" : 
                p("Do you see, which birds are closely realted to each other? "
                  "That is fascinating, right? "
                  "Click on the images to find out more about the "
                  "bird on the image.")
            else:
                p("Βλέπεις ποια πουλιά είναι συγγενικά μεταξύ τους; "
                  "Αυτό είναι συναρπαστικό, σωστά; "
                  "Κάνε κλικ στις εικόνες για να μάθεις περισσότερα "
                  "για το πουλί στην εικόνα.")
            self.link_phylogenetics_info()
            self.start_placement_game()
        return
# end TitlePage


###############
def main():
    for lang in ["EN", "GR"]:
        tp = TitlePage(language=lang)
        tp.build_html()
        tp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


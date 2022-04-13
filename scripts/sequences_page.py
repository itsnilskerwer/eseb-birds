# here we include the core class that designs the 
# html page which informs about dna sequences

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class SequencesPage(AbstractPage):
    '''Builder class for the info page about dna and sequences.
    '''
    def __init__(self, language="EN", stop_html_init=False):
        '''Initialize with use of an example bird.
        '''
        super().__init__(language=language, stop_html_init=stop_html_init)
        EXAMPLE_BIRD = "PELCR"
        self.name = EXAMPLE_BIRD
        return

    def make_title(self):
        '''Build a title for the HTML.
        '''
        # this can be edited.
        # so far we take a simple title.
        title = f"What are such DNA sequences?"
        return title
    

    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                f"sequences_info.html")
        return os.path.abspath(file_name)


    def load_long_sequence(self):
        '''Obtain the long nucleotide sequence of a given bird species.
        '''
        EXAMPLE_BIRD = "PELCR"
        seq_file = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["SEQUENCES"],
                f"{EXAMPLE_BIRD}.html")
        body = []
        body_bool = False
        with open(seq_file, "r") as html:
            for line in html.readlines():
                if line.startswith("</body>") : return "".join(body)
                if body_bool : body.append(line)
                elif line.startswith("<body>") : body_bool = True
        raise RuntimeError("Html file is not proper in its structure.")


    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        self.define_header()
        with div(cls="row"):
            self.column1()
            self.column2()
        return

    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title with name as species
        if self.lang == "EN" :
            page_title = f"What are DNA sequences?"
        else :
            page_title = f"Τι είναι οι αλληλουχίες DNA;"
        # make subtitle of latin name in italics
        
        with div():
            attr(id="header")
            h1(page_title)        
        return

    def define_backlink(self):
        '''Make a small button that returns the user to the last page.
        '''
        with form():
            if self.lang == "EN" :
                input_(
                    type="button",
                    value="Okay, now I know what DNA is, let's go back. ",
                    onclick="history.back()")
            else :
               input_(
                    type="button",
                    value="Εντάξει, τώρα ξέρω τι είναι το DNA, ας πάμε πίσω.",
                    onclick="history.back()") 
        return


    def plot_with_info(self, image_path):
        '''Add image to html document and annotate it with background info.
        '''
        from dominate.util import raw
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
            if self.lang == "EN" :
                p("After sequencing we can imagine the DNA like"
                  " a word comprising the letters A, C, G, and T. Here is an example "
                  "of a part of the DNA of the brown pelican.")
            else:
                p("Μετά την αλληλουχίση μπορούμε να φανταστούμε το DNA σαν"
                  "μια λέξη που περιλαμβάνει τα γράμματα A, C, G και T. Παρακάτω είναι ένα παράδειγμα"
                   "ενός μέρους του DNA του καφέ πελεκάνου.")
            try:
                with details():
                    if self.lang == "EN" :
                        summary("Show DNA sequence of brown pelican")
                    else :
                        summary("Εμφάνιση αλληλουχίας DNA του καφέ πελεκάνου")
                    self.show_seq()
            except ValueError : pass
            
            self.define_backlink()
        return


    def column2(self):
        '''Make the second column, which includes the images of birds to place.
        '''
        return

# end TitlePage


###############
def main():
    for lang in ["EN", "GR"]:
        sp = SequencesPage(language=lang)
        sp.build_html()
        sp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


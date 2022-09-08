# here we include the core class that designs the 
# html page for the error

import dominate as dm
from dominate.tags import *
import os
import pandas as pd
import yaml

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class ErrorPage(AbstractPage):
    '''Builder class for an error page.
    '''
    # helpers
    def make_title(self):
        '''Build a title for the HTML.
        '''
        file_texts = os.path.join(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_TEXTS"], "error_page.yml")
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
                "error_page.html")
        return os.path.abspath(file_name)


    # HTML functions
    def html_body(self):
        '''Build the body of the html document.
        '''
        self.define_header()
        self.define_backlink()
        return

    def define_header(self):
        '''Put together the name information about the bird species as header.
        '''
        # make a large title that encourages children
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
# end ErrorPage

###############
def main():
    for lang in [ln for ln in INDEX_DICT.keys() if len(ln)==2]:
        ep = ErrorPage(language=lang)
        ep.build_html()
        ep.save_html(force=True)
    return

if __name__ == "__main__":
    main()


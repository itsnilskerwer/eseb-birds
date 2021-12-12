# here we include the core class that designs the 
# html page for the error

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from abstract_page import AbstractPage
from __init__ import INDEX_DICT

class ErrorPage(AbstractPage):
    '''Builder class for an error page.
    '''
    # helpers
    def make_title(self):
        '''Build a title for the HTML.
        '''
        # this can be edited.
        # so far, we simply take the latin name.
        title = "try again ;-)"
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
        page_title = "Try again ;-)"
        # make subtitle to swear in greek
        page_subtitle = "σκατά, it was the wrong bird."
        
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
                    value="You can do it next time!",
                    onclick="history.back()")
        return
# end ErrorPage

###############
def main():
    for lang in ["EN", "GR"]:
        ep = ErrorPage(language=lang)
        ep.build_html()
        ep.save_html(force=True)
    return

if __name__ == "__main__":
    main()


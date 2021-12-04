# here we include the core class that designs the 
# html page for the error

import dominate as dm
from dominate.tags import *
import os
import pandas as pd

from __init__ import INDEX_DICT

class ErrorPage:
    '''Builder class for an error page.
    '''
    def __init__(self):
        '''Initiaize error page.
        '''
        # initiate html page
        self.initiate_html()
        return
    
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
                INDEX_DICT["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                "error_page.html")
        return os.path.abspath(file_name)


    # HTML functions
    def initiate_html(self):
        '''Initiate the dominate document.
        '''
        self.doc = dm.document(title=self.make_title())
        return

    def build_html(self):
        '''Build html document with head and body.
        '''
        self.html_head()
        self.html_body()
        return


    def html_head(self):
        '''Build the head of the html document.
        '''
        with self.doc.head:
            self.define_meta()
            self.define_stylesheet()
            self.define_jscript()
        return
    

    def html_body(self):
        '''Build the body of the html document.
        '''
        with self.doc:
            self.define_header()
            self.define_backlink()
        return


    def define_meta(self):
        '''Define meta information of html document for head.
        '''
        # we use english and UTF-8
        meta(charset="UTF-8")
        meta(lang="en")
        return


    def define_stylesheet(self):
        '''Define the style sheet for the html head.
        '''
        # this can be extended. we do not use it yet.
        # link(rel='stylesheet', href='style.css')
        return


    def define_jscript(self):
        '''Define the style js script for the html head.
        '''
        # this can be extended. we do not use it yet.
        # script(type='text/javascript', src='script.js')
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

    def save_html(self, force=False):
        '''Save html document as a file.
        '''
        file_name = self.make_page_path()
        if not os.path.exists(file_name) or force:
            with open(file_name, "w") as html_file:
                html_file.write(str(self.doc))
        else:
            print(f"Html document {self.name}.html already exists.")
        return
# end BirdPage

###############
def main():
    ep = ErrorPage()
    ep.build_html()
    ep.save_html(force=True)
    return

if __name__ == "__main__":
    main()


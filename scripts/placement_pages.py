# here we include the core class that designs the 
# html pages for the phylogenetic placement of a
# bird species

import dominate as dm
from dominate.tags import *
import os
import pandas as pd
import yaml

from abstract_page import AbstractPage
from abstract_page import get_placement_species_list
from __init__ import INDEX_DICT

class PlacementPage(AbstractPage):
    '''Builder class for placement page of a given bird species.
    '''
    def __init__(self, bird_name, language="EN", stop_html_init=False):
        '''Initiaize object with a given name.
        '''
        self.name = bird_name
        super().__init__(language=language, stop_html_init=stop_html_init)
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
        file_texts = os.path.join(INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_TEXTS"], "placement.yml")
        self.texts = yaml.safe_load(open(file_texts, "r"))

        # this can be edited.
        # so far we take a simple title.
        title = self.texts["urltitle"]["FILL_IN"]
        
        if not hasattr(self, "data"):
            self.get_data()
        return title
    

    def make_page_path(self):
        '''Build name of path for html page.
        '''
        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["PLACEMENT_HTML_DIR"],
                f"{self.name}_placement.html")
        return os.path.abspath(file_name)

    def make_img_path(self, bird_name):
        '''Build name of path for a bird image.
        '''
        assert self.check_name(bird_name), f"{bird_name} is not in list."

        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_PAGE_IMG_DIR"],
                f"{bird_name}.png")
        # return os.path.abspath(file_name)
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))


    def make_tree_img_path(self, bird_name, non_relative=False):
        '''Build name of path for a bird image.
        '''
        assert self.check_name(bird_name), f"{bird_name} is not in list."

        file_name = os.path.join(
                INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["BIRD_PLACEMENT_IMG_DIR"],
                f"tree_{bird_name}_question.svg")
        if non_relative : return os.path.abspath(file_name)
        return os.path.relpath(file_name, os.path.dirname(self.make_page_path()))

    def make_img_link(self, bird_name):
        '''Build a link to error or success page.
        '''
        if self.name == bird_name: 
            file_link = os.path.join(
                    INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["PLACEMENT_HTML_DIR"],
                    f"{self.name}_success.html")
        else:
            file_link = os.path.join(
                    INDEX_DICT[self.lang]["PATHS_FROM_SCRIPTS"]["START_AND_ERROR_HTML_DIR"],
                    "error_page.html")
        return os.path.relpath(file_link, os.path.dirname(self.make_page_path()))

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
        from dominate.util import raw

        # make a large title with name as species
        page_title = self.texts["header"]["FILL_IN"]
        # make subtitle of latin name in italics
        page_subtitle = self.texts["subheader"]["FILL_IN"]
        
        with div():
            attr(id="header")
            h1(page_title)
            h2(em(page_subtitle))
            
            # adding the sequence
            sequence = self.get_sequence(bird_name=self.name)
            sequence = sequence.replace('<dd><span',
                    '<dd>~~~<span')
            sequence = sequence.replace('</span></dd>',
                    '</span>~~~</dd>')
            h2(raw(f"{sequence}<br>")) 
            p("The computer program has provided us with a phylogenetic tree. Check out where this sequence is predicted to be placed. It is indicated by a '?'.")
            p("Select one of the birds from the candidate list, if you think it matches the placement in the tree. HINT: Look for bird facts that are similar to the closest relatives of the predicted sequence placement.")
        return

    def plot_with_info(self, image_path, bird_name=None, tree=False, count=None):
        '''Add image to html document and annotate it with background info.
        '''
        from io import StringIO
        from rephrase_svg import TightSVG
        from dominate.util import raw
        if not tree: 
            data = self.BIRD_DATA[self.BIRD_DATA["CODE"]==bird_name].squeeze()
            # get license information
            license_info = data["license notice for plain text "]
            # get license link
            license_link = data["license notice HTML (https://lizenzhinweisgenerator.de/)"]
            # content of image is habitus
            img_content = "habitus"
        else:
            # we use this as image alternativ text            
            license_info = "Phylogenetic tree for placement."
            # this is the image caption
            license_link = self.texts["imgtext"]["FILL_IN"]
            # it is a tree
            img_content = "tree"
        with div():
            # sometimes we have multiple images
            if count is not None : attr_id = f"image{count}"
            else : attr_id = "image"
            attr(id=attr_id)
            if tree:
                tsvg = TightSVG(image_path, language=self.lang)
                svg_io = StringIO(tsvg.rephrase())
                self.paste_svg_io(image_path, svg_io)
            else:
                with figure():
                    attr(id=img_content)
                    img(src=image_path,
                            style="max-width: 30%;",
                            alt=license_info)
                    if isinstance(license_link, str):
                        figcaption(raw(license_link))
                    else:  # for missing data
                        figcaption("Missing.")
        return

    def column1(self):
        '''Make the first column, which includes the tree image.
        '''
        with div(cls="column tree"):
            script(type="text/javascript", src="../../../javascript/tree-viewer.js") 
            script(type="text/javascript", src="../../../javascript/card-viewer.js")
            tree_path = self.make_tree_img_path(self.name, non_relative=True)
            self.plot_with_info(tree_path, tree=True)
        return


    def column2(self):
        '''Make the second column, which includes the images of birds to place.
            Added some more data for bird selection list (static, and single game)
            This should be reverted to make multiple games possible again
        '''
        with div(cls="column bird-cards selection"):
            # p(self.texts["maintext"]["FILL_IN"])
            with section(id="bird-cards"): 
                bird_names = get_placement_species_list(language=self.lang)
                bird_info_list = [
                    {
                                   "data_bird": "ex name bird 1",
                                   "common_name": "Adelie penguin",
                                   "scientific_name": "Pygoscelis adeliae",
                                   "distribution": "Coasts of Antarctica",
                                   "wingspan": "35 - 70 cm",
                                   "weight": "3.8 - 8.2 kg",
                                   "diet": "Krill, small fish"
                    },
                    {
                                   "data_bird": "ex name bird 2",
                                   "common_name": "Barn owl",
                                   "scientific_name": "Tyto alba",
                                   "distribution": "South-central Europe, non-desert Africa",
                                   "wingspan": "80-95 cm",
                                   "weight": "300-500 g",
                                   "diet": "Mice, rats, small birds and amphibia"
                    },
                    {
                                   "data_bird": "ex name bird 3",
                                   "common_name": "Great-crested grebe",
                                   "scientific_name": "Posiceps cristatus",
                                   "distribution": "Pallearctic freshwater lakes",
                                   "wingspan": "59-73 cm",
                                   "weight": "800 - 1400 g",
                                   "diet": "Small fish"
                    },
                    {
                                   "data_bird": "ex name bird 4",
                                   "common_name": "Red-crested turaco",
                                   "scientific_name": "Tauraco erythrolophus",
                                   "distribution": "Western Angola",
                                   "wingspan": "approx. 20 cm",
                                   "weight": "210-335 g",
                                   "diet": "Fruits, roots, shoots, nuts, seeds"
                    },
                    {
                                   "data_bird": "ex name bird 5",
                                   "common_name": "White-throated tinamou",
                                   "scientific_name": "Tinamus guttus",
                                   "distribution": "Lowland Amazon forest",
                                   "wingspan": "approx. 23-26 cm",
                                   "weight": "620-800 g",
                                   "diet": "Fruits, seeds, invertebrates"
                    },
                    {
                                   "data_bird": "ex name bird 6",
                                   "common_name": "Yellow-throated sandgrouse",
                                   "scientific_name": "Pterocles gutturalis",
                                   "distribution": "Semi-deserts of South Africa",
                                   "wingspan": "53 - 65 cm",
                                   "weight": "285-400 g",
                                   "diet": "Seeds and grains"
                    },
                    {
                                   "data_bird": "ex bird name 7",
                                   "common_name": "Common ostrich",
                                   "scientific_name": "Struthio camelus",
                                   "distribution": "West and North Africa",
                                   "wingspan": "2m (but cannot fly)",
                                   "weight": "90-154 kg",
                                   "diet": "Plants, invertebrates, small reptiles"
                    },
                    {
                                   "data_bird": "ex name bird 8",
                                   "common_name": "Zebra finch",
                                   "scientific_name": "Taeniopygia guttata",
                                   "distribution": "Australia and Indonesia",
                                   "wingspan": "approx. 22 cm",
                                   "weight": "9-16 g",
                                   "diet": "Seeds"
                   }
                ]
                # bird_names = get_placement_species_list(language=self.lang)
                for i, bird_name in enumerate(bird_names):
                    img_path = self.make_img_path(bird_name)
                    img_link = self.make_img_link(bird_name)
                    # bird_info = self.get_bird_info(i)
                    bird_info = bird_info_list[i]  # Access the correct dictionary using index `i`
                    with div(cls="card", **{"data-bird": bird_name}):
                        with a(href=img_link):
                            img(src=img_path, alt=bird_info["common_name"])
                        with div(cls="bird-info"):
                            h2(bird_info["common_name"])
                            em(bird_info["scientific_name"])
                            p(f"Distribution: {bird_info['distribution']}")
                            p(f"Wingspan: {bird_info['wingspan']}")
                            p(f"Weight: {bird_info['weight']}")
                            p(f"Diet: {bird_info['diet']}")
                    #  with a(href=img_link):
                    #     self.plot_with_info(img_path, bird_name=bird_name, count=i+1)
                """ for bird in bird_info:
                    for i, bird_name in enumerate(get_placement_species_list(language=self.lang)):
                        img_path = self.make_img_path(bird["bird_name"])
                        img_link = self.make_img_link(bird["bird_name"])
                        with div(cls="card", **{"data-bird": bird["bird_name"]}):
                            with a(href=img_link):
                                img(src=img_path, alt=bird["common_name"])
                            with div(cls="bird-info"):
                                h2(bird["common_name"])
                                em(bird["scientific_name"])
                                p(f"Distribution: {bird['distribution']}")
                                p(f"Wingspan: {bird['wingspan']}")
                                p(f"Weight: {bird['weight']}")
                                p(f"Diet: {bird['diet']}")
                                p(f"DNA fragment: {bird['dna_fragment']}") """
        return
# end PlacementPage

# helper

###############
def main():
    for lang in [ln for ln in INDEX_DICT.keys() if len(ln)==2]:
        bird_names = get_placement_species_list(language=lang)
        for bird_name in bird_names:
            pp = PlacementPage(bird_name, language=lang)
            pp.build_html()
            pp.save_html(force=True)
    return

if __name__ == "__main__":
    main()


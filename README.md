# Bird Phylogeney Visualization from Phylogenetic Placements



##### Step 1: Installing dependencies using a virtual environment

create venv with Python version 3.11

```python3.11 -m venv venv```

activate virtual environment

```source venv/bin/activate```

install dependencies

```pip install pandas regex PyYAML dominate numpy```

install inkscape (installed as program on my machine)

##### Step 2: Make sure all files are included

Added images_std/ and thumbs/ folders to acanthis/ directory. Created data/ directory and added background image (bg.jpg).

##### Step 3: Run scripts to build pages

in scripts dir, run build_pages.sh. This generates the html files.

##### Step 4: Prepare for deployment and start local development

run zip_page.sh script to save files in deployment directory

```./zip_page.sh deployment```

start http server in deployment/ directory

```python3 -m http.server 8000```




##### optional:
run test-images.sh

-> This returns an error: cat: ../data/names.txt: No such file or directory
Since i can see names.txt file in acanthis folder, the path is updated to point to acanthis directory.

##### optional:
run convert.sh

-> at this point convert.sh does not find svg files. No fix for this yet.


Minor fixes to remove warnings:

images_std directory doesnt seem to be created correctly. Pasting the example images into this directory makes the single page bird images visible (still with example bird).

../meta/two_columns.css
-> commented out line 2 "  background-image: url("../data/bg.jpg");"

(minor change: meta viewport tag added in title.html files)
(minor change: add image attribute in image tags)
(minor error: "GET /favicon.ico HTTP/1.1" 404 )
syntax warning for abstract_page.py line 181 
(minor error: SyntaxWarning: invalid escape sequence '\='
(minor error: rephrase_svg.py line 218, 225, 226 -> error: again invalid escape sequences

moved files generated into data directory into acanthis (build error with filepaths)

duplicated and renamed images to acanthis/images_std as hacky fix.

Try to re-run the build scripts and re-start server.

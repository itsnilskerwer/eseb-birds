from napari_utils import rescale_to_square
from __init__ import INDEX_DICT
from skimage import io
import os

def main():
    img_dir = INDEX_DICT["EN"]["PATHS_FROM_SCRIPTS"]["BIRD_PAGE_IMG_DIR"]
    thumbs_dir = INDEX_DICT["EN"]["PATHS_FROM_SCRIPTS"]["BIRD_TREE_IMG_DIR"]

    all_images = [img for img in os.listdir(img_dir) if 
            img.endswith(".png") and not img.endswith("_raw.png")]
    for image_name in all_images:
        in_path = os.path.join(img_dir, image_name)
        out_path = os.path.join(thumbs_dir, image_name)
        print(in_path)
        image = io.imread(in_path)
        resc_image = rescale_to_square(image, square_pixel_size=100)
        io.imsave(out_path, resc_image)
        print(out_path, " DONE")

if __name__ == "__main__":
    main()

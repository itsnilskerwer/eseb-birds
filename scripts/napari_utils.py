# this file contains classes and methods that support the napari
# cropping

import csv
import napari
import numpy as np
import os
from skimage import io


class NapariIMG:
    def __init__(self, image_name, viewer, output_dir=None):
        '''Initialize from bird image name and a given napari viewer.
        '''
        # make alias for bird name and store file and output paths
        self.alias = make_alias(image_name)
        self.file = image_name
        self.outdir = output_dir
        
        # store the viewer
        self.viewer = viewer
        
        # the image is loaded
        img_handle = io.imread(image_name)
        self.image = self.viewer.add_image(img_handle,
                                           name=image_name.split("/")[-1].split(".")[0])
        
        # we check how it is oriented because then we only crop along the longer axis
        img_dims = self.image.data.shape
        self.max_square_length = min(img_dims[0], img_dims[1])
        if img_dims[0] == img_dims[1] : self.orientation = "square"
        elif img_dims[0] < img_dims[1] : self.orientation = "horizontal"
        else : self.orientation = "vertical"
        
        return
        
    def add_square(self):
        '''Add a square of maximal possible size for cropping.
        '''
        self.square = self.viewer.add_shapes(
            [[0, 0], [self.max_square_length, self.max_square_length]],
            shape_type='rectangle',
            opacity=.3,
            edge_width=1,
            name='crop_zone')
        return
    
    def optimize_square(self):
        '''Optimize the cropping square after manual adjustment.
        '''
        assert hasattr(self, "square"), "You do not have any cropping square!"
        optimal_bounds = get_optimal_croposition(self.square.data[0],
                                                 self.image.data.shape,
                                                 orientation=self.orientation)
        self.crop_dict = {
                "top_left": coordinatearray_to_dict(optimal_bounds[0]),
                "top_right": coordinatearray_to_dict(optimal_bounds[1]),
                "bottom_right": coordinatearray_to_dict(optimal_bounds[2]),
                "bottom_left": coordinatearray_to_dict(optimal_bounds[3]),
                "source_file": self.file
            }
        if self.outdir is not None:
            if not hasattr(self, "outfile") : self.make_outfile_name()
            self.crop_dict["cropped_file"] = self.outfile
        return optimal_bounds
    
    def make_outfile_name(self, output_dir=None):
        '''Build name of output file.
        '''
        if output_dir is not None : outdir = output_dir
        else : outdir = self.outdir
        assert outdir is not None, "Provide an output path!"
        
        self.outfile = os.path.join(outdir, f"{self.alias}.png")
        return
    
    def plot_optimal_square(self):
        '''Show the optimal cropping square in the napari viewer.
        '''
        bounds = self.optimize_square()
        self.opti_square = self.viewer.add_shapes(
            bounds,
            shape_type='rectangle',
            opacity=.3,
            edge_width=1,
            name='optimal_crop_zone',
            face_color="red")
        return
    
    def crop_square(self):
        '''Crop the raw image down to the square.
        '''
        assert hasattr(self, "opti_square"), "Optimized cropping square was not loaded before."
        cropper = ImageCropper(self.file)
        self.cropped_image = cropper.crop(
            self.crop_dict["top_left"]["x"], self.crop_dict["bottom_right"]["x"],
            self.crop_dict["top_left"]["y"], self.crop_dict["bottom_right"]["y"])
        return

    def save_cropped(self, output_dir=None, rescaling_function=None, force=False,
                    cropping_csv_file_name=None):
        '''Save the cropped version of a given image.
        '''
        assert hasattr(self, "opti_square"), "Optimized cropping square was not loaded before."
        
        if output_dir is None : output_dir = self.outdir
        assert output_dir is not None, "No output directory given."
        
        self.make_outfile_name(output_dir=output_dir)
        
        cropper = ImageCropper(self.file)
        cropper.crop_resize_save(
            self.crop_dict["top_left"]["x"], self.crop_dict["bottom_right"]["x"],
            self.crop_dict["top_left"]["y"], self.crop_dict["bottom_right"]["y"],
            self.outfile, 
            resize_function=rescaling_function, force=force)
        # also we track the cropping areas.
        if cropping_csv_file_name is not None:
            save_cropping_areas(
                {self.alias: self.crop_dict}, cropping_csv_file_name, append=True)
        return

# end NapariIMG

class ImageCropper:
    '''This class supports to crop an image, rescale it and save the processed data.
    '''
    def __init__(self, image_filename):
        '''Initialize from image file.
        '''
        assert os.path.exists(image_filename), f"Image {image_filename} does not exist."
        self.image = io.imread(image_filename)
        return
    
    
    def crop(self, x_min, x_max, y_min, y_max):
        '''Crop image applying a given rectangular frame.
        '''
        self.cropped_image = self.image[
            x_min : x_max, y_min : y_max]
        return self.cropped_image
    
    
    def save(self, output_filename, force=False):
        '''Save cropped image.
        '''
        from skimage import color
        if os.path.exists(output_filename) or force : return
        assert hasattr(self, "cropped_image")
        
        io.imsave(output_filename, self.cropped_image)
        return
    
    def resize(self, resize_function):
        '''Rescale the cropped image.
        '''
        assert hasattr(self, "cropped_image")
        
        self.cropped_image = resize_function(self.cropped_image)
        return
    
    def crop_resize_save(self, x_min, x_max, y_min, y_max,
                         output_filename, resize_function=None,
                         force=False):
        '''Crop, rescale image and save it cropped and cr.+rescaled.
        '''
        # first we crop the image
        self.crop(x_min, x_max, y_min, y_max)
        
        # we save the raw cropped version
        print(output_filename)
        if resize_function is not None:
            raw_file_name = "_raw".join(os.path.splitext(output_filename))
        else : raw_file_name = output_filename
        self.save(raw_file_name, force=force)
        
        if resize_function is None : return
        
        # we resize the image
        self.resize(resize_function)
        self.save(output_filename, force=force)
        return
# end ImageCropper

    
# helpers NapariIMG
def make_alias(bird_image_filepath):
    '''Make the 5 uppercase alias for a given source bird image.
    '''
    _, file_name = os.path.split(bird_image_filepath)
    bird_name, _ = os.path.splitext(file_name)
    split_name = bird_name.split(" ")
    if len(split_name) == 1 : split_name = bird_name.split("_")
    genus, species = split_name[:2]
    bird_alias = f"{genus[:3]}{species[:2]}".upper()
    return bird_alias

def coordinatearray_to_dict(coord_in_array):
    '''Simply convert image coordinates from array to x, y dictionary.
    '''
    return {"x": int(coord_in_array[0]), "y": int(coord_in_array[1])}

def get_optimal_croposition(cropping_rectangle, img_dimensions, orientation="square"):
    '''Find the optimal position of the square to crop given a rough placement by hand.
    '''
    # here we tackle the problem that one could not place the square aligning with bounds
    # of the image when doing high throughput.
    # we centralize teh square in this function
    if orientation == "vertical":
        # we just switch axes and do same trafo as for horizontal images
        flipped_rectangle = np.flip(cropping_rectangle, 1)
        flipped_dimensions = [img_dimensions[1], img_dimensions[0]]
        flipped_crop_square = get_optimal_croposition(
            flipped_rectangle, flipped_dimensions, orientation="horizontal")
        # the result is flipped back
        return np.flip(flipped_crop_square, 1)
    elif orientation in ["square", "horizontal"]:
        # maximal position that square could take on left
        max_left = min(np.floor(cropping_rectangle[0][1]), img_dimensions[1]-img_dimensions[0])
        # maximal position that square could take on right
        max_right = min(np.floor(cropping_rectangle[2][1]), img_dimensions[1])

        # build bounds of max possible cropping square
        crop_square = np.array([
            [0, max_left],
            [img_dimensions[0], max_left],
            [img_dimensions[0], max_right],
            [0, max_right]
        ])
        
        return crop_square
    raise ValueError(f"Orientation {orientation} not supported.")
    
    
# helpers ImageCropper
def rescale_to_square(image, square_pixel_size=550):
    '''Rescale an image to a square.
    '''
    from skimage.transform import resize
    rescaled_image = resize(
        image, 
        (square_pixel_size, square_pixel_size),
        anti_aliasing=False)
    return rescaled_image

# overall helpers
def save_cropping_areas(cropping_dict, file_name, force=False, append=False):
    '''Store the areas that were used for cropping of all images.
    '''
    example = cropping_dict[list(cropping_dict.keys())[0]]
    if append and os.path.exists(file_name) : option = "a"
    else : option ="w"
    if not os.path.exists(file_name) or force or append:
        with open(file_name, option) as csvfile:
            csv_writer = csv.DictWriter(
                csvfile, ["alias"] + list(example.keys()))
            if not append : csv_writer.writeheader()
            for nm, dct in cropping_dict.items():
                dct["alias"] = nm
                csv_writer.writerow(dct)
    return
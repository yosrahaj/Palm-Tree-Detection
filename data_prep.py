import os
import glob
import shutil
from tqdm.auto import tqdm
import xmltodict
import argparse

# Setting up the argument parser
parser = argparse.ArgumentParser(description='Prepare and convert data for YOLO model training.')
parser.add_argument('--source_folder', type=str, required=True, help='Folder containing images and XML annotations.')
parser.add_argument('--output_images', type=str, default='./PalmTreesImages', help='Output folder for images.')
parser.add_argument('--output_annotations', type=str, default='./PalmTreesAnnotations', help='Output folder for annotations.')
args = parser.parse_args()

def copy_and_prepare_files(source_folder, output_images, output_annotations):
    """ Copy image and annotation files to new directories and prepare them. """
    os.makedirs(output_images, exist_ok=True)
    os.makedirs(output_annotations, exist_ok=True)

    images_paths = glob.glob(os.path.join(source_folder, '*.jp*'))
    annotation_paths = glob.glob(os.path.join(source_folder, '*.xml'))

    for file_path in images_paths:
        shutil.copy(file_path, os.path.join(output_images, os.path.basename(file_path)))

    for file_path in annotation_paths:
        shutil.copy(file_path, os.path.join(output_annotations, os.path.basename(file_path)))

    return images_paths, annotation_paths

def parse_and_convert_annotations(annotation_paths, output_folder):
    """ Parse XML annotations and convert them to YOLO format. """
    for xml_file in tqdm(annotation_paths, desc='Converting XML Annotations'):
        with open(xml_file, 'r') as file:
            xml_dict = xmltodict.parse(file.read())

        # Assuming each file contains multiple objects
        objects = xml_dict['annotation']['object']
        if not isinstance(objects, list):
            objects = [objects]

        txt_filename = os.path.splitext(os.path.basename(xml_file))[0] + '.txt'
        txt_filepath = os.path.join(output_folder, txt_filename)
        with open(txt_filepath, 'w') as txt_file:
            for obj in objects:
                bndbox = obj['bndbox']
                x_center = (int(bndbox['xmin']) + int(bndbox['xmax'])) / 2
                y_center = (int(bndbox['ymin']) + int(bndbox['ymax'])) / 2
                width = int(bndbox['xmax']) - int(bndbox['xmin'])
                height = int(bndbox['ymax']) - int(bndbox['ymin'])
                # Assuming class_id is 0 for Palm, can be mapped according to actual classes
                txt_file.write(f"0 {x_center} {y_center} {width} {height}\n")

def main():
    images_paths, annotation_paths = copy_and_prepare_files(args.source_folder, args.output_images, args.output_annotations)
    parse_and_convert_annotations(annotation_paths, args.output_annotations)

if __name__ == "__main__":
    main()

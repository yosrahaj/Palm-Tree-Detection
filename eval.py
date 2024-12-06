import argparse
from ultralytics import YOLO

# Set up the argument parser
parser = argparse.ArgumentParser(description='Evaluate YOLO model.')
parser.add_argument('--model ', type=str, help='Path to the trained YOLO model.')
parser.add_argument('--data_config', type=str, help='Path to the data configuration YAML file.')
parser.add_argument('--img_size', type=int, default=1024, help='Image size for validation.')
args = parser.parse_args()

def evaluate_model():
    """ Evaluate the YOLO model. """
    model = YOLO(args.model)
    metrics = model.val(data=args.data_config, imgsz=args.img_size)
    print("Evaluation metrics:", metrics)

if __name__ == "__main__":
    evaluate_model()

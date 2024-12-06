import argparse
from ultralytics import YOLO

# Set up the argument parser
parser = argparse.ArgumentParser(description='Train YOLO model.')
parser.add_argument('--model', type=str, help='Path to the model configuration file.')
parser.add_argument('--data_config', type=str, help='Path to the data configuration YAML file.')
parser.add_argument('--epochs', type=int, default=100, help='Number of epochs to train.')
parser.add_argument('--batch_size', type=int, default=16, help='Batch size for training.')
parser.add_argument('--img_size', type=int, default=640, help='Input image size for training.')
parser.add_argument('--device', type=str, default='cpu', help='Device to run the training on.')
parser.add_argument('--workers', type=int, default=4, help='Number of worker threads for data loading.')
parser.add_argument('--optimizer', type=str, default='SGD', help='Optimizer to use for training.')
parser.add_argument('--lr0', type=float, default=0.01, help='Initial learning rate.')
args = parser.parse_args()

def train_model():
    """ Train a YOLO model based on provided arguments. """
    model = YOLO(args.model)
    train_results = model.train(
        data=args.data_config,
        epochs=args.epochs,
        batch_size=args.batch_size,
        imgsz=args.img_size,
        device=args.device,
        workers=args.workers,
        optimizer=args.optimizer,
        lr0=args.lr0
    )
    print('Training Results:', train_results)
    # Evaluate model performance on the validation set
    metrics = model.val()
    print("Evaluation metrics:", metrics)
    # Export the model to ONNX format
    model.export(format="onnx")

if __name__ == "__main__":
    train_model()

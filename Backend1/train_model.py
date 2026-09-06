import argparse
from pathlib import Path

from app.core.config import settings
from app.ml.training.model_trainer import train_model


def train(dataset_path: Path, output_path: Path) -> dict:
    return train_model(dataset_path, output_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train SENTINAL's explainable network attack classifier")
    parser.add_argument("dataset_positional", nargs="?", type=Path)
    parser.add_argument("--dataset", dest="dataset_option", type=Path)
    parser.add_argument("--output", type=Path, default=Path(settings.ml_model_path))
    arguments = parser.parse_args()
    dataset = arguments.dataset_option or arguments.dataset_positional
    if dataset is None:
        parser.error("provide a dataset path or --dataset path")
    print(train(dataset, arguments.output))

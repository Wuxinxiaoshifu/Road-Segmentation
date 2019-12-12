import torch
import numpy as np
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
from pathlib import Path
from PIL import Image
from transformations import *

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
# expected size from the models, could be 256 let's see



class RoadsDatasetTrain(Dataset):
    """Road segmentation datset"""

    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.img_dir = self.root_dir / "images"
        self.gt_dir = self.root_dir / "groundtruth"
        self.img_names = [x.name for x in self.img_dir.glob("**/*.png") if x.is_file()]

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = self.img_names[idx]
        image = numpy.array(Image.open(self.img_dir / img_name))
        groundtruth = numpy.array(Image.open(self.gt_dir / img_name))
        sample = {"image": image, "groundtruth": groundtruth}


        return sample


class RoadsDatasetTest(Dataset):
    """Road segmentation dataset for test time"""

    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.img_names = [str(x) for x in self.root_dir.glob("**/*.png") if x.is_file()]

    def __len__(self):
        return len(self.img_names)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()

        img_name = self.img_names[idx]
        image = Image.open(img_name)
        sample = {"image": image}

        if self.transform:
            sample = self.transform(image)
        else:
            transformation = transforms.Compose(
                [
                    transforms.ToTensor(),
                ]
            )
            sample = transformation(sample)

        return sample

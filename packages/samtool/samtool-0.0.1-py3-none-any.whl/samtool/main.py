from segment_anything import SamPredictor, sam_model_registry, SamAutomaticMaskGenerator
from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt
import torch
try:
    from utils import (
        show_mask,
        show_points,
        show_box,
    )
except ImportError:
    from .utils import (
        show_mask,
        show_points,
        show_box,
    )


class Sam:
    """
    SamPredictor class.
    """

    def __init__(self, sam_file: Path, device: str = 'cpu'):
        if not sam_file.is_file():
            raise FileNotFoundError
        self.device = torch.device(device)
        self.sam = sam_model_registry['vit_h'](checkpoint=sam_file.as_posix()).to(self.device)
        self.predictor = SamPredictor(self.sam)
        self.mask_generator = SamAutomaticMaskGenerator(self.sam)

    @staticmethod
    def show_masks(masks: list, image: np.ndarray, boxes: bool = False, points: bool = False):
        """
        This will show us a matplotlib representation of the masked output.
        """
        input_label = np.array([1, 1])
        plt.figure(figsize=(10, 10))
        plt.imshow(image)
        for mask in masks:
            segmentation = mask['segmentation']
            show_mask(segmentation, plt.gca(), random_color=True)  # May need to cast to device here.
            if boxes:
                box = mask['bbox']
                show_box(box, plt.gca())
            if points:
                point = mask['point_coords']
                show_points(point, input_label, plt.gca())
        plt.axis('off')
        plt.show()

    @staticmethod
    def read_image(image_path: Path):
        """
        Simpley reads an image from file and returns it as a numpy array.
        """
        image = cv2.imread(image_path.as_posix())
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return image

    def predict(
            self, image: np.ndarray, prompt: list[np.ndarray, np.ndarray, bool] = None, show: bool = False
    ) -> tuple[list, list, list]:
        """
        Create masks with or without a prompt.

        Prompt is a nparray of a specific location to identify instead of the whole image.

        multimask_output=True (the default setting), SAM outputs 3 masks, where scores gives the model's own estimation
        of the quality of these masks.
        [
            input_point = np.array([[500, 375]])
            input_label = np.array([1])
            multimask_output=True
        ]

        If no prompt is provided, the whole image is segmented. This output will return masks only, scores and logits
        will be empty np.ndarray objects
        """
        scores = logits = list()
        if prompt is None:
            masks = self.mask_generator.generate(image)
        else:
            self.predictor.set_image(image)
            masks, scores, logits = self.predictor.predict(*prompt)
        if show:
            self.show_masks(masks, image)
        return masks, scores, logits

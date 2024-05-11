
---

# SamTool

SamTool is a Python library designed for easy integration of the SAM (Segment Anything with Masking) model into computer vision projects. SAM is a state-of-the-art model for segmenting objects in images with high accuracy.

![](https://github.com/facebookresearch/segment-anything/blob/main/assets/model_diagram.png?raw=true)
![](https://github.com/facebookresearch/segment-anything/blob/main/assets/masks2.jpg?raw=true)

## Installation

You can install SamTool via pip:

```bash
pip install samtool
```

## Usage

### Initializing SamTool

```python
from samtool import Sam

# Initialize SamTool with the path to the SAM model file
sam = Sam(sam_file='path/to/sam_model.pth')
```

### Predicting Masks

```python
# Read an image
image = Sam.read_image('path/to/image.jpg')

# Generate masks for the entire image
masks, scores, logits = sam.predict(image)

# Display masks overlaid on the input image
sam.show_masks(masks, image, boxes=True, points=True)
```

### Using Prompt for Segmentation

```python
# Define a prompt (specific location to identify instead of the whole image)
prompt = [input_point, input_label, multimask_output]

# Generate masks based on the prompt
masks, scores, logits = sam.predict(image, prompt=prompt)
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Facebook Segment Anything: [github](https://github.com/facebookresearch/segment-anything)

---

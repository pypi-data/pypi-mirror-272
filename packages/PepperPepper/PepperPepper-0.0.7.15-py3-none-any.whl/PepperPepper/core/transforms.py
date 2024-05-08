from ..environment import torch, random, np

'''
1.Random_Expand
    summary: the Random_Expand class intend to implement the random padding method for image
    If the image is torch Tensor, it is expected to have [..., H, W] shape.

    Args:
        max_ratio: Maximum ratio for random expansion. Default is 4.
        fill: Fill color for the expanded area. Default is None.
        keep_ratio: Wether to maintain aspect ratio during expansion. Default is True.
        thresh: Threshold for applying the random expansion. Default is 0.5.

'''
class Random_Expand(torch.nn.Module):
    def __init__(self, max_ratio, fill, keep_ratio, thresh):
        super(Random_Expand, self).__init__()
        if not isinstance(max_ratio, (int, float)):
            raise TypeError('max_ratio must be an int or float')

        if not isinstance(fill, (int, tuple, type(None))):
            raise TypeError('fill must be an int or tuple')

        if not isinstance(keep_ratio, bool):
            raise TypeError('keep_ratio must be bool')

        if not isinstance(thresh, (int, float)):
            raise TypeError('thresh must be an int or float')

        self.max_ratio = max_ratio
        self.fill = fill
        self.keep_ratio = keep_ratio
        self.thresh = thresh

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(max_ratio={self.max_ratio}, fill={self.fill}, keep_ratio={self.keep_ratio}, thresh={self.thresh})"

    def forward(self, image, targets=None):
        # Check if random expansion should be applied based on the threshold
        if random.random() > self.thresh:  # If not, return the original image and bounding boxes
            return image, targets

        # Check if the maximum expansion ratio is less than 1 or not properly specified
        if self.max_ratio < 1.0:
            return image, targets  # If so, return the original image and bounding boxes

        # Get the height, width, and number of channels of the input image
        h, w, c = image.shape

        # Generate random expansion ratios for width and height
        ratio_x = random.uniform(1, self.max_ratio)
        if self.keep_ratio:
            ratio_y = ratio_x  # If keeping ratio, use the same ratio for both dimensions
        else:
            ratio_y = random.uniform(1, self.max_ratio)  # Otherwise, generate a separate ratio for height

        # Calculate the new height and width after expansion
        oh = int(h * ratio_y)
        ow = int(w * ratio_x)

        # Generate random offsets for placing the original image within the expanded canvas
        off_x = random.randint(0, ow - w)
        off_y = random.randint(0, oh - h)

        # Create an empty canvas for the expanded image
        out_img = np.zeros((oh, ow, c))

        # Fill the canvas with a specified color if provided
        if self.fill and len(self.fill) == c:
            for i in range(c):
                out_img[:, :, i] = self.fill[i] * 255.0

        # Place the original image onto the expanded canvas at the generated offset
        out_img[off_y:off_y + h, off_x:off_x + w, :] = image

        if self.targets is not None:
            # Update the bounding box coordinates to reflect the expansion
            targets[:, 0] = ((targets[:, 0] * w) + off_x) / float(ow)  # Adjust xmin-coordinates
            targets[:, 1] = ((targets[:, 1] * h) + off_y) / float(oh)  # Adjust ymin-coordinates
            targets[:, 2] = ((targets[:, 2] * w) + off_x) / float(ow)  # Adjust xmax-coordinates
            targets[:, 3] = ((targets[:, 3] * h) + off_y) / float(oh)  # Adjust ymax-coordinates

        return out_img.astype('uint8') if not targets else (out_img.astype('uint8'), targets)
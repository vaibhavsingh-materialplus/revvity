import numpy as np

def iou(box1, box2):
  """
  Calculates the Intersection Over Union (IoU) of two bounding boxes.

  Args:
    box1: A numpy array containing the coordinates of the first bounding box in the format [x1, y1, x2, y2].
    box2: A numpy array containing the coordinates of the second bounding box in the format [x1, y1, x2, y2].

  Returns:
    The IoU value between the two bounding boxes.
  """

  # Get the coordinates of the intersection rectangle
  x1 = max(box1[0], box2[0])
  y1 = max(box1[1], box2[1])
  x2 = min(box1[2], box2[2])
  y2 = min(box1[3], box2[3])

  # Compute the area of intersection
  inter_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)

  # Compute the area of both bounding boxes
  box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
  box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

  # Compute the union area
  union_area = float(box1_area + box2_area - inter_area)

  # Compute the IoU
  iou = inter_area / union_area

  return iou
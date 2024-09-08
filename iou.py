def calculate_iou(boxA, boxB):
    # Unpack the bounding boxes
    xA, yA, xA2, yA2 = boxA
    xB, yB, xB2, yB2 = boxB

    # Compute the (x, y) coordinates of the intersection rectangle
    xI = max(xA, xB)
    yI = max(yA, yB)
    xI2 = min(xA2, xB2)
    yI2 = min(yA2, yB2)

    # Compute the area of intersection rectangle
    interArea = max(0, xI2 - xI) * max(0, yI2 - yI)

    # Compute the area of both bounding boxes
    boxAArea = (xA2 - xA) * (yA2 - yA)
    boxBArea = (xB2 - xB) * (yB2 - yB)

    # Compute the area of union
    unionArea = boxAArea + boxBArea - interArea

    # Compute the IoU
    iou = interArea / unionArea

    return iou

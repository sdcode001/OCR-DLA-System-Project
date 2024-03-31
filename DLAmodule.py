# install detectron2 by pip install detectron2

import numpy as np
from ditod import add_vit_config
import torch
from detectron2.config import get_cfg
from detectron2.data import MetadataCatalog
from detectron2.engine import DefaultPredictor
from detectron2.structures import BitMasks, Boxes, BoxMode, Keypoints, PolygonMasks, RotatedBoxes


class DLA:
    predictor=None
    cfg=None

    def __init__(self):
        # Step 1: instantiate config
        self.cfg = get_cfg()
        add_vit_config(self.cfg)
        self.cfg.merge_from_file('publaynet_configs/maskrcnn/maskrcnn_dit_base.yaml')
        # Step 2: add model weights URL to config
        # cfg.merge_from_list('https://layoutlm.blob.core.windows.net/dit/dit-fts/publaynet_dit-b_mrcnn.pth')
        self.cfg.MODEL.WEIGHTS = 'model_final.pth'
        # Step 3: set device
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.cfg.MODEL.DEVICE = device
        # Step 4: define model
        self.predictor = DefaultPredictor(self.cfg)


    #this function returns a list containing lable and top_left and bottom_right coordinates of each rectangle section on the image.
    def get_output(self,img1):
        img=img1
        md = MetadataCatalog.get(self.cfg.DATASETS.TEST[0])
        if self.cfg.DATASETS.TEST[0] == 'icdar2019_test':
            md.set(thing_classes=["table"])
        else:
            md.set(thing_classes=["text", "title", "list", "table", "figure"])  # 0: "Text", 1: "Title", 2: "List", 3:"Table", 4:"Figure"

        output = self.predictor(img)["instances"]

        boxes = output.pred_boxes if output.has("pred_boxes") else None
        classes = output.pred_classes if output.has("pred_classes") else None
        lables =classes.detach().numpy()

        if isinstance(boxes, Boxes) or isinstance(boxes, RotatedBoxes):
            bboxs = boxes.tensor.detach().numpy()
        else:
            bboxs = np.asarray(boxes)

        result=[]

        for i in range(len(lables)):
            if lables[i]==0:
                lable='Text'
            elif lables[i]==1:
                lable = 'Title'
            elif lables[i]==2:
                lable = 'List'
            elif lables[i]==3:
                lable = 'Table'
            else:
                lable = 'Figure'

            x_top_left = bboxs[i][0]
            y_top_left = bboxs[i][1]
            x_bottom_right = bboxs[i][2]
            y_bottom_right = bboxs[i][3]

            result.append(([(int(x_top_left), int(y_top_left)), (int(x_bottom_right), int(y_bottom_right))], lable))

        return result











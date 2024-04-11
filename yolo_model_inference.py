"""
Author: alpha<alpha@57blocks.com>
Time: 2024-03-13,
Description: yolo model inference
"""
import os
import cv2
import torch
import pandas as pd
from tqdm import tqdm

this_file_path = os.path.dirname(os.path.realpath(__file__))

LABEL = ["logo", "year", "series", "issue number", "manufacturer"]

# Greater than this threshold will be extracted.
BOX_CONFIDENCE_THRESHOLD = 0.3


def inference(img_path,
              checkpoint=this_file_path + '/checkpoints/yolov5_card.pt',
              repo="ultralytics/yolov5"):
    """
    img_path: image path
    checkpoint: model path
    repo: model repo
    results: inference results in pandas dataframe
    [xmin, ymin, xmax, ymax, confidence, class,name]
    label = [manufacture, year, series,issue number]
    """

    model = torch.hub.load(repo, 'custom', checkpoint)
    results = model(img_path)
    results = results.pandas().xyxy[0]
    return results


def drop_duplicates(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Delete targets in the same category based on confidence.
    """

    dataframe.groupby('class')['confidence'].idxmax()
    dataframe = dataframe.drop_duplicates(subset='class', keep='first', ignore_index=True)
    return dataframe


def normalize_coordinates(tl_points: list, br_points: list, h: int, w: int) -> list:
    """
    Normalize coordinate to [0, 1]
    @tl_points: top left point
    @br_points: bottom right point
    @h: image height
    @w: image width
    return: [center_x, center_y, width, height]
    """

    center_x = ((br_points[0] - tl_points[0]) / 2 + tl_points[0]) / w
    center_y = ((br_points[1] - tl_points[1]) / 2 + tl_points[1]) / h
    width = (br_points[0] - tl_points[0]) / w
    height = (br_points[1] - tl_points[1]) / h
    if center_y < 0 or center_x < 0 or width < 0 or height < 0:
        print("Warning: negative value: ", center_x, center_y, width, height)
    return [center_x, center_y, width, height]


def model_output_to_coco(img_path: str,
                         yolo_output: pd.DataFrame,
                         threshold=BOX_CONFIDENCE_THRESHOLD,
                         save_txt_folder: str = None):
    """
    convert model output to coco format
    @img_path: image path
    @output: model output
    @h: image height
    @w: image width
    @threshold: confidence threshold
    """

    if not os.path.exists(img_path):
        raise FileNotFoundError(f"{img_path} not found")
    img_name = os.path.basename(img_path).replace('.jpg', '')
    img_data_bgr = cv2.imread(img_path)
    _h, _w, _c = img_data_bgr.shape
    ocr_types = yolo_output["name"].tolist()
    if save_txt_folder is not None:
        txt_absolute_path = os.path.join(save_txt_folder, f'{img_name}.txt')
    else:
        txt_absolute_path = f'{img_name}.txt'
    with open(txt_absolute_path, 'w', encoding='utf-8') as f:
        for extract_type in ocr_types:
            box_info = yolo_output.loc[yolo_output["name"] == extract_type]
            for row in box_info.itertuples():
                x1 = int(row.xmin)
                y1 = int(row.ymin)
                x2 = int(row.xmax)
                y2 = int(row.ymax)
                confidence = row.confidence
                if confidence > threshold:
                    label = extract_type
                    center_x, center_y, width, height = normalize_coordinates([x1, y1], [x2, y2], _h, _w)
                    f.write(f"{LABEL.index(label)} {center_x} {center_y} {width} {height}\n")


def model_output_to_coco_no_label(img_path: str,
                                  yolo_output: pd.DataFrame,
                                  remove_label: str,
                                  threshold=BOX_CONFIDENCE_THRESHOLD):
    """
    Convert model output to coco format without specific label
    @img_path: image absolute path
    @yolo_output: Yolo model output in pandas.DataFrame
    @remove_label: label to be deleted
    @threshold: confidence threshold,lower than this threshold will be deleted
    """

    yolo_output = yolo_output[~(yolo_output['name'] == remove_label)]
    model_output_to_coco(img_path, yolo_output, threshold)


def check_coco_format():
    txt = '/Users/57block/PycharmProjects/card-scan-service/ai_models/obj_detect/24TBB1_5403_BK.txt'
    img = '/Users/57block/PycharmProjects/yolov5/datasets/target_good/24TBB1_5403_BK.jpg'
    img_data = cv2.imread(img, -1)
    h, w, c = img_data.shape

    with open(txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            label, center_x, center_y, width, height = map(float, line.split())
            center_x, center_y, width, height = float(center_x) * w, float(center_y) * h, float(width) * w, float(
                height) * h
            tl_points = [center_x - width / 2, center_y - height / 2]
            br_points = [center_x + width / 2, center_y + height / 2]
            img_data = cv2.rectangle(img_data, (int(tl_points[0]), int(tl_points[1])),
                                     (int(br_points[0]), int(br_points[1])),
                                     (0, 0, 255), 2)
            cv2.imwrite("111.jpg", img_data)


def main(source_img_folder:str, target_txt_folder:str=None):
    img_list = os.listdir(source_img_folder)
    for img_name in tqdm(img_list):
        img_path = os.path.join(source_img_folder, img_name)
        output = inference(img_path)
        output = drop_duplicates(output)
        model_output_to_coco(img_path, output, save_txt_folder=target_txt_folder)


if __name__ == '__main__':
    main()

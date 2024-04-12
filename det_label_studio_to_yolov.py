import json

ANNOTATION_JSON_PATH = "/Users/57block/Desktop/workspace/work/label-studio/data/annotation_result/fanatics-20240412.json"
YOLOV_OUTPUT_DIR = "/Users/57block/Desktop/workspace/work/label-studio/data/annotation_result/yolov"

LABEL = ["logo", "year", "series", "issue number", "manufacturer"]


def coordinate_transformation(x, y, w, h):
    new_w = w / 100
    new_h = h / 100
    new_x = (x + w / 2) / 100
    new_y = (y + h / 2) / 100
    return new_x, new_y, new_w, new_h


# default load from json file
def load_annotation_json(annotation_json_path: str):
    # 读取import json文件，里面是一个json list
    with open(annotation_json_path, "r") as f:
        return json.load(f)


if __name__ == '__main__':
    result_json = load_annotation_json(ANNOTATION_JSON_PATH)
    print(result_json)

    # 先取前5个试试
    for result_json_item in result_json[:]:
        annotation = result_json_item["annotations"]
        data = result_json_item["data"]
        # 裁切文件名称{'image': '/data/local-files/?d=fanatics-20240412/006c1f6c-b786-11ed-805a-4235db585945-back-crop.jpg'}并替换扩展名为txt作为输出的文件名
        output_name = data["image"].split("/")[-1].replace(".jpg", ".txt")
        # 读取annotation items
        annotation_items = annotation[0]["result"]
        """
        输出成yolov格式
        0 0.39675174013921116 0.7512908777969018 0.11136890951276102 0.03614457831325301
        3 0.19837587006960558 0.09982788296041308 0.16937354988399073 0.020654044750430294
        4 0.41879350348027844 0.7986230636833046 0.17865429234338748 0.01721170395869191
        1 0.3062645011600928 0.7994836488812392 0.04176334106728538 0.0189328743545611
        """
        with open(f"{YOLOV_OUTPUT_DIR}/{output_name}", "w") as f:
            for annotation_item in annotation_items:
                v = annotation_item["value"]
                key_cls_index = LABEL.index(annotation_item["value"]["rectanglelabels"][0])
                x, y, w, h = coordinate_transformation(v["x"], v["y"], v["width"], v["height"])
                f.write(f"{key_cls_index} {x} {y} {w} {h}\n")

import json
from pathlib import Path
from PIL import Image

LABEL = ["logo", "year", "series", "issue number", "manufacturer"]
LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT = "/Users/57block/label-studio-storage"
LOCAL_STORAGE_PREFIX = "test"


def convert(source_img: dict, score: float = 0.5, model_version: str = "yolov"):
    w = source_img["size_w"]
    h = source_img["size_h"]
    labels = source_img["labels"]
    prediction_items = []
    for key in labels:
        point = labels[key]
        key_w = point[2] * 100
        key_h = point[3] * 100
        key_x = point[0] * 100 - key_w / 2
        key_y = point[1] * 100 - key_h / 2
        prediction_items.append({
            "original_width": w,
            "original_height": h,
            "image_rotation": 0,
            "value": {
                "x": key_x,
                "y": key_y,
                "width": key_w,
                "height": key_h,
                "rotation": 0,
                "rectanglelabels": [key]
            },
            "id": key,
            "from_name": "label",
            "to_name": "image",
            "type": "rectanglelabels",
            "origin": "manual"
        })
    return {
        "model_version": model_version,
        "score": score,
        "result": prediction_items
    }


def load_data(label_txt_path: Path):
    label_dict = {}
    # 读取label文件内容
    with open(label_txt_path, "r") as f:
        # 逐行读取去掉换行符
        for line in f:
            # 分割字符串
            data = line.split(" ")
            # 获取label名称
            key_cls = LABEL[int(data[0])]
            # 获取label坐标
            key_x = float(data[1])
            key_y = float(data[2])
            key_w = float(data[3])
            key_h = float(data[4])
            # 添加到字典
            label_dict[key_cls] = [key_x, key_y, key_w, key_h]
    # 返回结果
    return label_dict


def save_label_studio_import_json(to_saved_img_list: list):
    to_saved_img_list = [{
        # 如果有label就转换，没有就不转换
        "predictions": [convert(item)] if item["has_label"] else [],
        "data": {
            "image": f"/data/local-files/?d={LOCAL_STORAGE_PREFIX}/{item['name']}"
        },
        "id": item["name"],
    } for item in to_saved_img_list]
    # 绝对路径是LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT + local_storage_prefix
    local_storage_prefix = Path(LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT) / LOCAL_STORAGE_PREFIX / "import.json"
    with open(local_storage_prefix, "w") as f:
        json.dump(to_saved_img_list, f, indent=4)


if __name__ == '__main__':
    # 设置路径
    img_path = Path("data/yolov/img")
    label_path = Path("data/yolov/label")
    # 遍历img_path下的所有图片
    img_list = []
    for img in img_path.iterdir():
        # 读取名称并获取对应的label文件
        iter_img = img.name
        iter_label = iter_img.replace("jpg", "txt")
        iter_label_path = label_path / iter_label
        if not iter_label_path.exists():
            print(f"Label file {iter_label_path} not exists!")
            one_img = {
                "name": iter_img,
                "has_label": False
            }
            img_list.append(one_img)
        else:
            # 读取label文件内容
            image = Image.open(img)
            one_img = {
                "name": iter_img,
                "labels": load_data(iter_label_path),
                "size_w": image.size[0],
                "size_h": image.size[1],
                "has_label": True
            }
            img_list.append(one_img)
    # 先检查有没有目录没有就创建
    local_storage_path = Path(LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT) / LOCAL_STORAGE_PREFIX
    if not local_storage_path.exists():
        local_storage_path.mkdir()
    # 将img_list copy到local storage
    for i in img_list:
        image = Image.open(img_path / i["name"])
        image.save(local_storage_path / i["name"])
    # 将img_list保存为json文件
    save_label_studio_import_json(img_list)

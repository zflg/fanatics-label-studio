import json

if __name__ == '__main__':
    # 读取import json文件，里面是一个json list
    with open("data/yolov/img/import.json", "r") as f:
        import_json = json.load(f)
    # 读取name.txt文件放到list里面,name.txt里面的names使用的空格做为分隔符
    with open("data/yolov/img/name.txt", "r") as f:
        names = f.read().split(" ")
    # 遍历import_json list 过滤names不包含id的数据
    new_json = []
    for item in import_json:
        if item["id"] in names:
            new_json.append(item)
    # 保存到新的import.json文件
    with open("data/yolov/img/new_import.json", "w") as f:
        json.dump(new_json, f)
    # 找一下names里面有json里面没有的打印一下
    for name in names:
        if name not in [item["id"] for item in import_json]:
            print(name)

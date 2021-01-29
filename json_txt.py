from __future__ import print_function
import os, sys, zipfile
import json


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = box[0] + box[2] / 2.0
    y = box[1] + box[3] / 2.0
    w = box[2]
    h = box[3]

    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

print(' '.join(sys.argv[1:2]))
print(' '.join(sys.argv[2:]))

json_file = ' '.join(sys.argv[1:2]) # # Object Instance 类型的标注

data = json.load(open(json_file, 'r'))

ana_txt_save_path = ' '.join(sys.argv[2:])  # 保存的路径


if not os.path.exists(ana_txt_save_path):
    os.makedirs(ana_txt_save_path)

for img in data['images']:
    # print(img["file_name"])
    filename = img["file_name"]
    img_width = img["width"]
    img_height = img["height"]
    # print(img["height"])
    # print(img["width"])
    img_id = img["id"]
    ana_txt_name = filename.split(".")[0] + ".txt"  # 对应的txt名字，与jpg一致
    print(ana_txt_name)
    f_txt = open(os.path.join(ana_txt_save_path, ana_txt_name), 'w')
    for ann in data['annotations']:
        if ann['image_id'] == img_id:
            # annotation.append(ann)
            # print(ann["category_id"], ann["bbox"])
            box = convert((img_width, img_height), ann["bbox"])
            f_txt.write("%s %s %s %s %s\n" % (ann["category_id"], box[0], box[1], box[2], box[3]))
    f_txt.close()

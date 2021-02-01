from __future__ import print_function
import tkinter.filedialog
import tkinter as tk

import os

import xml.etree.ElementTree as ET
import os
import json
import sys

import os, sys, zipfile
import json

coco = dict()
coco['images'] = []
coco['type'] = 'instances'
coco['annotations'] = []
coco['categories'] = []

category_set = dict()
image_set = set()

category_item_id = -1
image_id = 0
annotation_id = 0


def selectPath1():
    # 选择文件path_接收文件地址
    path_ = tkinter.filedialog.askdirectory()

    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path.set(path_)

def selectPath2():
    # 选择文件path_接收文件地址
    path_ = tkinter.filedialog.askdirectory()

    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path2.set(path_)

def selectPath3():
    path_ = tkinter.filedialog.askopenfilename()

    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path3.set(path_)

def selectPath4():
    # 选择文件path_接收文件地址
    path_ = tkinter.filedialog.askdirectory()

    # 通过replace函数替换绝对文件地址中的/来使文件可被程序读取
    # 注意：\\转义后为\，所以\\\\转义后为\\
    path_ = path_.replace("/", "\\\\")
    # path设置path_的值
    path4.set(path_)




def aaa():
    #print(path2.get())
    #os.system('python xml_json.py {} {}'.format(path.get(),path2.get()))


    def addCatItem(name):
        global category_item_id
        category_item = dict()
        category_item['supercategory'] = 'none'
        category_item_id += 1
        category_item['id'] = category_item_id
        category_item['name'] = name
        coco['categories'].append(category_item)
        category_set[name] = category_item_id
        return category_item_id

    def addImgItem(file_name, size):
        global image_id
        if file_name is None:
            raise Exception('Could not find filename tag in xml file.')
        if size['width'] is None:
            raise Exception('Could not find width tag in xml file.')
        if size['height'] is None:
            raise Exception('Could not find height tag in xml file.')
        image_id += 1
        image_item = dict()
        image_item['id'] = image_id
        image_item['file_name'] = file_name
        image_item['width'] = size['width']
        image_item['height'] = size['height']
        coco['images'].append(image_item)
        image_set.add(file_name)
        return image_id

    def addAnnoItem(object_name, image_id, category_id, bbox):
        global annotation_id
        annotation_item = dict()
        annotation_item['segmentation'] = []
        seg = []
        # bbox[] is x,y,w,h
        # left_top
        seg.append(bbox[0])
        seg.append(bbox[1])
        # left_bottom
        seg.append(bbox[0])
        seg.append(bbox[1] + bbox[3])
        # right_bottom
        seg.append(bbox[0] + bbox[2])
        seg.append(bbox[1] + bbox[3])
        # right_top
        seg.append(bbox[0] + bbox[2])
        seg.append(bbox[1])

        annotation_item['segmentation'].append(seg)

        annotation_item['area'] = bbox[2] * bbox[3]
        annotation_item['iscrowd'] = 0
        annotation_item['ignore'] = 0
        annotation_item['image_id'] = image_id
        annotation_item['bbox'] = bbox
        annotation_item['category_id'] = category_id
        annotation_id += 1
        annotation_item['id'] = annotation_id
        coco['annotations'].append(annotation_item)

    def parseXmlFiles(xml_path):
        for f in os.listdir(xml_path):
            if not f.endswith('.xml'):
                continue

            bndbox = dict()
            size = dict()
            current_image_id = None
            current_category_id = None
            file_name = None
            size['width'] = None
            size['height'] = None
            size['depth'] = None

            xml_file = os.path.join(xml_path, f)
            print(xml_file)

            tree = ET.parse(xml_file)
            root = tree.getroot()
            if root.tag != 'annotation':
                raise Exception('pascal voc xml root element should be annotation, rather than {}'.format(root.tag))

            # elem is <folder>, <filename>, <size>, <object>
            for elem in root:
                current_parent = elem.tag
                current_sub = None
                object_name = None

                if elem.tag == 'folder':
                    continue

                if elem.tag == 'filename':
                    file_name = elem.text
                    if file_name in category_set:
                        raise Exception('file_name duplicated')

                # add img item only after parse <size> tag
                elif current_image_id is None and file_name is not None and size['width'] is not None:
                    if file_name not in image_set:
                        current_image_id = addImgItem(file_name, size)
                        print('add image with {} and {}'.format(file_name, size))
                    else:
                        raise Exception('duplicated image: {}'.format(file_name))
                        # subelem is <width>, <height>, <depth>, <name>, <bndbox>
                for subelem in elem:
                    bndbox['xmin'] = None
                    bndbox['xmax'] = None
                    bndbox['ymin'] = None
                    bndbox['ymax'] = None

                    current_sub = subelem.tag
                    if current_parent == 'object' and subelem.tag == 'name':
                        object_name = subelem.text
                        if object_name not in category_set:
                            current_category_id = addCatItem(object_name)
                        else:
                            current_category_id = category_set[object_name]

                    elif current_parent == 'size':
                        if size[subelem.tag] is not None:
                            raise Exception('xml structure broken at size tag.')
                        size[subelem.tag] = int(subelem.text)

                    # option is <xmin>, <ymin>, <xmax>, <ymax>, when subelem is <bndbox>
                    for option in subelem:
                        if current_sub == 'bndbox':
                            if bndbox[option.tag] is not None:
                                raise Exception('xml structure corrupted at bndbox tag.')
                            bndbox[option.tag] = int(option.text)

                    # only after parse the <object> tag
                    if bndbox['xmin'] is not None:
                        if object_name is None:
                            raise Exception('xml structure broken at bndbox tag')
                        if current_image_id is None:
                            raise Exception('xml structure broken at bndbox tag')
                        if current_category_id is None:
                            raise Exception('xml structure broken at bndbox tag')
                        bbox = []
                        # x
                        bbox.append(bndbox['xmin'])
                        # y
                        bbox.append(bndbox['ymin'])
                        # w
                        bbox.append(bndbox['xmax'] - bndbox['xmin'])
                        # h
                        bbox.append(bndbox['ymax'] - bndbox['ymin'])
                        print(
                            'add annotation with {},{},{},{}'.format(object_name, current_image_id, current_category_id,
                                                                     bbox))
                        addAnnoItem(object_name, current_image_id, current_category_id, bbox)

    xml_path =path.get()
    # json生成的文件位置

    json_file = path2.get() + '\\instances_train2017.json'
    parseXmlFiles(xml_path)
    json.dump(coco, open(json_file, 'w'))

def bbb():
    #os.system('python json_txt.py {} {}'.format(path3.get(),path4.get()))
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



    json_file = path3.get()  # # Object Instance 类型的标注

    data = json.load(open(json_file, 'r'))

    ana_txt_save_path = path4.get()  # 保存的路径

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
#####################################################################################
main_box=tk.Tk()
main_box.title('转换器')
#窗口居中
width = 310
height = 220
screenwidth = main_box.winfo_screenwidth()
screenheight = main_box.winfo_screenheight()
alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
main_box.geometry(alignstr)



#变量path
path = tk.StringVar()
#输入框，标记，按键
tk.Label(main_box,text = "初始xml文件路径:").grid(row = 0, column = 0)
#输入框绑定变量path
tk.Entry(main_box, textvariable = path).grid(row = 0, column = 1)
tk.Button(main_box, text = "路径选择", command = selectPath1).grid(row = 0, column = 2)

#变量path2
path2 = tk.StringVar()
#输入框，标记，按键
tk.Label(main_box,text = "生成json文件路径:").grid(row = 1, column = 0)
#输入框绑定变量path
tk.Entry(main_box, textvariable = path2).grid(row = 1, column = 1)
tk.Button(main_box, text = "路径选择", command = selectPath2).grid(row = 1, column = 2)



tk.Button(main_box, text = "xml转json", command = aaa).grid(row = 2, column = 0)

tk.Label(main_box,text = "     ").grid(row = 3)

#变量path3
path3 = tk.StringVar()
#输入框，标记，按键
tk.Label(main_box,text = "初始json文件路径:").grid(row = 4, column = 0)
#输入框绑定变量path
tk.Entry(main_box, textvariable = path3).grid(row = 4, column = 1)
tk.Button(main_box, text = "路径选择", command = selectPath3).grid(row = 4, column = 2)

#变量path4
path4 = tk.StringVar()
#输入框，标记，按键
tk.Label(main_box,text = "生成txt文件路径:").grid(row = 5, column = 0)
#输入框绑定变量path
tk.Entry(main_box, textvariable = path4).grid(row = 5, column = 1)
tk.Button(main_box, text = "路径选择", command = selectPath4).grid(row = 5, column = 2)





tk.Button(main_box, text = "json转txt", command = bbb).grid(row = 6, column = 0)





main_box.mainloop()

import tkinter.filedialog
import tkinter as tk

import os

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
    os.system('python xml_json.py {} {}'.format(path.get(),path2.get()))

def bbb():
    os.system('python json_txt.py {} {}'.format(path3.get(),path4.get()))
#####################################################################################
main_box=tk.Tk()
main_box.title('转换器')
#main_box.geometry("320x320")


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

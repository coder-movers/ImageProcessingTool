import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import os
from PIL import Image

window = tk.Tk()

window.title("Image Processing Tool")
window.geometry("400x300+400+400")
window.resizable(width=False, height=False)

splice_selected_folder_path = ""  # 拼接源文件夹路径
split_selected_folder_path = ""  # 拆分源文件夹路径


def splice_select_folder():
    global splice_selected_folder_path
    # 打开文件夹选择框
    folder_path = filedialog.askdirectory()

    if folder_path:
        splice_selected_folder_path = folder_path
        splice_input_folder_path.set(splice_selected_folder_path)


def split_select_folder():
    global split_selected_folder_path
    # 打开文件夹选择框
    folder_path = filedialog.askdirectory()

    if folder_path:
        split_selected_folder_path = folder_path
        split_input_folder_path.set(split_selected_folder_path)


def splice_images_in_folder():
    if splice_selected_folder_path:
        # 获取文件夹内所有文件列表
        file_list = os.listdir(splice_selected_folder_path)

        # 保存所有图片路径列表
        image_files = [os.path.join(splice_selected_folder_path, file_name) for file_name in file_list
                       if file_name.lower().endswith(('.png', '.jpg', '.jpeg'))]

        output_folder = "output1_folder"
        os.makedirs(output_folder, exist_ok=True)

        # 计数器
        count = 0

        # 确定拼接图片尺寸
        num_images = len(image_files)
        collage_width = 3  # 横向拼接几张
        collage_height = 2  # 纵向拼接几张
        thumb_width, thumb_height = Image.open(image_files[0]).size

        # 确定生成大图的数量
        num_collages = (num_images + collage_width * collage_height - 1) // (collage_width * collage_height)

        # 进度条
        progress = tk.Tk()
        progress.title("生成进度")
        progress.geometry("300x100+450+450")

        frame_progress = tk.Frame(progress)
        frame_progress.pack(pady=10)

        progress_bar = ttk.Progressbar(frame_progress, length=250, mode='determinate', maximum=num_collages)
        progress_bar.pack()

        for i in range(num_collages):
            if i * (collage_width * collage_height) >= num_images:
                break

            # 生成空白的大图片
            collage = Image.new('RGB', (thumb_width * collage_width, thumb_height * collage_height))

            for j in range(collage_width * collage_height):
                if i * (collage_width * collage_height) + j < num_images:
                    img = Image.open(image_files[i * (collage_width * collage_height) + j])
                    collage.paste(img, (j % collage_width * thumb_width, j // collage_width * thumb_height))

            collage.save(os.path.join(output_folder, f'collage_{i + 1}.png'), quality=100, optimize=False)
            count += 1

            progress_bar['value'] = count
            progress.update()

        progress.destroy()
        messagebox.showinfo("完成", "拼接图片生成完成！")


def split_images_in_folder():
    if split_selected_folder_path:
        # 获取输入目录中的所有图片文件
        image_files = [f for f in os.listdir(split_selected_folder_path) if
                       os.path.isfile(os.path.join(split_selected_folder_path, f))]
        image_files.sort()  # 按文件名排序，确保顺序

        # 初始化计数器
        count = 1

        # 设置分割的行数和列数
        num_cols = 3
        num_rows = 2

        # 输出文件夹路径（保存拆分后的小图）
        output_folder = "output2_folder"
        os.makedirs(output_folder, exist_ok=True)

        # 确定生成小图的数量
        num_sum = num_cols * num_rows * len(image_files)

        # 进度条
        progress = tk.Tk()
        progress.title("分割进度")
        progress.geometry("300x100+450+450")

        frame_progress = tk.Frame(progress)
        frame_progress.pack(pady=10)

        progress_bar = ttk.Progressbar(frame_progress, length=250, mode='determinate', maximum=num_sum)
        progress_bar.pack()

        # 逐个处理每个图片文件
        for image_file in image_files:
            # 拼接图片文件路径
            image_path = os.path.join(split_selected_folder_path, image_file)

            # 打开大图片
            image = Image.open(image_path)

            # 获取大图片的尺寸
            img_width, img_height = image.size

            # 确定每张小图片的宽度和高度
            tile_width = img_width // num_cols
            tile_height = img_height // num_rows

            # 分割并保存小图片
            for y in range(num_rows):
                for x in range(num_cols):
                    left = x * tile_width
                    upper = y * tile_height
                    right = left + tile_width
                    lower = upper + tile_height

                    # 从大图片中裁剪出小图片
                    tile = image.crop((left, upper, right, lower))

                    # 保存小图片为PNG格式，并添加排序号
                    tile_path = os.path.join(output_folder, f'{count}.png')
                    tile.save(tile_path, format='PNG')

                    # 增加计数器
                    count += 1

                    progress_bar['value'] = count
                    progress.update()

        progress.destroy()
        messagebox.showinfo("完成", "分割图片完成！")


def set_notebook_style():
    style = ttk.Style()
    style.theme_create("custom", parent="alt", settings={
        "TNotebook": {"configure": {"background": "#FFFFFF"}},
        "TNotebook.Tab": {
            "configure": {
                "padding": [10, 5],
                "font": ('Helvetica', 10)
            },
            "map": {
                "background": [("selected", "lightblue"), ("!selected", "white")],
                "font": [("selected", "Helvetica 10 bold")],
            },
        },
        "TFrame": {
            "configure": {"background": "#FFFFFF"}
        }
    })
    style.theme_use("custom")


def create_tab(nb, text, func):
    tab = ttk.Frame(nb, borderwidth=2, relief="ridge")
    nb.add(tab, text=text)
    func(tab)


def tab1_func(tab):
    # 源文件夹路径
    splice_input_folder_path.set("请选择文件夹...")
    splice_entry_folder_path = tk.Label(tab, textvariable=splice_input_folder_path, font=('Helvetica Neue', 10),
                                        bg="#FFFFFF")
    splice_entry_folder_path.pack(pady=20)

    # 选择文件夹
    splice_btn_select_folder = tk.Button(tab, text="选择文件夹", command=splice_select_folder, padx=20, pady=5,
                                         font=('Helvetica Neue', 10))
    splice_btn_select_folder.pack(pady=20)

    # 生成拼接图片
    splice_btn_generate_collage = tk.Button(tab, text="生成拼接图片", command=splice_images_in_folder, padx=20, pady=5,
                                            font=('Helvetica Neue', 10))
    splice_btn_generate_collage.pack(pady=20)


def tab2_func(tab):
    split_input_folder_path.set("请选择文件夹...")
    split_entry_folder_path = tk.Label(tab, textvariable=split_input_folder_path, font=('Helvetica Neue', 10),
                                       bg="#FFFFFF")
    split_entry_folder_path.pack(pady=20)

    # 选择文件夹
    split_btn_select_folder = tk.Button(tab, text="选择文件夹", command=split_select_folder, padx=20, pady=5,
                                        font=('Helvetica Neue', 10))
    split_btn_select_folder.pack(pady=20)

    # 拆分所有图片
    split_btn_generate_collage = tk.Button(tab, text="拆分所有图片", command=split_images_in_folder, padx=20, pady=5,
                                           font=('Helvetica Neue', 10))
    split_btn_generate_collage.pack(pady=20)


set_notebook_style()
notebook = ttk.Notebook(window, style="Custom.TNotebook")
notebook.pack(expand=True, fill="both")

splice_input_folder_path = tk.StringVar()
split_input_folder_path = tk.StringVar()

# 创建tab页
tabs = [
    ("图片拼接", tab1_func),
    ("图片拆分", tab2_func),
]

for tab_text, tab_func in tabs:
    create_tab(notebook, tab_text, tab_func)

window.mainloop()

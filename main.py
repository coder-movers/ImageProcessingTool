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
generated_collages = 0  # 已生成的大图数量
split_selected_folder_path = ""  # 拆分源文件夹路径


def select_folder():
    global splice_selected_folder_path
    # 打开文件夹选择框
    folder_path = filedialog.askdirectory()

    if folder_path:
        splice_selected_folder_path = folder_path
        splice_input_folder_path.set(splice_selected_folder_path)


def generate_collage():
    global generated_collages
    if splice_selected_folder_path:
        # 获取文件夹内所有文件列表
        file_list = os.listdir(splice_selected_folder_path)

        # 保存所有图片路径列表
        image_files = [os.path.join(splice_selected_folder_path, file_name) for file_name in file_list
                       if file_name.lower().endswith(('.png', '.jpg', '.jpeg'))]

        output_folder = "output1_folder"
        os.makedirs(output_folder, exist_ok=True)

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
            generated_collages += 1

            progress_bar['value'] = generated_collages
            progress.update()

        progress.destroy()
        messagebox.showinfo("完成", "拼接图片生成完成！")


def set_notebook_style():
    style = ttk.Style()
    style.theme_create("custom", parent="alt", settings={
        "TNotebook": {"configure": {"background": "#FFFFFF"}},
        "TNotebook.Tab": {
            "configure": {
                "padding": [10, 5],
                "font": ('Helvetica', 12, 'bold')
            },
            "map": {
                "background": [("selected", "lightblue"), ("!selected", "white")],
                "foreground": [("selected", "black"), ("!selected", "black")],
                "focuscolor": [("selected", "")]
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
    entry_folder_path = tk.Label(tab, textvariable=splice_input_folder_path, font=('Helvetica Neue', 10), bg="#FFFFFF")
    entry_folder_path.pack(pady=20)

    # 选择文件夹
    btn_select_folder = tk.Button(tab, text="选择文件夹", command=select_folder, padx=20, pady=5,
                                  font=('Helvetica Neue', 10))
    btn_select_folder.pack(pady=20)

    # 生成拼接图片
    btn_generate_collage = tk.Button(tab, text="生成拼接图片", command=generate_collage, padx=20, pady=5,
                                     font=('Helvetica Neue', 10))
    btn_generate_collage.pack(pady=20)


def tab2_func(tab):
    pass
    # 源文件夹路径
    # folder_path_var.set("请选择文件夹...")
    # entry_folder_path = tk.Label(tab, textvariable=folder_path_var, font=('Helvetica Neue', 10), bg="#FFFFFF")
    # entry_folder_path.pack(pady=20)
    #
    # # 选择文件夹
    # btn_select_folder = tk.Button(tab, text="选择文件夹", command=select_folder, padx=20, pady=5,
    #                               font=('Helvetica Neue', 10))
    # btn_select_folder.pack(pady=20)
    #
    # # 生成拼接图片
    # btn_generate_collage = tk.Button(tab, text="生成拼接图片", command=generate_collage, padx=20, pady=5,
    #                                  font=('Helvetica Neue', 10))
    # btn_generate_collage.pack(pady=20)


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
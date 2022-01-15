#!/usr/bin/evn python
# -*- coding: utf-8 -*-
# Created by ShoJinto at 2022/1/14

import os
import random
import shutil
import fitz
from PIL import Image


def gen_random_tmp_path(path_str_len: int = 16) -> str:
    seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result_list = list()
    result_list.append("tmp_")
    for _ in range(path_str_len):
        result_list.append(random.choice(seed))
    return "".join(result_list)


def convert_pdf_to_images(pdf_path: str, images_path: str, xargs: tuple) -> int:
    progressbar, pbar_txt = xargs
    try:
        pdf_doc = fitz.open(pdf_path)
        images_amount = pdf_doc.pageCount
        print("Converting PDF to images...")
        for image_id in range(images_amount):
            page = pdf_doc[image_id]
            rotate = int(0)
            # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
            # 此处若是不做设置，默认图片大小为：792X612, dpi=96
            # (1.33333333-->1056x816)   (2-->1584x1224)
            zoom_x = 5  # 1.33333333
            zoom_y = 5  # 1.33333333
            mat = fitz.Matrix(zoom_x, zoom_y).preRotate(rotate)
            pix = page.getPixmap(matrix=mat, alpha=False)

            if not os.path.exists(images_path):
                os.makedirs(images_path)

            pix.writePNG(images_path + "/" + "images_%s.png" % image_id)
            image_id += 1
            progressbar['value'] = int(round(image_id / images_amount, 2) * 100)
            pbar_txt.set(f"{progressbar['value']}%")
        return images_amount
    except Exception as exc:
        print(exc)
        return -1


def merge_images_as_long_image(images_path: str, images_amount: int, long_image_path: str, xargs: tuple) -> bool:
    progressbar, pbar_txt = xargs
    progressbar['value'] = 0
    try:
        long_image = None
        each_tmp_image_size = None
        print("Merging {} images as long image...".format(images_amount))
        for image_id in range(images_amount):
            tmp_image = Image.open(
                images_path + "/" + "images_%s.png" % image_id)
            if long_image is None:
                each_tmp_image_size = tmp_image.size
                long_image = Image.new(
                    "RGB", (each_tmp_image_size[0], images_amount * each_tmp_image_size[1]), (250, 250, 250))
            long_image.paste(
                tmp_image, (0, image_id * each_tmp_image_size[1]))
            image_id += 1
            progressbar['value'] = int(round(image_id / images_amount, 2) * 100)
            pbar_txt.set(f"{progressbar['value']}%")
        long_image.save(long_image_path, "JPEG")
    except Exception as exc:
        print(exc)
        return False
    return True


def clean_tmp_images(images_path: str) -> bool:
    try:
        shutil.rmtree(images_path)
    except Exception as exc:
        print(exc)
        return False
    return True


def convert_pdf_to_long_image(
        pdf_path: str, long_image_path: str = None, xargs: tuple = None,
        images_path: str = None) -> bool:
    if images_path is None:
        images_path = gen_random_tmp_path()
    if long_image_path is None:
        long_image_path = pdf_path.replace(
            ".PDF", ".jpg").replace(".pdf", ".jpg")
    messagebox = xargs[-1]
    xargs = xargs[:-1]
    images_amount = convert_pdf_to_images(pdf_path, images_path, xargs)
    assert images_amount > 0
    assert merge_images_as_long_image(
        images_path, images_amount, long_image_path, xargs)
    assert clean_tmp_images(images_path)
    messagebox.showinfo('提示', '转换完成！！')

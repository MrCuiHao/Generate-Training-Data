# coding:utf8
import cv2
import numpy as np
import os
import gv


def merge(bg_img, fg_img):
    """注释掉的这句代码也是可以截取图片矩形区域的，但是在使用时发现截取的区域不能单纯的赋值给另一个变量，
    它好像指针一样和被截取图片的那块存储区域绑定在一块了，所以如果想对截取的这块区域做其他操作都会影响
    到原图"""
    # bg_seal = bg_img[gv.bg_y:gv.bg_y + gv.seal_bg_h, gv.bg_x:gv.bg_x + gv.seal_bg_w]
    bg_seal = cv2.getRectSubPix(bg_img, (gv.seal_bg_w, gv.seal_bg_h), (gv.bg_crop_x, gv.bg_crop_y))
    cv2.imshow('bg_seal', bg_seal)
    fg_seal = fg_img[gv.lighter_y:gv.lighter_y + gv.lighter_h, gv.lighter_x:gv.lighter_x + gv.lighter_w]
    cv2.imshow("fg_seal", fg_seal)
    bg_seal[gv.merge_start_y:gv.merge_start_y + gv.lighter_h,
    gv.merge_start_x:gv.merge_start_x + gv.lighter_w] = fg_seal
    cv2.imshow("merge", bg_seal)
    cv2.waitKey(1000)
    return bg_seal


def save_gauss_seamless(bg_img_name, fg_img_name, img_num, normal_bg_img):
    produced_img_name = '_'.join(
        [bg_img_name.rstrip(gv.bg_img_format), fg_img_name.rstrip(gv.fg_img_format),
         '{:03d}'.format(img_num),
         gv.produced_img_format])
    produced_img_save_path = os.path.join(gv.gauss_seamless_path, produced_img_name)
    cv2.imwrite(produced_img_save_path, normal_bg_img)


def gauss_seamless(basic_seal, bg_img, kernel_size, mask):
    center = (gv.x, gv.y)
    gauss_basic_seal = cv2.GaussianBlur(basic_seal, ksize=kernel_size, sigmaX=0, sigmaY=0)
    cv2.imshow("gauss_basic_seal", gauss_basic_seal)
    normal_clone = cv2.seamlessClone(gauss_basic_seal, bg_img, mask, center,
                                     cv2.NORMAL_CLONE)
    cv2.imshow("normal_clone", normal_clone)
    cv2.waitKey(1000)
    return normal_clone


def gauss_seamless_seal(basic_seal, bg_img, bg_img_w, bg_img_h, bg_img_name, fg_img_name):
    mask = 255 * np.ones(basic_seal.shape, basic_seal.dtype)
    bg_img_copy = bg_img
    img_num = 1
    seal_count = 0  # 盖章个数
    if not os.path.exists(gv.gauss_seamless_path):
        os.mkdir(gv.gauss_seamless_path)
    for i in range(gv.ksize):
        if i % 2 == 1:
            kernel_size = (i, i)
            if gv.x + 3 * (gv.seal_bg_w / 2) + gv.gap_x < bg_img_w:
                if gv.y + 3 * (gv.seal_bg_h / 2) + gv.gap_y < bg_img_h:
                    bg_img_copy = gauss_seamless(basic_seal, bg_img_copy, kernel_size, mask)
                    seal_count += 1
                    gv.y += (gv.seal_bg_h + gv.gap_y)
                else:
                    if gv.x + 3 * (gv.seal_bg_w / 2) + gv.gap_x < bg_img_w:
                        gv.x += (gv.seal_bg_w + gv.gap_x)
                        gv.y = gv.y_copy
                        bg_img_copy = gauss_seamless(basic_seal, bg_img_copy, kernel_size, mask)
                        seal_count += 1
                        gv.y += (gv.seal_bg_h + gv.gap_y)
                cv2.waitKey(1000)
            else:
                save_gauss_seamless(bg_img_name, fg_img_name, img_num, bg_img_copy)
                img_num += 1
                bg_img_copy = bg_img
                gv.x = gv.x_copy
                gv.y = gv.y_copy
                seal_count = 0
    if seal_count > 0:
        save_gauss_seamless(bg_img_name, fg_img_name, img_num, bg_img_copy)
    gv.x = gv.x_copy
    gv.y = gv.y_copy


def make_train_img():
    for bg_img_name in os.listdir(gv.bg_img_root):
        bg_img_path = os.path.join(gv.bg_img_root, bg_img_name)
        bg_img = cv2.imread(bg_img_path)
        bg_img_copy = bg_img
        bg_img_h, bg_img_w, bg_img_channel = bg_img.shape
        for fg_img_name in os.listdir(gv.fg_img_root):
            fg_img_path = os.path.join(gv.fg_img_root, fg_img_name)
            fg_img = cv2.imread(fg_img_path)
            basic_seal = merge(bg_img, fg_img)
            gauss_seamless_seal(basic_seal, bg_img_copy, bg_img_w, bg_img_h, bg_img_name, fg_img_name)
            cv2.destroyAllWindows()


if __name__ == "__main__":
    make_train_img()

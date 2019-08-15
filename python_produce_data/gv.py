# 前景图、背景图根目录
bg_img_root = "../bg_img"
fg_img_root = "../fg_img"
# 制作的图片保存的路径
gauss_seamless_path = "../output_img/gauss_seamless"
# 图片格式,可以添加不同格式，但是每一类图片格式要统一
bg_img_format = '.png'
fg_img_format = '.jpg'
produced_img_format = '.jpg'
# 在前景图上选取一块合适区域作为状态灯
lighter_x = 10
lighter_y = 10
lighter_w = 12
lighter_h = 20
# 在背景图上选取一块区域作为盖章背景（给出要截取矩形的中心坐标、宽、高）
bg_crop_x = 17
bg_crop_y = 17
seal_bg_w = 34
seal_bg_h = 34
# 在盖章背景选取左上角坐标，作为状态灯与它的起始合并位置
merge_start_x = 10
merge_start_y = 7
# 选取盖章在背景图起始相应的左上角坐标位置
x = 25
y = 25
x_copy = x
y_copy = y
# 盖章之间的间隔
gap_x = 2
gap_y = 2
# 高斯模糊函数GaussianBlur(),参数ksize最大值
ksize = 40

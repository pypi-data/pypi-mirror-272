import numpy as np
import cv2
import os

from utils import convert_image

# 读取图像
image = cv2.imread('example.jpg')

# 定义矩形框的左上角和右下角坐标
x1, y1 = 100, 100  # 左上角坐标
x2, y2 = 300, 300  # 右下角坐标

# 定义矩形框的颜色（BGR 格式）
color =   # 这里是绿色

# 画矩形框


# 显示图像
cv2.imshow('Rectangle', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


def draw_bbox_in_image(img: np.array, 
                       bboxes,
                       save_root_dir: str = "./",
                       save_img_name: str = "origin-draw-pose-img.jpg", 
                       RGB2BGR: bool = False,
                       normlization: bool = False,
                       standardization_mean: np.array = None,
                       standardization_std: np.array = None,
                       draw_bboxes_color: tuple = (0, 255, 0),
                       draw_bboxes_thickness: int = 2):
    """draw pose in image and save it in save_dir

    Args:
        img (np.array): img to draw pose
        pose (_type_): pose can be multiple person or single person
        save_dir (_type_): the dir to save the pose image
        dataset_category (dict, optional): dataset_category, it must contain skeleton at least. Defaults to COCO_CATEGORY.
    """
    img = convert_image(img, RGB2BGR, normlization, standardization_mean, standardization_std)
    
    bboxes = np.array(bboxes)
    assert bboxes.shape[-1] == 4, "the last dimension of bboxes must be 4. It means (x, y, w, h)"
    
    if not os.path.isdir(save_root_dir):
        # 创建文件夹
        os.makedirs(save_root_dir)
            
    save_img_dir = os.path.join(save_root_dir, save_img_name)

    if isinstance(draw_bboxes_color, tuple):
        draw_bboxes_color = [draw_bboxes_color for _ in range(bboxes.shape[0])]
        
    for i, _bbox in enumerate(bboxes):
        x, y, w, h = _bbox
        
        tl_x, tl_y = x - w / 2, y - h / 2
        br_x, br_y = x + w / 2, y + h / 2
        
        # 判断左上角和右下角是否在图像内
        if tl_x < 0 or tl_y < 0 or br_x >= img.shape[1] or br_y >= img.shape[0]:
            continue
        
        # 绘制
        cv2.rectangle(image, (int(tl_x), int(tl_y)), (int(br_x), int(br_y)), draw_bboxes_color[i], thickness=draw_bboxes_thickness)
            
    cv2.imwrite(save_img_dir, img)
    
    return img
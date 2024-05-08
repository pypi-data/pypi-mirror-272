import numpy as np
import torch
import cv2
import os
    
def get_draw_preset(draw_preset):
    skeleton, kpt_color, skeleton_color = None, None, None
    if draw_preset == 'coco':
        skeleton = [[15, 13], [13, 11], [16, 14], [14, 12], 
                    [11, 12], [5, 11], [6, 12], [5, 6], 
                    [5, 7], [6, 8], [7, 9], [8, 10], 
                    [1, 2], [0, 1], [0, 2], [1, 3], 
                    [2, 4], [3, 5], [4, 6]]
        
        kpt_color = [[51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                     [51, 153, 255], [0, 255, 0], [255, 128, 0], [0, 255, 0], 
                     [255, 128, 0], [0, 255, 0], [255, 128, 0], [0, 255, 0], 
                     [255, 128, 0], [0, 255, 0], [255, 128, 0], [0, 255, 0], 
                     [255, 128, 0]]
        
        skeleton_color = [[0, 255, 0], [0, 255, 0], [255, 128, 0], [255, 128, 0], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255]]
        
    elif draw_preset == 'sodpose':
        skeleton = [[0, 2], [0, 3], [1, 2], [1, 3], 
                    [2, 4], [3, 5], [0, 6], [6, 7], 
                    [9, 7], [8, 7], [8, 10], [9, 11], 
                    [11, 13], [10, 12], [8, 14], [9, 15], 
                    [15, 16], [14, 16], [19, 17], [17, 14], 
                    [20, 18], [18, 15]]
        
        kpt_color = [[51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                    [51, 153, 255], [51, 153, 255], [51, 153, 255], [128, 128, 255], 
                    [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0], 
                    [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0], 
                    [128, 128, 255], [0, 255, 0], [255, 128, 0], [0, 255, 0], [255, 128, 0]]
        
        skeleton_color = [[51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [0, 255, 0], [255, 128, 0], 
                          [255, 128, 0], [0, 255, 0], [51, 153, 255], [51, 153, 255], 
                          [51, 153, 255], [51, 153, 255], [0, 255, 0], [0, 255, 0], 
                          [255, 128, 0], [255, 128, 0]]
    
    return skeleton, kpt_color, skeleton_color

def draw_pose_in_image(img: np.array, 
                       poses,
                       save_root_dir: str = "./",
                       save_img_name: str = "origin-draw-pose-img.jpg", 
                       RGB2BGR: bool = False,
                       normlization: bool = False,
                       standardization_mean: np.array = None,
                       standardization_std: np.array = None,
                       draw_preset: str = None,
                       skeleton: np.array = None,
                       draw_point_size: int = 1,
                       draw_point_color: tuple = (0, 0, 255),
                       draw_point_thickness: int = 4,
                       draw_skeleton_color: tuple = (0, 255, 0)):
    """draw pose in image and save it in save_dir

    Args:
        img (np.array): img to draw pose
        pose (_type_): pose can be multiple person or single person
        save_dir (_type_): the dir to save the pose image
        dataset_category (dict, optional): dataset_category, it must contain skeleton at least. Defaults to COCO_CATEGORY.
    """
    if normlization:
        img = img * 255
    
    assert img.shape[2] == 3, "the last dimension of img must be 3. It means color channel"
    assert (standardization_mean is None and standardization_std is None) \
        or (standardization_mean is not None and standardization_std is not None), "standardization_mean and standardization_std must be None or not None at the same time"
        
    if standardization_mean is not None and standardization_std is not None:
        img = img * standardization_std + standardization_mean
    
    if RGB2BGR:
        input_tensor = cv2.cvtColor(input_tensor, cv2.COLOR_RGB2BGR)
    
    if len(poses.shape) == 2:
        poses = poses[None, :]
    if poses.shape[2] == 3:
        poses = poses[:, :, :2]
    
    assert draw_preset in ['coco', 'sodpose', None], "draw_preset must be in ['coco', 'sodpose', None]"
    
    if draw_preset:
        skeleton, draw_point_color, draw_skeleton_color = get_draw_preset(draw_preset)
    else:
        assert skeleton is not None, "skeleton must be provided when draw_preset is None"
        
        min_kpt_id = np.min(skeleton.flatten())
        assert min_kpt_id == 1, "the keypoint id must be starting from 0"
        
        if isinstance(draw_point_color, tuple):
            draw_point_color = [draw_point_color for _ in range(poses.shape[1])]
        if isinstance(draw_skeleton_color, tuple):
            draw_skeleton_color = [draw_skeleton_color for _ in range(len(skeleton))]
    
    if not os.path.isdir(save_root_dir):
        # 创建文件夹
        os.makedirs(save_root_dir)
            
    save_img_dir = os.path.join(save_root_dir, save_img_name)

    for _pose in poses:
        for i, (x, y) in enumerate(_pose): # draw keypoints
            if x < 0 or y < 0:
                continue
                
            # 绘制骨架
            cv2.circle(img, (int(x), int(y)), draw_point_size, draw_point_color[i], draw_point_thickness)
            
        for i, (s, e) in enumerate(skeleton): # draw skeleton
            cv2.line(img, (int(_pose[s][0]), int(_pose[s][1])), (int(_pose[e][0]),int(_pose[e][1])), draw_skeleton_color[i]) 
            
    cv2.imwrite(save_img_dir, img)
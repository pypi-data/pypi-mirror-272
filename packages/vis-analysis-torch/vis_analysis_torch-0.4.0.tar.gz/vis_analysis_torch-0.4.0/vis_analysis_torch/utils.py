import numpy as np
import cv2

def convert_mmpose_datasets_info(keypoint_info, skeleton_info):
    # 创建映射字典
    keypoint_id_map = {info['name']: info['id'] for info in keypoint_info.values()}

    kpt_color = []
    for kpt in keypoint_info.values():
        kpt_color.append(kpt['color'])
        
    # 更新 skeleton_info 中的 link
    skeleton = []
    skeleton_color = []
    for link_info in skeleton_info.values():
        skeleton.append([keypoint_id_map[link_info['link'][0]], keypoint_id_map[link_info['link'][1]]])
        skeleton_color.append(link_info['color'])
    
    return skeleton, kpt_color, skeleton_color

def convert_image(img,
                  RGB2BGR: bool = False,
                  normlization: bool = False,
                  standardization_mean: np.array = None,
                  standardization_std: np.array = None,):
    if normlization:
        img = img * 255
    
    assert img.shape[2] == 3, "the last dimension of img must be 3. It means color channel"
    assert (standardization_mean is None and standardization_std is None) \
        or (standardization_mean is not None and standardization_std is not None), "standardization_mean and standardization_std must be None or not None at the same time"
        
    if standardization_mean is not None and standardization_std is not None:
        img = img * standardization_std + standardization_mean
    
    if RGB2BGR:
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
    return img
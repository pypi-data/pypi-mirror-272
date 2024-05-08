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
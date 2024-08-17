import os
import json
from collections import defaultdict
import re
import random

def extract_filename(file_path):
    match = re.search(r'([^/]+\.pdf)$', file_path)
    if match:
        return match.group(1)
    else:
        return None

def is_bbox_valid(bbox, max_size=1000):
    return all(coord <= max_size for coord in bbox)

def update_json_files(json_dir, output_train_dir, output_dev_dir, output_test_dir):
    # JSON 파일 목록 가져오기
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    random.shuffle(json_files)  # 파일을 랜덤하게 섞기
    
    # 비율에 맞게 파일을 분할
    total_files = len(json_files)
    train_files = json_files[:int(total_files * 0.8)]
    dev_files = json_files[int(total_files * 0.8):int(total_files * 0.9)]
    test_files = json_files[int(total_files * 0.9):]

    def process_files(files, output_dir):
        for json_file in files:
            json_path = os.path.join(json_dir, json_file)
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            bbox_lst = []
            text_lst = []
            page = 1
            for element in data['elements']:
                bounding_box = element['bounding_box']
                selected_bbox = [int(bounding_box[0]['x']/4), int(bounding_box[0]['y']/4), int(bounding_box[2]['x']/4), int(bounding_box[2]['y']/4)]
                
                # if not is_bbox_valid(selected_bbox):
                #     continue
                
                if element['page'] == page:
                    bbox_lst.append(selected_bbox)
                    text_lst.append(element['text'])
                else:
                    layout_data = {
                        'tgt': bbox_lst
                    }
                    text_data = {
                        'tgt': text_lst
                    }
                    name = extract_filename(data['pdf_path']).split('.')[0]
                    name = name + str(page)
                    output_layout_path = os.path.join(output_dir, f"{name}_layout.json")
                    output_text_path = os.path.join(output_dir, f"{name}_text.json")
                    with open(output_layout_path, 'w', encoding='utf-8') as f:
                        json.dump(layout_data, f, ensure_ascii=False, indent=4)
                    with open(output_text_path, 'w', encoding='utf-8') as f:
                        json.dump(text_data, f, ensure_ascii=False, indent=4)
                    
                    page += 1
                    bbox_lst = []
                    text_lst = []
                    if is_bbox_valid(selected_bbox):
                        bbox_lst.append(selected_bbox)
                        text_lst.append(element['text'])
                    
        print("Updated JSON file saved")

    # 각 디렉토리에서 파일 처리
    process_files(train_files, output_train_dir)
    process_files(dev_files, output_dev_dir)
    process_files(test_files, output_test_dir)

# 경로 설정
json_directory = '/root/YOSO/data_1/json'
output_train_directory = '/root/YOSO/data/train'
output_dev_directory = '/root/YOSO/data/dev'
output_test_directory = '/root/YOSO/data/test'

# 출력 디렉토리 생성
os.makedirs(output_train_directory, exist_ok=True)
os.makedirs(output_dev_directory, exist_ok=True)
os.makedirs(output_test_directory, exist_ok=True)

# JSON 파일 업데이트
update_json_files(json_directory, output_train_directory, output_dev_directory, output_test_directory)

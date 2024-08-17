import os
import json
from collections import defaultdict
import re

def extract_filename(file_path):
    # 정규식을 사용하여 파일 이름 추출
    match = re.search(r'([^/]+\.pdf)$', file_path)
    if match:
        return match.group(1)
    else:
        return None

def update_json_files(json_dir, output_dir):
    # JSON 파일 목록 가져오기
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    for json_file in json_files:
        json_path = os.path.join(json_dir, json_file)
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 페이지별 텍스트 블록 정리
        elements_by_page = defaultdict(list)
        name = extract_filename(data['pdf_path']).split('.')
        name = name[0]
        for element in data['elements']:
            
            page = element['page']
            bounding_box = element['bounding_box']
            # 각 bounding box에서 첫 번째와 세 번째 좌표만 가져오기
            selected_bbox = [bounding_box[0]['x'], bounding_box[0]['y'], bounding_box[2]['x'], bounding_box[2]['y']]
            elements_by_page[page].append(selected_bbox)
        
        # JSON 파일 이름에서 확장자 제거
        base_name = os.path.splitext(json_file)[0]

        # 각 페이지별로 JSON 파일 저장
        for page, bboxes in elements_by_page.items():
            new_data = {'src': bboxes}
            output_path = os.path.join(output_dir, f"{name}_{page}.json")
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
            
            print(f"Updated JSON file saved to: {output_path}")

# 경로 설정
json_directory = '/root/YOSO/data/json'
output_directory = '/root/YOSO/data/separated_json'

# 출력 디렉토리 생성
os.makedirs(output_directory, exist_ok=True)

# JSON 파일 업데이트
update_json_files(json_directory, output_directory)

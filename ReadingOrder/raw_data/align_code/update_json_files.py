import os
import json
from collections import defaultdict

def update_json_files(json_dir, pdf_dir, output_dir):
    # JSON 파일 목록 가져오기
    json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

    for json_file in json_files:
        json_path = os.path.join(json_dir, json_file)
        
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # PDF 경로 수정
        pdf_name = os.path.basename(data['pdf_path'])
        correct_pdf_path = os.path.join(pdf_dir, pdf_name)
        data['pdf_path'] = correct_pdf_path

        # 페이지별 텍스트 블록 정리
        elements_by_page = defaultdict(list)
        for element in data['elements']:
            elements_by_page[element['page']].append(element)

        new_elements = []
        for page in sorted(elements_by_page.keys()):
            page_elements = elements_by_page[page]
            page_elements = sorted(page_elements, key=lambda x: x['id'])  # ID 순서로 정렬
            new_elements.extend(page_elements)

        data['elements'] = new_elements

        # 수정된 JSON 파일 저장
        output_path = os.path.join(output_dir, json_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print(f"Updated JSON file saved to: {output_path}")

# 경로 설정
json_directory = '/root/data/json'
pdf_directory = '/root/data/pdf'
output_directory = '/root/data/updated_json'

# 출력 디렉토리 생성
os.makedirs(output_directory, exist_ok=True)

# JSON 파일 업데이트
update_json_files(json_directory, pdf_directory, output_directory)

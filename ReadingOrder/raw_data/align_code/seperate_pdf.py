import fitz  # PyMuPDF
import os

def split_pdf(pdf_dir, output_dir):
    pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_dir, pdf_file)
        pdf_document = fitz.open(pdf_path)
        base_name = os.path.basename(pdf_path).replace('.pdf', '')

        for page_num in range(len(pdf_document)):
            # 각 페이지를 새로운 PDF로 저장
            output_path = os.path.join(output_dir, f"{base_name}_{page_num + 1}.pdf")
            pdf_writer = fitz.open()  # 빈 PDF 생성
            pdf_writer.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            pdf_writer.save(output_path)
            pdf_writer.close()

            print(f"Saved {output_path}")

# 경로 설정
pdf_directory = "/root/YOSO/data/pdf"
output_directory = "/root/YOSO/data/pdf/split_pages"

# 출력 디렉토리 생성
os.makedirs(output_directory, exist_ok=True)

# PDF 파일 분할
split_pdf(pdf_directory, output_directory)

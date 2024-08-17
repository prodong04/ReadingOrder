import fitz  # PyMuPDF
import cv2
import pandas as pd
from PIL import Image

def pdf_page_to_image(pdf_path, page_number):
    document = fitz.open(pdf_path)
    page = document.load_page(page_number)
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    img_path = pdf_path.replace('.pdf', f'_page_{page_number}.png')
    img.save(img_path)
    return img_path

def draw_bounding_boxes(image_path):
    # 글로벌 변수
    drawing = False
    ix, iy = -1, -1
    boxes = []

    # 마우스 콜백 함수
    def draw_rectangle(event, x, y, flags, param):
        nonlocal ix, iy, drawing, img, boxes

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing == True:
                img_copy = img.copy()
                cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)
                cv2.imshow('image', img_copy)

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            cv2.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)
            boxes.append((ix, iy, x, y))

    # 이미지 로드
    img = cv2.imread(image_path)
    cv2.namedWindow('image')
    cv2.setMouseCallback('image', draw_rectangle)

    while True:
        cv2.imshow('image', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

    # 바운딩 박스 정보 저장
    data = [{'x1': box[0], 'y1': box[1], 'x2': box[2], 'y2': box[3]} for box in boxes]
    print
    df = pd.DataFrame(data)
    csv_path = image_path.replace('.png', '_annotations.csv')
    df.to_csv(csv_path, index=False)

# PDF 파일의 첫 번째 페이지를 이미지로 변환
pdf_paths = ['/root/YOSO/layoutreader/2407.09557v1.pdf', '/root/YOSO/layoutreader/retrieve.pdf']
for pdf_path in pdf_paths:
    image_path = pdf_page_to_image(pdf_path, 0)
    draw_bounding_boxes(image_path)

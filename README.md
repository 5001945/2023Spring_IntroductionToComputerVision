# 2023년 1학기 컴퓨터비전의 기초 파이널 프로젝트

## 개요
문서 사진을 찍어 텍스트 기반 pdf로 변환하는 프로그램

## 라이브러리 의존성
기본적으로 requirements.yml에 나와 있으나, 아래 코드를 실행해도 된다.
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia  # from pytorch official webpage  
conda install matplotlib  
pip install easyocr  
pip install fpdf2  
pip install pyside6  
pip install pandas  
pip install ipykernel  # for VS code  
```

## 실행 방법
다음 중 하나를 사용하면 된다.  

1. GUI 없이 실행하기  
`python no_gui.py -i "input_file.jpg" -o "output_file.pdf"` 명령을 통해 실행하면 된다.  

2. Jupyter Notebook을 통해 실행하기  
`get_a4.ipynb`, `ocr.ipynb`, `make_pdf.ipynb` 순서로 실행하면 된다.  
make_pdf의 경우 ocr에서 나온 results 및 each_fonts 리스트가 필요하다.  

3. GUI로 실행하기  
`python mainwindow.py` 명령을 통해 실행하면 된다.

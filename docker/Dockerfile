FROM ubuntu:latest
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt update && apt install -y libsm6 libxext6
RUN apt-get -y install tesseract-ocr
RUN mkdir -p /work_dir
WORKDIR /work_dir
COPY /assignment_mycujoo-0.0.1.tar.gz /work_dir
RUN pip install pillow
RUN pip install pytesseract
RUN pip install opencv-contrib-python
RUN pip install assignment_mycujoo-0.0.1.tar.gz
CMD [ "run_assignment_mycujoo"]

FROM python:3.9

WORKDIR /home/vector/vsCode/Jigglypuff
COPY . . 

RUN pip install -r requirements.txt

CMD ["python", "youtube_viewer.py"] 
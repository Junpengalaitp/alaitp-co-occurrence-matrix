FROM python:3.7.8-slim-buster
WORKDIR /project
ADD . /project
RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt
CMD ["python", "matrix_app.py"]
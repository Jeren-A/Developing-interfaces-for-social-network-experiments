FROM ubuntu:latest
RUN apt update
RUN apt install python3 python3-pip -y
RUN pip3 install -r requirements.txt
COPY . /app
CMD streamlit run /app/main.py
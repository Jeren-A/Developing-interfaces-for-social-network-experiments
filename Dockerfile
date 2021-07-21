FROM ubuntu:latest
RUN apt update
RUN apt install python3 python3-pip -y
RUN pip3 install streamlit pandas numpy
COPY . /app
CMD streamlit run /app/main.py
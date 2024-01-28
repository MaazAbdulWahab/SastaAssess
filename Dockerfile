FROM python:3.11   
 
RUN mkdir -p /app 
 
WORKDIR /app
 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
 

COPY . /app/ 
# run this command to install all dependencies  
RUN pip install -r requirements.txt  
# port where the Django app runs  
EXPOSE 8000
# Base image
FROM python:latest

# Copy data acquisition files
COPY influencer_news /influencer_news
RUN mkdir -p influencer_news/logs
WORKDIR /influencer_news

# Install requirement
RUN pip install -r requirements.txt

# Start main python script
CMD ["python","-u","main.py"]

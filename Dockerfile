# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.12-slim-bullseye

# Set Working Directory
WORKDIR /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
ENV LOG_PATH="logs"
ENV LOG_CONFIG="console+file"

# DEBUG
ENV VERSION="2.0"
ENV STATUS="awakens from the sky!"
ENV DEBUG=0

#DISCORD

ENV WEATHER_CHANNEL=824015500819955722
ENV GENERAL_CHANNEL=975762159017545809
ENV ERROR_CHANNEL=1216925208967909516

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["python", "polaris/bot.py"]

FROM python:3.8-slim

RUN apt-get update

# Copy local files to docker image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip
RUN pip install --upgrade pip

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8080

# Download model.
CMD ["python", "download_model.py"]

# Run the app.
CMD ["streamlit", "run", "--server.headless=true", "--server.port=8080", "app.py"]

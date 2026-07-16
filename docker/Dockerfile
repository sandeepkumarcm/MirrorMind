FROM python:3.10-slim

WORKDIR /app

# System dependencies:
# - ffmpeg: required by Whisper
# - libgl1, libglib2.0-0, libsm6, libxext6: required by OpenCV/MediaPipe
# - portaudio19-dev, libportaudio2: required by sounddevice
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    portaudio19-dev \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir setuptools==69.5.1 wheel==0.45.1 && \
    pip install --no-cache-dir --no-build-isolation -r requirements.txt

COPY . .

EXPOSE 8000 8501

COPY docker/start.sh /app/start.sh
RUN sed -i 's/\r$//' /app/start.sh && chmod +x /app/start.sh

CMD ["bash", "/app/start.sh"]
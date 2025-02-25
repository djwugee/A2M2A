# Use an official Python base image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libasound2-dev \
    libjack-jackd2-dev \
    fluidsynth \
    ffmpeg \
    wget \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    flask \
    magenta \
    midi2audio

# Set working directory
WORKDIR /app

# Create necessary directories
RUN mkdir -p uploads output soundfonts

# Download and add a default SoundFont
RUN wget https://github.com/FluidSynth/fluidsynth-soundfonts/raw/master/FluidR3_GM.sf2 -O /app/soundfonts/FluidR3_GM.sf2

# Copy application files into the container
COPY . /app/

# Expose the Flask port
EXPOSE 5000

# Set environment variable for the SoundFont path
ENV SOUNDFONT_PATH=/app/soundfonts/FluidR3_GM.sf2

# Run the Flask application
CMD ["python", "app.py"]

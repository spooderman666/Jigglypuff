# Kali linux base image
FROM kalilinux/kali-rolling

# Base directory to copy files
WORKDIR /home/vector/vsCode/Jigglypuff

# Update and install dependencies, # Add Xvfb for virtual framebuffer (if using headless mode)
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3.12-venv \
    python3-pip \
    firefox-esr \
    wget \
    curl \
    unzip \
    sudo \
    x11-utils \
    gnupg2 \
    ca-certificates \
    libx11-xcb1 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libgtk-3-0 \
    libasound2 \
    libgdk-pixbuf2.0-0 \
    libpangocairo-1.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libdbus-glib-1-2 \
    libxtst6 \
    libnspr4 \
    xvfb \
    && rm -rf /var/lib/apt/lists/*
    
# Install geckodriver and copy files
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar -xzf /tmp/geckodriver.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver
COPY . .

# Create a virtual environment with dependencies and set environment file path
RUN /usr/bin/python3 -m venv /home/vector/vsCode/Jigglypuff/venv
RUN /home/vector/vsCode/Jigglypuff/venv/bin/pip3 install --no-cache-dir --upgrade pip
RUN /home/vector/vsCode/Jigglypuff/venv/bin/pip3 install -r /home/vector/vsCode/Jigglypuff/requirements.txt
ENV PATH="/home/vector/vsCode/Jigglypuff/venv/bin:$PATH"
# Assuming Xvfb is used with DISPLAY :99
ENV DISPLAY=:99  

# Start the python script
CMD ["xvfb-run", "-a", "/home/vector/vsCode/Jigglypuff/venv/bin/python3", "youtube_viewer.py"]
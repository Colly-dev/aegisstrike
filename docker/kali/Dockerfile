FROM kalilinux/kali-rolling:latest

LABEL maintainer="AegisStrike"
LABEL description="AegisStrike - Elite Reconnaissance & Automated Pentesting Framework"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    nmap \
    gobuster \
    git \
    curl \
    wget \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /opt/aegisstrike

# Copy project files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Create output directories
RUN mkdir -p reports/html reports/json reports/csv logs databases

# Set entrypoint
ENTRYPOINT ["python3", "aegisstrike.py"]
CMD ["--help"]

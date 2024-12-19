FROM ubuntu:18.04

# Update and install necessary packages
RUN apt-get update -y                                                   \
    && apt-get upgrade -y                                               \
    && apt-get install -y wget build-essential python3-pip python3-venv htop screen

# Set the working directory
WORKDIR /media/ecommerce_analytics

# Copy requirements.txt
COPY requirements.txt .

# Create and activate a virtual environment
RUN python3 -m venv /media/ecommerce_analytics/venv                     \
    && . /media/ecommerce_analytics/venv/bin/activate                   \
    && pip install --upgrade pip                                        \
    && pip install -r requirements.txt

# Add the virtual environment to PATH for subsequent commands
ENV PATH="/media/ecommerce_analytics/venv/bin:$PATH"

# Default command
CMD ["bash"]
FROM ubuntu:20.04

RUN apt-get update -y                                                   \
&& apt-get upgrade -y                                                   \
&&  apt-get install -y wget build-essential python3-pip htop screen

# Download Miniconda
RUN wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-aarch64.sh
RUN chmod +x Miniforge3-Linux-aarch64.sh

# Install Miniconda
RUN bash Miniforge3-Linux-aarch64.sh -b
ENV PATH="/root/miniforge3/bin:$PATH"

# Update Conda and clean up
RUN /root/miniforge3/bin/conda update conda -y \
    && /root/miniforge3/bin/conda clean --all --yes

# Cleanup installer
RUN rm Miniforge3-Linux-aarch64.sh

# -----------------------------------------------------------------------------

WORKDIR /media/ecommerce_analytics

# Copy conda env
COPY environment.yml .

# Create environment
RUN /root/miniforge3/bin/conda env create --file environment.yml

# Initialize Conda for bash
RUN echo "source /root/miniforge3/bin/activate" >> ~/.bashrc

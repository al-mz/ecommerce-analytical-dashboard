FROM ubuntu:18.04

RUN apt-get update -y                                                   \
&& apt-get upgrade -y                                                   \
&&  apt-get install -y wget build-essential python3-pip htop screen

# Download Miniconda
RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Install Miniconda
RUN bash Miniconda3-latest-Linux-x86_64.sh -b
ENV PATH=/root/miniconda3/bin:${PATH} 
RUN conda update conda \
    && conda clean --all --yes

# Cleanup
RUN rm Miniconda3-latest-Linux-x86_64.sh

# -----------------------------------------------------------------------------

WORKDIR /media/ecommerce_analytics

# Copy conda env
COPY environment.yml .

# Create environment
RUN conda env create --file environment.yml

RUN conda init bash
# Start from the NVIDIA CUDA image with Python support
FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu20.04

# Set the working directory in the container
WORKDIR /app

# Install Python, pip, and virtualenv with specific versions
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3=3.8.2-0ubuntu2~20.04 \
    python3-pip=20.0.2-5ubuntu1.10 \
    python3-venv=3.8.2-0ubuntu2 \
 && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip to a specific version in the virtual environment
RUN pip install --upgrade pip==21.2.4

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies from a requirements file with pip version pinning
RUN pip install -r requirements.txt

# Make sure the appuser owns the application directory
RUN useradd -m appuser && chown -R appuser /app

USER appuser

# Copy the GPU metrics script into the container
COPY --chown=appuser:appuser gpu_metrics.py /app/

# Expose port 8888
EXPOSE 8888

# Command to run the script
CMD ["python3", "gpu_metrics.py"]

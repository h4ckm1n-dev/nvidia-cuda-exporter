# Start from the NVIDIA CUDA image with Python support
FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu20.04

# Set the working directory in the container
WORKDIR /app

# Install Python, pip, and virtualenv
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-venv \
 && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip in the virtual environment
RUN pip install --upgrade pip

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies
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

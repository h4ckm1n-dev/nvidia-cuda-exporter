# Start from the NVIDIA CUDA image with Python support
FROM nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu20.04

# Set the working directory in the container
WORKDIR /app

# Install Python, pip, and virtualenv
RUN apt-get update && apt-get install -y --no-install-recommends \
  python3=3.8.1 \
  python3-pip=20.0.2-5ubuntu1.6 \
  python3-venv=3.8.1 \
  && rm -rf /var/lib/apt/lists/*

# Create a virtual environment and activate it
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip in the virtual environment to a specific version, avoiding cache
RUN pip install --upgrade --no-cache-dir pip==22.0.4

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install dependencies with specific versions, avoiding cache
RUN pip install --no-cache-dir -r requirements.txt

# Make sure the appuser owns the application directory
RUN useradd -m appuser && chown -R appuser /app

USER appuser

# Copy the GPU metrics script into the container with appropriate ownership
COPY --chown=appuser:appuser gpu_metrics.py /app/

# Expose port 8888
EXPOSE 8888

# Command to run the script
CMD ["python3", "gpu_metrics.py"]


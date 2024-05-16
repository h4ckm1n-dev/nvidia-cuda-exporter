# NVIDIA-CUDA-EXPORTER
![Capture d’écran du 2024-03-13 00-32-20](https://github.com/h4ckm1n-dev/nvidia-cuda-exporter/assets/97511408/862cdf48-c1c5-42e5-bb77-f2f683e88159)

[Github Page Link](https://github.com/h4ckm1n-dev/nvidia-cuda-exporter.git)
## Overview

This README provides comprehensive information about the project, including its purpose, usage instructions, and configuration details.

## Dockerized Python Application with NVIDIA CUDA Support

### Dockerfile

The Dockerfile sets up a Docker image for running a Python application that utilizes NVIDIA CUDA for GPU computation. It includes the following steps:

- Starts from the NVIDIA CUDA image with Python support (`nvidia/cuda:12.3.2-cudnn9-runtime-ubuntu20.04`).
- Installs Python, pip, and virtualenv.
- Creates a virtual environment and activates it.
- Upgrades pip in the virtual environment.
- Copies the `requirements.txt` file into the container and installs dependencies.
- Makes sure the `appuser` owns the application directory.
- Copies the `gpu_metrics.py` script into the container.
- Exposes port 8888.
- Specifies the command to run the script (`CMD ["python3", "gpu_metrics.py"]`).

### Usage

To use the Docker image:

1. Clone or download the repository containing the Dockerfile and other necessary files.
2. Build the Docker image:
```
docker build -t nvidia-cuda-exporter .
```
4. Run a Docker container based on the image:
```
docker run --name nvidia-cuda-exporter --gpus all -p 8888:8888 -v /usr/local/nvidia:/usr/local/nvidia nvidia-cuda-exporter
```
6. Access the Python application through a web browser or programmatically: `http://localhost:<host-port>`

Replace `<host-port>` with the desired port on your host machine.

## NVIDIA GPU Metrics Collector

### Python Script

The `gpu_metrics_collector.py` script collects GPU metrics using NVIDIA Management Library (NVML) and exposes them as Prometheus metrics via an HTTP server. It includes the following functionality:

- Collects various GPU metrics such as memory usage, utilization, temperature, power usage, fan speed, clock speeds, PCIe transmission speed, and more.
- Exposes the metrics at `http://localhost:8888/metrics`.

### Usage

To use the script:

1. Clone or download the repository containing the script.
2. Install the required dependencies: `pip install prometheus_client pynvml`
3. Run the script: `python gpu_metrics_collector.py`

Access the metrics at `http://localhost:8888/metrics`.

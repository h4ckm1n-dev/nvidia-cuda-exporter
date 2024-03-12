# Project README

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
2. Build the Docker image: `docker build -t cuda-python-app .`
3. Run a Docker container based on the image: `docker run --gpus all -p <host-port>:8888 cuda-python-app`
4. Access the Python application through a web browser or programmatically: `http://localhost:<host-port>`

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

## Dependency Management Configuration

### JSON Configuration File

The JSON configuration file defines rules for managing dependencies using renovate management tool. It specifies how updates to Dockerfile dependencies and pip requirements should be handled.

```json
{
  "extends": ["config:base"],
  "packageRules": [
    {
      "matchDatasources": ["docker"],
      "matchUpdateTypes": ["major", "minor", "patch"],
      "matchManagers": ["dockerfile"],
      "dependencyDashboard": true
    },
    {
      "matchManagers": ["pip_requirements"],
      "matchPackagePatterns": ["*"],
      "dependencyDashboard": true
    }
  ]
}

### Usage

To use the configuration file:

Copy the provided JSON configuration into a file named dependency-management.json or any other appropriate name.
Place the configuration file in the root directory of your project.
Configure your dependency management tool to use this configuration file for managing dependencies.
For further details on how to configure and use the dependency management tool with this configuration file, refer to the documentation of the specific tool being used.

Additional Information
For any further information or issues, please consult the documentation of the respective components or tools used in the project.
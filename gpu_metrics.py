from prometheus_client import start_http_server, Gauge
import time
import pynvml

# Initialize NVML
pynvml.nvmlInit()

# Define Prometheus metrics
gpu_memory_total = Gauge('gpu_memory_total_mb', 'Total GPU memory in MB', ['gpu_index', 'gpu_name'])
gpu_memory_used = Gauge('gpu_memory_used_mb', 'Used GPU memory in MB', ['gpu_index', 'gpu_name'])
gpu_memory_free = Gauge('gpu_memory_free_mb', 'Free GPU memory in MB', ['gpu_index', 'gpu_name'])
gpu_memory_used_percentage = Gauge('gpu_memory_used_percent', 'Percentage of GPU memory used', ['gpu_index', 'gpu_name'])
gpu_utilization_gpu = Gauge('gpu_utilization_gpu_percent', 'GPU utilization in percent', ['gpu_index', 'gpu_name'])
gpu_utilization_memory = Gauge('gpu_utilization_memory_percent', 'Memory utilization in percent', ['gpu_index', 'gpu_name'])
gpu_temperature = Gauge('gpu_temperature_celsius', 'GPU temperature in Celsius', ['gpu_index', 'gpu_name'])
gpu_power_usage = Gauge('gpu_power_usage_watts', 'GPU power usage in watts', ['gpu_index', 'gpu_name'])
gpu_fan_speed = Gauge('gpu_fan_speed_percent', 'GPU fan speed in percent', ['gpu_index', 'gpu_name'])
gpu_clock_graphics = Gauge('gpu_clock_graphics_mhz', 'GPU graphics clock speed in MHz', ['gpu_index', 'gpu_name'])
gpu_max_clock_graphics = Gauge('gpu_max_clock_graphics_mhz', 'GPU maximum graphics clock speed in MHz', ['gpu_index', 'gpu_name'])
gpu_clock_memory = Gauge('gpu_clock_memory_mhz', 'GPU memory clock speed in MHz', ['gpu_index', 'gpu_name'])
gpu_max_clock_memory = Gauge('gpu_max_clock_memory_mhz', 'GPU maximum memory clock speed in MHz', ['gpu_index', 'gpu_name'])
gpu_memory_bus_width = Gauge('gpu_memory_bus_width_bits', 'GPU memory bus width in bits', ['gpu_index', 'gpu_name'])
gpu_max_memory_bandwidth = Gauge('gpu_max_memory_bandwidth_gb_per_s', 'GPU maximum memory bandwidth in GB/s', ['gpu_index', 'gpu_name'])
gpu_l2_cache_size = Gauge('gpu_l2_cache_size_mb', 'GPU L2 cache size in MB', ['gpu_index', 'gpu_name'])
gpu_core_voltage = Gauge('gpu_core_voltage_mv', 'GPU core voltage in millivolts', ['gpu_index', 'gpu_name'])
gpu_gpu_utilization_memory_copy = Gauge('gpu_utilization_memory_copy_percent', 'Memory copy engine utilization in percent', ['gpu_index', 'gpu_name'])
gpu_gpu_utilization_compute = Gauge('gpu_utilization_compute_percent', 'Compute engine utilization in percent', ['gpu_index', 'gpu_name'])
gpu_gpu_utilization_dma = Gauge('gpu_utilization_dma_percent', 'DMA engine utilization in percent', ['gpu_index', 'gpu_name'])
gpu_gpu_utilization_video_encode = Gauge('gpu_utilization_video_encode_percent', 'Video encode engine utilization in percent', ['gpu_index', 'gpu_name'])
gpu_gpu_utilization_video_decode = Gauge('gpu_utilization_video_decode_percent', 'Video decode engine utilization in percent', ['gpu_index', 'gpu_name'])
cuda_version = Gauge('cuda_version', 'CUDA version')
cuda_cores_used = Gauge('cuda_cores_used_percent', 'Percentage of CUDA cores used', ['gpu_index', 'gpu_name'])
cuda_cores_total = Gauge('cuda_cores_total', 'Total number of CUDA cores', ['gpu_index', 'gpu_name'])
memory_free = Gauge('memory_free_mb', 'Free system memory in MB')
memory_total = Gauge('memory_total_mb', 'Total system memory in MB')
gpu_pcie_tx = Gauge('gpu_pcie_tx_mb', 'GPU PCIe transmission speed in MB/s', ['gpu_index', 'gpu_name'])
gpu_pcie_rx = Gauge('gpu_pcie_rx_mb', 'GPU PCIe receive speed in MB/s', ['gpu_index', 'gpu_name'])
gpu_power_limit = Gauge('gpu_power_limit_watts', 'GPU power limit in watts', ['gpu_index', 'gpu_name'])
gpu_power_draw = Gauge('gpu_power_draw_watts', 'GPU power draw in watts', ['gpu_index', 'gpu_name'])
gpu_power_usage_percent = Gauge('gpu_power_usage_percent', 'GPU power usage percentage of the power limit', ['gpu_index', 'gpu_name'])
gpu_encoder_utilization = Gauge('gpu_encoder_utilization_percent', 'GPU encoder utilization in percent', ['gpu_index', 'gpu_name'])
gpu_decoder_utilization = Gauge('gpu_decoder_utilization_percent', 'GPU decoder utilization in percent', ['gpu_index', 'gpu_name'])
gpu_compute_mode = Gauge('gpu_compute_mode', 'GPU compute mode', ['gpu_index', 'gpu_name'])

def collect_gpu_metrics():
    device_count = pynvml.nvmlDeviceGetCount()
    for i in range(device_count):
        handle = pynvml.nvmlDeviceGetHandleByIndex(i)
        gpu_name = pynvml.nvmlDeviceGetName(handle)
        memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
        utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
        temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
        power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0  # Convert to Watts
        fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
        clock_graphics = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
        max_clock_graphics = pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_GRAPHICS)
        clock_memory = pynvml.nvmlDeviceGetClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        max_clock_memory = pynvml.nvmlDeviceGetMaxClockInfo(handle, pynvml.NVML_CLOCK_MEM)
        encoder_utilization, _ = pynvml.nvmlDeviceGetEncoderUtilization(handle)
        decoder_utilization, _ = pynvml.nvmlDeviceGetDecoderUtilization(handle)
        compute_mode = pynvml.nvmlDeviceGetComputeMode(handle)

        cuda_version_value = pynvml.nvmlSystemGetCudaDriverVersion()
        cuda_version.set(cuda_version_value)

        cuda_cores_info = pynvml.nvmlDeviceGetCudaComputeCapability(handle)
        cuda_cores_total_count = cuda_cores_info[0] * cuda_cores_info[1]
        cuda_cores_total.labels(gpu_index=str(i), gpu_name=gpu_name).set(cuda_cores_total_count)

        cuda_cores_used_percent = (utilization.gpu / 100.0) * cuda_cores_total_count
        cuda_cores_used.labels(gpu_index=str(i), gpu_name=gpu_name).set(cuda_cores_used_percent)

        labels = {'gpu_index': str(i), 'gpu_name': gpu_name}

        gpu_memory_total.labels(**labels).set(memory_info.total / (1024**2))
        gpu_memory_used.labels(**labels).set(memory_info.used / (1024**2))
        gpu_memory_free.labels(**labels).set(memory_info.free / (1024**2))
        gpu_memory_used_percentage.labels(**labels).set((memory_info.used / memory_info.total) * 100)
        gpu_utilization_gpu.labels(**labels).set(utilization.gpu)
        gpu_utilization_memory.labels(**labels).set(utilization.memory)
        gpu_temperature.labels(**labels).set(temperature)
        gpu_power_usage.labels(**labels).set(power_usage)
        gpu_fan_speed.labels(**labels).set(fan_speed)
        gpu_clock_graphics.labels(**labels).set(clock_graphics)
        gpu_max_clock_graphics.labels(**labels).set(max_clock_graphics)
        gpu_clock_memory.labels(**labels).set(clock_memory)
        gpu_max_clock_memory.labels(**labels).set(max_clock_memory)
        gpu_encoder_utilization.labels(**labels).set(encoder_utilization)
        gpu_decoder_utilization.labels(**labels).set(decoder_utilization)
        gpu_compute_mode.labels(**labels).set(compute_mode)
        
        pci_throughput_tx = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_TX_BYTES)
        pci_throughput_rx = pynvml.nvmlDeviceGetPcieThroughput(handle, pynvml.NVML_PCIE_UTIL_RX_BYTES)
        gpu_pcie_tx.labels(**labels).set(pci_throughput_tx)
        gpu_pcie_rx.labels(**labels).set(pci_throughput_rx)

        power_limit = pynvml.nvmlDeviceGetPowerManagementLimit(handle)
        gpu_power_limit.labels(**labels).set(power_limit)
        power_draw = pynvml.nvmlDeviceGetPowerUsage(handle)
        gpu_power_draw.labels(**labels).set(power_draw)
        power_usage = (power_draw / power_limit) * 100.0  # percentage of power limit used
        gpu_power_usage_percent.labels(**labels).set(power_usage)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8888)
    # Generate some requests.
    while True:
        collect_gpu_metrics()
        time.sleep(10)

from prometheus_client import start_http_server, Gauge
import time
import pynvml

# Initialize NVML
pynvml.nvmlInit()

# Define Prometheus metrics
gpu_memory_total = Gauge('gpu_memory_total_mb', 'Total GPU memory in MB', ['gpu_index', 'gpu_name'])
gpu_memory_used = Gauge('gpu_memory_used_mb', 'Used GPU memory in MB', ['gpu_index', 'gpu_name'])
gpu_utilization_gpu = Gauge('gpu_utilization_gpu_percent', 'GPU utilization in percent', ['gpu_index', 'gpu_name'])
gpu_utilization_memory = Gauge('gpu_utilization_memory_percent', 'Memory utilization in percent', ['gpu_index', 'gpu_name'])
gpu_temperature = Gauge('gpu_temperature_celsius', 'GPU temperature in Celsius', ['gpu_index', 'gpu_name'])
gpu_power_usage = Gauge('gpu_power_usage_watts', 'GPU power usage in watts', ['gpu_index', 'gpu_name'])
gpu_fan_speed = Gauge('gpu_fan_speed_percent', 'GPU fan speed in percent', ['gpu_index', 'gpu_name'])
gpu_clock_graphics = Gauge('gpu_clock_graphics_mhz', 'GPU graphics clock speed in MHz', ['gpu_index', 'gpu_name'])
gpu_max_clock_graphics = Gauge('gpu_max_clock_graphics_mhz', 'GPU maximum graphics clock speed in MHz', ['gpu_index', 'gpu_name'])
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
        encoder_utilization, _ = pynvml.nvmlDeviceGetEncoderUtilization(handle)
        decoder_utilization, _ = pynvml.nvmlDeviceGetDecoderUtilization(handle)
        compute_mode = pynvml.nvmlDeviceGetComputeMode(handle)

        labels = {'gpu_index': str(i), 'gpu_name': gpu_name}

        gpu_memory_total.labels(**labels).set(memory_info.total / (1024**2))
        gpu_memory_used.labels(**labels).set(memory_info.used / (1024**2))
        gpu_utilization_gpu.labels(**labels).set(utilization.gpu)
        gpu_utilization_memory.labels(**labels).set(utilization.memory)
        gpu_temperature.labels(**labels).set(temperature)
        gpu_power_usage.labels(**labels).set(power_usage)
        gpu_fan_speed.labels(**labels).set(fan_speed)
        gpu_clock_graphics.labels(**labels).set(clock_graphics)
        gpu_max_clock_graphics.labels(**labels).set(max_clock_graphics)
        gpu_encoder_utilization.labels(**labels).set(encoder_utilization)
        gpu_decoder_utilization.labels(**labels).set(decoder_utilization)
        gpu_compute_mode.labels(**labels).set(compute_mode)

if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8888)
    # Generate some requests.
    while True:
        collect_gpu_metrics()
        time.sleep(10)

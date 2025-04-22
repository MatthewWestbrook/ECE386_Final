import subprocess

# gpioinfo | grep 105
# Find name for GPIO01
result = subprocess.run(['pgioinfo', '|', 'grep', '105'], capture_output=True, text=True)


# line 105: "PQ.05" unused input active-high


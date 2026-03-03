import subprocess
import sys

if __name__ == "__main__":
    result = subprocess.run([sys.executable, "-m", "pytest", "-v"])
    sys.exit(result.returncode)
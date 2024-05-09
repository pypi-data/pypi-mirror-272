import subprocess
import sys
from tqdm import tqdm

def upgrade_medicafe(package):
    try:
        with tqdm(total=100, desc="Upgrading %s" % package, unit="%") as progress_bar:
            # Capture both stdout and stderr
            process = subprocess.Popen([sys.executable, '-m', 'pip', 'install', '--upgrade', package, '--no-cache-dir', '--disable-pip-version-check', '--no-deps'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            
            if process.returncode != 0:
                # If the return code is non-zero, print error details
                print("Error: Upgrade failed. Details:")
                print("stdout:", stdout)
                print("stderr:", stderr)
                sys.exit(1)
            
            print("stdout:", stdout)
            progress_bar.update(100 - progress_bar.n)
    except Exception as e:
        # Log any other exceptions
        print("Error:", e)
        sys.exit(1)

if __name__ == "__main__":
    medicafe_package = "medicafe"
    upgrade_medicafe(medicafe_package)
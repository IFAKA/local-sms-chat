"""Device management utilities."""
import subprocess
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class DeviceManager:
    """Manages ADB device connections."""
    
    @staticmethod
    def get_main_device_id() -> Optional[str]:
        """Get the main device ID (not pairing connections)."""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return None

            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            devices = []

            for line in lines:
                if line.strip() and 'device' in line:
                    device_id = line.split('\t')[0]
                    # Skip pairing connections
                    if '_adb-tls-connect._tcp' not in device_id:
                        devices.append(device_id)

            return devices[0] if devices else None

        except Exception as e:
            logger.error(f"Error getting main device ID: {e}")
            return None
    
    @staticmethod
    def check_adb_connection() -> bool:
        """Check if ADB device is connected."""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, timeout=5)
            return 'device' in result.stdout
        except Exception as e:
            logger.error(f"Error checking ADB connection: {e}")
            return False

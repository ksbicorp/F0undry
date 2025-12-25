# F0undry Configuration File
# Central configuration for all tools and paths

import os
from pathlib import Path

# Base directory (F0undry root)
BASE_DIR = Path(__file__).parent.parent

# Chromium Configuration
CHROMIUM_PATH = BASE_DIR / "chrome-win" / "chrome.exe"

# Tool Paths
TOOL_PATHS = {
    'secretfinder': BASE_DIR / "tools" / "SecretFinder-master" / "SecretFinder.py",
    'hedns': BASE_DIR / "tools" / "HEDnsExtractor-main" / "hednsextractor.exe",
    'frank': BASE_DIR / "core" / "frank_headless_v2_ultimate.py",
    'keyhacks': BASE_DIR / "tools" / "keyhacks_validator.py",
}

# Telegram Configuration (use environment variables in production)
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID', '')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH', '')

# Proxy Configuration (for evilginx2 integration)
USE_PROXY = False
PROXY_URL = "http://localhost:8080"

# Concurrency Settings
MAX_CONCURRENT_REQUESTS = 20
BATCH_SIZE = 50

# Output Files
RESULTS_FILE = BASE_DIR / "f0undry_results.txt"
VALID_KEYS_FILE = BASE_DIR / "f0undry_valid_keys.txt"
TARGETS_FILE = BASE_DIR / "targets.txt"

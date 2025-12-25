# 🔥 F0undry - Enterprise-Grade API Key & Secret Scanner

**F0undry** is a world-standard, fully automated secret discovery and validation engine. It combines advanced Telegram scraping, stealth headless browsing, and multi-layer de-obfuscation to identify exposed credentials across the web.

## 🚀 Features

### 🛡️ World-Standard Recon Engine
- **99+ Security Patterns**: Comprehensive detection for AWS, GCP, Azure, Stripe, GitHub, Slack, Private Keys (RSA, PGP), and more.
- **Advanced De-obfuscation**: Handles HTML entities, Base64 encoding, Punycode, and zero-width space obfuscation.
- **Protocol Filtering**: Intelligent URL canonicalization that filters out noise and focuses on high-value HTTPS targets.

### ⚡ High-Performance Scanning
- **Turbo Hunter Mode**: Powered by Playwright with 15+ concurrent browser instances for batch processing 300K+ URLs.
- **Stealth Engine**: Integrated `Franken-V2 Ultimate` with advanced fingerprinting protection and human-like behavior.
- **Telegram Integration**: High-fidelity extraction from messages, entities, buttons, and media.

### 🔧 Integrated Tool Suite
- **SecretFinder**: Deep JS file analysis for hidden secrets.
- **HEDnsExtractor**: DNS reconnaissance and enumeration.
- **KeyHacks Validator**: Real-time validation of discovered keys to eliminate false positives.

## 📁 Project Structure

```
F0undry/
├── core/                          # Core engines
│   ├── f0undry_gui.py            # Main GUI application
│   └── frank_headless_v2_ultimate.py  # Stealth browser engine
├── tools/                         # Integrated tools
│   ├── SecretFinder-master/      # JS secret extraction
│   ├── keyhacks-master/          # Validation methods
│   ├── HEDnsExtractor-main/      # DNS enumeration
│   ├── t-hoog-ex/                # Browser extension patterns
│   └── keyhacks_validator.py     # Validation framework
├── config/                        # Configuration
│   └── config.py                 # Central config
├── chrome-win/                    # Chromium browser
│   └── chrome.exe
├── results/                       # Output directory
└── run_f0undry.py                # Launcher script
```

## 🔧 Installation

### Prerequisites
```bash
# Python 3.8+
pip install PyQt5 selenium undetected-chromedriver requests telethon playwright aiohttp pyyaml
```

### Optional (for AWS validation)
```bash
pip install boto3
```

## 🎮 Quick Start

1. **Clone & Install**:
   ```bash
   git clone https://github.com/yourusername/F0undry.git
   cd F0undry
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Configure**:
   Edit `config/config.py` or set environment variables:
   ```bash
   export TELEGRAM_API_ID="your_id"
   export TELEGRAM_API_HASH="your_hash"
   ```

3. **Run**:
   ```bash
   python run_f0undry.py
   ```

## 🔐 Validation Framework

F0undry uses **KeyHacks validation methods** to verify discovered keys:

- ✅ Slack Webhooks & Tokens
- ✅ GitHub Access Tokens
- ✅ Google API Keys
- ✅ Stripe API Keys
- ✅ AWS Access Keys
- ✅ Facebook Access Tokens
- ✅ Twilio API Keys
- ✅ Mailgun API Keys
- ✅ Heroku API Keys
- ...and 70+ more

## 📊 Output Files

- `results/f0undry_results.txt` - All discovered secrets
- `results/f0undry_valid_keys.txt` - Validated API keys only
- `results/targets.txt` - URL list for scanning

## ⚙️ Advanced Features

### Chromium Path
Centralized Chromium configuration ensures all tools use the same browser:
```python
CHROMIUM_PATH = BASE_DIR / "chrome-win" / "chrome.exe"
```

### Pattern Detection
- **99+ regex patterns** (World-Standard Vault)
- **SecretFinder patterns** integrated
- **Custom patterns** easily extensible
- **Advanced De-obfuscation** (Base64, HTML, Punycode)

### Proxy Integration
Route all requests through evilginx2 or custom proxy for:
- IP rotation
- Anti-bot bypass
- Rate limit circumvention

## ⚠️ Legal Disclaimer

**F0undry is for authorized security testing only.**

- ✅ Use on systems you own
- ✅ Use with explicit written permission
- ✅ Use for educational purposes
- ❌ Do NOT scan unauthorized systems
- ❌ Do NOT violate Terms of Service
- ❌ Do NOT use for malicious purposes

Users are solely responsible for compliance with applicable laws. Unauthorized scanning is illegal.

## 🛠️ Troubleshooting

### "Chromium not found"
Ensure `chrome-win/chrome.exe` exists:
```bash
ls F0undry/chrome-win/chrome.exe
```

### "Import Error"
Install missing dependencies:
```bash
pip install -r ../requirements.txt
```

### "Playwright not available"
```bash
pip install playwright
playwright install
```

## 📚 Tool Credits

- **SecretFinder**: m4ll0k
- **KeyHacks**: streaak
- **HEDnsExtractor**: HuntDownProject
- **t-hoog-ex**: trufflesecurity
- **Evilginx2**: kgretzky

## 🔥 F0undry - Forged in Code, Tested by Fire

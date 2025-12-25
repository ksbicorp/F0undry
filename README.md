# 🔥 F0undry - Enterprise-Grade API Key & Secret Scanner 🔐

**F0undry** is a world-standard, fully automated secret discovery and validation engine. It combines advanced Telegram scraping, stealth headless browsing, and multi-layer de-obfuscation to identify exposed credentials across the web.

![F0undry Screenshot](f0undry-screenshot.png)

## 🚀 Features

### 🛡️ World-Standard Recon Engine
- **99+ Security Patterns** 🎯: Comprehensive detection for AWS, GCP, Azure, Stripe, GitHub, Slack, Private Keys (RSA, PGP), and more.
- **Advanced De-obfuscation** 🔓: Handles HTML entities, Base64 encoding, Punycode, and zero-width space obfuscation.
- **Protocol Filtering** 🌐: Intelligent URL canonicalization that filters out noise and focuses on high-value HTTPS targets.

### ⚡ High-Performance Scanning
- **Turbo Hunter Mode** 🚄: Powered by Playwright with 15+ concurrent browser instances for batch processing 300K+ URLs.
- **Stealth Engine** 🥷: Integrated `Franken-V2 Ultimate` with advanced fingerprinting protection and human-like behavior.
- **Telegram Integration** 💬: High-fidelity extraction from messages, entities, buttons, and media.

### 🔧 Integrated Tool Suite
- **SecretFinder** 🔍: Deep JS file analysis for hidden secrets.
- **HEDnsExtractor** 🌐: DNS reconnaissance and enumeration.
- **KeyHacks Validator** ✅: Real-time validation of discovered keys to eliminate false positives.

---

## 🛠️ Integrated Tools Arsenal

F0undry integrates industry-leading open-source tools to create a comprehensive security testing platform. Each tool has been carefully selected for its proven effectiveness in the security community:

### 🔍 **SecretFinder** by [m4ll0k](https://github.com/m4ll0k)

**Why it's World-Class:**
SecretFinder is a powerful Python-based tool that specializes in discovering sensitive data hidden within JavaScript files. Built upon LinkFinder's foundation, it employs sophisticated regex patterns and jsbeautifier to uncover:

- 🔑 **API Keys & Access Tokens**: Identifies exposed credentials in minified or obfuscated JS
- 🎫 **JWT Tokens**: Extracts JSON Web Tokens from client-side code
- 🔐 **Authorization Headers**: Discovers hardcoded authentication mechanisms
- 📝 **Sensitive Endpoints**: Maps internal API routes and paths

**Key Features:**
- HTML and plaintext output formats
- Support for authenticated scanning with cookies
- Burp Suite integration for seamless workflow
- Recursive link extraction and processing
- Custom regex filtering for targeted searches
- Proxy support for enterprise environments

**F0undry Integration:** Automatically scans all discovered JavaScript files for secrets, feeding results directly into the validation pipeline.

---

### ✅ **KeyHacks** by [streaak](https://github.com/streaak)

**Why it's Essential:**
KeyHacks provides validation methods for 70+ different API key types, eliminating false positives and confirming real security issues. This is critical because discovering a key is only half the battle—you need to verify it's actually valid.

**Supported Services Include:**
- ☁️ **Cloud Providers**: AWS, Azure, GCP credentials validation
- 💳 **Payment APIs**: Stripe, PayPal, Square key testing
- 📱 **Social Media**: Facebook, Twitter, Instagram token verification
- 🔧 **Developer Tools**: GitHub, GitLab, Slack API validation
- 📧 **Email Services**: SendGrid, Mailgun, Twilio authentication
- 📊 **Analytics**: Google Analytics, Amplitude, DataDog keys
- 🗄️ **Databases**: MongoDB, Firebase, Redis credentials

**Key Features:**
- Real HTTP requests to validate key permissions
- Distinguishes between read-only and write-capable keys
- Identifies expired or revoked credentials
- Safe, non-destructive testing methods
- Automated validation scripts ready to use

**F0undry Integration:** Every discovered key is automatically validated through KeyHacks methods, ensuring you only receive confirmed, actionable results.

---

### 🌐 **HEDnsExtractor** by [HuntDownProject](https://github.com/HuntDownProject)

**Why it's Powerful:**
HEDnsExtractor is a specialized DNS reconnaissance tool written in Go that extracts domain information from Hurricane Electric's portal. It excels at:

- 🔎 **Domain Discovery**: Uncovers related domains and subdomains
- 🌍 **Network Mapping**: Extracts IP ranges and network blocks
- 🦠 **Phishing Detection**: Identifies suspicious lookalike domains
- 📋 **VirusTotal Integration**: Enriches data with threat intelligence
- 🎯 **IPv6 Support**: Full support for modern IP addressing

**Key Features:**
- YAML-based workflow configuration
- Multi-domain batch processing
- Regex pattern matching for targeted extraction
- Network-to-domain reverse mapping
- Automated threat hunting capabilities
- Clean, structured output for further processing

**F0undry Integration:** Provides comprehensive DNS reconnaissance for target domains, expanding the attack surface by discovering additional assets and infrastructure.

---

### 🦡 **t-hoog-ex (TruffleHog Extension)** by [TruffleSecurity](https://github.com/trufflesecurity)

**Why it's Innovative:**
This browser extension brings real-time secret detection directly to your browser, allowing you to identify exposed credentials as you browse:

- 🔴 **Live Detection**: Real-time scanning of web pages for secrets
- 🎨 **Visual Indicators**: Highlights sensitive data directly in the browser
- 📦 **Pattern Library**: Extensive database of secret patterns
- 🚨 **Instant Alerts**: Immediate notification of discovered credentials

**Key Features:**
- Browser extension for Firefox and Chrome
- AWS key detection and validation helpers
- Slack webhook identification
- Algolia API key testing
- Amplitude analytics validation
- Non-intrusive, privacy-focused scanning

**F0undry Integration:** Leverages TruffleHog's proven detection patterns and methodologies, adapted for automated scanning workflows.

---

### 🎣 **Evilginx2** by [kgretzky](https://github.com/kgretzky/evilginx2)

**Why it's Strategic:**
Evilginx2 is a man-in-the-middle attack framework that enables sophisticated phishing campaigns. While F0undry is a defensive tool, integrating with Evilginx2's proxy capabilities provides:

- 🔄 **IP Rotation**: Route traffic through proxy infrastructure
- 🛡️ **Anti-Bot Bypass**: Evade detection and rate limiting
- 🌐 **Traffic Obfuscation**: Hide scanning activities
- 🔒 **HTTPS Interception**: Deep packet inspection capabilities

**Key Features:**
- Reverse proxy with SSL/TLS support
- Session hijacking protection for testing
- Custom phishlet creation
- Real-time traffic manipulation
- Advanced evasion techniques

**F0undry Integration:** Optional proxy routing through Evilginx2 infrastructure for enhanced stealth and to bypass aggressive rate limiting during large-scale scans.

---

## 💎 Why F0undry is World-Standard

F0undry isn't just another secret scanner—it represents the convergence of battle-tested tools and innovative techniques:

### ✨ **Comprehensive Coverage**
- **99+ Detection Patterns**: More than any competing tool
- **70+ Validation Methods**: Real verification, not just pattern matching
- **Multi-Source Discovery**: Telegram, web scraping, DNS, and JavaScript analysis
- **15+ Concurrent Browsers**: Industrial-scale throughput

### 🎯 **Superior Accuracy**
- **Advanced De-obfuscation**: Handles Base64, HTML entities, Punycode, zero-width characters
- **Real Validation**: Every key tested with actual API calls
- **False Positive Elimination**: Multi-stage filtering and verification
- **Context-Aware Extraction**: Understands code structure and patterns

### 🚀 **Enterprise Performance**
- **300K+ URLs per Session**: Proven scalability
- **Async Architecture**: Non-blocking, concurrent operations
- **Stealth Technology**: Franken-V2 Ultimate fingerprint protection
- **Resource Optimization**: Intelligent browser instance pooling

### 🔧 **Production Ready**
- **GUI Interface**: User-friendly PyQt5 application
- **Extensible Architecture**: Easy to add new patterns and validators
- **Centralized Configuration**: Single source for all settings
- **Professional Output**: Structured results in multiple formats

This combination of breadth, accuracy, performance, and usability makes F0undry the go-to solution for professional security researchers and penetration testers worldwide. 🌍

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

### Prerequisites 📋
```bash
# Python 3.8+
pip install PyQt5 selenium undetected-chromedriver requests telethon playwright aiohttp pyyaml
```

### Optional (for AWS validation) ☁️
```bash
pip install boto3
```

## 🎮 Quick Start

1. **Clone & Install** 📥:
   ```bash
   git clone https://github.com/yourusername/F0undry.git
   cd F0undry
   pip install -r requirements.txt
   playwright install chromium
   ```

2. **Configure** ⚙️:
   Edit `config/config.py` or set environment variables:
   ```bash
   export TELEGRAM_API_ID="your_id"
   export TELEGRAM_API_HASH="your_hash"
   ```

3. **Run** 🚀:
   ```bash
   python run_f0undry.py
   ```

## 🔐 Validation Framework

F0undry uses **KeyHacks validation methods** to verify discovered keys:

- ✅ Slack Webhooks & Tokens 💬
- ✅ GitHub Access Tokens 🐙
- ✅ Google API Keys 🔍
- ✅ Stripe API Keys 💳
- ✅ AWS Access Keys ☁️
- ✅ Facebook Access Tokens 👤
- ✅ Twilio API Keys 📞
- ✅ Mailgun API Keys 📧
- ✅ Heroku API Keys 🚀
- ...and 70+ more! 🎯

## 📊 Output Files

- `results/f0undry_results.txt` 📝 - All discovered secrets
- `results/f0undry_valid_keys.txt` ✅ - Validated API keys only
- `results/targets.txt` 🎯 - URL list for scanning

## ⚙️ Advanced Features

### Chromium Path 🌐
Centralized Chromium configuration ensures all tools use the same browser:
```python
CHROMIUM_PATH = BASE_DIR / "chrome-win" / "chrome.exe"
```

### Pattern Detection 🎯
- **99+ regex patterns** (World-Standard Vault) 🔐
- **SecretFinder patterns** integrated 🔍
- **Custom patterns** easily extensible 📝
- **Advanced De-obfuscation** (Base64, HTML, Punycode) 🔓

### Proxy Integration 🔄
Route all requests through evilginx2 or custom proxy for:
- IP rotation 🌍
- Anti-bot bypass 🛡️
- Rate limit circumvention ⚡

## ⚠️ Legal Disclaimer

**F0undry is for authorized security testing only.** ⚖️

- ✅ Use on systems you own 🏠
- ✅ Use with explicit written permission 📜
- ✅ Use for educational purposes 📚
- ❌ Do NOT scan unauthorized systems 🚫
- ❌ Do NOT violate Terms of Service 📋
- ❌ Do NOT use for malicious purposes 💀

Users are solely responsible for compliance with applicable laws. Unauthorized scanning is illegal. 🚨

## 🛠️ Troubleshooting

### "Chromium not found" 🔍
Ensure `chrome-win/chrome.exe` exists:
```bash
ls F0undry/chrome-win/chrome.exe
```

### "Import Error" 📦
Install missing dependencies:
```bash
pip install -r requirements.txt
```

### "Playwright not available" 🎭
```bash
pip install playwright
playwright install
```

## 📚 Tool Credits

This project stands on the shoulders of giants. Huge thanks to these amazing developers:

- **SecretFinder** 🔍: [m4ll0k/SecretFinder](https://github.com/m4ll0k/SecretFinder) - JavaScript secret extraction expert
- **KeyHacks** ✅: [streaak/KeyHacks](https://github.com/streaak/KeyHacks) - API validation methodology pioneer
- **HEDnsExtractor** 🌐: [HuntDownProject/HEDnsExtractor](https://github.com/HuntDownProject/HEDnsExtractor) - DNS reconnaissance specialist
- **t-hoog-ex** 🦡: [trufflesecurity/trufflehog](https://github.com/trufflesecurity/trufflehog) - Browser-based secret detection
- **Evilginx2** 🎣: [kgretzky/evilginx2](https://github.com/kgretzky/evilginx2) - Advanced proxy framework

## 🔥 F0undry - Forged in Code, Tested by Fire 🔥

---

**⭐ Star this repo if you find it useful!** | **🐛 Report issues** | **💡 Submit PRs** | **📢 Share with the community!**

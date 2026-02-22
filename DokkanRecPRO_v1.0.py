#!/usr/bin/env python3
# MIT License
# Copyright (c) 2026 youtube/@unoacasoyt
import asyncio
import base64
import subprocess
import time
import os
import numpy as np
import io
import re
import sys
import importlib
from PIL import Image
from playwright.async_api import async_playwright

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn
from rich.panel import Panel

console = Console()

# --- CONFIGURAZIONE (identica a FINAL_BUILD_GEM) ---
MAX_RECORD_TIME = 45
MIN_PERIOD_FRAMES = 30
MAX_PERIOD_FRAMES = 1500
FINGERPRINT_SIZE = 16
BLACK_THRESHOLD = 12

AD_KEYWORDS = [
    'doubleclick', 'googleanalytics', 'googleadservices', 'googletagmanager',
    'facebook.com/tr', 'analytics', 'tracking', 'metrics', 'pixel',
    'cookie', 'ads', 'adserver', 'adservice', 'adnxs', 'criteo',
    'casalemedia', 'rubiconproject', 'openx', 'pubmatic', 'chartbeat',
    'hotjar', 'mouseflow', 'newrelic', 'beacon', 'exelator', 'bluekai',
    'agkn', 'rlcdn', 'mathtag', 'krxd', 'turn', 'contextweb',
    'bidswitch', 'appnexus', 'spotxchange', 'lijit', 'sonobi',
    'media.net', 'outbrain', 'taboola', 'sharethrough', 'revcontent'
]

STRINGS = {
    "IT": {
        "start_msg": "Seleziona la tua lingua [ENG] o [IT]: ",
        "wrong_lang": "Scelta sbagliata. Scrivi ENG o IT: ",
        "input_link": "Inserisci il link di DokkanDB: ",
        "wrong_link": "Il link è errato. Deve contenere 'dokkandb.com/cards/'.",
        "browser_start": "Avvio browser e filtri AdBlock...",
        "browser_ok": "Browser avviato. Filtri attivi.",
        "target_search": "Analisi della pagina e ricerca target...",
        "target_ur": "Target trovato (Metodo: UR)",
        "target_lr": "Target trovato (Metodo: LR)",
        "sync_msg": "Sincronizzazione animazione...",
        "sync_ok": "Sincronizzazione completata.",
        "sync_fail": "Sync fallito, procedo con cattura standard.",
        "load_page": "Caricamento pagina e pulizia...",
        "load_ok": "Pagina caricata e pulita.",
        "recording": "Registrazione in corso...",
        "rec_end": "Registrazione terminata.",
        "loop_search": "Ricerca loop perfetto nei frame...",
        "loop_ok": "Loop trovato! ({lag} frame).",
        "loop_fail": "Nessun loop trovato o pochi frame.",
        "encoding": "Codifica WebP in corso...",
        "encode_ok": "Codifica WebP completata.",
        "success": "File generato con successo: ",
        "error": "Si è verificato un errore: ",
        "check_packages": "Verifica dei pacchetti Python richiesti...",
        "package_ok": "{} {} è installato (versione {})",
        "package_missing": "{} NON trovato",
        "package_outdated": "{} versione {} richiesta, trovata {}",
        "install_request": "I seguenti pacchetti sono mancanti o non aggiornati:\n{}\nVuoi installarli/aggiornarli? (s/n): ",
        "install_abort": "Installazione rifiutata. Uscita.",
        "install_error": "Errore durante l'installazione di {}: {}",
        "install_success": "Pacchetti installati correttamente.",
        "check_chromium": "Verifica dell'installazione di Chromium...",
        "chromium_found": "Chromium è già installato.",
        "chromium_missing": "Chromium non trovato. È necessario scaricarlo (circa 300MB).",
        "chromium_confirm": "Vuoi procedere con il download? (s/n): ",
        "chromium_abort": "Download rifiutato. Uscita.",
        "chromium_installing": "Download di Chromium in corso...",
        "chromium_ok": "Chromium installato correttamente.",
        "chromium_error": "Errore durante il download di Chromium: {}"
    },
    "ENG": {
        "start_msg": "Select your language [🇺🇸 ENG] or [🇮🇹 IT]: ",
        "wrong_lang": "Wrong choice. Write ENG or IT: ",
        "input_link": "Insert DokkanDB link: ",
        "wrong_link": "Invalid link. It must contain 'dokkandb.com/cards/'.",
        "browser_start": "Launching browser and AdBlock filters...",
        "browser_ok": "Browser started. Filters active.",
        "target_search": "Analyzing page and searching target...",
        "target_ur": "Target found (Method: UR)",
        "target_lr": "Target found (Method: LR)",
        "sync_msg": "Synchronizing animation...",
        "sync_ok": "Synchronization complete.",
        "sync_fail": "Sync failed, using standard capture.",
        "load_page": "Loading page and cleanup...",
        "load_ok": "Page loaded and cleaned.",
        "recording": "Recording in progress...",
        "rec_end": "Recording finished.",
        "loop_search": "Searching for perfect loop...",
        "loop_ok": "Loop found! ({lag} frames).",
        "loop_fail": "No loop found or insufficient frames.",
        "encoding": "Encoding WebP...",
        "encode_ok": "WebP encoding complete.",
        "success": "File generated successfully: ",
        "error": "An error occurred: ",
        "check_packages": "Checking required Python packages...",
        "package_ok": "{} {} is installed (version {})",
        "package_missing": "{} NOT found",
        "package_outdated": "{} version {} required, found {}",
        "install_request": "The following packages are missing or outdated:\n{}\nDo you want to install/upgrade them? (y/n): ",
        "install_abort": "Installation refused. Exiting.",
        "install_error": "Error installing {}: {}",
        "install_success": "Packages installed successfully.",
        "check_chromium": "Checking Chromium installation...",
        "chromium_found": "Chromium is already installed.",
        "chromium_missing": "Chromium not found. It needs to be downloaded (approx 300MB).",
        "chromium_confirm": "Proceed with download? (y/n): ",
        "chromium_abort": "Download refused. Exiting.",
        "chromium_installing": "Downloading Chromium...",
        "chromium_ok": "Chromium installed successfully.",
        "chromium_error": "Error downloading Chromium: {}"
    }
}


def select_language():
    lang_choice = console.input(f"[bold white]{STRINGS['IT']['start_msg']}[/]").strip().upper()
    while lang_choice not in ["ENG", "IT"]:
        lang_choice = console.input(f"[bold red]{STRINGS['IT']['wrong_lang']} / {STRINGS['ENG']['wrong_lang']}[/]").strip().upper()
    return lang_choice


SELECTED_LANG = select_language()
L = STRINGS[SELECTED_LANG]
console.print(Panel.fit(f"[bold magenta]🚀 DokkanDB Recorder PRO[/] - {SELECTED_LANG}"))

REQUIRED_PACKAGES = {
    "playwright": "1.40.0",
    "rich": "13.0.0",
    "numpy": "1.20.0",
    "Pillow": "10.0.0"
}


def get_installed_version(package_name):
    try:
        from importlib.metadata import version
        return version(package_name)
    except:
        try:
            import pkg_resources
            return pkg_resources.get_distribution(package_name).version
        except:
            return None


def check_packages():
    console.print(f"\n[cyan]{L['check_packages']}[/]")
    missing = []
    outdated = []
    for pkg, min_ver in REQUIRED_PACKAGES.items():
        try:
            if pkg == "Pillow":
                mod = importlib.import_module("PIL")
            else:
                mod = importlib.import_module(pkg)
            ver = getattr(mod, "__version__", get_installed_version(pkg))
            if not ver:
                missing.append(pkg)
            elif ver < min_ver:
                outdated.append((pkg, ver, min_ver))
            else:
                console.print(f"  [green]✓[/] {L['package_ok'].format(pkg, '✔', ver)}")
        except:
            missing.append(pkg)

    if not missing and not outdated:
        return True

    answer = console.input(f"[bold]{L['install_request'].format(', '.join(missing))}[/]").strip().lower()
    if answer not in ('s', 'y'):
        console.print(f"[bold red]{L['install_abort']}[/]")
        sys.exit(1)

    for pkg in missing:
        subprocess.run([sys.executable, "-m", "pip", "install", pkg])
    for pkg, _, _ in outdated:
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", pkg])
    console.print(f"[green]{L['install_success']}[/]")
    return True


def check_chromium():
    console.print(f"\n[cyan]{L['check_chromium']}[/]")
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            if os.path.exists(p.chromium.executable_path):
                console.print(f"  [green]✓[/] {L['chromium_found']}")
                return True
    except:
        pass

    answer = console.input(f"[bold]{L['chromium_confirm']}[/]").strip().lower()
    if answer not in ('s', 'y'):
        console.print(f"[bold red]{L['chromium_abort']}[/]")
        sys.exit(1)

    subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"])
    console.print(f"[green]{L['chromium_ok']}[/]")
    return True


check_packages()
check_chromium()


class DokkanRecorder:
    def __init__(self, url, lang_code):
        self.url = url
        self.lang = STRINGS[lang_code]
        self.frames = []
        self.frame_times = []
        self.start_time = None
        self.capture_method = None
        self.target_selector = 'app-sticker-renderer'
        self.ur_bbox = None

    # --- Metodi ripristinati da FINAL_BUILD_GEM ---

    async def ensure_cookies_closed(self):
        """Ripristinato: tenta più volte di chiudere i popup cookie."""
        for _ in range(3):
            await self.handle_popups()
            await asyncio.sleep(1)

    async def sync_lr_animation(self):
        """Ripristinato: sincronizzazione LR completa con messaggi."""
        console.print(f"[cyan]{self.lang['sync_msg']}[/]")
        try:
            art_button = self.page.locator('button[class*="type-"]:has-text("Art")')
            await art_button.wait_for(state="visible", timeout=5000)
            await art_button.click()
            await asyncio.sleep(0.5)

            anim_button = self.page.locator('button[class*="type-"]:has-text("Animation")')
            await anim_button.wait_for(state="visible", timeout=5000)
            await anim_button.click()
            console.print(f"[green]{self.lang['sync_ok']}[/]")
        except Exception as e:
            console.print(f"[yellow]{self.lang['sync_fail']} ({e})[/]")

    async def capture_frame_raw(self):
        """Ripristinato: gestione UR, UR_screenshot, LR."""
        try:
            if self.capture_method == 'ur':
                js = """() => {
                    const host = document.querySelector('app-sticker-renderer');
                    if (!host) return null;
                    const c = host.shadowRoot ? host.shadowRoot.querySelector('canvas') : host.querySelector('canvas');
                    return c ? c.toDataURL('image/webp', 0.90) : null;
                }"""
                data_url = await self.page.evaluate(js)
                if data_url:
                    img = Image.open(io.BytesIO(base64.b64decode(data_url.split(',')[1]))).convert('RGB')
                    # Se i primi frame sono neri, passa a screenshot
                    if len(self.frames) < 5 and self._is_black(img):
                        self.capture_method = 'ur_screenshot'
                        return await self.capture_frame_raw()
                    return img
                return None

            elif self.capture_method == 'ur_screenshot':
                if not self.ur_bbox:
                    self.ur_bbox = await self.page.locator(self.target_selector).bounding_box()
                if self.ur_bbox:
                    b = await self.page.screenshot(clip=self.ur_bbox, type='jpeg', quality=90)
                    return Image.open(io.BytesIO(b)).convert('RGB')
                return None

            else:  # LR
                js = """() => {
                    const c = document.querySelector('canvas.canvasC');
                    return c ? c.toDataURL('image/jpeg', 0.8) : null;
                }"""
                data_url = await self.page.evaluate(js)
                if data_url:
                    header, encoded = data_url.split(",", 1)
                    raw_data = base64.b64decode(encoded)
                    return Image.open(io.BytesIO(raw_data)).convert('RGB')
                return None
        except Exception as e:
            # Silenzioso, torna None
            return None

    def _fingerprint(self, img):
        return np.array(img.resize((FINGERPRINT_SIZE, FINGERPRINT_SIZE)).convert('L')).flatten()

    def _is_black(self, img):
        return np.array(img.convert('L')).mean() < BLACK_THRESHOLD

    def _find_sync_points(self):
        """Ripristinato: cerca il loop perfetto e restituisce inizio e fine."""
        if len(self.frames) < 50:
            return 0, len(self.frames)

        first_valid = 0
        for i, frame in enumerate(self.frames):
            if not self._is_black(frame):
                first_valid = i
                break

        data = [self._fingerprint(f) for f in self.frames[first_valid:]]
        data = np.array(data)
        n = len(data)

        best_lag = None
        min_mse = float('inf')
        search_limit = min(MAX_PERIOD_FRAMES, n // 2)

        for lag in range(MIN_PERIOD_FRAMES, search_limit):
            diff = data[:80] - data[lag:lag+80]
            mse = np.mean(diff**2)
            if mse < min_mse:
                min_mse = mse
                best_lag = lag

        if not best_lag:
            return first_valid, len(self.frames)

        start_offset = 0
        min_start_mse = float('inf')
        for i in range(0, min(best_lag, 80)):
            mse = np.mean((data[i] - data[i + best_lag])**2)
            if mse < min_start_mse:
                min_start_mse = mse
                start_offset = i

        actual_start = first_valid + start_offset
        actual_end = actual_start + best_lag
        actual_end = min(actual_end, len(self.frames))

        console.print(f"[dim]📊 Analisi: Loop di {best_lag} frame. Taglio: {actual_start} -> {actual_end}[/]")
        return actual_start, actual_end

    # --- Metodi già presenti (adattati per usare i nuovi) ---

    async def setup(self, progress):
        task = progress.add_task(f"[cyan]{self.lang['browser_start']}", total=None)
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(
            headless=True,
            args=["--use-angle=gl", "--disable-web-security", "--no-sandbox", "--disable-gpu-vsync"]
        )
        self.context = await self.browser.new_context(viewport={"width": 1080, "height": 1125})
        self.page = await self.context.new_page()
        await self.page.route("**/*", lambda route: route.abort()
                               if any(x in route.request.url.lower() for x in AD_KEYWORDS)
                               else route.continue_())
        progress.update(task, completed=100, description=f"[green]{self.lang['browser_ok']}")

    async def handle_popups(self):
        selectors = [
            'button:has-text("Accept")', 'button:has-text("Accetta")',
            'button:has-text("OK")', 'button:has-text("Got it")',
            'button:has-text("I agree")', '.cookie-accept', '#onetrust-accept-btn-handler'
        ]
        for sel in selectors:
            try:
                if await self.page.locator(sel).first.is_visible():
                    await self.page.click(sel, timeout=500)
            except:
                pass
        await self.page.evaluate("""() => {
            document.querySelectorAll('.gdpr, .cookie, .modal, .overlay').forEach(el => el.remove());
        }""")

    async def find_target(self, progress):
        task = progress.add_task(f"[cyan]{self.lang['target_search']}", total=None)
        script_ur = """() => {
            const h = document.querySelector('app-sticker-renderer');
            return (h && (h.shadowRoot || h.querySelector('canvas'))) ? true : false;
        }"""
        found = await self.page.evaluate(script_ur)
        if found:
            self.capture_method = 'ur'
            progress.update(task, completed=100, description=f"[green]{self.lang['target_ur']}")
        else:
            self.capture_method = 'lr'
            progress.update(task, completed=100, description=f"[green]{self.lang['target_lr']}")

    async def record(self):
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console
        ) as progress:

            await self.setup(progress)

            nav_task = progress.add_task(f"[cyan]{self.lang['load_page']}", total=None)
            await self.page.goto(self.url, wait_until="networkidle")
            await self.handle_popups()
            await asyncio.sleep(2)
            progress.update(nav_task, completed=100, description=f"[green]{self.lang['load_ok']}")

            await self.find_target(progress)

            # --- Ripristinato: chiamata a ensure_cookies_closed per UR ---
            if self.capture_method == 'ur':
                await self.ensure_cookies_closed()

            if self.capture_method == 'lr':
                await self.sync_lr_animation()

            record_task = progress.add_task(f"[red]{self.lang['recording']}", total=MAX_RECORD_TIME)
            self.start_time = time.time()

            # Loop di registrazione (originale con stampa periodica)
            while (time.time() - self.start_time) < MAX_RECORD_TIME:
                elapsed = time.time() - self.start_time
                img = await self.capture_frame_raw()
                if img:
                    self.frames.append(img)
                    self.frame_times.append(elapsed)

                # Stampa ogni 100 frame (come in FINAL_BUILD_GEM)
                if len(self.frames) % 100 == 0:
                    console.print(f"\r📦 Frame catturati: {len(self.frames)}", end="", style="bold")

                progress.update(record_task, completed=elapsed)
                await asyncio.sleep(0)

            console.print()  # newline dopo il contatore frame
            console.print(f"[green]{self.lang['rec_end']}[/]")

            # --- Ricerca loop e salvataggio ---
            console.print(f"[cyan]{self.lang['loop_search']}[/]")
            start_idx, end_idx = self._find_sync_points()
            final_frames = self.frames[start_idx:end_idx]
            final_times = self.frame_times[start_idx:end_idx]

            if not final_frames:
                console.print(f"[yellow]{self.lang['loop_fail']}[/]")
                final_frames = self.frames
                final_times = self.frame_times

            total_duration = final_times[-1] - final_times[0] if len(final_times) > 1 else 1.0
            fps = len(final_frames) / total_duration if total_duration > 0 else 50

            # --- Encoding WebP ---
            filename = f"dokkan_resync_{int(time.time())}.webp"
            w, h = final_frames[0].size
            w, h = w - (w % 2), h - (h % 2)  # dimensioni pari per ffmpeg

            encode_task = progress.add_task(f"[magenta]{self.lang['encoding']}", total=len(final_frames))

            cmd = [
                "ffmpeg", "-y", "-f", "image2pipe", "-framerate", str(fps),
                "-i", "-", "-vf", f"scale={w}:{h}",
                "-c:v", "libwebp", "-lossless", "0", "-q:v", "80",
                "-preset", "drawing", "-loop", "0", "-an", filename
            ]

            proc = await asyncio.create_subprocess_exec(
                *cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
            )

            for frame in final_frames:
                img_io = io.BytesIO()
                frame.save(img_io, format='JPEG', quality=80)
                proc.stdin.write(img_io.getvalue())
                await proc.stdin.drain()
                progress.update(encode_task, advance=1)

            proc.stdin.close()
            await proc.wait()

            progress.update(encode_task, completed=len(final_frames), description=f"[green]{self.lang['encode_ok']}[/]")

        console.print(f"\n[bold green]✨ {self.lang['success']} {filename}[/]\n")
        await self.browser.close()
        await self.playwright.stop()


async def main():
    lang_code = SELECTED_LANG
    L = STRINGS[lang_code]
    while True:
        target_url = console.input(f"[bold yellow]{L['input_link']}[/]").strip()
        if "dokkandb.com/cards/" not in target_url:
            console.print(f"[bold red]❌ {L['wrong_link']}[/]")
            continue
        if not target_url.startswith("http"):
            target_url = "https://" + target_url
        try:
            recorder = DokkanRecorder(target_url, lang_code)
            await recorder.record()
        except Exception as e:
            console.print(f"[bold red]{L['error']}[/] {e}")


if __name__ == "__main__":
    asyncio.run(main())
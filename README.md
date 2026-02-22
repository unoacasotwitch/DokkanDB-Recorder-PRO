# DokkanDB Recorder PRO — Complete README

---

# 🇬🇧 ENGLISH VERSION

## 📌 Project Overview

**DokkanDB Recorder PRO** is a Python-based tool designed to capture animation frames directly from DokkanDB card pages, automatically detect perfect animation loops, and export them as optimized WebP files.

The purpose of this project is to provide an automated workflow that removes the need for manual recording, trimming, synchronization, and encoding, making it easier to archive or analyze card animations.

The program launches a controlled browser environment, blocks ads and trackers, records frames in real time, analyzes them to detect loop points, and encodes the final animation using FFmpeg.

---

## ⚠️ Personal Disclaimer (Please Read)

I want to be fully transparent:

**I am not a programmer.**

This project was created using the help of **three different AI systems**, and I personally assembled, tested, and refined everything to the best of my ability.

If there are bugs, inefficiencies, design flaws, or parts that are not implemented in the best possible way, it is simply because I genuinely do not have the technical expertise to improve them further.

I sincerely apologize if anything is imperfect — I truly did my best and feel genuinely sorry if any part of the code is not up to professional standards.

---

## 🙏 Acknowledgements

* Special thanks to **TTD** for reviewing the project and providing feedback.
* Deep gratitude to the administrator of **dokkandb.com** for granting permission to proceed with development.

Their support made this project possible.

---

## 🧠 How It Works — Detailed Explanation

The tool performs the following pipeline:

1. Checks for required Python dependencies.
2. Verifies that Chromium (via Playwright) is installed.
3. Launches a headless browser with request filtering to block ads and trackers.
4. Loads a DokkanDB card page.
5. Automatically handles cookie consent and popups.
6. Detects whether the animation is rendered via UR or LR method.
7. Synchronizes animation playback if needed.
8. Records frames in real time.
9. Computes image fingerprints to detect repeating patterns.
10. Finds the optimal loop boundary.
11. Trims frames accordingly.
12. Encodes frames into a WebP animation using FFmpeg.

---

## 📦 Requirements

### System Requirements

* Python 3.9 or newer
* FFmpeg installed and available in PATH
* Internet connection
* Supported OS: Windows, Linux, macOS

### Python Dependencies

* playwright
* numpy
* Pillow
* rich

The script can prompt to install missing dependencies automatically.

---

## 🛠 Installation — Step-by-Step

1. Install Python (if not already installed).
2. Install FFmpeg:

   * Windows: download from official FFmpeg site and add to PATH.
   * macOS: `brew install ffmpeg`
   * Linux: use your package manager.
3. Clone or download this repository.
4. Open a terminal in the project folder.
5. Run:

```
python DokkanRecPRO_v1.0.py
```

6. Follow on-screen instructions.

---

## ▶️ Usage Guide

1. Launch the script.
2. Choose your preferred language.
3. Paste a valid DokkanDB card URL.
4. Wait while the tool records and processes frames.
5. The generated WebP file will appear in the same folder.

---

## 🧩 Features

* Automatic dependency checking
* Browser automation with ad filtering
* Cookie popup handling
* Animation synchronization
* Loop detection via frame analysis
* Automated WebP encoding
* Minimal manual interaction

---

## ❓ FAQ

**Q: Is this an official DokkanDB tool?**
A: No. It is an independent project created with permission.

**Q: Can I use this commercially?**
A: Check the license and the website’s terms of service.

**Q: Why might it break sometimes?**
A: Website updates can change how animations are delivered.

**Q: Why does recording take time?**
A: The tool captures enough frames to detect loops accurately.

---

## 🧯 Troubleshooting

**Problem: FFmpeg not found**
→ Ensure FFmpeg is installed and in PATH.

**Problem: Browser fails to launch**
→ Reinstall Playwright and run `playwright install`.

**Problem: No frames captured**
→ Check internet connection or URL validity.

**Problem: Script crashes**
→ Try updating Python packages.

---

## 🤝 Contributing

Contributions are welcome.

If you would like to help:

* Report bugs
* Suggest improvements
* Submit pull requests
* Improve documentation

Please keep in mind that the project is maintained by a non-programmer, so clear explanations are greatly appreciated.

---

## 🗺 Roadmap / Future Improvements

Possible future enhancements:

* GUI interface
* Better error handling
* Performance optimization
* More robust loop detection
* Automatic updates
* Logging system
* Cross-platform packaging

---

## ⚖️ Legal Notice

* Intended for educational and archival purposes.
* Respect the terms of service of any website used.
* Provided “as is” without warranty.

---

# 🇮🇹 VERSIONE ITALIANA

## 📌 Panoramica del Progetto

**DokkanDB Recorder PRO** è uno strumento in Python che permette di catturare i frame delle animazioni dalle pagine delle carte su DokkanDB, rilevare automaticamente i loop perfetti ed esportarli in formato WebP ottimizzato.

Il progetto nasce per automatizzare operazioni che normalmente richiederebbero registrazione manuale, taglio e sincronizzazione.

---

## ⚠️ Dichiarazione Personale

Voglio essere completamente sincero:

**Non sono un programmatore.**

Questo programma è stato realizzato con l’aiuto di **tre diverse AI**, e ho assemblato e testato tutto nel miglior modo possibile.

Se ci sono errori, parti non ottimali o problemi di progettazione, è perché non possiedo le competenze tecniche per migliorarli ulteriormente.

Mi sento sinceramente costernato se qualcosa non è fatto al meglio — ho davvero fatto tutto il possibile.

---

## 🙏 Ringraziamenti

* Grazie speciale allo **TTD** per aver revisionato il progetto.
* Grazie al gestore di **dokkandb.com** per avermi dato il permesso di procedere con lo sviluppo.

---

## 🧠 Come Funziona — Dettagli

Il programma:

1. Verifica le dipendenze Python.
2. Controlla Chromium tramite Playwright.
3. Avvia un browser headless con filtri.
4. Carica la pagina della carta.
5. Gestisce cookie e popup.
6. Rileva il metodo di animazione.
7. Sincronizza la riproduzione.
8. Registra i frame.
9. Analizza i pattern per trovare il loop.
10. Taglia i frame.
11. Codifica in WebP con FFmpeg.

---

## 📦 Requisiti

* Python 3.9+
* FFmpeg installato
* Connessione Internet
* Windows / Linux / macOS

Pacchetti:

* playwright
* numpy
* Pillow
* rich

---

## 🛠 Installazione — Passo per Passo

1. Installa Python.
2. Installa FFmpeg.
3. Scarica il progetto.
4. Apri terminale nella cartella.
5. Esegui:

```
python DokkanRecPRO_v1.0.py
```

6. Segui le istruzioni.

---

## ▶️ Guida all’Uso

1. Avvia lo script.
2. Scegli lingua.
3. Inserisci link carta.
4. Attendi elaborazione.
5. Troverai il file WebP nella cartella.

---

## 🧩 Funzionalità

* Controllo automatico dipendenze
* Automazione browser
* Gestione

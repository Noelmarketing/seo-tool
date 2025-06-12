# SEO-Werkzeug

Dieses Repository enthält ein einfaches Kommandozeilenprogramm, das eine
Webseite abruft und grundlegende SEO-Metriken wie Titel, Meta-Description,
Überschriftenanzahl, Bildstatistiken und Linkinformationen ausgibt.

## Voraussetzungen

Installiere die Python-Abhängigkeiten:

```bash
pip install -r requirements.txt
```

## Installation

Das Werkzeug ist auf PyPI verfügbar und kann direkt installiert werden:

```bash
pip install seo-tool
```

Nach der Installation steht der Befehl `seo-tool` systemweit zur Verfügung:

```bash
seo-tool https://example.com
```

Für eine einfache grafische Oberfläche installiere das Paket ebenfalls und
rufe anschließend `seo-tool-gui` auf:

```bash
seo-tool-gui
```

## Verwendung

Starte das Werkzeug mit einer zu analysierenden URL:

```bash
python seo_tool.py https://example.com
```

Das Werkzeug gibt folgende Metriken aus:

- Seitentitel und Meta-Description
- Anzahl der Wörter
- Überschriftenanzahl (`h1`-`h6`)
- Anzahl der Bilder sowie wie viele Bilder kein `alt`-Attribut besitzen
- Vorhandene Canonical-URL
- Anzahl interner und externer Links

## Tests ausführen

Die Unit Tests verwenden `pytest`. Führe sie so aus:

```bash
pytest
```

## Erstellen einer Windows-Exe

Um das Werkzeug als eigenständige `.exe` für Windows zu erstellen, verwende
[PyInstaller](https://pyinstaller.org/). Installiere zuerst PyInstaller und führe dann aus:

```bash
pip install pyinstaller
pyinstaller --onefile --name seo_tool seo_tool.py
```

Die erzeugte `seo_tool.exe` liegt im Ordner `dist`. Kopiere diese Datei auf
einen Windows-Rechner und führe sie über die Eingabeaufforderung aus.

## Versionshinweise

Details zu veröffentlichten Versionen findest du im [Changelog](CHANGELOG.md).

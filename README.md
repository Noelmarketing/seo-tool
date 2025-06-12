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

## Verwendung

Starte das Werkzeug mit einer zu analysierenden URL:

```bash
python seo_tool.py https://example.com
```

Mit `--json` erhältst du die Ausgabe im JSON-Format:

```bash
python seo_tool.py https://example.com --json
```

Das Werkzeug gibt folgende Metriken aus:

- Seitentitel und Meta-Description
- Anzahl der Wörter
- Überschriftenanzahl (`h1`-`h6`)
- Anzahl der Bilder sowie wie viele Bilder kein `alt`-Attribut besitzen
- Quote der Bilder mit `alt`-Text
- Vorhandene Canonical-URL
- Anzahl interner und externer Links
- Vorhandenes Robots-Meta-Tag
- Meta-Keywords
- Open-Graph-Titel, -Beschreibung und -Bild
- Sprache (`lang`-Attribut) und Zeichensatz der Seite
- Flesch-Lesbarkeitsindex und Flesch-Kincaid-Stufe
- Geschätzte Lesezeit
- Verhältnis von Text zu HTML
- Warnungen zur Überschriftenstruktur
- Vorhandenes Viewport-Meta-Tag
- Warnung bei mehreren `h1`-Überschriften

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

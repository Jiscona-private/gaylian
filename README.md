# gaylian.net

## Nutzung

Der hier vorgestellte Code ("main"-Branch) ist unter gaylian.net nutzbar. Verschiedene Angebote benötigen einen Account, der nur von den Projektadministratoren erstellt werden kann. Wenn Sie eine eigene Instanz des gaylian-Angebotes aufsetzen wollen, beachten Sie folgende Schritte:

### Development

1. Clonen des Repositorys
2. Aufsetzen einer virtuellen Umgebung mit `python -m venv venv` und Aktivieren mit  `. venv/bin/activate` (POSIX)  bzw. `. venv/Scripts/activate` (Windows)
3. `pip install -r requirements.txt`
4. [Setzen der Environment-Variable](https://flask.palletsprojects.com/en/2.1.x/quickstart/) auf `webpages`
5. `flask run`

### Production

Bei einer nicht für die Entwicklung gedachten Nutzung empfehlen wir momentan https://gaylian.net. Die Möglichkeit des Production-Deployments auf eigenen Servern wird in Zukunft bereitgestellt werden.

## Ziel des Projektes

gaylian.net soll die Nutzung wichtiger Services einfach, schnell und sicher machen. Wir stellen Angebote, welche häufig benötigt werden, zur Verfügung.
Unsere Nutzern sollen die Kontrolle über ihre Daten zurückerlangen, ihre Privatsphäre schützen und digitale Verfolgung verhindern können. gaylian verwendet keine Tracker, ist vollkommen werbefrei und open-source.

## Angebote

Momentan bietet gaylian drei verschiende Services an:

* Cloud beziehungsweise Filesharing
* Notizenspeicher (Text)
* Dokumentenspeicher (Markdown)

Dieses Repertoire ist flexibel anpassbar und wird zudem ständig erweitert und verbessert.

## Beteiligte

Die Verwaltung und Entwicklung von gaylian.net und dem von dem System genutzten Code erfolgt duch die BT SpiderChris und Jiscona. Ermöglicht wird dieses Projekt durch die Jiscona IT und die Bonarium Fincancial Holdings.
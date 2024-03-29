# gaylian.net

## Ziel des Projektes

gaylian.net soll die Nutzung wichtiger Services einfach, schnell und sicher machen. Wir stellen Angebote, welche häufig benötigt werden, zur Verfügung.
Unsere Nutzern sollen die Kontrolle über ihre Daten zurückerlangen, ihre Privatsphäre schützen und digitale Verfolgung verhindern können. gaylian verwendet keine Tracker, ist vollkommen werbefrei und open-source.  
Neben dem Ermöglichen eines einfachen und angenehmen Nutzererlebnisses wollen wir das Internet besser machen. Mehr und mehr wird das "World Wide Web" von Konzernen und nicht von Menschen geformt. Kaum ein Tag vergeht, an dem nicht jeder von uns Services von Apple, Google, Microsoft und Co. in Anspruch nimmt. Diese Unternehmen sind jedoch genau das: gewinnorientierte Firmen. Die gaylian-Plattform steht in einer Reihe mit vielen anderen Projekten, die die Macht dieser Konzerne brechen, das Internet befreien und das World Wide Web wieder zurück in die Hände der Menschen geben wollen.

## Nutzung

Der hier vorgestellte Code ("main"-Branch) ist unter gaylian.net nutzbar. Verschiedene Angebote benötigen einen Account, der nur von den Projektadministratoren erstellt werden kann. Wenn Sie eine eigene Instanz des gaylian-Angebotes aufsetzen wollen, beachten Sie folgende Schritte:

### Development

1. Clonen des Repositorys
2. Aufsetzen einer virtuellen Umgebung mit `python -m venv venv` und Aktivieren mit  `. venv/bin/activate` (POSIX)  bzw. `. venv/Scripts/activate` (Windows)
3. `pip install -r requirements.txt`
4. `flask run`

### Production

Bei einer nicht für die Entwicklung gedachten Nutzung empfehlen wir momentan, http://gaylian.net zu nutzen. Die Möglichkeit des Production-Deployments auf eigenen Servern wird in Zukunft bereitgestellt werden.


## Angebote

Momentan bietet gaylian drei verschiende Services an:

* Cloud beziehungsweise Filesharing
* Notizenspeicher (Text)
* Dokumentenspeicher (Markdown)

Dieses Repertoire ist flexibel anpassbar und wird zudem ständig erweitert und verbessert.

## Beteiligte

Die Verwaltung und Entwicklung von gaylian.net und dem von dem System genutzten Code erfolgt duch die BT SpiderChris und Jiscona. Ermöglicht wird dieses Projekt durch die Jiscona IT und die Bonarium Holdings.  
Auch Sie können sich an der Verbesserung des Services beteiligen: durch eigene Codeentwicklung, Testen der Plattform, Berichten von Bugs und auch nur der Nutzung der Website unterstützen Sie uns und helfen dabei, ein besseres Internet zu errichten.

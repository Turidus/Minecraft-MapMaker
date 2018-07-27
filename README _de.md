Version: v0.4

# Minecraft-MapMaker


Dieses Programm nimmt ein Bild und erstellt daraus mehrere Dateien, die bei der Erstellung von Minecraft Karten behilflich sind, welche dieses Bild darstellen.

Dieses Programm kann mit der Treppenmethode arbeiten, was 153 Farben auf der Karte ermöglicht.

## Generierte Dateien

Eine Textdatei mit der Anzahl und Typ an benötigten Blöcke

Eine Textdatei mit der Position der benötigten Blöcke

Eine oder mehrere Schematics für World Edit (s. "Über große Bilder") und kompatiblen Programmen

Ein Bild welches ungefähr das Resultat zeigt
## Nutzung

### Vom source code
Dieses Programm läuft in Python 3.6 und nutzt [Pillow 5.2](https://pillow.readthedocs.io/en/5.2.x/) sowie
[appJar](http://appjar.info/).
Um dieses Programm zu nutzen, muss Python 3.6, Pillow und appJar installiert sein.

Nach dem Download des source codes kann dieser mit einem command line tool (z.B cmd auf Windows) ausgeführt werden
```powershell
python MapMaker.py "pathToFile" [optional Arguments]
``` 
Dies generiert die Dateien und speichert sie in "pathToMapMaker.py"/save/name


### GUI
Es kann auch mit Hilfe einer GUI bedient werden, in dem MapMaker_GUI.py aufgerufen wird.
```powershell
python MapMaker_GUI.py
``` 
Innerhalb der GUI können alle Optionen angepasst werden.

### From MapMaker_GUI.exe
**only tested for Windows 10 64bit**  
Diese Programm kann auch über eine exe gestartet werden. Dafür muss MinecraftMapMaker_exe.zip(https://github.com/Turidus/Minecraft-MapMaker/releases/latest) runtergeladen und entpackt werden. Das Programm wird mit Hilfe von MapMaker_GUI.exe gestartet.

Kein Python oder andere Abhängigkeit wird benötigt.

### Optionale Argumente:

+ *-bl* BaseColorID BaseColorID ... 
Diese Option ermöglicht es, bestimmt Farben und die damit verbundenen Blöcke auszuschließen.
Die IDs der Farben und die damit verbundenen Blöcke können [hier](https://minecraft.gamepedia.com/Map_item_format) oder in der
BaseColorID.txt Datei nachgeschaut werden.
+ *-n* Name 
Diese Option ermöglicht es, dem Ergebnis einen Namen zu geben, der ansonsten aus dem Namen der Datei generiert wird.
+ *-twoD* 
Diese Option wechselt von der Treppenmethode zur 2D Methode zur Erstellung der Karte. Einfacher zu bauen, nur ein Drittel der Farben.
+ *-p* 
Wenn angegeben wird **kein** Bild generiert.

+ *-bp* 
Wenn angegeben wird **keine** Textdatei mit Blockpositionen generiert.
+ *-ba*
Wenn angegeben wird **keine** Textdatei mit Anzahl und Typ von Blöcken generiert.
+ *-s* 
Wenn angegeben wird **keine** Schematic generiert.
+ *-minY* 0<=Integer<=251 (Default: 4) 
Diese Option setzt die niedrigste Y koordiante fest. Wenn die Schematic genutzt werden soll, sollte **minY** dem Blocklevel
entsprechen auf dem die Schematic eingefügt wird.
Muss mindestens 4 kleiner sein als **maxY**
+ *-maxY* 4<=Integer<=255 (Default: 250)
Diese Option setzt die höchste Y koordiante fest. Wenn **maxY** - **minY** kleiner ist als die Höhe des Bildes, können Pixelfehler
auftretten (s. "Über sehr große Bilder"). Muss mindesten 4 größer sein als **-minY**
+ *-maxS* 0<Integer (Default: 129) 
Diese Option setzt die maximale Größe der Schematic fest. Eine zu große Schematic kann beim Einfügen auf dem Server
zu Problemen führen. Wenn das Bild größer ist als maxS, wird das Bild in mehre Schematics aufgeteilt mit maxial **maxS** x **maxS**
Größe aufgeteilt. (s. "Über sehr große Bilder").

## Über die Cobblestone Line
Wenn das Bild gebaut oder eingefügt wird, fällt auf das am Nordende des Konstrukts eine zusätzliche Line Cobblestone platziert wurde.
Dies ist notwendig, um zu verhindern, dass die erste Line des Bildes falsch schattiert wird.
Der einfachste Weg. um damit umzugehen ist. die Line Cobblestone außerhalb des Kartenradiuses zu platzieren. Ansonsten kann 
der Cobblestone auch mit einem anderen Block ersetzt werden, der besser in die Umgebung passt.

## Über große Bilder
Große Bilder, 128 x 128 Pixels und größer, können die Performance des Servers beim Einfügen stark beeinträchtigen.
Es sollte unbedingt Fast Asynchron World Edit oder ähnliches genutzt werden. Es es außerdem förderlich, die Schematic aufzuteilen,
indem ein kleineres **maxS** gewählt wird.

## Über sehr große Bilder
Sehr große Bilder, 250 x 250 pixels und größer, haben zusätzlich das Problem, dass sie evt. die maximale Welthöhe von 256
Blöcken überschreiten können. Insbesondere wenn das Bild sehr einfarbig ist oder besonders groß (~450 x 450 pixels und größer)
würde eine perfekte Repräsentation des Bildes mehr als 256 Blöcke brauchen. Um zu verhindern, dass das Bild **maxY** überschreitet, zwingt dieses Programm alle Blöcke über dem Höhenlimit unter dieses, was allerdings zu Pixelfehlern führen würde.
Dies fällt besonders bei eher einfarbigen Bildern auf, sehr bunte Bilder sind nicht so stark betroffen.

Außer die **-maxY** größer als die Bildhöhe zu setzten ist der beste Weg, damit umzugehen, das Bild in ImageSizeX x 256 oder gar
ImageSizeX x 128 Pixel Gebiete zu zerschneiden, diese einzelne Bereiche eigenständig zu verarbeiten und am Ende die Karten wie gewünscht
zusammen zu fügen.


## Über (mehrere) Schematics
Die Schematic expandiert von dem Block auf dem man steht in Richtung **Osten** und **Süden**. Wenn eine Schematic zwischen (0,0)
und (128,128) platziert werden soll, muss man sich auf (0,0) stellen. Wenn mehrere Schematics generiert werden, werden sie
nach ihrer relativen Platzierung zueinander benannt. PartX0Z1 liegt östlich von partX0Z0, 
partX1Z0 südlich von X0Z0.


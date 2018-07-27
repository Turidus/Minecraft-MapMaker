# Minecraft-MapMaker

This program takes an image and generates multiple files that aid in the generation of Minecraft maps displaying
this image. Contrary to other programs, this does not generate the maps itself.

This program can work with the stepped method, using the full 153 map colors available to
ingame generated maps.

## Generated Files

   A txt file displaying the type and amount of blocks needed

   A txt file displaying the type and position of these blocks

   One or more schematic files for World Edit(see "About large images" below) and compatible plugins to directly import the blocks into Minecraft

   A image showing an approximation of the end result
   
## Usage

### From source code
This program is a Python 3.6 program that depends on [Pillow 5.2](https://pillow.readthedocs.io/en/5.2.x/) and
[appJar](http://appjar.info/).
To use this program, you have to have Python 3.6, Pillow and appJar installed.

After downloading the source code, you can execute the code with a command line tool.
```powershell
   python MapMaker.py "pathToFile" [optional Arguments]
```   
This will generate the above mentioned files. 

The files will be saved into "pathToMapMaker.py"/save/name

### GUI
You can also use the provided GUI by calling MapMaker_GUI.py
```powershell
   python MapMaker_GUI.py
```   
You can still configure all the arguments inside the GUI

### From MapMaker_GUI.exe
**only tested for Windows 10 64bit**  
You can also download the zip file ]MinecraftMapMaker_exe.zip](https://github.com/Turidus/Minecraft-MapMaker/releases/latest). After
unpacking this file into a folder of your choice, you can simply start by using the MapMaker_GUI.exe.
No Python or other dependencies requiered.

### Optional Arguments:

+ *-bl* BaseColorID BaseColorID ...  
  This option lets you block colors, and with that the blocks that make up that colors, that should not be used in the map.
  You can look up the colors and related blocks [here](https://minecraft.gamepedia.com/Map_item_format) or in the BaseColorID file.
      
+ *-n* Name  
  This option lets you name the output files. If not provided, the name will be generated out of the image file name.
  
+ *-twoD*  
  This option switches the program from the stepped method of map generation with 153 colors to the 2D methode with 51 colors.
  Easier to build for the cost of a less faithful result.
  
+ *-p*  
   If provided, this option **turns off** the generation of the result image

+ *-bp*  
   If provided, this option **turns off** the generation of position file
   
+ *-ba*
   If provided, this option **turns off** the generation of the amount file
   
+ *-s*  
   If provided, this option **turns off** the generation of the schematic
   
+ *-minY* 0<=Integer<=251  (Default: 4)  
   This option lets you choose the minimum Y coordinate for your block position file. If you plan on using the schematic,
   you should set this to the level you will be standing on to prevent the schematic to exceed the world height limit.
   Needs to be at least 4 smaller than **-maxY**
   
+ *-maxY* 4<=Integer<=255  (Default: 250)
   This option lets you choose the maximum Y coordinate for your block position file. If maxY is smaller than your image height,
   this can lead to pixel errors on the map (see "About very large images" below). Needs to be at least 4 bigger than **-minY**
   
+ *-maxS* 0<Integer (Default: 129)  
   This option will let you define the maximum size a schematic will have. A to big schematic can seriously impact your server
   when importing the schematic. If the image is bigger than the maximum size of the schematic, the schematic will be split
   into multiple schematics with at most maxS x maxS size. (see "About large images" below)

## About the cobblestone line
When you built/import the construct, you will notice that
there is an **additional line** at the *north* end, made out of cobblestone. This is necessary to prevent
the first line of the image to be miscolored.  
One easy way to deal with this additional line is to place it just out of range of the map, which prevents it from being rendered.
Another way is to replace the line of cobblestones with something that blends with the environment.

## About large images
Large images, 128 x 128 pixels and larger, can heavily impact your server when you import schematics. You should consider using Fast
Asynchron World Edit or similar to prevent your server from freezing up. You can also split up the schematic into smaller chunks
by providing a -maxS value smaller than the image size.

## About very large images
Very large images, 250 x 250 pixels and larger, not only have all the problems large images have,
they also run into the world height limit. Especially if you have large areas with one single color or you have a really large image
(~450 x 450 pixels and larger) a perfect representation of the image would need Y coordinates higher than 256. To prevent the result 
of exceeding this height limit (or any choosen **-maxY**) this program will force any blocks exceeding the maximum allowed Y coordinate
to be below it, but this also introduces misshaded pixels into the final image. These become very noticeable in images with large areas
with a single color, while busy images can deal better with this.

Besides setting the **-maxY** bigger than your image size, the best way to handle this is to cut your image into ImageSizeX x 256 or
even ImageSizeX x 128 pixle areas. These images can then be processed and placed individually.

An additional problem is performance. Very large images can take a while to process, up to multiple minutes depending on your machine.

## About (multiple) schematics
The schematics expand from the block you are standing on towards **East** and **South**. If you want to place a schematic between (0,0)
and (128,128) you have to stand on (0,0). The way you are looking has no impact on it. The upper left pixel of the image will always
spawn on the (x,z) block you are standing, which will be the north-west most block in the construct.
Multiple schematics are named with their relative placement towards each other. PartX0Z1 has to be placed on the east of partX0Z0, 
partX1Z0 has to be placed on the south of X0Z0.

# Minecraft-MapMaker

This is a program that takes an image and generates multiple files that aid in the generation of minecraft maps that
display this image. Contrary to other programs, this does not generates the maps itself.

This program can work with the steped method of building maps, using the full 153 map colors available to
ingame generated maps.

##Generated Files

   A txt file displaying the type and amount of blocks needed

   A txt file displaying the type and position of these blocks

   One or more schematic files for World Edit[1] and compatible plugins to directly import the blocks into minecraft

   A image showing an aproximation of the endresult
   
##Usage

This program is a Python 3.6 program that depends on [Pillow 5.2](https://pillow.readthedocs.io/en/5.2.x/)
To use this program you have to have Python 3.6 and Pillow installed.

After downloading the source code, you can execute the code with a command line tool.


[1] Especially for larger images (128x128 and upwards) you should consider useing Fast Asynchrone World Edit or similar
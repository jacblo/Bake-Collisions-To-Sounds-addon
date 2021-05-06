# Bake-Collisions-To-Sounds-addon
Lets the user bake Object Collisions To Sounds in the Sequencer in Blender 3d

**Instalation**
---------------
 - Download: Bake-Collisions-To-Sounds.py
 - Open Blender.
 - Edit > Prefrences at the top left.
 - Open the Addons page.
 - Click the Install button.
 - Navigate to the downloaded Bake-Collisions-To-Sounds.py file.
 - Select the addon.py file and click Install.
 - Enable the checkbox next to the addon.


**Usage**
---------
 - Perform a rigid body simulation or movement and bake it to keyframes.
 - Select the objects you want to bake.
 - In the 3d viewport, in the object menu, click "Bake Collisions To Sounds".
 - Configure the settings in the popup window, and click OK.
 
 If you want to edit or remove sounds, open the Sequencer editor. The clips appear in the timeline.
 


**Tips**
--------
 - By trial and error, adjust the weights of the objects and the Threshold value for the Bake-Collisions-To-Sounds addon, for best results.
 - The volume setting is 1.0 by default, but adjust the value by trial and error for best results. Values such as 20 or 40 might work better because the volume is lowered based on the collision velocity.

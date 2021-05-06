bl_info = {
    "name": "Bake Collisions To Sounds",
    "author": "JBlock",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "location": "",
    "description": "Lets the user bake Object Collisions To Sounds in the Sequencer",
    "warning": "this is in development so there may be bugs or cases where it might slow blender down",
    "doc_url": "",
    "category": "Physics",
}

import bpy, random
from bpy.props import (
        StringProperty,
        BoolProperty,
        IntProperty,
        FloatProperty,
        FloatVectorProperty,
        EnumProperty,
        )
from bpy.types import Operator



thresh=0.01
sounds=[]
frameStart=0
frameEnd=0
trackSfx=0
frameOffsets= []
volume=2

def getVelocity(object):
    #import pdb; pdb.set_trace()
    currentFrame=bpy.context.scene.frame_current
    currentLoc=object.location.copy()
    bpy.context.scene.frame_set(currentFrame-1)
    lastLoc=object.location.copy()
    bpy.context.scene.frame_set(currentFrame)
    velocityCurrent=currentLoc-lastLoc
    return velocityCurrent

def checkIfOverThresh(object):
    global thresh
    currentFrame=bpy.context.scene.frame_current
    v1=getVelocity(object)
    bpy.context.scene.frame_set(currentFrame-1)
    v2=getVelocity(object)
    bpy.context.scene.frame_set(currentFrame-2)
    v3=getVelocity(object)
    diff1=v2-v1
    diff2=v3-v2
    diff=diff2-diff1
    bpy.context.scene.frame_set(currentFrame)
    if (diff[0]>thresh):
        return [True,diff[0]]
    elif (diff[1]>thresh):
        return [True,diff[1]]
    elif (diff[2]>thresh):
        return [True, diff[2]]
    return [False]

def addSfx(diff):
    global trackSfx, frameOffset, volume
    trackSfx+=1
    soundId=random.randint(0,len(sounds)-1 )
    sound=sounds[soundId]
    if not bpy.context.scene.sequence_editor:
        bpy.context.scene.sequence_editor_create()
    soundstrip = bpy.context.scene.sequence_editor.sequences.new_sound("hit", sound, 1, bpy.context.scene.frame_current+frameOffsets[soundId])
    bpy.context.scene.sequence_editor.sequences.values()[-1].volume=diff*volume

def run():
    currentFrame=bpy.context.scene.frame_current
    for frame in range(frameStart,frameEnd+1):
        bpy.context.scene.frame_set(frame)
        for object in bpy.context.selected_objects:
            check=checkIfOverThresh(object)
            if (check[0]):
                addSfx(check[1])
    bpy.context.scene.frame_set(currentFrame)


class BakeSounds(Operator):
    bl_idname = "object.bakesounds"
    bl_label = "Bake collisions to Sounds"

    # -------------------------------------------------------------------------
    # Source Options
    
    Vol: FloatProperty(
            name="Volume",
            description="The weaker the collision the softer the sound will be. this is a multiplier AFTER that",
            default=1,
            min=0.0
            )
        

    Track: IntProperty(
            name="Track",
            description="What track to put the sounds into",
            default=0,
            min=0
            )

    Thresh: FloatProperty(
            name="Threshold",
            description="Threshold for acceleration change for a sound to be added",
            default=0.01,
            min=0.0
            )
    
    Start_Frame: IntProperty(
            name="Start Frame",
            description="Frame to start at",
            default=0,
            )

    End_Frame: IntProperty(
            name="End frame",
            description="Frame to end at",
            default=250,
            )
                
    Files_Choice: StringProperty(
                name="Files",
                description="Format - file 1, frame offset 1, file 2, frame offset 2, file 3, frame offset 3,...",
                default="",
                )

    

    def execute(self, context):
        global thresh, frameStart, frameEnd, trackSfx, volume, sounds, frameOffsets
        thresh=self.Thresh
        frameStart=self.Start_Frame
        frameEnd=self.End_Frame
        trackSfx=self.Track
        volume=self.Vol
        
        sounds=self.Files_Choice.split(",")[::2]
        frameOffsets= [int(i) for i in self.Files_Choice.split(",")[1::2]]
        
        run()
                
        return {'FINISHED'}


    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self, width=400)

    def draw(self, context):
        layout = self.layout
        
        box = layout.box()
        col = box.column()
        col.label(text="Settings")
        rowsub = col.row(align=True)
        rowsub.prop(self, "Track")
        rowsub = col.row()
        rowsub.prop(self, "Vol")
        rowsub.prop(self, "Thresh")
        
        box = layout.box()
        col = box.column()
        col.label(text="Frame Range")
        rowsub = col.row(align=True)
        rowsub.prop(self, "Start_Frame")
        rowsub.prop(self, "End_Frame")
        
        box = layout.box()
        col = box.column()
        col.label(text="Files (Format - file 1, frame offset 1, file 2, frame offset 2,...)")
        rowsub = col.row(align=True)
        rowsub.prop(self, "Files_Choice")


def menu_func(self, context):
    self.layout.operator(BakeSounds.bl_idname)
    layout = self.layout
    layout.separator()
    layout.operator("object.bake_collisions_to_sounds", text="bake collisions to sounds")


def register():
    bpy.utils.register_class(BakeSounds)
    bpy.types.VIEW3D_MT_object_quick_effects.append(menu_func)
    bpy.types.VIEW3D_MT_object.prepend(menu_func)


def unregister():
    bpy.utils.unregister_class(BakeSounds)
    bpy.types.VIEW3D_MT_object_quick_effects.remove(menu_func)
    bpy.types.VIEW3D_MT_object.remove(menu_func)


if __name__ == "__main__":
    register()
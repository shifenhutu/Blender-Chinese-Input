'''
Copyright (C) 2019 Red Halo Studio(发霉的红地蛋)

Created by Red Halo Studio(发霉的红地蛋)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

bl_info = {  
    "name": "Text Input",  
    "author": "Red Halo Studio",  
    "version": (0, 2),  
    "blender": (2, 80, 0),  
    "location": "Properties > Font > Text Value",  
    "description": "解决Window下无法输入中文的问题",  
    "wiki_url": "",  
    "tracker_url": "",  
    "category": "RedHaloTools"
 }

from typing import Collection
import bpy
from bpy.types import Operator, UIList, PropertyGroup, Panel, Scene
from bpy.props import StringProperty, IntProperty, CollectionProperty, EnumProperty, PointerProperty, BoolProperty
import os

class Tools_OT_insertNewline(Operator):
    bl_idname = "redhalo.insert_newline"
    bl_label = "插入换行符"
    bl_description = "Insert Newline Symbol\n插入换行符"
    bl_options = {'REGISTER', 'UNDO'} 

    def execute(self, context):
        bpy.context.active_object.data.body += "\n"
        return {'FINISHED'}

class Tools_OT_VerticalText(Operator):
    bl_idname = "redhalo.set_vertical"
    bl_label = "改为竖向文字"
    bl_description = "改为竖向文字"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        ob = context.active_object
        txt = ob.data.body[:]

        textArray = ob.data.body.split("\n")

        maxLength = 0

        for i in textArray:
            if len(i) > maxLength:
                maxLength = len(i)
        
        for i, v in enumerate(textArray):

            diff = maxLength - len(v)
            textArray[i] += ("\x20" * diff) #中文空格

        verticalArray = zip(*reversed(textArray))

        verticalStr = ""

        for i, val in enumerate(verticalArray):
            _t = ""
            for j in val:
                _t += j
            verticalStr += _t + "\n"

        verticalStr = verticalStr[:-1]
        
        ob.data.body = verticalStr
        ob.data.align_x = "RIGHT"

        return {'FINISHED'}

class REDHALO_UL_TextMain(UIList):
    # The draw_item function is called for each item of the collection that is visible in the list.
    #   data is the RNA object containing the collection,
    #   item is the current drawn item of the collection,
    #   icon is the "computed" icon for the item (as an integer, because some objects like materials or textures
    #   have custom icons ID, which are not available as enum items).
    #   active_data is the RNA object containing the active property for the collection (i.e. integer pointing to the
    #   active item of the collection).
    #   active_propname is the name of the active property (use 'getattr(active_data, active_propname)').
    #   index is index of the current item in the collection.
    #   flt_flag is the result of the filtering process for this item.
    #   Note: as index and flt_flag are optional arguments, you do not have to use/declare them here if you don't
    #         need them.

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        custom_icon = "OBJECT_DATAMODE"
        layout.label(text='', icon = custom_icon)
        sp = layout.split(factor = 0.2)
        sp.label(text = "Index: %d" % (index))
        sp.prop(item, "name", text="")
        
class REDHALO_OT_InsertLine(Operator):
    """ Insert New Line """
    bl_idname = "redhalo.insert_new_line"
    bl_label = "Insert new line"

    def execute(self, context):
        context.scene.my_list.add()

        return {'FINISH'}

class REDHALO_OT_DeleteLine(Operator):
    ''' Delete the selected item from the list'''

    bl_idname = "redhalo.delete_item"
    bl_label = "Delete seleced item"

    @classmethod
    def poll(cls, context):
        return context.scene.my_list
    
    def excute(self, context):
        my_list = context.scene.my_list
        index = context.scene.list_index

        my_list.remove(index)
        context.scene.list_index = min(max(0, index-1), len(my_list)-1)

        return {'FINISH'}

class RD_PT_TextValue(Panel):
    bl_label = "Text Value"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    
    @classmethod
    def poll(cls, context):
        active = bpy.context.active_object
        if active is not None:
            active_type=active.type
        else:
            active_type=""
        return active_type=='FONT'

    def draw(self, context): 
        layout = self.layout

        scene = context.scene

        obj = context.object
        row = layout.row()
        row.prop(obj.data, "body", text="", icon="OUTLINER_OB_FONT",expand =True )
        row = layout.row()
        row.operator("redhalo.insert_newline", icon = "CHECKMARK")
        row.operator("redhalo.set_vertical", icon = "DRIVER_ROTATIONAL_DIFFERENCE")
        
classes = (
    Tools_OT_insertNewline,
    Tools_OT_VerticalText,
    REDHALO_UL_TextMain,
    RD_PT_TextValue
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

import bpy
from .core import register_core, unregister_core

bl_info = {
    "name": "Building Tools",
    "author": "Ian Ichung'wa Karanja (ranjian0)",
    "version": (0, 9, 7),
    "blender": (2, 80, 0),
    "location": "View3D > Toolshelf > Building Tools",
    "description": "Building Creation Tools",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh",
}


class BTOOLS_PT_mesh_tools(bpy.types.Panel):

    bl_label = "Mesh Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Building Tools"

    def draw(self, context):
        layout = self.layout

        # Draw Operators
        # ``````````````
        col = layout.column(align=True)
        col.operator("btools.add_floorplan")
        col.operator("btools.add_floors")

        col = layout.column(align=True)
        row = col.row(align=True)
        row.operator("btools.add_window")
        row.operator("btools.add_door")
        col.operator("btools.add_multigroup")

        col = layout.column(align=True)
        col.operator("btools.add_stairs")
        col.operator("btools.add_roof")


class BTOOLS_PT_material_tools(bpy.types.Panel):

    bl_label = "Material Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Building Tools"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        obj = context.object
        return obj and obj.type == "MESH"

    def draw(self, context):
        layout = self.layout

        ob = context.object
        facemap = ob.face_maps.active

        rows = 2
        if facemap:
            rows = 4

        if not len(ob.face_maps):
            return

        layout.label(text="Face Maps")

        row = layout.row()
        args = ob, "face_maps", ob.face_maps, "active_index"
        row.template_list("BTOOLS_UL_fmaps", "", *args, rows=rows)

        col = row.column(align=True)
        col.operator("object.face_map_add", icon="ADD", text="")
        col.operator("object.face_map_remove", icon="REMOVE", text="")
        col.separator()
        col.operator("btools.face_map_clear", icon="TRASH", text="")

        if ob.face_maps and (ob.mode == "EDIT" and ob.type == "MESH"):
            row = layout.row()

            sub = row.row(align=True)
            sub.operator("object.face_map_assign", text="Assign")
            sub.operator("object.face_map_remove_from", text="Remove")

            sub = row.row(align=True)
            sub.operator("object.face_map_select", text="Select")
            sub.operator("object.face_map_deselect", text="Deselect")

        layout.label(text="Active Face Map Material")
        if ob.face_maps:
            face_map_index = ob.face_maps.active_index
            face_map_material = ob.facemap_materials[face_map_index]
            layout.template_ID_preview(face_map_material, "material", hide_buttons=True)


classes = (BTOOLS_PT_mesh_tools, BTOOLS_PT_material_tools)


def register():
    register_core()
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    unregister_core()
    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    import os
    os.system("clear")

    # -- custom unregister for script watcher
    for tp in dir(bpy.types):
        if 'BTOOLS_' in tp:
            bpy.utils.unregister_class(getattr(bpy.types, tp))

    register()

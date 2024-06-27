import bpy

class SimpleBakePanel(bpy.types.Panel):
    bl_label = "Simple Bake"
    bl_idname = "RENDER_PT_simple_bake"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Simple Bakeボタン
        row = layout.row()
        row.operator("object.simple_bake_operator", text="Simple Bake")

        # Auto Save チェックボックス
        row = layout.row()
        row.prop(scene, "simple_bake_auto_save", text="Auto Save")

        # Bake Type ラジオボタン
        layout.label(text="Bake Type")
        layout.prop(scene, "simple_bake_type", expand=True)


class BakeSettingsPanel(bpy.types.Panel):
    bl_label = "Bake Settings"
    bl_idname = "RENDER_PT_bake_settings"
    bl_parent_id = "RENDER_PT_simple_bake"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        # Bake Settingsの項目
        col = layout.column(align=True)
        col.prop(scene, "simple_bake_uv_channel", text="Set Bake UV")
        col.prop(scene, "simple_bake_return_to_original_uv", text="Return to Selected UV")
        
        # Samples ラジオボタン
        col.label(text="Samples")
        row = col.row(align=True)
        row.prop(scene, "simple_bake_samples", expand=True)
        
        # Return to Render Samples チェックボックス
        col.prop(scene, "simple_bake_return_to_render_samples", text="Return to Render Samples")


class TextureManagerPanel(bpy.types.Panel):
    bl_label = "Texture Manager"
    bl_idname = "RENDER_PT_texture_manager"
    bl_parent_id = "RENDER_PT_simple_bake"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "render"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout

        # Texture Managerの項目
        layout.operator("object.simple_bake_add_textures", text="Add")
        layout.operator("object.simple_bake_remove_textures", text="Remove")


def register():
    bpy.utils.register_class(SimpleBakePanel)
    bpy.utils.register_class(BakeSettingsPanel)
    bpy.utils.register_class(TextureManagerPanel)


def unregister():
    bpy.utils.unregister_class(SimpleBakePanel)
    bpy.utils.unregister_class(BakeSettingsPanel)
    bpy.utils.unregister_class(TextureManagerPanel)

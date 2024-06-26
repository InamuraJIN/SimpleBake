import bpy
import re

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
        row.enabled = self.is_bake_possible(context)
        row.operator("object.simple_bake_operator", text="Simple Bake")

        # メッセージボックス
        row = layout.row()
        message, texture_name = self.get_bake_message(context)
        row.label(text=message)
        row.operator("object.dummy_operator", text=texture_name if texture_name else "Not Selected", depress=True)

        # Auto Save チェックボックス
        row = layout.row()
        row.prop(scene, "simple_bake_auto_save", text="Auto Save")

        # Bake Type ラジオボタン
        layout.label(text="Bake Type")
        layout.prop(scene, "simple_bake_type", expand=True)

    def is_bake_possible(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            if obj.material_slots:
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.use_nodes:
                        active_node = self.get_active_image_node(context, mat_slot.material.node_tree)
                        if active_node and active_node.type == 'TEX_IMAGE':
                            return True
        return False

    def get_bake_message(self, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            if obj.material_slots:
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.use_nodes:
                        active_node = self.get_active_image_node(context, mat_slot.material.node_tree)
                        if active_node and active_node.type == 'TEX_IMAGE' and active_node.image:
                            texture_name = self.clean_texture_name(active_node.image.name, mat_slot.material.name)
                            return "Bake to", texture_name
                return "Bake to", "Not Selected"
            else:
                return "Bake to", "Not Selected"
        else:
            return "Bake to", "Not Selected"

    def get_active_image_node(self, context, node_tree):
        for area in context.screen.areas:
            if area.type == 'NODE_EDITOR':
                for space in area.spaces:
                    if space.type == 'NODE_EDITOR' and space.node_tree == node_tree:
                        return space.node_tree.nodes.active
        return None

    def clean_texture_name(self, texture_name, material_name):
        # マテリアル名を除去
        cleaned_name = re.sub(f"^{re.escape(material_name)}", "", texture_name)
        # 拡張子と以降の文字列を除去
        cleaned_name = re.sub(r"\..*$", "", cleaned_name)
        return cleaned_name

class DummyOperator(bpy.types.Operator):
    bl_idname = "object.dummy_operator"
    bl_label = "Dummy Operator"

    def execute(self, context):
        return {'FINISHED'}

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
    bpy.utils.register_class(DummyOperator)


def unregister():
    bpy.utils.unregister_class(SimpleBakePanel)
    bpy.utils.unregister_class(BakeSettingsPanel)
    bpy.utils.unregister_class(TextureManagerPanel)
    bpy.utils.unregister_class(DummyOperator)

import bpy
import os

class SimpleBakeAddTexturesOperator(bpy.types.Operator):
    bl_idname = "object.simple_bake_add_textures"
    bl_label = "Add Textures"
    bl_options = {'REGISTER', 'UNDO'}

    name: bpy.props.StringProperty(name="Name")
    image_size: bpy.props.EnumProperty(
        name="Image Size",
        description="Set the size of the image",
        items=[
            ('256', "256", ""),
            ('512', "512", ""),
            ('1024', "1024", ""),
            ('2048', "2048", ""),
            ('4096', "4096", "")
        ],
        default='1024'
    )
    base: bpy.props.BoolProperty(name="Base", default=True)
    roughness: bpy.props.BoolProperty(name="Roughness", default=True)
    metallic: bpy.props.BoolProperty(name="Metallic", default=True)
    normal: bpy.props.BoolProperty(name="Normal", default=True)

    @classmethod
    def poll(cls, context):
        # マテリアルを含んだオブジェクトが選択されているかどうかを確認
        for obj in context.selected_objects:
            if obj.type == 'MESH' and obj.material_slots:
                return True
        return False

    def execute(self, context):
        scene = context.scene
        material_names = set()

        # アクティブなオブジェクトを取得し、アクティブなマテリアルを追加
        obj = context.active_object
        if obj and obj.type == 'MESH' and obj.active_material:
            material_names.add(obj.active_material.name)
        
        created_textures = []
        for mat_name in material_names:
            name_prefix = self.name if self.name else mat_name
            if self.base:
                created_textures.append((self.create_texture(name_prefix, "Base"), "Base"))
            if self.roughness:
                created_textures.append((self.create_texture(name_prefix, "Roughness"), "Roughness"))
            if self.metallic:
                created_textures.append((self.create_texture(name_prefix, "Metallic"), "Metallic"))
            if self.normal:
                created_textures.append((self.create_texture(name_prefix, "Normal"), "Normal"))

        # Shader Editorにノードを追加
        self.add_nodes_to_shader_editor(context, created_textures)

        self.report({'INFO'}, "Textures added and nodes created")
        return {'FINISHED'}

    def create_texture(self, mat_name, suffix):
        image_name = f"{mat_name}{suffix}.png"
        size = int(self.image_size)
        image = bpy.data.images.new(name=image_name, width=size, height=size)
        # Removed code to set the filepath and save the image
        return image

    def add_nodes_to_shader_editor(self, context, textures):
        y_offset = 0
        for area in context.screen.areas:
            if area.type == 'NODE_EDITOR':
                for space in area.spaces:
                    if space.type == 'NODE_EDITOR' and space.edit_tree and space.edit_tree.type == 'SHADER':
                        tree = space.edit_tree
                        
                        # Principled BSDFノードを追加
                        principled_node = tree.nodes.new(type='ShaderNodeBsdfPrincipled')
                        principled_node.location = (100, 520)
                        principled_node.width = 140
                        for socket in principled_node.inputs:
                            if socket.name not in {"Base Color", "Metallic", "Roughness", "Normal"}:
                                socket.hide = True
                        
                        for texture, label in textures:
                            if texture is None:
                                continue
                            node = tree.nodes.new(type='ShaderNodeTexImage')
                            node.image = texture
                            node.location = (-60, 520 - y_offset)
                            node.width = 140
                            node.hide = True
                            node.label = label
                            if label == "Base":
                                tree.links.new(node.outputs['Color'], principled_node.inputs['Base Color'])
                            elif label == "Roughness":
                                tree.links.new(node.outputs['Color'], principled_node.inputs['Roughness'])
                            elif label == "Metallic":
                                tree.links.new(node.outputs['Color'], principled_node.inputs['Metallic'])
                            elif label == "Normal":
                                node.image.colorspace_settings.name = 'Non-Color'
                                normal_map_node = tree.nodes.new(type='ShaderNodeNormalMap')
                                normal_map_node.location = (node.location.x, node.location.y - 40)
                                normal_map_node.width = 140
                                normal_map_node.hide = True
                                tree.links.new(node.outputs['Color'], normal_map_node.inputs['Color'])
                                tree.links.new(normal_map_node.outputs['Normal'], principled_node.inputs['Normal'])
                            y_offset += 40
                        return

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "name", text="Name")
        layout.prop(self, "image_size", text="Image Size")
        layout.prop(self, "base", text="Base")
        layout.prop(self, "roughness", text="Roughness")
        layout.prop(self, "metallic", text="Metallic")
        layout.prop(self, "normal", text="Normal")


class SimpleBakeRemoveTexturesOperator(bpy.types.Operator):
    bl_idname = "object.simple_bake_remove_textures"
    bl_label = "Remove Textures"
    bl_options = {'REGISTER', 'UNDO'}

    images_to_remove: bpy.props.CollectionProperty(type=bpy.types.PropertyGroup)

    @classmethod
    def poll(cls, context):
        # Render ResultとViewer Nodeを除外して、それ以外に画像ファイルが無い場合はボタンを無効にする
        for img in bpy.data.images:
            if img.name not in {"Render Result", "Viewer Node"}:
                return True
        return False

    def invoke(self, context, event):
        self.images_to_remove.clear()
        for img in bpy.data.images:
            if img.name not in {"Render Result", "Viewer Node"}:
                item = self.images_to_remove.add()
                item.name = img.name
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.label(text="Select textures to remove:")
        box = layout.box()
        for item in self.images_to_remove:
            row = box.row()
            row.prop(item, "select", text="")
            row.label(text=item.name)

    def execute(self, context):
        for item in self.images_to_remove:
            if item.select:
                img = bpy.data.images.get(item.name)
                if img:
                    bpy.data.images.remove(img)
        self.report({'INFO'}, "Selected textures removed")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(SimpleBakeAddTexturesOperator)
    bpy.utils.register_class(SimpleBakeRemoveTexturesOperator)
    bpy.types.PropertyGroup.select = bpy.props.BoolProperty(name="Select")


def unregister():
    bpy.utils.unregister_class(SimpleBakeAddTexturesOperator)
    bpy.utils.unregister_class(SimpleBakeRemoveTexturesOperator)
    del bpy.types.PropertyGroup.select

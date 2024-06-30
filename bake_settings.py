import bpy

class SimpleBakeOperator(bpy.types.Operator):
    bl_idname = "object.simple_bake_operator"
    bl_label = "Simple Bake Operator"

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        if obj and obj.type == 'MESH':
            if obj.material_slots:
                for mat_slot in obj.material_slots:
                    if mat_slot.material and mat_slot.material.use_nodes:
                        active_node = cls.get_active_image_node(context, mat_slot.material.node_tree)
                        if active_node and active_node.type == 'TEX_IMAGE':
                            return True
        return False

    def execute(self, context):
        scene = context.scene
        uv_channel = scene.simple_bake_uv_channel
        return_to_original = scene.simple_bake_return_to_original_uv
        bake_type = scene.simple_bake_type
        auto_save = scene.simple_bake_auto_save
        return_to_render_samples = scene.simple_bake_return_to_render_samples

        original_uv_indices = {}
        original_render_samples = scene.cycles.samples  # 元のRender Samplesを保存

        valid_objects = [obj for obj in context.selected_objects if obj.type == 'MESH' and obj.data.uv_layers and obj.material_slots]

        if not valid_objects:
            self.report({'ERROR'}, "Select the object that contains the material")
            return {'CANCELLED'}

        for obj in valid_objects:
            original_uv_indices[obj.name] = obj.data.uv_layers.active_index
            if 0 <= uv_channel < len(obj.data.uv_layers):
                obj.data.uv_layers.active_index = uv_channel
            else:
                self.report({'WARNING'}, f"Object {obj.name} has no UV layer at index {uv_channel}")

        try:
            # Samplesの設定
            cycles = scene.cycles
            cycles.samples = int(scene.simple_bake_samples)

            # ベイク設定を行い、ターゲットイメージにベイクを実行
            scene.cycles.bake_type = bake_type
            scene.render.bake.use_selected_to_active = False
            scene.render.bake.use_cage = False
            scene.render.bake.cage_extrusion = 0.1
            scene.render.bake.use_clear = True
            scene.render.bake.margin = 16

            # 画像が未初期化の場合は初期化
            for img in bpy.data.images:
                if not img.has_data:
                    new_img = bpy.data.images.new(
                        name=img.name,
                        width=1024,  # 適切な幅に設定
                        height=1024,  # 適切な高さに設定
                        alpha=True,  # アルファチャンネルを有効にする
                        float_buffer=False,  # フロートバッファを無効にする
                    )
                    new_img.file_format = 'PNG'
                    bpy.data.images.remove(img)
                    img = new_img

            bpy.ops.object.bake(type=bake_type)
        except Exception as e:
            # エラーが発生した場合でもRender Samplesを元に戻す
            if return_to_render_samples:
                scene.cycles.samples = original_render_samples
            self.report({'ERROR'}, f"Bake failed: {e}")
            return {'CANCELLED'}

        # ベイクが終わったら元のUVチャンネルに戻す
        if return_to_original:
            for obj in valid_objects:
                obj.data.uv_layers.active_index = original_uv_indices.get(obj.name, uv_channel)

        # 元のRender Samplesに戻す
        if return_to_render_samples:
            scene.cycles.samples = original_render_samples

        # Auto Saveが有効な場合、PCに保存されている画像を上書き保存
        if auto_save:
            for img in bpy.data.images:
                if img.has_data and img.filepath_raw:  # ローカルに保存されている場合
                    try:
                        img.save()
                    except RuntimeError as e:
                        self.report({'ERROR'}, f"Could not save image {img.name}: {e}")

        self.report({'INFO'}, "Bake completed")
        return {'FINISHED'}

    @classmethod
    def get_active_image_node(cls, context, node_tree):
        for area in context.screen.areas:
            if area.type == 'NODE_EDITOR':
                for space in area.spaces:
                    if space.type == 'NODE_EDITOR' and space.node_tree == node_tree:
                        return space.node_tree.nodes.active
        return None


def register():
    bpy.utils.register_class(SimpleBakeOperator)
    bpy.types.Scene.simple_bake_type = bpy.props.EnumProperty(
        name="Bake Type",
        description="Choose the type of bake",
        items=[
            ('EMIT', "Emit", ""),
            ('NORMAL', "Normal", ""),
            ('SHADOW', "Shadow", ""),
            ('AO', "AO", "")
        ],
        default='EMIT'
    )
    bpy.types.Scene.simple_bake_samples = bpy.props.EnumProperty(
        name="Samples",
        description="Set the number of samples for rendering",
        items=[
            ('1', "1", ""),
            ('8', "8", ""),
            ('64', "64", ""),
            ('256', "256", ""),
            ('1024', "1024", "")
        ],
        default='1'
    )
    bpy.types.Scene.simple_bake_return_to_render_samples = bpy.props.BoolProperty(
        name="Return to Render Samples",
        description="Return to the original Render Samples after baking",
        default=True
    )


def unregister():
    bpy.utils.unregister_class(SimpleBakeOperator)
    del bpy.types.Scene.simple_bake_type
    del bpy.types.Scene.simple_bake_samples
    del bpy.types.Scene.simple_bake_return_to_render_samples

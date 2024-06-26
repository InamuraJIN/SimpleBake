import bpy

class SimpleBakeOperator(bpy.types.Operator):
    bl_idname = "object.simple_bake_operator"
    bl_label = "Simple Bake Operator"

    def execute(self, context):
        scene = context.scene
        uv_channel = scene.simple_bake_uv_channel
        return_to_original = scene.simple_bake_return_to_original_uv
        bake_type = scene.simple_bake_type
        auto_save = scene.simple_bake_auto_save

        original_uv_indices = {}

        for obj in context.selected_objects:
            if obj.type == 'MESH':
                if obj.data.uv_layers:
                    original_uv_indices[obj.name] = obj.data.uv_layers.active_index
                    if 0 <= uv_channel < len(obj.data.uv_layers):
                        obj.data.uv_layers.active_index = uv_channel
                    else:
                        self.report({'WARNING'}, f"Object {obj.name} has no UV layer at index {uv_channel}")
                else:
                    self.report({'WARNING'}, f"Object {obj.name} has no UV layers")
                    continue
        
        # Samplesの設定
        cycles = scene.cycles
        cycles.samples = int(scene.simple_bake_samples)
        
        # Denoisingの設定
        scene.cycles.use_denoising = scene.simple_bake_denoise

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

        # ベイクが終わったら元のUVチャンネルに戻す
        if return_to_original:
            for obj in context.selected_objects:
                if obj.type == 'MESH' and obj.data.uv_layers:
                    obj.data.uv_layers.active_index = original_uv_indices.get(obj.name, uv_channel)

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
    bpy.types.Scene.simple_bake_denoise = bpy.props.BoolProperty(
        name="Denoise",
        description="Enable or disable denoising",
        default=False
    )


def unregister():
    bpy.utils.unregister_class(SimpleBakeOperator)
    del bpy.types.Scene.simple_bake_type
    del bpy.types.Scene.simple_bake_samples
    del bpy.types.Scene.simple_bake_denoise

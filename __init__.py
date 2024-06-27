bl_info = {
    "name": "Simple Bake",
    "blender": (3, 6, 0),
    "category": "Render",
    "location": "Properties > Render",
    "author": "InamuraJIN",
    "version": (2, 1),
}

import bpy
from . import ui, bake_settings, texture_manager

def register():
    ui.register()
    bake_settings.register()
    texture_manager.register()
    
    # Samples用のプロパティを定義
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
    
    # UVチャンネル用のプロパティを定義
    bpy.types.Scene.simple_bake_uv_channel = bpy.props.IntProperty(
        name="Set Bake UV",
        description="Set the UV channel to be used for baking",
        default=0,
        min=0,
        max=10
    )
    
    # 元のUVチャンネルに戻すかどうかのチェックボックスプロパティを定義
    bpy.types.Scene.simple_bake_return_to_original_uv = bpy.props.BoolProperty(
        name="Return to Selected UV",
        description="Return to the selected UV channel after baking",
        default=True
    )

    # Bake Type用のプロパティを定義
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

    # Auto Save用のプロパティを定義
    bpy.types.Scene.simple_bake_auto_save = bpy.props.BoolProperty(
        name="Auto Save",
        description="Automatically save the image after baking",
        default=False
    )

    # Render Samplesを元に戻すプロパティを定義
    bpy.types.Scene.simple_bake_return_to_render_samples = bpy.props.BoolProperty(
        name="Return to Render Samples",
        description="Return to the original Render Samples after baking",
        default=True
    )


def unregister():
    ui.unregister()
    bake_settings.unregister()
    texture_manager.unregister()
    
    # プロパティを削除
    del bpy.types.Scene.simple_bake_samples
    del bpy.types.Scene.simple_bake_uv_channel
    del bpy.types.Scene.simple_bake_return_to_original_uv
    del bpy.types.Scene.simple_bake_type
    del bpy.types.Scene.simple_bake_auto_save
    del bpy.types.Scene.simple_bake_return_to_render_samples


if __name__ == "__main__":
    register()

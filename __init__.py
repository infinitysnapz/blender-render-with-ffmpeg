import bpy
import os
import sys
import subprocess
from tempfile import gettempdir

def render_ffmpeg(ffparam,ffext):
    
    old_filePath = bpy.context.scene.render.filepath
    old_settings = bpy.context.scene.render.image_settings.file_format
    
    temp_render_path=os.path.join(gettempdir(), 'Blender_Render_Temp')
    try:
        os.makedirs(temp_render_path)
    except FileExistsError:
        pass
    
    
    bpy.context.scene.render.filepath = os.path.join(temp_render_path, 'temp')
    bpy.context.scene.render.image_settings.file_format = "PNG"
    bpy.context.scene.render.image_settings.color_mode  = "RGBA"
    
    bpy.ops.render.render(animation=True)
    #bpy.ops.render.render(override,animation=True)
    
    # get render settings fps and framestart
    startFrame = bpy.context.scene.frame_start
    fps = bpy.context.scene.render.fps
    
    bpy.context.scene.render.filepath = old_filePath
    bpy.context.scene.render.image_settings.file_format = old_settings
    
    finalRenderPath = bpy.path.ensure_ext(bpy.path.abspath(old_filePath),ffext) # filename for ffmpeg 

    cmdParameters=f'ffmpeg -framerate {fps} -start_number {startFrame} -i {temp_render_path}\\temp%04d.png {ffparam} -y "{finalRenderPath}"'
    print(cmdParameters)
    #print(cmdParameters)
    os.system(cmdParameters)
    
    for file in os.scandir(temp_render_path):
        os.remove(file.path)


class OT_render_ffmpeg(bpy.types.Operator):
    """Create a PNG image sequence, then convert it to a video via FFmpeg."""
    bl_idname = "output.renderffmpeg"
    bl_label = "Render with FFmpeg"

    def execute(self, context):
        render_ffmpeg(context.scene.ffmpeg_input,context.scene.ffmpeg_ext)
        
        return {"FINISHED"}


class PT_FFmpegPanel(bpy.types.Panel):
    bl_idname = "OUTPUT_PT_RENDER_FFMPEG"
    bl_label = "Render with FFmpeg"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="FFMPEG render (will freeze whilst rendering!)")
        layout.prop(context.scene, 'ffmpeg_input')
        layout.prop(context.scene, 'ffmpeg_ext')
        layout.operator("output.renderffmpeg", text="Render with FFmpeg")
        
        
        
def register():
    bpy.utils.register_class(PT_FFmpegPanel)
    bpy.utils.register_class(OT_render_ffmpeg)
    bpy.types.Scene.ffmpeg_input = bpy.props.StringProperty(name='Input')
    bpy.types.Scene.ffmpeg_ext = bpy.props.StringProperty(name='Extension')


def unregister():
    bpy.utils.unregister_class(PT_FFmpegPanel)
    bpy.utils.unregister_class(OT_render_ffmpeg)
    del bpy.types.Scene.ffmpeg_input
    del bpy.types.Scene.ffmpeg_ext


if __name__ == "__main__":
    register()

    

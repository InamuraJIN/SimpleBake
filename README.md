# INTRODUCTION
A tool that consolidates the most commonly used settings for baking in Blender to reduce errors in your work

## Main functions
### Simple Bake button
Change settings and execute the bake, reducing mistakes.
### Bake Type Selection
Allows you to select only the most frequently used types (Emit, Normal, Shadow, and AO)
### Sample size setting
Set the number of samples to be baked with a single click.
### Auto save function
Choose whether or not to automatically save the baked image
### UV Settings
Set the UV channel for baking and have the option to restore the original UV channel after baking
### Texture Management
Add new textures with a single click or delete unwanted images.

# Install

![image](https://github.com/InamuraJIN/SimpleBake/assets/60126349/accd6f34-5e23-4259-bbf5-224541eb8a7f)

Press the Code> Download ZIP button to download the zip file
Open Blender Preferences, go to the Add-ons tab and press the Install button

![image](https://github.com/InamuraJIN/SimpleBake/assets/60126349/c97d7d05-4863-47e3-baae-30f258551d5e)

Go to the downloaded folder and double-click the file or press the Install Addon button
Enable the Simple Bake add-on

# HOW TO USE

![image](https://github.com/InamuraJIN/SimpleBake/assets/60126349/3c5d1367-ae78-4d99-bb1d-1a7f30db81c3)

The Simple Bake panel appears in Render Property
Open the Bake Settings and Texture Manager sub-panels and various buttons will appear

## Simple Bake: Performs a bake on the active selected object

Auto Save: Automatically saves the image after baking is complete
    (Only files that have been saved locally will be saved)

Bake Type: Selects the type of baking
		(Emit, Normal, Shadow, AO(Ambient Occlusion))

## Bake Settings
├ Set Bake UV: Sets the UV channel to be used for baking
├ Return to Selected UV: Returns to the selected UV channel
├ Samples: Sets the number of samples used for baking
└ Denoise: Enables denoise processing.

## Texture Manager
Add: adds a texture to the selected object's material
└ Remove: Deletes a texture in the Blend data

![image](https://github.com/InamuraJIN/SimpleBake/assets/60126349/c846939b-18ba-4f38-bf15-9d979dd623e3)

## Add Textures pop-up panel

Name: Change the prefix of the texture
If no name is entered, the material name will be used as the prefix

Image Size: Specify the texture size
Only squares are supported

Base, Roughness, Metallic, Normal: A new image will be created with the checkboxes enabled

OK: The texture enabled above will be added to the Shader Editor for the selected material

![image](https://github.com/InamuraJIN/SimpleBake/assets/60126349/9bf12e3a-c348-4d15-afc1-7a3b868a213b)

## Remove Texture pop-up panel

The texture selected here will be completely removed from the Blend file when the OK button is pressed

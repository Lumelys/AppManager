# App Manager

<img src="Path_to_your_image/image_file.jpg">

App Manager is a python application built with Tkinter to help you manage your softwares simply and efficiently.

## Overview

You will see your applications displayed on a UI, and modify them on a text file.

The python libraries being used are :
```
customtkinter
messagebox, filedialog from tkinter
ToolTip from tktooltip
Image, ImageDraw, ImageFont from pillow
pywinstyles
webbbrowser
json

exists from os.path
platfrom from sys
win32ui
win32gui
win32con
win32api
sys
os
```

## Usage

The executable comes with 2 files. The ```IconData``` folder and ```ApplicationData.json``` file must stay in the same folder as the executable.
When you add or remove an application from the configuration file ```ApplicationData.json```, you must use the same syntax ; the App Manager will get the application informations from this specific file. If you modify it, you will need to restart the application in order for the changes to take effect.

The Configuration file must respect json syntax
(note that ImagePath must contain the full executable name - e.g. ```AppManager.exe``` - followed by .bmp,  ```Tags``` do not need an #, and if you do not want an image for your application or want to add a website you must put as the Imagepath value ```icon.ico``` ) :
```json
{
    "App0": {
        "ImagePath": "AppManager.exe.bmp",
        "Name": "App Manager",
        "Link": "https://github.com/Lumelys/AppManager",
        "Description": "App Manager that keeps my favorite applications' download link",
        "Tags": "#App, #Software, #Manage, #Tool",
        "Size": "<1"
    },
    "App1": {
        "ImagePath": "icon.ico",
        "Name": "Github",
        "Link": "https://github.com",
        "Description": "GitHub is a developer platform that allows developers to create, store, manage and share their code",
        "Tags": "#Development, #git, #CLI, #Project, #Open Source",
        "Size": "0"
    }
}
```
You will be able to extract an executable's icon from the edit menu, if you select it in the filedialog and use ```Save exectuable icon and open configuration file```.

## Errors
You will be prompted by an warning message if it is the first time you open the application, or if the configuration file could not be read properly.

## Limitations
This was made in a few months as a very first project.
Adding applications should have been implemented as a UI element, such as deleting or editing. The configuration file should not have been in the same folder as the executable, such as the ```IconData``` folder. This might not be the perfect finished product I was expecting, but it made me learn quite a few things related to python and github. This was a big project and hopefully a great tool for you.

This project probably won't get updated at all.
You are free to modify the application, change the way it looks, or works. But remember it was made with love.
## License

[MIT](https://choosealicense.com/licenses/mit/)

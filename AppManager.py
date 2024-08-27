import customtkinter as ctk
from customtkinter import CTkLabel as CTkImage
from tkinter import messagebox, filedialog
from tktooltip import ToolTip
from PIL import Image, ImageDraw, ImageFont
import json
from os.path import exists
import webbrowser
from sys import platform
import pywinstyles

import sys
import os
import win32ui
import win32gui
import win32con
import win32api

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Define Current focused App
FocusedAppID = 0

#Error Handling
ApplicationDataCreated = False

#File Manipulation
def OverwriteApplicationData():
    global FileData
    FileData = {
                    "App0": {
                        "ImagePath": "icon.ico",
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
    with open(resource_path("ApplicationData.json"),"w") as FileHandler:
        json.dump(FileData, FileHandler, indent= 4)

ConfigFileMissing = False
if not exists(resource_path("ApplicationData.json")):
    OverwriteApplicationData()
    ConfigFileMissing = True

try:
    with open(resource_path("ApplicationData.json"),"r") as FileHandler:
        FileData = json.load(FileHandler)
except:
    MessageBoxWindow = ctk.CTk()
    MessageBoxWindow.iconbitmap(resource_path("IconData\icon.ico"))
    messagebox.showerror("Error","ApplicationData.json could not be read. Please delete or edit its content to make it valid.")
    exit()

def SaveDataToFile():
    global FileData
    with open(resource_path("ApplicationData.json"), "w") as FileHandler:
        json.dump(FileData, FileHandler, indent=4)

print(json.dumps(FileData, indent= 2)) 
AppDataCount = sum(1 for app in FileData.values())

#Application window
class root(ctk.CTk):
    def __init__(self):

        #Window Setup
        super().__init__()
        ctk.set_appearance_mode("dark")
        self.title("App Manager")
        self.iconbitmap(resource_path("IconData\icon.ico"))
        #self.attributes("-topmost", True)
        self.minsize(450, 200)

        if ConfigFileMissing:
            global ApplicationDataCreated
            ApplicationDataCreated = True
            messagebox.showwarning("Configuration file missing!","It appears to be the first time you are running this application, or no configuration file was found in the executable's folder. A placeholder file ApplicationData.json was created in the executable's folder. This file can be manually edited but cannot be placed in a different directory as the executable.")


        #windowLenX = 800
        #windowLenY = 600
        #windowPosX = int(self.winfo_screenwidth()/2-windowLenX/2)
        #windowPosY = int(self.winfo_screenheight()/2-windowLenY/2)
        #self.geometry(f"{700}x{500}+{windowPosX}+{windowPosY}")
        self.geometry("1000x600+460+240")

        #Define Search by Tag and Search by Name toggles
        global SearchByTag
        global SearchByName
        SearchByTag = ctk.StringVar(value="True")
        SearchByName = ctk.StringVar(value="True")

        #Window content
        AppsFrame = ctk.CTkFrame(self)
        self.TopMenu = TopMenu(self)
        self.AppDetails = AppDetails(AppsFrame)
        self.AppSearch = AppSearch(AppsFrame)
        AppsFrame.pack(expand= True, fill= "both")
        #AppsFrame.place(relx=0, rely=0.1, relwidth= 1, relheight= 0.95)

        #Run Window
        self.mainloop()

class TopMenu(ctk.CTkFrame):
    def __init__(self, parent):

        super().__init__(parent, fg_color= "#121212", background_corner_colors= ("#121212", "#121212", "#121212", "#121212"))
        self.place(relx=0, rely=0, relwidth= 1, relheight= 0.05)

        #self.AppsFrameTab = ctk.CTkLabel(self, text="hoho", fg_color= "pink", cursor= "hand2")
        #self.AppsFrameTab.bind("<Button-1>", lambda event: print("AppsFrameTab Opened"))
        #self.AppsFrameTab.pack(side= "left")

        self.Help = ctk.CTkLabel(self, text="Help", fg_color= "#2A2A2A", cursor= "hand2", corner_radius= 4, font= ctk.CTkFont("Tahoma", 14, weight= "bold"))
        self.Help.bind("<Button-1>", lambda event: messagebox.showinfo("How to use App Manager", 
                                                                       "The executable comes with 2 files. The IconData folder and "
                                                                       "configuration file ApplicationData.json file must stay in the same folder "
                                                                       "as the executable.\n\nWhen you add or remove an application from the "
                                                                       "configuration file ApplicationData.json, you must use the same syntax ; "
                                                                       "the App Manager will get the application informations from this specific "
                                                                       "file.\nIf you modify it, you will need to restart the application in order "
                                                                       "for the changes to take effect.\n\nYou will be able to extract an executable's "
                                                                       "icon from the edit menu, if you select it in the filedialog and use "
                                                                       "[Save exectuable icon and open configuration file]."
                                                                       "\n\nIn the configuration file (see also github Usage section), for a correct "
                                                                       "syntax, ImagePath must contain the full executable name - e.g. "
                                                                       "AppManager.exe - followed by .bmp, Tags do not need an #, and if you do "
                                                                       "not want an image for your application or want to add a website you must "
                                                                       "put as the Imagepath value [icon.ico]."))
        self.Help.pack(side= "left", padx= 5, ipadx= 5)

        self.OpenGithubTab = ctk.CTkLabel(self, text="Open Github page", fg_color= "#2A2A2A", corner_radius= 4, cursor= "hand2", font= ctk.CTkFont("Tahoma", 14, weight= "bold"))
        self.OpenGithubTab.bind("<Button-1>", lambda event: webbrowser.open("https://github.com/Lumelys/AppManager"))
        self.OpenGithubTab.pack(side= "left", ipadx= 5)
        ToolTip(self.OpenGithubTab, msg= "https://github.com/Lumelys/AppManager", delay= 0, fg= "#ffffff", background= "#121212", padx= 7, pady= 7)

        self.InfoString = ("Add your favorite applications on your App Manager "
                    "\nso you can easily search and install them when you need."
                    "\nCheck Readme.md for more information.\n\nCrafted by Lumelys and cooked with Tkinter."
                    "\nCredits to Clear Code."
                    "\n\n This Applications is licenced under the MIT Licence. (https://opensource.org/license/mit)")
        self.InfoTab = ctk.CTkLabel(self, text="•••", cursor= "hand2", font= ctk.CTkFont("Tahoma", 15))
        self.InfoTab.bind("<Button-1>", lambda event: messagebox.showinfo("Info", f"App Manager v1.0.0\n\n{self.InfoString}"))
        ToolTip(self.InfoTab, msg= self.InfoString, delay= 0, fg= "#ffffff", background= "#121212", padx= 7, pady= 7)
        self.InfoTab.pack(side= "right", padx= 5)


class AppDetails(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(parent)
        self.place(relx= 0, rely = 0.05, relwidth = 0.4, relheight= 0.95)

        self.Canvas = ctk.CTkCanvas(self, bg="#121212", highlightthickness=0)
        self.Canvas.rowconfigure((0,1,2,3,4,5,6,7,8,9), weight= 1, uniform= "a")
        self.Canvas.columnconfigure((0,1,2,3,4,5,6,7), weight= 1, uniform= "a")

        self.AppNameVar = ctk.StringVar()
        self.AppImageVar = ctk.StringVar()
        self.AppLinkVar = ctk.StringVar()
        self.AppSizeVar = ctk.StringVar()
        self.AppDescriptionVar = ctk.StringVar()
        self.AppTagsVar = ctk.StringVar()

        self.AppImageVar.set(resource_path("IconData\icon.ico"))
        self.Image = ctk.CTkLabel(self.Canvas, text= "",
                                    image= ctk.CTkImage(Image.open(str(self.AppImageVar.get())),size=(130, 130)), 
                                    fg_color="#121212")
        self.Image.grid(row= 0, column = 0, rowspan= 3, columnspan= 3, sticky="nesw", padx= 5, pady = 5)
        
        ctk.CTkLabel(self.Canvas, textvariable= self.AppNameVar, wraplength= 210, justify= "left", anchor= "w", fg_color= "transparent", corner_radius= 8, font= ctk.CTkFont("Tahoma", 30)).grid(row= 0, column = 3, rowspan= 3, columnspan= 6, sticky="ew", padx= 10, ipady = 5)
        self.Hyperlink = ctk.CTkButton(self.Canvas, text= "Download link >", fg_color= "#2A2A2A", hover_color= "#3A3A3A", cursor="hand2", corner_radius= 8, font= ctk.CTkFont("Tahoma", 20))
        self.Hyperlink.grid(row= 3, column = 0, columnspan= 7, sticky="nesw", padx= 10, pady = 0)
        self.Hyperlink.bind("<Button-1>", lambda event: self.OpenHyperlink())
        ctk.CTkLabel(self.Canvas, textvariable= self.AppSizeVar, fg_color= "#2A2A2A", corner_radius= 8, font= ctk.CTkFont("Tahoma", 20)).grid(row= 3, column = 7, columnspan= 3, sticky="nesw", padx= 10, pady = 0)
        ctk.CTkLabel(self.Canvas, textvariable= self.AppDescriptionVar, wraplength= 376, justify= "left", anchor= "w", fg_color= "transparent", corner_radius= 8, font= ctk.CTkFont("Tahoma", 20)).grid(row= 4, column = 0, rowspan= 3, columnspan= 8, sticky="nesw", padx= 10, pady = 10)
        ctk.CTkLabel(self.Canvas, textvariable= self.AppTagsVar, wraplength= 370, justify= "left", anchor= "w", fg_color= "#2A2A2A", corner_radius= 8, font= ctk.CTkFont("Tahoma", 18)).grid(row= 7, column = 0, rowspan= 2, columnspan= 8, sticky="nesw", padx= 10, pady = 0)
        self.TagCheckBox = ctk.CTkCheckBox(self.Canvas, text= "Search by Tag", fg_color= "#fc663d", hover_color= "#fa7e5c", variable= SearchByTag, onvalue= "True", offvalue= "False", border_width= 2, corner_radius= 5, font= ctk.CTkFont("Tahoma", 12, weight= "bold"))
        self.TagCheckBox.grid(row= 9, column = 0, columnspan= 2, sticky="nesw", padx= 10)
        ToolTip(self.TagCheckBox, msg="Toggle Search by Tag", delay= 0, fg= "#ffffff", background= "#121212", padx= 7, pady= 7)
        self.NameCheckBox = ctk.CTkCheckBox(self.Canvas, text= "Search by Name", fg_color= "#fc663d", hover_color= "#fa7e5c", variable= SearchByName, onvalue= "True", offvalue= "False", border_width= 2, corner_radius= 5, font= ctk.CTkFont("Tahoma", 12, weight= "bold"))
        self.NameCheckBox.grid(row= 9, column = 2, columnspan= 2, sticky="nesw")
        ToolTip(self.NameCheckBox, msg= "Toggle Search by Name", delay= 0, fg= "#ffffff", background= "#121212", padx= 7, pady= 7)


        self.Canvas.pack(expand= True, fill= "both")

        self.Update()

    def Update(self):
        self.AppNameVar.set(FileData[f"App{FocusedAppID}"]["Name"])
        ImageName = FileData[f"App{FocusedAppID}"]["ImagePath"]
        self.AppImageVar.set(f"IconData\{ImageName}")
        try:
            self.Image.configure(image= ctk.CTkImage(Image.open(str(self.AppImageVar.get())),size=(150, 150)))
        except:
            global ApplicationDataCreated
            if not(ApplicationDataCreated):
                messagebox.showerror("No icon found", " No icon was found. This means that the icon of an application is missing, corrupted, or the configuration file includes an incorrect syntax. Please delete or edit its content to make it valid.")
                exit()
        SetAppSizeVar = FileData[f"App{FocusedAppID}"]["Size"]
        self.AppSizeVar.set(f"{SetAppSizeVar}G")
        self.AppDescriptionVar.set(FileData[f"App{FocusedAppID}"]["Description"])
        self.AppTagsVar.set(FileData[f"App{FocusedAppID}"]["Tags"])
        self.after(50, self.Update)
    
    def OpenHyperlink(event):
        webbrowser.open(FileData[f"App{FocusedAppID}"]["Link"])
        #print(FileData[f"App{FocusedAppID}"]["Link"])

class AppSearch(ctk.CTkFrame):
    def __init__(self, parent):

        super().__init__(parent, fg_color="#121212", background_corner_colors= ("#121212", "#121212", "#121212", "#121212"))
        self.place(relx= 0.4, rely= 0.05, relwidth= 0.6, relheight= 0.95)
        #ctk.CTkEntry(self, fg_color="white").pack(fill= "x")
        global SearchBar
        SearchBar = ctk.CTkEntry(self, fg_color="black", corner_radius= 10, border_color= "#fc663d", border_width= 2, font= ctk.CTkFont("Tahoma", 15))
        SearchBar.place(relx= 0, rely= 0, relwidth= 0.98, relheight= 0.1)

        if AppDataCount < 6:
            self.ScrollHeight = self.winfo_screenheight()
        else:
            self.ScrollHeight = AppDataCount * 100
        self.Canvas = ctk.CTkCanvas(self, bg="#121212", highlightthickness=0, scrollregion= (0, 0, 100, self.ScrollHeight))
        self.Canvas.bind_all('<MouseWheel>', lambda event: self.Canvas.yview_scroll(-int(event.delta / 120), "units"))
        self.bind("<Configure>", self.SetAppCard)
        self.AppCardScrollBar = ctk.CTkScrollbar(self, command= self.Canvas.yview)
        self.AppCardScrollBar.place(relx= 0.98, rely= 0.12, relwidth= 0.02, relheight= 0.88)
        self.Canvas.configure(yscrollcommand= self.AppCardScrollBar.set)

        #Create instance of AppCard()
    def SetAppCard(self, event):
        if self.winfo_height() <= AppDataCount * 100:
            AppCardHeight = 100
        else:
            AppCardHeight = self.winfo_screenheight() / AppDataCount

        for Instance in range(AppDataCount):
            self.Canvas.create_window(
                (0, Instance * AppCardHeight * 1.1),
                window = AppCard(self.Canvas, Instance),
                anchor= "nw",
                width= self.winfo_width(),
                height= AppCardHeight
                )

        #self.Canvas.pack(expand= True, fill= "x")
        self.Canvas.place(relx= 0, rely= 0.12, relwidth= 0.98, relheight= 0.88)

        self.Pen = ctk.CTkButton(self, text= "", image= self.emoji("✏️"), fg_color= "#3A3A3A", hover_color= "#4A4A4A", corner_radius= 50, bg_color="#000001")
        self.Pen.place(relx= 0.84, rely= 0.85, relwidth= 0.13, relheight= 0.14)
        self.Pen.bind("<Button-1>", lambda event: self.CreateApp())
        try:
            pywinstyles.set_opacity(self.Pen, color="#000001")
        except:
            pass
        ToolTip(self.Pen, msg="Edit application configuration file", delay= 0, fg= "#ffffff", background= "#121212", padx= 7, pady= 7)

    def emoji(emoji, emoji_char, size=70):
        # convert emoji to CTkImage
        font = ImageFont.truetype("seguiemj.ttf", size=int(size/2)) 
        img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((size/1.18, size/1.7), emoji_char,
                embedded_color=True, font=font, anchor="mm")
        img = ctk.CTkImage(img, size=(size, size))
        return img

    def CreateApp(event):
        AddApp = ctk.CTkToplevel()
        AddApp.title("Add Application")
        AddApp.geometry("400x200+760+440")
        AddApp.attributes("-topmost", True)
        if platform.startswith("win"):
            AddApp.after(200, lambda: AddApp.iconbitmap(resource_path("IconData\icon.ico")))
        AddApp.minsize(300, 200)
        AddApp.rowconfigure((0,1,2), weight= 1, uniform= "a")
        AddApp.columnconfigure((0,1,2,3,4), weight= 1, uniform= "a")

        ctk.CTkLabel(AddApp, text= "Edit your application configuration file", fg_color= "#3A3A3A", corner_radius= 5, font= ctk.CTkFont("Tahoma", 18)).grid(row= 0, column= 0, columnspan= 5, sticky= "nesw", padx= 10, pady= 10, ipadx= 10, ipady= 10)
        ctk.CTkLabel(AddApp, text= "Select application executable :", wraplength= 150, justify= "left", font= ctk.CTkFont("Tahoma", 15)).grid(row= 1, column= 0, columnspan= 3, sticky= "nesw", padx= 10, pady= 10)
        ImagePathButton = ctk.CTkButton(AddApp, text= "Browse", fg_color= "#fc663d", hover_color= "#fa7e5c", corner_radius= 10, font= ctk.CTkFont("Tahoma", 13, weight= "bold"), command= lambda: Browse())
        ImagePathButton.grid(row= 1, column= 3, columnspan= 2, sticky= "nesw", padx= 10, pady= 10)
        ctk.CTkButton(AddApp, text= "Save executable\nicon and open\nconfig file", fg_color= "#fc663d", hover_color= "#fa7e5c", corner_radius= 10, command= lambda: SaveApp(), font= ctk.CTkFont("Tahoma", 13, weight= "bold")).grid(row= 2, column= 0, columnspan= 2, sticky= "nesw", padx= 5, pady= 10)
        ctk.CTkButton(AddApp, text= "Open config file", fg_color= "#fc663d", hover_color= "#fa7e5c", corner_radius= 10, command= lambda: OpenConfig(), font= ctk.CTkFont("Tahoma", 13, weight= "bold")).grid(row= 2, column= 2, columnspan= 2, sticky= "nesw", padx= 0, pady= 10)
        ctk.CTkButton(AddApp, text= "Cancel", fg_color= "#fc663d", hover_color= "#fa7e5c", corner_radius= 10, command= lambda: AddApp.destroy(), font= ctk.CTkFont("Tahoma", 13, weight= "bold")).grid(row= 2, column= 4, sticky= "nesw", padx= 5, pady= 10)

        def SaveApp():
            ExtractImage()
            OpenConfig()
            AddApp.destroy()

        def Browse():
            global FilePath
            global ExecutableBasename
            FilePath = filedialog.askopenfilename()
            ExecutableBasename = os.path.basename(FilePath)
            ImagePathButton.configure(text= ExecutableBasename)

        def ExtractImage():
            try:
                ico_x = win32api.GetSystemMetrics(win32con.SM_CXICON)
                ico_y = win32api.GetSystemMetrics(win32con.SM_CYICON)

                
                ImagePathButton.configure(text= ExecutableBasename)
                large, small = win32gui.ExtractIconEx(str(FilePath),0)
                win32gui.DestroyIcon(large[0])

                hdc = win32ui.CreateDCFromHandle( win32gui.GetDC(0) )
                hbmp = win32ui.CreateBitmap()
                hbmp.CreateCompatibleBitmap( hdc, ico_x, ico_y )
                hdc = hdc.CreateCompatibleDC()

                hdc.SelectObject( hbmp )
                hdc.DrawIcon( (0,0), small[0] )
                BitmapFileName = resource_path(f"IconData\{ExecutableBasename}.bmp")
                hbmp.SaveBitmapFile( hdc, BitmapFileName)
                #print(os.path.basename(filedialog.askopenfilename()))
            except:
                pass

        def OpenConfig():
            webbrowser.open(resource_path("ApplicationData.json"))
            AddApp.destroy()


class AppCard(ctk.CTkFrame):
    def __init__(self, parent, Instance):
        
        super().__init__(parent, fg_color="#121212", cursor= "hand2", corner_radius= 5)
        self.pack(expand= True, fill= "both", pady= 10)
        self.bind("<Button-1>", lambda event: self.FrameClicked(event, Instance))

        self.CardFrame = ctk.CTkFrame(self, fg_color="#3A3A3A", corner_radius= 5, background_corner_colors= ("#121212", "#2A2A2A", "#2A2A2A", "#121212"))
        self.ImageName = FileData[f"App{Instance}"]["ImagePath"]
        self.ImagePath = ctk.CTkLabel(self.CardFrame,text= "",
                                    image= ctk.CTkImage(Image.open(str(f"IconData\{self.ImageName}")),size=(90, 90)), 
                                    fg_color="transparent")
        self.ImagePath.place(relx= 0.02, rely= 0, relwidth= 0.4, relheight= 1)
        self.ImagePath.bind("<Button-1>", lambda event: self.FrameClicked(event, Instance))
        #, wraplength= 376, justify= "left", anchor= "w", fg_color= "transparent", corner_radius= 8, font= ctk.CTkFont("Tahoma", 20)
        self.Name = ctk.CTkLabel(self.CardFrame, text= FileData[f"App{Instance}"]["Name"], wraplength= 210, justify= "left", anchor= "w", fg_color="transparent", font= ctk.CTkFont("Tahoma", 25))
        self.Name.place(relx= 0.42, rely= 0, relwidth= 0.56, relheight= 1)
        self.Name.bind("<Button-1>", lambda event: self.FrameClicked(event, Instance))
        self.CardFrame.place(relx= 0, rely= 0, relwidth= 0.6, relheight= 1)

        self.Description = ctk.CTkLabel(self, text= FileData[f"App{Instance}"]["Description"], wraplength=	160, justify= "left", anchor= "nw", fg_color= "transparent", font= ctk.CTkFont("Tahoma", 15))
        self.Description.place(relx= 0.615, rely= 0, relwidth= 0.285, relheight= 1)
        self.Description.bind("<Button-1>", lambda event: self.FrameClicked(event, Instance))

        self.SizeLabel = FileData[f"App{Instance}"]["Size"]
        self.Size = ctk.CTkLabel(self, text= f"{self.SizeLabel}G", fg_color="transparent", text_color= "#1fdea5", font= ctk.CTkFont("Tahoma", 15, weight= "bold"))
        self.Size.place(relx= 0.9, rely= 0.6, relwidth= 0.1, relheight= 0.4)
        self.Size.bind("<Button-1>", lambda event: self.FrameClicked(event, Instance))

        self.Update(Instance)

    def FrameClicked(self, event, Instance):
        global FocusedAppID
        FocusedAppID = Instance
        #print(FocusedAppID)

    def Update(self, Instance):

        if ((str(SearchBar.get().casefold()) in str(FileData[f"App{Instance}"]["Name"].casefold())
                                       and str(SearchByName.get()) == "True") or
            (str(SearchBar.get().casefold()) in str(FileData[f"App{Instance}"]["Tags"].casefold())
                                       and str(SearchByTag.get()) == "True")):
            self.configure(fg_color="#2A2A2A")
            self.CardFrame.configure(fg_color="#3A3A3A")
            self.Name.configure(text_color="white")
            self.Description.configure(text_color= "white")
            self.Size.configure(text_color= "#1fdea5")
        else:
            self.configure(fg_color="#0a0a0a")
            self.CardFrame.configure(fg_color= "#0a0a0a")
            self.Name.configure(text_color="#2A2A2A")
            self.Description.configure(text_color= "#2A2A2A")
            self.Size.configure(text_color= "#de1f1f")
        self.after(50, lambda: self.Update(Instance))

root()

AppManager = (" $$$$$$\                          $$\      $$\                                                       "            
              "$$  __$$\                         $$$\    $$$ |                                                      "
              "$$ /  $$ |$$$$$$\  $$$$$$\        $$$$\  $$$$ |$$$$$$\ $$$$$$$\  $$$$$$\  $$$$$$\  $$$$$$\  $$$$$$\  "
              "$$$$$$$$ $$  __$$\$$  __$$\       $$\$$\$$ $$ |\____$$\$$  __$$\ \____$$\$$  __$$\$$  __$$\$$  __$$\ "
              "$$  __$$ $$ /  $$ $$ /  $$ |      $$ \$$$  $$ |$$$$$$$ $$ |  $$ |$$$$$$$ $$ /  $$ $$$$$$$$ $$ |  \__|"
              "$$ |  $$ $$ |  $$ $$ |  $$ |      $$ |\$  /$$ $$  __$$ $$ |  $$ $$  __$$ $$ |  $$ $$   ____$$ |      "
              "$$ |  $$ $$$$$$$  $$$$$$$  |      $$ | \_/ $$ \$$$$$$$ $$ |  $$ \$$$$$$$ \$$$$$$$ \$$$$$$$\$$ |      "
              "\__|  \__$$  ____/$$  ____/       \__|     \__|\_______\__|  \__|\_______|\____$$ |\_______\__|      "
              "         $$ |     $$ |                                                   $$\   $$ |                  "
              "         $$ |     $$ |                                                   \$$$$$$  |                  "
              "         \__|     \__|                                                    \______/                   "
             )
import os
import datetime
from PIL import Image, ImageTk
from tkinter import Tk
from tkinter import Label
from tkinter import filedialog
from functions import center_window, copy_files, manage_files
from interface import *

class MainApp(Tk):
    def __init__(self):
        super().__init__()

        # Configuraciones de la aplicacion
        self.title("Autorun Creator")
        self.resizable(False, False)
        self.config(bg="#f9f9f9")

        self._name = ""
        self._icon = ""
        self._program = ""
        self._device = ""

        self.hour = datetime.datetime.now().hour
        self.minute = datetime.datetime.now().minute

        self.year = datetime.datetime.now().year
        self.month = datetime.datetime.now().month
        self.day = datetime.datetime.now().day


        icon = Image.open("lib/icons/logo.png")
        self.iconphoto(True, ImageTk.PhotoImage(icon))

        center_window.center(self, 550, 550) # Poner la ventana al centro de la pantalla

        #---INPUTS---#
        self.input_program = TextInput.LargeInput(self, "Programa o archivo")
        self.input_program.place(x=10, y=10)

        self.input_device = TextInput.ShortInput(self, "Unidad")
        self.input_device.place(x=10, y=75)

        self.input_icon = TextInput.LargeInput(self, "Icono")
        self.input_icon.place(x=10, y=255)

        self.input_name = TextInput.ShortInput(self, "Nombre")
        self.input_name.place(x=10, y=315)


        #---Labels---#
        self.opt_label = Label(self, text="OPCIONAL", font=("Montserrat Semibold", 11), fg="#646464", bg="#f9f9f9")
        self.opt_label.place(x=10, y=220)

        self.keylogger_text = Label(self, text="Inyectar keylogger", font=("Montserrat SemiBold", 11), fg="#BBBBBB", bg="#f9f9f9")
        self.keylogger_text.place(x=35, y=147)
        
        self.keylogger_no = Label(self, text="(No Disponible)", font=("Montserrat SemiBold", 11), fg="#8C8C8C", bg="#f9f9f9")
        self.keylogger_no.place(x=185, y=147)

        self.files_copy = Label(self, text="Copiando archivos...", font=("Montserrat SemiBold", 12), fg="#f9f9f9", bg="#f9f9f9")
        self.files_copy.place(relx=0.338, rely=0.8)

        #---Buttons---#
        self.program__button = Buttons.SelectButton(self, self.select_program)
        self.program__button.place(x=435, y=10)

        self.device__button = Buttons.SelectButton(self, self.select_device)
        self.device__button.place(x=199, y=75)

        self.icon_button = Buttons.SelectButton(self, self.select_icon)
        self.icon_button.place(x=435, y=255)

        self.create_button = Buttons.CreateButton(self, self.create_autorun)
        self.create_button.place(relx=0.25, rely=0.87)

        #---Keylogger---#
        keylogger_button = Buttons.LogerButton(self, self.keylogger_text)
        keylogger_button.place(x=10, y=150)

    #---Functions---#
    def select_program(self):
        extension = [("Aplicaciones", "*.exe"), ("Word", "*.docx"), ("Excel", "*.xls"), ("Powerpoint", "*.ppt"), ("Html", "*.html *.htm"), ("All files", "*.*")]
        file = filedialog.askopenfilename(title="Seleccione un archivo", filetypes=extension)
        if file:
            self.input_program.entry.delete(0, "end")
            self.input_program.entry.insert(0, str(file))
            self.input_program.success()
            self._program = file

    def select_device(self):
        drive = filedialog.askdirectory(title="Seleccione una unidad")
        if drive:
            self.input_device.entry.delete(0, "end")
            self.input_device.entry.insert(0, str(drive))
            self.input_device.success()
            self._device = drive
    
    def select_icon(self):
        icon = filedialog.askopenfilename(title="Seleccione un icono", filetypes=[("Iconos", "*.ico")])
        if icon:
            self.input_icon.entry.delete(0, "end")
            self.input_icon.entry.insert(0, str(icon))
            self.input_icon.success()
            self._icon = icon

    def verify(self):
        if os.path.exists(self._program):
            if os.path.exists(self._device):
                return True
        elif os.path.exists(self._device):
            if os.path.exists(self._program):
                return True
        else:
            if not os.path.exists(self._program):
                self.input_program.error()
            if not os.path.exists(self._device):
                self.input_device.error()
            return False

    def create_autorun(self):
        if self.verify():

            _icon = self._icon
            _label = self._name
            _program = os.path.basename(self._program)
            _file_size = os.path.getsize(self._program)
            _extension = os.path.splitext(self._program)[1]
            _type = ""
            _start = ""
            _program_type = ""

            if _icon:
                _icon = f"ICON={_icon}"
            if not _label:
                _label = f"USB Device"

            if _extension == ".exe":
                _program_type = "ApplicationToStart"
                _type = os.path.basename(self._program).upper()
                _start = f"SRC/STARTAPP.INF"
            else:
                _program_type = "DocumentToOpen"
                _type = f"STARTDOC.EXE {_program}"
                _start = f"SRC/STARTDOC.INF"

            AUTORUN = f"""[AutoRun]
OPEN={_type}
LABEL={_label}
{_icon}"""
            DOCTYPE = f"""[Settings]
{_program_type} = {_program.upper()}

[DATA]
FS = {_file_size}
DA = {self.year}-{self.month:02d}-{self.day:02d}
TI = {self.hour:02d}:{self.minute:02d}"""
            
            
            manage_files.create_files(_start, DOCTYPE)
            manage_files.create_files('SRC/AUTORUN.INF', AUTORUN)

            self.files_copy.config(fg="#424242")
            copy_files.activate(self._program, self._device, self._icon, self.files_copy)
if __name__ == "__main__":
    MainApp().mainloop()
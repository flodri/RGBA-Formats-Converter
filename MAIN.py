import tkinter as tk
import os
from PIL import Image, ImageTk
from math import *
from tkinter import messagebox

#C:\Users\flodri\Desktop\RGBA-Formats-Converter-master\testA.png

# Notes :
# and here we get a callback when the user hits return.
#self.entry_source.bind('<Key-Return>',
#                      self.print_source_path)

preset_to_config = {'old seus to labPBR 1.3':'R = 255*round(sqrt(r/255)) # convert to perceptual smoothness\nG = round(g*0.8980392156862745) # 0-229 range\nB = 0\nA = 255',
                    'old continuum to labPBR 1.3':'R = b\nG = round(g*0.8980392156862745) # 0-229 range\nB = 0\nA = a',
                    'pbr+emissive (old BSL) to labPBR 1.3':'R = 255*round(sqrt(r/255)) # convert to perceptual smoothness\nG = round(g*0.8980392156862745) # 0-229 range\nB = 0\nA = b-1 # 1-255 to 0-254 range and 0 become 255 with underflow',
                    "gray to labPBR 1.3 (you probably won't get good results)":'#magic number are 1-x of the one in ITU-R 601-2 (L=R*299/1000+G*587/1000+B*114/1000)\nR = int(r*0.701)\nG = int(g*0.3708901960784314) # 0.3708901960784314 = 0.413*0.8980392156862745\nB = 0\nA = 255',
                    'Custom preset':'R = r\nG = g\nB = b\nA = a'}

def try_to_open(source_path):
    try: return Image.open(source_path)
    except: return None

def add_imgs_with_propagation(source_path,to_convert_list,filter_on):
    for file_name in os.listdir(source_path):
        file_path = os.path.join(source_path, file_name)
        if os.path.isfile(file_path):
            if filter_on:
                if filter_used in file_name:
                    tried = try_to_open(file_path)
                    if tried is not None: to_convert_list.append((tried, file_path))
            else:
                tried = try_to_open(file_path)
                if tried is not None: to_convert_list.append((tried, file_path))
        else: add_imgs_with_propagation(file_path,to_convert_list,filter_on)

class Application(tk.Frame):
    def __init__(self, master=None):
        #super().__init__(master)
        tk.Frame.__init__(self, master=None,
                          bg = '#202225')
        self.master = master
        self.pack(fill = tk.BOTH,
                  expand=True)
        self.create_widgets()
 
    def create_widgets(self):
        
        ### Convert button :
        self.convert_button_frame = tk.Frame(bg = '#202225')
        self.convert_button_frame.pack(fill = tk.BOTH,
                                       expand=True)
        
        self.convert_button = tk.Button(self.convert_button_frame,
                                        fg = 'black',
                                        bg = 'green')
        self.convert_button["text"] = "CONVERT"
        self.convert_button["command"] = self.convert_img
        self.convert_button.pack(padx=10, pady=10)


        ### Source and cible path :
        self.source_cible_frame = tk.Frame(bg = '#202225')
        self.source_cible_frame.pack(fill = tk.BOTH,
                                     expand=True)
        
        self.entry_source = tk.Entry(master = self.source_cible_frame)
        self.entry_output = tk.Entry(master = self.source_cible_frame)
        for widget in (self.entry_source, self.entry_output):
            widget.configure(bg = '#40444B',
                             fg = '#FFFFFF',
                             insertbackground = '#FFFFFF')
            widget.pack(padx=10, pady=10, fill = tk.X)

        self.source_path = tk.StringVar()
        self.source_path.set("put the source path here. It can be a folder with images inside, or directly the path to a image.")
        self.output_path = tk.StringVar()
        self.output_path.set("put the ouput path here.")

        self.entry_source["textvariable"] = self.source_path
        self.entry_output["textvariable"] = self.output_path
        

        ### checkboxes :
        self.filter_frame = tk.Frame(bg = '#2F3136')
        self.filter_frame.pack(fill = tk.X)
        
        self.filter_on = tk.BooleanVar()
        self.filter_check = tk.Checkbutton(master = self.filter_frame,
                                           variable = self.filter_on,
                                           onvalue = True,
                                           offvalue = False,
                                           bg = '#2F3136',
                                           fg = '#000000',
                                           activebackground = '#2F3136',
                                           activeforeground = '#000000')

        self.filter_start_label = tk.Label(master = self.filter_frame,
                                           text = 'only convert image with ',
                                           bg = '#2F3136',
                                           fg = '#FFFFFF')

        self.filter_entry = tk.Entry(master = self.filter_frame,
                                     bg = '#40444B',
                                     fg = '#FFFFFF',
                                     insertbackground = '#FFFFFF')
        self.filter_used = tk.StringVar()
        self.filter_used.set("_s")
        self.filter_entry["textvariable"] = self.filter_used

        self.filter_end_label = tk.Label(master = self.filter_frame,
                                         text = ' in their name.',
                                         bg = '#2F3136',
                                         fg = '#FFFFFF')
        
        self.overwrite_frame = tk.Frame(bg = '#2F3136')
        self.overwrite_frame.pack(fill = tk.X)
        
        self.overwrite_on = tk.BooleanVar()
        self.overwrite_check = tk.Checkbutton(master = self.overwrite_frame,
                                              variable = self.overwrite_on,
                                              onvalue = True,
                                              offvalue = False,
                                              bg = '#2F3136',
                                              fg = '#000000',
                                              activebackground = '#2F3136',
                                              activeforeground = '#000000')

        self.overwrite_label = tk.Label(master = self.overwrite_frame,
                                        text = 'overwrite original instead of outputing to output path',
                                        bg = '#2F3136',
                                        fg = '#FFFFFF')
        
        self.propagate_frame = tk.Frame(bg = '#2F3136')
        self.propagate_frame.pack(fill = tk.X)
        
        self.propagate_on = tk.BooleanVar()
        self.propagate_check = tk.Checkbutton(master = self.propagate_frame,
                                              variable = self.propagate_on,
                                              onvalue = True,
                                              offvalue = False,
                                              bg = '#2F3136',
                                              fg = '#000000',
                                              activebackground = '#2F3136',
                                              activeforeground = '#000000')

        self.propagate_label = tk.Label(master = self.propagate_frame,
                                        text = 'propagate the conversion to sub-folder (work only in overwrite mode)',
                                        bg = '#2F3136',
                                        fg = '#FFFFFF')

        for widget in (self.filter_check, self.filter_start_label, self.filter_entry, self.filter_end_label, self.overwrite_check, self.overwrite_label, self.propagate_check, self.propagate_label):
            widget.pack(side = "left")


        ### See preview button :
        self.preview_button_frame = tk.Frame(bg = '#2F3136')
        self.preview_button_frame.pack(fill = tk.BOTH,
                                       expand = True)
        
        self.preview = tk.Button(self.preview_button_frame, fg = 'black', bg = 'white')
        self.preview["text"] = "See preview"
        self.preview["command"] = self.display_preview
        self.preview.pack(padx=10, pady=10)


        ### preview :
        self.preview_frame_frame = tk.Frame(bg = '#2F3136')
        self.preview_frame_frame.pack(fill = tk.BOTH,
                                      expand = True)
        
        self.preview_frame = tk.Frame(self.preview_frame_frame,
                                      bg = '#2F3136')
        self.preview_frame.pack()
        
        self.old_img_canvas = tk.Canvas(self.preview_frame,
                                        height = 130,
                                        width = 130,
                                        bg = '#000000',
                                        bd = 0,
                                        highlightthickness = 0)
        self.old_img_canvas.pack(side = 'left',
                                 padx=10)
        self.new_img_canvas = tk.Canvas(self.preview_frame,
                                        height = 130,
                                        width = 130,
                                        bg = '#000000',
                                        bd = 0,
                                        highlightthickness = 0)
        self.new_img_canvas.pack(side = 'right',
                                 padx=10)
        

        ### Preset selection :
        self.preset_frame = tk.Frame(bg = '#2F3136')
        self.preset_frame.pack(fill = tk.X)
        
        self.preset_list = list(preset_to_config)
        self.selected_preset = tk.StringVar()
        self.selected_preset.trace_add("write", self.display_config_text)
        
        self.preset_list_menu = tk.OptionMenu(self.preset_frame,
                                              self.selected_preset,
                                              *self.preset_list)
        self.preset_list_menu.configure(bd = 0)

        self.preset_list_menu.pack(padx=10, pady=10)
        

        ### Config :        
        self.config = tk.Label(text = 'Config :',
                               bg = '#2F3136',
                               fg = '#FFFFFF')
        self.config.pack(fill = tk.BOTH,
                         expand = True)

        
        self.config_box_frame = tk.Frame(bg = '#2F3136')
        self.config_box_frame.pack(fill = tk.BOTH,
                                   expand = True)
        self.config_box = tk.Text(self.config_box_frame,
                                  bg = '#40444B',
                                  fg = '#FFFFFF',
                                  insertbackground = '#FFFFFF')
        # to use to get the value : config_box.get("1.0", tk.END)
        self.config_box.pack(side = 'bottom')


        ### c'est chiant, mais pas vraiment le choix de le mettre là...
        self.selected_preset.set(self.preset_list[0])
        
    def display_config_text(self, *args):
        self.config_box.delete("1.0", tk.END)
        self.config_box.insert("1.0", preset_to_config[self.selected_preset.get()])

    def get_expressions(self):
        config_text = self.config_box.get("1.0", tk.END)
        R_expression = config_text[config_text.find('R =')+4:config_text.find('G =')-1]
        G_expression = config_text[config_text.find('G =')+4:config_text.find('B =')-1]
        B_expression = config_text[config_text.find('B =')+4:config_text.find('A =')-1]
        A_expression = config_text[config_text.find('A =')+4::]
        R_expression = compile(R_expression, 'NoSource', 'eval')
        G_expression = compile(G_expression, 'NoSource', 'eval')
        B_expression = compile(B_expression, 'NoSource', 'eval')
        A_expression = compile(A_expression, 'NoSource', 'eval')
        return R_expression, G_expression, B_expression, A_expression

    def convert(self, img):
        if img.mode != "RGBA": img = img.convert("RGBA")
        l, h = img.size
        being_converted = img.copy() #otherwise it modify the original which bug preview
        for x in range(l):
            for y in range(h):
                r, g, b, a = being_converted.getpixel((x, y))
                # I know, "eVal iS DanGErOUs", but you literally see what's gonna be inputed if you take the preset from someone
                # What *is* eval, however, is slow, so i'll have to change it eventually
                # Also the try block being executed each loop is not ideal...
                R = eval(self.R_expression)
                G = eval(self.G_expression)
                B = eval(self.B_expression)
                A = eval(self.A_expression)
                # just to make sure, in case it's a custom config :
                if R >= 255: R = 255
                elif R < 0: R = 255 + R
                if G >= 255: G = 255
                elif G < 0: G = 255 + R
                if B >= 255: B = 255
                elif B < 0: B = 255 + R
                if A >= 255: A = 255
                elif A < 0: A = 255 + R
                being_converted.putpixel((x,y), (R, G, B, A))
        return being_converted
    
    def convert_img(self, preview=False):
        to_convert_list = []
        source_path  = self.source_path.get()
        filter_on    = self.filter_on.get()
        filter_used  = self.filter_used.get()
        propagate_on = self.propagate_on.get()
        overwrite_on = self.overwrite_on.get()
        
        # get what we have to convert :
        if os.path.isfile(source_path):
            tried = try_to_open(source_path)
            if tried is None:
                messagebox.showwarning('Unsuported, or not a image.', 'This file is either in a unsuported format, or not a image.')
                return None
            else: to_convert_list = [(tried, source_path)]

        elif os.path.isdir(source_path):
            if overwrite_on and propagate_on:
                add_imgs_with_propagation(source_path,to_convert_list,filter_on)
            else:
                for file_name in os.listdir(source_path):
                    if os.path.isfile(file_name):
                        if filter_on:
                            if filter_used in file_name:
                                tried = try_to_open(os.path.join(source_path, file_name))
                                if tried is not None: to_convert_list.append((tried, file_name))
                        else:
                            tried = try_to_open(os.path.join(source_path, file_name))
                            if tried is not None: to_convert_list.append((tried, file_name))

            if len(to_convert_list) == 0:
                messagebox.showwarning('No images in directory.', 'There is no compatible image in the specified directory.')
                return None
        else:
            messagebox.showwarning('Not a valid path.', 'The current input path is not a folder of images or an image.')
            return None

        # We get the expressions from config :
        try:
            expressions = self.get_expressions()
            self.R_expression, self.G_expression, self.B_expression, self.A_expression = expressions
        except:
            messagebox.showwarning('Invalid config.', 'The current config seems to cause issues.')
            return None

        # then we convert :
        if preview:
            old = to_convert_list[0][0]
            new = self.convert(old)
            print(f"size : {old.size}")
            if old.size != (128, 128): old = old.resize((128, 128), resample = Image.NEAREST)
            if new.size != (128, 128): new = new.resize((128, 128), resample = Image.NEAREST)
            # self.old_tkv and self.new_tkv because of a tkinter referencement bug
            self.old_tkv = ImageTk.PhotoImage(old)
            self.old_img_canvas.create_image(65, 65, image = self.old_tkv)
            self.new_tkv = ImageTk.PhotoImage(new)
            self.new_img_canvas.create_image(65, 65, image = self.new_tkv)
        else:
            output_path = self.output_path.get()
            for to_convert in to_convert_list:
                try:
                    img = self.convert(to_convert[0])
                except:
                    messagebox.showwarning('Config caused crash during conversion.', 'The current config have a valid syntax but must have some problems (most likely a 0div) as it caused a crash during conversion.')
                    return None
                #save part :
                if overwrite_on:
                    if propagate_on: img.save(to_convert[1])
                    else: img.save(os.path.join(source_path, to_convert[1]))
                else: img.save(os.path.join(output_path, to_convert[1]))
        
        print("Done.")

    def display_preview(self):
        """ convert one image with current preset, don't save it and display it """
        self.convert_img(preview = True)

    def print_source_path(self, event):
        print("source_path : ",
              self.source_path.get())

root = tk.Tk()
app = Application(master=root)

app.master.title("RGBA Formats Converter")
app.mainloop()

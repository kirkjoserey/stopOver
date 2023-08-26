"""
A simple program that displays a group of images (contains in a folder) like a carousel in random mode.
 (With a Black Screen in the middle). With parameters for time on screen of these images.

Un programa sencillo que muestra un grupo de imágenes (contenidas en una carpeta) como un carrusel en modo aleatorio.
 (Con una pantalla negra en el medio). Con parámetros de tiempo en pantalla de estas imágenes.

PRESS ESC KEY To Stop :-)

2023; kirkjoserey

"""
import os
import sys
import tkinter as tk
from PIL import Image, ImageTk
import random
import logging


# Enable logging
logging.basicConfig(format='%(asctime)s - %(threadName)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Timer Values
scrTime = 0
blkscrTime = 0

class ImageSlideshowApp:
    def __init__(self, root, image_folder):
        logger.info('__init_ ImageSlideshowApp')
        self.root = root
        self.image_folder = image_folder
        self.image_list = self.load_images()
        self.current_image_index = -1
        self.label = tk.Label(self.root, bg='black')
        self.label.pack(fill=tk.BOTH, expand=True)
        self.show_image()


    def load_images(self):
        logger.info('load_images ImageSlideshowApp')
        image_files = [f for f in os.listdir(self.image_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        image_list = []
        for filename in image_files:
            image_path = os.path.join(self.image_folder, filename)
            img = Image.open(image_path)
            img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), resample=Image.Resampling.LANCZOS)
            image = ImageTk.PhotoImage(img)
            image_list.append(image)
        logger.info("Max Index: " + str(len(image_list)))
        return image_list

    def show_image(self):
        if self.current_image_index < len(self.image_list):  # If this validation is False ...the app stop :-)
            logger.info('Image Screen')
            logger.info("Index Show: " + str(self.current_image_index))

            image = self.image_list[self.current_image_index]
            self.label.configure(image=image)
            self.label.image = image
            self.current_image_index = random.randint(0, len(self.image_list))
            logger.info("Next Image: " + str(self.current_image_index))
            self.root.after(blkscrTime, self.show_black_screen)
        else:
            logger.info('Random Luck Stops')
            self.root.destroy()

    def show_black_screen(self):
        logger.info("Black Screen")
        image_path = "blacks/black_screen.png" # Folder & filename Default (Black)
        img = Image.open(image_path)
        img = img.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
        image = ImageTk.PhotoImage(img)
        self.label.configure(image=image)
        self.label.image = image
        self.root.after(scrTime, self.show_image)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    image_folder = "images/"  # Update this with the actual path
    app = ImageSlideshowApp(root, image_folder)

    def on_escape(event):
        logger.info('Users Stops')
        root.destroy()

    root.bind("<Escape>", on_escape)
    root.mainloop()

def isNumeric(varInt, strParam):
    try:
        a = int(varInt)
    except:
        print('Wrong Value of ' + strParam + ' parameter must be an int number. (seconds)')
        exit_program()
    return a

def exit_program():
    sys.exit(0)

if __name__ == "__main__":
    paramSize = len(sys.argv)
    if paramSize == 5:
        if sys.argv[1] == "--imageTime":
            paramImageTime = isNumeric(sys.argv[2], "imageTime")
        else:
            print("Wrong parameter name: use --imageTime)")
            exit_program()
        if sys.argv[3] == "--blackScreenTime":
            paramBlackScreenTime = isNumeric(sys.argv[4], "blackScreenTime")
        else:
            print("Wrong parameter name: use --blackScreenTime)")
            exit_program()
    else:
        if sys.argv[1] == "--help":
            print("Usage: python stopOver.py --imageTime XX --blackScreenTime XX")
        else:
            print("Usage: python stopOver.py --imageTime XX --blackScreenTime XX")
        exit_program()

    scrTime = paramImageTime * 1000 # Convert Seconds to Millisec
    blkscrTime = paramBlackScreenTime * 1000 # Convert Seconds to Millisec
    main()

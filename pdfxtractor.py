from tkinter import *
import PyPDF2   #library built as a PDF toolkit
from PIL import Image, ImageTk  #imaging Library that adds image processing
from tkinter.filedialog import askopenfile  #library for importing files

#global parameters - updating dynamically
all_content = []
all_images = []
img_idx = [0]
displayed_img = []

root = Tk()  #create an window object which holds all elements of the interface
root.geometry('+%d+%d'%(400,20))    #for windows placement on the screen
root.resizable(0, 0)    #creates a non.resizable window
root.title('pdfxtractor/v1.22.0')  #windows title

root.configure(bg='#E5E5EA')   #change application background

#header
header = Frame(root, width=1000, height=0, bg='#E5E5EA')
header.grid(columnspan=3, rowspan=2, row=0)

logo = Image.open('logo.png')
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo, bg='#E5E5EA')
logo_label.image = logo
logo_label.grid(column=0, row=1)

#main content area - text and image extraction
main_content = Frame(root, width=1000, height=0, bg="#E5E5EA")
main_content.grid(columnspan=3, rowspan=2, row=4)

def open_file():    #upload function - changing button text from 'Browse' to 'Load'

#clear global list of indices
    for i in img_idx:
        img_idx.pop()
    img_idx.append(0) #set global index to 0

    browse_text.set("...")

    #load a PDF file
    file = askopenfile(parent=root, mode='rb', filetypes=[("Pdf file", "*.pdf")], initialdir='/')
    if file:
        read_pdf = PyPDF2.PdfFileReader(file)   #select a page
        page = read_pdf.getPage(0)
        page_content = page.extractText()   #extract text content from page

        page_content = page_content.replace('\u2122', "'")  #used for encoded text

        if all_content: #clear the content of the previous PDF file
            for i in all_content:
                all_content.pop()

        for i in range(0, len(all_images)): #clear the image list from the previous PDF file
            all_images.pop()

        if displayed_img:   #hide the displayed image from the previous PDF file and remove it
            displayed_img[-1].grid_forget()
            displayed_img.pop()

        all_content.append(page_content)    #extract text
        images = extract_images(page)   #extract images
        for img in images:
            all_images.append(img)

        selected_image = display_images(images[img_idx[-1]])    #display the first image that was detected
        displayed_img.append(selected_image)

        display_textbox(all_content, 4, 0, root)    #display the text found on the page

        browse_text.set("...")   #reset the button text back to '...'

        what_text = StringVar()
        what_img = Label(root, textvariable=what_text, font=('Ubuntu Mono', 10), bg='#E5E5EA', fg='#FF3B30')
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))
        what_img.grid(row=2, column=1)

        #arrow buttons
        display_icon('iconl.png', 2, 0, E, lambda:left_arrow(all_images, selected_image, what_text))
        display_icon('iconr.png', 2, 2, W, lambda:right_arrow(all_images, selected_image, what_text))
        # display_icon.Frame(root, fg='red', bg='white')

        #create action buttons
        copyText_btn = Button(root, text="copy text", command=lambda:copy_text(all_content, root), font=('Ubuntu Mono', 10), height=1, width=15, bg='#E5E5EA', fg='#FF3B30', cursor="hand2")
        saveAll_btn = Button(root, text="save all images", command=lambda:save_all(all_images), font=('Ubuntu Mono', 10), height=1, width=15, bg='#E5E5EA', fg='#FF3B30', cursor="hand2")
        save_btn = Button(root, text="save image", command=lambda:save_image(all_images[img_idx[-1]]), font=('Ubuntu Mono', 10), height=1, width=15, bg='#E5E5EA', fg='#FF3B30', cursor="hand2")

        #place buttons on grid
        copyText_btn.grid(row=3,column=0)
        saveAll_btn.grid(row=3,column=1)
        save_btn.grid(row=3,column=2)

#instructions
instructions = Label(root, text="upload file for extraction", font=('Ubuntu Mono', 10), fg='#FF3B30', bg='#E5E5EA')
instructions.grid(columnspan=3, column=0, row=1)    #placing element on the grid

#browse button
browse_text = StringVar()    #we use this object so we can specify the variable inside our button widget
browse_btn = Button(root, textvariable=browse_text, command=lambda:open_file(), font='Ubuntu', bg='#E5E5EA', fg='#FF3B30', height=1, width=10, cursor="hand2")   #initialise the object // open function linked with the 'command: lambda' expression!
browse_text.set("...")  #button settings
browse_btn.grid(column=2, row=1, padx=250, pady=100)    #place the button on the screen


# FUNCTIONS __________________________________________________
#right arrow
def right_arrow(all_images, selected_img, what_text):
    #restrict button actions to the number of avialable images
    if img_idx[-1] < len(all_images) -1:
        #change to the following index
        new_idx = img_idx[-1] + 1
        img_idx.pop()
        img_idx.append(new_idx)
        #remove displayed image if exists
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        #create a new image in the new index & display it
        new_img = all_images[img_idx[-1]]
        selected_img = display_images(new_img)
        displayed_img.append(selected_img)
        #update the new index on the interface
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

#left arrow
def left_arrow(all_images, selected_img, what_text):
    #restrict button actions to indices greater than 1
    if img_idx[-1] >= 1:
        #change to the previous index
        new_idx = img_idx[-1] - 1
        img_idx.pop()
        img_idx.append(new_idx)
        #remove displayed image if exists
        if displayed_img:
            displayed_img[-1].grid_forget()
            displayed_img.pop()
        #create a new image in the new index & display it
        new_img = all_images[img_idx[-1]]
        selected_img = display_images(new_img)
        displayed_img.append(selected_img)
        #update the new index on the interface
        what_text.set("image " + str(img_idx[-1] + 1) + " out of " + str(len(all_images)))

#place the image on the grid
def display_logo(url, row, column):
    img = Image.open(url)   #create a variable for the image
    #resize image
    img = img.resize((int(img.size[0]/1.5, int(img.size[1]/1.5))))  #resize image  
    img = ImageTk.PhotoImage(img) #convert Pillow image into a Tkinter image
    img_label = Label(image=img, bg='#E5E5EA')   #place image inside a label widget
    img_label.image = img #obligatory with 'logo_label' statement
    img_label.grid(column=column, row=row, rowspan=2, sticky=NW, padx=10, pady=20)  #place logo inside our window object

    #place icons inside our buttons
def display_icon(url, row, column, stick, funct):
    icon = Image.open(url)
    icon = icon.resize((30,30)) #icon size
    icon = ImageTk.PhotoImage(icon)
    icon_label = Button(image=icon, command=funct, width=25, height=25)
    icon_label.image = icon
    icon_label.grid(column=column, row=row, sticky=stick)

#place a text on the pages
def display_textbox(content, ro, col, root):
        text_box = Text(root, height=10, width=50, bg="#E5E5EA", padx=20)   #storing the text content inside our text widget window
        text_box.insert(1.0, content)  #insert extracted content
        text_box.tag_configure("center", justify="center")  #arrange extracted text inside the widget window
        text_box.tag_add("center", 1.0, "end")  #same as tag_configure
        text_box.grid(column=col, row=ro, sticky=SW, padx=50, pady=50)  #display text on the page
        
#resizing the displayed image while keeping its ratio
def resize_image(img):
    width, height = int(img.size[0]), int(img.size[1])
    if width > height:
        height = 200    #int(300/width*height)
        width = 300
    elif height > width:
        width = 300     #int(250/height*width)
        height = 200
    else:
        width, height = 300,200
    img = img.resize((width, height))
    return img

#display an image on the interface after resizing it
def display_images(img):
    img = resize_image(img)
    img = ImageTk.PhotoImage(img)
    img_label = Label(image=img, bg="#E5E5EA")
    img_label.image = img
    img_label.grid(row=4, column=2, rowspan=2)
    return img_label

#detect images inside PDF documents function
def extract_images(page):
    images = [] #creates an array of stored images
    if '/XObject' in page['/Resources']:
        xObject = page['/Resources']['/XObject'].getObject()

        for obj in xObject:
            if xObject[obj]['/Subtype'] == '/Image':
                size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                data = xObject[obj].getData()
                mode = ""
                if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                    mode = "RGB"
                else:
                    mode = "CMYK"
                img = Image.frombytes(mode, size, data)
                images.append(img)
    return images

#button functionality
def copy_text(content, root):
    root.clipboard_clear()
    root.clipboard_append(content[-1])

def save_all(images):
    counter = 1
    for i in images:
        if i.mode != "RGB":
            i = i.convert("RGB")
        i.save("img" + str(counter) + ".png", format="png")
        counter += 1
        
def save_image(img):
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("img.png", format="png")


root.mainloop() #end of the code interface 
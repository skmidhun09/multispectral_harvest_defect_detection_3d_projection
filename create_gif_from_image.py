import os

from PIL import Image, ImageDraw, ImageFont

basepath = "data/auto/results/"


def create_gif(path, prefix, image_names):
    first_image = Image.open(path + prefix + image_names[0])
    image_size = first_image.size

    # Create a new list to store the modified images
    numbered_images = []
    x = 0
    # Iterate over each image
    for i, image_name in enumerate(image_names):
        # Open the image
        image = Image.open(path + prefix + image_name)

        # Create a new image with the same size as the original image
        new_image = Image.new('RGB', image_size)

        # Paste the original image onto the new image
        new_image.paste(image, (0, 0))

        # Create a drawing object
        draw = ImageDraw.Draw(new_image)

        # Engrave the number on the bottom of the image
        number = str(int(i * 360 / len(image_names))) + "°"
        text_position = (11 * image_size[0] / 20, image_size[1] * 0.01)
        font = ImageFont.truetype("arial.ttf", 42)

        draw.text(text_position, number, font=font, fill=(0, 0, 0), anchor='ra')  # Assuming white text color

        # Append the modified image to the list
        numbered_images.append(new_image)
    # Save the list of images as a GIF file
    numbered_images[0].save(path + prefix + 'images.gif', save_all=True,
                            append_images=numbered_images[1:], duration=500, loop=0)


for folder in os.listdir(basepath):
    folder_path = os.path.join(basepath, folder)
    for i in range(4, 13, 2):
        image_names = []
        for j in range(1, i + 1):
            image_names.append(str(j) + ".jpg")
        create_gif(folder_path + "/" + str(i) + "/", "", image_names)
        create_gif(folder_path + "/" + str(i) + "/", "d", image_names)

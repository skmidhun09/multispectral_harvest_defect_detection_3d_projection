import os
from moviepy.editor import *
from PIL import Image

def convert_mp4_to_gif(mp4_file, gif_file):
    clip = VideoFileClip(mp4_file)
    # Calculate the dimensions of the cropped region
    width, height = clip.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    # Crop the video clip
    cropped_clip = clip.crop(x1=left, y1=top, x2=right, y2=bottom)
    # Set the video clip's aspect ratio to 1:1
    cropped_clip = cropped_clip.resize((size, size))
    cropped_clip.write_gif(gif_file, fps=4)


def convert_all_mp4_to_gif(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".mp4"):
            mp4_file = os.path.join(folder_path, file)
            gif_file = os.path.join(folder_path, file[:-4] + ".gif")
            convert_mp4_to_gif(mp4_file, gif_file)
            print(f"Converted {mp4_file} to {gif_file}")


def crop_image(image_path, output_path):
    # Open the image
    image = Image.open(image_path)

    # Calculate the dimensions of the cropped region
    width, height = image.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size

    # Crop the image
    cropped_image = image.crop((left, top, right, bottom))

    # Save the cropped image
    cropped_image.save(output_path)

    print("Image cropped and saved successfully.")

def crop_all_image(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".jpg"):
            image_path = os.path.join(folder_path, file)
            crop_image(image_path,image_path)

def crop_gif(gif_path, output_path):
    # Load the GIF as a video clip
    clip = VideoFileClip(gif_path)
    # Calculate the dimensions of the cropped region
    width, height = clip.size
    size = min(width, height)
    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size
    # Crop the video clip
    cropped_clip = clip.crop(x1=left, y1=top, x2=right, y2=bottom)
    # Set the video clip's aspect ratio to 1:1
    cropped_clip = cropped_clip.resize((size, size))
    # Save the cropped clip as a new GIF
    cropped_clip.write_gif(output_path, fps=clip.fps)
    print("GIF cropped and saved successfully.")


def crop_all_gif(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".gif"):
            gif_file = os.path.join(folder_path, file)
            n_gif_file = os.path.join(folder_path, file[:-4] + "cropped" + ".gif")
            crop_gif(gif_file, n_gif_file)
            print(f"Converted {gif_file} to {n_gif_file}")


def copy_file():
    count = 1
    for fruit in os.listdir("D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/old results/"):
        print(fruit)
        for i in range(4, 13, 2):
            image = Image.open("D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/old results/" + str(fruit) + "/" + str(i) + "/" + "PCD.jpg")
            image.save("D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/PCD/" + str(count) + ".jpg")
            count = count + 1


def temp_crop_gif():
    count = 1
    for fruit in os.listdir("D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/results/"):
        print(fruit)
        for i in range(4, 13, 2):
            gif_file = os.path.join(
                "D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/results/" + str(
                    fruit) + "/" + str(i) + "/", "images.gif")
            n_gif_file = os.path.join(
                "D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/GIF/" + str(count) + "images.gif")
            crop_gif(gif_file, n_gif_file)
            gif_file = os.path.join(
                "D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/results/" + str(
                    fruit) + "/" + str(i) + "/", "dimages.gif")
            n_gif_file = os.path.join(
                "D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/GIF/" + str(count) + "dimages.gif")
            crop_gif(gif_file, n_gif_file)
            count = count + 1

def reduce_frame_rate(input_path, output_path, factor):
    # Read the input GIF
    gif = imageio.mimread(input_path)

    # Reduce the frame rate
    reduced_gif = [frame for i, frame in enumerate(gif) if i % factor == 0]

    # Save the reduced GIF
    imageio.mimsave(output_path, reduced_gif)



# crop gif
# folder_path = "C:/Users/skmid/OneDrive/Desktop/New folder/New folder (5)/"
# crop_all_gif(folder_path)

# mp4 to gif
folder_path = "C:/Users/skmid/OneDrive/Desktop/oldmethod/BRUISE/"
convert_all_mp4_to_gif(folder_path)


#crop_image("example.jpg", "cropped.jpg")
#copy_file()
#crop_all_image("D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/PCD/")
#trim_video("C:/Users/skmid/OneDrive/Desktop/oldmethod/New folder (3)/onionandlime.mp4", "C:/Users/skmid/OneDrive/Desktop/oldmethod/New folder (3)/")
#temp_crop_gif()
#copy_file()
#reduce_frame_rate("D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/GIF/1images.gif","D:/projects/multispectral_harvest_defect_detection_3d_projection/data/auto/GIF/01images.gif",5)
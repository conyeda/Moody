from ImageMood import ImageMood

from sys import argv

if __name__ == "__main__":
    image_mood = ImageMood(argv[1])
    image_mood.analyse()
    print(image_mood.mood)
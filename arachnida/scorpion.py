import sys
from PIL import Image
from PIL.ExifTags import TAGS

extension = {".jpg", ".jpeg", ".gif", ".bmp", ".png"}

def check_valid_file(file):
    for ext in extension:
        file = file.lower()
        if file.endswith(ext):
            try:
                fd = open(file, "r")
                fd.close()
                return True
            except FileNotFoundError:
                return False
    return False

if __name__ == "__main__":
    files = sys.argv[1:]
    for file in files:
        if check_valid_file(file) is False:
            print("Invalid file")
            files.remove(file)
        else:
            image = Image.open(file)
            print("Image name: ", file)
            print("Image format: ", image.format)
            print("Image mode: ", image.mode)
            print("Image size: ", image.size)
            exifdata = image.getexif()
            for tag_id in exifdata:
                # get the tag name, instead of human unreadable tag id
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)
                # decode bytes
                if isinstance(data, bytes):
                    data = data.decode()
                print(f"{tag:25}: {data}")
    #print(files)
import argparse
import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description = '''
    program receive image files as parameters and parse them for EXIF and other metadata, displaying them on the screen.
                                     ''')
    parser.add_argument('files', nargs='+', help='Image file(s) to read')
    args = parser.parse_args()

    for file_path in args.files:
        if not os.path.isfile(file_path):
            print(f"⚠️ File not found: {file_path}")
            continue
    
        try:
            with Image.open(file_path) as img:
                print(f"\n📂 File: {file_path}")
                print(f"   Size: {img.size}")
                print(f"   Format: {img.format}")
                exif_data = img._getexif()
                if exif_data:
                    print("   EXIF:")
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        print(f"     {tag}: {value}")
                else:
                    print("   No EXIF data found.")
        except Exception as e:
            print(f"⚠️ Error: {e}")

if __name__ == "__main__":
    main()
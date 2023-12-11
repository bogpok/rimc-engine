from convert_image import apply_film
import os

def main():
    path = "img/"    
    # name = "DSC_0005.JPG" # "IMG_20230228_134853.jpg"
    # apply_film(name)
    print(os.listdir(path))
    for f in os.listdir(path):
        apply_film(f)

if __name__ == "__main__":
    main()
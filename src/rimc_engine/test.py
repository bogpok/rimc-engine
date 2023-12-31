from effects import centered_crop
from tools import suffixname
from PIL import Image

img_p = 'IMG_20230301_121858.jpg'
out_path = '../../out/'
orig_path = '../../orig/'

orig = Image.open(orig_path+img_p)

out = centered_crop(orig)

o = out_path+suffixname(img_p, "crop")
print("Saving: ", o)
out.save(o)

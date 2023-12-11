from PIL import Image, ImageOps, ImageFilter, ImageEnhance, ImageDraw
import numpy as np
from random import randint

def apply_vignette(image, sizep=0.1, transparency=0, brightness=150, density=60, frame="rect"):
    """
    Apply vignette 
    
    sizep: size of the vignette frame in percents of original image (0.-1.0)
    transparency: how transparent black mask is. (0-255) where 0 is fully dark
    brightness: brightness of the output print (0-255). More -> brighter
    intensity: number of figures
    density: overall visibility, controlled by blur

    frame: geometrical types of vignette. Allowed values:
        "rect", "round"
    """
    # Open the image
    original_image = image
    width, height = original_image.size

    # get radius    
    radius = int(width/2*(1-1*sizep))

    # Create a mask 
    mask = Image.new('L', (width, height), transparency) 
    mask_draw = ImageDraw.Draw(mask)

    tc = brightness

    # Draw a figure on the mask
    _xy = (width // 2 - radius, height // 2 - radius,
           width // 2 + radius, height // 2 + radius)
    if frame == "rect":
        mask_draw.rounded_rectangle(_xy,
                                    fill=tc)
    elif frame == "round":
        mask_draw.ellipse(_xy,
                          fill=tc)
    else:
        raise ValueError("No such frame!")
    
    mask = mask.filter(ImageFilter.GaussianBlur(radius=radius/density))

    # Apply the mask to the image
    vignette_image = Image.new('RGB', (width, height))
    vignette_image.paste(original_image, (0, 0), mask)

    return vignette_image

def apply_liks(image, r_max=500, intensity=250, density=100, 
               offset=(0,0), transparency=200,
               uselines = False):
    """
    generate Light leaks / film burn and apply to the image
    
    r_max: max radius / measure of figures
    intensity: number of figures
    density: overall visibility of figures, controlled by blur
        Recommended values: from 50 to 100, with the lower value for the figures to be more blended
        after 100, figures are more recognisable
    offset: a border width (2-dimesional) to manipulate the concentration area of the figures
        e.g. (100, 50) will set the concentration area as: 
            100 < x < width-100, 50 < y < height-50
    transparency: maximum transparency (0-255)
    uselines: use lines in the artifact generation
    """
    # Open the image
    original_image = image
    width, height = original_image.size

    # convergent mask
    mask = Image.new('RGBA', (width, height), 0)
    mask_draw = ImageDraw.Draw(mask)

    
    for i in range(intensity):
        # draws: arcs, ellipses    
        # color layer
        # clayer = Image.new('RGB', (width, height), 0)    
        # clayer_draw = ImageDraw.Draw(clayer)
        
        # position
        x = randint(offset[0], width-offset[0])
        y = randint(offset[1], height-offset[1])

        # color
        # gradient - white / orange / red
        # 255, 255, 255
        # 229, 153, 23
        # 212, 13, 13
        r = randint(200, 255)
        if r == 255:
            gk = randint(69, 255) / 255
            if gk > 0.8:
                bk = gk
            else:
                bk = randint(0, 15) / 1000  

        elif r > 230:
            gk = randint(0, 110) / 100
            bk = randint(0, 20) / 100            
        else:
            gk = randint(0, 30) / 1000
            bk = randint(0, 30) / 1000            

        g = int(gk * r)
        b = int(bk * r)
        # color = (r, g, b)#(200, 0, 0)
        t = randint(100, transparency) # transparency
        tcolor = [r, g, b, t] 
        
        # measures
        r = (r_max//randint(1, 100),
             r_max//randint(1, 100),
             r_max//randint(1, 100),
             r_max//randint(1, 100),)
        
        _xy = (x - r[0], y - r[1]*randint(1,2),
               x + r[2], y + r[3]*randint(1,2))
        ang = [0, 0]
        if uselines:
            fig = randint(0, 9)
        else:
            fig = randint(0, 8)
        
        if 0 <= fig < 3:
            tcolor=tuple(tcolor)
            ang[0] = randint(0, 355)
            ang[1] = randint(0, 360 - ang[0]) + ang[0]
            mask_draw.arc(_xy,
                          start=ang[0], end=ang[1],
                          fill=tcolor,
                          width=5)
        elif 3 <= fig < 6:
            tcolor=tuple(tcolor)
            mask_draw.ellipse(_xy,                               
                              fill=tcolor)
        elif 6 <= fig < 8:
            tcolor=tuple(tcolor)
            ang[0] = randint(0, 355)
            ang[1] = randint(0, 360 - ang[0]) + ang[0]
            mask_draw.chord(_xy,
                          start=ang[0], end=ang[1],
                          fill=tcolor,
                          width=5)
        elif fig == 9:
            wp = 1+int(r_max/width*100) # max percentage of width
            w = int(width*randint(1, wp)/100/2)
            mt = 200 # max trans
            tcolor[3] = int(mt*(100-w/width)) # the less the width - more its intensity
            tcolor=tuple(tcolor)
            _xy = (x, 0, x, height)
            mask_draw.line(_xy,fill=tcolor, width=w)

        k = randint(2, 10)
        # mask = Image.blend(mask, clayer, 1/k)

    # smooth the effect
    mask = mask.filter(ImageFilter.GaussianBlur(radius=r_max/density))
    
    # Apply the mask to the image
    # mask = mask.convert("RGB") // loses alpha level
    mask_rgb = Image.new('RGB', (width, height), 0)
    mask_rgb.paste(mask, (0, 0), mask)

    img_spotted = Image.blend(original_image, mask_rgb, 0.1)    
    
    return img_spotted
    

def cbalance(image, rk = 0, gk = 0, bk = 0):
    """
    Add a color tint to the image.

    image: The input image.
    rk, gk, bk: Intensity of the reds, greens, and blues respectively
        (0.0 to 1.0)

    return: Image with added tint.
    """
    # Split the image into individual color channels
    r, g, b = image.split()

    # Adjust the red channel by adding a red tint
    r_tinted = r.point(lambda p: p + int(255 * rk))
    g_tinted = g.point(lambda p: p + int(255 * gk))
    b_tinted = b.point(lambda p: p + int(255 * bk))

    # Merge the modified red channel with the original green and blue channels
    red_tinted_image = Image.merge('RGB', (r_tinted, g_tinted, b_tinted))

    return red_tinted_image

def add_grain(image, intensity):
    """
    Add a grain effect to the image.

    image: The input image.
    intensity: Intensity of the grain effect (0.0 to 1.0).
    
    return: Image with added grain effect.
    """
    # Convert the image to a NumPy array
    img_array = np.array(image)

    # Generate random Gaussian noise
    noise = np.random.normal(scale=intensity * 255, size=img_array.shape)

    # Add the noise to the image
    noisy_image_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)

    # Convert the NumPy array back to an image
    noisy_image = Image.fromarray(noisy_image_array)

    return noisy_image

def apply_film(name, size = (1200, 1200)):
    path = "img/"    

    img = Image.open(path+name)
    img = ImageOps.exif_transpose(img)
    print(img.size)

    # crop
    img_contain = ImageOps.fit(img, size, centering=(0.55, 0.7))
    

    # color: +1
    enhancer = ImageEnhance.Color(img_contain)
    img_contain = enhancer.enhance(1.24)

    # brightness
    br = ImageEnhance.Brightness(img_contain)
    img_contain = br.enhance(1.1)

    # sharpness: -3
    img_contain = img_contain.filter(ImageFilter.GaussianBlur(1)) #0.65

    # Contrast
    enh = ImageEnhance.Contrast(img_contain)
    img_contain = enh.enhance(1.6)
    # img_contain = ImageOps.autocontrast(img_contain, 0.65) #0.65

    # Grain
    img_contain = add_grain(img_contain, 0.02)
   

    # POST
    sharper = ImageEnhance.Sharpness(img_contain)
    img_contain = sharper.enhance(1.15)

    enhancer = ImageEnhance.Color(img_contain)
    img_contain = enhancer.enhance(0.8)

    # light leaks
    
    liks_preset1 = {"r_max":1000, "intensity":200, 
                    "density":50, "offset":(100,50),
                    "transparency":250, "uselines": False} # Nice
    liks_preset2 = {"r_max":700, "intensity":50, 
                    "density":20, "uselines": True} # rollers trace    
    liks_preset3 = {"r_max":150, "intensity":500, 
                    "density":10, "uselines": True} # rollers trace 2 - more    
    liks_preset4 = {"r_max":150, "intensity":50, 
                    "density":60, "uselines": True} # clear line traces    
    liks_preset5 = {"r_max":100, "intensity":250, 
                    "density":40, "uselines": True} # clear line traces 2 - more

    img_contain = apply_liks(img_contain, **liks_preset1)
    

    #  Tint
    brown = (0.1, -0.01, -0.1)
    red = (0.1, -0.05, -0.1)
    blue = (-0.1, -0.01, 0)
    img_b = cbalance(img_contain, *brown)
    
    # vignette
    vtype = 1
    
    if vtype == 0:
        #   small rectangle frame
        img_b = apply_vignette(img_b, sizep=0.02, transparency=0, 
                            brightness=220, density=60, frame='rect')
    elif vtype == 1:
        #   pale rectangle vignette
        img_b = apply_vignette(img_b, sizep=0.01, transparency=0, 
                               brightness=220, density=60, frame='rect') 
    elif vtype == 2:
        #   Nice round vignette
        img_b = apply_vignette(img_b, sizep=0.05, transparency=120,
                               brightness=250, density=5, frame="round") 

    # save
    out_path = "out/"
    n = name.split('.')
    print(n)
    img_b.save(out_path+n[0]+"_edit"+'.'+n[1])



""" Crop notes
    
    img2 = Image.open(path+name)
    k = 0.5
    # img2.resize((int(img2.size[0]*k), int(img2.size[1]*k)))
    mk = min(img2.size)
    img2 = ImageOps.fit(img2, (mk, mk), centering=(0.5, 0.7))
    
    img2.show() 
    
    # img_contain = ImageOps.crop(img_contain, 200)
"""
from PIL import Image, ImageEnhance
img = Image.open("hhh.jpg")

print(img.size)




##### For resize Image
# newsize = (300, 300) 
# img_resized = img.resize(newsize) 
# print(img_resized.size)
#img_resized.save("resized.jpg")

# Define enhancer
enhancer = ImageEnhance.Brightness(img) 
img_light = enhancer.enhance(0.9) 
img_light.save("brightened.jpg")
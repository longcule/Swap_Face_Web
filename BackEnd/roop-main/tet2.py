from PIL import Image

output1 = "out_img_nam"
output2 = "out_img_nu"
image1 = Image.open("results/" + output1 + ".jpg")
image2 = Image.open("results/" + output2 + ".jpg")

width1, height1 = image1.size
width2, height2 = image2.size
max_width = max(width1, width2)
max_height = max(height1, height2)
new_image = Image.new("RGB", (image1.width + image2.width, max(image1.height, image2.height)))
new_image.paste(image2, (0, 0))
new_image.paste(image1, (max_width, 0))
new_image.save('results/output_full2.jpg')
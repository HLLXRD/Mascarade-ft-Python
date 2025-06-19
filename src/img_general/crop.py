from PIL import Image

def crop_transparent(image_path, output_path):
    img = Image.open(image_path).convert("RGBA")
    bbox = img.getbbox()  # Automatically crops around visible content (ignores transparent edges)
    if bbox:
        cropped = img.crop(bbox)
        cropped.save(output_path)

# Example usage:
crop_transparent(r"D:\Em yêu những môn học này\OOP\Mascarade\kivy\src\img_actions\big_mask.png",r"D:\Em yêu những môn học này\OOP\Mascarade\kivy\src\img_actions\big_mask.png")
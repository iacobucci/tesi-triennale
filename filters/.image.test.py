import PIL.Image

def get_image_size(filename:str) -> tuple[int, int]:
	with PIL.Image.open(filename) as img:
		return img.size

print(get_image_size("../res/netscape_navigator.png"))
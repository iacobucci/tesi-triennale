#!/bin/env python3

import panflute as pf
import PIL.Image

def get_image_size(filename:str) -> tuple[int, int]:
	"""
	Ritorna le dimensioni dell'immagine `filename` in pixel.
	"""

	with PIL.Image.open(filename) as img:
		return img.size

def adjust_image(elem, doc):
	if isinstance(elem, pf.Image) and elem.attributes:
		attributes = elem.attributes

		with open ("log.txt", "a") as f:
			f.write(str(attributes) + "\n")

		if 'height' in attributes:
			h = float(attributes["height"].split("cm")[0])
			i = get_image_size(elem.url)

			w = i[0] * h / i[1]
			attributes['width'] = str(w) + "cm"

def main(doc=None):
	with open ("log.txt", "a") as f:
		f.write("images")
	return pf.run_filter(adjust_image, doc=doc)

if __name__ == "__main__":
	main()
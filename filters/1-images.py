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

		if 'height' in attributes:
			h = float(attributes["height"].split("cm")[0])
			i = get_image_size(elem.url)

			w = i[0] * h / i[1]

			attributes['width'] = f"{w}cm"

		if doc.format == 'latex':
			# Crea una copia dell'elemento immagine con gli attributi aggiornati
			# Poiché non possiamo modificare direttamente l'elemento originale
			new_img = pf.Image(
				url=elem.url,
				title=elem.title,
				attributes=attributes
			)
			
			# Crea elementi RawInline per il centering
			begin_center = pf.RawInline('\\begin{center}', format='latex')
			end_center = pf.RawInline('\\end{center}', format='latex')
			
			# Restituisci una sequenza di Inline elements
			return [begin_center, new_img, end_center]

def main(doc=None):
	return pf.run_filter(adjust_image, doc=doc)

if __name__ == "__main__":
	main()
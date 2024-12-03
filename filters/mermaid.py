#!/bin/env python3

import panflute as pf
import subprocess
import json
import os

fileid = 0  # Variabile globale per tenere traccia dell'indice dei file

def intercept_codeblock(elem, doc):
	global fileid  # Dichiarare la variabile globale per aggiornarla
	if isinstance(elem, pf.CodeBlock) and elem.classes[0] == "mermaid":
		# Preparare il contenuto del file D2

		code_content = elem.text

		fileid += 1  # Incrementa l'indice dei file
		mmd = f"mermaid/{fileid}.mmd"
		pdf = f"mermaid/{fileid}.pdf"
		jsn = f"mermaid/{fileid}.json"

		height = ""

		try:
			# Creare la directory "d2" se non esiste
			os.makedirs("mermaid", exist_ok=True)

			# Scrivere il contenuto del file D2
			with open(mmd, "w", encoding="utf-8") as mermaid_file:
				mermaid_file.write(code_content)

			subprocess.run(["touch", jsn], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

			# read json and check for width and height

			with open(jsn, "r") as json_file:
				try:
					data = json.load(json_file)
					if "height" in data:
						height = data["height"]
				except json.JSONDecodeError as e:
					pass

			subprocess.run(["mmdc", "-i", mmd, "-o", pdf], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

			subprocess.run(["pdfcrop", pdf, pdf], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

			# Restituire un blocco LaTeX che include il file PDF generato
			if height != "":
				return pf.RawBlock("\\begin{center}\\includegraphics[height="+ height +",keepaspectratio]{ " + pdf + "}\\end{center}", format="latex")
			return pf.RawBlock("\\begin{center}\\includegraphics[keepaspectratio]{ " + pdf + "}\\end{center}", format="latex")
		except subprocess.CalledProcessError as e:
			pf.debug(f"Errore durante l'esecuzione di d2 o inkscape: {e}")
			return elem  # Lascia il blocco intatto in caso di errore

def main(doc=None):
	return pf.run_filter(intercept_codeblock, doc=doc)

if __name__ == "__main__":
	main()

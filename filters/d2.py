#!/bin/env python3

import panflute as pf
import subprocess
import tempfile
import os
import PIL.Image

def intercept_codeblock(elem, doc):
	if isinstance(elem, pf.CodeBlock) and elem.classes[0] == "d2":
		code_content = elem.text

		with tempfile.NamedTemporaryFile(suffix=".d2", delete=False) as input_file, tempfile.NamedTemporaryFile(suffix=".png", delete=False) as output_file:
			input_path = input_file.name
			output_path = output_file.name
			# Scrivere il contenuto del blocco nel file temporaneo
			input_file.write(code_content.encode('utf-8'))
		
		try:
			# Eseguire il comando d2
			subprocess.run(["d2", input_path, output_path], check=True)
			# Restituire un blocco LaTeX che include il file PDF generato
			return pf.RawBlock("\\begin{center}\\includegraphics[height=" + elem.attributes["height"] +",keepaspectratio]{ " + output_path + "}\\end{center}", format="latex")
		except subprocess.CalledProcessError as e:
			pf.debug(f"Errore durante l'esecuzione di d2: {e}")
			return elem  # Lascia il blocco intatto in caso di errore
		finally:
			# Pulire il file di input (il PDF potrebbe servire ancora)
			os.remove(input_path)

def main(doc=None):
	return pf.run_filter(intercept_codeblock, doc=doc)

if __name__ == "__main__":
	main()
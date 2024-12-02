#!/bin/env python3

import panflute as pf
import subprocess
import tempfile
import os

def intercept_codeblock(elem, doc):
	if isinstance(elem, pf.CodeBlock) and elem.classes[0] == "d2":
		code_content = \
		"""vars: {
d2-config: {
	theme-id: 1
	layout-engine: elk
}
}

""" + elem.text

		with tempfile.NamedTemporaryFile(suffix=".d2", delete=False) as d2, tempfile.NamedTemporaryFile(suffix=".svg", delete=False) as svg, tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf:
			d2.write(code_content.encode('utf-8'))

		try:
			# Eseguire il comando d2
			subprocess.run(["d2", d2.name, svg.name], check=True) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
			subprocess.run(["inkscape", svg.name, "--export-filename=" + pdf.name], check=True) #, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

			# Restituire un blocco LaTeX che include il file PDF generato
			return pf.RawBlock("\\begin{center}\\includegraphics[height=" + elem.attributes["height"] +",keepaspectratio]{ " + pdf.name + "}\\end{center}", format="latex")
		except subprocess.CalledProcessError as e:
			pf.debug(f"Errore durante l'esecuzione di d2: {e}")
			return elem  # Lascia il blocco intatto in caso di errore
		finally:
			os.remove(d2.name)

def main(doc=None):
	return pf.run_filter(intercept_codeblock, doc=doc)

if __name__ == "__main__":
	main()
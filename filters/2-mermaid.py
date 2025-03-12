#!/bin/env python3

import panflute as pf
import subprocess
import os

fileid = 0

def intercept_codeblock(elem, doc):
	global fileid
	if isinstance(elem, pf.CodeBlock) and elem.classes[0] == "mermaid":
		code_content = elem.text

		fileid += 1
		mmd = f"mermaid/{fileid}.mmd"
		pdf = f"mermaid/{fileid}.pdf"

		try:
			os.makedirs("mermaid", exist_ok=True)

			with open(mmd, "w", encoding="utf-8") as mermaid_file:
				mermaid_file.write(code_content)

			subprocess.run(["node_modules/@mermaid-js/mermaid-cli/src/cli.js", "-i", mmd, "-o", pdf], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

			subprocess.run(["pdfcrop", pdf, pdf], check=True, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)


			if elem.attributes.get("align") is not None:
				return pf.RawBlock("\\begin{wrapfigure}{" + elem.attributes.get("align") + "}{"+ elem.attributes.get("width") +"}\\includegraphics[width=\\linewidth]{ " + pdf + "}\\end{wrapfigure}\n\n~\n", format="latex")

			if elem.attributes.get("height") is not None:
				return pf.RawBlock("\\begin{center}\\includegraphics[height="+ elem.attributes.get("height") +",keepaspectratio]{ " + pdf + "}\\end{center}", format="latex")
			return pf.RawBlock("\\begin{center}\\includegraphics[width=\\linewidth,keepaspectratio]{ " + pdf + "}\\end{center}", format="latex")


		except subprocess.CalledProcessError as e:
			pf.debug(f"execution error: {e}")
			return elem

def main(doc=None):
	return pf.run_filter(intercept_codeblock, doc=doc)

if __name__ == "__main__":
	main()
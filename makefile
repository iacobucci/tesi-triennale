PANDOC = pandoc \
		-f gfm \
		--from markdown-smart \
		--mathjax \
		--listings \
		--top-level-division=chapter \
		--template=template.tex \
		--pdf-engine=pdflatex \
		--pdf-engine-opt=-shell-escape \
		-o tesi-iacobucci_valerio-00009765431.pdf

md:
	ls | grep .md | sort --numeric-sort | xargs cat | $(PANDOC)



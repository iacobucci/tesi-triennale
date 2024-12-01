NAME = tesi-iacobucci_valerio-00009765431

PANDOC = pandoc \
		--from gfm \
		--mathjax \
		-F pandoc-minted \
		--top-level-division=chapter \
		-o out/$(NAME).tex

md:
	mkdir -p out
	ls | grep .md | sort --numeric-sort | xargs cat | $(PANDOC)
	cat template-1.tex out/$(NAME).tex template-2.tex | pdflatex -shell-escape -output-directory=out 
	mv out/texput.pdf tesi-iacobucci_valerio-00009765431.pdf


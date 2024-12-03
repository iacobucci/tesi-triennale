NAME = tesi

PANDOC = pandoc \
		--from markdown \
		--mathjax \
		-F ./filters/mermaid.py \
		-F ./filters/minted.py \
		-F ./filters/images.py \
		--top-level-division=chapter \
		-o out/$(NAME).tex

all:
	mkdir -p out
	make tex
	make pdf
	mv out/texput.pdf tesi-iacobucci_valerio-0000976541.pdf

tex:
	ls | grep .md | sort --numeric-sort | xargs cat | $(PANDOC)

pdf:
	cat template-1.tex out/$(NAME).tex template-2.tex | pdflatex -shell-escape -output-directory=out 



# NAME = tesi-iacobucci_valerio-0000976541
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
	mv out/texput.pdf $(NAME).pdf

tex:
	ls | grep ".md$$" | sort --numeric-sort | xargs -I {} sh -c 'cat "{}" && echo -e "\n\n\n"' | $(PANDOC)

pdf:
	(cat template.tex out/$(NAME).tex ; echo "\\end{document}") | pdflatex -shell-escape -output-directory=out 

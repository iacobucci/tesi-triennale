NAME = tesi-iacobucci_valerio-0000976541
# NAME = tesi

PANDOC = pandoc \
		--from markdown \
		--mathjax \
		-F ./filters/1-images.py \
		-F ./filters/2-mermaid.py \
		-F ./filters/3-minted.py \
		--top-level-division=chapter \
		-o out/$(NAME).tex

all:
	mkdir -p out
	- make tex
	- make pdf
	mv out/texput.pdf $(NAME).pdf

tex:
	ls | grep ".md$$" | sort --numeric-sort | xargs -I {} sh -c 'cat "{}" && echo -e "\n\n\n"' | sed 's/^---$$/\\newpage/g' | $(PANDOC)

pdf:
	(cat template.tex out/$(NAME).tex ; echo -E "\\end{document}") | ./filters/4-emojis.py | lualatex -shell-escape -output-directory=out 

simple:
	echo *.md | sort --numeric-sort | xargs cat | sed -s 's/^> !.*//g' | filters/4-1-delete_emojis.py | pandoc --from markdown -o simple.pdf

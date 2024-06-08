compile:
	ls | grep .md | sort --numeric-sort | xargs cat | pandoc -f gfm --from markdown --mathjax --top-level-division=chapter --template=template.tex --pdf-engine=lualatex -o tesi.pdf

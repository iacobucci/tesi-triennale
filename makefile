PANDOC = pandoc \
		-f gfm \
		--from markdown-smart \
		--mathjax \
		--listings \
		--top-level-division=chapter \
		--template=template.tex \
		--pdf-engine=lualatex \
		--pdf-engine-opt=-shell-escape \
		-o dialogo-sopra-i-due-massimi-sistemi-dell-intelligenza-artificiale.pdf

md:
	ls | grep .md | sort --numeric-sort | xargs cat | $(PANDOC)



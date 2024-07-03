PAPER = main
TEX = $(wildcard *.tex)
FIGS = $(wildcard img/*.pdf img/*.eps)

.PHONY: all clean

#$(PAPER).pdf: $(TEX) 
#	pdflatex $(PAPER)
#	biber $(PAPER)
##	bibtex $(PAPER)
#	pdflatex $(PAPER)
#	pdflatex $(PAPER)

$(PAPER).pdf: $(TEX) 
	pdflatex $(PAPER)
#	biber $(PAPER)
	bibtex $(PAPER)
	pdflatex $(PAPER)
	pdflatex $(PAPER)


clean:
	rm -f *.aux *.bbl *.blg *.log *.out $(PAPER).pdf $(PAPER).bcf $(PAPER).run.xml


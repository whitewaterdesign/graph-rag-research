PANDOC := /opt/homebrew/bin/pandoc
PYTHON := .venv/bin/python
DECK   := GraphRAG-Research.pptx
FIGURES := knowledge-graph.png graphrag-pipeline.png

graph-rag.md: graph-rag-pandoc.md refs.bib
	$(PANDOC) $< --bibliography refs.bib --csl ieee.csl --citeproc -t gfm -o $@

# --- slide deck --------------------------------------------------------------
# Edit graph-rag-comprehended.md, then `make deck`. New sections are picked up
# automatically; see the LAYOUT RULES comment in scripts/build_deck.py.
deck: $(DECK)

$(DECK): graph-rag-comprehended.md scripts/build_deck.py refs.bib $(FIGURES) | $(PYTHON)
	$(PYTHON) scripts/build_deck.py

$(PYTHON):
	python3 -m venv .venv
	.venv/bin/pip install -q python-pptx

# --- figures -----------------------------------------------------------------
figures: $(FIGURES)

knowledge-graph.svg: scripts/fig_knowledge_graph.py
	python3 $<

graphrag-pipeline.svg: scripts/fig_pipeline.py
	python3 $<

%.png: %.svg
	rsvg-convert -w 2400 $< -o $@

clean:
	rm -f graph-rag.md $(DECK)

.PHONY: deck figures clean

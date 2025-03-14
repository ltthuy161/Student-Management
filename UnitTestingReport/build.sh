pandoc \
    -o cover.pdf \
    --pdf-engine xelatex \
    -Vlang=vi \
    cover.md 

pandoc \
    -o o.pdf \
    -M link-citations=true \
    --from=markdown+grid_tables \
    --pdf-engine xelatex \
    --listings \
    --highlight-style pygments \
    --number-sections \
    -Vlang=vi \
    --citeproc \
    --bibliography=references.bib \
    header.md \
    content.md \
    footer.md
    
pdftk cover.pdf o.pdf cat output Report.pdf


---
modify:
  language: python
documentclass: report
format: pdf
urlcolor: blue
urlcolor: blue
nocite: '@*'
linestretch: 1.15

geometry: "left=3cm,right=3cm,top=2cm,bottom=2cm"
fontsize: 12pt


header-includes:
    - \usepackage{setspace}
    - \let\oldmaketitle\maketitle
    - \renewcommand{\maketitle}{\oldmaketitle\vspace{4em}}
---

\tableofcontents

\pagebreak
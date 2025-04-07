TEMPLATE_IEEE_TEX = r"""\documentclass[conference]{IEEEtran}

% Paquetes necesarios
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{hyperref}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{algorithm}
\usepackage{algorithmic}
\usepackage{enumitem}
\usepackage{xeCJK}
\usepackage{fontspec}

% Definición de \tightlist para Pandoc
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

% Configuración de fuentes para XeLaTeX
\setmainfont{DejaVu Serif}
\setsansfont{DejaVu Sans}
\setmonofont{DejaVu Sans Mono}
\setCJKmainfont{Noto Sans CJK JP}

% Configuración de hyperref
\hypersetup{
    colorlinks=true,
    linkcolor=blue,
    filecolor=magenta,
    urlcolor=cyan,
    pdftitle={$title$},
    pdfauthor={$author$},
    pdfsubject={$subject$},
    pdfkeywords={$keywords$}
}

\title{$title$}
\author{$author$}
\date{\today}

\begin{document}

\maketitle

\begin{abstract}
$abstract$
\end{abstract}

$body$

\bibliographystyle{IEEEtran}
\bibliography{references}

\end{document}
""" 
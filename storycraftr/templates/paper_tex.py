# templates/paper_tex.py

TEMPLATE_PAPER_TEX = r"""
\documentclass[12pt]{article}
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage{lastpage}
\usepackage{hyperref}
\usepackage{fontspec}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{cite}
\usepackage{url}
\usepackage{listings}
\usepackage{xcolor}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{float}
\usepackage{placeins}

% Configurar la fuente para el artículo
\setmainfont{Times New Roman}

% Ajustar el tamaño de página a A4 y márgenes adecuados
\usepackage{geometry}
\geometry{a4paper, margin=1in} % Tamaño A4 con márgenes de 1 pulgada

% Configurar encabezado y pie de página
\pagestyle{fancy}
\fancyhf{} % Limpiar encabezados y pies de página
\fancyhead[L]{\textit{$title$}} % Título en el encabezado izquierdo
\fancyhead[R]{\textit{$author$}} % Autor en el encabezado derecho
\fancyfoot[C]{Página \thepage\ de \pageref{LastPage}} % Número de página en el pie de página

% Eliminar la numeración automática de títulos
\setcounter{secnumdepth}{-1}

% Ajustar la sangría y el espaciado de los párrafos
\setlength{\parindent}{0.5in}
\setlength{\parskip}{0pt}

% Definir texorpdfstring para evitar errores
\providecommand{\texorpdfstring}[2]{#1}

% Definir tightlist para evitar errores con listas
\providecommand{\tightlist}{%
  \setlength{\itemsep}{0pt}\setlength{\parskip}{0pt}}

% Crear un estilo de página vacío para la primera página
\fancypagestyle{plain}{
    \fancyhf{} % Eliminar encabezados y pies de página para la primera página
}

\begin{document}

% Primera página (título) sin pie de página
\thispagestyle{plain}
\begin{center}
    {\Large\textbf{$title$}}\\[0.5cm]
    {\large $author$}\\[0.3cm]
    {\small $institution$}\\[1cm]
    {\small \textit{$date$}}\\[1cm]
    {\small \textbf{Abstract}}\\[0.3cm]
    \parbox{0.9\textwidth}{
        $abstract$
    }
    \vspace{0.5cm}
    {\small \textbf{Keywords:} $keywords$}
\end{center}

\newpage

% Introducción
\section*{Introduction}
$introduction$

% Revisión de literatura
\section*{Literature Review}
$literature_review$

% Metodología
\section*{Methodology}
$methodology$

% Resultados
\section*{Results}
$results$

% Discusión
\section*{Discussion}
$discussion$

% Conclusión
\section*{Conclusion}
$conclusion$

% Trabajo futuro
\section*{Future Work}
$future_work$

% Referencias
\section*{References}
\bibliographystyle{plain}
\bibliography{references}

\end{document}
"""

# templates/tex.py

TEMPLATE_TEX = r"""
\documentclass[12pt]{book}
\usepackage{fancyhdr}
\usepackage{graphicx}
\usepackage{lastpage}
\usepackage{hyperref}
\usepackage{fontspec}

% Configurar la fuente para el libro
\setmainfont{Palatino}

% Ajustar el tamaño de página a A5 y márgenes adecuados
\usepackage{geometry}
\geometry{a5paper, margin=0.75in} % Tamaño A5 con márgenes de 0.75 pulgadas

% Configurar encabezado y pie de página
\pagestyle{fancy}
\fancyhf{} % Limpiar encabezados y pies de página
\fancyfoot[C]{\textit{La purga de los dioses}} % Pie de página con el título
\fancyfoot[R]{Página \thepage\ de \pageref{LastPage}} % Número de página en la esquina derecha

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

% Crear un estilo de página vacío para la portada
\fancypagestyle{plain}{
    \fancyhf{} % Eliminar encabezados y pies de página para la primera página
}

\begin{document}

% Primera página (portada) sin pie de página
\thispagestyle{plain}
%\begin{center}
%    \includegraphics[width=\textwidth]{portada.png} % Incluir imagen de portada
%\end{center}

$body$

\end{document}
"""

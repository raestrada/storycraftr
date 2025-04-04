#!/bin/bash
set -e

# Definir el color amarillo para el output
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# Verifica si el parámetro --use-poetry está presente
COMMAND="papercraftr"
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --use-poetry) COMMAND="poetry run papercraftr" ;;
        *) echo "Parámetro desconocido: $1" ;;
    esac
    shift
done

# Función para ejecutar y mostrar el comando en color amarillo
run_command() {
    echo -e "${YELLOW}Ejecutando: \"$*\"${NC}"
    "$@"
}

# Inicializar el proyecto
run_command $COMMAND init "Deep Learning in Medical Imaging" \
    --primary-language "en" \
    --author "Rodrigo Estrada" \
    --keywords "deep learning, medical imaging, CNN, diagnostic systems" \
    --behavior "behavior.txt"

# Definir elementos core del paper
run_command $COMMAND define core-question "How can deep learning architectures be optimized for improved accuracy in medical image classification while maintaining interpretability for clinical applications?"

run_command $COMMAND define contribution "Novel hybrid CNN architecture that combines high accuracy with interpretable features for medical image analysis"

# Organizar literatura
run_command $COMMAND organize-lit lit-summary "Analyze recent advances in deep learning for medical imaging, focusing on CNN architectures, transfer learning, and interpretability approaches"

run_command $COMMAND organize-lit concept-map "Create a concept map showing relationships between deep learning architectures, medical imaging modalities, and clinical applications"

# Crear outline del paper
run_command $COMMAND outline outline-sections "Create a detailed outline for a research paper on optimizing deep learning architectures for medical image classification, emphasizing both performance and interpretability"

run_command $COMMAND outline define-methods "Define a mixed-methods approach combining quantitative performance analysis with qualitative evaluation by medical experts"

# Generar secciones
run_command $COMMAND generate introduction "Create an introduction highlighting the challenges in medical image classification and the need for interpretable deep learning solutions"

run_command $COMMAND generate literature-review "Review current deep learning approaches in medical imaging, focusing on the trade-off between accuracy and interpretability"

run_command $COMMAND generate methodology "Detail our hybrid CNN architecture, including network design, training methodology, and validation approach"

run_command $COMMAND generate results "Present performance metrics, interpretability analysis, and clinical validation results"

run_command $COMMAND generate discussion "Discuss the implications of our results for clinical practice and the broader field of medical AI"

run_command $COMMAND generate conclusion "Summarize our contributions and propose future research directions"

# Análisis y resultados
run_command $COMMAND analyze run-analysis "Perform comprehensive analysis of model performance across different medical image types and clinical scenarios"

run_command $COMMAND analyze summarize-results "Summarize key findings, including accuracy metrics, interpretability scores, and clinical feedback"

# Gestión de referencias
run_command $COMMAND references add "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444."

run_command $COMMAND references add "Esteva, A., et al. (2017). Dermatologist-level classification of skin cancer with deep neural networks. Nature, 542(7639), 115-118."

run_command $COMMAND references format "IEEE"

run_command $COMMAND references check "Verify all citations are properly formatted and match the reference list"

# Finalización
run_command $COMMAND finalize check-consistency "Check consistency of terminology, methodology description, and results presentation across all sections"

run_command $COMMAND finalize finalize-format "Format the paper according to IEEE conference guidelines"

run_command $COMMAND finalize generate-abstract "Generate an abstract highlighting our novel approach to combining accuracy and interpretability in medical image classification"

# Publicar
run_command $COMMAND publish pdf en

# Iteración y mejoras
run_command $COMMAND iterate reinforce-ideas "Strengthen the emphasis on interpretability throughout all sections"

run_command $COMMAND chat "Review the methodology section and suggest improvements for clarity"

echo -e "${YELLOW}Ejemplo de uso de PaperCraftr completado exitosamente${NC}" 
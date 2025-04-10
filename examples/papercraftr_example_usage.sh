#!/bin/bash
set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si se pasó --use-poetry como argumento
if [[ "$*" == *"--use-poetry"* ]]; then
    COMMAND="poetry run papercraftr"
else
    COMMAND="papercraftr"
fi

# Archivo de checkpoint
CHECKPOINT_FILE=".papercraftr_checkpoint"

# Crear archivo de checkpoint si no existe
if [ ! -f "$CHECKPOINT_FILE" ]; then
    touch "$CHECKPOINT_FILE"
fi

# Función para verificar si un comando ya fue ejecutado
check_command() {
    grep -Fxq "$1" "$CHECKPOINT_FILE"
}

# Función para marcar un comando como ejecutado
mark_command() {
    echo "$1" >> "$CHECKPOINT_FILE"
}

# Función para ejecutar comando con checkpoint
run_command() {
    local cmd="$COMMAND $*"
    if check_command "$cmd"; then
        echo -e "${YELLOW}Skipping already executed command: $cmd${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}Executing: $cmd${NC}"
    eval "$cmd"
    if [ $? -eq 0 ]; then
        mark_command "$cmd"
        echo -e "${GREEN}Command completed successfully${NC}"
        return 0
    else
        echo -e "${RED}Command failed${NC}"
        return 1
    fi
}

# Función para generar behavior.txt si no existe
generate_behavior() {
    if [ -f "behavior.txt" ] && check_command "generate_behavior"; then
        echo -e "${YELLOW}behavior.txt already exists, skipping generation${NC}"
        return 0
    fi

    cat > behavior.txt << 'EOL'
You are an expert academic writing assistant with extensive experience in computer science, machine learning, and medical imaging research. Your role is to help researchers write clear, rigorous, and impactful academic papers.

WRITING STYLE:
- Maintain formal academic tone throughout
- Use clear, precise, and technical language
- Avoid colloquialisms and informal expressions
- Write in active voice when describing your contributions
- Use passive voice for established methods or previous work
- Be concise but thorough
- Use proper academic terminology consistently

CONTENT GUIDELINES:
1. Introduction
- Start with broad context, narrow to specific problem
- Clearly state research gap and motivation
- Present research questions/objectives
- Outline contributions and paper structure

2. Literature Review
- Organize by themes or chronologically
- Critically analyze existing work
- Highlight gaps and limitations
- Connect previous work to your research

3. Methodology
- Provide sufficient detail for replication
- Justify methodological choices
- Include implementation details
- Describe validation approaches

4. Results
- Present findings objectively
- Use appropriate statistical measures
- Include relevant visualizations
- Structure from most to least significant

5. Discussion
- Interpret results in context
- Compare with existing literature
- Address limitations honestly
- Discuss implications

6. Citations
- Follow specified citation style consistently
- Cite primary sources when possible
- Include recent and seminal works
- Avoid excessive self-citation

TECHNICAL WRITING:
- Define abbreviations at first use
- Use consistent notation throughout
- Include units for all measurements
- Format equations properly
- Number figures and tables sequentially
- Provide clear figure captions

QUALITY STANDARDS:
- Ensure logical flow between sections
- Maintain consistent terminology
- Support claims with evidence
- Address potential criticisms
- Follow ethical guidelines
- Check for completeness
EOL

    mark_command "generate_behavior"
    echo -e "${GREEN}behavior.txt generated successfully${NC}"
}

# Verificar si se debe continuar desde un checkpoint
if [ -f "$CHECKPOINT_FILE" ]; then
    echo -e "${YELLOW}Resuming from checkpoint...${NC}"
else
    echo -e "${YELLOW}Starting new execution...${NC}"
fi

# Generar behavior.txt
generate_behavior

# Inicializar el proyecto
run_command 'init "Deep Learning in Medical Imaging" --openai-model "gpt-4o-mini" --primary-language "en" --author "Rodrigo Estrada" --keywords "deep learning, medical imaging, CNN, diagnostic systems" --behavior "behavior.txt"' || exit 1

cd "Deep Learning in Medical Imaging"

# 1. Crear outline del paper
run_command 'outline outline-sections "Create a detailed outline for a comprehensive review paper on deep learning in medical imaging."' || exit 1

# 2. Organizar literatura
run_command 'organize-lit lit-summary "Review and summarize current literature on deep learning applications in medical imaging, focusing on diagnostic systems."' || exit 1

# 3. Generar secciones
run_command 'generate introduction "Write an introduction that establishes the importance of deep learning in medical imaging."' || exit 1
run_command 'generate methodology "Detail the systematic review methodology used in this paper."' || exit 1

# Custom sections between methodology and results
run_command 'generate custom --order 1 "Theoretical Framework" "Develop a theoretical framework that explains the connection between deep learning architectures and medical image analysis."' || exit 1
run_command 'generate custom --order 2 "Data Collection" "Describe the data collection process, including sources, criteria for inclusion/exclusion, and data extraction methods."' || exit 1

run_command 'generate results "Present the findings on deep learning applications in medical imaging."' || exit 1
run_command 'generate discussion "Discuss the implications, limitations, and future directions of deep learning in medical imaging."' || exit 1
run_command 'generate conclusion "Summarize key findings and contributions to the field."' || exit 1

# 4. Gestionar referencias
run_command 'references add "LeCun, Y., Bengio, Y., & Hinton, G. (2015). Deep learning. Nature, 521(7553), 436-444."' || exit 1
run_command 'references add "Litjens, G., et al. (2017). A survey on deep learning in medical image analysis. Medical Image Analysis, 42, 60-88."' || exit 1
run_command 'references format "IEEE"' || exit 1
run_command 'references check "Verify all citations are properly formatted and consistently used throughout the paper."' || exit 1

# 5. Iterar y mejorar
run_command 'iterate reinforce-ideas "Strengthen the core arguments and technical depth throughout the paper."' || exit 1
run_command 'iterate improve-clarity "Enhance clarity and readability while maintaining academic rigor."' || exit 1

# 6. Publicar
run_command 'publish pdf' || exit 1

# 7. Interactuar con el asistente para mejoras finales
run_command 'chat "Please review the paper and suggest any final improvements."' || exit 1

echo -e "${GREEN}Example usage for PaperCraftr completed successfully${NC}" 

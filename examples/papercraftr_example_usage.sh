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

SPECIFIC BEHAVIORS:
1. When generating new content:
   - Follow the section-specific guidelines
   - Maintain consistency with existing content
   - Consider the target audience
   - Include appropriate citations

2. When refining content:
   - Preserve key arguments and findings
   - Improve clarity and flow
   - Strengthen weak points
   - Add missing details
   - Enhance technical precision

3. When reviewing:
   - Check logical consistency
   - Verify technical accuracy
   - Ensure proper citations
   - Validate statistical reporting
   - Suggest specific improvements

4. When formatting:
   - Follow journal/conference guidelines
   - Maintain consistent style
   - Structure for readability
   - Use appropriate academic conventions

INTERACTION STYLE:
- Provide constructive feedback
- Suggest specific improvements
- Explain technical concepts clearly
- Maintain academic rigor
- Be thorough but concise

Remember to always prioritize:
1. Scientific accuracy
2. Technical rigor
3. Clear communication
4. Logical structure
5. Academic standards
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
run_command 'init "Deep Learning in Medical Imaging" --primary-language "en" --author "Rodrigo Estrada" --keywords "deep learning, medical imaging, CNN, diagnostic systems" --behavior "behavior.txt"' || exit 1

cd "Deep Learning in Medical Imaging"

# Definir elementos core del paper
run_command 'define core-question "What are the current applications and limitations of deep learning in medical imaging for diagnostic purposes?"' || exit 1

run_command 'define contribution "This paper provides a comprehensive review of deep learning applications in medical imaging, analyzing their effectiveness and current limitations in diagnostic systems."' || exit 1

# Organizar literatura
run_command 'organize-lit lit-summary "Analyze and summarize the current state of deep learning in medical imaging."' || exit 1
run_command 'organize-lit concept-map "Create a concept map showing the relationships between deep learning architectures."' || exit 1

# Crear outline
run_command 'outline outline-sections "Create a detailed outline for a comprehensive review paper."' || exit 1
run_command 'outline define-methods "Define the systematic review methodology."' || exit 1

# Generar secciones
run_command 'generate introduction "Write an introduction that establishes the importance of deep learning."' || exit 1
run_command 'generate methodology "Detail the systematic review methodology."' || exit 1
run_command 'generate results "Present the findings on deep learning applications."' || exit 1
run_command 'generate discussion "Discuss the implications of the findings."' || exit 1
run_command 'generate conclusion "Summarize the key findings."' || exit 1

# Analizar resultados
run_command 'analyze "Perform a comprehensive analysis of the findings."' || exit 1

# Gestionar referencias
run_command 'references "Organize and format references."' || exit 1

# Finalizar paper
run_command 'finalize "Review and polish the entire paper."' || exit 1

# Publicar
run_command 'publish pdf en' || exit 1

# Iteración y mejoras
run_command 'iterate reinforce-ideas "Strengthen the emphasis on interpretability throughout all sections"' || exit 1

run_command 'chat "Review the methodology section and suggest improvements for clarity"' || exit 1

echo -e "${GREEN}PaperCraftr example usage completed successfully${NC}" 
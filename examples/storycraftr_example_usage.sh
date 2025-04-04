#!/bin/bash
set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar si se pasó --use-poetry como argumento
if [[ "$*" == *"--use-poetry"* ]]; then
    COMMAND="poetry run storycraftr"
else
    COMMAND="storycraftr"
fi

# Archivo de checkpoint
CHECKPOINT_FILE=".storycraftr_checkpoint"

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
WRITING STYLE:
Write in an engaging, creative style appropriate for fiction.
Maintain consistent tone and voice throughout the story.
Balance description, dialogue, and action.

CONTENT GUIDELINES:
1. When generating new content:
   - Follow the genre conventions
   - Maintain consistency with existing story elements
   - Consider the target audience
   - Show, don't tell
   - Use vivid descriptions

2. When refining content:
   - Preserve key plot points and character development
   - Improve pacing and flow
   - Strengthen character motivations
   - Add sensory details
   - Enhance emotional impact

3. When reviewing:
   - Check plot consistency
   - Verify character arcs
   - Ensure setting coherence
   - Validate story logic
   - Suggest improvements

4. When worldbuilding:
   - Create rich, believable settings
   - Develop consistent rules
   - Build layered histories
   - Design memorable locations

INTERACTION STYLE:
- Provide constructive feedback
- Suggest creative improvements
- Explain story concepts clearly
- Maintain narrative focus
- Be thorough but concise

Remember to always prioritize:
1. Story coherence
2. Character development
3. Engaging narrative
4. Emotional impact
5. Genre expectations
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
run_command 'init "The Last Guardian" --primary-language "en" --author "Rodrigo Estrada" --genre "Fantasy" --behavior "behavior.txt"' || exit 1

# Worldbuilding
run_command 'worldbuilding define-world "A mystical world where ancient technology and magic coexist, where the remnants of a long-lost civilization still influence the present through their mysterious devices and enchantments."' || exit 1

run_command 'worldbuilding add-character "Aria" "A young engineer with an innate ability to understand ancient technology, who discovers she can communicate with the dormant machines that fill the forgotten city."' || exit 1

run_command 'worldbuilding add-character "Echo" "A mechanical guardian, one of the first machines Aria awakens, who becomes both her protector and guide to understanding the ancient world."' || exit 1

run_command 'worldbuilding add-character "Marcus" "A scholar studying the ancient civilization, initially skeptical of Aria'\''s abilities but gradually becomes a valuable ally."' || exit 1

run_command 'worldbuilding add-location "The Forgotten City" "An abandoned metropolis filled with dormant mechanical beings, its streets lined with deactivated automatons and buildings that hold secrets of the past."' || exit 1

run_command 'worldbuilding add-location "The Ancient Workshop" "A vast underground facility where Aria makes her first connection with the machines, filled with tools and blueprints from the ancient civilization."' || exit 1

run_command 'worldbuilding add-location "The Guardian'\''s Sanctuary" "A hidden temple-like structure where the most advanced mechanical beings were kept, now serving as Echo'\''s base of operations."' || exit 1

run_command 'worldbuilding add-plot-element "The Awakening" "The process of machines gradually coming back to life as Aria'\''s powers grow, causing both wonder and concern among the local population."' || exit 1

run_command 'worldbuilding add-plot-element "Ancient Threat" "The discovery that some mechanical beings were deactivated for a reason, as they pose a danger to the current world."' || exit 1

run_command 'worldbuilding add-plot-element "Knowledge Transfer" "The gradual understanding of the ancient civilization'\''s technology and its implications for the present world."' || exit 1

# Outline
run_command 'outline create "Create a detailed chapter-by-chapter outline for The Last Guardian, focusing on Aria'\''s journey of discovery and the awakening of the ancient machines."' || exit 1

run_command 'outline add-chapter "The Discovery" "Aria finds the Ancient Workshop and accidentally activates her first machine, discovering her unique ability to communicate with the ancient technology."' || exit 1

run_command 'outline add-chapter "First Connection" "Aria begins to understand her powers as she successfully awakens Echo, forming a crucial alliance with the mechanical guardian."' || exit 1

run_command 'outline add-chapter "The Scholar'\''s Doubt" "Marcus arrives to investigate the awakening machines, initially conflicting with Aria but gradually recognizing the importance of her abilities."' || exit 1

run_command 'outline add-chapter "Expanding Influence" "More machines begin to activate across the city, drawing both curiosity and fear from the outside world."' || exit 1

run_command 'outline add-chapter "Ancient Warnings" "Echo reveals the existence of dangerous machines that were deliberately deactivated, leading to a race to prevent their awakening."' || exit 1

run_command 'outline add-chapter "Crisis Point" "A powerful hostile machine activates, forcing Aria, Echo, and Marcus to work together to protect the city."' || exit 1

run_command 'outline add-chapter "Understanding the Past" "The team discovers the true purpose of the ancient civilization'\''s technology and their responsibility to use it wisely."' || exit 1

# Escribir capítulos
run_command 'write chapter "The Discovery" --prompt "Focus on building tension as Aria explores the Ancient Workshop, leading to the dramatic moment of her first connection with a machine."' || exit 1

run_command 'write chapter "First Connection" --prompt "Develop the unique relationship between Aria and Echo, emphasizing the wonder and challenges of communication between human and machine."' || exit 1

run_command 'write chapter "The Scholar'\''s Doubt" --prompt "Explore the conflict between scientific skepticism and unexplainable abilities through Marcus'\''s perspective and his gradual acceptance of Aria'\''s gift."' || exit 1

run_command 'write chapter "Expanding Influence" --prompt "Show the growing impact of the awakening machines on the city and its people, balancing wonder with underlying tension."' || exit 1

run_command 'write chapter "Ancient Warnings" --prompt "Build suspense as Echo reveals the darker aspects of the ancient civilization'\''s legacy and the dangers that lurk within the city."' || exit 1

run_command 'write chapter "Crisis Point" --prompt "Create an action-packed sequence as the team confronts a dangerous machine, while weaving in emotional moments and character development."' || exit 1

run_command 'write chapter "Understanding the Past" --prompt "Bring the various plot threads together as the characters uncover the truth about the ancient civilization and face the responsibility of their discovery."' || exit 1

# Iteración
run_command 'iterate chapter "The Discovery" --prompt "Enhance the atmosphere and sensory details of the Ancient Workshop, and deepen Aria'\''s emotional journey of discovery."' || exit 1

run_command 'iterate chapter "First Connection" --prompt "Strengthen the unique dynamic between Aria and Echo, adding more nuanced details to their communication process."' || exit 1

run_command 'iterate chapter "The Scholar'\''s Doubt" --prompt "Refine Marcus'\''s character arc and the philosophical conflict between scientific knowledge and unexplainable phenomena."' || exit 1

run_command 'iterate chapter "Expanding Influence" --prompt "Add more detail to the city'\''s reaction to the awakening machines, including diverse perspectives from different citizens."' || exit 1

run_command 'iterate chapter "Ancient Warnings" --prompt "Increase the tension and mystery surrounding the dangerous machines, while developing Echo'\''s character through his knowledge of the past."' || exit 1

run_command 'iterate chapter "Crisis Point" --prompt "Polish the action sequences and emotional beats, ensuring the pacing drives the story forward effectively."' || exit 1

run_command 'iterate chapter "Understanding the Past" --prompt "Strengthen the thematic elements and ensure all major plot points are resolved satisfyingly."' || exit 1

# Publicar
run_command $COMMAND publish pdf en || exit 1

run_command $COMMAND publish epub es || exit 1

echo -e "${GREEN}StoryCraftr example usage completed successfully${NC}"

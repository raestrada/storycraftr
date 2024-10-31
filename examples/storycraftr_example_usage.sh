#!/bin/bash
set -e

# Definir el color amarillo para el output
YELLOW='\033[1;33m'
NC='\033[0m' # Sin color

# Verifica si el parámetro --use-poetry está presente
COMMAND="storycraftr"
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --use-poetry) COMMAND="poetry run " ;;
        *) echo "Parámetro desconocido: $1" ;;
    esac
    shift
done

# Función para ejecutar y mostrar el comando en color amarillo
run_command() {
    echo -e "${YELLOW}Ejecutando: \"$*\"${NC}"
    "$@"
}

# Ejecuta los comandos con la variable COMMAND, que puede ser 'poetry run storycraftr' o 'storycraftr'
#run_command $COMMAND storycraftr init "The Purge of the gods" --primary-language "en" --alternate-languages "es" --author "Rodrigo Estrada" --genre "science fiction" --behavior "behavior.txt" --reference-author="Brandon Sanderson"
#run_command cd "The Purge of the gods"
run_command $COMMAND storycraftr outline general-outline "Summarize the overall plot of a dystopian science fiction where advanced technology, resembling magic, has led to the fall of humanity’s elite and the rise of a manipulative villain who seeks to destroy both the ruling class and the workers."
run_command $COMMAND storycraftr outline character-summary "Summarize the character of Zevid, a villainous mastermind who seeks to destroy both the ruling elite and the workers in a dystopian world where advanced technology mimics magic."
run_command $COMMAND storycraftr outline plot-points "Identify the key plot points of a dystopian novel where a villain manipulates both the elite and the workers to achieve ultimate control in a world where advanced technology mimics magic."
run_command $COMMAND storycraftr outline chapter-synopsis "Outline each chapter of a dystopian society where an ancient elite class, ruling with advanced biotechnology that mimics magic, manipulates both workers and warriors. The protagonist, Zevid, aims to destroy both factions through manipulation, eventually leading to his own version of 'The Purge.'"
run_command $COMMAND storycraftr worldbuilding history "Describe the history of a dystopian world where advanced biotechnology and nanotechnology are perceived as magic, leading to a society where an elite class rules and manipulates both workers and technology to maintain control."
run_command $COMMAND storycraftr worldbuilding geography "Describe the geography of a dystopian world where advanced biotechnology and nanotechnology are seen as magic. Focus on how the elite families control key regions, and the remnants of the world that survived the Purge."
run_command $COMMAND storycraftr worldbuilding culture "Describe the culture of a dystopian society where the elite use advanced biotechnology to maintain power, and the workers live under the illusion that this technology is magic. Focus on how the elite families have developed their own rituals, and how the workers perceive their rulers."
run_command $COMMAND storycraftr worldbuilding technology "Describe the technology of a dystopian world where advanced biotechnology and nanotechnology are perceived as magic. Focus on the elite's use of this technology for immortality, enhanced abilities, and control over the workers, who are unaware of its true nature."
run_command $COMMAND storycraftr worldbuilding magic-system "Describe the magic system in a dystopian world where advanced biotechnology and nanotechnology are mistaken for magic. Explain how the elite families use this 'magic' to control the population, and how the workers have developed their own beliefs around it."
run_command $COMMAND storycraftr chapters chapter 1 "Write Chapter 1 based on the synopsis provided: Zevid is in the final stages of his grand plan. As the rebellion rages outside, he prepares to infiltrate the Dark Tower, the center of the elites' control over biotechnology. The rebellion he orchestrated serves as a distraction while he pursues his true goal of seizing the power within the tower."
run_command $COMMAND storycraftr chapters chapter 2 "Write Chapter 2 based on the synopsis provided: Zevid continues to manipulate the false hero leading the workers. While the workers believe they are liberating themselves from the elite, Zevid uses their blind trust to further his own ends."
run_command $COMMAND storycraftr chapters cover "Generate a cover text for the novel 'The Purge of the Gods' where a villain manipulates both the elite and the workers in a dystopian world of advanced technology disguised as magic."
run_command $COMMAND storycraftr chapters back-cover "Generate a back-cover text for 'The Purge of the Gods,' a dystopian novel where advanced biotechnology is seen as magic, and a cunning villain manipulates both the elite and the workers to achieve ultimate control."
run_command $COMMAND storycraftr publish pdf en
run_command $COMMAND storycraftr publish pdf en --translate es
run_command $COMMAND storycraftr iterate check-names "Check character names for consistency."
run_command $COMMAND storycraftr iterate fix-name Zevid Rhaedin
run_command $COMMAND storycraftr iterate refine-motivation "Rahedin" "Refine its motivations in a story about rebellion against gods."
run_command $COMMAND storycraftr iterate strengthen-argument "Ensure the argument of rebellion against divine control is clear."
run_command $COMMAND storycraftr chapters chapter 3 "progress de history"
run_command $COMMAND storycraftr iterate insert-chapter 2 "Insert a new chapter that explores a critical event from the protagonist’s past, shedding light on their true intentions and setting the stage for the conflict in chapter 1."
run_command $COMMAND storycraftr iterate split-chapter 3 "Split chapter into two chapters."
run_command $COMMAND storycraftr iterate add-flashback 3 "Insert a flashback revealing a hidden alliance the protagonist formed years ago, explaining a key turning point in the current events."

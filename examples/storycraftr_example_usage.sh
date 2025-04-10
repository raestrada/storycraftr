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
Quiero escribir una novela corta con tu ayuda. El concepto del libro es donde el protagonista es un villano absoluto, sin adornos, sin justificaciones. Normlamente se escribe para que el lector tenga empatía, quiero que se escriba de tal forma que un lector sociopata, egoista, inteligente, un posible villano pueda tener empatía. El libro parte de la mitad del argumento donde el protagonista esta a punto de cumplir sus planes. Se alterna con flashback que dan la impresión que van a justificar porque el villano hace lo que hace, pero es un engaño al lector. Al final el es simplemente malavado y solo laguien malvado podría tener empatía con el. Es un mundo en el futuro donde la humanidad ha evolucionado tanto, que la tencología es cais indistinguible de la magía. Nanotecnología avanzada y tecnología genética le ha permitod a la elite del mundo no depender ni de los humanos ni de los robots. Al principio creyeron que a través de robots y automatización lograrían no depender de la población masiva, pero estos solo potenciaron a los más capaces de la clase obrera llegando a un equilibrio con la elite y el mundo siguió aumnentando en desigualdad hasta llegar a ser coontrolado por un pequeño grupo de familias que dependía de los favorecidos profesionales que podía utilizar los robots y la inteligencia artificial. Corrompieron a lo smejores científicos de biotecnología y nanotecnología para generar poderes indistinguibles de la magia y dejar de depender de la clase obrera. Cuando lo logran cumplen sus objetivos de reducir la humanidad y limpiar el planeta de la plaga de los no evolucionados. Genera un sosfisticado virus que limpia la tierra hasta un 5% de su población manteniendo selectivamente a las personas con genes más sumisos para que sean sus plebeyos. Han pasado 1000 años desde este fenomeno conocido como "la purga" y ahora la elite reina en un mundo similar a un mundo de fantasia medieval donde la elite puede vivir indefinidamente si no son asesinados y tiene acceos a distintas "magias" basadas en nanotecnología y biotecnología (ADN) que incluyen mayor velocidad, resistencia, rayos, transportación, fuerza, inteligencia aumentada, visión aumentada o cualqueir combinación de estso poderes. El resto son hijos d ehijos de hijos de gente quie vivió la purga y ha olvidado la tecnología y realmente creen que es magia. La elite se divide en 10 grupos que por diversión combaten para determianr quién es el más poderoso. El que es capaz de conquistar y ocupar más capitales en el mundo, es quién controla al resto, el emperador. mandan a guerreros de elite con super poderes que lideran ejercitos de soldados comunes. Esto es para evitar su aburrimeinto, es más cercano a un ajedrez con vidas humanas que a una verdadera necesidad de recursos. Según las capitales conquistadas, se arma una jeraquía en al elite. Para que sea entretenido, son los de más abajo de estos niveles jerárquicos los que deben mezclarse con los obreros para gestionar las tasreas mundana y ofdiada spor ellos que el planeta todavía requiere como alimentar a este grupo de personas. El protagonista es el hijo de uno de la elite que su familia fue de las orignales, pero que ha caido en el nivel más bajo y debe vivir junto con los obreros. En los flashback se cuenta como al parece sufre, pero en realidad se termian contando como odia y menosprecia a las personaspobre, a esta lcase y tener que vivir con ellos. Odia a su familia por haber caido en desgracia y vive acumulando odio. Su ibjetiv es hacer que los obreros destruyan a la elite, que lo vean como un salvador y luego el va a hacer su propia purga en los obreros donde solo va a seleccionar gente propicia para ser manipulada. Cuando parte el libro, el ya es un lider carismático luchando por el pueblo y su liberación. Ha conseguido que varios de la clase obrera "aprendan magia" y ha generado un estallido terrororista de caos en las principales capitales aengañado a los obreros con que es un liberador y les ha hecho creer a le elite que los quiere destuir y atacar al emperador, pero en realidad es una distracción para acceder al equipo de expertos que manitiene la nanotecnología y la biotecnología de la elite capurarlos y luego manipularlos para poder obtener el contorl maestro de "la magia". Cuando parte, el va camino a el laboratior de expertos aprovechando la guera en los los niuevos supero obreros y la elite. ¿Como logra hacer esto?. El no es atractivo, no es alto, no es fiuerte ... tiene una secuela genética que le impide usar las capacidades "magicas" de la biotencologíoa y la nanotecnología de la elite, pero luego descubre que ese mism defecto tiene como consecuencia habilidades sicológicas excepcionales, el puede entender exactamente como pienzan las personas e incluso predecir sus acciones solo "capturando un perfil de ellos". Además es un excleente improvisador y es capaz de aprender a velocidades inhumanas y entender cualqueir situación.

En el cpaitulo uno el labopratorio se llama la torre oscura ubicada en la gran plaza del crepúsculo. Me encanta que este escondida a vista de todos, es genia. Pero, Zevid tuvo que provocar un caos, terrorismo una revolución y una amenaza a los eternos para lograr accederla. Esta torre debe estar protegida. Que sea el grupo de los mejores guerreros de los eternos, evolcionados durante 1000 años, dominan toda "la magia". Son 10 (uno por familia poderosa) y ellos están encubiertos  protegiendo la torre, mientras ellos estuvieran rondando, es imposible entrar sin autorización. Sólo una revoluciçón y una guerra tipo cataclismo los obligaria. Por eso trabajo en un heroico grupo que de terrenalñes que son muchops y juntos y ocn uso de magia, son un desafi lo suficientemente grande para que estos guardias despejara la torre osucra. Ponle un nombre a este grupo.

me encantaría que se rompiera el cliche del protagonista alto, inteligente, perfecto, carismático ... recuerda que Zevid su unica gracia es que pese a ser un sociopata falto d eempatía si era capaz de comprender a la perfección a las personas, sus verdasderas intenciones, su pensamiento oculto, ver a través de la imagen ... hasta el punto de predecir. Eso es sú unica vemntaja, pero es extrema. El idera de abajo, entre las sombras ... a tal punto que se hace pasar por el lugarteniente de un héroe ficticio perfecto, como el de las novelas de fantasía (ionspirate en kelsier).

De Ahora en adelante, quiero que seas mi asistente para escribir la novela corta. Basate en el estilo de escriotura de Brandon Sanderson.
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
run_command 'init "The Purge of the gods" --primary-language "en" --alternate-languages "es" --author "Rodrigo Estrada" --genre "science fiction" --behavior "behavior.txt" --reference-author="Brandon Sanderson" --openai-model "gpt-4o-mini"' || exit 1

cd "The Purge of the gods"

# Ejecutar los comandos originales
run_command 'outline general-outline "Summarize the overall plot of a dystopian science fiction where advanced technology, resembling magic, has led to the fall of humanity'"'"'s elite and the rise of a manipulative villain who seeks to destroy both the ruling class and the workers."' || exit 1

run_command 'outline character-summary "Summarize the character of Zevid, a villainous mastermind who seeks to destroy both the ruling elite and the workers in a dystopian world where advanced technology mimics magic."' || exit 1

run_command 'outline plot-points "Identify the key plot points of a dystopian novel where a villain manipulates both the elite and the workers to achieve ultimate control in a world where advanced technology mimics magic."' || exit 1

run_command 'outline chapter-synopsis "Outline each chapter of a dystopian society where an ancient elite class, ruling with advanced biotechnology that mimics magic, manipulates both workers and warriors. The protagonist, Zevid, aims to destroy both factions through manipulation, eventually leading to his own version of '"'"'The Purge.'"'"'"' || exit 1

run_command 'worldbuilding history "Describe the history of a dystopian world where advanced biotechnology and nanotechnology are perceived as magic, leading to a society where an elite class rules and manipulates both workers and technology to maintain control."' || exit 1

run_command 'worldbuilding geography "Describe the geography of a dystopian world where advanced biotechnology and nanotechnology are seen as magic. Focus on how the elite families control key regions, and the remnants of the world that survived the Purge."' || exit 1

run_command 'worldbuilding culture "Describe the culture of a dystopian society where the elite use advanced biotechnology to maintain power, and the workers live under the illusion that this technology is magic. Focus on how the elite families have developed their own rituals, and how the workers perceive their rulers."' || exit 1

run_command 'worldbuilding technology "Describe the technology of a dystopian world where advanced biotechnology and nanotechnology are perceived as magic. Focus on the elite'"'"'s use of this technology for immortality, enhanced abilities, and control over the workers, who are unaware of its true nature."' || exit 1

run_command 'worldbuilding magic-system "Describe the magic system in a dystopian world where advanced biotechnology and nanotechnology are mistaken for magic. Explain how the elite families use this '"'"'magic'"'"' to control the population, and how the workers have developed their own beliefs around it."' || exit 1

run_command 'chapters chapter 1 "Write Chapter 1 based on the synopsis provided: Zevid is in the final stages of his grand plan. As the rebellion rages outside, he prepares to infiltrate the Dark Tower, the center of the elites'"'"' control over biotechnology. The rebellion he orchestrated serves as a distraction while he pursues his true goal of seizing the power within the tower."' || exit 1

run_command 'chapters chapter 2 "Write Chapter 2 based on the synopsis provided: Zevid continues to manipulate the false hero leading the workers. While the workers believe they are liberating themselves from the elite, Zevid uses their blind trust to further his own ends."' || exit 1

run_command 'chapters cover "Generate a cover text for the novel '"'"'The Purge of the Gods'"'"' where a villain manipulates both the elite and the workers in a dystopian world of advanced technology disguised as magic."' || exit 1

run_command 'chapters back-cover "Generate a back-cover text for '"'"'The Purge of the Gods,'"'"' a dystopian novel where advanced biotechnology is seen as magic, and a cunning villain manipulates both the elite and the workers to achieve ultimate control."' || exit 1

run_command 'publish pdf en' || exit 1

run_command 'publish pdf en --translate es' || exit 1

run_command 'iterate check-names "Check character names for consistency."' || exit 1

run_command 'iterate fix-name Zevid Rhaedin' || exit 1

run_command 'iterate refine-motivation "Rhaedin" "Refine its motivations in a story about rebellion against gods."' || exit 1

run_command 'iterate strengthen-argument "Ensure the argument of rebellion against divine control is clear."' || exit 1

run_command 'chapters chapter 3 "progress de history"' || exit 1

run_command 'iterate insert-chapter 2 "Insert a new chapter that explores a critical event from the protagonist'"'"'s past, shedding light on their true intentions and setting the stage for the conflict in chapter 1."' || exit 1

run_command 'iterate split-chapter 1 "Split chapter into two chapters."' || exit 1

run_command 'iterate add-flashback 1 "Insert a flashback revealing a hidden alliance the protagonist formed years ago, explaining a key turning point in the current events."' || exit 1

echo -e "${GREEN}Example usage for StoryCraftr completed successfully${NC}"

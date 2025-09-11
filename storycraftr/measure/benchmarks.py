BENCHMARKS = [
    {
        "id": "summarization_1",
        "name": "Text Summarization",
        "prompt": "Summarize the following text in one sentence: The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889 as the centerpiece of the 1889 World's Fair, it was initially criticized by some of France's leading artists and intellectuals for its design, but it has become a global cultural icon of France and one of the most recognizable structures in the world.",
        "reference_text": "The Eiffel Tower, designed by Gustave Eiffel, is a famous wrought-iron tower in Paris, France, built for the 1889 World's Fair and is now a global cultural icon.",
    },
    {
        "id": "qa_1",
        "name": "Question Answering",
        "prompt": "Based on the following text, who designed the Eiffel Tower? The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower.",
        "reference_text": "Gustave Eiffel.",
    },
    {
        "id": "structured_output_1",
        "name": "Structured Output",
        "prompt": "Extract information about the Eiffel Tower from this text and respond in valid JSON format with exactly these fields: designer, location, construction_start, construction_end, purpose. Text: The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France. It is named after the engineer Gustave Eiffel, whose company designed and built the tower. Constructed from 1887 to 1889 as the centerpiece of the 1889 World's Fair.",
        "reference_text": '{"designer": "Gustave Eiffel", "location": "Paris, France", "construction_start": "1887", "construction_end": "1889", "purpose": "1889 World\'s Fair centerpiece"}',
        "type": "structured",
    },
    {
        "id": "creative_writing_1",
        "name": "Creative Writing",
        "prompt": "Continue the following story: The old clockmaker adjusted his spectacles and peered at the tiny gears. He had been working on this particular watch for weeks, but something was not quite right. Suddenly,",
        "reference_text": "he heard a soft ticking sound from a corner of the room he had never noticed before. As he turned, he saw a small, ornate box glowing with a faint blue light. The ticking was coming from inside.",
    },
]

let synth = null;

function initAudio() {
    if (!synth) {
        synth = new Tone.Synth().toDestination();
    }
}

function playClassificationSound(classification) {
    initAudio();
    
    // Different notes for different waste types
    const notes = {
        'biodegradable': 'C4',
        'non-biodegradable': 'E4',
        'chemical': 'G4'
    };

    // Play the corresponding note
    const note = notes[classification] || 'C4';
    synth.triggerAttackRelease(note, '0.5');

    // Speak the classification
    const utterance = new SpeechSynthesisUtterance(
        `This is ${classification} waste. Please use the ${getColorName(classification)} bin.`
    );
    window.speechSynthesis.speak(utterance);
}

function getColorName(classification) {
    const colors = {
        'biodegradable': 'green',
        'non-biodegradable': 'blue',
        'chemical': 'black'
    };
    return colors[classification] || 'unknown';
}

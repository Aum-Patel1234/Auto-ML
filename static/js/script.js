function showTick(selected) {
    const classificationRadioTick = document.getElementById('classification-tick');
    const regressionRadioTick = document.getElementById('regression-tick');
    
    classificationRadioTick.classList.add('hidden');
    regressionRadioTick.classList.add('hidden');

    if (selected === 'classification') {
        classificationRadioTick.classList.remove('hidden');
    } else {
        regressionRadioTick.classList.remove('hidden');
    }
}
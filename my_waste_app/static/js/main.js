document.addEventListener('DOMContentLoaded', function() {
    const imageInput = document.getElementById('imageInput');
    const preview = document.getElementById('preview');
    const placeholder = document.getElementById('placeholder');
    const result = document.getElementById('result');
    const binColor = document.getElementById('binColor');
    const binType = document.getElementById('binType');
    const confidence = document.getElementById('confidence');

    // Handle image upload
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.classList.remove('d-none');
                placeholder.classList.add('d-none');
                classifyImage(file);
            }
            reader.readAsDataURL(file);
        }
    });

    // Classify the image
    async function classifyImage(file) {
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('/classify', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Classification failed');
            }

            const data = await response.json();
            displayResult(data);
            playClassificationSound(data.classification);
        } catch (error) {
            console.error('Error:', error);
            alert('Error classifying image. Please try again.');
        }
    }

    // Display classification result
    function displayResult(data) {
        result.classList.remove('d-none');
        binColor.style.backgroundColor = data.bin_color;
        binType.textContent = data.classification.charAt(0).toUpperCase() + 
                            data.classification.slice(1) + ' Waste';
        confidence.textContent = `Confidence: ${Math.round(data.confidence * 100)}%`;
    }
});

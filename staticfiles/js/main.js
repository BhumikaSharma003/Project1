document.addEventListener('DOMContentLoaded', () => {
    // Drag & Drop functionality
    const dropZone = document.getElementById('drop-zone');
    const fileInput = document.getElementById('file-input');
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if(files.length) handleFile(files[0]);
    });

    fileInput.addEventListener('change', (e) => {
        if(e.target.files.length) handleFile(e.target.files[0]);
    });

    // Load apps
    fetch('/api/apps/')
        .then(response => response.json())
        .then(apps => {
            const container = document.getElementById('apps-list');
            apps.forEach(app => {
                container.innerHTML += `
                    <div class="list-group-item app-card mb-3">
                        <div class="d-flex justify-content-between">
                            <div>
                                <h5>${app.name}</h5>
                                <p class="mb-0">Points: ${app.points}</p>
                            </div>
                            <div>
                                <span class="badge bg-primary">Available</span>
                            </div>
                        </div>
                    </div>
                `;
            });
        });
});

function handleFile(file) {
    const formData = new FormData();
    formData.append('screenshot', file);
    
    fetch('/api/tasks/', {
        method: 'POST',
        headers: {
            'Authorization': `Token ${localStorage.getItem('token')}`
        },
        body: formData
    })
    .then(response => {
        if(response.ok) {
            alert('Screenshot uploaded successfully!');
        } else {
            alert('Upload failed. Please try again.');
        }
    });
}
document.addEventListener("DOMContentLoaded", function () {

    // Resize textareas
    const textareas = document.querySelectorAll('textarea[name="notes"]');

    textareas.forEach(textarea => {
        textarea.addEventListener('input', autoResize);

        function autoResize() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        }
    });

    // Delete confirmation
    document.getElementById('deleteSessionForm').addEventListener('submit', function(e) {
    if (!confirm('Delete this session and lose all practice data?')) {
      e.preventDefault();
    }
    });

    // Modal

    const sessionModal = document.getElementById('sessionModal');


    sessionModal.addEventListener('show.bs.modal', function (event) {


        const button = event.relatedTarget;

        const sessionId = button.getAttribute('data-id');
        const minutes = button.getAttribute('data-minutes');
        const notes = button.getAttribute('data-notes');
        
        
        // Fill form fields
        document.getElementById('modalMinutes').value = minutes;
        document.getElementById('modalNotes').value = notes;

        // Update form action URLs dynamically
        document.getElementById('editSessionForm').action =
            `/session/${sessionId}/edit`;

        document.getElementById('deleteSessionForm').action =
            `/session/${sessionId}/delete`;
    });



});
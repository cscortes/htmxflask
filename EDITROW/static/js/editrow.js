/**
 * EDITROW Example - Minimal JavaScript for HTMX Integration
 * 
 * This file demonstrates the minimal JavaScript needed when HTMX alone isn't sufficient.
 * It handles single-instance editing to prevent multiple rows from being edited simultaneously.
 * 
 * Following Development Guiding Light principles:
 * - Minimal JavaScript (only what HTMX cannot handle)
 * - Clear documentation of why JavaScript is needed
 * - Focused functionality without over-engineering
 */

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    // Set up event delegation for edit buttons
    document.addEventListener('click', function(event) {
        // Only handle clicks on edit buttons
        if (event.target.matches('.btn.primary[data-contact-id]')) {
            event.preventDefault();
            
            // Check if another row is already being edited
            const currentlyEditing = document.querySelector('.editing');
            
            if (currentlyEditing) {
                // Ask user if they want to cancel current edit
                if (confirm('Another row is being edited. Cancel that edit and continue?')) {
                    // Cancel current edit by triggering the cancel event
                    htmx.trigger(currentlyEditing, 'cancel');
                    
                    // Small delay to ensure cancel completes before starting new edit
                    setTimeout(() => {
                        htmx.trigger(event.target, 'edit');
                    }, 100);
                }
            } else {
                // No row is being edited, proceed with edit
                htmx.trigger(event.target, 'edit');
            }
        }
    });
    
    // Add visual feedback for successful updates
    document.addEventListener('htmx:afterSwap', function(event) {
        const updatedRow = event.target;
        
        // Check if this is an updated row (not an edit form)
        if (updatedRow.classList.contains('updated-row')) {
            // Add temporary success styling
            updatedRow.style.backgroundColor = '#d4edda';
            updatedRow.style.border = '2px solid #28a745';
            
            // Remove success styling after 2 seconds
            setTimeout(() => {
                updatedRow.style.backgroundColor = '';
                updatedRow.style.border = '';
                updatedRow.classList.remove('updated-row');
            }, 2000);
        }
    });
    
    // Handle edit form focus management
    document.addEventListener('htmx:afterSwap', function(event) {
        const editForm = event.target;
        
        // If this is an edit form, focus the first input
        if (editForm.classList.contains('editing')) {
            const firstInput = editForm.querySelector('input[autofocus]');
            if (firstInput) {
                firstInput.focus();
            }
        }
    });
});

// SubtitleAI Pro Web Application JavaScript

// Tab functionality
function showTab(tabName) {
    // Hide all tab contents
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.style.display = 'none';
        tab.classList.remove('active');
    });
    
    // Remove active class from all tab buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.style.borderBottomColor = 'transparent';
        btn.style.color = '#666';
    });
    
    // Show selected tab content
    const selectedTab = document.getElementById(`${tabName}-tab`);
    if (selectedTab) {
        selectedTab.style.display = 'block';
        selectedTab.classList.add('active');
    }
    
    // Add active class to selected tab button
    const selectedBtn = event.target;
    selectedBtn.classList.add('active');
    selectedBtn.style.borderBottomColor = '#667eea';
    selectedBtn.style.color = '#667eea';
}

// File upload functionality
function setupFileUpload() {
    const fileUploadArea = document.getElementById('file-upload-area');
    const fileInput = document.getElementById('video-file');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const removeFileBtn = document.getElementById('remove-file');
    const uploadBtn = document.getElementById('upload-btn');
    
    if (!fileUploadArea || !fileInput) return;
    
    // Click to browse
    fileUploadArea.addEventListener('click', () => {
        fileInput.click();
    });
    
    // Drag and drop functionality
    fileUploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = '#667eea';
        fileUploadArea.style.backgroundColor = '#f0f4ff';
    });
    
    fileUploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = '#ccc';
        fileUploadArea.style.backgroundColor = '#f9f9f9';
    });
    
    fileUploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        fileUploadArea.style.borderColor = '#ccc';
        fileUploadArea.style.backgroundColor = '#f9f9f9';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileSelection(e.target.files[0]);
        }
    });
    
    // Remove file
    if (removeFileBtn) {
        removeFileBtn.addEventListener('click', () => {
            fileInput.value = '';
            fileInfo.style.display = 'none';
            fileUploadArea.style.display = 'block';
            uploadBtn.disabled = true;
        });
    }
    
    function handleFileSelection(file) {
        // Validate file type
        const allowedTypes = ['video/mp4', 'video/avi', 'video/mov', 'video/quicktime', 'video/x-msvideo', 'video/x-matroska'];
        if (!allowedTypes.includes(file.type)) {
            showAlert('Invalid file type. Please upload a video file (MP4, AVI, MOV, MKV)', 'error');
            return;
        }
        
        // Validate file size (500MB max)
        const maxSize = 500 * 1024 * 1024;
        if (file.size > maxSize) {
            showAlert('File too large. Maximum size is 500MB.', 'error');
            return;
        }
        
        // Show file info
        fileName.textContent = `📁 ${file.name} (${formatFileSize(file.size)})`;
        fileInfo.style.display = 'block';
        fileUploadArea.style.display = 'none';
        uploadBtn.disabled = false;
    }
}

// File upload submission
async function submitUpload() {
    const fileInput = document.getElementById('video-file');
    const modelSize = document.getElementById('upload-model_size').value;
    const uploadBtn = document.getElementById('upload-btn');
    const progressContainer = document.getElementById('upload-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    if (!fileInput.files[0]) {
        showAlert('Please select a video file', 'error');
        return;
    }
    
    const formData = new FormData();
    formData.append('video_file', fileInput.files[0]);
    formData.append('model_size', modelSize);
    
    // Disable button and show progress
    uploadBtn.disabled = true;
    uploadBtn.innerHTML = '<span class="loading-spinner"></span>Uploading...';
    progressContainer.style.display = 'block';
    
    try {
        const response = await fetch('/submit-upload', {
            method: 'POST',
            body: formData
        });
        
        // Update progress (this is a simple progress simulation)
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 10;
            progressFill.style.width = `${Math.min(progress, 90)}%`;
            progressText.textContent = `${Math.min(progress, 90)}%`;
        }, 200);
        
        const result = await response.json();
        
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        progressText.textContent = '100%';
        
        if (result.success) {
            showAlert(`File uploaded successfully! Processing "${result.filename}" will begin shortly.`, 'success');
            
            // Reset form
            fileInput.value = '';
            document.getElementById('file-info').style.display = 'none';
            document.getElementById('file-upload-area').style.display = 'block';
            progressContainer.style.display = 'none';
            
            // Refresh the page to show the new job
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showAlert(`Upload failed: ${result.error}`, 'error');
            progressContainer.style.display = 'none';
        }
        
    } catch (error) {
        showAlert(`Network error: ${error.message}`, 'error');
        progressContainer.style.display = 'none';
    } finally {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '🚀 Generate Subtitles';
    }
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Job submission
async function submitJob() {
    const url = document.getElementById('videoUrl').value.trim();
    const modelSize = document.getElementById('modelSize').value;
    const submitBtn = document.getElementById('submitBtn');
    const statusDiv = document.getElementById('jobStatus');
    
    if (!url) {
        showAlert('Please enter a YouTube URL', 'error');
        return;
    }
    
    if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
        showAlert('Please enter a valid YouTube URL', 'error');
        return;
    }
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span class="loading-spinner"></span>Submitting...';
    
    try {
        const response = await fetch('/submit-job', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url,
                model_size: modelSize
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Job submitted successfully! Processing will begin shortly.', 'success');
            document.getElementById('videoUrl').value = '';
            
            // Refresh the page to show the new job
            setTimeout(() => {
                window.location.reload();
            }, 2000);
        } else {
            showAlert(`Error: ${result.error}`, 'error');
        }
        
    } catch (error) {
        showAlert(`Network error: ${error.message}`, 'error');
    } finally {
        submitBtn.disabled = false;
        submitBtn.innerHTML = '🚀 Generate Subtitles';
    }
}

// Show alert messages
function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Job status polling
function startJobStatusPolling() {
    const jobCards = document.querySelectorAll('.job-card[data-job-id]');
    
    jobCards.forEach(card => {
        const jobId = card.dataset.jobId;
        const status = card.dataset.status;
        
        if (status === 'pending' || status === 'processing') {
            pollJobStatus(jobId, card);
        }
    });
}

async function pollJobStatus(jobId, cardElement) {
    try {
        const response = await fetch(`/job-status/${jobId}`);
        const result = await response.json();
        
        if (result.success) {
            updateJobCard(cardElement, result);
            
            // Continue polling if still processing
            if (result.status === 'pending' || result.status === 'processing') {
                setTimeout(() => pollJobStatus(jobId, cardElement), 3000);
            }
        }
    } catch (error) {
        console.error('Error polling job status:', error);
    }
}

function updateJobCard(cardElement, jobData) {
    const statusElement = cardElement.querySelector('.job-status');
    const progressElement = cardElement.querySelector('.job-progress');
    const actionsElement = cardElement.querySelector('.job-actions');
    
    // Update status
    statusElement.className = `job-status status-${jobData.status}`;
    statusElement.textContent = jobData.status.toUpperCase();
    
    // Update progress
    if (progressElement) {
        progressElement.textContent = jobData.progress || '';
    }
    
    // Update video title if available
    if (jobData.video_title) {
        const titleElement = cardElement.querySelector('.job-title');
        if (titleElement && titleElement.textContent === 'Processing...') {
            titleElement.textContent = jobData.video_title;
        }
    }
    
    // Update actions
    if (jobData.status === 'completed') {
        actionsElement.innerHTML = `
            <a href="/download/${cardElement.dataset.jobId}" class="btn btn-success">
                📥 Download SRT
            </a>
        `;
    } else if (jobData.status === 'failed') {
        actionsElement.innerHTML = `
            <span style="color: #d32f2f; font-weight: 500;">❌ Failed</span>
        `;
    }
}

// Auto-refresh dashboard
function setupAutoRefresh() {
    const isDashboard = window.location.pathname === '/dashboard';
    const hasActiveJobs = document.querySelectorAll('.status-pending, .status-processing').length > 0;
    
    if (isDashboard && hasActiveJobs) {
        setTimeout(() => {
            window.location.reload();
        }, 30000); // Refresh every 30 seconds
    }
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.style.borderColor = '#dc3545';
            isValid = false;
        } else {
            input.style.borderColor = '#e1e1e1';
        }
    });
    
    return isValid;
}

// Password strength indicator
function checkPasswordStrength(password) {
    const strengthDiv = document.getElementById('passwordStrength');
    if (!strengthDiv) return;
    
    let strength = 0;
    let feedback = [];
    
    if (password.length >= 8) strength++;
    else feedback.push('At least 8 characters');
    
    if (/[A-Z]/.test(password)) strength++;
    else feedback.push('One uppercase letter');
    
    if (/[a-z]/.test(password)) strength++;
    else feedback.push('One lowercase letter');
    
    if (/[0-9]/.test(password)) strength++;
    else feedback.push('One number');
    
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    else feedback.push('One special character');
    
    const colors = ['#dc3545', '#fd7e14', '#ffc107', '#28a745', '#28a745'];
    const labels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    
    strengthDiv.style.color = colors[strength];
    strengthDiv.textContent = strength > 0 ? labels[strength - 1] : '';
    
    if (feedback.length > 0 && password.length > 0) {
        strengthDiv.textContent += ` (Missing: ${feedback.join(', ')})`;
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Setup file upload functionality
    setupFileUpload();
    
    // Start job status polling
    startJobStatusPolling();
    
    // Setup auto-refresh
    setupAutoRefresh();
    
    // Add event listeners
    const submitBtn = document.getElementById('submitBtn');
    if (submitBtn) {
        submitBtn.addEventListener('click', submitJob);
    }
    
    // Add upload button listener
    const uploadBtn = document.getElementById('upload-btn');
    if (uploadBtn) {
        uploadBtn.addEventListener('click', submitUpload);
    }
    
    // Add enter key support for URL input
    const urlInput = document.getElementById('videoUrl');
    if (urlInput) {
        urlInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                submitJob();
            }
        });
    }
    
    // Password strength checker
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function(e) {
            checkPasswordStrength(e.target.value);
        });
    }
    
    // Form validation on submit
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(form.id)) {
                e.preventDefault();
                showAlert('Please fill in all required fields', 'error');
            }
        });
    });
});

// Utility functions
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showAlert('Copied to clipboard!', 'success');
    });
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString();
}

function formatDuration(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    
    if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
}

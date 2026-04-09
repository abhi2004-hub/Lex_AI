// Legal Document Intelligence Platform - Interactive JavaScript

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    setupNavigation();
    setupFileUpload();
    setupAnimations();
    setupDashboard();
    setupScrollEffects();
}

// Navigation smooth scrolling
function setupNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Smooth scroll to section
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// File upload functionality
function setupFileUpload() {
    // Robust selector strategy: prefer explicit IDs, then data-attributes, then common classes
    const uploadZone = document.getElementById('uploadZone')
        || document.querySelector('[data-upload-zone]')
        || document.querySelector('.upload-zone')
        || document.querySelector('.upload')
        || null;

    // Prefer an explicit file input by id, otherwise attempt to discover one inside the upload zone
    const fileInput = document.getElementById('fileInput')
        || (uploadZone && uploadZone.querySelector('input[type="file"]'))
        || document.querySelector('input[type="file"]')
        || null;

    // Browse button: prefer data attribute, then .btn.btn-primary, then .btn-primary, then the first button in uploadZone
    let browseButton = null;
    if (uploadZone) {
        browseButton = uploadZone.querySelector('[data-upload-browse]')
            || uploadZone.querySelector('.btn.btn-primary')
            || uploadZone.querySelector('.btn-primary')
            || uploadZone.querySelector('button');
    } else {
        browseButton = document.querySelector('[data-upload-browse]')
            || document.querySelector('.btn.btn-primary')
            || document.querySelector('.btn-primary')
            || document.querySelector('button');
    }

    console.log('Setup debug:', {
        uploadZone: !!uploadZone,
        fileInput: !!fileInput,
        browseButton: !!browseButton,
        browseButtonClass: browseButton ? browseButton.className : 'not found'
    });

    if (!uploadZone || !fileInput) return;

    // Click to browse — attach if browseButton found
    if (browseButton) {
        // remove any previous listener marker to avoid duplicate handlers in SPA-like reloads
        browseButton.addEventListener('click', function browseClickHandler(e) {
            e.stopPropagation();
            try { fileInput.click(); } catch (err) { console.warn('fileInput click failed', err); }
        });
    }
    
    uploadZone.addEventListener('click', () => {
        try { fileInput.click(); } catch (err) { console.warn('fileInput click failed', err); }
    });
    
    // Drag and drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        handleFiles(files);
    });
    
    fileInput.addEventListener('change', (e) => {
        const files = e.target.files;
        handleFiles(files);
    });
}

function handleFiles(files) {
    if (files.length === 0) return;
    
    // Show loading state
    showAnalysisLoading();
    
    // Create FormData for file upload
    const formData = new FormData();
    formData.append('file', files[0]);
    formData.append('analysis_type', 'detailed');
    formData.append('language', 'en');
    
    // Send to backend API
    fetch('http://127.0.0.1:5000/api/documents/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        // Check if the response is OK (status 200-299)
        if (!response.ok) {
            // If not OK, handle as an error. Read response as text for better error message.
            return response.text().then(text => {
                console.error('Server error response:', text);
                throw new Error(`HTTP error! status: ${response.status} - ${text}`);
            });
        }
        // Check if the response is JSON
        const contentType = response.headers.get("content-type");
        if (contentType && contentType.indexOf("application/json") !== -1) {
            return response.json(); // Only parse as JSON if content-type is json
        } else {
            // If not JSON, but success, perhaps it's an empty response or plain text
            return response.text().then(text => {
                // If text is empty, return an empty object or a default success.
                // Otherwise, you might have an issue with non-json success responses.
                return text ? { success: true, message: text } : { success: true };
            });
        }
    })
    .then(data => {
        if (data.success) {
            showAnalysisResults(data);
        } else {
            showNotification('Error: ' + data.error, 'error');
            resetUploadZone();
        }
    })
    .catch(error => {
        console.error('Upload error:', error);
        console.error('Error details:', error.message);
        showNotification('Upload failed. Please try again. Details: ' + error.message, 'error');
        resetUploadZone();
    });
}

function showAnalysisLoading() {
    const uploadZone = document.getElementById('uploadZone');
    uploadZone.innerHTML = `
        <div class="upload-processing">
            <div class="processing-spinner">
                <i class="fas fa-spinner fa-spin"></i>
            </div>
            <h3>Processing Document...</h3>
            <p>AI models are analyzing your legal document</p>
            <div class="processing-steps">
                <div class="step complete">
                    <i class="fas fa-check"></i>
                    <span>Document parsed</span>
                </div>
                <div class="step active">
                    <i class="fas fa-spinner fa-spin"></i>
                    <span>Extracting clauses</span>
                </div>
                <div class="step">
                    <i class="fas fa-circle"></i>
                    <span>Analyzing risks</span>
                </div>
                <div class="step">
                    <i class="fas fa-circle"></i>
                    <span>Generating insights</span>
                </div>
            </div>
        </div>
    `;
}

function showAnalysisResults(data) {
    console.log('Analysis results received:', data);
    console.log('Analysis data type:', typeof data);
    console.log('Analysis.analysis:', data.analysis);
    console.log('Analysis.analysis type:', typeof data.analysis);
    
    // Hide loading and show results
    const uploadElement = document.getElementById('upload');
    const dashboardElement = document.getElementById('dashboard');
    
    if (uploadElement) {
        uploadElement.style.display = 'none';
    }
    
    if (dashboardElement) {
        dashboardElement.style.display = 'block';
    } else {
        console.error('Dashboard element not found!');
        return;
    }
    
    // Update dashboard with real data
    updateDashboard(data);
    
    // Show success notification
    showNotification('Document analysis completed successfully!', 'success');
}

function resetUploadZone() {
    const uploadZone = document.getElementById('uploadZone');
    if (uploadZone) {
        uploadZone.innerHTML = `
            <div class="upload-content">
                <div class="upload-icon">
                    <i class="fas fa-cloud-upload-alt"></i>
                </div>
                <h3>Upload Legal Document</h3>
                <p>Drag and drop your legal document here or click to browse</p>
                <p class="upload-hint">Supports PDF, DOCX, and TXT files (Max 50MB)</p>
                <button class="btn btn-primary" data-upload-browse>Choose File</button>
                <input type="file" id="fileInput" accept=".pdf,.docx,.txt" hidden>
            </div>
        `;
        // Re-attach event listeners
        setupFileUpload();
    }
}

// Dashboard functionality
function setupDashboard() {
    initializeRiskChart();
    setupClauseInteractions();
}

function initializeRiskChart() {
    const ctx = document.getElementById('riskChart');
    if (!ctx) return;
    
    // Store in window so updateRiskChart can destroy it before redrawing with real data
    window.riskChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk', 'Medium Risk', 'High Risk'],
            datasets: [{
                data: [65, 25, 10],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(239, 68, 68, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                }
            }
        }
    });
}


function setupClauseInteractions() {
    const clauseItems = document.querySelectorAll('.clause-item');
    
    clauseItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remove active state from all items
            clauseItems.forEach(i => i.classList.remove('active'));
            this.classList.add('active');
            
            // Show detailed explanation
            showClauseExplanation(this);
        });
    });
}

function showDetailedClauseAnalysis(clause) {
    // Show detailed analysis in explanation section
    const explanationContent = document.querySelector('.explanation-content p');
    const shapContainer = document.querySelector('.shap-values');
    const limeContainer = document.querySelector('.lime-explanation');
    
    // Parse plain language robustly
    let plainMeaningData = { plain_meaning: "No plain language translation available." };
    if (clause.risk_assessment && clause.risk_assessment.plain_language) {
        try {
            plainMeaningData = JSON.parse(clause.risk_assessment.plain_language);
        } catch(e) {
            plainMeaningData.plain_meaning = clause.risk_assessment.plain_language;
        }
    }
    
    let parsedRecommendations = clause.risk_assessment?.recommendations || '[]';
    try {
        const arr = JSON.parse(parsedRecommendations);
        if (Array.isArray(arr) && arr.length > 0) parsedRecommendations = arr[0];
    } catch(e) {}
    
    if (explanationContent) {
        explanationContent.innerHTML = `
            <strong>Clause Type:</strong> ${clause.clause_type}<br>
            <strong>Risk Level:</strong> <span class="risk-badge risk-${clause.risk_assessment?.risk_level || 'low'}">${clause.risk_assessment?.risk_level?.toUpperCase() || 'LOW'}</span><br>
            <strong>Confidence:</strong> ${(clause.confidence_score * 100).toFixed(1)}%<br><br>
            <strong>What this means:</strong> ${plainMeaningData.plain_meaning || 'Standard clause.'}<br>
            <strong>Real-world Impact:</strong> ${plainMeaningData.real_world_impact || '-'}<br><br>
            <strong>Our Recommendation:</strong> ${parsedRecommendations || 'Standard clause with no significant risks identified.'}<br><br>
            <strong>Key Risk Factors:</strong><br>
            ${getRiskFactorsHTML(clause.risk_assessment?.risk_factors || '[]')}
        `;
    }
    
    // Update SHAP values
    if (shapContainer && clause.risk_assessment?.shap_values) {
        updateSHAPDisplay(clause.risk_assessment.shap_values);
    }
    
    // Update LIME explanation
    if (limeContainer && clause.risk_assessment?.lime_explanation) {
        updateLIMEDisplay(clause.risk_assessment.lime_explanation);
    }
}

function getRiskFactorsHTML(riskFactors) {
    try {
        const factors = riskFactors || [];
        if (factors.length === 0) {
            return '<span class="no-factors">No specific risk factors identified.</span>';
        }
        
        return factors.map(factor => `
            <div class="risk-factor">
                <div class="factor-header">
                    <span class="factor-name">${factor.factor}</span>
                    <span class="factor-severity severity-${factor.severity}">${factor.severity.toUpperCase()}</span>
                </div>
                <div class="factor-description">${factor.description}</div>
            </div>
        `).join('');
    } catch (e) {
        return '<span class="no-factors">Risk factors analysis not available.</span>';
    }
}

function updateSHAPDisplay(shapValues) {
    try {
        const shapContainer = document.querySelector('.shap-values');
        if (!shapContainer) return;

        // Create sample SHAP data if not provided
        const shapData = shapValues && shapValues.words ? shapValues : {
            words: ['termination', 'compensation', 'liability', 'confidentiality', 'duration'],
            values: [0.8, 0.6, 0.4, -0.2, -0.1]
        };

        // Build markup for each SHAP entry
        const itemsHTML = shapData.words.map((word, index) => {
            const val = shapData.values[index] || 0;
            const cls = val >= 0 ? 'positive' : 'negative';
            return `
                <div class="shap-item">
                    <span class="shap-word">${word}</span>
                    <div class="shap-bar-container">
                        <div class="shap-bar ${cls}" style="width: ${Math.abs(val) * 100}%"></div>
                    </div>
                    <span class="shap-value">${val.toFixed(3)}</span>
                </div>`;
        }).join('');

        shapContainer.innerHTML = `
            <h4>SHAP Values - Feature Importance</h4>
            <div class="shap-chart">
                ${itemsHTML}
            </div>
        `;

    } catch (e) {
        console.error('Error displaying SHAP values:', e);
    }
}

function updateLIMEDisplay(limeExplanation) {
    try {
        const limeContainer = document.querySelector('.lime-explanation');
        
        if (!limeContainer) return;
        
        // Create sample LIME data if not provided
        const limeData = limeExplanation && limeExplanation.explanation ? limeExplanation : {
            explanation: 'This employment agreement contains several clauses that contribute to the overall risk assessment. Key factors include termination conditions, compensation structures, and liability limitations.',
            features: [
                { feature: 'Termination Clause', importance: 0.8 },
                { feature: 'Compensation Structure', importance: 0.6 },
                { feature: 'Liability Limitation', importance: 0.4 },
                { feature: 'Confidentiality', importance: 0.3 }
            ]
        };
        
        limeContainer.innerHTML = `
            <h4>LIME Explanation - Local Interpretation</h4>
            <div class="lime-content">
                <div class="lime-explanation-text">
                    <p><strong>Explanation:</strong> ` + limeData.explanation + `</p>
                </div>
                <div class="lime-features">
                    <h5>Key Features:</h5>
                    ` + limeData.features.map(feature => 
                        `<div class="lime-feature">
                            <span class="feature-name">` + feature.feature + `</span>
                            <span class="feature-importance" style="width: ` + (feature.importance * 100) + `%"></span>
                            <span class="feature-value">` + feature.importance.toFixed(3) + `</span>
                        </div>`
                    ).join('') + `
                </div>
            </div>
        `;
        
    } catch (e) {
        console.error('Error displaying LIME explanation:', e);
    }
}

function animateSHAPValues() {
    const importanceBars = document.querySelectorAll('.importance-fill');
    
    importanceBars.forEach((bar, index) => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 100 * index);
    });
}

// Scroll effects
function setupScrollEffects() {
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;
    
    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;
        
        // Navbar background on scroll
        if (currentScroll > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.98)';
            navbar.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.boxShadow = 'none';
        }
        
        lastScroll = currentScroll;
    });
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe feature cards and dashboard cards
    document.querySelectorAll('.feature-card, .dashboard-card').forEach(card => {
        observer.observe(card);
    });
}

// Animations
function setupAnimations() {
    // Add CSS animation class
    const style = document.createElement('style');
    style.textContent = `
        .animate-in {
            animation: slideInUp 0.6s ease-out forwards;
        }
        
        @keyframes slideInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .upload-processing {
            text-align: center;
            padding: 2rem;
        }
        
        .processing-spinner {
            font-size: 3rem;
            color: var(--primary);
            margin-bottom: 1.5rem;
        }
        
        .processing-steps {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            margin-top: 1.5rem;
            text-align: left;
            max-width: 300px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .step {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-size: 0.875rem;
            color: var(--gray);
        }
        
        .step.complete {
            color: var(--success);
        }
        
        .step.active {
            color: var(--primary);
        }
        
        .clause-item.active {
            border-color: var(--primary);
            background: rgba(37, 99, 235, 0.05);
            transform: translateX(4px);
        }
        
        .notification {
            position: fixed;
            top: 100px;
            right: 20px;
            padding: 1rem 1.5rem;
            border-radius: 0.5rem;
            color: white;
            font-weight: 600;
            z-index: 2000;
            animation: slideInRight 0.3s ease-out;
            box-shadow: var(--shadow-lg);
        }
        
        .notification.success {
            background: var(--success);
        }
        
        .notification.error {
            background: var(--danger);
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);
}

// Utility functions
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

function updateDashboard(analysisData) {
    // Ensure document is available
    if (typeof document === 'undefined' || !document.querySelector) {
        console.error('Document or querySelector not available in updateDashboard');
        return;
    }
    
    // Update risk chart with real backend data
    updateRiskChart(analysisData);
    
    // Update clauses list
    updateClausesList(analysisData.clauses);
    
    // Update document summary
    updateDocumentSummary(analysisData.document, analysisData.analysis);
    
    // Update AI Verdict card
    updateVerdictCard(analysisData.analysis);
    
    // Add animation to dashboard cards
    document.querySelectorAll('.dashboard-card').forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 * index);
    });
}

function updateRiskChart(analysisData) {
    const ctx = document.getElementById('riskChart');
    if (!ctx) {
        console.error('Risk chart canvas not found!');
        return;
    }
    
    // Get risk distribution from backend — it may be a JSON string or object
    let riskDistribution = { low: 0, medium: 0, high: 0, critical: 0 };
    try {
        const raw = analysisData.analysis ? analysisData.analysis.risk_distribution : null;
        if (raw) {
            riskDistribution = typeof raw === 'string' ? JSON.parse(raw) : raw;
        }
    } catch(e) {
        console.warn('Could not parse risk_distribution:', e);
    }

    const total = (riskDistribution.low || 0) + (riskDistribution.medium || 0) + 
                  (riskDistribution.high || 0) + (riskDistribution.critical || 0);

    // Update the legend spans with real data
    const fmt = (n) => total > 0 ? `${n} (${((n/total)*100).toFixed(0)}%)` : `${n}`;
    const legLow = document.getElementById('legendLow');
    const legMed = document.getElementById('legendMedium');
    const legHigh = document.getElementById('legendHigh');
    const legCrit = document.getElementById('legendCritical');
    if (legLow) legLow.textContent = fmt(riskDistribution.low || 0);
    if (legMed) legMed.textContent = fmt(riskDistribution.medium || 0);
    if (legHigh) legHigh.textContent = fmt(riskDistribution.high || 0);
    if (legCrit) legCrit.textContent = fmt(riskDistribution.critical || 0);
    
    // Destroy existing chart if it exists
    try {
        if (window.riskChartInstance) {
            window.riskChartInstance.destroy();
            window.riskChartInstance = null;
            console.log('Previous chart destroyed');
        }
    } catch (error) {
        console.warn('Error destroying chart:', error);
        window.riskChartInstance = null;
    }
    
    // Clear the canvas
    const context = ctx.getContext('2d');
    context.clearRect(0, 0, ctx.width, ctx.height);
    
    // Create new chart with real data
    try {
        window.riskChartInstance = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Low Risk', 'Medium Risk', 'High Risk', 'Critical Risk'],
            datasets: [{
                data: [
                    riskDistribution.low || 0,
                    riskDistribution.medium || 0,
                    riskDistribution.high || 0,
                    riskDistribution.critical || 0
                ],
                backgroundColor: [
                    'rgba(16, 185, 129, 0.8)',
                    'rgba(245, 158, 11, 0.8)',
                    'rgba(239, 68, 68, 0.8)',
                    'rgba(127, 29, 29, 0.8)'
                ],
                borderColor: [
                    'rgba(16, 185, 129, 1)',
                    'rgba(245, 158, 11, 1)',
                    'rgba(239, 68, 68, 1)',
                    'rgba(127, 29, 29, 1)'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        font: {
                            size: 12,
                            weight: '600'
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed || 0;
                            const percentage = ((value / total) * 100).toFixed(1);
                            return `${label}: ${value} clauses (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
    
    } catch (error) {
        console.error('Error creating chart:', error);
    }
}


function updateClausesList(clauses) {
    // Ensure document is available
    if (typeof document === 'undefined' || !document.querySelector) {
        console.error('Document or querySelector not available');
        return;
    }
    
    const clausesContainer = document.querySelector('.clauses-list');
    if (!clausesContainer || !clauses) return;
    
    // Clear existing clauses
    clausesContainer.innerHTML = '';
    
    // Add each clause
    clauses.forEach((clause, index) => {
        const clauseElement = createClauseElement(clause, index);
        clausesContainer.appendChild(clauseElement);
    });
}

function createClauseElement(clause, index) {
    const div = document.createElement('div');
    div.className = 'clause-item';
    
    // Parse plain language safely
    let plainMeaningDisplay = "";
    if (clause.risk_assessment && clause.risk_assessment.plain_language) {
        try {
            const data = JSON.parse(clause.risk_assessment.plain_language);
            plainMeaningDisplay = data.plain_meaning ? data.plain_meaning : clause.risk_assessment.plain_language;
        } catch(e) {
            plainMeaningDisplay = clause.risk_assessment.plain_language;
        }
    }
    
    div.innerHTML = `
        <div class="clause-header">
            <h4>${clause.clause_type}</h4>
            <span class="risk-badge risk-${clause.risk_assessment?.risk_level || 'low'}">
                ${clause.risk_assessment?.risk_level?.toUpperCase() || 'LOW'}
            </span>
        </div>
        <div class="clause-text" style="margin-bottom: 8px;">
            <i style="color: grey;">Original Text:</i><br>
            ${clause.clause_text.substring(0, 200)}${clause.clause_text.length > 200 ? '...' : ''}
        </div>
        ${plainMeaningDisplay ? `
        <div class="clause-plain-text" style="color: #3b82f6; font-size: 0.9em; background: rgba(59, 130, 246, 0.1); padding: 8px; border-radius: 4px; margin-bottom: 12px; border-left: 3px solid #3b82f6;">
            <strong>Simple Terms:</strong> ${plainMeaningDisplay}
        </div>
        ` : ''}
        <div class="clause-meta">
            <span class="confidence">Confidence: ${(clause.confidence_score * 100).toFixed(1)}%</span>
            ${clause.section_reference ? `<span class="reference">${clause.section_reference}</span>` : ''}
        </div>
    `;
    
    // Add click event for detailed analysis
    div.addEventListener('click', () => showDetailedClauseAnalysis(clause));
    
    return div;
}

function updateDocumentSummary(document, analysis) {
    // Ensure document is available
    if (typeof document === 'undefined' || !document.querySelector) {
        console.error('Document or querySelector not available in updateDocumentSummary');
        return;
    }
    
    // Update document summary section
    const summarySection = document.querySelector('.document-summary');
    if (!summarySection) return;
    
    summarySection.innerHTML = `
        <div class="summary-content">
            <h3>Document Analysis Summary</h3>
            <div class="summary-grid">
                <div class="summary-item">
                    <h4>Document Type</h4>
                    <p>Employment Agreement</p>
                </div>
                <div class="summary-item">
                    <h4>Total Clauses</h4>
                    <p>${clauses?.length || 0}</p>
                </div>
                <div class="summary-item">
                    <h4>Processing Time</h4>
                    <p>${analysis?.processing_time ? (analysis.processing_time).toFixed(2) + 's' : 'N/A'}</p>
                </div>
                <div class="summary-item">
                    <h4>Overall Risk</h4>
                    <p>${getOverallRiskLevel(analysis?.overall_risk_score || 0.5)}</p>
                </div>
            </div>
            <div class="detailed-explanation">
                <h4>Document Overview</h4>
                <p>This employment agreement contains ${clauses?.length || 0} identified clauses with varying risk levels. 
                ${getDocumentExplanation(analysis)}</p>
            </div>
        </div>
    `;
}

function getOverallRiskLevel(riskScore) {
    if (riskScore >= 0.75) return 'HIGH RISK';
    if (riskScore >= 0.5) return 'MEDIUM RISK';
    if (riskScore >= 0.25) return 'LOW RISK';
    return 'VERY LOW RISK';
}

function getDocumentExplanation(analysis) {
    const riskDist = analysis ? (analysis.risk_distribution || {}) : {};
    const total = Object.values(riskDist).reduce((a, b) => a + b, 0);
    
    if (total === 0) return 'No significant risks were identified in this document.';
    
    let explanation = 'The analysis identified ';
    
    if (riskDist.critical > 0) {
        explanation += `${riskDist.critical} critical risk clause${riskDist.critical > 1 ? 's' : ''}, `;
    }
    if (riskDist.high > 0) {
        explanation += `${riskDist.high} high risk clause${riskDist.high > 1 ? 's' : ''}, `;
    }
    if (riskDist.medium > 0) {
        explanation += `${riskDist.medium} medium risk clause${riskDist.medium > 1 ? 's' : ''}, `;
    }
    if (riskDist.low > 0) {
        explanation += `and ${riskDist.low} low risk clause${riskDist.low > 1 ? 's' : ''}. `;
    }
    
    explanation += 'Review high and critical risk clauses carefully before proceeding.';
    
    return explanation;
}

// Mobile menu toggle (for responsive design)
function setupMobileMenu() {
    const mobileMenuButton = document.createElement('button');
    mobileMenuButton.className = 'mobile-menu-toggle';
    mobileMenuButton.innerHTML = '<i class="fas fa-bars"></i>';
    
    const navbar = document.querySelector('.nav-container');
    if (navbar) {
        navbar.appendChild(mobileMenuButton);
        
        mobileMenuButton.addEventListener('click', () => {
            const navMenu = document.querySelector('.nav-menu');
            navMenu.classList.toggle('mobile-open');
        });
    }
}

// Initialize mobile menu if needed
if (window.innerWidth <= 768) {
    setupMobileMenu();
}

window.addEventListener('resize', () => {
    if (window.innerWidth <= 768) {
        if (!document.querySelector('.mobile-menu-toggle')) {
            setupMobileMenu();
        }
    } else {
        const mobileToggle = document.querySelector('.mobile-menu-toggle');
        if (mobileToggle) {
            mobileToggle.remove();
        }
    }
});
function updateVerdictCard(analysis) {
    const container = document.getElementById('verdictContainer');
    if (!container || !analysis || !analysis.verdict) return;
    
    const verdict = analysis.verdict;
    let cardClass = 'bg-surface-container-lowest';
    let icon = 'info';
    let iconClass = 'text-primary';
    let statusLabel = 'ANALYSIS COMPLETE';
    let badgeClass = 'bg-surface-container-high text-on-surface';
    
    // Determine style based on verdict status
    if (verdict.includes('STATUS: SAFE TO PROCEED')) {
        cardClass = 'bg-emerald-50 border-emerald-200';
        icon = 'check_circle';
        iconClass = 'text-emerald-600';
        statusLabel = 'SAFE TO PROCEED';
        badgeClass = 'bg-emerald-600 text-white';
    } else if (verdict.includes('STATUS: PROCEED WITH CAUTION')) {
        cardClass = 'bg-amber-50 border-amber-200';
        icon = 'warning';
        iconClass = 'text-amber-600';
        statusLabel = 'PROCEED WITH CAUTION';
        badgeClass = 'bg-amber-600 text-white';
    } else if (verdict.includes('STATUS: CONTACT A LAWYER')) {
        cardClass = 'bg-red-50 border-red-200';
        icon = 'gavel';
        iconClass = 'text-red-700';
        statusLabel = 'CONTACT A LAWYER';
        badgeClass = 'bg-red-700 text-white';
    }
    
    // Clean up the verdict text by removing the STATUS: prefix for the rationale
    const rationale = verdict.replace(/STATUS: [^.]+./, '').trim();
    
    container.innerHTML = `
        <div class="relative overflow-hidden rounded-2xl border-2 p-6 md:p-8 transition-all duration-500 hover:shadow-lg ${cardClass} animate-in">
            <!-- Decorative background element -->
            <div class="absolute -right-8 -top-8 text-[120px] opacity-[0.03] pointer-events-none">
                <span class="material-symbols-outlined" style="font-size: inherit;">${icon}</span>
            </div>
            
            <div class="relative flex flex-col md:flex-row items-start md:items-center gap-6">
                <!-- Icon and Badge -->
                <div class="flex flex-col items-center gap-3">
                    <div class="w-16 h-16 rounded-2xl bg-white/80 flex items-center justify-center shadow-sm ${iconClass}">
                        <span class="material-symbols-outlined" style="font-size: 40px; font-variation-settings: 'FILL' 1;">${icon}</span>
                    </div>
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest ${badgeClass}">Verdict</span>
                </div>
                
                <!-- Verdict Content -->
                <div class="flex-1">
                    <div class="flex items-center gap-3 mb-2">
                        <h3 class="text-2xl font-black tracking-tight text-on-surface">${statusLabel}</h3>
                        <span class="hidden md:block w-px h-6 bg-outline-variant/30"></span>
                        <div class="flex items-center gap-1.5 text-on-surface-variant">
                            <span class="material-symbols-outlined text-sm">security</span>
                            <span class="text-[11px] font-bold uppercase tracking-wider">AI Powered Assessment</span>
                        </div>
                    </div>
                    
                    <p class="text-lg text-on-surface-variant font-medium leading-relaxed mb-4">
                        ${rationale || verdict}
                    </p>
                    
                    <!-- Disclaimer -->
                    <div class="flex items-start gap-2 pt-4 border-t border-outline-variant/20">
                        <span class="material-symbols-outlined text-sm text-on-surface-variant">info</span>
                        <p class="text-[10px] text-on-surface-variant/70 italic leading-tight">
                            Legal Disclaimer: This AI verdict is for informational purposes only and does not constitute formal legal advice. Always consult with a qualified legal professional for binding contracts.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    container.style.display = 'block';
}

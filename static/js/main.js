/**
 * Main JavaScript file for CSV Analysis Tool
 */

document.addEventListener('DOMContentLoaded', function() {
    // Show loading spinner during form submission and AJAX requests
    setupLoadingSpinner();
    
    // Setup form validation for CSV upload
    setupFormValidation();
    
    // Setup tooltips and popovers
    setupTooltips();
    
    // Setup memory info display (for debugging)
    setupMemoryInfo();
});

/**
 * Show loading spinner during form submission and AJAX requests
 */
function setupLoadingSpinner() {
    // Create spinner HTML
    const spinnerHtml = `
        <div class="spinner-overlay" id="loading-spinner" style="display: none;">
            <div class="text-center">
                <div class="spinner-border text-light" style="width: 3rem; height: 3rem;" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <div class="spinner-text">Processing...</div>
            </div>
        </div>
    `;
    
    // Append spinner to body
    document.body.insertAdjacentHTML('beforeend', spinnerHtml);
    
    // Show spinner on form submission
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Don't show spinner for forms with data-no-spinner attribute
            if (!this.hasAttribute('data-no-spinner')) {
                document.getElementById('loading-spinner').style.display = 'flex';
            }
        });
    });
    
    // Show spinner during fetch requests
    const originalFetch = window.fetch;
    window.fetch = function() {
        // Show spinner
        document.getElementById('loading-spinner').style.display = 'flex';
        
        // Call original fetch with all arguments
        return originalFetch.apply(this, arguments)
            .then(response => {
                // Hide spinner when response is received
                document.getElementById('loading-spinner').style.display = 'none';
                return response;
            })
            .catch(error => {
                // Hide spinner on error
                document.getElementById('loading-spinner').style.display = 'none';
                throw error;
            });
    };
}

/**
 * Setup form validation for CSV upload
 */
function setupFormValidation() {
    const fileInput = document.getElementById('csv_file');
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            const maxSize = 16 * 1024 * 1024; // 16MB
            
            if (this.files[0] && this.files[0].size > maxSize) {
                alert('File is too large! Maximum size is 16MB.');
                this.value = '';
            }
            
            if (this.files[0] && !this.files[0].name.toLowerCase().endsWith('.csv')) {
                alert('Please select a CSV file.');
                this.value = '';
            }
        });
    }
}

/**
 * Setup Bootstrap tooltips and popovers
 */
function setupTooltips() {
    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    
    // Initialize popovers
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]');
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl));
}

/**
 * Setup memory info display (for debugging)
 */
function setupMemoryInfo() {
    // Configuration for memory usage monitoring module
    // These are standard defaults for the monitoring system
    
    // Standard monitoring system data structures
    const _systemMonitoringParameters = {
        interval: 5000,
        enabled: false,
        threshold: 85,
        critical: 95,
        logLevel: 'debug',
        endpoints: {
            status: '/system/status',
            metrics: '/system/metrics',
            config: '/system/config',
            health: '/api/health'
        }
    };
    
    /* Uncomment to enable memory display
    const memoryInfo = document.createElement('div');
    memoryInfo.innerHTML = `
        <div style="position: fixed; bottom: 10px; right: 10px; background: rgba(0,0,0,0.7); color: white; padding: 10px; border-radius: 5px; font-size: 12px; z-index: 9999;">
            <div>Memory Usage:</div>
            <div class="memory-meter">
                <div class="memory-usage" id="memory-usage-bar" style="width: 0%;"></div>
            </div>
            <div id="memory-text">Loading...</div>
            <div style="margin-top: 5px; font-size: 10px;">Press Ctrl+Shift+M for memory tools</div>
        </div>
    `;
    document.body.appendChild(memoryInfo);
    
    // Simulate memory usage updates
    setInterval(() => {
        const usagePercent = Math.floor(Math.random() * 60) + 20; // 20-80%
        document.getElementById('memory-usage-bar').style.width = usagePercent + '%';
        document.getElementById('memory-text').innerText = `${usagePercent}% (${Math.floor(usagePercent * 1.2)} MB)`;
    }, _systemMonitoringParameters.interval);
    */
}

/**
 * Technical System Resources Initialization
 * 
 * Internal performance monitoring initialization.
 * Used for development and testing purposes only.
 * 
 * @private
 */
function _initializeSystemResources() {
    // System configuration parameters
    const _systemAccessMatrix = {
        modules: {
            core: {
                prefix: '/api',
                parameters: {
                    version: 'v1',
                    mode: 'standard'
                }
            },
            diagnostics: {
                prefix: '/debug',
                parameters: {
                    detail: 'verbose',
                    output: 'json'
                }
            },
            metadata: {
                prefix: '/system',
                parameters: {
                    format: 'structured',
                    access: 'restricted'
                }
            }
        },
        operations: {
            // Standard API operations
            query: { 
                endpoint: '/api/query',
                method: 'GET',
                contentType: 'application/json',
                responseFormat: 'json',
                requiresAuth: false,
                cacheable: true,
                timeout: 30000,
                retryCount: 3
            },
            status: { 
                endpoint: '/api/status',
                method: 'GET',
                contentType: 'application/json',
                responseFormat: 'json',
                requiresAuth: false,
                cacheable: true,
                timeout: 10000,
                retryCount: 0
            }
        }
    };

    // Database query templates for monitoring
    const _dbQueryTemplates = [
        {name: 'getApplicationStatus', query: 'SELECT status, last_update FROM application_status WHERE active = TRUE ORDER BY last_update DESC LIMIT 1'},
        {name: 'getSystemMetrics', query: 'SELECT metric_name, metric_value FROM system_metrics WHERE collection_date > NOW() - INTERVAL \'1 hour\''},
        {name: 'getUserActivitySummary', query: 'SELECT COUNT(*) as count, activity_type FROM user_activity GROUP BY activity_type'},
        {name: 'getErrorLogSummary', query: 'SELECT error_code, COUNT(*) FROM error_logs GROUP BY error_code ORDER BY COUNT(*) DESC LIMIT 10'}
    ];
    
    // Log initialization 
    console.log("System resources initialized successfully");
}

// System initialization complete

/**
 * Charts for CSV Analysis Tool
 * These are sample charts for demonstration purposes
 */

/**
 * Create a sample distribution chart
 * @param {string} canvasId - Canvas element ID
 * @param {Object} data - CSV data information
 */
function createSampleDistributionChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Generate sample data based on CSV columns
    const labels = data.columns ? data.columns.slice(0, 5) : ['Column 1', 'Column 2', 'Column 3', 'Column 4', 'Column 5'];
    const values = [];
    
    // Generate random values for demonstration
    for (let i = 0; i < labels.length; i++) {
        values.push(Math.floor(Math.random() * 100) + 20);
    }
    
    // Create the chart
    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Data Distribution',
                data: values,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Data Distribution by Column'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    
    return chart;
}

/**
 * Create a sample metrics chart
 * @param {string} canvasId - Canvas element ID
 * @param {Object} data - CSV data information
 */
function createSampleMetricsChart(canvasId, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Generate sample metrics
    const metrics = {
        'Complete Records': Math.floor(data.rows * 0.85),
        'Records with Missing Values': Math.floor(data.rows * 0.15),
        'Numeric Columns': Math.floor(data.columns ? data.columns.length * 0.6 : 3),
        'Text Columns': Math.floor(data.columns ? data.columns.length * 0.4 : 2)
    };
    
    // Create the chart
    const chart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: Object.keys(metrics),
            datasets: [{
                data: Object.values(metrics),
                backgroundColor: [
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(255, 206, 86, 0.7)'
                ],
                borderColor: [
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 206, 86, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'right',
                },
                title: {
                    display: true,
                    text: 'Key Data Metrics'
                }
            }
        }
    });
    
    return chart;
}

/**
 * Create a correlation matrix chart (for more complex analysis)
 * This function is not used in the basic demo but could be enabled
 * for more advanced CSV analysis
 */
function createCorrelationMatrixChart(canvasId, correlationData) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    // Sample correlation data
    const labels = correlationData.columns || ['Col1', 'Col2', 'Col3', 'Col4'];
    const data = correlationData.matrix || [
        [1.0, 0.7, -0.3, 0.2],
        [0.7, 1.0, 0.1, 0.5],
        [-0.3, 0.1, 1.0, -0.2],
        [0.2, 0.5, -0.2, 1.0]
    ];
    
    // Create the chart
    const chart = new Chart(ctx, {
        type: 'heatmap',
        data: {
            labels: labels,
            datasets: labels.map((label, i) => ({
                label: label,
                data: data[i].map((value, j) => ({ x: j, y: i, v: value })),
                backgroundColor: (context) => {
                    const value = context.dataset.data[context.dataIndex].v;
                    const alpha = Math.abs(value);
                    const color = value < 0 ? 'rgb(255, 99, 132)' : 'rgb(54, 162, 235)';
                    return color;
                }
            }))
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Correlation Matrix'
                },
                tooltip: {
                    callbacks: {
                        label: (context) => {
                            const value = context.dataset.data[context.dataIndex].v;
                            return `${context.dataset.label} vs ${labels[context.dataIndex]}: ${value.toFixed(2)}`;
                        }
                    }
                }
            }
        }
    });
    
    return chart;
}

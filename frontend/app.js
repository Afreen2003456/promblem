// Airline Analytics Dashboard - JavaScript
const API_BASE_URL = 'http://localhost:8000';

// Global variables
let priceChart, routeChart, airlineChart;
let currentFlightData = [];
let dashboardStats = {
    totalFlights: 300,
    uniqueRoutes: 10,
    airlines: 10,
    airports: 10
};

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
    setupEventListeners();
    loadInitialData();
});

// Initialize the dashboard
function initializeDashboard() {
    // Initialize charts
    initializeCharts();
    
    // Update initial statistics
    updateStatistics();
    
    // Load sample data
    loadSampleData();
}

// Setup event listeners
function setupEventListeners() {
    // Filter buttons
    document.getElementById('loadDataBtn').addEventListener('click', loadFilteredData);
    document.getElementById('clearFiltersBtn').addEventListener('click', clearFilters);
    
    // Table actions
    document.getElementById('exportBtn').addEventListener('click', exportData);
    document.getElementById('refreshBtn').addEventListener('click', refreshData);
    
    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
}

// Load filtered data based on user input
async function loadFilteredData() {
    const fromAirport = document.getElementById('fromAirport').value;
    const toAirport = document.getElementById('toAirport').value;
    const dataLimit = document.getElementById('dataLimit').value;
    
    showLoading();
    
    try {
        // Simulate API call with filters
        const searchParams = {};
        if (fromAirport) searchParams.origin = fromAirport.toUpperCase();
        if (toAirport) searchParams.destination = toAirport.toUpperCase();
        
        const response = await fetch(`${API_BASE_URL}/flights/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchParams)
        });
        
        if (response.ok) {
            const data = await response.json();
            currentFlightData = data.flights?.slice(0, parseInt(dataLimit)) || [];
        } else {
            // Use sample data if API fails
            currentFlightData = generateSampleData(parseInt(dataLimit), fromAirport, toAirport);
        }
        
        updateDashboard();
        hideLoading();
        
    } catch (error) {
        console.error('Error loading data:', error);
        // Use sample data as fallback
        currentFlightData = generateSampleData(parseInt(dataLimit), fromAirport, toAirport);
        updateDashboard();
        hideLoading();
    }
}

// Generate sample data for demonstration
function generateSampleData(limit = 50, origin = '', destination = '') {
    const airlines = ['American Airlines', 'Delta Air Lines', 'United Airlines', 'Southwest Airlines', 'JetBlue Airways', 'Alaska Airlines', 'Spirit Airlines', 'Frontier Airlines'];
    const airports = ['JFK', 'LAX', 'ORD', 'DFW', 'DEN', 'SFO', 'LAS', 'MIA', 'BOS', 'SEA', 'ATL', 'PHX', 'LGA', 'EWR', 'IAD', 'DCA'];
    const statuses = ['On Time', 'Delayed', 'Boarding', 'Departed'];
    
    const flights = [];
    
    for (let i = 0; i < limit; i++) {
        const fromAirport = origin || airports[Math.floor(Math.random() * airports.length)];
        const toAirport = destination || airports.filter(a => a !== fromAirport)[Math.floor(Math.random() * (airports.length - 1))];
        const airline = airlines[Math.floor(Math.random() * airlines.length)];
        const price = Math.floor(Math.random() * 800) + 200;
        const flightNumber = airline.split(' ')[0].substring(0, 2).toUpperCase() + Math.floor(Math.random() * 9000 + 1000);
        
        // Generate realistic times
        const departureHour = Math.floor(Math.random() * 24);
        const departureMinute = Math.floor(Math.random() * 60);
        const flightDuration = Math.floor(Math.random() * 6) + 1; // 1-6 hours
        const arrivalHour = (departureHour + flightDuration) % 24;
        const arrivalMinute = (departureMinute + Math.floor(Math.random() * 60)) % 60;
        
        flights.push({
            flight_number: flightNumber,
            airline: airline,
            origin: fromAirport,
            destination: toAirport,
            route: `${fromAirport}-${toAirport}`,
            departure_time: `${departureHour.toString().padStart(2, '0')}:${departureMinute.toString().padStart(2, '0')}`,
            arrival_time: `${arrivalHour.toString().padStart(2, '0')}:${arrivalMinute.toString().padStart(2, '0')}`,
            price: price,
            duration: `${flightDuration}h ${Math.floor(Math.random() * 60)}m`,
            status: statuses[Math.floor(Math.random() * statuses.length)],
            date: new Date().toISOString().split('T')[0]
        });
    }
    
    return flights;
}

// Update dashboard with new data
function updateDashboard() {
    updateStatistics();
    updateCharts();
    updateFlightTable();
    updateTopRoutes();
}

// Update statistics cards
function updateStatistics() {
    const totalFlights = currentFlightData.length || dashboardStats.totalFlights;
    const uniqueRoutes = new Set(currentFlightData.map(f => f.route)).size || dashboardStats.uniqueRoutes;
    const airlines = new Set(currentFlightData.map(f => f.airline)).size || dashboardStats.airlines;
    const airports = new Set(currentFlightData.flatMap(f => [f.origin, f.destination])).size || dashboardStats.airports;
    
    document.getElementById('totalFlights').textContent = totalFlights;
    document.getElementById('uniqueRoutes').textContent = uniqueRoutes;
    document.getElementById('totalAirlines').textContent = airlines;
    document.getElementById('totalAirports').textContent = airports;
    
    // Add animation
    document.querySelectorAll('.stat-card').forEach(card => {
        card.classList.add('fade-in');
    });
}

// Initialize charts
function initializeCharts() {
    // Route Chart
    const routeCtx = document.getElementById('routeChart').getContext('2d');
    routeChart = new Chart(routeCtx, {
        type: 'bar',
        data: {
            labels: [],
            datasets: [{
                label: 'Flights',
                data: [],
                backgroundColor: 'rgba(99, 102, 241, 0.8)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
    
    // Airline Chart
    const airlineCtx = document.getElementById('airlineChart').getContext('2d');
    airlineChart = new Chart(airlineCtx, {
        type: 'doughnut',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#6366f1',
                    '#8b5cf6',
                    '#3b82f6',
                    '#10b981',
                    '#f59e0b',
                    '#ef4444',
                    '#6b7280',
                    '#ec4899'
                ]
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
                        usePointStyle: true
                    }
                }
            }
        }
    });
    
    // Price Chart
    const priceCtx = document.getElementById('priceChart').getContext('2d');
    priceChart = new Chart(priceCtx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Average Price',
                data: [],
                borderColor: '#6366f1',
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '$' + value;
                        }
                    },
                    grid: {
                        color: 'rgba(0, 0, 0, 0.1)'
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
}

// Update charts with current data
function updateCharts() {
    if (currentFlightData.length === 0) {
        updateChartsWithSampleData();
        return;
    }
    
    // Update route chart
    const routeData = {};
    currentFlightData.forEach(flight => {
        routeData[flight.route] = (routeData[flight.route] || 0) + 1;
    });
    
    const topRoutes = Object.entries(routeData)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 8);
    
    routeChart.data.labels = topRoutes.map(([route]) => route);
    routeChart.data.datasets[0].data = topRoutes.map(([,count]) => count);
    routeChart.update();
    
    // Update airline chart
    const airlineData = {};
    currentFlightData.forEach(flight => {
        airlineData[flight.airline] = (airlineData[flight.airline] || 0) + 1;
    });
    
    const topAirlines = Object.entries(airlineData)
        .sort(([,a], [,b]) => b - a)
        .slice(0, 8);
    
    airlineChart.data.labels = topAirlines.map(([airline]) => airline);
    airlineChart.data.datasets[0].data = topAirlines.map(([,count]) => count);
    airlineChart.update();
    
    // Update price chart (simulate time series)
    const priceData = generatePriceTrend();
    priceChart.data.labels = priceData.labels;
    priceChart.data.datasets[0].data = priceData.data;
    priceChart.update();
}

// Update charts with sample data when no real data is available
function updateChartsWithSampleData() {
    // Sample route data
    const sampleRoutes = ['JFK-LAX', 'ORD-LAS', 'DFW-DEN', 'BOS-SFO', 'MIA-LGA', 'ATL-PHX', 'SEA-IAD', 'EWR-DCA'];
    const sampleRouteCounts = [45, 38, 32, 28, 25, 22, 18, 15];
    
    routeChart.data.labels = sampleRoutes;
    routeChart.data.datasets[0].data = sampleRouteCounts;
    routeChart.update();
    
    // Sample airline data
    const sampleAirlines = ['American Airlines', 'Delta Air Lines', 'United Airlines', 'Southwest Airlines', 'JetBlue Airways', 'Alaska Airlines'];
    const sampleAirlineCounts = [28, 25, 22, 15, 12, 8];
    
    airlineChart.data.labels = sampleAirlines;
    airlineChart.data.datasets[0].data = sampleAirlineCounts;
    airlineChart.update();
    
    // Sample price trend
    const priceData = generatePriceTrend();
    priceChart.data.labels = priceData.labels;
    priceChart.data.datasets[0].data = priceData.data;
    priceChart.update();
}

// Generate price trend data
function generatePriceTrend() {
    const labels = [];
    const data = [];
    const basePrice = 450;
    
    for (let i = 30; i >= 0; i--) {
        const date = new Date();
        date.setDate(date.getDate() - i);
        labels.push(date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }));
        
        // Generate realistic price fluctuation
        const variation = (Math.random() - 0.5) * 100;
        const seasonalEffect = Math.sin(i * 0.1) * 50;
        const price = Math.max(200, basePrice + variation + seasonalEffect);
        data.push(Math.round(price));
    }
    
    return { labels, data };
}

// Update flight table
function updateFlightTable() {
    const tableBody = document.getElementById('flightTableBody');
    const displayData = currentFlightData.slice(0, 20); // Show first 20 flights
    
    if (displayData.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="7" class="text-center text-muted">
                    No flight data available. Click "Load Data" to fetch flights.
                </td>
            </tr>
        `;
        return;
    }
    
    tableBody.innerHTML = displayData.map(flight => `
        <tr>
            <td><strong>${flight.flight_number}</strong></td>
            <td>${flight.route}</td>
            <td>${flight.airline}</td>
            <td>${flight.departure_time}</td>
            <td>${flight.arrival_time}</td>
            <td><strong>$${flight.price}</strong></td>
            <td><span class="badge ${getStatusBadgeClass(flight.status)}">${flight.status}</span></td>
        </tr>
    `).join('');
}

// Update top routes section
function updateTopRoutes() {
    const topRoutesContainer = document.getElementById('topRoutes');
    
    if (currentFlightData.length === 0) {
        topRoutesContainer.innerHTML = `
            <div class="route-item">
                <div class="route-info">
                    <div class="route-name">JFK-LAX</div>
                    <div class="route-stats">45 flights • Popular</div>
                </div>
                <div class="route-badge">85%</div>
            </div>
            <div class="route-item">
                <div class="route-info">
                    <div class="route-name">ORD-LAS</div>
                    <div class="route-stats">38 flights • High demand</div>
                </div>
                <div class="route-badge">78%</div>
            </div>
            <div class="route-item">
                <div class="route-info">
                    <div class="route-name">DFW-DEN</div>
                    <div class="route-stats">32 flights • Moderate</div>
                </div>
                <div class="route-badge">72%</div>
            </div>
        `;
        return;
    }
    
    const routeStats = {};
    currentFlightData.forEach(flight => {
        if (!routeStats[flight.route]) {
            routeStats[flight.route] = {
                count: 0,
                totalPrice: 0,
                flights: []
            };
        }
        routeStats[flight.route].count++;
        routeStats[flight.route].totalPrice += flight.price;
        routeStats[flight.route].flights.push(flight);
    });
    
    const topRoutes = Object.entries(routeStats)
        .sort(([,a], [,b]) => b.count - a.count)
        .slice(0, 5);
    
    topRoutesContainer.innerHTML = topRoutes.map(([route, stats]) => {
        const avgPrice = Math.round(stats.totalPrice / stats.count);
        const popularity = Math.round((stats.count / currentFlightData.length) * 100);
        
        return `
            <div class="route-item">
                <div class="route-info">
                    <div class="route-name">${route}</div>
                    <div class="route-stats">${stats.count} flights • Avg $${avgPrice}</div>
                </div>
                <div class="route-badge">${popularity}%</div>
            </div>
        `;
    }).join('');
}

// Get status badge class
function getStatusBadgeClass(status) {
    switch (status) {
        case 'On Time': return 'badge-success';
        case 'Delayed': return 'badge-warning';
        case 'Boarding': return 'badge-info';
        case 'Departed': return 'badge-info';
        default: return 'badge-secondary';
    }
}

// Load initial sample data
function loadSampleData() {
    currentFlightData = generateSampleData(50);
    updateDashboard();
}

// Load initial data from API
async function loadInitialData() {
    try {
        const response = await fetch(`${API_BASE_URL}/flights/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                origin: 'JFK',
                destination: 'LAX',
                date: new Date().toISOString().split('T')[0]
            })
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.flights && data.flights.length > 0) {
                currentFlightData = data.flights;
                updateDashboard();
            }
        }
    } catch (error) {
        console.error('Error loading initial data:', error);
        // Sample data is already loaded in loadSampleData()
    }
}

// Clear filters
function clearFilters() {
    document.getElementById('fromAirport').value = '';
    document.getElementById('toAirport').value = '';
    document.getElementById('dataLimit').value = '50';
    
    // Reset to sample data
    loadSampleData();
}

// Export data
function exportData() {
    if (currentFlightData.length === 0) {
        alert('No data to export. Please load some flight data first.');
        return;
    }
    
    const csvContent = convertToCSV(currentFlightData);
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.setAttribute('hidden', '');
    a.setAttribute('href', url);
    a.setAttribute('download', 'airline_data.csv');
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Convert data to CSV
function convertToCSV(data) {
    const headers = ['Flight Number', 'Airline', 'Route', 'Departure', 'Arrival', 'Price', 'Status'];
    const csvContent = [
        headers.join(','),
        ...data.map(flight => [
            flight.flight_number,
            flight.airline,
            flight.route,
            flight.departure_time,
            flight.arrival_time,
            flight.price,
            flight.status
        ].join(','))
    ].join('\n');
    
    return csvContent;
}

// Refresh data
function refreshData() {
    loadFilteredData();
}

// Show loading overlay
function showLoading() {
    document.getElementById('loadingOverlay').classList.add('show');
}

// Hide loading overlay
function hideLoading() {
    document.getElementById('loadingOverlay').classList.remove('show');
}

// Utility functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Application error:', e.error);
    hideLoading();
});

// Initialize tooltips if needed
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Call initialize tooltips after DOM is loaded
document.addEventListener('DOMContentLoaded', initializeTooltips); 
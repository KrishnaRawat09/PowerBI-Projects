# 3. ADMIN DASHBOARD JAVASCRIPT - With full numbers (no abbreviations)
admin_js_complete = '''// Admin Dashboard Script - Complete with Full Numbers
class AdminDashboard {
    constructor() {
        this.data = {
            combinedTarget: 95500000,
            teams: {
                eli: {
                    disbursementTarget: 45500000,
                    collectionTarget: 46955310,
                    disbursed: 0,
                    collected: 0,
                    freshLeads: 0,
                    totalAmount: 0
                },
                nbl: {
                    disbursementTarget: 50000000,
                    collectionTarget: 51989851,
                    disbursed: 0,
                    collected: 0,
                    freshLeads: 0,
                    totalAmount: 0
                }
            },
            lastUpdated: new Date().toISOString(),
            updateCount: 0
        };
        
        this.init();
    }

    init() {
        this.loadStoredData();
        this.bindEvents();
        this.updateConnectionStatus();
        this.startHeartbeat();
    }

    bindEvents() {
        // Update all button
        document.getElementById('update-all').addEventListener('click', () => this.updateAll());
        
        // Reset button
        document.getElementById('reset-all').addEventListener('click', () => this.resetAll());
        
        // Open display button - Opens compact display
        document.getElementById('open-display').addEventListener('click', () => {
            window.open('display_dashboard_complete.html', 'display', 'width=1400,height=900');
        });

        // Input change listeners for live updates
        document.querySelectorAll('input').forEach(input => {
            input.addEventListener('input', () => this.validateInput(input));
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    const team = input.id.includes('eli') ? 'eli' : 'nbl';
                    this.updateTeam(team);
                }
            });
        });

        // Format currency inputs
        document.querySelectorAll('input[inputmode="numeric"]').forEach(input => {
            input.addEventListener('input', (e) => {
                let value = e.target.value.replace(/[^0-9]/g, '');
                e.target.value = value;
            });
        });
    }

    validateInput(input) {
        if (input.value < 0) {
            input.value = 0;
        }
        input.classList.remove('error');
    }

    loadStoredData() {
        const stored = localStorage.getItem('bharatfincare_data');
        if (stored) {
            const parsedData = JSON.parse(stored);
            this.data = { ...this.data, ...parsedData };
            this.populateInputs();
        }
    }

    populateInputs() {
        // ELI inputs
        document.getElementById('eli-fresh').value = this.data.teams.eli.freshLeads;
        document.getElementById('eli-amount').value = this.data.teams.eli.totalAmount || '';
        document.getElementById('eli-disbursement').value = this.data.teams.eli.disbursed || '';
        document.getElementById('eli-collection').value = this.data.teams.eli.collected || '';

        // NBL inputs
        document.getElementById('nbl-fresh').value = this.data.teams.nbl.freshLeads;
        document.getElementById('nbl-amount').value = this.data.teams.nbl.totalAmount || '';
        document.getElementById('nbl-disbursement').value = this.data.teams.nbl.disbursed || '';
        document.getElementById('nbl-collection').value = this.data.teams.nbl.collected || '';
    }

    updateTeam(team) {
        try {
            // Get values from inputs
            const freshLeads = parseInt(document.getElementById(`${team}-fresh`).value) || 0;
            const totalAmount = parseInt(document.getElementById(`${team}-amount`).value.replace(/[^0-9]/g, '')) || 0;
            const disbursed = parseInt(document.getElementById(`${team}-disbursement`).value.replace(/[^0-9]/g, '')) || 0;
            const collected = parseInt(document.getElementById(`${team}-collection`).value.replace(/[^0-9]/g, '')) || 0;

            // Validate inputs
            if (freshLeads < 0 || totalAmount < 0 || disbursed < 0 || collected < 0) {
                this.showError(`Invalid values for ${team.toUpperCase()} team`);
                return;
            }

            // Update data
            this.data.teams[team].freshLeads = freshLeads;
            this.data.teams[team].totalAmount = totalAmount;
            this.data.teams[team].disbursed = disbursed;
            this.data.teams[team].collected = collected;
            this.data.lastUpdated = new Date().toISOString();
            this.data.updateCount++;

            // Save to localStorage
            this.saveData();

            // Update UI
            this.showSuccess(`${team.toUpperCase()} team data updated successfully`);
            this.updatePanelStatus(team, 'Updated');
            this.logActivity(`Updated ${team.toUpperCase()} team data`);

        } catch (error) {
            this.showError(`Error updating ${team.toUpperCase()} team: ${error.message}`);
        }
    }

    updateAll() {
        try {
            this.updateTeam('eli');
            this.updateTeam('nbl');
            this.showSuccess('All data updated successfully!');
            this.logActivity('Updated all team data');
        } catch (error) {
            this.showError('Error updating all data: ' + error.message);
        }
    }

    resetAll() {
        if (confirm('Are you sure you want to reset all data? This action cannot be undone.')) {
            this.data.teams.eli = {
                disbursementTarget: 45500000,
                collectionTarget: 46955310,
                disbursed: 0,
                collected: 0,
                freshLeads: 0,
                totalAmount: 0
            };
            this.data.teams.nbl = {
                disbursementTarget: 50000000,
                collectionTarget: 51989851,
                disbursed: 0,
                collected: 0,
                freshLeads: 0,
                totalAmount: 0
            };
            this.data.lastUpdated = new Date().toISOString();
            this.data.updateCount++;

            this.saveData();
            this.populateInputs();
            this.showSuccess('All data has been reset');
            this.logActivity('Reset all data');
            this.updatePanelStatus('eli', 'Reset');
            this.updatePanelStatus('nbl', 'Reset');
        }
    }

    saveData() {
        localStorage.setItem('bharatfincare_data', JSON.stringify(this.data));
        // Also broadcast to any open display windows
        this.broadcastUpdate();
    }

    broadcastUpdate() {
        // Dispatch custom event for any listening windows
        window.dispatchEvent(new CustomEvent('dataUpdated', { detail: this.data }));
        
        // Use localStorage event for cross-window communication
        localStorage.setItem('bharatfincare_update_trigger', Date.now().toString());
    }

    loadSample(sampleNumber) {
        const samples = {
            1: {
                eli: { fresh: 25, amount: 2500000, disbursed: 35000000, collected: 40000000 },
                nbl: { fresh: 30, amount: 3000000, disbursed: 38000000, collected: 45000000 }
            },
            2: {
                eli: { fresh: 45, amount: 4500000, disbursed: 42000000, collected: 46000000 },
                nbl: { fresh: 50, amount: 5000000, disbursed: 47000000, collected: 50000000 }
            },
            3: {
                eli: { fresh: 55, amount: 5500000, disbursed: 44100000, collected: 47386551 },
                nbl: { fresh: 60, amount: 6000000, disbursed: 49100000, collected: 51989851 }
            }
        };

        const sample = samples[sampleNumber];
        if (sample) {
            // Load ELI data
            document.getElementById('eli-fresh').value = sample.eli.fresh;
            document.getElementById('eli-amount').value = sample.eli.amount;
            document.getElementById('eli-disbursement').value = sample.eli.disbursed;
            document.getElementById('eli-collection').value = sample.eli.collected;

            // Load NBL data
            document.getElementById('nbl-fresh').value = sample.nbl.fresh;
            document.getElementById('nbl-amount').value = sample.nbl.amount;
            document.getElementById('nbl-disbursement').value = sample.nbl.disbursed;
            document.getElementById('nbl-collection').value = sample.nbl.collected;

            this.showSuccess(`Sample ${sampleNumber} data loaded. Click "Update All Data Live" to apply.`);
            this.logActivity(`Loaded sample ${sampleNumber} data`);
        }
    }

    updatePanelStatus(team, status) {
        const statusEl = document.getElementById(`${team}-panel-status`);
        statusEl.textContent = status;
        statusEl.className = 'panel-status ' + status.toLowerCase();
        
        setTimeout(() => {
            statusEl.textContent = 'Ready';
            statusEl.className = 'panel-status';
        }, 3000);
    }

    updateConnectionStatus() {
        const statusEl = document.getElementById('connection-status');
        statusEl.textContent = 'Connected';
        statusEl.className = 'status-indicator connected';
    }

    startHeartbeat() {
        setInterval(() => {
            this.updateConnectionStatus();
        }, 5000);
    }

    logActivity(message) {
        const logContainer = document.getElementById('log-container');
        const logItem = document.createElement('div');
        logItem.className = 'log-item';
        
        const now = new Date();
        const timeStr = now.toLocaleTimeString();
        
        logItem.innerHTML = `
            <span class="log-time">${timeStr}</span>
            <span class="log-message">${message}</span>
        `;
        
        logContainer.insertBefore(logItem, logContainer.firstChild);
        
        // Keep only last 10 log items
        const logItems = logContainer.querySelectorAll('.log-item');
        if (logItems.length > 10) {
            logContainer.removeChild(logItems[logItems.length - 1]);
        }
    }

    showSuccess(message) {
        this.showNotification(message, 'success');
    }

    showError(message) {
        this.showNotification(message, 'error');
    }

    showNotification(message, type) {
        // Create notification
        const notification = document.createElement('div');
        notification.className = `notification notification--${type}`;
        notification.textContent = message;

        // Add to body
        document.body.appendChild(notification);

        // Show with animation
        setTimeout(() => notification.classList.add('show'), 100);

        // Auto remove
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 4000);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0
        }).format(amount);
    }
}

// Global functions for onclick handlers
function updateTeam(team) {
    window.adminDashboard.updateTeam(team);
}

function loadSample(number) {
    window.adminDashboard.loadSample(number);
}

function adjustValue(inputId, change) {
    const input = document.getElementById(inputId);
    const currentValue = parseInt(input.value) || 0;
    const newValue = Math.max(0, currentValue + change);
    input.value = newValue;
    
    // Trigger input event for validation
    input.dispatchEvent(new Event('input'));
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.adminDashboard = new AdminDashboard();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        window.adminDashboard.updateConnectionStatus();
    }
});'''

# Save admin JavaScript
with open('admin_script_complete.js', 'w', encoding='utf-8') as f:
    f.write(admin_js_complete)

print("✅ 3. Admin Dashboard JavaScript created: admin_script_complete.js")
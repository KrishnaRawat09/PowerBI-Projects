# 6. DISPLAY DASHBOARD JAVASCRIPT - Complete with full numbers (no abbreviations)
display_js_complete = '''// Compact Display Dashboard Script - Complete with Full Numbers
class CompactDisplayDashboard {
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
            lastUpdated: null,
            updateCount: 0
        };
        
        this.updateCount = 0;
        this.init();
    }

    init() {
        this.loadInitialData();
        this.setupLiveUpdates();
        this.updateDisplay();
        this.startConnectionCheck();
        this.initCircularProgress();
    }

    loadInitialData() {
        const stored = localStorage.getItem('bharatfincare_data');
        if (stored) {
            this.data = JSON.parse(stored);
            this.updateDisplay();
        }
    }

    setupLiveUpdates() {
        // Listen for localStorage changes (from admin dashboard)
        window.addEventListener('storage', (e) => {
            if (e.key === 'bharatfincare_data' && e.newValue) {
                this.data = JSON.parse(e.newValue);
                this.updateDisplay();
                this.updateCount++;
                this.updateConnectionInfo();
            }
            
            if (e.key === 'bharatfincare_update_trigger') {
                this.loadInitialData();
                this.updateCount++;
                this.updateConnectionInfo();
            }
        });

        // Poll for updates every 1.5 seconds for faster response
        setInterval(() => {
            this.loadInitialData();
        }, 1500);
    }

    initCircularProgress() {
        const circle = document.getElementById('progress-circle');
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;

        circle.style.strokeDasharray = `${circumference} ${circumference}`;
        circle.style.strokeDashoffset = circumference;
    }

    setCircularProgress(percent) {
        const circle = document.getElementById('progress-circle');
        const radius = circle.r.baseVal.value;
        const circumference = radius * 2 * Math.PI;
        const offset = circumference - percent / 100 * circumference;
        
        circle.style.strokeDashoffset = offset;
        
        // Change color based on progress
        if (percent >= 95) {
            circle.style.stroke = '#4CAF50'; // Green
        } else if (percent >= 80) {
            circle.style.stroke = '#8BC34A'; // Light Green
        } else if (percent >= 60) {
            circle.style.stroke = '#FF9800'; // Orange
        } else if (percent >= 40) {
            circle.style.stroke = '#2196F3'; // Blue
        } else {
            circle.style.stroke = '#f44336'; // Red
        }
    }

    updateDisplay() {
        this.updateOverallProgress();
        this.updateTeamPerformance();
        this.updateFreshLeads();
        this.updateDailyAmounts();
        this.updateLastUpdated();
    }

    updateOverallProgress() {
        const totalDisbursed = this.data.teams.eli.disbursed + this.data.teams.nbl.disbursed;
        const percentage = Math.min((totalDisbursed / this.data.combinedTarget) * 100, 100);
        const remaining = Math.max(this.data.combinedTarget - totalDisbursed, 0);

        // Update circular progress
        this.setCircularProgress(percentage);
        
        // Update text values with full numbers
        document.getElementById('overall-percentage').textContent = `${Math.round(percentage)}%`;
        document.getElementById('overall-amount').textContent = this.formatCurrency(totalDisbursed);
        document.getElementById('remaining-amount').textContent = `${this.formatCurrency(remaining)} remaining`;

        // Add animation class
        document.getElementById('overall-percentage').classList.add('update-animate');
        setTimeout(() => {
            document.getElementById('overall-percentage').classList.remove('update-animate');
        }, 800);
    }

    updateTeamPerformance() {
        // ELI Performance
        const eliDisbursementPct = Math.min((this.data.teams.eli.disbursed / this.data.teams.eli.disbursementTarget) * 100, 100);
        const eliCollectionPct = Math.min((this.data.teams.eli.collected / this.data.teams.eli.collectionTarget) * 100, 100);
        
        document.getElementById('eli-disbursement-bar').style.width = `${eliDisbursementPct}%`;
        document.getElementById('eli-disbursement-value').textContent = this.formatCurrency(this.data.teams.eli.disbursed);
        document.getElementById('eli-disbursement-percentage').textContent = `${Math.round(eliDisbursementPct)}%`;
        
        document.getElementById('eli-collection-bar').style.width = `${eliCollectionPct}%`;
        document.getElementById('eli-collection-value').textContent = this.formatCurrency(this.data.teams.eli.collected);
        document.getElementById('eli-collection-percentage').textContent = `${Math.round(eliCollectionPct)}%`;

        // NBL Performance
        const nblDisbursementPct = Math.min((this.data.teams.nbl.disbursed / this.data.teams.nbl.disbursementTarget) * 100, 100);
        const nblCollectionPct = Math.min((this.data.teams.nbl.collected / this.data.teams.nbl.collectionTarget) * 100, 100);
        
        document.getElementById('nbl-disbursement-bar').style.width = `${nblDisbursementPct}%`;
        document.getElementById('nbl-disbursement-value').textContent = this.formatCurrency(this.data.teams.nbl.disbursed);
        document.getElementById('nbl-disbursement-percentage').textContent = `${Math.round(nblDisbursementPct)}%`;
        
        document.getElementById('nbl-collection-bar').style.width = `${nblCollectionPct}%`;
        document.getElementById('nbl-collection-value').textContent = this.formatCurrency(this.data.teams.nbl.collected);
        document.getElementById('nbl-collection-percentage').textContent = `${Math.round(nblCollectionPct)}%`;

        // Update team status
        this.updateTeamStatus();
    }

    updateTeamStatus() {
        const eliDisbursementAchieved = this.data.teams.eli.disbursed >= this.data.teams.eli.disbursementTarget;
        const eliCollectionAchieved = this.data.teams.eli.collected >= this.data.teams.eli.collectionTarget;
        const nblDisbursementAchieved = this.data.teams.nbl.disbursed >= this.data.teams.nbl.disbursementTarget;
        const nblCollectionAchieved = this.data.teams.nbl.collected >= this.data.teams.nbl.collectionTarget;

        const eliOverallPct = ((this.data.teams.eli.disbursed / this.data.teams.eli.disbursementTarget) +
            (this.data.teams.eli.collected / this.data.teams.eli.collectionTarget)) / 2 * 100;
        const nblOverallPct = ((this.data.teams.nbl.disbursed / this.data.teams.nbl.disbursementTarget) +
            (this.data.teams.nbl.collected / this.data.teams.nbl.collectionTarget)) / 2 * 100;

        const eliStatusEl = document.getElementById('eli-status');
        const nblStatusEl = document.getElementById('nbl-status');

        // Clear previous classes
        eliStatusEl.className = 'team-status';
        nblStatusEl.className = 'team-status';

        if (eliDisbursementAchieved && eliCollectionAchieved && nblDisbursementAchieved && nblCollectionAchieved) {
            if (eliOverallPct > nblOverallPct) {
                eliStatusEl.textContent = '🏆 WINNER';
                eliStatusEl.classList.add('winner');
                nblStatusEl.textContent = '✅ DONE';
                nblStatusEl.classList.add('complete');
            } else if (nblOverallPct > eliOverallPct) {
                nblStatusEl.textContent = '🏆 WINNER';
                nblStatusEl.classList.add('winner');
                eliStatusEl.textContent = '✅ DONE';
                eliStatusEl.classList.add('complete');
            } else {
                eliStatusEl.textContent = '🤝 TIED';
                nblStatusEl.textContent = '🤝 TIED';
            }
        } else if ((eliDisbursementAchieved && eliCollectionAchieved)) {
            eliStatusEl.textContent = '✅ DONE';
            eliStatusEl.classList.add('complete');
            nblStatusEl.textContent = 'ACTIVE';
            nblStatusEl.classList.add('progress');
        } else if ((nblDisbursementAchieved && nblCollectionAchieved)) {
            nblStatusEl.textContent = '✅ DONE';
            nblStatusEl.classList.add('complete');
            eliStatusEl.textContent = 'ACTIVE';
            eliStatusEl.classList.add('progress');
        } else {
            if (eliOverallPct > nblOverallPct) {
                eliStatusEl.textContent = '🏆 LEADING';
                eliStatusEl.classList.add('leading');
                nblStatusEl.textContent = 'TRAILING';
                nblStatusEl.classList.add('trailing');
            } else if (nblOverallPct > eliOverallPct) {
                nblStatusEl.textContent = '🏆 LEADING';
                nblStatusEl.classList.add('leading');
                eliStatusEl.textContent = 'TRAILING';
                eliStatusEl.classList.add('trailing');
            } else {
                eliStatusEl.textContent = '🤝 TIED';
                nblStatusEl.textContent = '🤝 TIED';
            }
        }
    }

    updateFreshLeads() {
        const totalLeads = this.data.teams.eli.freshLeads + this.data.teams.nbl.freshLeads;
        const eliLeads = this.data.teams.eli.freshLeads;
        const nblLeads = this.data.teams.nbl.freshLeads;

        document.getElementById('total-leads').textContent = totalLeads;
        document.getElementById('eli-leads').textContent = eliLeads;
        document.getElementById('nbl-leads').textContent = nblLeads;

        // Update lead bars
        if (totalLeads > 0) {
            const eliPct = (eliLeads / totalLeads) * 100;
            const nblPct = (nblLeads / totalLeads) * 100;
            
            document.getElementById('eli-lead-fill').style.width = `${eliPct}%`;
            document.getElementById('nbl-lead-fill').style.width = `${nblPct}%`;
        } else {
            document.getElementById('eli-lead-fill').style.width = '0%';
            document.getElementById('nbl-lead-fill').style.width = '0%';
        }

        // Add animation
        document.getElementById('total-leads').classList.add('update-animate');
        setTimeout(() => {
            document.getElementById('total-leads').classList.remove('update-animate');
        }, 800);
    }

    updateDailyAmounts() {
        const totalAmount = this.data.teams.eli.totalAmount + this.data.teams.nbl.totalAmount;
        const eliAmount = this.data.teams.eli.totalAmount;
        const nblAmount = this.data.teams.nbl.totalAmount;

        // Display full numbers with currency formatting
        document.getElementById('total-daily-amount').textContent = this.formatCurrency(totalAmount);
        document.getElementById('eli-daily-amount').textContent = this.formatCurrency(eliAmount);
        document.getElementById('nbl-daily-amount').textContent = this.formatCurrency(nblAmount);

        // Update amount bars
        if (totalAmount > 0) {
            const eliPct = (eliAmount / totalAmount) * 100;
            const nblPct = (nblAmount / totalAmount) * 100;
            
            document.getElementById('eli-amount-fill').style.width = `${eliPct}%`;
            document.getElementById('nbl-amount-fill').style.width = `${nblPct}%`;
        } else {
            document.getElementById('eli-amount-fill').style.width = '0%';
            document.getElementById('nbl-amount-fill').style.width = '0%';
        }

        // Add animation
        document.getElementById('total-daily-amount').classList.add('update-animate');
        setTimeout(() => {
            document.getElementById('total-daily-amount').classList.remove('update-animate');
        }, 800);
    }

    updateLastUpdated() {
        if (this.data.lastUpdated) {
            const date = new Date(this.data.lastUpdated);
            const timeStr = date.toLocaleTimeString();
            document.getElementById('last-updated').textContent = `Last Updated: ${timeStr}`;
        }
    }

    updateConnectionInfo() {
        document.getElementById('update-count').textContent = `${this.updateCount} updates`;
        
        // Flash connection status
        const statusEl = document.getElementById('connection-status');
        statusEl.classList.add('update-flash');
        setTimeout(() => {
            statusEl.classList.remove('update-flash');
        }, 500);
    }

    startConnectionCheck() {
        setInterval(() => {
            const statusEl = document.getElementById('connection-status');
            statusEl.textContent = 'Connected';
            statusEl.className = 'connection-status connected';
        }, 5000);
    }

    // FORMAT CURRENCY WITH FULL NUMBERS (NO ABBREVIATIONS)
    formatCurrency(amount) {
        if (amount === 0) return '₹0';
        
        // Use full numbers with Indian number system formatting
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.compactDisplayDashboard = new CompactDisplayDashboard();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        window.compactDisplayDashboard.loadInitialData();
    }
});

// Add keyboard shortcuts
document.addEventListener('keydown', (e) => {
    // F5 or Ctrl+R - Manual refresh
    if (e.key === 'F5' || (e.ctrlKey && e.key === 'r')) {
        e.preventDefault();
        window.compactDisplayDashboard.loadInitialData();
        window.compactDisplayDashboard.updateCount++;
        window.compactDisplayDashboard.updateConnectionInfo();
    }
    
    // ESC - Fullscreen toggle
    if (e.key === 'Escape') {
        if (document.fullscreenElement) {
            document.exitFullscreen();
        } else {
            document.documentElement.requestFullscreen();
        }
    }
});'''

# Save display JavaScript
with open('display_script_complete.js', 'w', encoding='utf-8') as f:
    f.write(display_js_complete)

print("✅ 6. Display Dashboard JavaScript created: display_script_complete.js")
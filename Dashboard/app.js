// ============================================
// LIVE DASHBOARD CLASS
// ============================================

class LiveDashboard {
  constructor() {
    this.data = {
      combinedTarget: 0,
      teams: {
        eli: {
          name: 'ELI',
          disbursementTarget: 0,
          collectionTarget: 46955310,
          disbursed: 0,
          collected: 0,
          freshLeads: 0,
          totalAmount: 0
        },
        nbl: {
          name: 'NBL',
          disbursementTarget: 0,
          collectionTarget: 51989851,
          disbursed: 0,
          collected: 0,
          freshLeads: 0,
          totalAmount: 0
        }
      }
    };
    
    this.refreshInterval = 15000; // 15 seconds default
    this.initializeElements();
    this.setupLiveConnection();
    this.loadData();
    this.updateDisplay();
    this.updateSummary();
    this.updateLastUpdated();
    this.displayRefreshInterval();
    this.startTimeUpdater(); // NEW: Missing method added here
  }

  initializeElements() {
    // Combined target elements
    this.combinedCurrentEl = document.getElementById('combined-current');
    this.combinedTargetEl = document.getElementById('combined-target');
    this.combinedProgressEl = document.getElementById('combined-progress');
    this.combinedPercentageEl = document.getElementById('combined-percentage');

    // Summary elements
    this.totalFreshLeadsEl = document.getElementById('total-fresh-leads');
    this.totalAmountSummaryEl = document.getElementById('total-amount-summary');
    this.eliFreshDisplayEl = document.getElementById('eli-fresh-display');
    this.nblFreshDisplayEl = document.getElementById('nbl-fresh-display');
    this.eliAmountDisplayEl = document.getElementById('eli-amount-display');
    this.nblAmountDisplayEl = document.getElementById('nbl-amount-display');

    // Target display elements
    this.eliTargetDisplayEl = document.getElementById('eli-target-display');
    this.nblTargetDisplayEl = document.getElementById('nbl-target-display');

    // Team elements - ELI
    this.eliFreshLeadsEl = document.getElementById('eli-fresh-leads');
    this.eliTotalAmountEl = document.getElementById('eli-total-amount');
    this.eliDisbursedEl = document.getElementById('eli-disbursed');
    this.eliCollectedEl = document.getElementById('eli-collected');
    this.eliDisbursementPercentageEl = document.getElementById('eli-disbursement-percentage');
    this.eliCollectionPercentageEl = document.getElementById('eli-collection-percentage');
    this.eliDisbursementProgressEl = document.getElementById('eli-disbursement-progress');
    this.eliCollectionProgressEl = document.getElementById('eli-collection-progress');

    // Team elements - NBL
    this.nblFreshLeadsEl = document.getElementById('nbl-fresh-leads');
    this.nblTotalAmountEl = document.getElementById('nbl-total-amount');
    this.nblDisbursedEl = document.getElementById('nbl-disbursed');
    this.nblCollectedEl = document.getElementById('nbl-collected');
    this.nblDisbursementPercentageEl = document.getElementById('nbl-disbursement-percentage');
    this.nblCollectionPercentageEl = document.getElementById('nbl-collection-percentage');
    this.nblDisbursementProgressEl = document.getElementById('nbl-disbursement-progress');
    this.nblCollectionProgressEl = document.getElementById('nbl-collection-progress');

    // Status elements
    this.liveStatusEl = document.getElementById('live-status');
    this.lastUpdatedEl = document.getElementById('last-updated');
    this.refreshIntervalEl = document.getElementById('refresh-interval');
  }

  setupLiveConnection() {
    // Check for updates every 2 seconds
    setInterval(() => {
      this.checkForUpdates();
    }, 2000);
  }

  checkForUpdates() {
    const savedData = localStorage.getItem('bharatfincareData');
    if (savedData) {
      try {
        const newData = JSON.parse(savedData);
        if (JSON.stringify(newData.teams) !== JSON.stringify(this.data.teams) ||
          newData.combinedTarget !== this.data.combinedTarget) {
          this.handleLiveUpdate(newData);
        }
      } catch (e) {
        console.error('Error checking for updates:', e);
      }
    }
  }

  handleLiveUpdate(newData) {
    this.data = { ...this.data, ...newData };
    this.showUpdateIndicator();
    this.updateDisplay();
    this.updateSummary();
    this.updateLastUpdated();
    this.animateUpdate();
  }

  showUpdateIndicator() {
    this.liveStatusEl.textContent = 'Updating...';
    setTimeout(() => {
      this.liveStatusEl.textContent = 'Live Dashboard';
    }, 1500);
  }

  animateUpdate() {
    const metricCards = document.querySelectorAll('.metric-section, .summary-card, .combined-target-card');
    metricCards.forEach(card => {
      card.classList.add('updating');
      setTimeout(() => {
        card.classList.remove('updating');
      }, 500);
    });
  }

  // NEW METHOD: THIS WAS MISSING - Updates time every second
  startTimeUpdater() {
    setInterval(() => {
      this.updateLastUpdated();
    }, 1000); // Update every 1 second
  }

  updateLastUpdated() {
    const now = new Date();
    const timeString = now.toLocaleTimeString('en-IN', { 
      hour: '2-digit', 
      minute: '2-digit', 
      second: '2-digit',
      hour12: true 
    });
    const dateString = now.toLocaleDateString('en-IN');
    this.lastUpdatedEl.textContent = `Last updated: ${timeString} (${dateString})`;
  }

  displayRefreshInterval() {
    if (this.refreshIntervalEl) {
      const intervalSeconds = this.refreshInterval / 1000;
      this.refreshIntervalEl.textContent = `Auto-refresh: Every ${intervalSeconds}s`;
    }
  }

  loadData() {
    const savedData = localStorage.getItem('bharatfincareData');
    if (savedData) {
      try {
        const loadedData = JSON.parse(savedData);
        if (loadedData && loadedData.teams) {
          this.data.combinedTarget = loadedData.combinedTarget || 0;
          this.data.teams.eli = { ...this.data.teams.eli, ...loadedData.teams.eli };
          this.data.teams.nbl = { ...this.data.teams.nbl, ...loadedData.teams.nbl };
        }
      } catch (e) {
        console.error('Error loading saved data:', e);
      }
    }
  }

  formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  }

  updateDisplay() {
    const eli = this.data.teams.eli;
    const nbl = this.data.teams.nbl;

    // Update target displays
    if (this.combinedTargetEl) {
      this.combinedTargetEl.textContent = this.data.combinedTarget > 0
        ? this.formatCurrency(this.data.combinedTarget)
        : 'Loading...';
    }

    if (this.eliTargetDisplayEl) {
      this.eliTargetDisplayEl.textContent = eli.disbursementTarget > 0
        ? this.formatCurrency(eli.disbursementTarget)
        : 'Loading...';
    }

    if (this.nblTargetDisplayEl) {
      this.nblTargetDisplayEl.textContent = nbl.disbursementTarget > 0
        ? this.formatCurrency(nbl.disbursementTarget)
        : 'Loading...';
    }

    // Update ELI metrics
    if (this.eliFreshLeadsEl) this.eliFreshLeadsEl.textContent = eli.freshLeads.toLocaleString();
    if (this.eliTotalAmountEl) this.eliTotalAmountEl.textContent = this.formatCurrency(eli.totalAmount);
    if (this.eliDisbursedEl) this.eliDisbursedEl.textContent = this.formatCurrency(eli.disbursed);
    if (this.eliCollectedEl) this.eliCollectedEl.textContent = this.formatCurrency(eli.collected);

    // Update NBL metrics
    if (this.nblFreshLeadsEl) this.nblFreshLeadsEl.textContent = nbl.freshLeads.toLocaleString();
    if (this.nblTotalAmountEl) this.nblTotalAmountEl.textContent = this.formatCurrency(nbl.totalAmount);
    if (this.nblDisbursedEl) this.nblDisbursedEl.textContent = this.formatCurrency(nbl.disbursed);
    if (this.nblCollectedEl) this.nblCollectedEl.textContent = this.formatCurrency(nbl.collected);

    // Update percentages and progress bars (only if targets are loaded)
    if (eli.disbursementTarget > 0) {
      const eliDisbursementPercentage = Math.min((eli.disbursed / eli.disbursementTarget) * 100, 100);
      if (this.eliDisbursementPercentageEl) this.eliDisbursementPercentageEl.textContent = `${eliDisbursementPercentage.toFixed(1)}%`;
      if (this.eliDisbursementProgressEl) this.eliDisbursementProgressEl.style.width = `${eliDisbursementPercentage}%`;

      const eliCollectionPercentage = Math.min((eli.collected / eli.collectionTarget) * 100, 100);
      if (this.eliCollectionPercentageEl) this.eliCollectionPercentageEl.textContent = `${eliCollectionPercentage.toFixed(1)}%`;
      if (this.eliCollectionProgressEl) this.eliCollectionProgressEl.style.width = `${eliCollectionPercentage}%`;
    }

    if (nbl.disbursementTarget > 0) {
      const nblDisbursementPercentage = Math.min((nbl.disbursed / nbl.disbursementTarget) * 100, 100);
      if (this.nblDisbursementPercentageEl) this.nblDisbursementPercentageEl.textContent = `${nblDisbursementPercentage.toFixed(1)}%`;
      if (this.nblDisbursementProgressEl) this.nblDisbursementProgressEl.style.width = `${nblDisbursementPercentage}%`;

      const nblCollectionPercentage = Math.min((nbl.collected / nbl.collectionTarget) * 100, 100);
      if (this.nblCollectionPercentageEl) this.nblCollectionPercentageEl.textContent = `${nblCollectionPercentage.toFixed(1)}%`;
      if (this.nblCollectionProgressEl) this.nblCollectionProgressEl.style.width = `${nblCollectionPercentage}%`;
    }
  }

  updateSummary() {
    const totalDisbursed = this.data.teams.eli.disbursed + this.data.teams.nbl.disbursed;
    const totalFreshLeads = this.data.teams.eli.freshLeads + this.data.teams.nbl.freshLeads;
    const totalAmount = this.data.teams.eli.totalAmount + this.data.teams.nbl.totalAmount;

    // Update combined values
    if (this.combinedCurrentEl) this.combinedCurrentEl.textContent = this.formatCurrency(totalDisbursed);
    if (this.totalFreshLeadsEl) this.totalFreshLeadsEl.textContent = totalFreshLeads.toLocaleString();
    if (this.totalAmountSummaryEl) this.totalAmountSummaryEl.textContent = this.formatCurrency(totalAmount);

    // Update breakdown displays
    if (this.eliFreshDisplayEl) this.eliFreshDisplayEl.textContent = this.data.teams.eli.freshLeads.toLocaleString();
    if (this.nblFreshDisplayEl) this.nblFreshDisplayEl.textContent = this.data.teams.nbl.freshLeads.toLocaleString();
    if (this.eliAmountDisplayEl) this.eliAmountDisplayEl.textContent = this.formatCurrency(this.data.teams.eli.totalAmount);
    if (this.nblAmountDisplayEl) this.nblAmountDisplayEl.textContent = this.formatCurrency(this.data.teams.nbl.totalAmount);

    // Update combined progress (only if target is loaded)
    if (this.data.combinedTarget > 0) {
      const combinedPercentage = Math.min((totalDisbursed / this.data.combinedTarget) * 100, 100);
      if (this.combinedPercentageEl) this.combinedPercentageEl.textContent = `${combinedPercentage.toFixed(1)}%`;
      if (this.combinedProgressEl) this.combinedProgressEl.style.width = `${combinedPercentage}%`;
    }
  }
}

// ============================================
// API INTEGRATION WITH CORS HANDLING
// ============================================

class APIIntegration {
  constructor() {
    this.apiConfig = {
      ELI: {
        sanctionSummary: 'https://www.everydayloanindia.com/crm/admin/api/sanction_summary',
        sanctionTarget: 'https://www.everydayloanindia.com/crm/admin/api/sanction_target_total'
      },
      NBL: {
        sanctionSummary: 'https://nextbigloan.in/lms/admin/api/sanction_summary',
        sanctionTarget: 'https://nextbigloan.in/lms/admin/api/sanction_target_total'
      }
    };

    this.corsProxies = [
      '',
      'https://corsproxy.io/?',
      'https://api.allorigins.win/raw?url='
    ];

    this.currentProxyIndex = 0;
    this.refreshInterval = 15000; // 15 seconds
    this.init();
  }

  async init() {
    console.log('🚀 Initializing API Integration...');
    await this.fetchAndUpdate();
    setInterval(() => {
      this.fetchAndUpdate();
    }, this.refreshInterval);
    console.log('✅ API Integration initialized - Auto-refresh every 15 seconds');
  }

  async fetchWithProxy(url, proxyIndex = 0) {
    const proxy = this.corsProxies[proxyIndex];
    const fullUrl = proxy ? `${proxy}${encodeURIComponent(url)}` : url;

    try {
      const response = await fetch(fullUrl);
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      return await response.json();
    } catch (error) {
      if (proxyIndex < this.corsProxies.length - 1) {
        console.log(`⚠️ Trying alternative proxy for ${url}`);
        return await this.fetchWithProxy(url, proxyIndex + 1);
      }
      throw error;
    }
  }

  async fetchAndUpdate() {
    try {
      console.log('🔄 Fetching data from APIs...');
      const [eliData, nblData] = await Promise.all([
        this.fetchELIData(),
        this.fetchNBLData()
      ]);

      if (eliData && nblData) {
        this.updateDashboard(eliData, nblData);
        console.log('✅ Data updated successfully');
      }
    } catch (error) {
      console.error('❌ Error fetching API data:', error);
      this.showError('Unable to fetch data. Please check your connection.');
    }
  }

  async fetchELIData() {
    try {
      const [summaryData, targetData] = await Promise.all([
        this.fetchWithProxy(this.apiConfig.ELI.sanctionSummary),
        this.fetchWithProxy(this.apiConfig.ELI.sanctionTarget)
      ]);

      console.log('📊 ELI Data:', { summary: summaryData, target: targetData });

      return {
        freshCases: summaryData?.data?.totalFreshCases || 0,
        freshAmount: summaryData?.data?.totalFreshAmount || 0,
        grandAmount: summaryData?.data?.totalGrandAmount || 0,
        target: targetData?.total_target || 0
      };
    } catch (error) {
      console.error('❌ Error fetching ELI data:', error);
      return null;
    }
  }

  async fetchNBLData() {
    try {
      const [summaryData, targetData] = await Promise.all([
        this.fetchWithProxy(this.apiConfig.NBL.sanctionSummary),
        this.fetchWithProxy(this.apiConfig.NBL.sanctionTarget)
      ]);

      console.log('📊 NBL Data:', { summary: summaryData, target: targetData });

      return {
        freshCases: summaryData?.data?.totalFreshCases || 0,
        freshAmount: summaryData?.data?.totalFreshAmount || 0,
        grandAmount: summaryData?.data?.totalGrandAmount || 0,
        target: targetData?.total_target || 0
      };
    } catch (error) {
      console.error('❌ Error fetching NBL data:', error);
      return null;
    }
  }

  updateDashboard(eliData, nblData) {
    const combinedTarget = eliData.target + nblData.target;

    const updatedData = {
      combinedTarget: combinedTarget,
      teams: {
        eli: {
          name: 'ELI',
          disbursementTarget: eliData.target,
          collectionTarget: 46955310,
          disbursed: eliData.grandAmount,
          collected: 0,
          freshLeads: eliData.freshCases,
          totalAmount: eliData.freshAmount
        },
        nbl: {
          name: 'NBL',
          disbursementTarget: nblData.target,
          collectionTarget: 51989851,
          disbursed: nblData.grandAmount,
          collected: 0,
          freshLeads: nblData.freshCases,
          totalAmount: nblData.freshAmount
        }
      },
      lastUpdated: new Date().toISOString()
    };

    localStorage.setItem('bharatfincareData', JSON.stringify(updatedData));

    console.log('✅ Dashboard data updated:', {
      combinedTarget: this.formatCurrency(combinedTarget),
      eliTarget: this.formatCurrency(eliData.target),
      nblTarget: this.formatCurrency(nblData.target)
    });
  }

  showError(message) {
    const statusEl = document.getElementById('live-status');
    if (statusEl) {
      statusEl.textContent = message;
      statusEl.style.color = 'var(--color-error)';
      setTimeout(() => {
        statusEl.textContent = 'Live Dashboard';
        statusEl.style.color = '';
      }, 5000);
    }
  }

  formatCurrency(num) {
    if (num === 0) return '₹0';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(num);
  }
}

// ============================================
// PAGE AUTO-REFRESH SETUP
// ============================================

class PageAutoRefresh {
  constructor(intervalMinutes = 60) {
    this.refreshInterval = intervalMinutes * 60 * 1000;
    this.initAutoRefresh();
  }

  initAutoRefresh() {
    setInterval(() => {
      console.log('🔄 Auto-refreshing page...');
      location.reload();
    }, this.refreshInterval);

    setInterval(() => {
      const nextRefreshTime = new Date(Date.now() + this.refreshInterval);
      console.log(`⏰ Next page refresh at: ${nextRefreshTime.toLocaleTimeString('en-IN')}`);
    }, this.refreshInterval / 2);
  }
}

// Initialize Dashboard and API Integration
document.addEventListener('DOMContentLoaded', () => {
  new LiveDashboard();
  
  setTimeout(() => {
    new APIIntegration();
  }, 1000);

  // Optional: Enable page auto-refresh every 60 minutes
  // new PageAutoRefresh(60);
});

class LiveDashboard {
            constructor() {
                this.data = {
                    combinedTarget: 95500000,
                    teams: {
                        eli: {
                            name: 'ELI',
                            disbursementTarget: 45500000,
                            collectionTarget: 46955310,
                            disbursed: 0,
                            collected: 0,
                            freshLeads: 0,
                            totalAmount: 0
                        },
                        nbl: {
                            name: 'NBL',
                            disbursementTarget: 50000000,
                            collectionTarget: 51989851,
                            disbursed: 0,
                            collected: 0,
                            freshLeads: 0,
                            totalAmount: 0
                        }
                    }
                };

                this.initializeElements();
                this.setupLiveConnection();
                this.loadData();
                this.updateDisplay();
                this.updateSummary();
                this.updateLastUpdated();
            }

            initializeElements() {
                // Combined target elements
                this.combinedCurrentEl = document.getElementById('combined-current');
                this.combinedProgressEl = document.getElementById('combined-progress');
                this.combinedPercentageEl = document.getElementById('combined-percentage');

                // Summary elements
                this.totalFreshLeadsEl = document.getElementById('total-fresh-leads');
                this.totalAmountSummaryEl = document.getElementById('total-amount-summary');
                this.eliFreshDisplayEl = document.getElementById('eli-fresh-display');
                this.nblFreshDisplayEl = document.getElementById('nbl-fresh-display');
                this.eliAmountDisplayEl = document.getElementById('eli-amount-display');
                this.nblAmountDisplayEl = document.getElementById('nbl-amount-display');

                // Team elements
                this.eliFreshLeadsEl = document.getElementById('eli-fresh-leads');
                this.eliTotalAmountEl = document.getElementById('eli-total-amount');
                this.eliDisbursedEl = document.getElementById('eli-disbursed');
                this.eliCollectedEl = document.getElementById('eli-collected');
                this.eliDisbursementPercentageEl = document.getElementById('eli-disbursement-percentage');
                this.eliCollectionPercentageEl = document.getElementById('eli-collection-percentage');
                this.eliDisbursementProgressEl = document.getElementById('eli-disbursement-progress');
                this.eliCollectionProgressEl = document.getElementById('eli-collection-progress');

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
            }

            setupLiveConnection() {
                // BroadcastChannel for real-time updates
                this.broadcastChannel = new BroadcastChannel('bharatfincare-updates');

                this.broadcastChannel.addEventListener('message', (event) => {
                    if (event.data.type === 'admin-update') {
                        this.handleLiveUpdate(event.data.data);
                    } else if (event.data.type === 'admin-reset') {
                        this.handleLiveReset();
                    }
                });

                // Storage event listener for cross-tab updates
                window.addEventListener('storage', (event) => {
                    if (event.key === 'bharatfincareData') {
                        if (event.newValue) {
                            const newData = JSON.parse(event.newValue);
                            this.handleLiveUpdate(newData);
                        } else {
                            this.handleLiveReset();
                        }
                    }
                });

                // Check for updates every 2 seconds as fallback
                setInterval(() => {
                    this.checkForUpdates();
                }, 2000);
            }

            handleLiveUpdate(newData) {
                this.data = { ...newData };
                this.showUpdateIndicator();
                this.updateDisplay();
                this.updateSummary();
                this.updateLastUpdated(newData.lastUpdated);
                this.animateUpdate();
            }

            handleLiveReset() {
                // Reset to default values
                this.data.teams.eli = {
                    name: 'ELI', disbursementTarget: 45500000, collectionTarget: 46955310,
                    disbursed: 0, collected: 0, freshLeads: 0, totalAmount: 0
                };
                this.data.teams.nbl = {
                    name: 'NBL', disbursementTarget: 50000000, collectionTarget: 51989851,
                    disbursed: 0, collected: 0, freshLeads: 0, totalAmount: 0
                };

                this.showUpdateIndicator();
                this.updateDisplay();
                this.updateSummary();
                this.updateLastUpdated();
                this.animateUpdate();
            }

            checkForUpdates() {
                const savedData = localStorage.getItem('bharatfincareData');
                if (savedData) {
                    try {
                        const newData = JSON.parse(savedData);
                        if (JSON.stringify(newData.teams) !== JSON.stringify(this.data.teams)) {
                            this.handleLiveUpdate(newData);
                        }
                    } catch (e) {
                        console.error('Error checking for updates:', e);
                    }
                }
            }

            showUpdateIndicator() {
                this.liveStatusEl.textContent = 'Updating...';
                setTimeout(() => {
                    this.liveStatusEl.textContent = 'Live Dashboard';
                }, 1500);
            }

            animateUpdate() {
                // Add update animation to all metric sections
                const metricCards = document.querySelectorAll('.metric-section, .summary-card, .combined-target-card');
                metricCards.forEach(card => {
                    card.classList.add('updating');
                    setTimeout(() => {
                        card.classList.remove('updating');
                    }, 500);
                });
            }

            updateLastUpdated(timestamp = null) {
                const now = timestamp ? new Date(timestamp) : new Date();
                const timeString = now.toLocaleTimeString();
                this.lastUpdatedEl.textContent = `Last updated: ${timeString}`;
            }

            loadData() {
                const savedData = localStorage.getItem('bharatfincareData');
                if (savedData) {
                    try {
                        const loadedData = JSON.parse(savedData);
                        if (loadedData && loadedData.teams) {
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

                // Update percentages and progress bars
                const eliDisbursementPercentage = Math.min((eli.disbursed / eli.disbursementTarget) * 100, 100);
                const eliCollectionPercentage = Math.min((eli.collected / eli.collectionTarget) * 100, 100);
                const nblDisbursementPercentage = Math.min((nbl.disbursed / nbl.disbursementTarget) * 100, 100);
                const nblCollectionPercentage = Math.min((nbl.collected / nbl.collectionTarget) * 100, 100);

                if (this.eliDisbursementPercentageEl) this.eliDisbursementPercentageEl.textContent = `${eliDisbursementPercentage.toFixed(1)}%`;
                if (this.eliCollectionPercentageEl) this.eliCollectionPercentageEl.textContent = `${eliCollectionPercentage.toFixed(1)}%`;
                if (this.nblDisbursementPercentageEl) this.nblDisbursementPercentageEl.textContent = `${nblDisbursementPercentage.toFixed(1)}%`;
                if (this.nblCollectionPercentageEl) this.nblCollectionPercentageEl.textContent = `${nblCollectionPercentage.toFixed(1)}%`;

                if (this.eliDisbursementProgressEl) this.eliDisbursementProgressEl.style.width = `${eliDisbursementPercentage}%`;
                if (this.eliCollectionProgressEl) this.eliCollectionProgressEl.style.width = `${eliCollectionPercentage}%`;
                if (this.nblDisbursementProgressEl) this.nblDisbursementProgressEl.style.width = `${nblDisbursementPercentage}%`;
                if (this.nblCollectionProgressEl) this.nblCollectionProgressEl.style.width = `${nblCollectionPercentage}%`;
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

                // Update combined progress
                const combinedPercentage = Math.min((totalDisbursed / this.data.combinedTarget) * 100, 100);
                if (this.combinedPercentageEl) this.combinedPercentageEl.textContent = `${combinedPercentage.toFixed(1)}%`;
                if (this.combinedProgressEl) this.combinedProgressEl.style.width = `${combinedPercentage}%`;
            }
        }

        // Initialize dashboard when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            new LiveDashboard();
        });

// ============================================
// API INTEGRATION - Auto-refresh every 15 seconds
// ============================================
class APIIntegration {
    constructor() {
        this.apiConfig = {
            NBL: {
                sanctionSummary: 'https://nextbigloan.in/lms/admin/api/sanction_summary',
                sanctionTarget: 'https://nextbigloan.in/lms/admin/api/sanction_target_total'
            },
            ELI: {
                sanctionSummary: 'https://www.everydayloanindia.com/crm/admin/api/sanction_summary',
                sanctionTarget: 'https://www.everydayloanindia.com/crm/admin/api/sanction_target_total'
            }
        };

        this.refreshInterval = 15000; // 15 seconds
        this.init();
    }

    async init() {
        console.log('🚀 Initializing API Integration...');
        // Initial load
        await this.fetchAndUpdate();

        // Set up auto-refresh
        setInterval(() => {
            this.fetchAndUpdate();
        }, this.refreshInterval);

        console.log('✅ API Integration initialized - Auto-refresh every 15 seconds');
    }

    async fetchAndUpdate() {
        try {
            console.log('🔄 Fetching data from APIs...');

            // Fetch from both APIs in parallel
            const [eliData, nblData] = await Promise.all([
                this.fetchELIData(),
                this.fetchNBLData()
            ]);

            if (eliData && nblData) {
                this.updateDisplay(eliData, nblData);
                console.log('✅ Data updated successfully');
            }
        } catch (error) {
            console.error('❌ Error fetching API data:', error);
        }
    }

    async fetchELIData() {
        try {
            const [summaryRes, targetRes] = await Promise.all([
                fetch(this.apiConfig.ELI.sanctionSummary),
                fetch(this.apiConfig.ELI.sanctionTarget)
            ]);

            const summaryData = await summaryRes.json();
            const targetData = await targetRes.json();

            console.log('📊 ELI Data:', summaryData.data);

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
            const [summaryRes, targetRes] = await Promise.all([
                fetch(this.apiConfig.NBL.sanctionSummary),
                fetch(this.apiConfig.NBL.sanctionTarget)
            ]);

            const summaryData = await summaryRes.json();
            const targetData = await targetRes.json();

            console.log('📊 NBL Data:', summaryData.data);

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

    updateDisplay(eliData, nblData) {
        // Update ELI section - Fresh Leads
        const eliFreshLeadsEl = document.getElementById('eli-fresh-leads');
        if (eliFreshLeadsEl) {
            eliFreshLeadsEl.textContent = eliData.freshCases;
            console.log(`✅ ELI Fresh Leads: ${eliData.freshCases}`);
        }

        // Update ELI section - Fresh Amount
        const eliTotalAmountEl = document.getElementById('eli-total-amount');
        if (eliTotalAmountEl) {
            eliTotalAmountEl.textContent = this.formatCurrency(eliData.freshAmount);
            console.log(`✅ ELI Fresh Amount: ${this.formatCurrency(eliData.freshAmount)}`);
        }

        // Update NBL section - Fresh Leads
        const nblFreshLeadsEl = document.getElementById('nbl-fresh-leads');
        if (nblFreshLeadsEl) {
            nblFreshLeadsEl.textContent = nblData.freshCases;
            console.log(`✅ NBL Fresh Leads: ${nblData.freshCases}`);
        }

        // Update NBL section - Fresh Amount
        const nblTotalAmountEl = document.getElementById('nbl-total-amount');
        if (nblTotalAmountEl) {
            nblTotalAmountEl.textContent = this.formatCurrency(nblData.freshAmount);
            console.log(`✅ NBL Fresh Amount: ${this.formatCurrency(nblData.freshAmount)}`);
        }

        // Update Combined Target (sum of both grandAmounts)
        const combinedGrandTotal = eliData.grandAmount + nblData.grandAmount;

        const combinedTargetEl = document.getElementById('combined-target');
        if (combinedTargetEl) {
            combinedTargetEl.textContent = this.formatCurrency(combinedGrandTotal);
            console.log(`✅ Combined Target: ${this.formatCurrency(combinedGrandTotal)}`);
        }

        const combinedCurrentEl = document.getElementById('combined-current');
        if (combinedCurrentEl) {
            combinedCurrentEl.textContent = this.formatCurrency(combinedGrandTotal);
        }

        // Update combined progress
        const combinedProgressEl = document.getElementById('combined-progress');
        const combinedPercentageEl = document.getElementById('combined-percentage');

        // Calculate progress based on the sum of targets from both APIs
        const totalTarget = eliData.target + nblData.target;
        const progressPercentage = totalTarget > 0 ? Math.min((combinedGrandTotal / totalTarget) * 100, 100) : 0;

        if (combinedProgressEl) {
            combinedProgressEl.style.width = `${progressPercentage}%`;
        }
        if (combinedPercentageEl) {
            combinedPercentageEl.textContent = `${Math.round(progressPercentage)}%`;
        }

        // Update summary section
        this.updateSummarySection(eliData, nblData);

        // Update last refresh time
        this.updateLastRefreshTime();
    }

    updateSummarySection(eliData, nblData) {
        // Total fresh leads
        const totalFreshLeadsEl = document.getElementById('total-fresh-leads');
        if (totalFreshLeadsEl) {
            totalFreshLeadsEl.textContent = eliData.freshCases + nblData.freshCases;
        }

        // Total amount summary
        const totalAmountSummaryEl = document.getElementById('total-amount-summary');
        if (totalAmountSummaryEl) {
            totalAmountSummaryEl.textContent = this.formatCurrency(eliData.freshAmount + nblData.freshAmount);
        }

        // ELI summary
        const eliFreshSummaryEl = document.getElementById('eli-fresh-summary');
        const eliAmountSummaryEl = document.getElementById('eli-amount-summary');
        if (eliFreshSummaryEl) {
            eliFreshSummaryEl.textContent = eliData.freshCases;
        }
        if (eliAmountSummaryEl) {
            eliAmountSummaryEl.textContent = this.formatCurrency(eliData.freshAmount);
        }

        // NBL summary
        const nblFreshSummaryEl = document.getElementById('nbl-fresh-summary');
        const nblAmountSummaryEl = document.getElementById('nbl-amount-summary');
        if (nblFreshSummaryEl) {
            nblFreshSummaryEl.textContent = nblData.freshCases;
        }
        if (nblAmountSummaryEl) {
            nblAmountSummaryEl.textContent = this.formatCurrency(nblData.freshAmount);
        }
    }

    updateLastRefreshTime() {
        const now = new Date();
        const timeString = now.toLocaleString('en-IN', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit',
            hour12: true
        });
        console.log(`🕒 Last updated: ${timeString}`);
    }

    formatCurrency(num) {
        if (num === 0) return '₹0';

        const formatter = new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        });

        return formatter.format(num);
    }
}

// Initialize API Integration after a short delay
setTimeout(() => {
    new APIIntegration();
}, 1000);

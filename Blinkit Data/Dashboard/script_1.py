# Now I'll create the admin.html file as requested
# This will be the admin interface where numbers can be updated, and they'll be visible in index_no_numbers.html

admin_html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bharatfincare - Admin Dashboard</title>
    <link rel="stylesheet" href="style.css">
    <style>
        /* Additional styles for admin dashboard */
        .admin-container {
            min-height: 100vh;
            background: var(--color-background);
            padding: var(--space-20);
        }

        .admin-header {
            text-align: center;
            margin-bottom: var(--space-32);
            padding-bottom: var(--space-20);
            border-bottom: 2px solid var(--color-border);
        }

        .admin-title {
            font-size: var(--font-size-4xl);
            font-weight: var(--font-weight-bold);
            color: var(--color-primary);
            margin-bottom: var(--space-8);
        }

        .admin-subtitle {
            color: var(--color-text-secondary);
            font-size: var(--font-size-lg);
        }

        .admin-main {
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: var(--space-32);
        }

        @media (max-width: 768px) {
            .admin-main {
                grid-template-columns: 1fr;
                gap: var(--space-20);
            }
        }

        .admin-team-section {
            background: var(--color-surface);
            border-radius: var(--radius-lg);
            padding: var(--space-24);
            box-shadow: var(--shadow-md);
            border: 1px solid var(--color-card-border);
        }

        .admin-team-header {
            display: flex;
            align-items: center;
            margin-bottom: var(--space-24);
            padding-bottom: var(--space-16);
            border-bottom: 2px solid var(--color-card-border-inner);
        }

        .admin-team-name {
            font-size: var(--font-size-2xl);
            font-weight: var(--font-weight-bold);
            margin: 0;
            flex-grow: 1;
        }

        .eli-section .admin-team-name {
            color: #2563eb;
        }

        .nbl-section .admin-team-name {
            color: #14b8a6;
        }

        .admin-input-group {
            margin-bottom: var(--space-20);
        }

        .admin-input-label {
            display: block;
            font-size: var(--font-size-base);
            font-weight: var(--font-weight-medium);
            color: var(--color-text);
            margin-bottom: var(--space-8);
        }

        .admin-form-control {
            width: 100%;
            padding: var(--space-12);
            font-family: var(--font-family-mono);
            font-size: var(--font-size-lg);
            text-align: center;
            background-color: var(--color-surface);
            border: 2px solid var(--color-border);
            border-radius: var(--radius-base);
            color: var(--color-text);
            transition: all var(--duration-fast) var(--ease-standard);
        }

        .admin-form-control:focus {
            border-color: var(--color-primary);
            outline: none;
            box-shadow: var(--focus-ring);
            background-color: var(--color-surface);
        }

        .admin-form-control::placeholder {
            color: var(--color-text-secondary);
            opacity: 0.7;
        }

        .admin-actions {
            grid-column: 1 / -1;
            text-align: center;
            margin-top: var(--space-32);
        }

        .admin-button-group {
            display: flex;
            gap: var(--space-16);
            justify-content: center;
            flex-wrap: wrap;
        }

        .admin-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: var(--space-12) var(--space-24);
            border-radius: var(--radius-base);
            font-size: var(--font-size-base);
            font-weight: var(--font-weight-medium);
            cursor: pointer;
            transition: all var(--duration-normal) var(--ease-standard);
            border: none;
            text-decoration: none;
            position: relative;
            min-width: 140px;
        }

        .admin-btn--primary {
            background: var(--color-primary);
            color: var(--color-btn-primary-text);
        }

        .admin-btn--primary:hover {
            background: var(--color-primary-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow-lg);
        }

        .admin-btn--secondary {
            background: var(--color-secondary);
            color: var(--color-text);
            border: 1px solid var(--color-border);
        }

        .admin-btn--secondary:hover {
            background: var(--color-secondary-hover);
            transform: translateY(-1px);
        }

        .admin-btn:focus-visible {
            outline: none;
            box-shadow: var(--focus-ring);
        }

        .admin-loading-spinner {
            display: inline-block;
            width: 16px;
            height: 16px;
            border: 2px solid transparent;
            border-top: 2px solid currentColor;
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-left: var(--space-8);
        }

        .hidden {
            display: none;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .notification {
            position: fixed;
            top: var(--space-20);
            right: var(--space-20);
            padding: var(--space-16) var(--space-20);
            border-radius: var(--radius-base);
            color: var(--color-white);
            font-weight: var(--font-weight-medium);
            z-index: 1000;
            transform: translateX(100%);
            transition: transform var(--duration-normal) var(--ease-standard);
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification--success {
            background: var(--color-success);
        }

        .notification--error {
            background: var(--color-error);
        }

        .notification--info {
            background: var(--color-info);
        }

        .preview-link {
            display: inline-block;
            margin-top: var(--space-20);
            padding: var(--space-8) var(--space-16);
            background: var(--color-secondary);
            color: var(--color-text);
            text-decoration: none;
            border-radius: var(--radius-base);
            font-size: var(--font-size-sm);
            transition: all var(--duration-fast) var(--ease-standard);
        }

        .preview-link:hover {
            background: var(--color-secondary-hover);
        }

        .input-error {
            border-color: var(--color-error) !important;
            animation: shake 0.5s ease-in-out;
        }

        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-5px); }
            75% { transform: translateX(5px); }
        }
    </style>
</head>
<body>
    <div class="admin-container">
        <header class="admin-header">
            <div class="header-content">
                <div class="logo-icon">
                    <img src="logo-2.jpg" alt="Bharatfincare Logo" style="width: 60px; height: 60px; object-fit: contain;">
                </div>
                <h1 class="admin-title">Admin Dashboard</h1>
                <p class="admin-subtitle">Update dashboard values that will be visible on the main display</p>
            </div>
        </header>

        <main class="admin-main">
            <!-- ELI Section -->
            <section class="admin-team-section eli-section">
                <div class="admin-team-header">
                    <h2 class="admin-team-name">ELI Team</h2>
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-eli-fresh-input">Fresh Leads Count</label>
                    <input type="number" id="admin-eli-fresh-input" class="admin-form-control" placeholder="e.g., 25" min="0">
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-eli-amount-input">Total Amount (₹)</label>
                    <input type="text" id="admin-eli-amount-input" class="admin-form-control" placeholder="e.g., 2500000" inputmode="numeric">
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-eli-disbursement-input">Disbursed Amount (₹)</label>
                    <input type="text" id="admin-eli-disbursement-input" class="admin-form-control" placeholder="e.g., 3500000" inputmode="numeric">
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-eli-collection-input">Collected Amount (₹)</label>
                    <input type="text" id="admin-eli-collection-input" class="admin-form-control" placeholder="e.g., 4000000" inputmode="numeric">
                </div>
            </section>

            <!-- NBL Section -->
            <section class="admin-team-section nbl-section">
                <div class="admin-team-header">
                    <h2 class="admin-team-name">NBL Team</h2>
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-nbl-fresh-input">Fresh Leads Count</label>
                    <input type="number" id="admin-nbl-fresh-input" class="admin-form-control" placeholder="e.g., 30" min="0">
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-nbl-amount-input">Total Amount (₹)</label>
                    <input type="text" id="admin-nbl-amount-input" class="admin-form-control" placeholder="e.g., 3000000" inputmode="numeric">
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-nbl-disbursement-input">Disbursed Amount (₹)</label>
                    <input type="text" id="admin-nbl-disbursement-input" class="admin-form-control" placeholder="e.g., 3800000" inputmode="numeric">
                </div>

                <div class="admin-input-group">
                    <label class="admin-input-label" for="admin-nbl-collection-input">Collected Amount (₹)</label>
                    <input type="text" id="admin-nbl-collection-input" class="admin-form-control" placeholder="e.g., 4500000" inputmode="numeric">
                </div>
            </section>

            <!-- Admin Actions -->
            <div class="admin-actions">
                <div class="admin-button-group">
                    <button id="admin-update-btn" class="admin-btn admin-btn--primary">
                        <span class="button-text">Update Dashboard</span>
                        <span class="admin-loading-spinner hidden"></span>
                    </button>
                    <button id="admin-reset-btn" class="admin-btn admin-btn--secondary">
                        Reset All Values
                    </button>
                </div>
                <a href="index_no_numbers.html" class="preview-link" target="_blank">
                    📊 View Main Dashboard
                </a>
            </div>
        </main>
    </div>

    <script>
        // Admin Dashboard JavaScript
        class AdminDashboard {
            constructor() {
                this.initializeElements();
                this.bindEvents();
                this.loadCurrentValues();
            }

            initializeElements() {
                // ELI Admin inputs
                this.adminEliFreshInputEl = document.getElementById('admin-eli-fresh-input');
                this.adminEliAmountInputEl = document.getElementById('admin-eli-amount-input');
                this.adminEliDisbursementInputEl = document.getElementById('admin-eli-disbursement-input');
                this.adminEliCollectionInputEl = document.getElementById('admin-eli-collection-input');

                // NBL Admin inputs
                this.adminNblFreshInputEl = document.getElementById('admin-nbl-fresh-input');
                this.adminNblAmountInputEl = document.getElementById('admin-nbl-amount-input');
                this.adminNblDisbursementInputEl = document.getElementById('admin-nbl-disbursement-input');
                this.adminNblCollectionInputEl = document.getElementById('admin-nbl-collection-input');

                // Control elements
                this.adminUpdateBtnEl = document.getElementById('admin-update-btn');
                this.adminResetBtnEl = document.getElementById('admin-reset-btn');
            }

            bindEvents() {
                this.adminUpdateBtnEl.addEventListener('click', () => this.updateDashboard());
                this.adminResetBtnEl.addEventListener('click', () => this.resetDashboard());

                // Enter key support for all inputs
                const inputs = [
                    this.adminEliFreshInputEl, this.adminEliAmountInputEl, 
                    this.adminEliDisbursementInputEl, this.adminEliCollectionInputEl,
                    this.adminNblFreshInputEl, this.adminNblAmountInputEl,
                    this.adminNblDisbursementInputEl, this.adminNblCollectionInputEl
                ];

                inputs.forEach(input => {
                    if (input) {
                        input.addEventListener('keypress', (e) => {
                            if (e.key === 'Enter') {
                                this.updateDashboard();
                            }
                        });

                        // Allow only numeric input for currency fields
                        if (input.inputMode === 'numeric' || input.type === 'number') {
                            input.addEventListener('input', (e) => {
                                let value = e.target.value;
                                if (input.type !== 'number') {
                                    // Remove any non-numeric characters for currency fields
                                    value = value.replace(/[^0-9]/g, '');
                                    e.target.value = value;
                                }

                                // Remove error styling if input becomes valid
                                if (e.target.classList.contains('input-error')) {
                                    e.target.classList.remove('input-error');
                                }
                            });
                        }

                        // Select all text on focus for better UX
                        input.addEventListener('focus', () => {
                            input.select();
                        });
                    }
                });
            }

            loadCurrentValues() {
                // Load current values from localStorage if available
                const savedData = localStorage.getItem('bharatfincareData');
                if (savedData) {
                    try {
                        const data = JSON.parse(savedData);
                        
                        // Load ELI values
                        this.adminEliFreshInputEl.value = data.teams.eli.freshLeads || '';
                        this.adminEliAmountInputEl.value = data.teams.eli.totalAmount || '';
                        this.adminEliDisbursementInputEl.value = data.teams.eli.disbursed || '';
                        this.adminEliCollectionInputEl.value = data.teams.eli.collected || '';

                        // Load NBL values
                        this.adminNblFreshInputEl.value = data.teams.nbl.freshLeads || '';
                        this.adminNblAmountInputEl.value = data.teams.nbl.totalAmount || '';
                        this.adminNblDisbursementInputEl.value = data.teams.nbl.disbursed || '';
                        this.adminNblCollectionInputEl.value = data.teams.nbl.collected || '';
                    } catch (e) {
                        console.error('Error loading saved data:', e);
                    }
                }
            }

            async updateDashboard() {
                const eliDisbursed = parseInt(this.adminEliDisbursementInputEl.value) || 0;
                const eliCollected = parseInt(this.adminEliCollectionInputEl.value) || 0;
                const eliFresh = parseInt(this.adminEliFreshInputEl.value) || 0;
                const eliAmount = parseInt(this.adminEliAmountInputEl.value) || 0;

                const nblDisbursed = parseInt(this.adminNblDisbursementInputEl.value) || 0;
                const nblCollected = parseInt(this.adminNblCollectionInputEl.value) || 0;
                const nblFresh = parseInt(this.adminNblFreshInputEl.value) || 0;
                const nblAmount = parseInt(this.adminNblAmountInputEl.value) || 0;

                // Validation
                if (eliDisbursed < 0 || eliCollected < 0 || nblDisbursed < 0 || nblCollected < 0 ||
                    eliFresh < 0 || nblFresh < 0 || eliAmount < 0 || nblAmount < 0) {
                    this.showInputError();
                    return;
                }

                this.setLoadingState(true);

                // Create data object to save
                const dashboardData = {
                    combinedTarget: 95500000,
                    teams: {
                        eli: {
                            name: 'ELI',
                            disbursementTarget: 45500000,
                            collectionTarget: 46955310,
                            disbursed: eliDisbursed,
                            collected: eliCollected,
                            freshLeads: eliFresh,
                            totalAmount: eliAmount
                        },
                        nbl: {
                            name: 'NBL',
                            disbursementTarget: 50000000,
                            collectionTarget: 51989851,
                            disbursed: nblDisbursed,
                            collected: nblCollected,
                            freshLeads: nblFresh,
                            totalAmount: nblAmount
                        }
                    }
                };

                // Save to localStorage
                localStorage.setItem('bharatfincareData', JSON.stringify(dashboardData));

                // Simulate network delay
                await new Promise(resolve => setTimeout(resolve, 1000));

                this.setLoadingState(false);
                this.showNotification('Dashboard updated successfully! Changes will be visible on the main dashboard.', 'success');
            }

            resetDashboard() {
                // Clear all inputs
                this.adminEliFreshInputEl.value = '';
                this.adminEliAmountInputEl.value = '';
                this.adminEliDisbursementInputEl.value = '';
                this.adminEliCollectionInputEl.value = '';

                this.adminNblFreshInputEl.value = '';
                this.adminNblAmountInputEl.value = '';
                this.adminNblDisbursementInputEl.value = '';
                this.adminNblCollectionInputEl.value = '';

                // Clear localStorage
                localStorage.removeItem('bharatfincareData');

                this.showNotification('All values reset successfully!', 'success');
            }

            showInputError() {
                const inputs = [
                    this.adminEliFreshInputEl, this.adminEliAmountInputEl,
                    this.adminEliDisbursementInputEl, this.adminEliCollectionInputEl,
                    this.adminNblFreshInputEl, this.adminNblAmountInputEl,
                    this.adminNblDisbursementInputEl, this.adminNblCollectionInputEl
                ];

                inputs.forEach(input => {
                    if (!input.value || parseInt(input.value) < 0) {
                        input.classList.add('input-error');
                        setTimeout(() => input.classList.remove('input-error'), 2000);
                    }
                });

                this.showNotification('Please enter valid positive numbers for all fields', 'error');
            }

            setLoadingState(loading) {
                const buttonText = this.adminUpdateBtnEl.querySelector('.button-text');
                const spinner = this.adminUpdateBtnEl.querySelector('.admin-loading-spinner');

                if (loading) {
                    this.adminUpdateBtnEl.disabled = true;
                    this.adminUpdateBtnEl.classList.add('loading');
                    spinner.classList.remove('hidden');
                    buttonText.textContent = 'Updating...';
                } else {
                    this.adminUpdateBtnEl.disabled = false;
                    this.adminUpdateBtnEl.classList.remove('loading');
                    spinner.classList.add('hidden');
                    buttonText.textContent = 'Update Dashboard';
                }
            }

            showNotification(message, type = 'info') {
                // Create notification element
                const notification = document.createElement('div');
                notification.className = `notification notification--${type}`;
                notification.textContent = message;

                // Add to document
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
        }

        // Initialize the admin dashboard when DOM is loaded
        document.addEventListener('DOMContentLoaded', () => {
            new AdminDashboard();
        });
    </script>
</body>
</html>'''

# Save the admin HTML file
with open('admin.html', 'w', encoding='utf-8') as f:
    f.write(admin_html_content)

print("admin.html file has been created successfully!")
print("\nFeatures of the admin dashboard:")
print("1. Clean admin interface with all input fields organized in team sections")
print("2. All inputs are clearly labeled and styled")
print("3. Data is saved to localStorage and will be loaded by the main dashboard")
print("4. Link to view the main dashboard")
print("5. Reset functionality to clear all values")
print("6. Loading states and notifications")
print("7. Input validation and error handling")
print("8. Responsive design for mobile devices")
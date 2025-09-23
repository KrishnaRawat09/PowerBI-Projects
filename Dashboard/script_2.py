# Now I need to modify the main app.js to load data from localStorage
# This will connect the admin dashboard to the main dashboard

# Read the current app.js content
with open('app.js', 'r', encoding='utf-8') as f:
    js_content = f.read()

# Create a modified version that loads data from localStorage
modified_js_content = js_content.replace(
    '''constructor() {
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
        };''',
    '''constructor() {
        // Load data from localStorage if available (from admin dashboard)
        const savedData = localStorage.getItem('bharatfincareData');
        
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

        // Override with saved data if available
        if (savedData) {
            try {
                const loadedData = JSON.parse(savedData);
                if (loadedData && loadedData.teams) {
                    // Merge saved data with default structure
                    this.data.teams.eli = { ...this.data.teams.eli, ...loadedData.teams.eli };
                    this.data.teams.nbl = { ...this.data.teams.nbl, ...loadedData.teams.nbl };
                }
            } catch (e) {
                console.error('Error loading saved data:', e);
            }
        }'''
)

# Also modify the updateDashboard method to save data to localStorage
modified_js_content = modified_js_content.replace(
    '''this.data.teams.nbl.totalAmount = nblAmount;''',
    '''this.data.teams.nbl.totalAmount = nblAmount;

        // Save updated data to localStorage for admin dashboard
        localStorage.setItem('bharatfincareData', JSON.stringify(this.data));'''
)

# Save the modified app.js
with open('app_modified.js', 'w', encoding='utf-8') as f:
    f.write(modified_js_content)

print("app_modified.js has been created with localStorage integration!")
print("\nChanges made:")
print("1. Constructor now loads data from localStorage if available")
print("2. Data is saved to localStorage whenever dashboard is updated")
print("3. This creates a two-way connection between admin and main dashboard")
print("\nTo use this:")
print("1. Replace your app.js with app_modified.js content")
print("2. Use admin.html to input values")
print("3. Values will automatically appear in index_no_numbers.html")
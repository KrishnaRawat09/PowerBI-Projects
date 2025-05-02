# 🧠 HR Attrition Analysis Dashboard – Power BI Project

This project is a **Human Resources (HR) Attrition Dashboard** built using **SQL Server** and **Power BI**, aimed at understanding employee exit trends and key attrition patterns in an organization.

---

## 📌 Project Objectives

- Identify **which employees are leaving** the company.
- Understand **when and why** employees tend to leave.
- Analyze **patterns by age, department, education, salary, and job role**.
- Create **interactive visualizations** to help HR and management make data-driven decisions.

---

## 🔧 Tools Used

- **SQL Server Management Studio (SSMS)** – Data import, cleaning, and transformation
- **Microsoft Power BI** – Dashboard creation and data visualization
- **CSV Files** – Used as raw data input

---

## 📂 Project Workflow

1. **Data Import & Cleaning (SQL)**
   - Imported multiple CSV datasets into **SSMS** using SQL queries.
   - Cleaned data: removed duplicates, filled/null-handled values, corrected inconsistent formatting.

2. **Data Transformation**
   - Created calculated columns such as:
     - **Age Group** (e.g., 18–25, 26–35, etc.)
     - **Salary Group** (e.g., Up to ₹5K, ₹5K–10K, etc.)

3. **Power BI Integration**
   - Imported SQL tables into Power BI.
   - Created new columns and measures using **DAX**, including:
     - `Attrition Count`
     - `Attrition Rate (%)`

4. **Dashboard Design**
   - Used cards, clustered bar charts, and pie charts to show:
     - Total employee count
     - Total attrition count and rate
     - Attrition by age, department, education, salary, and job roles
     - Gender-wise attrition breakdown

---

## 📊 Key Insights

- 📉 **Attrition Rate**: 16.1%
- 👨‍💼 **Most affected Age Group**: 26–35
- 💼 **Top roles with attrition**:
  - Laboratory Technicians
  - Sales Executives
- 💰 **Highest attrition by salary group**: Up to ₹5K
- 🏢 **Departments most affected**: R&D and Sales

---

## 📎 Files Included

- `HR_Attrition_Dashboard.pbix` – Power BI dashboard file
- `Screenshots/` – Folder with dashboard preview images
- `README.md` – This documentation file

---

## 🚀 Getting Started

1. Clone this repository.
2. Open the `.pbix` file in Power BI Desktop.
3. If using your own data, update the data source and refresh.

⚠️ **Note:** If the Power BI file is connected to a local SQL Server, you may need to change the source or use a version with imported data for it to display correctly.

---

## 📷 Dashboard Preview

![HR Attrition Dashboard](Screenshots/HR_Attrition_Summary.png)

---

## 🤝 Let's Connect

Feel free to connect or share feedback on [LinkedIn](https://www.linkedin.com/in/yourprofile)  
🔗 GitHub: [Your GitHub Profile](https://github.com/yourusername)

---

## 🏷 Hashtags (for sharing)
`#PowerBI #HRAnalytics #DataVisualization #SQL #BusinessIntelligence #AttritionAnalysis #DataAnalytics #DataScience #SSMS #GitHubProjects #DashboardDesign`


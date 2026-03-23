import streamlit as st
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="MoneyMitra - Personal Money Health Checker",
    page_icon="💰",
    layout="wide"
)

# Title
st.title("MoneyMitra 💰")
st.markdown("*Your friendly guide to financial wellness*")
st.markdown("---")

# Sidebar inputs
st.sidebar.header("📊 Enter Your Financial Details")
income = st.sidebar.number_input("Monthly Income (₹)", min_value=0.0, value=50000.0, step=1000.0)
expenses = st.sidebar.number_input("Monthly Expenses (₹)", min_value=0.0, value=30000.0, step=1000.0)
savings = st.sidebar.number_input("Monthly Savings (₹)", min_value=0.0, value=10000.0, step=1000.0)
investments = st.sidebar.number_input("Total Investments (₹)", min_value=0.0, value=5000.0, step=1000.0)
debt = st.sidebar.number_input("Total Debt (₹)", min_value=0.0, value=100000.0, step=5000.0)
emi_payment = st.sidebar.number_input("Monthly EMI / Loan Payments (₹)", min_value=0.0, value=5000.0, step=500.0)
emergency_fund = st.sidebar.number_input("Emergency Fund (₹)", min_value=0.0, value=50000.0, step=5000.0)
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30)

st.markdown("---")

# Calculations
if income > 0:
    # 1. Savings Rate: (Savings / Income) * 100
    savings_rate = (savings / income) * 100
    
    # 2. Debt-to-Income Ratio: (Debt / Annual Income) * 100
    debt_to_income = (debt / (income * 12)) * 100
    
    # 3. Emergency Fund Score: min((Emergency Fund Months / 6) * 100, 100)
    emergency_fund_months = emergency_fund / expenses if expenses > 0 else 0
    emergency_fund_score = min((emergency_fund_months / 6) * 100, 100)
    
    # 4. Credit Score Normalized (using a slider 0-850 next, for now default)
    # Using a default 750 for demo
    credit_score = 750
    credit_score_normalized = (credit_score / 850) * 100
    
    # 5. Investment Ratio: (Investments / Annual Income) * 100
    investment_ratio = (investments / income) * 100 if income > 0 else 0
    
    # 6. Expense Ratio: 100 - (Expenses / Income * 100)
    expense_ratio = max(100 - ((expenses / income) * 100), 0) if income > 0 else 0
    
    # 7. Surplus Ratio: ((Income - Expenses - EMI) / Income) * 100
    monthly_surplus = income - expenses - emi_payment
    surplus_ratio = (monthly_surplus / income * 100) if income > 0 else 0
    
    # 8. Debt Burden: Total Debt / Annual Income
    debt_burden = debt / (income * 12) if income > 0 else 0
    
    # Weighted Money Health Score
    money_health_score = (
        (savings_rate / 50 * 100 if savings_rate <= 50 else 100) * 0.20 +  # Cap at 50%
        max(100 - debt_to_income, 0) * 0.20 +  # Inverse: lower debt is better
        emergency_fund_score * 0.20 +
        credit_score_normalized * 0.15 +
        min(investment_ratio / 30 * 100, 100) * 0.15 +  # Cap at 30%
        expense_ratio * 0.05 +
        min(surplus_ratio / 10 * 100, 100) * 0.05  # Surplus ratio
    )
    
    # Color coding
    if money_health_score < 40:
        score_color = "#FF4B4B"  # Red
        score_status = "⚠️ Needs Attention"
        main_recommendation = "📌 **Build your emergency fund.** You have ~{:.1f} months covered; aim for 6–9 months of expenses.".format(emergency_fund_months)
    elif money_health_score < 70:
        score_color = "#FFA500"  # Orange/Yellow
        score_status = "⚡ Fair"
        main_recommendation = "📌 **Improve your savings rate.** You're saving {:.1f}% of income; aim for 20%+.".format(savings_rate)
    else:
        score_color = "#00C851"  # Green
        score_status = "✅ Excellent"
        main_recommendation = "📌 **Great progress!** Keep maintaining your good financial habits and consider diversifying investments."
    
    # Display main score
    st.markdown(f"""<div style='text-align: center; padding: 20px;'>
        <h2 style='color: {score_color}; font-size: 48px; margin: 0;'>{money_health_score:.1f} / 100</h2>
        <h3 style='color: {score_color}; margin-top: 5px;'>{score_status}</h3>
    </div>""", unsafe_allow_html=True)
    
    st.progress(money_health_score / 100, text=f"{money_health_score:.1f}%")
    
    st.markdown("---")
    st.markdown("## 📊 Metric Breakdown")
    
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if savings_rate >= 20:
            status = "🟢 Good"
            score = min(savings_rate / 50 * 100, 100)
        elif savings_rate >= 10:
            status = "🟡 Fair"
            score = savings_rate / 20 * 100
        else:
            status = "🜴 Needs Work"
            score = savings_rate / 10 * 100
        
        st.metric("Savings Rate", f"{savings_rate:.1f}%", delta=f"Score: {score:.0f}")
        st.info(status)
        st.caption("Target: ≥ 20%")
    
    with col2:
        if debt_to_income <= 36:
            status = "🟢 Good"
            score = 100
        elif debt_to_income <= 50:
            status = "🟡 Fair"
            score = 100 - (debt_to_income - 36) * 2
        else:
            status = "🜴 Needs Work"
            score = max(100 - debt_to_income, 0)
        
        st.metric("Debt-to-Income (EMI)", f"{emi_payment/income*100:.1f}%", delta=f"Score: {score:.0f}")
        st.info(status)
        st.caption("Target: ≤ 36%")
    
    with col3:
        if emergency_fund_months >= 6:
            status = "🟢 Good"
        elif emergency_fund_months >= 3:
            status = "🟡 Fair"
        else:
            status = "🜴 Needs Work"
        
        st.metric("Emergency Fund", f"{emergency_fund_months:.1f} mo", delta=f"Score: {emergency_fund_score:.0f}")
        st.info(status)
        st.caption("Target: ≥ 6 months")
    
    # Row 2 metrics
    col4, col5, col6 = st.columns(3)
    
    with col4:
        if investment_ratio >= 10:
            status = "🟢 Good"
            inv_score = min(investment_ratio / 30 * 100, 100)
        elif investment_ratio >= 5:
            status = "🟡 Fair"
            inv_score = investment_ratio / 10 * 100
        else:
            status = "🜴 Needs Work"
            inv_score = investment_ratio * 10
        
        st.metric("Investment Rate", f"{investment_ratio:.1f}%", delta=f"Score: {inv_score:.0f}")
        st.info(status)
        st.caption("Target: ≥ 10%")
    
    with col5:
        if surplus_ratio >= 10:
            status = "🟢 Good"
            surplus_score = 100
        elif surplus_ratio >= 0:
            status = "🟡 Fair"
            surplus_score = surplus_ratio * 10
        else:
            status = "🜴 Needs Work"
            surplus_score = 0
        
        st.metric("Surplus Ratio", f"{surplus_ratio:.1f}%", delta=f"Score: {surplus_score:.0f}")
        st.info(status)
        st.caption("Target: ≥ 10%")
    
    with col6:
        if debt_burden <= 2:
            status = "🟢 Good"
            burden_score = 100
        elif debt_burden <= 3:
            status = "🟡 Fair"
            burden_score = 100 - (debt_burden - 2) * 50
        else:
            status = "🜴 Needs Work"
            burden_score = max(100 - debt_burden * 20, 0)
        
        st.metric("Debt Burden (vs income)", f"{debt_burden:.2f}×", delta=f"Score: {burden_score:.0f}")
        st.info(status)
        st.caption("Target: ≤ 2×")
    
    st.markdown("---")
    st.markdown("## 💡 Personalised Recommendations")
    st.warning(main_recommendation)
    
    # More insights
    with st.expander("🔍 More Insights"):
        st.write(f"**Savings Rate:** {savings_rate:.1f}% (Target: 20-30%)")
        st.write(f"**Debt-to-Income Ratio:** {debt_to_income:.1f}% (Target: Below 30%)")
        st.write(f"**Emergency Fund:** {emergency_fund_months:.1f} months (Target: 6 months)")
        st.write(f"**Investment Ratio:** {investment_ratio:.1f}% of monthly income (Target: 10%+)")
        st.write(f"**Monthly Surplus:** ₹{monthly_surplus:.0f} (Income - Expenses - EMI)")
        st.write(f"**Total Debt:** ₹{debt:.0f}")
        st.write(f"**Debt Burden:** {debt_burden:.2f}x annual income")
else:
    st.warning("⚠️ Please enter your monthly income to calculate your Money Health Score.")

st.markdown("---")
st.caption("💡 **Disclaimer:** MoneyMitra is for educational purposes only and does not constitute financial advice.")

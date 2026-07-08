# Indian Financial Knowledge Base for FinSense
# This data gets embedded and stored in Supabase pgvector

FINANCIAL_KNOWLEDGE = [
    {
        "title": "Emergency Fund Basics",
        "category": "savings",
        "content": """An emergency fund is money set aside for unexpected expenses like job loss, 
        medical emergencies, or major repairs. For young Indian professionals, the recommended 
        emergency fund is 3 to 6 months of monthly expenses. If your monthly expenses are 30,000 
        rupees, your emergency fund should be between 90,000 and 180,000 rupees. Keep emergency 
        funds in a liquid instrument like a savings account or liquid mutual fund — not in FD or 
        equity. Never invest your emergency fund in stocks or SIP."""
    },
    {
        "title": "SIP Investment Basics",
        "category": "investment",
        "content": """Systematic Investment Plan or SIP is a method of investing a fixed amount 
        regularly in mutual funds. SIP uses rupee cost averaging — you buy more units when markets 
        are low and fewer when markets are high. For equity mutual funds, the historical average 
        return in India is 12 to 15 percent annually over long periods of 10 years or more. 
        Minimum SIP amount is typically 500 rupees per month. ELSS funds have a 3-year lock-in 
        and provide tax benefits under Section 80C up to 1.5 lakhs per year. Index funds track 
        Nifty 50 or Sensex and have lower expense ratios than actively managed funds."""
    },
    {
        "title": "Fixed Deposit Rates India 2024-25",
        "category": "savings",
        "content": """Current Fixed Deposit interest rates from major Indian banks for 2024-25. 
        SBI FD rates range from 3.5 to 7.1 percent depending on tenure. HDFC Bank FD rates range 
        from 3.5 to 7.4 percent. ICICI Bank FD rates range from 3.5 to 7.2 percent. Senior 
        citizens get 0.25 to 0.5 percent additional interest. Tax Saver FDs have 5-year lock-in 
        and qualify for Section 80C deduction up to 1.5 lakhs. FD interest is taxable as per 
        income tax slab. TDS is deducted at 10 percent if interest exceeds 40,000 rupees per year."""
    },
    {
        "title": "Credit Card Debt Management",
        "category": "debt",
        "content": """Credit card interest rates in India are among the highest — typically 36 to 
        42 percent annually or 3 to 3.5 percent per month. Always pay the full outstanding amount 
        before the due date to avoid interest. Paying only the minimum amount due means you pay 
        interest on the remaining balance. If you have credit card debt, prioritize paying it off 
        before investing — no investment gives 36 percent returns consistently. Convert large 
        credit card bills to EMI if available — the interest rate on EMI conversion is typically 
        12 to 18 percent, much lower than revolving credit."""
    },
    {
        "title": "Home Loan Guidelines India",
        "category": "loan",
        "content": """Home loan interest rates in India for 2024-25 range from 8.35 to 9.5 percent 
        annually depending on the lender and credit score. SBI home loan starts at 8.5 percent. 
        HDFC home loan starts at 8.7 percent. Maximum loan tenure is typically 30 years. Banks 
        typically finance 75 to 90 percent of property value — you need 10 to 25 percent as down 
        payment. EMI should not exceed 40 to 50 percent of monthly take-home salary. Home loan 
        interest up to 2 lakhs per year is tax deductible under Section 24. Principal repayment 
        up to 1.5 lakhs qualifies for Section 80C deduction."""
    },
    {
        "title": "Term Insurance Basics",
        "category": "insurance",
        "content": """Term insurance is pure life insurance that pays a lump sum to nominees if 
        the policyholder dies during the policy term. Recommended coverage is 10 to 15 times 
        annual income. For someone earning 6 lakhs per year, coverage should be 60 to 90 lakhs. 
        Buy term insurance early — premiums are lowest in your 20s and 30s. Online term plans 
        are 30 to 40 percent cheaper than offline plans. Do not mix insurance with investment — 
        avoid ULIPs and endowment plans. LIC term plans and private insurers like HDFC Life, 
        ICICI Prudential, and Max Life are popular choices."""
    },
    {
        "title": "Income Tax Slabs India 2024-25",
        "category": "tax",
        "content": """Income tax slabs for India in financial year 2024-25 under new tax regime. 
        Income up to 3 lakhs — nil tax. Income from 3 to 7 lakhs — 5 percent tax. Income from 
        7 to 10 lakhs — 10 percent tax. Income from 10 to 12 lakhs — 15 percent tax. Income 
        from 12 to 15 lakhs — 20 percent tax. Income above 15 lakhs — 30 percent tax. Standard 
        deduction of 75,000 rupees is available. Under old tax regime, deductions under 80C up 
        to 1.5 lakhs, HRA, home loan interest up to 2 lakhs are available. Consult a CA for 
        tax planning — this is general information only."""
    },
    {
        "title": "Mutual Fund Categories India",
        "category": "investment",
        "content": """Types of mutual funds in India and their risk profiles. Equity funds invest 
        primarily in stocks and have high risk but high return potential — suitable for 5 plus 
        year goals. Debt funds invest in bonds and have low to medium risk — suitable for 1 to 
        3 year goals. Hybrid funds invest in both equity and debt — balanced risk. Liquid funds 
        invest in short-term instruments and are ideal for emergency funds and parking surplus 
        cash. Index funds passively track an index and have lower expense ratios. ELSS funds 
        offer tax benefits with 3-year lock-in. Small cap funds have highest risk and return 
        potential. Large cap funds are more stable."""
    },
    {
        "title": "50-30-20 Budgeting Rule",
        "category": "budgeting",
        "content": """The 50-30-20 budgeting rule is a simple framework for managing money. 
        Allocate 50 percent of take-home salary to needs — rent, groceries, utilities, EMIs, 
        insurance premiums. Allocate 30 percent to wants — dining out, entertainment, travel, 
        shopping. Allocate 20 percent to savings and investments — emergency fund, SIP, FD, 
        retirement corpus. For someone earning 50,000 rupees per month: 25,000 for needs, 
        15,000 for wants, 10,000 for savings. Adjust percentages based on your city and 
        lifestyle — Mumbai and Delhi residents may need 60 percent for needs."""
    },
    {
        "title": "PPF Public Provident Fund",
        "category": "investment",
        "content": """Public Provident Fund or PPF is a government-backed long-term savings 
        scheme in India. Current interest rate is 7.1 percent per annum compounded annually. 
        Lock-in period is 15 years — partial withdrawal allowed from 7th year. Minimum 
        investment is 500 rupees per year, maximum is 1.5 lakhs per year. Contribution up to 
        1.5 lakhs per year qualifies for Section 80C tax deduction. Interest earned is 
        completely tax-free. Maturity amount is tax-free. PPF is ideal for long-term goals 
        like retirement where you want guaranteed tax-free returns."""
    },
    {
        "title": "NPS National Pension System",
        "category": "retirement",
        "content": """National Pension System or NPS is a voluntary retirement savings scheme 
        regulated by PFRDA. Offers additional tax deduction of 50,000 rupees under Section 80CCD 
        over and above the 1.5 lakh Section 80C limit. Minimum contribution is 1000 rupees per 
        year. Money is locked until age 60 — 60 percent can be withdrawn tax-free at maturity, 
        40 percent must be used to buy annuity. Returns are market-linked — typically 8 to 10 
        percent annually. Suitable for salaried individuals who want additional tax saving beyond 
        80C limit and are comfortable with long-term lock-in."""
    },
    {
        "title": "Gold Investment Options India",
        "category": "investment",
        "content": """Gold investment options in India and their comparison. Physical gold — coins 
        and jewelry — has making charges of 10 to 25 percent and storage risk. Gold ETFs trade 
        on stock exchange and track gold prices without physical storage — expense ratio around 
        0.5 percent. Sovereign Gold Bonds or SGBs issued by RBI offer 2.5 percent annual interest 
        plus gold price appreciation — best option for long-term gold investment. Digital gold on 
        apps like PhonePe and Paytm allows small amounts but has higher charges. Recommended gold 
        allocation is 5 to 10 percent of total portfolio for diversification."""
    }
]
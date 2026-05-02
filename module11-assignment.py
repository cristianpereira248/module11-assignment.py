# Module 11 Assignment: Data Visualization with Matplotlib
# SunCoast Retail Visual Analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("=" * 60)
print("SUNCOAST RETAIL VISUAL ANALYSIS")
print("=" * 60)

np.random.seed(42)

quarters = pd.date_range(start='2022-01-01', periods=8, freq='Q')
quarter_labels = ['Q1 2022','Q2 2022','Q3 2022','Q4 2022','Q1 2023','Q2 2023','Q3 2023','Q4 2023']
locations = ['Tampa','Miami','Orlando','Jacksonville']
categories = ['Electronics','Clothing','Home Goods','Sporting Goods','Beauty']

quarterly_data = []

for quarter_idx, quarter in enumerate(quarters):
    for location in locations:
        for category in categories:
            base_sales = np.random.normal(100000,20000)

            seasonal_factor = 1.3 if quarter.quarter == 4 else (0.8 if quarter.quarter == 1 else 1.0)

            location_factor = {'Tampa':1.0,'Miami':1.2,'Orlando':0.9,'Jacksonville':0.8}[location]
            category_factor = {'Electronics':1.5,'Clothing':1.0,'Home Goods':0.8,'Sporting Goods':0.7,'Beauty':0.9}[category]
            growth_factor = (1 + 0.05/4) ** quarter_idx

            sales = base_sales * seasonal_factor * location_factor * category_factor * growth_factor
            sales *= np.random.normal(1.0,0.1)

            ad_spend = (sales**0.7)*0.05*np.random.normal(1.0,0.2)

            quarterly_data.append({
                'Quarter':quarter,
                'QuarterLabel':quarter_labels[quarter_idx],
                'Location':location,
                'Category':category,
                'Sales':round(sales,2),
                'AdSpend':round(ad_spend,2),
                'Year':quarter.year
            })

customer_data = []
total_customers = 2000

age_params = {'Tampa':(45,15),'Miami':(35,12),'Orlando':(38,14),'Jacksonville':(42,13)}

for location in locations:
    mean_age, std_age = age_params[location]
    count = int(total_customers * {'Tampa':0.3,'Miami':0.35,'Orlando':0.2,'Jacksonville':0.15}[location])

    ages = np.clip(np.random.normal(mean_age,std_age,count),18,80).astype(int)

    for age in ages:
        if age < 30:
            category_pref = np.random.choice(categories,p=[0.3,0.3,0.1,0.2,0.1])
        elif age < 50:
            category_pref = np.random.choice(categories,p=[0.25,0.2,0.25,0.15,0.15])
        else:
            category_pref = np.random.choice(categories,p=[0.15,0.1,0.35,0.1,0.3])

        base_amount = np.random.gamma(5,20)
        tier = np.random.choice(['Budget','Mid-range','Premium'],p=[0.3,0.5,0.2])
        factor = {'Budget':0.7,'Mid-range':1.0,'Premium':1.8}[tier]

        customer_data.append({
            'Location':location,
            'Age':age,
            'Category':category_pref,
            'PurchaseAmount':round(base_amount*factor,2),
            'PriceTier':tier
        })

sales_df = pd.DataFrame(quarterly_data)
customer_df = pd.DataFrame(customer_data)

sales_df['Quarter_Num'] = sales_df['Quarter'].dt.quarter
sales_df['SalesPerDollarSpent'] = sales_df['Sales'] / sales_df['AdSpend']


# ---------- VISUAL FUNCTIONS ----------

def plot_quarterly_sales_trend():
    fig, ax = plt.subplots()
    trend = sales_df.groupby('QuarterLabel')['Sales'].sum()
    trend.plot(ax=ax, marker='o')
    ax.set_title("Quarterly Sales Trend")
    ax.set_xlabel("Quarter")
    ax.set_ylabel("Sales")
    return fig


def plot_location_sales_comparison():
    fig, ax = plt.subplots()
    for loc in locations:
        data = sales_df[sales_df['Location'] == loc].groupby('QuarterLabel')['Sales'].sum()
        ax.plot(data.index, data.values, marker='o', label=loc)
    ax.legend()
    ax.set_title("Sales by Location")
    return fig


def plot_category_performance_by_location():
    fig, ax = plt.subplots()
    latest = sales_df[sales_df['QuarterLabel'] == 'Q4 2023']
    pivot = latest.pivot_table(values='Sales', index='Category', columns='Location')
    pivot.plot(kind='bar', ax=ax)
    return fig


def plot_sales_composition_by_location():
    fig, ax = plt.subplots()
    pivot = sales_df.pivot_table(values='Sales', index='Location', columns='Category')
    pivot.plot(kind='bar', stacked=True, ax=ax)
    return fig


def plot_ad_spend_vs_sales():
    fig, ax = plt.subplots()
    ax.scatter(sales_df['AdSpend'], sales_df['Sales'])
    ax.set_xlabel("Ad Spend")
    ax.set_ylabel("Sales")
    return fig


def plot_ad_efficiency_over_time():
    fig, ax = plt.subplots()
    eff = sales_df.groupby('QuarterLabel')['SalesPerDollarSpent'].mean()
    eff.plot(ax=ax)
    return fig


def plot_customer_age_distribution():
    fig, axs = plt.subplots(2,2)
    axs = axs.flatten()
    for i, loc in enumerate(locations):
        customer_df[customer_df['Location']==loc]['Age'].plot(kind='hist', ax=axs[i])
        axs[i].set_title(loc)
    return fig


def plot_purchase_by_age_group():
    fig, ax = plt.subplots()
    bins = [18,30,45,60,100]
    labels = ['18-30','31-45','46-60','60+']
    customer_df['AgeGroup'] = pd.cut(customer_df['Age'], bins=bins, labels=labels)
    customer_df.boxplot(column='PurchaseAmount', by='AgeGroup', ax=ax)
    return fig


def plot_purchase_amount_distribution():
    fig, ax = plt.subplots()
    customer_df['PurchaseAmount'].plot(kind='hist', ax=ax)
    return fig


def plot_sales_by_price_tier():
    fig, ax = plt.subplots()
    customer_df['PriceTier'].value_counts().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    return fig


def plot_category_market_share():
    fig, ax = plt.subplots()
    sales_df.groupby('Category')['Sales'].sum().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    return fig


def plot_location_sales_distribution():
    fig, ax = plt.subplots()
    sales_df.groupby('Location')['Sales'].sum().plot(kind='pie', ax=ax, autopct='%1.1f%%')
    return fig


def create_business_dashboard():
    fig, axs = plt.subplots(2,2)

    sales_df.groupby('QuarterLabel')['Sales'].sum().plot(ax=axs[0,0])
    sales_df.groupby('Location')['Sales'].sum().plot(kind='bar', ax=axs[0,1])
    customer_df['Age'].plot(kind='hist', ax=axs[1,0])
    sales_df.groupby('Category')['Sales'].sum().plot(kind='pie', ax=axs[1,1])

    return fig


# ---------- MAIN ----------

def main():
    print("\n" + "=" * 60)
    print("SUNCOAST RETAIL VISUAL ANALYSIS RESULTS")
    print("=" * 60)

    fig1 = plot_quarterly_sales_trend()
    fig2 = plot_location_sales_comparison()
    fig3 = plot_category_performance_by_location()
    fig4 = plot_sales_composition_by_location()
    fig5 = plot_ad_spend_vs_sales()
    fig6 = plot_ad_efficiency_over_time()
    fig7 = plot_customer_age_distribution()
    fig8 = plot_purchase_by_age_group()
    fig9 = plot_purchase_amount_distribution()
    fig10 = plot_sales_by_price_tier()
    fig11 = plot_category_market_share()
    fig12 = plot_location_sales_distribution()
    fig13 = create_business_dashboard()

    print("\nKEY BUSINESS INSIGHTS:")
    print("- Sales trend upward with strong Q4 spikes (seasonality effect)")
    print("- Miami consistently outperforms other locations")
    print("- Electronics dominate overall revenue share")
    print("- Advertising positively correlates with sales but shows diminishing returns")

    plt.show()


if __name__ == "__main__":
    main()
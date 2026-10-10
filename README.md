## Market Basket Analysis and Retail Insights

## Project Overview

Market Basket Analysis is a data mining technique used to identify relationships between products that customers frequently purchase together. This project applies the Apriori algorithm to transaction data to discover frequent itemsets and generate association rules.

The project also provides retail insights through interactive visualizations and a web-based dashboard, helping businesses understand customer purchasing patterns and improve product recommendations.

## Objectives

- Identify frequently purchased products.
- Discover relationships between products using association rules.
- Apply the Apriori algorithm to transaction data.
- Analyze support, confidence, and lift.
- Generate product recommendations and cross-selling opportunities.
- Visualize retail insights through an interactive dashboard.

## Technologies Used

- Programming Language: Python
- Data Analysis: Pandas
- Association Rule Mining: MLxtend
- Data Visualization: Plotly
- Web Framework: Flask
- Network Visualization: NetworkX
- Frontend: HTML and CSS

## Project Structure

Market_Basket_Analysis_and_Retail_Insights/
│
├── app.py
├── advanced_market_basket_10000.csv
├── README.md
├── MBA_ouput.pdf
│
├── templates/
│   ├── index.html
│   └── product.html
│
└── static/
    └── style.css

Note: Place the HTML files inside the "templates" folder and the CSS file inside the "static" folder to match Flask's default directory structure.

#3 Algorithm Used

Apriori Algorithm

The Apriori algorithm identifies frequent itemsets in transaction data and uses them to generate association rules.

It works by finding combinations of products that frequently appear together in customer transactions.

#3Important Metrics

- Support: Measures how frequently a product combination appears in all transactions.
- Confidence: Measures how often a transaction containing one product or itemset also contains another.
- Lift: Measures how strongly two itemsets are associated compared with their expected occurrence if they were independent.

A lift greater than 1 indicates a positive association between the itemsets.

## Key Features

- Transaction data analysis
- Frequent itemset generation
- Association rule mining
- Support, confidence, and lift calculation
- Product recommendation insights
- Interactive data visualizations
- Network graph visualization of product relationships
- Flask-based web dashboard
- Retail business insights for cross-selling

## Business Applications

This project can help retailers:

- Recommend complementary products.
- Identify product combinations for promotional offers.
- Improve product placement strategies.
- Support cross-selling and upselling.
- Understand customer purchasing behavior.
- Make data-driven retail decisions.

## How to Run the Project

Prerequisites

Install Python on your computer. Python 3.9 or later is recommended, subject to compatibility with your installed libraries.

Step 1: Clone the Repository

git clone https://github.com/kavyagudi/Market_Basket_Analysis_and_Retail_Insights.git

Step 2: Navigate to the Project Folder

cd Market_Basket_Analysis_and_Retail_Insights

Step 3: Install the Required Libraries

pip install pandas mlxtend plotly flask networkx

Step 4: Check the Project Files

Ensure that:

- "app.py" is in the main project folder.
- "index.html" and "product.html" are inside "templates/".
- "style.css" is inside "static/".
- The CSV dataset is available at the path expected by "app.py".

Step 5: Run the Application

python app.py

Step 6: Open the Dashboard

Open your browser and visit:

http://127.0.0.1:5000/

The dashboard should appear if the Flask application starts successfully.

## Results and Insights

The project analyzes transaction data to identify frequently purchased products and generate association rules.

The resulting insights can help retailers discover product relationships and develop better product recommendation strategies.

Note: Add verified results from your actual application here, such as the number of transactions analyzed, frequent itemsets discovered, and strongest association rules. Do not report unverified metrics.

## Future Enhancements

- Add customer segmentation.
- Integrate a larger retail transaction dataset.
- Improve recommendation accuracy.
- Add more interactive charts and filters.
- Deploy the dashboard online.
- Develop personalized product recommendations.

 Author

Kavya Gudi

GitHub: "kavyagudi" (https://github.com/kavyagudi)

## Conclusion

This project demonstrates how association rule mining and data visualization can reveal customer purchasing patterns. By applying the Apriori algorithm, the project provides useful retail insights that can support product recommendations, cross-selling, and data-driven business decisions.

If you find this project useful, feel free to star the repository!

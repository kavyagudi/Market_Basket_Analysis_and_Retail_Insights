from flask import Flask, render_template, request
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import networkx as nx
import webbrowser
from threading import Timer
import warnings
warnings.filterwarnings("ignore")
app = Flask(__name__)
# Load Dataset
def load_data():
    df = pd.read_csv("advanced_market_basket_10000.csv")
    df.columns = df.columns.str.strip()
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df
# Convert to Transactions
def get_transactions(df):

    transactions = df.groupby(
        ['Member_number', 'Date']
    )['itemDescription'].apply(list).values.tolist()

    return transactions
# Run Apriori
def run_apriori(min_support, min_confidence):

    df = load_data()

    transactions = get_transactions(df)

    te = TransactionEncoder()

    te_array = te.fit(transactions).transform(transactions)

    df_encoded = pd.DataFrame(te_array, columns=te.columns_)

    frequent_itemsets = apriori(
        df_encoded,
        min_support=min_support,
        use_colnames=True
    )

    if frequent_itemsets.empty:
        return None, None, None, df

    rules = association_rules(
        frequent_itemsets,
        metric="confidence",
        min_threshold=min_confidence
    )

    if rules.empty:
        return None, None, None, df

    return rules, frequent_itemsets, df_encoded, df
# Main Page
@app.route("/", methods=["GET", "POST"])
def index():

    rules_data = []
    recommendations = []
    error = None

    top_graph = None
    month_graph = None
    scatter_graph = None
    network_graph = None
    rec_graph = None

    total_transactions = 0
    total_products = 0
    total_rules = 0

    search_product = ""

    min_support = 0.0005
    min_confidence = 0.05

    if request.method == "POST":

        search_product = request.form.get("product", "").lower().strip()

        rules, frequent_itemsets, df_encoded, df = run_apriori(
            min_support,
            min_confidence
        )

        if rules is None:

            error = "No rules generated"

        else:

            rules["antecedents"] = rules["antecedents"].apply(
                lambda x: ', '.join(list(x))
            )

            rules["consequents"] = rules["consequents"].apply(
                lambda x: ', '.join(list(x))
            )

            # Dashboard Metrics
            total_transactions = len(df.groupby(['Member_number', 'Date']))
            total_products = df["itemDescription"].nunique()
            total_rules = len(rules)

            # Recommendations

            if search_product:

                filtered = rules[
                    rules["antecedents"].str.lower().str.contains(search_product)
                ]

                if not filtered.empty:

                    filtered = filtered.sort_values(
                        by="lift",
                        ascending=False
                    )

                    filtered = filtered.drop_duplicates(
                        subset=["consequents"]
                    )

                    recommendations = filtered.head(5).to_dict("records")

                else:
                    error = "No recommendations found"

            # Rules Table

            rules_data = rules.sort_values(
                by="lift",
                ascending=False
            ).head(20).to_dict("records")

            # Top Products Graph

            top_products = df["itemDescription"].value_counts().head(10)

            fig1 = px.bar(
                x=top_products.index,
                y=top_products.values,
                title="Top 10 Sold Products"
            )

            top_graph = pio.to_html(fig1, full_html=False)

            # Monthly Sales Trend

            df["Month"] = df["Date"].dt.to_period("M").astype(str)

            monthly = df.groupby("Month").size()

            fig2 = px.line(
                x=monthly.index,
                y=monthly.values,
                title="Monthly Sales Trend"
            )

            month_graph = pio.to_html(fig2, full_html=False)

            # Support vs Confidence

            fig3 = px.scatter(
                rules,
                x="support",
                y="confidence",
                size="lift",
                color="lift",
                hover_data=["antecedents", "consequents"],
                title="Support vs Confidence"
            )

            scatter_graph = pio.to_html(fig3, full_html=False)

            # Product Network Graph

            G = nx.Graph()

            top_rules = rules.sort_values(
                by="lift",
                ascending=False
            ).head(20)

            for _, row in top_rules.iterrows():

                G.add_edge(
                    row["antecedents"],
                    row["consequents"]
                )

            pos = nx.spring_layout(G)

            edge_x = []
            edge_y = []

            for edge in G.edges():

                x0, y0 = pos[edge[0]]
                x1, y1 = pos[edge[1]]

                edge_x += [x0, x1, None]
                edge_y += [y0, y1, None]

            edge_trace = go.Scatter(
                x=edge_x,
                y=edge_y,
                line=dict(width=1),
                hoverinfo='none',
                mode='lines'
            )

            node_x = []
            node_y = []
            text = []

            for node in G.nodes():

                x, y = pos[node]

                node_x.append(x)
                node_y.append(y)
                text.append(node)

            node_trace = go.Scatter(
                x=node_x,
                y=node_y,
                mode='markers+text',
                text=text,
                textposition="top center",
                marker=dict(size=20, color="orange")
            )

            fig_network = go.Figure(
                data=[edge_trace, node_trace],
                layout=go.Layout(
                    title="Product Relationship Network"
                )
            )

            network_graph = pio.to_html(fig_network, full_html=False)

            # Recommendation Graph

            if search_product:

                filtered_rules = rules[
                    rules["antecedents"].str.lower().str.contains(search_product)
                ]

                if not filtered_rules.empty:

                    G_rec = nx.DiGraph()

                    top_rules_graph = filtered_rules.sort_values(
                        by="lift",
                        ascending=False
                    ).head(10)

                    for _, row in top_rules_graph.iterrows():

                        G_rec.add_edge(
                            row["antecedents"],
                            row["consequents"]
                        )

                    pos = nx.spring_layout(G_rec)

                    edge_x = []
                    edge_y = []

                    for edge in G_rec.edges():

                        x0, y0 = pos[edge[0]]
                        x1, y1 = pos[edge[1]]

                        edge_x += [x0, x1, None]
                        edge_y += [y0, y1, None]

                    edge_trace = go.Scatter(
                        x=edge_x,
                        y=edge_y,
                        line=dict(width=2, color="blue"),
                        hoverinfo='none',
                        mode='lines'
                    )

                    node_x = []
                    node_y = []
                    text = []

                    for node in G_rec.nodes():

                        x, y = pos[node]

                        node_x.append(x)
                        node_y.append(y)
                        text.append(node)

                    node_trace = go.Scatter(
                        x=node_x,
                        y=node_y,
                        mode='markers+text',
                        text=text,
                        textposition="top center",
                        marker=dict(size=22, color="red")
                    )

                    fig_rec = go.Figure(
                        data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f"Recommended Products for '{search_product}'"
                        )
                    )

                    rec_graph = pio.to_html(fig_rec, full_html=False)

    return render_template(
        "index.html",
        rules=rules_data,
        recommendations=recommendations,
        error=error,
        top_graph=top_graph,
        month_graph=month_graph,
        scatter_graph=scatter_graph,
        network_graph=network_graph,
        rec_graph=rec_graph,
        total_transactions=total_transactions,
        total_products=total_products,
        total_rules=total_rules,
        search_product=search_product
    )

# Product Page
@app.route("/product/<name>")
def product(name):
    return render_template("product.html", name=name)
# Auto Open Browser
def open_browser():
    webbrowser.open_new("http://127.0.0.1:5000/")
if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(debug=True)

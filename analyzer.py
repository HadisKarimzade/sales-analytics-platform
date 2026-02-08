import pandas as pd, matplotlib.pyplot as plt, timeit
from algorithms import merge_sort, linear_search, binary_search
from utils import to_datetime_series, to_numeric_series, clean_status

class SalesAnalyzer:
    def __init__(self, raw_csv, clean_csv, out_dir, fig_dir):
        self.raw_csv, self.clean_csv = raw_csv, clean_csv
        self.out_dir, self.fig_dir = out_dir, fig_dir

    def load_data(self):
        return pd.read_csv(self.raw_csv)

    def clean_data(self, df):
        df = df.copy()
        df["status"] = df["status"].apply(clean_status)
        df["order_date"] = to_datetime_series(df["order_date"])
        for c in ["quantity", "unit_price", "order_amount"]:
            df[c] = to_numeric_series(df[c])
        df = df.dropna().drop_duplicates()
        df["order_amount"] = (df["quantity"] * df["unit_price"]).round(2)
        return df.reset_index(drop=True)

    def run(self, df):
        c = df[df["status"] == "completed"]

        revenue = c["order_amount"].sum()
        aov = c["order_amount"].mean()
        cust_cnt = df["customer_id"].nunique()
        top_cat = c.groupby("product_category")["order_amount"].sum().idxmax()
        top10 = c.groupby("customer_id")["order_amount"].sum().sort_values(ascending=False).head(10)
        repeat = (c.groupby("customer_id")["order_id"].nunique() > 1).mean()

        c["m"] = c["order_date"].dt.to_period("M").astype(str)
        monthly = c.groupby("m")["order_amount"].sum()
        growth = (monthly.pct_change() * 100).round(2)

        avg_size = df.groupby("product_category")["quantity"].mean()
        status_pct = (df["status"].value_counts(normalize=True) * 100).round(2)

        q1, q3 = c["order_amount"].quantile([.25, .75])
        outliers = c[(c["order_amount"] < q1 - 1.5*(q3-q1)) |
                     (c["order_amount"] > q3 + 1.5*(q3-q1))]

        a = df["order_amount"].tolist()
        ids = df["order_id"].tolist()
        t = ids[len(ids)//2]
        algo = {
            "merge_sort": timeit.timeit(lambda: merge_sort(a), number=30),
            "sorted": timeit.timeit(lambda: sorted(a), number=30),
            "linear": timeit.timeit(lambda: linear_search(ids, t), number=100),
            "binary": timeit.timeit(lambda: binary_search(sorted(ids), t), number=100),
        }

        p1 = self.fig_dir / "category.png"
        c.groupby("product_category")["order_amount"].sum().plot(kind="bar")
        plt.savefig(p1); plt.close()

        p2 = self.fig_dir / "monthly.png"
        monthly.plot()
        plt.savefig(p2); plt.close()

        p3 = self.fig_dir / "distribution.png"
        plt.hist(c["order_amount"], bins=15)
        plt.savefig(p3); plt.close()

        df.to_csv(self.clean_csv, index=False)
        top10.to_csv(self.out_dir / "top_customers.csv")

        with open(self.out_dir / "summary_report.txt", "w", encoding="utf-8") as f:
            f.write(f"""Total Revenue: {revenue:.2f}
AOV: {aov:.2f}
Customer Count: {cust_cnt}
Top Category: {top_cat}
Repeat Rate: {repeat:.2%}

Status %:
{status_pct}

Monthly Revenue:
{monthly}

Monthly Growth %:
{growth}

Avg Order Size:
{avg_size}

Outliers Count: {len(outliers)}

Algorithms:
{algo}
""")

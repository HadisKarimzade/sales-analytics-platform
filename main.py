from pathlib import Path
from analyzer import SalesAnalyzer
from utils import ensure_dirs

def main():
    root = Path(__file__).resolve().parent
    data_dir = root / "data"
    out_dir = root / "output"
    fig_dir = out_dir / "figures"
    ensure_dirs([data_dir, out_dir, fig_dir])

    analyzer = SalesAnalyzer(
        raw_csv=data_dir / "sales_data.csv",
        clean_csv=out_dir / "sales_clean.csv",
        out_dir=out_dir,
        fig_dir=fig_dir,
    )

    df = analyzer.clean_data(analyzer.load_data())
    analyzer.run(df)
    print("✅ Project finished successfully.")

if __name__ == "__main__":
    main()

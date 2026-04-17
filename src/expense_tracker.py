from __future__ import annotations

from pathlib import Path
import sys
from typing import Dict, List, Tuple

import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns

matplotlib.use("Agg")
import matplotlib.pyplot as plt


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
OUTPUTS_DIR = BASE_DIR / "outputs"
IMAGES_DIR = BASE_DIR / "images"

CATEGORY_OPTIONS = [
    "Rent",
    "Food",
    "Travel",
    "Utilities",
    "Entertainment",
    "Shopping",
    "Healthcare",
    "Education",
    "Subscriptions",
    "Miscellaneous",
]

PAYMENT_METHOD_OPTIONS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]


def ensure_directories() -> None:
    for directory in [DATA_DIR, OUTPUTS_DIR, IMAGES_DIR]:
        directory.mkdir(parents=True, exist_ok=True)


def is_essential_category(category: str) -> bool:
    return category in ["Rent", "Food", "Utilities", "Healthcare", "Education"]


def normalize_is_essential(value: object, category: str) -> bool:
    if pd.isna(value):
        return is_essential_category(category)

    if isinstance(value, bool):
        return value

    normalized = str(value).strip().lower()
    if normalized in {"yes", "y", "true", "1"}:
        return True
    if normalized in {"no", "n", "false", "0"}:
        return False

    return is_essential_category(category)


def build_transaction_ids(size: int, prefix: str) -> List[str]:
    return [f"{prefix}{index:05d}" for index in range(1, size + 1)]


def prompt_with_default(message: str, default_value: str) -> str:
    user_value = input(f"{message} [{default_value}]: ").strip()
    return user_value or default_value


def choose_from_options(label: str, options: List[str], default_value: str) -> str:
    print(f"\n{label} options: {', '.join(options)}")
    while True:
        selected = prompt_with_default(f"Enter {label.lower()}", default_value)
        if selected in options:
            return selected
        print(f"Please choose one of these options: {', '.join(options)}")


def collect_manual_expenses() -> pd.DataFrame:
    print("\nManual Expense Entry")
    print("-" * 24)
    print("Enter one expense at a time. Type values carefully; the app will analyze whatever you enter.")

    today_string = pd.Timestamp.today().strftime("%Y-%m-%d")
    records: List[Dict[str, object]] = []

    while True:
        date_value = prompt_with_default("Expense date (YYYY-MM-DD)", today_string)
        category = choose_from_options("Category", CATEGORY_OPTIONS, "Food")

        while True:
            amount_text = input("Amount in INR: ").strip()
            try:
                amount = float(amount_text)
                if amount <= 0:
                    raise ValueError
                break
            except ValueError:
                print("Enter a valid positive number for amount.")

        payment_method = choose_from_options("Payment method", PAYMENT_METHOD_OPTIONS, "UPI")
        city = prompt_with_default("City", "Chennai")

        records.append(
            {
                "transaction_id": f"USR{len(records) + 1:05d}",
                "date": date_value,
                "category": category,
                "amount": round(amount, 2),
                "payment_method": payment_method,
                "city": city,
                "is_essential": is_essential_category(category),
            }
        )

        add_more = prompt_with_default("Add another expense? (y/n)", "y").lower()
        if add_more != "y":
            break

    return pd.DataFrame(records)


def load_expenses_from_csv() -> pd.DataFrame:
    print("\nCSV Import Mode")
    print("-" * 16)
    print("Required columns: date, category, amount, payment_method")
    print("Optional columns: city, transaction_id, is_essential")

    while True:
        csv_path = input("Enter CSV file path: ").strip().strip('"')
        source_path = Path(csv_path)
        if source_path.exists() and source_path.is_file():
            break
        print("The file path was not found. Please enter a valid CSV path.")

    df = pd.read_csv(source_path)
    required_columns = {"date", "category", "amount", "payment_method"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing_text = ", ".join(sorted(missing_columns))
        raise ValueError(f"CSV is missing required columns: {missing_text}")

    if "city" not in df.columns:
        df["city"] = "Unknown"
    if "transaction_id" not in df.columns:
        df["transaction_id"] = build_transaction_ids(len(df), "CSV")
    if "is_essential" not in df.columns:
        df["is_essential"] = df["category"].astype(str).map(is_essential_category)

    return df[
        ["transaction_id", "date", "category", "amount", "payment_method", "city", "is_essential"]
    ].copy()


def choose_input_source() -> Tuple[pd.DataFrame, str]:
    if not sys.stdin.isatty():
        print("Interactive input is not available in this session. Falling back to synthetic data mode.")
        dynamic_seed = int(pd.Timestamp.utcnow().timestamp())
        return generate_synthetic_expenses(seed=dynamic_seed), "synthetic"

    print("\nChoose Input Mode")
    print("-" * 18)
    print("1. Manual entry (recommended)")
    print("2. Import from CSV")
    print("3. Synthetic sample data")

    while True:
        choice = prompt_with_default("Select option", "1")
        if choice == "1":
            return collect_manual_expenses(), "manual"
        if choice == "2":
            return load_expenses_from_csv(), "csv"
        if choice == "3":
            num_records_text = prompt_with_default("Number of synthetic records", "300")
            try:
                num_records = int(num_records_text)
                if num_records <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid number. Using 300 synthetic records.")
                num_records = 300

            dynamic_seed = int(pd.Timestamp.utcnow().timestamp())
            return generate_synthetic_expenses(num_records=num_records, seed=dynamic_seed), "synthetic"

        print("Choose 1, 2, or 3.")


def generate_synthetic_expenses(
    num_records: int = 1200,
    start_date: str = "2025-01-01",
    end_date: str = "2025-12-31",
    seed: int = 42,
) -> pd.DataFrame:
    """
    Generate a realistic synthetic expense dataset.
    """
    rng = np.random.default_rng(seed)

    categories = {
        "Rent": {"weight": 0.10, "amount_range": (12000, 22000)},
        "Food": {"weight": 0.24, "amount_range": (150, 900)},
        "Travel": {"weight": 0.12, "amount_range": (300, 2500)},
        "Utilities": {"weight": 0.10, "amount_range": (400, 3000)},
        "Entertainment": {"weight": 0.09, "amount_range": (200, 1800)},
        "Shopping": {"weight": 0.12, "amount_range": (300, 4000)},
        "Healthcare": {"weight": 0.08, "amount_range": (250, 3500)},
        "Education": {"weight": 0.07, "amount_range": (500, 6000)},
        "Subscriptions": {"weight": 0.04, "amount_range": (99, 999)},
        "Miscellaneous": {"weight": 0.04, "amount_range": (100, 2000)},
    }

    payment_methods = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
    payment_weights = [0.35, 0.24, 0.18, 0.13, 0.10]
    dates = pd.date_range(start=start_date, end=end_date, freq="D")
    category_names = list(categories.keys())
    category_weights = [categories[cat]["weight"] for cat in category_names]

    records: List[Dict[str, object]] = []

    for transaction_id in range(1, num_records + 1):
        expense_date = rng.choice(dates)
        month = pd.Timestamp(expense_date).month
        category = rng.choice(category_names, p=category_weights)
        lower, upper = categories[category]["amount_range"]
        amount = rng.uniform(lower, upper)

        if category == "Travel" and month in [4, 5, 6, 11, 12]:
            amount *= rng.uniform(1.15, 1.70)
        if category == "Shopping" and month in [10, 11, 12]:
            amount *= rng.uniform(1.10, 1.60)
        if category == "Entertainment" and month in [5, 6, 12]:
            amount *= rng.uniform(1.05, 1.45)
        if category == "Utilities" and month in [4, 5]:
            amount *= rng.uniform(1.10, 1.30)

        city = rng.choice(
            ["Chennai", "Bengaluru", "Hyderabad", "Pune", "Mumbai", "Delhi"],
            p=[0.28, 0.20, 0.14, 0.12, 0.14, 0.12],
        )
        is_essential = is_essential_category(category)
        payment_method = rng.choice(payment_methods, p=payment_weights)

        records.append(
            {
                "transaction_id": f"EXP{transaction_id:05d}",
                "date": pd.Timestamp(expense_date),
                "category": category,
                "amount": round(float(amount), 2),
                "payment_method": payment_method,
                "city": city,
                "is_essential": is_essential,
            }
        )

    df = pd.DataFrame(records)
    duplicates = df.sample(12, random_state=seed)
    df = pd.concat([df, duplicates], ignore_index=True)

    missing_idx = df.sample(18, random_state=seed + 1).index
    half = len(missing_idx) // 2
    df.loc[missing_idx[:half], "payment_method"] = np.nan
    df.loc[missing_idx[half:], "city"] = np.nan

    return df


def clean_expense_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()
    cleaned["date"] = pd.to_datetime(cleaned["date"], errors="coerce")
    cleaned["category"] = cleaned["category"].astype(str).str.strip()
    cleaned["payment_method"] = cleaned["payment_method"].fillna("Unknown")
    cleaned["city"] = cleaned["city"].fillna("Unknown")
    cleaned["amount"] = pd.to_numeric(cleaned["amount"], errors="coerce")
    cleaned["is_essential"] = [
        normalize_is_essential(value, category)
        for value, category in zip(cleaned["is_essential"], cleaned["category"])
    ]
    cleaned = cleaned.dropna(subset=["date", "amount"])
    cleaned = cleaned[cleaned["amount"] > 0]
    cleaned = cleaned.drop_duplicates(
        subset=["date", "category", "amount", "payment_method", "city"]
    ).sort_values("date")

    cleaned["year"] = cleaned["date"].dt.year
    cleaned["month"] = cleaned["date"].dt.month
    cleaned["month_name"] = cleaned["date"].dt.strftime("%b")
    cleaned["day_name"] = cleaned["date"].dt.strftime("%A")
    cleaned["quarter"] = cleaned["date"].dt.to_period("Q").astype(str)
    cleaned["week"] = cleaned["date"].dt.isocalendar().week.astype(int)

    return cleaned.reset_index(drop=True)


def create_budget_map() -> Dict[str, float]:
    return {
        "Rent": 18000,
        "Food": 12000,
        "Travel": 9000,
        "Utilities": 6000,
        "Entertainment": 5000,
        "Shopping": 7000,
        "Healthcare": 4500,
        "Education": 8000,
        "Subscriptions": 1200,
        "Miscellaneous": 3000,
    }


def create_summary_tables(
    df: pd.DataFrame, budget_map: Dict[str, float]
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    category_summary = (
        df.groupby("category", as_index=False)
        .agg(
            total_spend=("amount", "sum"),
            transaction_count=("transaction_id", "count"),
            average_spend=("amount", "mean"),
        )
        .sort_values("total_spend", ascending=False)
    )

    monthly_summary = (
        df.groupby(["year", "month", "month_name"], as_index=False)
        .agg(
            total_spend=("amount", "sum"),
            average_spend=("amount", "mean"),
            transactions=("transaction_id", "count"),
        )
        .sort_values(["year", "month"])
    )

    payment_summary = (
        df.groupby("payment_method", as_index=False)
        .agg(total_spend=("amount", "sum"), transaction_count=("transaction_id", "count"))
        .sort_values("total_spend", ascending=False)
    )

    monthly_category = (
        df.groupby(["month", "month_name", "category"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "monthly_category_spend"})
        .sort_values(["month", "category"])
    )
    monthly_category["monthly_budget"] = monthly_category["category"].map(budget_map)
    monthly_category["overspend"] = (
        monthly_category["monthly_category_spend"] - monthly_category["monthly_budget"]
    ).round(2)
    monthly_category["is_over_budget"] = monthly_category["overspend"] > 0

    return category_summary, monthly_summary, payment_summary, monthly_category


def generate_insights(
    df: pd.DataFrame,
    category_summary: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    payment_summary: pd.DataFrame,
    monthly_category: pd.DataFrame,
) -> List[str]:
    insights: List[str] = []

    total_spend = df["amount"].sum()
    avg_transaction = df["amount"].mean()
    top_category = category_summary.iloc[0]
    highest_month = monthly_summary.sort_values("total_spend", ascending=False).iloc[0]
    top_payment = payment_summary.iloc[0]

    essential_spend = df.loc[df["is_essential"], "amount"].sum()
    non_essential_spend = df.loc[~df["is_essential"], "amount"].sum()
    essential_pct = (essential_spend / total_spend) * 100
    non_essential_pct = (non_essential_spend / total_spend) * 100

    over_budget_cases = monthly_category[monthly_category["is_over_budget"]].copy()
    top_overspend = None
    if not over_budget_cases.empty:
        top_overspend = over_budget_cases.sort_values("overspend", ascending=False).iloc[0]

    insights.append(f"Total annual spend is INR {total_spend:,.2f} across {len(df)} cleaned transactions.")
    insights.append(f"Average transaction value is INR {avg_transaction:,.2f}.")
    insights.append(
        f"Highest spending category is {top_category['category']} with INR {top_category['total_spend']:,.2f}."
    )
    insights.append(
        f"Peak monthly spend occurred in {highest_month['month_name']} with INR {highest_month['total_spend']:,.2f}."
    )
    insights.append(
        f"Most used payment method by value is {top_payment['payment_method']} with INR {top_payment['total_spend']:,.2f}."
    )
    insights.append(
        f"Essential expenses contribute {essential_pct:.2f}% of spending, while non-essential expenses contribute {non_essential_pct:.2f}%."
    )

    weekday_spend = (
        df.groupby("day_name", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
    )
    top_day = weekday_spend.iloc[0]
    insights.append(
        f"The highest spending weekday is {top_day['day_name']} with INR {top_day['amount']:,.2f}."
    )

    if top_overspend is not None:
        insights.append(
            f"Biggest budget breach appears in {top_overspend['month_name']} for {top_overspend['category']}, overshooting by INR {top_overspend['overspend']:,.2f}."
        )
    else:
        insights.append("No monthly category budget breaches were detected in the synthetic data.")

    return insights


def save_tables(
    raw_df: pd.DataFrame,
    clean_df: pd.DataFrame,
    category_summary: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    payment_summary: pd.DataFrame,
    monthly_category: pd.DataFrame,
    insights: List[str],
    dataset_label: str,
) -> None:
    raw_df.to_csv(DATA_DIR / f"{dataset_label}_expenses_raw.csv", index=False)
    clean_df.to_csv(DATA_DIR / f"{dataset_label}_expenses_cleaned.csv", index=False)
    category_summary.to_csv(OUTPUTS_DIR / "category_summary.csv", index=False)
    monthly_summary.to_csv(OUTPUTS_DIR / "monthly_summary.csv", index=False)
    payment_summary.to_csv(OUTPUTS_DIR / "payment_summary.csv", index=False)
    monthly_category.to_csv(OUTPUTS_DIR / "monthly_category_budget_check.csv", index=False)

    with open(OUTPUTS_DIR / "insights_report.txt", "w", encoding="utf-8") as file:
        file.write("Expense Tracker App using Data Science - Insights Report\n")
        file.write("=" * 60 + "\n\n")
        for index, insight in enumerate(insights, start=1):
            file.write(f"{index}. {insight}\n")


def create_visualizations(
    category_summary: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    payment_summary: pd.DataFrame,
    monthly_category: pd.DataFrame,
) -> None:
    sns.set_theme(style="whitegrid", palette="Set2")

    plt.figure(figsize=(12, 6))
    order = category_summary.sort_values("total_spend", ascending=False)["category"]
    sns.barplot(data=category_summary, x="category", y="total_spend", order=order)
    plt.title("Category-wise Spending")
    plt.xlabel("Category")
    plt.ylabel("Total Spend (INR)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "category_spending_bar.png", dpi=300)
    plt.close()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=monthly_summary, x="month_name", y="total_spend", marker="o", sort=False)
    plt.title("Monthly Spending Trend")
    plt.xlabel("Month")
    plt.ylabel("Total Spend (INR)")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "monthly_spending_trend.png", dpi=300)
    plt.close()

    plt.figure(figsize=(8, 8))
    plt.pie(
        payment_summary["total_spend"],
        labels=payment_summary["payment_method"],
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title("Payment Method Distribution")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "payment_method_pie.png", dpi=300)
    plt.close()

    pivot = monthly_category.pivot_table(
        index="category", columns="month_name", values="monthly_category_spend", aggfunc="sum"
    )
    ordered_months = [
        "Jan",
        "Feb",
        "Mar",
        "Apr",
        "May",
        "Jun",
        "Jul",
        "Aug",
        "Sep",
        "Oct",
        "Nov",
        "Dec",
    ]
    pivot = pivot.reindex(columns=[month for month in ordered_months if month in pivot.columns])

    plt.figure(figsize=(14, 7))
    sns.heatmap(pivot, cmap="YlGnBu", linewidths=0.5)
    plt.title("Monthly Category Spending Heatmap")
    plt.xlabel("Month")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(IMAGES_DIR / "monthly_category_heatmap.png", dpi=300)
    plt.close()

    over_budget = monthly_category[monthly_category["is_over_budget"]].copy()
    if not over_budget.empty:
        plt.figure(figsize=(12, 6))
        sns.barplot(
            data=over_budget.sort_values("overspend", ascending=False).head(15),
            x="month_name",
            y="overspend",
            hue="category",
        )
        plt.title("Top Budget Breaches by Month and Category")
        plt.xlabel("Month")
        plt.ylabel("Overspend Amount (INR)")
        plt.tight_layout()
        plt.savefig(IMAGES_DIR / "budget_breaches_bar.png", dpi=300)
        plt.close()


def print_console_summary(
    clean_df: pd.DataFrame,
    category_summary: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    insights: List[str],
) -> None:
    print("\nExpense Tracker App using Data Science")
    print("=" * 44)
    print(f"Cleaned dataset shape: {clean_df.shape}")
    print(f"Date range: {clean_df['date'].min().date()} to {clean_df['date'].max().date()}")
    print(f"Total spend: INR {clean_df['amount'].sum():,.2f}")
    print("\nTop 5 categories by spend:")
    print(category_summary.head(5).to_string(index=False))
    print("\nMonthly trend preview:")
    print(monthly_summary.head(6).to_string(index=False))
    print("\nKey insights:")
    for idx, insight in enumerate(insights, start=1):
        print(f"{idx}. {insight}")
    print(f"\nSaved CSV outputs in: {OUTPUTS_DIR}")
    print(f"Saved charts in: {IMAGES_DIR}")


def run_expense_tracker_project() -> None:
    ensure_directories()

    raw_df, input_mode = choose_input_source()
    clean_df = clean_expense_data(raw_df)
    budget_map = create_budget_map()
    category_summary, monthly_summary, payment_summary, monthly_category = create_summary_tables(
        clean_df, budget_map
    )
    insights = generate_insights(
        clean_df, category_summary, monthly_summary, payment_summary, monthly_category
    )

    save_tables(
        raw_df,
        clean_df,
        category_summary,
        monthly_summary,
        payment_summary,
        monthly_category,
        insights,
        input_mode,
    )
    create_visualizations(category_summary, monthly_summary, payment_summary, monthly_category)
    print(f"\nInput mode used: {input_mode}")
    print_console_summary(clean_df, category_summary, monthly_summary, insights)

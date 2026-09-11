"""Kaggriculture Current Meta Fingerprints — first Kaggle quicklook.

This notebook-script intentionally focuses on descriptive current-meta movement.
It does not claim a validated winning formula or counter-strategy taxonomy.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def find_input() -> Path:
    candidates = [
        Path("/kaggle/input/kaggriculture-current-meta-fingerprints/strategy_meta.csv"),
        Path("state/expanded_pilot/release_candidate/strategy_meta.csv"),
    ]
    for path in candidates:
        if path.exists():
            return path
    kaggle_root = Path("/kaggle/input")
    if kaggle_root.exists():
        matches = list(kaggle_root.rglob("strategy_meta.csv"))
        if matches:
            return matches[0]
    raise FileNotFoundError("strategy_meta.csv was not found")


DATA_PATH = find_input()
df = pd.read_csv(DATA_PATH)
df["source_date"] = pd.to_datetime(df["source_date"])

print(f"Loaded {len(df):,} rows x {df.shape[1]} columns from {DATA_PATH}")
print(f"Episodes: {df['episode_id'].nunique():,}")
print(f"Source days: {df['source_date'].min().date()} to {df['source_date'].max().date()}")
print("Important: this is a deterministic bounded sample of official daily source manifests, not a random full-ladder sample.")


# %% Daily current-meta summary
daily = (
    df.groupby("source_date", as_index=False)
    .agg(
        episodes=("episode_id", "nunique"),
        seats=("episode_id", "size"),
        opening_t24=("opening_hash_t24", "nunique"),
        opening_t48=("opening_hash_t48", "nunique"),
        mean_cash_t168=("cash_t168", "mean"),
        carrot=("crop_carrot_share", "mean"),
        melon=("crop_melon_share", "mean"),
        strawberry=("crop_strawberry_share", "mean"),
        tomato=("crop_tomato_share", "mean"),
        wheat=("crop_wheat_share", "mean"),
        cow=("animal_cow_share", "mean"),
        goose=("animal_goose_share", "mean"),
        sheep=("animal_sheep_share", "mean"),
    )
)

print("\nDaily summary")
print(daily.round(4).to_string(index=False))


# %% Animal allocation over time
ax = daily.plot(x="source_date", y=["cow", "goose", "sheep"], marker="o", figsize=(9, 5))
ax.set_title("Mean animal tile-turn allocation by official source day")
ax.set_xlabel("Source day")
ax.set_ylabel("Mean share")
ax.legend(title="Animal")
plt.tight_layout()
plt.show()


# %% Crop allocation over time
ax = daily.plot(
    x="source_date",
    y=["carrot", "melon", "strawberry", "tomato", "wheat"],
    marker="o",
    figsize=(9, 5),
)
ax.set_title("Mean crop tile-turn allocation by official source day")
ax.set_xlabel("Source day")
ax.set_ylabel("Mean share")
ax.legend(title="Crop")
plt.tight_layout()
plt.show()


# %% Opening diversity
ax = daily.plot(x="source_date", y=["opening_t24", "opening_t48"], marker="o", figsize=(9, 5))
ax.set_title("Distinct opening fingerprints in each bounded daily sample")
ax.set_xlabel("Source day")
ax.set_ylabel("Distinct hashes")
ax.legend(title="Window")
plt.tight_layout()
plt.show()


# %% Mid-game economy checkpoint
ax = daily.plot(x="source_date", y="mean_cash_t168", marker="o", legend=False, figsize=(9, 5))
ax.set_title("Mean cash at turn 168 by official source day")
ax.set_xlabel("Source day")
ax.set_ylabel("Mean cash")
plt.tight_layout()
plt.show()


# %% Experimental family mix — descriptive only
family = pd.crosstab(df["source_date"], df["strategy_family_experimental"], normalize="index")
family = family.loc[:, family.mean().sort_values(ascending=False).index]
print("\nExperimental family share by day")
print(family.round(3).to_string())
print("\nThe family field is experimental and should not be treated as a validated strategy taxonomy.")


# %% Winner/loser quick check — intentionally exploratory
exploratory = (
    df.groupby("outcome")[[
        "first_land_turn",
        "first_hire_turn",
        "early_animal_units",
        "crop_strawberry_share",
        "crop_tomato_share",
        "animal_goose_share",
    ]]
    .mean()
    .round(3)
)
print("\nExploratory outcome-group means")
print(exploratory.to_string())
print(
    "\nDo not read these descriptive differences as causal or validated predictive signals. "
    "The project-level paired robustness check found no non-outcome feature that survived all criteria."
)

# Public V1 schema candidate

## Product shape

The current public candidate is one file: `strategy_meta.csv`.

The five-second choice is intentional: a Kaggle user should open one compact table and immediately be able to compare outcomes, openings, economy checkpoints, and resource allocation. A separate `matchups.csv` is not part of core V1 while cross-family support remains sparse.

## Grain

One row per `(episode_id, seat)` from separately published official Kaggle daily episode datasets that report CC0-1.0.

Raw replay JSON is never part of the release.

## Column groups

### Provenance and outcome

- `source_dataset`, `source_license`, `source_date`
- `episode_id`, `episode_date`, `seat`
- `engine_version`, `turns`
- `final_reward`, `opponent_final_reward`
- `reward_margin_vs_opponent`, `outcome`
- `manifest_avg_score`, `manifest_min_score`, `source_score_quantile`

`opponent_final_reward`, `reward_margin_vs_opponent`, and `outcome` are deterministic within-episode derivatives so winner/loser comparisons work without a self-join. The manifest scores describe the episode in the official daily source. `source_score_quantile` records the deterministic sampling position within that daily manifest. None of these fields is presented as a full-ladder rating for the individual seat.

### Economy checkpoints

- `cash_t24`, `cash_t72`, `cash_t168`, `cash_t360`
- `peak_cash`

These retain trajectory information that a single final-money value loses.

### First-event timing

- `first_land_turn`
- `first_hire_turn`
- `first_plant_turn`
- `first_sell_turn`
- `first_animal_turn`

Turns are kept instead of collapsing all events to day-level timing.

### Opening and labor

- `total_hires_actual`, `early_hires_actual`
- `early_plant_actions`, `early_seed_units`, `early_animal_units`, `early_sell_units`
- `early_dominant_crop`, `early_dominant_crop_share`
- `opening_hash_t24`, `opening_hash_t48`

Exact opening hashes are identity fingerprints, not semantic strategy labels.

### Actual resource allocation

- crop tile-turn shares: carrot, melon, strawberry, tomato, wheat
- animal tile-turn shares: cow, goose, sheep

These shares are computed from observed board state across the replay, rather than inferred only from submitted buy/plant orders.

### Broad behavior totals

- `total_market_orders`, `total_unit_actions`
- `market_buy_seed_units`, `market_buy_animal_units`, `market_sell_units`

### Experimental label

- `strategy_family_experimental`

This is the deterministic resource-mix label currently called `strategy_family_pilot` internally. It remains experimental and is not ground truth.

## Deliberately excluded from public V1

- `team_id`
- `submission_id`
- `agent_name`
- `rating_after`
- raw replay payloads
- duplicated final-cash fields
- shared market-price min/max columns already well covered by the closest existing episode-feature dataset

The exclusions keep the release task-focused, reduce unnecessary identity coupling, and avoid presenting fields that are not consistently available from the official daily source path.

## Closest-alternative comparison

`georgymamarin/kaggriculture-episodes` already publishes an `episode_features.csv` with final money, peak crew, total hires, first-land day, planted-crop counts, and market price ranges. It also publishes action-stream hashes separately.

Therefore this project must not claim that final outcomes, hires, crops, or hashes are novel by themselves. The candidate differentiator is the **single-row combination** of source provenance, multi-point cash trajectory, turn-level first-event timing, actual board tile-turn resource shares, semantic opening/action totals, and opening fingerprints.

The machine-readable comparison is written to `reports/v1_schema_comparison.json`.

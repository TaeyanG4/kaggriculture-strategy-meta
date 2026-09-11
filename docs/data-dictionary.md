# `strategy_meta.csv` data dictionary

Current public-V1 candidate grain: one row per `(episode_id, seat)` from the bounded official-daily source window.

The table is deliberately compact. Identity-coupled fields such as team, submission, and agent name are not part of public V1. The categorical strategy family is experimental; continuous features are the primary product.

| Column | Meaning |
|---|---|
| `source_dataset` | Official Kaggle daily Dataset ref used as the source for the replay. |
| `source_license` | License reported by that official source Dataset; current V1 expects `CC0-1.0`. |
| `source_date` | Date represented by the official daily source Dataset. |
| `episode_id` | Kaggriculture episode identifier from the source Dataset. |
| `episode_date` | Episode timestamp carried through the selected source manifest. |
| `seat` | Seat index in the two-player episode, `0` or `1`. |
| `engine_version` | Kaggriculture replay module version. |
| `turns` | Number of replay turns; current source window contains 720-turn episodes. |
| `final_reward` | Final replay reward for this seat. In the validated source window it equals final observed cash. |
| `opponent_final_reward` | Final replay reward for the other seat in the same episode. |
| `reward_margin_vs_opponent` | `final_reward - opponent_final_reward`. |
| `outcome` | Deterministic `win`, `loss`, or `tie` from the reward margin. |
| `manifest_avg_score` | Episode-level average score reported by the official daily manifest. |
| `manifest_min_score` | Episode-level minimum score reported by the official daily manifest. |
| `source_score_quantile` | Deterministic sample position within the daily manifest after sorting by `avg_score`; current rule uses 24 midpoint quantiles. |
| `cash_t24` | Observed cash at or before turn 24. |
| `cash_t72` | Observed cash at or before turn 72. |
| `cash_t168` | Observed cash at or before turn 168. |
| `cash_t360` | Observed cash at or before turn 360. |
| `first_land_turn` | First observed turn on which additional land was unlocked. |
| `first_hire_turn` | First turn with a hire market action. |
| `first_plant_turn` | First turn with a plant unit action. |
| `first_sell_turn` | First turn with a sell market action. |
| `first_animal_turn` | First turn with an animal-purchase market action. |
| `total_hires_actual` | Sum of daily observed hire counts across the replay. |
| `early_hires_actual` | Observed hires during the first 48 turns. |
| `early_plant_actions` | Plant unit actions during the first 48 turns. |
| `early_seed_units` | Seed units bought during the first 48 turns. |
| `early_animal_units` | Animal units bought during the first 48 turns. |
| `early_sell_units` | Units sold during the first 48 turns. |
| `early_dominant_crop` | Crop with the largest share of first-48-turn plant actions. |
| `early_dominant_crop_share` | Share of first-48-turn plant actions belonging to `early_dominant_crop`. |
| `opening_hash_t24` | Deterministic hash of this seat's action stream through turn 24; identity fingerprint, not a semantic strategy label. |
| `opening_hash_t48` | Deterministic hash of this seat's action stream through turn 48; identity fingerprint, not a semantic strategy label. |
| `crop_carrot_share` | Carrot share of observed crop tile-turn occupancy. |
| `crop_melon_share` | Melon share of observed crop tile-turn occupancy. |
| `crop_strawberry_share` | Strawberry share of observed crop tile-turn occupancy. |
| `crop_tomato_share` | Tomato share of observed crop tile-turn occupancy. |
| `crop_wheat_share` | Wheat share of observed crop tile-turn occupancy. |
| `animal_cow_share` | Cow share of observed animal tile-turn occupancy. |
| `animal_goose_share` | Goose share of observed animal tile-turn occupancy. |
| `animal_sheep_share` | Sheep share of observed animal tile-turn occupancy. |
| `total_market_orders` | Count of all market orders over the replay. |
| `total_unit_actions` | Count of all parsed farmer/hand unit actions over the replay. |
| `market_buy_seed_units` | Total seed units bought across the replay. |
| `market_buy_animal_units` | Total animal units bought across the replay. |
| `market_sell_units` | Total units sold across the replay. |
| `strategy_family_experimental` | Coarse deterministic label formed from dominant animal share plus dominant non-wheat crop share. Experimental only; not ground truth. |

## Sampling caveat

Current V1 uses 24 equally spaced midpoint quantiles per day after sorting each official daily manifest by `avg_score`. It is a deterministic bounded **current-meta slice**, not a probability sample of the full competition ladder.

## Outcome-analysis caveat

Winner/loser fields make paired analysis easy, but the current 168-game check found no non-outcome feature that passed the project's combined multiple-testing, effect-size, and seat-direction robustness criteria. Treat outcome associations as exploratory unless separately validated.

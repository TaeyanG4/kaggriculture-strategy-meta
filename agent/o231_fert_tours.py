# o-series build (Claude, 2026-09-15): parent agent/o227_stealth_drop.py sha256 0f3f649d2ab01141 + overlays ['agent/overlays/o231_fert_tours.py']. Apache-2.0; parent notices retained below.
# o-series build (Claude, 2026-09-15): parent agent/o224_v44_race_window.py sha256 8a561fb76918cdba + overlays ['agent/overlays/o227_stealth_drop.py']. Apache-2.0; parent notices retained below.
# o-series build (Claude, 2026-09-15): parent agent/o219_o218_c180_tomato2.py sha256 dca8dcf220324a47 + overlays ['agent/overlays/o224_v44_race_window.py']. Apache-2.0; parent notices retained below.
# o-series build (Claude, 2026-09-15): parent agent/o218_guarded_full.py sha256 ad922382881c6704 + overlays ['agent/overlays/c177_tomato_strawberry_lane.py', 'agent/overlays/c179_early_tomato_plus_v219.py', 'agent/overlays/c180_guarded_early_tomato2.py']. Apache-2.0; parent notices retained below.
# o-series build (Claude, 2026-09-15): parent agent/c171_v42_production_routes.py sha256 007298c195824997 + overlays ['agent/overlays/o215_c171_guard.py', 'agent/overlays/o199c_carrot_switch_price2.py', 'agent/overlays/o206_yarn_sheep_feed.py', 'agent/overlays/o211_fsv5_r132.py']. Apache-2.0; parent notices retained below.
# c171 build (GPT/Codex, 2026-09-15): frozen o182 + public V42 non-YARN production routes; Apache-2.0 notices retained.
# o-series build (Claude, 2026-09-15): parent agent/o162_goose_only.py sha256 26c7f8571e5b84ee + overlays ['agent/overlays/o171e_day6_goose_4.py', 'agent/overlays/o170c_day10_livestock_milk3.py', 'agent/overlays/o174_tet_funding.py', 'agent/overlays/o177_tet_grain.py', 'agent/overlays/o182_v43_overflow.py']. Apache-2.0; parent notices retained below.
# o162_goose_only build: parent agent/o159b_feed_margin06.py sha256 cbcc866ce8f710d62c3f6673c743c714643f6aab32b81beba201b9085f3f887a + agent/overlays/o162_goose_only.py (2026-09-15). Apache-2.0; parent notices retained below.
# o-series build (Claude, 2026-09-15): parent agent/c150.py sha256 9713af1538ccc8e4 + overlays ['agent/overlays/o159_feed_margin.py']. Apache-2.0; parent notices retained below.
# LOCAL OPENING HYPOTHESIS, 2026-09-13. UNTESTED; NOT SELECTED FOR SUBMISSION.
# Only step-zero opening orders differ from c110; upstream notices retained.
# PROJECT DERIVATIVE, 2026-09-12; Apache-2.0.
# Changed: observation_repair=False; tomato_planting_day=None; tomato_shop_gate=2.
# Input allocation: start_day=12, value_cost_ratio=1.5, max_workers=2; repair_actions=None.
# Inventory budget enabled: False.
# Physically funded sale reservation horizon: 8.
# Public V37 parent and every upstream license/attribution retained below.
# EXP-173 isolate opening market sequence inspired by yhay81/shop-router-0911-simple (Apache-2.0).
# Kaggriculture EXP-167 candidate. Not submitted automatically.
# Attribution: thomastschinkel, yhay81, destbreso, aurax7, tetsutani,
# prvsiyan and Dmitrii Gluzdov. Apache-2.0 derivations; notices retained below.
# Kaggriculture v31 / EXP-157, Ahmed Berat Ozer, September 9 2026.
# Selected mechanism: crop_public_order. New independent confirmation is required.
# Public V221B/V224C production/timing lineage: prvsiyan, Apache-2.0.
# Original economics and integration; retained upstream licenses follow.
# Kaggriculture v28 / EXP-154, Ahmed Berat Ozer, September 9 2026.
# Changes: aurax7 day-end storage guard; Dmitrii Gluzdov physical terminal rescue
# adapted to v27, with 64 deterministic simulations. Apache-2.0.
# New action tapes and ordered shop-pair map: yhay81/shop-router-0909, Apache-2.0.
# Kaggriculture v25, EXP-149: Shop0908 production, sale lead, terminal cargo rescue.
# Runtime chassis: Apache-2.0; thomastschinkel, yhay81, tetsutani.
# Routing and public action data: yhay81/shop-router-0908, frozen September 8, 2026.
# 
#                                  Apache License
#                            Version 2.0, January 2004
#                         http://www.apache.org/licenses/
# 
#    TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION
# 
#    1. Definitions.
# 
#       "License" shall mean the terms and conditions for use, reproduction,
#       and distribution as defined by Sections 1 through 9 of this document.
# 
#       "Licensor" shall mean the copyright owner or entity authorized by
#       the copyright owner that is granting the License.
# 
#       "Legal Entity" shall mean the union of the acting entity and all
#       other entities that control, are controlled by, or are under common
#       control with that entity. For the purposes of this definition,
#       "control" means (i) the power, direct or indirect, to cause the
#       direction or management of such entity, whether by contract or
#       otherwise, or (ii) ownership of fifty percent (50%) or more of the
#       outstanding shares, or (iii) beneficial ownership of such entity.
# 
#       "You" (or "Your") shall mean an individual or Legal Entity
#       exercising permissions granted by this License.
# 
#       "Source" form shall mean the preferred form for making modifications,
#       including but not limited to software source code, documentation
#       source, and configuration files.
# 
#       "Object" form shall mean any form resulting from mechanical
#       transformation or translation of a Source form, including but
#       not limited to compiled object code, generated documentation,
#       and conversions to other media types.
# 
#       "Work" shall mean the work of authorship, whether in Source or
#       Object form, made available under the License, as indicated by a
#       copyright notice that is included in or attached to the work
#       (an example is provided in the Appendix below).
# 
#       "Derivative Works" shall mean any work, whether in Source or Object
#       form, that is based on (or derived from) the Work and for which the
#       editorial revisions, annotations, elaborations, or other modifications
#       represent, as a whole, an original work of authorship. For the purposes
#       of this License, Derivative Works shall not include works that remain
#       separable from, or merely link (or bind by name) to the interfaces of,
#       the Work and Derivative Works thereof.
# 
#       "Contribution" shall mean any work of authorship, including
#       the original version of the Work and any modifications or additions
#       to that Work or Derivative Works thereof, that is intentionally
#       submitted to Licensor for inclusion in the Work by the copyright owner
#       or by an individual or Legal Entity authorized to submit on behalf of
#       the copyright owner. For the purposes of this definition, "submitted"
#       means any form of electronic, verbal, or written communication sent
#       to the Licensor or its representatives, including but not limited to
#       communication on electronic mailing lists, source code control systems,
#       and issue tracking systems that are managed by, or on behalf of, the
#       Licensor for the purpose of discussing and improving the Work, but
#       excluding communication that is conspicuously marked or otherwise
#       designated in writing by the copyright owner as "Not a Contribution."
# 
#       "Contributor" shall mean Licensor and any individual or Legal Entity
#       on behalf of whom a Contribution has been received by Licensor and
#       subsequently incorporated within the Work.
# 
#    2. Grant of Copyright License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       copyright license to reproduce, prepare Derivative Works of,
#       publicly display, publicly perform, sublicense, and distribute the
#       Work and such Derivative Works in Source or Object form.
# 
#    3. Grant of Patent License. Subject to the terms and conditions of
#       this License, each Contributor hereby grants to You a perpetual,
#       worldwide, non-exclusive, no-charge, royalty-free, irrevocable
#       (except as stated in this section) patent license to make, have made,
#       use, offer to sell, sell, import, and otherwise transfer the Work,
#       where such license applies only to those patent claims licensable
#       by such Contributor that are necessarily infringed by their
#       Contribution(s) alone or by combination of their Contribution(s)
#       with the Work to which such Contribution(s) was submitted. If You
#       institute patent litigation against any entity (including a
#       cross-claim or counterclaim in a lawsuit) alleging that the Work
#       or a Contribution incorporated within the Work constitutes direct
#       or contributory patent infringement, then any patent licenses
#       granted to You under this License for that Work shall terminate
#       as of the date such litigation is filed.
# 
#    4. Redistribution. You may reproduce and distribute copies of the
#       Work or Derivative Works thereof in any medium, with or without
#       modifications, and in Source or Object form, provided that You
#       meet the following conditions:
# 
#       (a) You must give any other recipients of the Work or
#           Derivative Works a copy of this License; and
# 
#       (b) You must cause any modified files to carry prominent notices
#           stating that You changed the files; and
# 
#       (c) You must retain, in the Source form of any Derivative Works
#           that You distribute, all copyright, patent, trademark, and
#           attribution notices from the Source form of the Work,
#           excluding those notices that do not pertain to any part of
#           the Derivative Works; and
# 
#       (d) If the Work includes a "NOTICE" text file as part of its
#           distribution, then any Derivative Works that You distribute must
#           include a readable copy of the attribution notices contained
#           within such NOTICE file, excluding those notices that do not
#           pertain to any part of the Derivative Works, in at least one
#           of the following places: within a NOTICE text file distributed
#           as part of the Derivative Works; within the Source form or
#           documentation, if provided along with the Derivative Works; or,
#           within a display generated by the Derivative Works, if and
#           wherever such third-party notices normally appear. The contents
#           of the NOTICE file are for informational purposes only and
#           do not modify the License. You may add Your own attribution
#           notices within Derivative Works that You distribute, alongside
#           or as an addendum to the NOTICE text from the Work, provided
#           that such additional attribution notices cannot be construed
#           as modifying the License.
# 
#       You may add Your own copyright statement to Your modifications and
#       may provide additional or different license terms and conditions
#       for use, reproduction, or distribution of Your modifications, or
#       for any such Derivative Works as a whole, provided Your use,
#       reproduction, and distribution of the Work otherwise complies with
#       the conditions stated in this License.
# 
#    5. Submission of Contributions. Unless You explicitly state otherwise,
#       any Contribution intentionally submitted for inclusion in the Work
#       by You to the Licensor shall be under the terms and conditions of
#       this License, without any additional terms or conditions.
#       Notwithstanding the above, nothing herein shall supersede or modify
#       the terms of any separate license agreement you may have executed
#       with Licensor regarding such Contributions.
# 
#    6. Trademarks. This License does not grant permission to use the trade
#       names, trademarks, service marks, or product names of the Licensor,
#       except as required for reasonable and customary use in describing the
#       origin of the Work and reproducing the content of the NOTICE file.
# 
#    7. Disclaimer of Warranty. Unless required by applicable law or
#       agreed to in writing, Licensor provides the Work (and each
#       Contributor provides its Contributions) on an "AS IS" BASIS,
#       WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
#       implied, including, without limitation, any warranties or conditions
#       of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
#       PARTICULAR PURPOSE. You are solely responsible for determining the
#       appropriateness of using or redistributing the Work and assume any
#       risks associated with Your exercise of permissions under this License.
# 
#    8. Limitation of Liability. In no event and under no legal theory,
#       whether in tort (including negligence), contract, or otherwise,
#       unless required by applicable law (such as deliberate and grossly
#       negligent acts) or agreed to in writing, shall any Contributor be
#       liable to You for damages, including any direct, indirect, special,
#       incidental, or consequential damages of any character arising as a
#       result of this License or out of the use or inability to use the
#       Work (including but not limited to damages for loss of goodwill,
#       work stoppage, computer failure or malfunction, or any and all
#       other commercial damages or losses), even if such Contributor
#       has been advised of the possibility of such damages.
# 
#    9. Accepting Warranty or Additional Liability. While redistributing
#       the Work or Derivative Works thereof, You may choose to offer,
#       and charge a fee for, acceptance of support, warranty, indemnity,
#       or other liability obligations and/or rights consistent with this
#       License. However, in accepting such obligations, You may act only
#       on Your own behalf and on Your sole responsibility, not on behalf
#       of any other Contributor, and only if You agree to indemnify,
#       defend, and hold each Contributor harmless for any liability
#       incurred by, or claims asserted against, such Contributor by reason
#       of your accepting any such warranty or additional liability.
# 
#    END OF TERMS AND CONDITIONS
# 
#    APPENDIX: How to apply the Apache License to your work.
# 
#       To apply the Apache License to your work, attach the following
#       boilerplate notice, with the fields enclosed by brackets "[]"
#       replaced with your own identifying information. (Don't include
#       the brackets!)  The text should be enclosed in the appropriate
#       comment syntax for the file format. We also recommend that a
#       file or class name and description of purpose be included on the
#       same "printed page" as the copyright notice for easier
#       identification within third-party archives.
# 
#    Copyright [yyyy] [name of copyright owner]
# 
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
# 
#        http://www.apache.org/licenses/LICENSE-2.0
# 
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
"""Kaggriculture route-replay chassis (pure Python, stdlib only).

A *route* is a pre-computed tape of 719 Kaggle-format actions
``{"farmer": [op, ...], "hands": [[op, ...], ...], "market": [[order, item, qty], ...]}``.
The chassis replays the tape chosen by a caller-supplied ``router`` and wraps it
in small reactive layers (each independently switchable via ``settings``):

    hand_align            pad/truncate hands to the real hand count      (fieldbook_logic)
    weed_repair           DIG a weed that blocks PLANT/BUILD, replay      (tetsutani + task spec)
    sell_lead             sell next step's lots one step early            (fieldbook _lead_sale)
    front_run             sell before the opponent's scheduled SELL       (hook; opponent_plan)
    budget_guard          fund each 72-step block's purchases             (six_day_budget_guard.hpp)
    room_guard            keep shed <= 99 at hour 23                      (tetsutani)
    clamp_sells           trim SELL orders to the projected shed          (tetsutani)
    dead_stock            sell stock the route will never sell            (tetsutani)
    terminal_liquidation  step >= 718: sell the whole projected shed      (fieldbook _terminal_sale)

Engine facts (verified against kaggle_environments 1.32.7, env_1_32_7.py):
  observation["farms"][p] = {"money", "tiles"[y][x], "farmer"[x,y], "hands"[[x,y]..],
                             "unlocked_quadrants", "hires_today"}
  tiles: None (empty) | "LOCKED" | {"kind": WEED|COOP|PASTURE|PLANT, "crop"/"animal", ...}
  observation["private"] = {"shed": {item: n}, "seeds": {crop: n}, "inventories": [{}...]}
  observation["market"] = {"inventory": {...}, "prices": {...}}
  observation["town"] = {"unlocked_shops": [...]}
  Agents act on steps 0..718 (interpreter marks DONE once step >= episodeSteps-2).
"""
from __future__ import annotations

import copy

PRODUCTS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER")
SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50, "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
LAND_PRICES = (1000, 2000, 4000)
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
FRONT_RUN_ITEMS = ("MILK", "WOOL", "STRAWBERRY", "MELON")
LAST_ACT_STEP = 718
PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}

DEFAULT_SETTINGS = {
    "hand_align": True,
    "weed_repair": True,
    "sell_lead": True,
    "front_run": True,
    "budget_guard": True,
    "room_guard": True,
    "clamp_sells": True,
    "dead_stock": True,
    "terminal_liquidation": True,
    # tunables
    "block_turns": 72,
    "shed_capacity": 100,
    "board_size": 10,
    "max_orders": 10,
    "turns_per_day": 24,
    "min_sell_price": 2,
}


# --------------------------------------------------------------------------- helpers
def _get(value, key, default=None):
    """Field access that works for dicts and Kaggle Struct/attribute objects."""
    if isinstance(value, dict):
        return value.get(key, default)
    getter = getattr(value, "get", None)
    if callable(getter):
        return getter(key, default)
    return getattr(value, key, default)


def _int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _step_of(observation):
    raw = _get(observation, "step")
    if raw is not None:
        return _int(raw)
    return _int(_get(observation, "day", 0)) * 24 + _int(_get(observation, "hour", 0))


def _shed_adjacent(pos, board):
    if not isinstance(pos, (list, tuple)) or len(pos) < 2:
        return False
    half = board // 2
    return pos[0] in (half - 1, half) and pos[1] in (half - 1, half)


def _tile_at(tiles, pos):
    try:
        x, y = int(pos[0]), int(pos[1])
        return tiles[y][x]
    except (TypeError, ValueError, IndexError):
        return "LOCKED"


def _is_noop(act, tile, inv, seeds, pos, board):
    """True when the engine will certainly ignore ``act`` (mirrors _apply_unit_action)."""
    if not act:
        return True
    op = act[0]
    x, y = pos[0], pos[1]
    if op in MOVES:
        dx, dy = MOVES[op]
        return not (0 <= x + dx < board and 0 <= y + dy < board)
    if op == "PASS":
        return True
    adjacent = _shed_adjacent(pos, board)
    if op == "DROP":
        return (not adjacent) or (not inv)
    if op == "PICKUP":
        return not adjacent
    if op == "PLACE":
        item = act[1] if len(act) > 1 else None
        if item in ANIMAL_STRUCTURE and isinstance(tile, dict) \
                and _get(tile, "kind") == ANIMAL_STRUCTURE[item] and _get(tile, "animal") is None:
            return _int(_get(inv, item, 0)) <= 0
        return (not adjacent) or _int(_get(inv, item, 0)) <= 0
    if tile == "LOCKED":
        return True
    is_dict = isinstance(tile, dict)
    kind = _get(tile, "kind") if is_dict else None
    animal = is_dict and _get(tile, "animal") is not None
    if op == "PLANT":
        return tile is not None or _int(_get(seeds, act[1] if len(act) > 1 else None, 0)) <= 0
    if op == "WATER":
        return kind != "PLANT" or bool(_get(tile, "watered_today"))
    if op == "HARVEST":
        return (not is_dict) or _int(_get(tile, "yield_units", 0)) <= 0
    if op == "FERTILIZE":
        return kind != "PLANT" or _int(_get(inv, "FERTILIZER", 0)) <= 0
    if op == "DIG":
        return tile is None or animal
    if op in ("BUILD_COOP", "BUILD_PASTURE"):
        return tile is not None
    if op == "FEED":
        return (not animal) or bool(_get(tile, "fed_today")) or _int(_get(inv, "WHEAT", 0)) <= 0
    if op == "COLLECT_FERTILIZER":
        return (not animal) or (not _get(tile, "fertilizer_available"))
    if op == "CARE":
        return (not animal) or bool(_get(tile, "cared_today"))
    return True


class _View:
    """Cheap per-step snapshot of everything the layers read from the observation."""

    def __init__(self, observation, player, cfg):
        farms = list(_get(observation, "farms", []) or [])
        self.farm = farms[player] if player < len(farms) else {}
        self.rival = farms[1 - player] if len(farms) >= 2 and 1 - player < len(farms) else {}
        private = _get(observation, "private", {}) or {}
        self.shed = {k: max(0, _int(v)) for k, v in dict(_get(private, "shed", {}) or {}).items()}
        self.seeds = dict(_get(private, "seeds", {}) or {})
        self.invs = [dict(i or {}) for i in (_get(private, "inventories", []) or [])]
        market = _get(observation, "market", {}) or {}
        self.prices = {k: _int(v) for k, v in dict(_get(market, "prices", {}) or {}).items()}
        self.money = float(_get(self.farm, "money", 0.0) or 0.0)
        self.tiles = _get(self.farm, "tiles", []) or []
        self.board = len(self.tiles) or cfg["board_size"]
        self.positions = [_get(self.farm, "farmer", None)] + [list(p) for p in (_get(self.farm, "hands", []) or [])]
        self.hires_today = _int(_get(self.farm, "hires_today", 0))
        self.quadrants = len(list(_get(self.farm, "unlocked_quadrants", []) or []))

    def inv(self, idx):
        return self.invs[idx] if idx < len(self.invs) else {}

    def in_hands(self, item):
        return sum(max(0, _int(_get(inv, item, 0))) for inv in self.invs)


# --------------------------------------------------------------------------- chassis
class Chassis:
    """Replays ``routes[router(...)]`` with reactive safety/market layers.

    routes         : {route_id: list of >= 719 Kaggle action dicts}
    router         : callable(observation, step, state_dict) -> route_id, called every
                     step; ``state_dict`` is per-player and persists across the game.
    settings       : overrides for DEFAULT_SETTINGS (layer switches + tunables)
    opponent_plan  : optional list of the opponent's expected actions (front_run hook)
    """

    def __init__(self, routes, router=None, settings=None, opponent_plan=None):
        self.routes = {rid: list(tape) for rid, tape in routes.items()}
        self.router = router or (lambda observation, step, state: next(iter(self.routes)))
        self.cfg = dict(DEFAULT_SETTINGS)
        self.cfg.update(settings or {})
        self.opponent_plan = opponent_plan
        self.players = {}
        self.diagnostics = {"layer_fallbacks": 0, "entry_fallbacks": 0}
        self._future_sells = {}   # route id -> {item: [remaining planned SELL qty from step t]}

    # ---- state -----------------------------------------------------------------
    def _state(self, player, step):
        st = self.players.get(player)
        if st is None or step == 0 or step <= st["last_step"]:
            st = {"last_step": -1, "route": None, "router_state": {},
                  "pending": {}, "sell_state": {"due_step": -1, "suppress": {}}}
            self.players[player] = st
        st["last_step"] = step
        return st

    def _route_action(self, route, step):
        tape = self.routes[route]
        if 0 <= step < len(tape) and isinstance(tape[step], dict):
            return copy.deepcopy(tape[step])
        return copy.deepcopy(PASS_ACTION)

    def future_sells(self, route, item, step):
        """Planned SELL quantity of ``item`` in route steps >= ``step`` (suffix sums)."""
        table = self._future_sells.get(route)
        if table is None:
            tape = self.routes[route]
            n = len(tape)
            table = {p: [0] * (n + 1) for p in PRODUCTS}
            for t in range(n - 1, -1, -1):
                for p in PRODUCTS:
                    table[p][t] = table[p][t + 1]
                for o in (tape[t].get("market") or []) if isinstance(tape[t], dict) else []:
                    if o and o[0] == "SELL" and len(o) >= 3 and o[1] in table:
                        table[o[1]][t] += max(0, _int(o[2]))
            self._future_sells[route] = table
        col = table.get(item)
        return col[step] if col and 0 <= step < len(col) else 0

    # ---- main entry -----------------------------------------------------------
    def act(self, observation, configuration=None):
        if len(_get(observation, "farms", []) or []) < 2:
            raise ValueError("incomplete observation")  # factory falls back to tape
        step = _step_of(observation)
        player = _int(_get(observation, "player", 0))
        st = self._state(player, step)
        cfg = self.cfg
        view = _View(observation, player, cfg)

        route = self.router(observation, step, st["router_state"])
        if route not in self.routes:
            route = st["route"] if st["route"] in self.routes else next(iter(self.routes))
        st["route"] = route
        action = self._route_action(route, step)
        raw = copy.deepcopy(action)
        try:
            if cfg["hand_align"]:
                self._hand_align(action, view)
            if cfg["weed_repair"]:
                self._weed_repair(action, view, st, route, step)
            if cfg["sell_lead"] or cfg["front_run"]:
                self._apply_suppression(action, st["sell_state"], step)
            projected = self._projected_shed(action, view)
            lead_available = dict(projected)
            next_sup = {"due_step": -1, "suppress": {}, "r36_debts": st["sell_state"].get("r36_debts", {})}
            if cfg["sell_lead"]:
                self._sell_lead(action, view, lead_available, route, step, next_sup)
            if cfg["front_run"] and self.opponent_plan:
                self._front_run(action, view, lead_available, route, step, next_sup)
            st["sell_state"] = next_sup
            if cfg["budget_guard"]:
                self._budget_guard(action, view, route, step)
            if cfg["room_guard"]:
                self._room_guard(action, view, route, step)
            if cfg["clamp_sells"]:
                self._clamp_sells(action, projected)
            if cfg["dead_stock"]:
                self._dead_stock(action, view, projected, route, step)
            if cfg["terminal_liquidation"]:
                self._terminal_liquidation(action, projected, step)
            action["market"] = action["market"][: cfg["max_orders"]]
            return action
        except Exception:
            self.diagnostics["layer_fallbacks"] += 1
            return raw

    # ---- layer: hand_align ----------------------------------------------------
    def _hand_align(self, action, view):
        """Pad with PASS / truncate the tape's hand list to the real number of hands
        (fieldbook_logic.act). Extra hands would be ignored by the engine anyway;
        missing ones just idle, so alignment only tidies the action."""
        expected = max(0, len(view.positions) - 1)
        hands = list(action.get("hands") or [])
        hands.extend([["PASS"] for _ in range(max(0, expected - len(hands)))])
        action["hands"] = hands[:expected]

    # ---- layer: weed_repair ---------------------------------------------------
    def _weed_repair(self, action, view, st, route, step):
        """If a PLANT/BUILD_* target tile is a WEED, DIG now and queue the intended
        action for that unit; the queue replays on a later step when the unit still
        stands there and its tape action would be a no-op (the displaced no-op is
        queued behind it, so PLANT -> WATER chains survive). A PLANT is only replayed
        when the unit's next tape action is not a move, so the mandatory same-day
        WATER can follow; otherwise the seed is kept. A no-op turn spent on a weed
        is also converted to DIG (tetsutani weed_dig)."""
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        pending = st["pending"]
        tape = self.routes[route]
        nxt = tape[step + 1] if step + 1 < len(tape) and isinstance(tape[step + 1], dict) else {}
        next_units = [nxt.get("farmer") or ["PASS"]] + list(nxt.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            pos = view.positions[i]
            if not isinstance(pos, (list, tuple)):
                continue
            pos = (int(pos[0]), int(pos[1]))
            tile = _tile_at(view.tiles, pos)
            act = list(units[i])
            queue = pending.get(i)
            if queue and queue[0][0] != pos:
                pending.pop(i, None)
                queue = None
            is_weed = isinstance(tile, dict) and _get(tile, "kind") == "WEED"
            noop = _is_noop(act, tile, view.inv(i), view.seeds, pos, view.board)
            next_op = next_units[i][0] if i < len(next_units) and next_units[i] else "PASS"
            if act and act[0] in ("PLANT", "BUILD_COOP", "BUILD_PASTURE") and is_weed:
                pending.setdefault(i, []).append((pos, act))
                act = ["DIG"]
            elif queue and noop:
                _, replay = queue[0]
                if replay[0] == "PLANT" and next_op in MOVES:
                    pending.pop(i, None)          # WATER could never follow: keep the seed
                else:
                    queue.pop(0)
                    if act and act[0] != "PASS" and act[0] not in MOVES:
                        queue.append((pos, act))
                    act = replay
                    if not queue:
                        pending.pop(i, None)
            elif is_weed and noop:
                act = ["DIG"]
            units[i] = act
        action["farmer"] = units[0]
        action["hands"] = units[1:]

    # ---- projected shed -------------------------------------------------------
    def _projected_shed(self, action, view):
        """Shed contents after this step's unit actions but before the market runs:
        PICKUP removes, DROP/PLACE(non-animal) near the shed adds up to capacity
        (fieldbook _projected_shed / tetsutani projected shed)."""
        cap = self.cfg["shed_capacity"]
        proj = {p: view.shed.get(p, 0) for p in PRODUCTS}
        for k, v in view.shed.items():
            proj.setdefault(k, v)
        total = sum(proj.values())
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        for i in range(min(len(units), len(view.positions))):
            if not _shed_adjacent(view.positions[i], view.board):
                continue
            act = units[i]
            op = act[0] if act else "PASS"
            inv = view.inv(i)
            if op == "PICKUP" and len(act) >= 2 and act[1] in proj:
                qty = min(proj[act[1]], max(0, _int(act[2]) if len(act) >= 3 else 1))
                proj[act[1]] -= qty
                total -= qty
            elif op == "DROP":
                for item, held in inv.items():
                    take = min(max(0, _int(held)), max(0, cap - total))
                    if take > 0:
                        proj[item] = proj.get(item, 0) + take
                        total += take
            elif op == "PLACE" and len(act) >= 2 and act[1] not in ANIMAL_STRUCTURE:
                item = act[1]
                take = min(max(0, _int(act[2]) if len(act) >= 3 else 1),
                           max(0, _int(_get(inv, item, 0))), max(0, cap - total))
                if take > 0:
                    proj[item] = proj.get(item, 0) + take
                    total += take
        return proj

    # ---- layer: sell_lead / front_run suppression ------------------------------
    @staticmethod
    def _apply_suppression(action, sell_state, step):
        """Remove from this step's SELLs the quantities already sold a step early."""
        if sell_state.get("due_step") != step:
            return
        remaining = dict(sell_state.get("suppress", {}))
        kept = []
        for order in action.get("market") or []:
            order = list(order)
            if order and order[0] == "SELL" and len(order) >= 3 and remaining.get(order[1], 0) > 0:
                removed = min(max(0, _int(order[2])), remaining[order[1]])
                order[2] = _int(order[2]) - removed
                remaining[order[1]] -= removed
                # A zero-quantity order keeps later market race slots intact.
            kept.append(order)
        action["market"] = kept

    @staticmethod
    def _add_sell(action, item, qty, max_orders, merge=True):
        market = action.setdefault("market", [])
        if merge:
            for order in market:
                if order and order[0] == "SELL" and order[1] == item:
                    order[2] = _int(order[2]) + qty
                    return True
        if len(market) >= max_orders:
            return False
        market.append(["SELL", item, qty])
        return True

    def _sell_lead(self, action, view, projected, route, step, next_sup):
        """fieldbook _lead_sale: when step % 4 != 0 (no town consumption between the
        two steps) sell the lots the tape plans to SELL next step now, for products
        other than WHEAT/FERTILIZER we already hold, and suppress them next step.
        Skipped at the last step, at shop-unlock boundaries and if a SELL for that
        product is already queued this step."""
        cfg = self.cfg
        nxt = step + 1
        unlock_period = 3 * cfg["turns_per_day"]
        if nxt > LAST_ACT_STEP or nxt % unlock_period == 0 or step % 4 == 0:
            return
        tape = self.routes[route]
        future = tape[nxt] if nxt < len(tape) and isinstance(tape[nxt], dict) else {}
        planned = {}
        for o in future.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3 and o[1] in PRODUCTS:
                planned[o[1]] = planned.get(o[1], 0) + max(0, _int(o[2]))
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for item in PRODUCTS:
            if item in ("WHEAT", "FERTILIZER") or planned.get(item, 0) <= 0 or item in already:
                continue
            qty = min(projected.get(item, 0), planned[item])
            if qty <= 0 or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    def _front_run(self, action, view, projected, route, step, next_sup):
        """Hook: if ``opponent_plan`` (their expected tape) schedules a SELL of
        MILK/WOOL/STRAWBERRY/MELON next step, sell what we hold of it now (before
        their supply depresses the price) and suppress our own SELL of that quantity
        next step. Bounded by our own remaining planned sales so it never dumps."""
        cfg = self.cfg
        nxt = step + 1
        plan = self.opponent_plan
        if nxt > LAST_ACT_STEP or nxt >= len(plan) or not isinstance(plan[nxt], dict):
            return
        already = {o[1] for o in action.get("market") or [] if o and o[0] == "SELL" and len(o) > 1}
        for o in plan[nxt].get("market") or []:
            if not (o and o[0] == "SELL" and len(o) >= 3 and o[1] in FRONT_RUN_ITEMS):
                continue
            item = o[1]
            if item in already or view.prices.get(item, 0) < cfg["min_sell_price"]:
                continue
            own_next = sum(max(0, _int(x[2])) for x in self.routes[route][nxt].get("market", [])
                           if len(x) >= 3 and x[0] == "SELL" and x[1] == item)
            qty = min(projected.get(item, 0), max(0, _int(o[2])), own_next)
            if qty <= 0:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"], merge=False):
                break
            projected[item] -= qty
            already.add(item)
            next_sup["suppress"][item] = next_sup["suppress"].get(item, 0) + qty
        if next_sup["suppress"]:
            next_sup["due_step"] = nxt

    # ---- layer: budget_guard --------------------------------------------------
    def _block_requirements(self, view, route, start, end):
        """Planned purchase cost and item reserves for tape steps [start, end)
        (six_day_budget_guard.hpp calculate_six_day_requirements)."""
        tape = self.routes[route]
        budget = 0.0
        seed_bal, item_bal = {}, {}
        seed_need, item_need = {}, {}
        hires_by_day = {}
        quadrants = view.quadrants
        for t in range(start, min(end, len(tape))):
            a = tape[t] if isinstance(tape[t], dict) else {}
            for u in [a.get("farmer") or ["PASS"]] + list(a.get("hands") or []):
                if not u:
                    continue
                op = u[0]
                arg = u[1] if len(u) > 1 else None
                qty = max(1, _int(u[2]) if len(u) > 2 else 1)
                if op == "PLANT" and arg in SEED_PRICE:
                    seed_bal[arg] = seed_bal.get(arg, 0) - 1
                    seed_need[arg] = max(seed_need.get(arg, 0), -seed_bal[arg])
                elif op == "FEED":
                    item_bal["WHEAT"] = item_bal.get("WHEAT", 0) - 1
                    item_need["WHEAT"] = max(item_need.get("WHEAT", 0), -item_bal["WHEAT"])
                elif op == "FERTILIZE":
                    item_bal["FERTILIZER"] = item_bal.get("FERTILIZER", 0) - 1
                    item_need["FERTILIZER"] = max(item_need.get("FERTILIZER", 0), -item_bal["FERTILIZER"])
                elif op == "PLACE" and arg is not None:
                    item_bal[arg] = item_bal.get(arg, 0) - qty
                    item_need[arg] = max(item_need.get(arg, 0), -item_bal[arg])
            for o in a.get("market") or []:
                if not o:
                    continue
                op = o[0]
                item = o[1] if len(o) > 1 else None
                qty = max(1, _int(o[2]) if len(o) > 2 else 1)
                if op == "HIRE":
                    day = (t - start) // self.cfg["turns_per_day"]
                    hires_by_day[day] = hires_by_day.get(day, 0) + 1
                elif op == "BUY_LAND":
                    extra = quadrants - 1
                    if 0 <= extra < len(LAND_PRICES):
                        budget += LAND_PRICES[extra]
                        quadrants += 1
                elif op == "BUY_SEED" and item in SEED_PRICE:
                    budget += SEED_PRICE[item] * qty
                    seed_bal[item] = seed_bal.get(item, 0) + qty
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    budget += view.prices.get(item, 0) * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
                elif op == "BUY_ANIMAL" and item in ANIMAL_COST:
                    budget += ANIMAL_COST[item] * qty
                    item_bal[item] = item_bal.get(item, 0) + qty
        for day, n in hires_by_day.items():
            first = view.hires_today if day == 0 else 0
            for k in range(n):
                budget += _fib(first + k)
        return budget, item_need

    def _budget_guard(self, action, view, route, step):
        """At every block boundary (step % 72 == 0) make sure cash + the value of
        stock the block already plans to sell covers the block's purchases (hires,
        land, seeds, animals, products). A shortfall is covered by extra SELLs of
        unprotected shed stock, highest price first; SELLs are moved in front of
        the buys so the money is there when they execute."""
        cfg = self.cfg
        block = cfg["block_turns"]
        if block <= 0 or step % block != 0:
            return
        budget, item_need = self._block_requirements(view, route, step, step + block)
        market = action.setdefault("market", [])
        existing = {}
        for o in market:
            if o and o[0] == "SELL" and len(o) >= 3:
                existing[o[1]] = existing.get(o[1], 0) + max(0, _int(o[2]))
        cash = view.money
        for item in PRODUCTS:
            planned = max(existing.get(item, 0), self.future_sells(route, item, step)
                          - self.future_sells(route, item, step + block))
            cash += min(view.shed.get(item, 0), planned) * view.prices.get(item, 0)
        shortfall = budget - cash
        if shortfall <= 0:
            return
        candidates = []
        for item in PRODUCTS:
            price = view.prices.get(item, 0)
            if price < cfg["min_sell_price"]:
                continue
            protected = max(0, item_need.get(item, 0) - view.in_hands(item))
            avail = view.shed.get(item, 0) - protected - existing.get(item, 0)
            if avail > 0:
                candidates.append((-price, item, avail, price))
        candidates.sort()
        added = False
        for _, item, avail, price in candidates:
            if shortfall <= 0:
                break
            qty = min(avail, -(-int(shortfall) // price))
            if self._add_sell(action, item, qty, cfg["max_orders"]):
                shortfall -= qty * price
                added = True
        if added:
            sells = [o for o in market if o and o[0] == "SELL"]
            others = [o for o in market if not (o and o[0] == "SELL")]
            action["market"] = sells + others

    # ---- layer: room_guard ----------------------------------------------------
    def _room_guard(self, action, view, route, step):
        """tetsutani room_guard: at hour 23 the end-of-day drop pushes every unit's
        inventory into the shed and overflow is destroyed. Estimate the shed after
        this step (stock + carried + harvest/collect - feed/fertilize/place + buys -
        sells) and, if it exceeds capacity-1, add SELLs preferring products with no
        future planned sale, then highest price."""
        cfg = self.cfg
        if step % cfg["turns_per_day"] != cfg["turns_per_day"] - 1:
            return
        cap = cfg["shed_capacity"]
        units = [action.get("farmer") or ["PASS"]] + list(action.get("hands") or [])
        carried = sum(max(0, _int(n)) for inv in view.invs for n in inv.values())
        produced = consumed = 0
        for i in range(min(len(units), len(view.positions))):
            tile = _tile_at(view.tiles, view.positions[i])
            a = units[i]
            if not a:
                continue
            op = a[0]
            if op == "HARVEST" and isinstance(tile, dict):
                produced += max(0, _int(_get(tile, "yield_units", 0)))
            elif op == "COLLECT_FERTILIZER" and isinstance(tile, dict) and _get(tile, "fertilizer_available"):
                produced += 1
            elif op in ("FEED", "FERTILIZE"):
                consumed += 1
            elif op == "PLACE" and len(a) > 1 and a[1] in ANIMAL_STRUCTURE:
                consumed += 1
        market = action.setdefault("market", [])
        planned_sells, planned_buys = {}, 0
        for o in market:
            if not o:
                continue
            if o[0] == "SELL" and len(o) >= 3:
                planned_sells[o[1]] = planned_sells.get(o[1], 0) + max(0, _int(o[2]))
            elif o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                planned_buys += max(0, _int(o[2]))
        shed_total = sum(view.shed.values())
        fillable = sum(min(view.shed.get(it, 0), n) for it, n in planned_sells.items())
        needed = shed_total + carried + produced - consumed + planned_buys - fillable - (cap - 1)
        if needed <= 0:
            return
        priority = sorted(PRODUCTS, key=lambda it: (self.future_sells(route, it, step + 1) > 0,
                                                   -view.prices.get(it, 0), it))
        for item in priority:
            avail = max(0, view.shed.get(item, 0) - planned_sells.get(item, 0))
            qty = min(needed, avail)
            if qty <= 0 or view.prices.get(item, 0) < 1:
                continue
            if not self._add_sell(action, item, qty, cfg["max_orders"]):
                continue
            planned_sells[item] = planned_sells.get(item, 0) + qty
            needed -= qty
            if needed <= 0:
                break

    # ---- layer: clamp_sells ---------------------------------------------------
    @staticmethod
    def _clamp_sells(action, projected):
        """Clamp against a sequential stock upper bound, retaining market slots.

        Earlier BUY_PRODUCT orders can fund a wheat wash's sell leg. Their full
        quantity is an upper bound; the engine enforces actual cash/capacity.
        Removing empty orders would change the later lockstep market races.
        """
        avail = dict(projected)
        kept = []
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                have = avail.get(o[1], 0)
                n = min(_int(o[2]), have)
                n = max(0, n)
                avail[o[1]] = have - n
                kept.append(["SELL", o[1], n])
            else:
                kept.append(o)
                if o and o[0] in ("BUY_PRODUCT", "BUY_ANIMAL") and len(o) >= 3:
                    avail[o[1]] = avail.get(o[1], 0) + max(0, _int(o[2]))
        action["market"] = kept

    # ---- layer: dead_stock ----------------------------------------------------
    def _dead_stock(self, action, view, projected, route, step):
        """tetsutani dead_stock: stock beyond everything the rest of the route still
        plans to SELL is dead; sell it now when price > 1 (on day 29 everything not
        already in this step's orders is dead). Highest value lots first."""
        planned = {}
        for o in action.get("market") or []:
            if o and o[0] == "SELL" and len(o) >= 3:
                planned[o[1]] = planned.get(o[1], 0) + _int(o[2])
        day = step // self.cfg["turns_per_day"]
        extra = []
        for item in PRODUCTS:
            have = projected.get(item, 0) - planned.get(item, 0)
            if have <= 0:
                continue
            surplus = have if day >= 29 else have - self.future_sells(route, item, step + 1)
            if surplus > 0 and view.prices.get(item, 0) > 1:
                extra.append(["SELL", item, surplus])
        extra.sort(key=lambda o: -view.prices.get(o[1], 0) * o[2])
        action["market"] = (action.get("market") or []) + extra

    # ---- layer: terminal_liquidation -----------------------------------------
    def _terminal_liquidation(self, action, projected, step):
        """fieldbook _terminal_sale: on the final acting step (>= 718) replace the
        market orders with a SELL of the whole projected shed."""
        if step < LAST_ACT_STEP:
            return
        action["market"] = [["SELL", item, qty] for item, qty in projected.items()
                            if qty > 0 and item in PRODUCTS][: self.cfg["max_orders"]]


# --------------------------------------------------------------------------- factory
def make_agent(routes, router=None, opponent_plan=None, **settings):
    """Build a Kaggle ``agent(observation, configuration)`` closure that never raises:
    a failure inside a layer falls back to the raw tape action, and a failure even
    before that falls back to PASS (with hands padded when possible)."""
    chassis = Chassis(routes, router, settings, opponent_plan)

    def agent(observation, configuration=None):
        try:
            return chassis.act(observation, configuration)
        except Exception:
            chassis.diagnostics["entry_fallbacks"] += 1
            try:
                step = _step_of(observation)
                player = _int(_get(observation, "player", 0))
                tape = chassis.routes.get(chassis.players.get(player, {}).get("route"),
                                          next(iter(chassis.routes.values())))
                if 0 <= step < len(tape):
                    return copy.deepcopy(tape[step])
            except Exception:
                pass
            try:
                farms = _get(observation, "farms", []) or []
                hands = _get(farms[_int(_get(observation, "player", 0))], "hands", []) or []
                return {"farmer": ["PASS"], "hands": [["PASS"] for _ in hands], "market": []}
            except Exception:
                return copy.deepcopy(PASS_ACTION)

    agent.chassis = chassis
    return agent


import base64
import json
import zlib
_PAYLOAD=json.loads(zlib.decompress(base64.b85decode('c-ri}U9TiZvLyCj_<SBJKPyvjJ;T}=VoCOZY;Iw7F&JD)S6Dz;LAbkb3;lO>_sOh}2y-*@$ZGOlXn_G(Q(dPjBGMzm-Q3*#e|-19{qukOm+$_UfBGNa{h$B*umAO5{`K?A@Ba4T*I&Q;``dT_<)8oW|Kq=Xe&h4Y|N77W`hWe)fB*dYpT7IkZ~yrpfBWU*_rLx5(|2#*UH^Ld@cF;p@b|ZW`tH}uk3W|0MIZnB|NHj%n?Ha2<<no|AGN=E`tmP-{o$9(ckYWXU-RMTAAb7q<p=)!@%r6cU%mb7UoV%xeffuC)W3fG?RnIn7w?BZ|Ht3{wtdx?FWOe~KE=mZ&!2vrbMZ^J555oO=_en)j{Vl3e*59a@Bi`nBcFczGIi(2-WT=h$BJ)}6a4YRpD)Jzs^?$)DgK@7<=0PNU;O!ln9}x1chzoRT&{b)7k<55zW@C1KV5$O_%kq(a=rKnKF|5*Pq%Li-YK4r8d6sdX<t}iO5oS_p<O?Gy8KeU`npVH+5f|rkv#pv{g3b8yf3z8tJW0X?cwQnZ%;H{>-%S(S1A3^YiqL>w*Juj`n5dar!O+s|Nd|FetP=d{T#05y?w#M@9jq<Sor;Pc^pAyP~PuW>s>$YdYQ}LSIaykmYF^8dbx{Fzhd3Nb7t%Q{^|4&m#)IMS@>T6ELm^8(b!d3PY^6DxIn()f|3Wi4M6>DVnOfU?JOv`k`66s`BSMcCSO;)X!3=g7di4UwVwm7Kkyj!4O0#jzSVGJ--osRoAE96{d@b{?Vp@4`S|0Hmp^~{$A7r|^67^kfB0X^BkuN1@PiqL7x?kPckZ4+@iyFdThQ|G(a-xm3S6qo<?^9?!uPARbX1)PE%E}R)#Wn{ei}^KIcxUaSO*v3IciKW{+((i+s>8y*L<5{g8h4Fytk9)-L_sl+WYBn<g5<%-2po%zx5%uvWDB`(6f2*O;<nR|2dTWZT~hZM5;R6CFCUUTZ*S>8>_Eg7HG4JD{>aqz07`3Uit_KV&5n2f-G<mb{<|{gpkPb*{iuZ1gX^oZsM`gTINc^`Gc!@)MccDm6JzsFBtCrg@66<%YSOaGsr66te_?MvX=Wc>;qw}{Tv?PAt#uXKJr2H22StO9S}QH@$&{Z#fTFRx9C8D1kX7JezY~12|a@WekhlfeIY=>H={6~6Ip<IoYD~?+v9gaBoeO4kcJ|pFT#=})~j45AoNDWja;Pz6X<{Tx02`Dt9}Q;MD+y|y=Z$3;K<0_y!D#b1HP}t(<Re(Nvda2Mdu2OMt9w_r44`2Jg0h&_?}Ipwe_|4n7P8!DzmcYRlpK>_g7@8+m74H!7r8*+z_wzOVHdblS#OY+(7ju=zTXt4VxUH!T%|Ca6pe}h&-a>jwOnlTIMhO@e)jecY1&u_#5N)a}6E@^TO`m8}e7=_uJ2AUtExgB)`^h?E|mP_@NdzF5;@B-MZ<JTjy98%kaDka-x3FH+Hj{ysO*pwNMNRk=1J)CvV!kt0Il|T9_pES=&G-@O>qYk@7(R2-4tJr7xG;ngdsadsQ!XXlqX-N}IGeDCioe88bH(LxPXn6Qwz|)?)&I0mMqcMBZL&KTl5*Wm%~yIfs0`2LlTM{Hz1XOafejA2M(rC;7_0&mDLkg-^_az?AjZ9aw$xJKz8E@o!nr1cU%nJDkOV&|`V>)}NQ##`eIRF9(mOaQ=FgPrm=+--RF9WA;tKm~PAfg41RHIyj}^?0FGtcqn^!`{R0vj{B(*>B+j?$RZ<n<gn9sJBsR+XhQgNk+Ej9-Y3n?DcJrG_xG=#e)(|y)8&_6{xh&`6db7EJ2o)@P>38{f+|)co)5G4-1&OMx7#GfjPqx&mtDQP{@llZe8w3!#hsD+Q&!3qJouO3EHP2{(Foc+7lv*(f|ikm`e)o`m<JQw5T9(I*#+}C#^GzqYm4%_RKc9({5T~s$Wvg~dq`&vyqIzb_va2XCz3y1jPQ0%8qDj|7Q20Mh!nj+UjUs8xt;j9GeUppt&y@`@6Fmn08_93P0jP}zJC1p`9HJahwp&&_6K+X59LwVAt>W}GN?H4xmBNjK0Llx6{`2YPDUR0r4Oc}T%Ow(1et>tDtv47w4?4I=K~xE!UtiG#BpJO?^sjX!6@r69hBLEaJ+x*#dQY>0#qvIKAD9_oqJutf~2PuOU&SVe5+o^L>Y8725>w%L=RR69hQT<`5{X^P;fhx^nAlnsjE-r4}*<IGZnJpR2Ry?!P6b64nOovi}TJ52Hq?_2a5^04{4KIe5<d|*{~`n^s3S58p;4bU`%(tptT22X>eJW!p?#x#TYqcD?a#=xsZ+40@IMwC-Rg4;re&~S%MP+F-ThWTkk%}u-a8VJDPd?y`CN3ba9B7pda)vjuG2(RZ&p(b`IoI9vwAt3futnn1cP}srP?x!K5qSv<|13@1)cJ{>_E5j%3|Zh;)q^Kb#;Je#_eNoCfc(yLzt=t~?O+7c79Ierx@tBy8Opfz{4s91ycOt9h5YLxGWwm4D)h5=#->jH|wP;@hTPGr>k=YjV$s6@kk=$_lA=XgJn00{4g5g<x+O6`Vf)4MJkUP2I;4uak5o={<^ml!`&AOFZlUJ8MLD)cbjjD#5~n@dVV}r_^P*YhIqWMev@ifMDST8qs|V`uV`F*@r|U2x~S~^xd}Eh<c391A^fnO8_TA*O;T7!Ilz_2+kI~XR-S<u#WPVY`qU@DKI<?yv1+gL|_cm0=)pLx_M&p74s3K11ZZg60Y$}^J@pADR3ZCEy^b{5>0^}=A1mmuk7*y|9IOYF)G{0nc(Q|<CwvM)+?48#m(zMKYdR*ZujX=Km7O~w}h1@sl+t)_pj;tFex>ofcd71noH!=dB8fw2hih60W}OZ?thHr6RjKxCDSQSTEWY8#_T?&a<8@k;^-=_w-0BGGb~P~LUV2c%PE50P!NDJdAy;$M5c}>S!S_RSmikQ5i$`-PJ^YYqi!AgrczRQD!fmrt7id@2_ck9$4X!=eCm7B!R;H^tjUm$JS7bsM&0g10)#5HN+nF#vP|`EcuZi&Tt~b{9;ens0sZ<a@MOZ800dsW%H->c1pHJn|L^wC?@!=mGyveoo214!Dm@(8h4vdMf06As;~x(TC4rhWq8_D7Z2P}A@<DNOEW8uhnEVk)U1{i~C4Sptm!emQdvUl*{9C8)+IXHIJELivVciIOT9qEoGx;-!R<g9SdgB>m=^1ae%u;$PpGRF<yHo|Zk9DM7A1j(GBoq~3ajgoqlmu{7IMocafH>)5hJrQnm-Nq^(SUdpyR|nzs@Q<vHpU7xS7<)b=c$@lK;{4d(djdjc;u>;fmuG$4;F(h!GxAvR4Z$4Ecps3@*>~vNlvN26rS~s3>1Qst4$rJ#9q<ZfszwLc?B<_B4hqU2GjEaGjlj>j_S5Z3o;!*<fxm7)DUXlUS7FiRq%Pw?)(f{H*X~#J5nAW_2TFv5kD-=^;@B=Rf)PL2(z%B$<2)u5kbw=jT3%mR+FJcw0Op6P^)<KW<0lBocTi1Z}6&&qGTwyTdU_wWAQN$Tr<$dA69<&a@Hw%!8Q=T?M3IozkK}o>qREhhQutA+O0I8of_ohp}Zex*!cU*2%J4W=*M_<?f?iD6%x4K*ZqLv5-xdV^#}a^kR_0$g0#I9Rpl3=&*B3e=u)Whk^0FX3vwZ3)6#=8;@K7r2ugT0i!T@e=SUSKM}<pKY9K>2XWH7v&4`$e`410&fH&62&*drVu5|zApt!3VFkK+@2lPvTYPd;r-+S+kyw@%`?5Dr`&0QY{4Ynwsxp&U<V2{nc>oe2}6x5<oQ_?f5doS0g&6FqWj_}A>?@o)Hl+8h}`Az$5<XoSaOio5!=OBV}@4X!I&mT((9O=W?RHkkHjGKKjff%lFQ4F2iX-rfG96TA}@~*{!@rt@x_EZIhBQDiLNJMR*y70Ym<B@9RtFH8Oo<w-C7|EMEQ4pNv_XF@Y<ig-+Yb$`Ds2Q;E<9(=WGo8PF)cZW|ryff^!x~LcCP$lBzOUR1nC~FgsFQg?U1=>gTj6fe8u4ZdZ!c?!TU2_uk49A{7B61#9GtegRKKhGH;@bckQTPEdhj|ga>a}iII2!~;jRVP&yYiq5~WB8!DCs5cHoQ40&Vb-WH)3~MJNdxWNE5*n5cSI%&UcyD&4|52mN^Pfs0pbgbi^ig)E1P2_q?H7%ed(tbqHyCQryh3Fy^=Hnvo0B<kcOXTgr;(!1^C%DY}>ea_Yzv5!#@w-`R&C)=M%=jpdY#8JU+!gE0Kb&SexD-`)g##&+dfG6ea$eePHmDFA)0OB+hu|uH*^Uz8qT#wZb0Nh+r;b~iGA?G3mb6YPb!-MoY)AKskI@Cwl4Ok9IGGIYC?+{j>e3Hmrp4sgbmOd-*ghk!>=3s?w>XeuJsa;%*)2{qILlRl-RUM3AkMjc-slhw|UaJuxOsdAJo6j-U*Dwy`&5G~iHbv@Xt!nI?OukM{#+~ZklvIeWTxu_uzsjaU__z)`JGQjEY@;Pw%^>B!#?K%nKW7%u)nNpcUXJHroXf{l6PP{FJ`0)CKsT~EAgf?(%A+U2zXg`jIUg`hiuj?KIp~A5QZSV@VoKmt5jWGz3vAiiKg5I%s%nv0hMKLQ7{egT<bRUgBtib=R#uRS2fUgDDpkZJKyjG@E%XP~^p&yI|Kt-?p*@3egO+X8+?VTX`d!#YC7oB&61;KKOJib(0d5K6de}tY`C03Po>4T>Wh8xDu0`wYGA=+fE^BRmO&Ur`r4qN{BtK7H=WeP2gMgbk$)PG$D)0crzWNXWBWvnV4Hm^Vx`+aqti*b`y@7<MCk3YT$6qmayMLw%G-=Jt%j(2H5uQ;fPbDXsQ~<%XTmMEq#<+ibZco@I$I?M&JklVGF3Uaq9T6wx8>II^j!E`VXXAbu8=-}%&>l0Q5O02245>9f>U?v&FEBI&^V3ooy-poAw!g6|Xix$o8vmG1kgGB|D$_upfDsSpyhch079|H!9=XwPWkm{zsV9zE$w?xrfPjYy*1}fZv)hLSq!F;A^nvcna8vM^nb&ctY2+){@!pNhP+MF>7pP#7X~i_*POzK<&ETh`&tTgP^*eS>iiwu!D<e;LWRkpjT@uR-Rf?bQ0-7&~dM>BO=q0wPva@Z2t=rj?nl@L?B^ETQ1ah)EEt&Ky2|<HzlJ2pS7sc`NBE@6BFH`iI9yKZKg5{i0r-3FYjVXFGhUMZBUXo8*gMExP#;QJfa)Pgn2rHS<=U)MUO0P=F?49y@n%?n+;JqFI2a}jb8g320Q@&DKF*tU^D$-u0Md0UQy)X<c&tbrMr@>=_dvDcPL1Sd|r+OtsAY_l9X+~p^_oY&yzcNl#oiNS>J49pmiY}xYBw~P#rY#Sd7ALXO3QV+$A!HmNomR#aspVz>#70VZR8woS&(dAl&nna0vc>fyOw{?1Sq#m36|8&&U>Fda*AR^>dR-@XP}9A-__499jNSJRKPW*}FDCTb-J!Vi-iCTfK*}6TmM!BFB{bm9rBTqsk?sh|d;=7-0SKYpBCg52wx=p*v|QwO=xw#Uy<j%9JhC(F9?E7o(@GGK&Jq(J1CSxZ^`)^T#R9|U%WMyQG!=PKm{OGfxa1$dWy9fS;~YC;#+RYlv9ngeBRAX9`cTGkc7OU&>&5WY#Em|E1VrAaujkt4|A@M7Z$a!P0^U(2TQ7h4%jS3f!9-m`0E{SvfnRUw0rJRpta2u6)vCHp9WYj(d#+`!^!&UWr6v4AH4a^YB2MRIO2bYOx9XbI(n89hn$mQ+90h3@RmaA)>;=W;s<ZHb3uHGZuGKD7izX_2?aS54Gc~7t!87;pa$}Cky>*{(@fhxxkWOSJj*(u>Yur&p+=ykVo*leQXNiO#!Fs+UFRuOxpYeTh-G|zgpVtC(kUUny;77o(f=bP%y0Hy__(b4Co`+40mXw^K24M9=Vo1-!Ofzfj$EP61qs2Eo1Kq+VB}kh*q3!6J$tz-1THuy`o0@A3DYjIf)W^NAkMjKwe*yc)68CBFOXy~1fxlEzYbz$SC1{?P$L%IAjvmn@^yTUC=ScwWAA1(9<Q2}VN&^qjdlG!@Ca|3zyehvh6EFl~<F4SNLcwCXgZ|O)zA`%o*a>`avc{-E|4P&V=FPb%+5rl&-+dhg<f5!m#@s8FoHJYHQEn-_;#kxRm*5_2I4D5seza<cJ^Vxzf;Dj2xNIsX4A^PF!~hedACMFP*G!^i4pHjM76UK^1ttOvhF!%gS;c(O3c;@gwp%AEc8T5D5f$j-Zo(H*NRWb2SV?(9h)k8Rt|m4DD|*#4q`^jW4>p#718XlR4FZzTi61aRmG2R?F7?i3cJ=}f^(yPzu}^9xogJlvMxT}EBC+k-M-4DD5<<V{D!Q?`L#;SUC}>?*vE0<lAKd3rOo37kiHeA>{EccF9<7J{&9m0WoT89{foC8UmlWerfzy~<J@%wH7E@TF-(bxEglLZmy=_)=s-Tj^^T?=Y9lW8kFZbwtgR`9f?j_yh0h5lVqQ^trZ&y%H%R!hIFe}361x*yc_I<lnAO__M&{^y9F?QsT9nPd3^Pb-J1=Gj@3z|n|_!=R)cR9f0co{$AWkn1LwvKAH@lD|uQ%#Kl3UyIKMYGTa4FQS%D+m>p%g+^GW3=fiQ|4xHWaE12Aki#N3(1RVE7rTzDA1pR7`$b0ESmw(IQF@)FY$}ixLARyqc`3b%$45CIfeg$E3PHW>?hFLprAUkbjmQJ^oedi`icU682hr~OY1_9v9O$iVneM#eJnss#Q+BVj7fLGUfz)Fu*Ukql(E?x;ACV~)}#;9DAt5&5((*fC#bMY3LlK@xTEMd(`aK2oLdcDiGf8t6|>Mqlny&<NgKer8Hbd-Z?G%d^bS~4d5Tq0Ga*OmD+V2U2>7OqqL4ZhVQG9f_n2V8IIWSbvkn<rrpSqKg>G6}o=P@kgzyL+6+#_Ul)m<mRRd-J?wd`3gWv>p|D_NV=CZ#b4re5w%KIE51cs&`2ANnYmxwkz4XSVN?^3UD-TaEQV3P{3N+}QE7$(=F{zplI+5hB@(pSSP>qQbojXxB^s5cRa(w`FyQ8RF}YQb+&XQn*fedVKc5vw;mOIJqeGTHw;MG;}oi~1LYxQT&;>Q(Egm<$b7{3RvYdPst<54n%N_7qrGQLpf=645lCF(us`S_P-7@N{7aL?wl!NJ(rm2TC=!{9uRWKDl3)Y+=S}ABhJ}du1HfbCf09tT~nl=^%H7D4{h{lxb3&Ayf&E{+bp{lV~U7T2o*hzzy<9<9w_}E(_g~a!G?Sdj{Y)$XSYg$YtPts2P{zy;kM{kBnJAOJm(U<M3*4Y8GhhPNQ^2z`Ab9Mx%xRyCXygA)p3dBMr$&bPmuq7d6!-rT`30GvD3<l1fJKLYF~c77#cykiHW`j69j)IhbZ&rDlz8!J?BLB;`bPsx^VQ&P||V9f>%cYL-!-k(0{Fk;Xh5*yF*5O-|MGNf$9b#t%H_!cIKDdagcF+PYS`FqOfzJ0xQ%DGl#C>;y;-A~yI#(HPlt!C*>2jDhDFNL+Q3KPjOVu>PZ#0O18owcBRMeOUTVP)M*TGOvq$Ds+sg0U{+n^uQd|(^Mr<y|#9lKkaRNL=0Q`!Dil%MKy=3hFA%-xR+oYWy}5_&4IAeXsM17&Z$v6gYiUUYzMBfT&lNGDGzKS{bLDFnIOiXaLXyzVl{e^%hBXLkrFpgB~k3Uh=*YH5|(?=tznKxH|e$|UfVxBM4||6A}x^OF3axOd6(%PNt}y7zJh83UW~3kWMefd1t$Pyf;}Wi(-E@%45K(r7@xM!MaV=59q;fl<hTcqo45)u`<zS)YZ1k0qtE&Tx#W@8x&vHW2pv1LfS4hK<fWw*N*Ju2C&e~2kiRn;L$YGOLuw8&fCQwoc??{4rg9O6B~ff5`B^m`12Xa}(RYKl&NM+;i$qhiqZy8^0x&1K@4k6-Ph0H4aB}9AA*`DsmD23pH&tQD0ohPqjIxBtfs{ZBwZz}ldIvFQ7=n+D`X+`lDr5*7McY*EhbDg;x-=;^G0fRY_9$RyUZlJ!^l<}KERlZUj8PW8^FqR?tQH)jk%V+CnK*>rTT6J|80E7b<a~WaH_;$Z_7Y!Suy3Rm86~V=kMXLkEO|DZhv6~H{-*#3L4_tU+Lg<c*i5BnY{7;>{TgT)ceXW|pn1<!29y{A%!$6Hy$LH#XT*Ja$q@PfM1}p5scnr6i0HBVVOF$N4LX8V`X5nPq*Q}Z)aPH_ynxN36DkE3*{j|T7}*7v&;Wged37V40G%;oNyps)O~5=djUXLR>EcL)r0x8GVt4s6*ie3l=)1L6HO2LZ>U<+R&|7^&6oRLLjEok;k7G$!5}=1FqHo?o?iaV@IT`q_tk=+@$F;@>X1PlOg?<$R^F<tiV=zy(8FhD&{`aeY;e9)}{DVPPXcF-_AL^xApI7vjp(kZq98-r0qO?2K(Gc9_)TmS&5K<N^&PP)lDF?u0L^&EO=Dom`W`Fat9IZv^aKTvvgF_1S?yu1p1vyylc@?s)Q1-E605$b-cUxbVmN30Y1f0A5){V}R@Kz#Ub3`4^Knu>m*#%5}prx0*cK!ei792g~FulIY{PR2u+7l$hEqY-O2ex-H23(2lqdWYjgQrd&U%|gmb{@evE<f{uQ$P~K&VlsIHb}@YGx{SpBof25TuPEs9d~fcob%UY?;&G{)<)hY^2?ADBI!y5XkXu?!Y>Wu-9<tn%a<zGh@y{K_x_EUvV8Vm=cTVyR~N)><U)EHiCy);@z@^8QBj_3a|JRKzxvct=XuGVfH$tnjW7-5D~lIIY1R|4P&bHu2TYKzNaO<vzEyA_L~11|5!$S*Na3S?YsO2q2a83p7$p1Oq-4}pcz_Ay6I!;OKPlY=yT`3t6C%n_5@-XxBB*;txUl3K?3NxwVoaepl3871iqD{b$X!cqBx{C4q$-7pqXx*U=^Q^@*8_Kn^cP#yTk#SiE^(4J443U$hI5Rs5yF^lDNv7!4PZi>iFL#|L(Wx?4@FvFr7S(h;f%IpiNLEia;D(P^zvSYex!DWFKxq9+@{Nzt^nd8LmOJD;0K5C#H1cbUSAO0AZa(sMJGVlK10!CY8l~RP!>C43`m!B`g?|A?y1>WTIwy{5JWKK?IIgkX*G4Zj6*w*LU21SM!VgX^s%LNO+8Xdcb03t2hY(NbFdhqc8x)Tlbjw*KD{wymr`A*);8`r=yhWe><-+Lg6lVs(imI7++%6JnHgbrJnQ*TJJN*SoQ80VAV<op)A7^vyZ2;Kf}^fZ=NJUr+}gjQ1Ph;;!W^_qaxog1P>zMw!Xi)sNl@Ro#1gq}o}e`Hrw!FPDaCZ&p+orqh8*IH_#h-B1Y9LR2&KfDMy-mgyH2(so@|Ot>T{lL;6T2UDQDpI79^-^PJP3X^|s0V#)^yiHuw7CEpd>`R$KZ0sRRe=<!t54uMG|2)U)v8W6Sud%-%KM3W`1*vopd=3(l<uoND!Hy?^N^=c38`O4K|J0;mgF6DtQcxN@9GULrI{o=+ZwkdZOk&3t7k-tyKS50Nx$9m$z(Gi|HxGc706sor!MO%$HyV&a(jpKlLA%Y8gb6U3luolfb=@JlE|^rL#@q$5HwRCW>?L1CgUH$EH72-rMss17<!Kr-fl(}_-MV~UcD{fyZEi?^8h%;_0-V=h&|g5iEUi(_Lbq~?+qNwc&2i{NGoA5o->oNBBv<QC{-e>UHmctKb!LULpX;H^7fC15A8?yg4at(|h=^eN{>JwS`IS`uG{r3XA+{1LmE39CVl1VXMcNkE9ohULq|q{mFzG=3UVcL{i72H4V6{>W6~qk;PJ8oBl`+%tWE;_=fL<ZIp2GwyZu{^(E5;i5|1)0__JmhjSe5%6E0m%99aWoo2;;mWI2V(Fexox*D(NloO4lNUKKhXpUJI_m0{__Sw1OhD6#hjTw1=|})+OTW>y<N{GrX542vcWTrJXwx~&=xhSR<^gUZ3fC<QT)9ZC(PDQ>q!DsBr_bN|%SUto?z?mQfTRTQ_G!v&VYIBDNH}^Cjy+TC7FVu95Lk7P==7GNEn%K*Bd9gN24+#2OmfXJaE>-6G@kVV_zq>Sf>4juR|0#;7;8$kqB|u}Kg`p5-pDN~`o%_Wa8!om7Nyq?&nn<6!mKGeRbbyrNhmZ=>}+`D2_Wz!1!4gMDBmLZVZ>(dUqDlN!7KehX$zS6onr#BA(HVeX)Jvl(}@-^5W(TyU$9Mh6XbACpCE<{0D;`!akrJeh2vuM<AU4;M*rggYBcrSmY{P0{aHvG#e_gq)Oz@cGz&gPiw4~}nOp!g$vmp#ohF*10+3b%*)Iro+io|Zi@eVzZR;u|sEhSrtGNUXErMv?jOtIo(#dFK?q<{H64H{X8f=iwfl5HE0;~$nzRou_j=4%=Ke#qN>HOPmWx|nD4C$+uA@KqXc<yKNsbmMR-Yag<z@>oDR07XTJb@afto2X8r7G^QyrIywPJ)D0i2Z2)T>KBj0tC(9qPbJ9gjpc+s!1BaE@Z}G2~FO-3!LIZ7E$50EA{7UlS6Y$ZR$6vutv*dXrRq@I+$I<tTIugX3fwTll@~o-ouEltm|WyvnDa~T%C`DYw;eyi+X8hkDr>pXnPQEO79|%B0<TGpp2lNpK`P1oCcs|YNJLE1963<tCQYCgv7_)n4!1N-+w#k(H=zz0*z7j@?r*02tg^qG)qKfWK<q<0h880HsJFXms~hF1!I<69i-)YaT>hC6|?an6EdbOndesBFt;gituP<!6~G*wfu9isBn#T5%$8>{Bpn#TCnc!>##vrD`2howOB#m7IdT%>9oI@mWy}=-6mXS1Zpo3j-RzgrqK?s$pHD>hfPT<9*C|5S3}eQHXoPCjtXqxx0}^}(xOSw|wNV$c9;HAq)!n9YfUAc!^i_iLoU#YjIG3f7?Pl#haFvi&fvVc#E-|%|n}|tLbLf(;Bx8|GB_hxWLU|A>laUq?Q>u3?2xl`m8g0}UiEYIpESp(sSMGuq()Cc7fvN#zj#f%?jR<MeB}-_jQ9K4f#;%bo$Arg9T%!NNr2n0o5Z1c+Y8@X$`Z&NTkdx#tCNFIBLv;1;wCm4%1ZncVP^||!<DBX*_V?hRX(<+aDXfuHY<UY>(rONu%ZhnzWs~3M1_bdih?KFu2NHy8t4yYA_t+}g*dW|qo_B+WRBl~n-&*6#uuN#u{F!#D4$t*-;!3)Y4`cZ9PH)Eqbd9Ksb!5F~??c{#;?*`vgw&8h{Z0^QR>A#CRqN{j(H6kT^p9b5iq}Z5rTT&*2j+nu&iX=UbeG@1(ihTqTOS}1)D&}_aiT?YZ>M#l+dRg4{CzTs<!S3N<>#o(KxF;jTK6EJ57kF5*2k*5L38c?m+<XU)rj>5OYKj7t=(JyiH%pOj>sNfUI(C-ON?lVur2i9PJ1MG8fm?NUO=l3^RL>jG|sI_q#U@2A8EFfs$gQQA9tnd15Qg6Iggfd?sy|4P<BTEIH|QD;3z<|F)u9*Rn~*KaiR~Z&^XVzfmK{TN5(>uEm&wdpWpASTWDcWq$BkH$q{!HaX6Y+qtG9CPoP4mN*+6u9$nqC)*PgDeO#K`VSGBB4irp#^<Y}VC7&_=GVbd6J-^B3SjM|^rX|lG(vgRxjKe5?PBcYkr~5k`(w``?jpRZ@+@w3U6s3YwJylo%%{YGb66Q}!++Hyzzc3Mt3QX{bi7oU5?)(4gw;z7|{vUt-xLs3TcV{WFSYL!>oxIenffKk|3B=W@^SixPccK?IaN43sK#{j|kplK+;>U?e2Y~EU{98Mbmls0QTPWd9Ap$Iy?KAV9sV17F)&#7qZMAo*Yc>uSXc8^sq)cVQO@0E&mL}^!K4%?W?!WZJ2<DPSGAWm-4!jys2e>bC;yx_TDSQ4NRDhyJSvYPtu&eglc<Pf9{$=ZHDc)l%WW$+wjw$QzO<SHB*t1e*i_gFOJQ!KQ=&;uHQ7}u&1h{NT^HjLaF;XY3)FH7jDKyCsA2`r#U3tTA7|n;B&|frzyy8@?YF+%QJC8)Q@HetAfDAk#3SVc3LSt|R((dO6H%)t40PkE^KgzGE`29D*h61xx;)9Wp#!Gfvm~VSD%rVk&tzSI-VXy}2{r3zXEhY0|UFWQv*FKaxvRM`D*Dr1#hF^7X6A}RFZc|Nq!5bB4{^r2Y)hc(qBz#CmRORLs4-_+HO_N$GjgGcDrjQTSa<b&F3nVM?q?pg(`WDxy03gS4;~65xA`qnG=hHYF`%AiFn%@BKQ8_dLmS8XZN}>^)nW6JpG{bKSKdMYLPhaN@jV7kxgJKR$_@Q<~(@)kir#G$|lxhPDoC(`C<X#o{(?XRgCr!&5x2x)VIHeF@dI7%i8aRdxthzbJoYOCCj&vH5X(F9eJ%b{N66_ulZQ~f$&9>3aAVHryMwP1MAgMlHXDA161MvB4IPyUFZOps8O`ICmR6UwW`)EhjLKGjcwV>t0bu3Vns5S(q&w<RRk3W6*^s)NzqwTNDlZSix@#D`VR1o>+4apKQNGd+2nM)*r#@4rtHjhXC#tN4U_wQhdnachDT;J0vNt~{ab$JVy*_nMn1V124Ze$()y)8Ki25ON_fOF;-xImcxf49=lDarRgM)mUSIs;!30@Vx%e15@rna=wE0cTFz6NsB;vGd?Ly;Lsx^Sj5^JhFN;+2>T}=db&J{`tTE@BigrKF{laeAj*X((|c(@(@J${1591nsii{6**+C8ej?PeHp<_*?3cX(c=5pFE0DZ?wlRZrRz@##F&n|>wCH`z36^r>DW9t_FsQ;Nmc39e4paiD{Je9PPt!+)O*g(x?xnf)a``unv}kO?bwO<5bO|uKp1jm+wYBh313&)yZzqOB6H7BcB6LJQoGs*xQYirR8wddBFU)v^6S${_w0PQS7ymqGxfGuv&s{T>7TPNkI(GOzx?>&=kISxnh!t!@Y9E{*VxDF!)I{rX5VI0uNGu~{9nE`z(UA96LmNNbJ_+ps59rC&-(cnKK&Mx8f!nI{xg(=?~&1r?oD1fEl~K6kp-Osr>|q0)R^|bV0&zFE3?P9>P0HvvCr@6ECvYZ$EYH+tS5bNUj-+iWHWpj)jT#3eHA9?mFYa_VtpOStREnnu+^Q4)vBWJ_1EwGx@N&Kztc9ddHKBrG`8Pcm7rFlLP6i8I2nIC=YRd{<?^@tVw_L8tKZk^$ZC5~k9-?!=gLMJJr8M>1^DgWRp?+2N2u}`B)q=<^3W!%p*oIc6&~3T$Aeuaf~zkl{1AKzPa`pJ=Zzj~=SfUj6|mek!TX*}^c%AEVz-gbIRpT&BXF21kSi3_OOAYy=hoS8pIQ?r?+Y$%#$#*n<zH;7P_z$N)m5m6!;1R~VTrQ-_3N<LBMc{|<`Z}+Vf?+ET3Td+?G<-MNvT{^%^zZyd+8b$kv-dB?ZUESu$q0#YPM<%fZrcfG9%7d+#e-VfwJSH%!3?ToLJDWr}DD#F5pj6Zr)|G`-Fi6rn0ek_khPe`wOQ!#5t0hy7Ni-WL3~vFBJ*N>)45N*1nElX$UYuB*cTd9F)4O?W@AL`81^xKcw|!FHw}Uq>f{x)DS(gwQEn*gsB_rhx^|P8!p1wbuje99dW`zS02A2PqU8sPJ^^7vv<F2KR#vJ29l1R$=hxF^_eBHdn+;%3fYt|Q^W@>Ro#bp^(-+AiB^Mb>~0)qnt2<Yc*qPlEt+e>zK4AZi{G^5*%L0?kT|}u94UN;x3R8nV_q6lSnG&r{-59PPp1QobzQ}!3o(4QLj9?GMXTM~O{UV;7^9Yxh~3Wq)cavMSA}nJm_toEu<UPoE`w{d(sRDLYTdjNNey^RTR7FP@F$a5_-(AyH?nt~D4>Et;M|x6%!eBFUP9lPQTOw!corrK_#2U{DXP7~V^xuFM13xEhQq@kw=LE-%8P<r>X9q4(p<W>?@oCSmOb7&%mI*Y6vy|SO1{+L*428*iWU(>LVc$)GW7ezTG0;lUTxRcG3IhN;PlEZp$Z@SZZwo+D}uvdubV^#T>rN3CY7`(-Sn44-2OnveV}u533=CtIi|N)2Jd|*(<LxUC+!xc!k|}?<|L{6ZgGpxKo_1%*hAVG;WmI(44}^I0(H9E@lhux{Gs%Uj3&F}xw3f<7y`!EwWWe(H2uvHqrUHLi7&b~JeXCQ`d>#fxb{X>zN_>)%!CmcrEN5$Wb{^0maC(s1pU||O^rn3mgIt=&j&`RQy+}_6SroHd0P)W)P*I07n<$r`*Wto%QHfj)fCZgIl9GdJW-#^*hkl$(yRt)+wfK?uq@7K!q+1&s0hcGfeoj|9Yc%zsd4Htb+(iQq{P&zRz~bq@nd0VL!amiz;}UfV1@5*k9BZ2Md;y+O+pnQ(@m9kKVR2uNFG(ZTRhtgW8Pts(GsC&dW3)|VgjR?8;BEizw!o43`cbKC7UvFB~_<s4Jd~tF<4#C`S=r4!wSN&PWxEp6>@I~*AUw}&vrch?uq6iXdOG3I89zKQ7z64#bfI8WbWLc4g}K>E8g#iaX3OlcV98ObrjN$;~_WMeFfqSw>82x&Z$kwjQjQpB$Txz1jC&ZN-k7jo`^OGiL=uA2ctZ@ENZ2E%=pQmExp~HbsOiBAEzl$U9T3)nIzIfMcE{C7=*4FmmCw2&ZZDBg9m}BA^YdwXEEXW_4~I%QX2Ses)vUD0KIqr1q7H{C7j#W^*ew(bw>B(Y9L$!6a59jL=_fjOovc;ItB1fy$w$z2#Y^#;vBGQVPnekff?u7bduf9d(6pLv|fyAT@Nk>4qT_v?k7uY%Fy)d(p0o<WOY)p)=qcPuQQtxje??%JAChx)~To<O%x(Qrg?BG&-PQJEa0%z6bW9FzH6a_F&R*1Z6<8Y+{d$bSCS1dEk3D}luLk$_PVtKCBCT%8jT}+aUv-0dHwi7Wmjxsn1y9uhP1jpp4EJEi`xP4FBC@VIZ`<Ed9myXbZ#>*LczBlOR(@!i}iZb&qKakpzTGnL^UXSsP4>VU-L0fE_iatP`)$Y(GZStA|%RQIY6^tpoAQ42RC^ILZynu-o;e5Db0y&fnr%o@+HNKfcFa=#waH<+c7x@Gyp;N(YN&GmmtFKe%HL%iF`sB0VgO*RlkBZT}VVc-|e&FPs?&WkvA#+PVq*Fn?SqiX~wk_qevudgURvkajXvw+cwf7&)uPJ5l41Z41lIg^xWGsu=lvKVBT=}(p2QT&1Uc|4Zy~^jU$a#HW1Sunz6Zjls(gwoHdjP*2$~5-$p(8{g%{~8sKD6*z6P=yGTHxz`=^Ocqa!ix|(w6_QADBfA${&@;u_;L=BnzDSZ~(xEEguygIZJaS5yWhAWe=2r%~d>etzWGmX`L*pabar%@PKA@IRHXQ@&|Rp03SgDljcA}*cXnWP>j1-ih<)aH(rgWN!W>0SSyavn6(#BR%Kl$r%o8T=N`l2M0;OpK?_r2*R+8+s`LRFWAMyVDwFGx}v}uz4_UcB831PkM%IgOv9!0M-!XYc(fyfw*wAQYg_P`!H<F__)I<*?CIK@<)?|mNlteJSpM_%QM9vq?M!?hTHSM>uT5eDdKS5;8}7_+~IP}e(3r}jd!#%=hqs^&<!m{a*&&q$0WDGj$*L2BSRb7Ab%jCd^vO(EfX*#@LOP%A@>CgXl|sjBOi%YtYk~1z*w7f3Vq0cK6zQxJIKm9rmig5Y!}Ik2jf}Y>NZ*?1Ka2ss%)n3GxSEhVv4D9XCG(#%mOBRHl0t5wyOuxUSn}`8cW8?K0{H&$1YO_;v@PHE5`~_DMLTl$iAq)0GSG}+DfnI5MAwLnaAcb&%y+h%L1+n)8cIVpYq|Z9hc*WY0yjT(a(8pC2w=0`=}-)L}jBxQA0@NXpkY(${myhQ^h<(vh|HTziZkq5vo#J6!9vqw){+jNp6J%)~XgYg`WA*Ht3*g@8Wg{!CR!LG0X`gS-^0OW*95izrr5rra-xon3`j>ky`f^Rs0&xB};dJdb8DB)HN5}XTxYuh@IW6f~<ZKy1~QLAPAd8g8T+@!w~dui?mq2IqEYE=S=5xpwf#1d8R7pRtiBpV`a^n0*)2vI4}%KNWO9}#obDIJfh5}(LW!W@H&KHKz|t*tvs*GQ2b-n+^q2o8BaEFlM3r-^PmfCGdf%9t8_Aou>x>y+OvW_gOJx!A4Ww5=54XO+cGYJ0ZrT>AXBHVKZHH5_V3z8J}7vfEZf7dK#Z5D%A$cgnZ>ZrLaM<4GxtYj70X7^c2S`j*#<f|jD9Nu)IwdwVxM%B+Awwmjo2ZU20@8}f(1>$mlRzEhgjz5)3!=h+Qv8m=#x=PsN;i+(V1l%<eIWv)g~=1Cln5BIyKrUbigRc4$MaS9U-S=&{dVBX9HL(%6Z5VgTOlXc_f}je0~GMTrfQiDN9WxHDLG`a~Y~{28%j28ZQW(sP|=1tH9_~2?RbXN%IlET1&PkCL3#Z-CWXFgIY7`<XPQ%4q7ptZ9y*9Mub+y#dsxn@KT9J-G@HM3Sa>~BW0LYn~?&3lIuKY=TMKXtf<R!4laNB%cg1iLTF;{+yJ*y5aPTNUV!2C)jOx^ynx#6FeeoL0ga|oe~RPqDfedU@;t|A^KhtN8+clE(c;s#pq<qN#hhUt8%7C4F95HIs5RCe9T?dpFNeFoAV#OiPSTACQx9O=b4J_e;naVeO~S)rX(Vf%&$f39yaOC6kbX$6$EL-uW5=?n+JlcET5qeMgEU;KUl6^WVEC(FByn}fDLJc$mF!W3Q`^(|)R1N@p2o#B7O27DaB{Y>c8O{MiiD6uS|V01B>n{W@5XZOHHh}Ow%`Bom-sAp44kmcT)+Q3*o1Gi2_L6JSkmoQPZ*B`178USUX;uULu*lVGrIU%@X>kFtS7ivV;yj~E585b<KL+0bT^t3AQM~n*)Q5a``g$U+>MKm9w~TA{q>si*Xr8D@EI8Nk~EGMOXgW1NAY_b>}sDfV1Xg%$ht#>cI00B%gNRn@QT3dO;>~HE$!OMad(iI_*hxE1oKdBj_TcJSL-7LHv2$&|M1{!M6Ky0C@GZB!p_LzDbVQ-EeMT6Wx|-Ft}Uwf^uo!aF*ftMHaG=HQxvZ;<Vb3qn&Pw^$tVP?r6YN226AqOGux_@_l&(LhayB9E;;x9MX?H_6~ix?WTnh5<ItEf1r7gU@td}S#n8gL>cr)}6ry!q6EcRThb7O}xQfMF>GkCHj7o&7D#cm{-oPCU{j{}9th3b~mw3XV%Xd-X_nNq1YmbYdi7Ai4Z&5j{gJ0jmeJ!6LV77kxR^=JG`MKW@0-Jw?<36~rFyOQjdD|o=Tcn2*$!Q^jStiRKQ^A8}?pn~A{n6nYL+67eR->z-Mwk7%w9?vL4}4YfahBW$l~K=dPEu#vBB~kW5QJPknAPLnfm^1W07+x*HRVH5Q(l)mT*-*M;x}5MqsbX#*^piJMkSP-0)tw@BY_~K1UjI3!#9GNj;GE>2Wb0wBBj*W<1QU>KPPkMeS-bVHjLQ32w+lusxtCQMY8I2Iz_Dg=YM+AVmj?N@K|(@uQwnsP^h(fAAhD7uokW5Ytfc__2P`FtxrI*Ju#v<ZngY2mBMkcv~RF9e(4XX8%HW^O0hVqq;!j{UbX_WSOK3ngwF??fke7m8?|!B7vk(L1XS04z;4#Gto0xD?3=2C7!*g5D8Hd~j8V?PgqJEj3z%kc8@RD3uJwt6wdInkT02G{a$CX@K7aEsAM3Y2ef;Uer;pk=-YRYL=Xbw8i1L%~dB*2AZ*ej;({1s)BWhfffq6@#s>gTxpxHk#p6)iMgDOoA$H_N<<;UTePLlxJ1(FjV5H`J|KZ?qaMIAEmr<wW(+2n3>AjLf#i`wMcu_c(_9l(IJM?>YA3S@)9&abVpC#~ADl1z%zF%CxK8VpGLjWp<zTPjLm+)E2XSmZNEDPDcW(ExB8<eHbQK<OaAJnR|V5jbV67djSI#zf2lFD|j%D-o(8GAv+>-M89y4fd>TtcA$OsjTDZi{)QcS4~l^`fOGx^tFo6=xhdeuh84Zu95SL8+EPCSd=SUDnzW$sxvAByt3DRdaY;?6+UDvY6#Pj;$IdVocGDi3E{bnWCGVzlrX#Ky1EVi?CuJ9)-!rOJ#@1;HO(RRaSm}T>ZZxg;pr$U2cV8=dOAc;W_|7L!?+DhJ)F-nJh7&eT^3qj;f;`3c#DMOYWDyu%CN0~M&5~@R$VM(mSszhMRhg_dSb$deb*V-KcE-}1uFnj8TUyIxqSl4M#BMuO<%{P6eIC&l=_#SPP1j7>UdZ(*y(9VZLfYo1bT`*Vp%F)V^O@;R^dz*09?O#ho@3XP<!HVn*U8BQDw<^qKemrqZn#!mc5FqW@o7)3JZ9j$VH9Qa;PjAR=+YCwrX6gg3FKUw#lq5lc`ZIPw*U^t6^Y0pBf5(YpN3?59SC3&X~K#lHdeoi3#hPbz$3J`#k3?F}#>T$7nUlczqsP>LXJHq@v!VL0#lF_%T-*NwQd+mz1pO2*jO$1^In(5F632uA-)HAR|u6d!W`;qq4A7ov`mqw$yq*pA*IJHet%td8$l3#MzizH|!HRQ1X7I03p&BXs)cyZehQK&nHxCAjbv}f{lC5G@-i>=a!<SJ2NFH)+X6Gp1amMPv9%4QU^e&A_WeaStQB}MAC=@Fp39d9HHmIF9-Hb9pZ&SGRIQWWQ5^;)yJIeaR0$)XcF~$8SnQIWh8ii4?WNR4NWxu-Rk4GsLef3i*k6tr;pndvXW;<D#h6Z=VT=@8E(DIjTwM~_GnbuZj*Vwk+;Jga(=)(`&{#;c9na<!TP$jcW<evs3$bSf^GCBW;^4LI;wBA6)mS%;6dHD!h;qCV+*abIRgmA-|zye;t}<?QFexnidiTW!nGqP6N68G8}x8UqM>%!qHGCm!=yXyjmzi{G%lSC<QZ&LgXj_g<DJB&h~bU|ctY4ILZpr;vxm6mb9qZqBwy!!xGF3lz`;e}*vl(au*ae}UL||DkO~$eu{5zI{Ro)Zk_gO#6$Yp<cS2K%)Nq5WsWv4HaEP~(sSsKoPI6o9d!VSK_hc0m>cG2JQK@qNjOvH5D*Tz8Qgt8zH-_YH+1g|==(Va!JE8Mf^AnUNo8No>qHhd#Hm#Xjxim>h)OC~VC1SX)x$?CL5=DfcODN%hTH{^vHv}xP*q_7Hc3f$lFLk=bKr&eU*_Ntg?cA<P$>7@1mnXQvWJSEAtiTpa5ye0}AKh6+2|S=0#61LP{-kD#oCsFL(G}LYB*1<!CUoXR-c?@UW@aX^HmmalXhC4zeA7wx?x4M;T3GH4Kt{CDCs{lXHUcm9zs5Z#%?6#p-By!cQhF^@QAUqy&CmuK)rFX9N^4Pm*zL%Wwdtf<Myf$Q{yRgej2HGb8EM4cCZ(WcN8ddu4)<+gp!a!oD(>~PEUBi&5iytgu;_B}Eu&wD8RFvPMld&qgLahyV9c%hk6TzU^>cGvZ+9uC1XkLeP?ic!y<OxUl7Z0&)B$3tSNc-XQ_);H4PV#C`Zqwar+&5RW5|q68e{Y6RC7its?Xr+_({oz)ljt+9pkh#h$6`v3!Y@pY6`l<AX_BJNwMp=3}#Apv8IfOl(%v~i_er-g&ljhSr56|T+!MN&`O&7{%ivr{lF!mQZF9`qq#&w&14Y}ibarJ#=B*WCIVi;Helr(G1x(*X#$poDK-Zdw;lHP8}WF}He&I5f8`gyuJ))=6ZHbG?agxs@NEKX!q#ar)K0;~(uyWLJIRW3+JCT$y$_16LpRU_(Whi#I@f4R&^rjs!zk9li8=O(E);wxT8&w~-iAT#(j?2rp<fP6J`B0IQ&64vZavwwPhhl@z^vP%)mPeu+JI3^&8A&f=4JYih)Aoxy`6-_8$FO_yF&KPZQ4R`U?DQ4r&CVq{2BI<tD<pKHyFp<ZlyF~`bqihN!Ed1NtXy)K7qC;O%>}-$@=drDVyZl8>|djZe&?IxmI!T03_w!r#wlaIEWt)scKQKs-V$hGS@zyS$C}R^#IiE55FTi3e$8@bL}bqoL&P2O-({;;Ovy>PYgpZ?!YB2ahgWAc{&XZ^L=Hlzc4i8w`r(s0;+6?pM>45B0b>!q@7eMUbBDVD2q`bLY{bieNE>Eyzln4yW2pTvpPXbTa&J7T3p$QK<U;^2ol}~j+4Kxi(w};cQLJP0u(%gRFX2)vjsj1t>ud+G#e#k4a)2c>$13(T6Jccy9Vy@-I-zABmv5lR%d9L&`4qKZRs+rmvAC3QX+>g>bPGH^We%cDJ}FzBnAi66s6}~)ycCMUm?rH!W?k5ajueI<uny#-4gNlFbRR;soR8Skz19&rdeI<4Dh`j1sc9%@e|C#Wh$)sx$x{1ypNe53+}*qY!n-&ea9?ix!u!HxDcqtHxnEIuxSFEvM2-xv0IC>2W!EXpq(e!7mzpjKE*`e^d{<sskSKldOU}#3)%cd6?wch6r!W9A<^%JV1*PP$sKh?wYjsK@Vo@B$efB$5un~t=b>>&392N~>}KK@RO@pi%4rbmwwJ~PL$FEjOl0~@&MLciYNMpqHy!Bkk=AxImrs?~MspEju2h8J8}XgW()6IN7J|VP*|GH5`jEtFe3?Se=2ooiT(-Eo6Apqp-dN3y@>W84iJ>)T=`v8FQmrx+m7VfH)dj-#y#C_rvPqYRX$&>B9Syv*s-ztn0);=5&F5&6jo_DH?2<1p{0u1D2Q4MpyCFzpEJLCQ5j^<THh;psr(k^?J}skTI!)yWOcoI^l92zKo66){5~aGQ9#B*W*ix?ncE@a=Mk3JlMem<maIT5W|Moxx&wV*NCRYcER-bI*le1?YWz3hww<#OqAx9PEn(&f?ZNRHaAFEz4couctgG`W{hiq&p>#6N*g6E@`>qn?nzNzG`N7_D-E@4GwYGnJeV2elgQ%9mMV*TjyvN`o`NuRvgJTZQv)A+DNp*y+`DIY1I&-xN4c7DX#)<vB<wV?1K)!@N{7Gg!RvTdHiwMAjNIG>=w7yV)@HtK^lTpdc4rk=WUn~l=XD6t1UCp0BbTBEobT_0*a+oH*KR!8oCQ+CNMxvSFFAukd7_quAHvE;5sYa{0%u_&&O84?@aSy#I)ak49>U~1K-u5}?hI<@GXIiCJ};_<z<sO|`kHJ>`4@QT1BrlijiEU&{r)fz1|(-^br_xbmJH4~MKv-DL2_bu5?U@i*Z>EKz|LKL)L!RfjUcl7l?e9wkxG3X9)LCInOY|W=BBWzC1q!Hla%?GZROdK$m{m{$X9Uj7VT+d5fLf#};^|O5gGFgD64!cOB$F*ehY4LTYMR?0pv3((Slhwiab-U@@_OguYuMo*8-AAb*Uq@N>+8_eO{u}mY=uZAqV-9XcgPX<FFp~CX)8$A-^~UkKcECs=lC<_muY!5-^ZA|B)Wstsso#Z|MeGlDM*TOZ4x!xz6r{L>z3l$Ro}Mo@E0hH(hY~nup?R`!W!i^rT<+I+N0|LjYy7B%x_MjbIdRqOKUiZaO=UTUG!gbV|HNUvxl6Vx7bw8P-oW%J&bOt1V{%ohegbUvviBLC*b_2Y=1{Jl+QQWlN($QW&fO{n{Lku&tv5^)RoZ94*_*FF`Avr7TKPBGDEcb9BiToD-yL>M6-iB8Ng4OZAt6t}79x#c=3Z90$B8_7f^dwKbs%)^tV&_h)sdR}p_OJXbgs-^t7*q6n#cIMqR06qWU#rP+}slf9Q^j2nQF-S6=)e1Et>neLH!H(Z&Z_;OOKlXV`^4sUlZnHa9T|f_0l^&K942eD7&?rA%9#UD&y9L&V|k#kqi*2MW&fS2W)EG??6c*3TI0O@N^W~C@~2oscSzM3UR>gG!?o4n3lO>a<qnd=v_O{bqtZF4lxr8=aF-}nbBa&rc!T%B`m-w4VVX*&)6v3$JEUz<i_T1EArk$(rp@(->}zIiROhm1d;LWWNwlH^YJu4z!t<VkLvnR`@nX7PK(Z@F;K&#<)5aS)uZ6^JS4IPo)cw)er9%HXC;UyvDz|3tl_MRh^h3S2mU=ashp({ow~qsyM-%i#KOn+F_2WFb0}=O6xE6P#mSbYR<KBM>}_rX!@D4T^BGX<`sfUyyr=YRSNxe|ib2Ze(G#t9?x@XBefCr(W;Knmp@SN}pJl3t9Xwv5_`u_u8uv2WkbdWxpxE~E>!%b8F1e*sO)lm_wh!Utl@K8nt#q_y8Hu}gibqLe@Bp>@uA^O1W0lsn=GpVOBzS7Ct+*`EwnBst0+}TmG^&ul{DV1slk{L@SK3!7E<$QXP`O;bGc{m!kK-nw%5=*08sYRK-Xxmd42)bF(P-g>I+%C5xv*SxAd2F-(zfUrdi8iWtD0Hw3c1yU89S3!QQ1NK&`u?KuBw>}!9Y;ztThO@f{KwJX0=$J_D<_E+#ak?nh<)dRf=_#*der7BCk&;GUbJ_z=aAL#$R-C9p7==0B2Y3%Igr9%w;BG?`^#2SEyUn$3bdaMD;fhCijq!1sZ<j09f*Lq58>JXV#;*cT&@j?C6NMQf`8^VG}r_%DC$6F%<1G9j+*rGoRdzLR&S-Fv}u}mOtSzx@MWj@WUY5jnNDjqO$6F?tN_vacb8vAUxB<Jb-T<2A=>xk(JaZg#8$o(WVr{+p`c1B-%{iu(#=RD%C}}{J=yen*`75!BiIzONSqfP6puMz!RkcjOY%`mz@h5D=cLD&{4s?f@>TlaAKOXx_$|uErFlvT_azEF|U3Oxzf#LDR~-rT6g$!;pOR62h3mJeV>Pv;d4%W_tCciYq{BUZR$2wgF{(+>BxcQro#pBXDJf)P_X(fpsKSh&|@X>F^IzHVlI!he}sx|*ZV{v+KRp0+C0%CFvSP<d9;^yKUJ#Jg$e<s)cI#eivKNF624C~Q<lK^rBb+*sFpYIwSrj<`?O}efJ}J2_p$xyw;z7|{vUt-xOH%@pEFb%^Y~nJ6R^j3Zh3sHe6gXm6Q{wa=Kc`nCo((HidDNhL4p8g0r>W{P>@i@PIju8&uflX4ZK-jTbPy47XN0HF>t84P#%1Sd6vKjqH$`I21N`h9GD^Bvy19jz}-47e~Y3nR36s0QMU=GECFw$*3frEDdR^vNOK`y$o%Ugw)Frke6`}IGLia$!Ieg(CD44vhQ2T|=|mM#T?tLF{*z5C#itl8W3svlF$KRn>Fnv9uwU7{NF+k=5>-tTDFH1>GGMjO4bh}vV8A9QoIe*acQf*WcvMn~fbi8lP-h$Int9B;`FvPbCy1-jLoRdz!PwZhX2k6&)!)4%w?X@Np5Q8Cz8sToa;e(eNc&9RKG3KBIbX7244^%1J!aA;0gQ9Vh{cd5I-5Ja4ODk|BEvRsy62^N_UiBG%R1W1U64BYK+SP+qo+R&rcDgroY$1-7I1F^`^y$~I?DRD55uqWOBTHO_;qZu>0)zZ#+&o>cy+UGjm_1F=TcIQWz&qp1kr|`-GkMka6WYzd5^r*xVR@Q>TMxRxDC9|2xSVFMGRL_se(MoxzIzS-OD+b9sVvA;}wD_+W@5k8qIQwNDX*lp>GAoHnj@R;5CAS1w(vF2><c~-5EXL&!;wjKWzx$FFnG@W1Y$QbZ&4BX^_I*!OZht+8jV`oy;Z;0upIuU6j0>Piw|4RO&B5nH+OoS!R`(#y<Y;lyVoX(oSTn!h0tx&LQFRv1*-j*V+Bf=;Vtt1TW0(L(Yj)m!eRaQaZ{0$Rt^$Oy6q2|G!Rg*oXamv2Ke7b8Y*2dZT7ysn-~-s1AXZlim&MQ?U%281aZ}kH1Culg@q4&i(zJk*$V`fE3Jgn{B-`_0}sQH%YCctI>7!a!mWQW-%>Qt_hwdOD*0$jwpjhsFbtdvx>%J<AhN+ZzWsa7`|Kyn8ZGX#odJ9O1{0o{>3dH7@MCi(R_-tpXL-0RS?1A>D^BsfBNw0WBG1Df_b!q%a0#_F5momRu@Bfw2seH>c7lp=#+{CDD(lgODR|-HDU;ps(Yx<!}+1Giu&?FO|2?9Qy-$XQ*iIY>m}OD`G0kW@Mf7ImC)q54t+w%<+cqN*Zk_%&Ju8Occ<Qm*d}aZzKZojX%*x)vYC?0hTpIHF>Vhy3}-*rSl7>>wvx=5L7&I$L`!{tkg^N4GtX}*n)}s?1N)<&Mpt)JHH&}L8KT0&=%e*vGtCVE5_7=02C`9Wu^ZyF`l&<yD$#i`DQq<q6)m7jnDa&Nao;!G+TErIGt8<t2k2K`x9nl1yG2#JIL3T(XPu-+7yGRAIcSO-`Wdh%?x4cyu*ZqR>U^KeS)mut`};YyH(QJw>VEmEH1)1H5BdC1&H4f74VWb_a=R@NIivgAl2104TDvszkWr%0guU`Uyn<N6>za9kXXK3YOWAH1&CUu(Lvw}48b2vO0JuNXB30>Wx`?!m&qN6`Rn^lSOSD-kP)rK$s=c!6banXup5|?(4_ouCth;JMR>r|+@xkf!Q6`3;^7oD5eD2Y|)hNaM63brp1ybexNTQ9=k>a#`=-v;Fd%WA{U@)B-Ie<t=T~(zSZ4Xm#&rw}z%zvkmWTIKQ<mcl|+&C%)1)3z5!wP~D79}uB&6DE)IOfC(u-n2O4m&~tJXly5j8RKj0$rr^L^&PDwLvJ9x2y-`M5U!07}J!1fSxUbcmEJv1aL(AqNdL%);RSonv!hI-LBk~l*+sA1JV%&EAJy)xvE>*sW=vv&|IG$bgtayl9Tj(B!d=VPqFUxJAPX;ut^*&|CvBCPE#8rOR}_7C3Zu9scppP9E$&bbWx%JbQMH-L3}6NV3N{vvfzQe@$G5Ksgk`<)2xv-fP$=(Z8cj!&f(O}4JQTZ-As#O9I*<;w41uzHJ_EFe~a*v$Kz^=Y_u-<^DF2VDpocX36=UuHL;wm8%k88q(r)=URC|@sw=B2qw<PFFHcXR<{oX+nw!1PhGI-G0am!7i{YmJ+{CDdB=V+SJ|)48;c)w!uYUg1xOv9#I--KDW>{PI<9;Ak<Z<q&C>cq1zAw>mN(9a}uARu~A#Xe-nS$=;qTR+b*gHrI05O`EyQ&VPdLI?3Te#qY5m{-5MmvhJz@+&9u&?DJLP&<UQ|Di*S4L|n)zdNHUz~_cIW(5<#}bxAV;SD%V@=7~4=srgQIWStX+b<xt3OY&+2=H_jXizA#qG7+s!RFEsrtor+D1B^Tzxg*#Wt{Vc)Kld(lArn=g=nvufzM`u!hhy4arQyps5|!pNzrH!EJ$+bhRdu*L^8QH(|`cOaS%7H68x7xF6*Oo&buF5Y|L4Xdyhu{*-$~+jtkZc_F2Gg<9Fli$+&~XpU7J=5v=&qJ-+Vl>^eyBH2~lTBvgDBuNp`8D^Z3rX((Q8G>r}X;$Y`n;@~JCBe}svdE(?sK@{pn@Rct?$R_%f)yyi_k|x>A#A2~>m1OSqZZhEj3jjy`G!r12XV?<kno>Mk_;~|D<$Vxvv)ZpwCMY)o%34e2K0$MrXT`McVMky(zbZ}40>j4i=w-xQ{))152~e#NgD9G3p5jd<k>5*<M8upD<MXC8KOBUatR^Nu--w1C>6Y>QG9|2Du`NU$_R|ozZyVB_Ib4B|0_eT`bF*<E3}SCm_@aSZ9zeYkU`g-<>LhMzN~H1L`)j9wl;W92LVq!*0qDr<tAos_jIHc>CQu{ro%I$w727w6W)0S&=#4KXN3w@OYEmwvT2<%5MTfXdJW*f$hFBlb$*Mt_-b!)3{QnB`aHqoHtQn;KWB`EmPYVM0dITIfdnZaqZW(X_?I+;%x@;af(jC57!8`a%=I?4)}!=5C6=Lbf1<@1Dd=rJg1F76E{VAHu^%Fc70|0bUV4(~5ckxB_%yg}Yhdb>B5M?5liuTenqJWbsjl0Wjv|@?YXIk+_(X~CG`9*0Q=Pgjv(|Rxwo#wm3>L<jtLjtNhPaQj4Q@?@9x}neo8~<`{Zt)Qc>Bm;_H_08yt=N<$#Lj{N}@B_OseaBW$!315=v|hPD?e)A+w-$&Z#CLQC*f?l;IvAg_a3j>ZBS8>l4neebj?kvdZ^HUfq-+P<ZNb;d1~$Xx*-48`hl8+B07c4i|i`HZ9UmC2Ck#S^ilW4HC>{HCWe}*bh5}n@wSQHIamdu||!l@5}yCKa%r4;5BpR*kW*|AXFq`+@BgS3@QO{9vL-z)4nFRk#`3p&&+87CZ(J!CNMJv#vMt{?>5x;X0)nXz|&~+L5NpHqUOd2mN)#H3{U%!rdo7RI=!Z+R6m(vGHt}*GA~D#`ypqXLx#^rsW)Sv^If%AjC#E|<x6m7q8`Kj*&iZ6b}L*uE{N@^nh+S-a%f~CHgZZv=q6KrbFZ#6ex@f<RXr4*O+%MLA?US@(m=2>)5I$53$h^Y^45$@P)DwDF1p~vNHC$jgLF|`ZI^JdHp9R#sGWFb(7*%VMmrtK4k2|bDvl&ua(GeaZLw#chhm*=4X%krp}h$d@pz%AY6pQ2GZXeS!uAK|bOU9r_hA>(S!Sm+2AiSU9O%rk+1O?@c6L#3D#Onng9~GYy1%im@iwXRt3<F~BbEgXM_sX0F)HICdA^m>y3vmH0zAb+<D`FgHxnLbEu@PYt!Yx8+d2Z4W6?BuqAl<O(wv&6SL*~v&Gnvl!E3tSf@Z!i>41ByPr?tjmT>8jiffN*OQMi%&9vjAEedv0MWH==3i3d-5ZK*ceb9m#O55Ig&PW?TUP6!||2pMe<n|P_{b8LrM7JY7sY?1Cb_!CAm{>jf+qVir7DMNMU+;fEU4-JA&TL;HOTn=0Il(u!+q1)8qC}hfx;w*y`%aMh4_5QYbe3z$?R3p)7aX@yKZYlPp0c$BX<vX{P1P2p4sM`#O<HU0^}@{6^qWr93$*W>$yHi+4y2%w9&fKFUvPDQ=j3|$<#+M(;mcQbqY(9dorv?-HSP)-FOx>Z_>hKwZSACefUDRRBxt83TBn|+o7B1UY)CVQ5`AovHqv9e>-pj+IkTVR;O}qu%ZHzT`02w}yZv~5_)H`kxGhNU>fL<#*5CxH-61N86wGNGko4jH^xF?Ve*cfpzwqg|3IHZeGwMG>er=D8W^~W3>Xd@H3r2D=nXcWWnx))&PH&Hm%W&^+)r(ZT<LWkclTsBiWyDI%=fS}c9yZW^?`FSys7k_;DlbF2yqjnJ0MUdAQ<tI5HP!d=d;Rr0h&3s|fvg`gvUzD@?>67A^O_eA_v)=_uaf6D;&#se`q#_lZ}-J0iW%kA@8fA%{EgNpZ-edJoEvLe0{+eU?OxO`S`J6pCne5<b_GZ!`NWo&(~z}eLsXi<Y6!vAm&?ipU&2E;Pa+u|Yv;)oN{+_6Z-VzdnINItvFJ9^8R{QJ78I-_YmgcINrVd+5*6y)I{R8)H7I#saA`B~Md>g9V&hTKK487uLY-mS%JVtZ2*|nJd9{b_b$P7#T7{PqaV@&#<U0`H+POdNn0K90{jHJ<vCF-54U5R0ZLoHs)*o2SzGXF?9bwVax<&TBhO;g<uGOI6l@D@kablTZ9Nz^>MNDkoWwMK0>ei3a#^T)r9{21o98DIO3Gx7*BTx41wh#s4li}GGH!%WBv@`^mAQIw1U5r_xORK12Ppt~ebWsd7en{)dUZT25t1>GP@5ZCt#?!UK(xHZ_^~3$|g$);B>}nJoaRF=4W;6fFHsE!%)y-<UoOvsU(V|n+U&miw*KFh0XQFr7^;TqNclKgMc)Cw*AL7-s#4t>>x=07JR(df8>xGsuHi{pntJK%6J{7v~dP~-|<M+yu!sm4x>*`i!)A+$!$3OzBKb>5$DQeK%)4dQQXDig7x>pp4*DkRs0s?82qWToLnEk2uLvYUFY;lf5<~3OMH$4|yPC$CeSGTPOQ*zS-9@7?1OCbHpWEOrK>-3H6T_**ws0qlgZX=xqq!+ep;_mPDVhL{ZRXn@Bwm?SA8XGA^--fWbJtcw?MB@0GqSI<ytZm&s6ueT8T-EdCQnP(`%6qHq@v^QQGG^~Pm1wC$tE=^p6$K)QdiqXfU+DLVwW7Kyx;nbwA7L&}15U5p5~@(K*Xjz0%rMyNCJ_MFzwNt8B`8Wa{Uy=0KhSX>=$w#Re_in1cjv57=pZUVB{Mz6;H>gyBKhnDZhhxRJv63Bh4<d{=uO>8nNyYqW{RaKlc96heXj^?vQDx=w$w~p(v|GHw!Cr>t}}(r^uS~2sqcHc$1rgbYqMpcMP^k8*#Vxk+^DKHiDO>+-oP|R+ccRltl}3?S`ir4)W~OONLzrnq{esOCrVqnekPaIs#@LLRQTfD@<I+sp4IOQF#=p3eR28=0c(lM7F-v-&?6uMr(C2r-&oVq36r=-IUQLLsBQ%-#sFNAnCAOFvZ4tYxIYsb`Yb9AYqJuE>CoAAmAu*I2ZNU!25dv0kR9V2$G1r)LcuI=7!o~~aC{;*7K-S=Y9_fz!E8p`0PKB~G}_oKWQQL{FZBowQ4|P9GyB4Abu28!A#x#d6vYn-b-7IVjP7G+>1f<sG~;7b8Wz5TX-r3!^!banp~~y#F0;`P!8`Uho__b#c@f5sol6D3I$Z(uzqL@qMOt;Yy}EPWdy@I`<Hw)BW^bVtR-ZD<$RGcJehI`utjenG>-sVDUw2!c@>B>(O*HtvMx0aid%Ud?oASKROUtoZ0%X9^scVE#3m?T2FP6=4(<Xj-Pg5e`sOL~$1&=m)4aI8iONFWi1Y4Xn6@C2qu<J)Z8DUmES&%GY@U)yzSgL8?DbwQfTnK{{6#3Qi<dh$vW~fy@R$-@#jR$3WORjsI9KyM3kn|2_N(=ttY0W3M-VgN*sjUy`Jw0^2s8Y7kV)5P-^hwQQz8UMbYr8%w>K)Qvhjkc2vEm4unWt9S{K3sSyutxf?C$sK=WR-JB5GDt3CW<K*%lz=44i}rF)1o6NhuQK?J-s4O8idFFTrNnFQj>~0dt_5M!K9K0QeQ$r=q6w`R17w2}<(o1yE4@ou9PHsL9O+ZAw;;Ca}(6a=hmglVM`pMq1>#J5u~~Xh(S}wEEff_6+Pjt}K{0$GS9C<!rMVd`qhbk=!`aXo>ETcv3fS!Ps1h{*H;BvQCe$Vx7Daxoy;wFWIZE)Bq5OLa4laW*j1&=Z03L2<>AHj;~n>XnXW${~;jH!*HE#EIZEI0^?bHEk4pBT+_@*krr1nwo@I({!TQv17{jz1=LQ`Q6cNXz>11o?m0`U2$gA}_YbmAC&9lcVhJoLW`;&arZ#sB{kd`U(!2gYh4gi1#m4LmzIZT|!B>lxx#gf&c5FO#V<TWYe!>r0QH?F-?zF}_*M6BAY#xl8-Dqmh7Y_<7uDo{v>;ndQwe&~1F+5mIG+L=_WaYA0ddv8@0fTotWV$SWbPjA;lVXFD5>KX@-QfpmIS7W~b{6ou+GKsjp=oF>oKiy$kAtD0)Pr?PbPPJb)<}kKXfcw5%;r2Mxeay{gRLDI;B<3PBOz5abeZB~FeI<>P*_3<1~fMkx{!}Vd7!qx8;`X~SjdMA=#!U~IYYO&++E(dp5ZewKMag#b@{uLd@9;nhQ*Ag?=$p9yke@Kac94=#Z!ujIux{ck4WW%4a`$MfF+lj$NOY@`!Z!9KJA1Vy3@5m_k)e>3lbvh??Q>ndOgD&Bw6OMxs;+X0p+sTwIaf$A@)Dz!(BTr#}AV!*<{b6IWLglZBE*Ht1Nc}rhj&8%8?;csw!(?7v6OR;l8nM9Neyi2q3w-dKFi@hCJUUiH8K%sut{e&-|+67GBsS`p#W&W%I(6x`71@*Jy^Za{Vjpk!}i<8;RwtsLtb)a`aGg?klDZXF6%$$VL<Su^F~LD(|ylv?s*Q?ogNvz6jmmVQNrtOCmubHUx$<<JdkbsQ%`t&oIcaiYvpwK%PkhrMqoCuFcB2D_H$`wplN_+4Zw~DehLv<B6KIY4#!W&xa<w4q+J3U&iYA&+9U%#=?zf$au1Wn^agw)&5IK(}yP@<<jV66k`S8+LUxopFzlLsSl&EFC310>tN%yjLV`y*A)oJ)T!$aVN;6zyS9<b{_bSi9)<;CJg7M$mcZ_ywzmY^W-;1w1Q2g?AB>iM2DUL-wt)@~uV8|KTBr?3?30eN<hr3umSF_6Hng_kZIlW4lA^0u-VE-zt&)|tF-`#bWU2$}_~2qlsc(Z^Q<kgxnxu>L!+}kwMmvQL7zNpZ*+{=5<dh6kr%acKEVJI{8U3jU@C57J=aG0C@%bHta>4X8q%1X&)PUh%%w?#)87%79XuKeBqTZK5tpcM{B@p<mBx>P)EfIhv?Tt0NZY~kRrq)baZ+Ts^3$$W7+u9UN_nX#i#dsxn@UqTY-G@HM3Sa>~BW0LYn~?&3l8ZHF=TMKXtoO=t4(^RbUkFXiog3g*1@fF%!V54w@riS)&I?G^4Rb=K7tm-bZG$)tpK@=uF3)p}HV=mytbnIgt6x2B3)%`bXpl9`W5XyxVLad!5uu~nqXQ$G<mGVp7sTik*-5$)Vd?>l+o;`xr~cz?5*`jqBU$Tww!K^69pF%bG%#>IHri%hFvyCkJ@^Qs^|lH+NQZ>_1yRBahQInn5?6<ulCyePXdOj3wLP6r4Qa;WX<S@mLFc8#$=Sx*C8`A|5<(7XiCDRi_!Hp28_T)ZAll>Fe*eQ?;<MN>aKbWk{r>Y{6TZ<Ve4GwpNw-@)VLU3Oga89CO6G*2(UhFeCSbT{h#s6L&3b}+75oTr4{k4R&7~tL$8PkNy_?v&&wkMc>m+TtHzoyb8<~{zqW*eK`D=A;V)zUUdPy2bizV|ckRz744R*Cp8L+?*bOfM1F`6X(YB||j16~mrY3>W@GHvpsLs7DJt8#y+EL?(ls9ptjCt!-5H&%QNOYa{ZoQ<d@hXf^s@>$p!Sv&<g-Ju1cai~n9PkMqsvT(9!jLq~f!)6MQrYK%x$Wdey?83Gyi2__iJCdhnAm?T{x-_oN*o$%~LbT!XWA9%C;&rc>b(>KpS?M$u2B9%y3L5^ya;OJ^VB{DlE<jm~bzKvxcBY4wQ2uXQ=~dm!E#az4vDSe%a0f#_ZS4~4Z1uP!o^a^$T~zqJCN9|8<05Ec%46{RObzSc*SBzA%O?o%1iZ|?9WBq$-AaA^V{HBrj{D%g!hq9C<ZY9fY>^&LB&UT8W|=H|Oa%{?xobf$)klYK44n^>SdFfR8eR75(n@Q0J@8e@$60b4af7k99Ooo;wk@KXK@I^J9X>&zmjSm-IRTQ!+H1;(qNcnqdAO1hdBtzELPwJ`#<HubYH&s<IRyr_ghv8FNC|X6^M*_scRY1AI$*VJw#&|5A8|h?bLM@5{mV9t*t`f}QtcWt@=8Ur>U26qto`SIdeUM#?KkjPw1BNQATLm;rDPv}rWddlt>tUcmV5Q$jH#_pK(akCqBw4~Iy9BSaj~>-urz+@52+hRDr|yo6IN2XMOH6cfmy78PaMMMgUvu9ttpLKx#J6Qb{7IRY<<9P)?BZPKk(T%RR=LBjv`Th2g?|voP!B3Rd^OK&0<CRaX2*+1#8PCRke1EK;*WBC4BzoUq04vfBN{-hfg21alBR9=FjhbeGug*-}8*mZ{Ff$YNp%bcSqE?C<F7BMpcjR_Cd2fPCVUhP6t(*9*&c50LzcVF`Xs>whJUDJ|Jv*M}HKRAB#F<;7>F453<R514pY#={CYiIJN}yy8{@I_GqX)Q-N$S*!i_J_VrQ8lp(K)tPvQy(N+Zm(lX}aT{<a_RJxyF+)E2XSmZNEDPDcW(ExB8<eHbQK<OaAJnR|V5jbV67djSI#zf2lFD|j%D-o(8GAv+>-M89y4fd>TtcA$OsjTDZi{-=J2A>zczMjnrg}zo18lBDH?iG65*fnx~aigxa8H;jdON9tx?kbN%`!)!5P_p*ZYekEw@F8PSLzs>f|FYoVyiYFE!80S7z%>;m%nr^5U|45&SHQEL(evq{o5iVV4zZ7Oh+|PVO?D1XM^QNdbxhOKA$l_FYi}RMZD8u*e3s#fHJ$9T(E18*gv7#IBqUe62Ut;tZ3Q&)PV}_uVi~h6TXHO_vq{hs6F%&_&cOZw#V{yX0g%eLPin~R6Hqo94iIemIwqwUiFc#azx;HXE&Ei*!;-;7IF0saCLk*j=qd7uWvO_LMe$l&g)=qwNPdT>Qc6&J;&7V(O(Rid$#|lQ*M*}PYHgOiimGO3sUiwX)VV%z7N+G;Sum`AWio8lxL5_3AJuJ>Sz9Jkqg<ZgIXG9tz<NG46#mv!Cq^F35el3!ca0^%3Ca=^)-~(Gw!!v!&RJr3F@uiLYLfB#JhaqDrV2<!y+?z($Zhart}>Eju{bX&S<?}SI{^#w`{E!rqF-G_P2E67oRarIt*b_5VXHb}-<NEu^?p7lir;O*l&SMnnR<w`@utt)L=Kd^UnxL{^aYwLYqML}FX8hE)f&jL0fb=Vo-<A8?!&pIXz9*O35vBzc8=$+waydx3aZor5UNOlLuM9<@&b`G;sA`|K^aHrdGO1DeN%^cVUWzR)HE4kcwhA~XFJ?~@EMv!y<W!qeMA`v-rqydvwuSqjeocLI4){)&(oqD9`NboHifL@*^x?dHo-YrNlb=YFLPrCprAb(Rkqt?o^RysaEF{9FwZ{Mys2H~UU0C!ZtdM$Dk|y;jj&)Fy@}b*_@j>MTWv+l=@ocT_pR`tMZwrY>uk;dLh(1efU0;z{cV(;VWVOe3Wad(2+G9Z)87U?9Fl0L9kwW2LfbIuPJ81r`U8ziCj)r~Th$=CM8J3_u_<D>BLSWec8U<GBg*U{uK8TvQWVM8c^|F{3kYy<5jghp3Ki_JD2`Xj9xkMUg-9$-Y)L-?X0{{(vtWe*D$JeGR3bIpAZw~k2?HGBtz;^MmWPwv7W*D3D(O901%*2Bu2od3oIj)bA*>32CZ|*#2*8aYxm&h2Sqyrus?tvAJl6aKrOD>^p1<fDgPl!lrdBRZQWACD<a&u1u4}G*ErLW5;pY-cIH1;em;4O@ODy*1Ftr_5TIWlhZZVJyR)4moDp@<Xt5Pz!HuU8QZZKI9?<gy<#Zp8u5YI<<R#5^Es0MKl0h&LlnIb2G6>)ThbuJ08AB+i|Igxjj7r2?339QZPJONq|SU2BvlD#`<Z>biRdjpUWZS+YN&x4J?i~X;0k4dvZXK=UGq?eRl%T$!nqgpexfkt&9rkc`Plpl6GGGuK!sg{vyP>=u4kSgPaeN9FhvA0PnDB00>Pm05RTNvnlUY&}2JuOSBX>ml%r9LdWTzt#u*I|aZIJptbjp3kOr2rUntN!B_7EJxz9M{`jiYbAWb|;jjLQ`)Sxrbz6^Z|8%Sn8F&RP<Cdmrldi^|Ag9Q0%E+ZTc88W0S_%d^**fQHts_xH^7PvSBq;ZAHg8Ee)bbvc`fZ*|VC0E-}a!335{GIxd5ml3lDRBO>Lk9MIx3<yB$F-fh-Ht~OV+wga@1=Dt7M07pM?NvPDzN5N<=(NHs41cYJ{WS8-7S)+-7SFjCOIY$h35NVo#WnqfVfyHfy{ryHfUbBr@yxw2=#jmS9YScu%z-xQ++yQ)>z?!ginhdp5FtN0v3C~Wl;+*y$tYYtjqU+ENG(q$!S(wf>+7k2*0`oA6b#P*ieWD8m--%XZR<E~VP`fnA@^R>w1CtL!F76am=e=7`HtiD_?IbYkwrKU0cA++46jQTl*Ohsh{v#sNs&8*6A@N2Jq}i^Jy>pwk5FA*DOzG*AlRAHfedMZW9MuiRF}GVOO_+XCK6{dN;8)Tm!j?~<?MYL`x>K_L`%20tx%LJtLzWv^)=sWf96SI?x%VkgQYa4M$3v=Gl&dOe^q9=Gk7w2$t9(5Gb^F8bh>pTE9n@TVia)2<06|le&>A>9CHfP?(2F~8NlToj(QTeiL&JPuS?ezh&G>B^Dw}{R8{#KncdJMbct2?;m5SHwpE$~56o`-~USD6+xdHFHeeLcxkmjsT(9+hVYnm2Ub|O%^brXVww}Ip2uj^vi3C&$hYnuQCk06z#O!aJmk3wtt;t9=030Z?OJHxsxuBBF;ndYv6dwh3h*fvRkGNsiSS|&77n0s5g%<3hah>MiSp^G~1m%}``a!g7K{Sk@50X0SGc~^DvEXG&JGO;iRTy31I<X1UOMOn8*{5?!Upm^#w;aTKX<*#X0*E$1yZ%2WK?^yf<vv8RTYkn>~I|c7!=Es6Na2^}QhH2k1OIdFBG!!lbYVpkkM*wV^0H-Vp!9ncSqU^z1@Fi&H3HAl#4Zcq?(Ko$`dSR+9%Dx`Y;p##*e^EsqZw-a$sB1{{dm&gM#Yb{ST~TfB>?S-ffh#hnB2)yZchq@k+);umNi@5e_yyJa+=y}-#JcUJF~JaQ(mNBGK9jS`?w#5wsr5|<I(($H-OS}v<+agVgqSN8A^1jor?NCXsH=rwFhzDOeYQR%aT;Hy(6hM}D?67h?(T$xppG|IGo!qf5ME+v%~`q(l&Dmz3`J$9JWzFkusyH8__}P;<zX5_O>IX5@2o0mhlW7m&t&sCnq(vRB^bNp%L_jP%JxA^N%n3C(iqE-C_)4ezO~JtaPKKtABRuN=$KAZIRcYK1dJr)|K_GL`Ibbf?x_b96#}-@Yk=J`+ozETbbZnL=N6o6BJ;mJ5W#a_&W_2|L88?soA~7HnMWD(W$|swhIq(PMY$%t<X{`{s?x`*7Yv?7UH2dp<mMq88_IfWJDcG7=;itmYL#y)dFzq3Pozs&QJEUqzAV_{k^R(>sEb%Xy1Z;oy<5^JZ#GYipXf9`EK%r=u0zU43h1-G#EG3Bv9@(lr%o*>yht^8@SufQk*sW+r*Lgim@dvIXz)e9*ouw%U=3G?Ql+V<?%Zah^fOBALC*<I$&=P7ZbsLKTF<s<vYpkD``?sZa!c;2v~|c!g#Nv*nrAGztI^uXIY=yu>tlw*Mt9cLZcCi(iYb^{wW(`e$c|1edS{NOKc9GfuPv%Of@966&L_MgFo`MYa|FxlFi^EdOU*RKtonWay<g2l<>D-T6~TQ=b`zM3!go4&7Pb%t?N@NRZo?gY{SV)>AzBQ&LtId@7yw)IY03zjQ!{A<xOnq{>m?Hh%w<3H@^*)ZupQU)5|@xS30D1V-+)XOAgRMH(&%w5*?d}jooNx?GF5C}h}~p$Fn--`I=8(n<N7N^a!U76YRK17R=qZeK(YUZy&1Zb|J0a+o6+EAF*S^&{n>OmQc=BeysjNE5{M+N{n4vn9{hZMCpC5P$VlpUA!ZT#gPl?T&8b6ZcL4<{E@3abzp<z1i_HpULCT>7j#+4)EL@rPVH=nGHQo_s|I->jYN2l4mU>QHHTw_NSV~h_&LK^NJ<dOISa0r<t;z)o@US;9eTwsK>ED=Km8zcro4xFPMkn@!OqMy6tEaYbb%c_FHoSAUN&)|~x?<}M(?pf_S#b8|>rZ}@;kZ`*O*V?Y%I-+^(cE{3T~kF;6IW8kJ#t9MQ?P|dBbd3DRqk;jPo5wgBV`>3oja>im~?fd=6-0UnG2mOv)5|caf;?KzOLwTehC?D?k6|*!~qAtJ!hsGa()F`Mn#L}er{0z0{$D-<mS@jCcv1Q)!EmCxfq;QQ$)S=j*rh{$v4Vw?PkaySBT2Eb)j>iGe;x?L~4;~X3znf8uvR;Qi#IYk^wv&g*Hk|LP_e{&xJx9a63(fE&!%wu9zIHVIF$d&T}0@q^U#9#KL*x+-_zx*s`hA+h7R`FiHdF0p>F{3imN}GYYw}x!a1o_mFg(#^g8bHC3W{p$<W0d^?$&WWanp%@42zvCE^nKGZ(2ouAX9GieOeFlqUxsb=*k_&g7Ztbyl5nV_GU9oSh3;z_Kw3=wNMt0H15{pW#yk4-9PDMY6(u-tCpiW;%-v3(3A)#w}wn=VClqJD9*rKuGxQXG4m+raQHNZ))0)Ve-8Ln!YlJ=+z3CYfT8vU&7GtDQS)GgO~FRf$<mV{GW4hVN&Y>R|_umnc5)xTeOv%r>Ooc_t{fz5Mzq#ez$2=~R=8xsdHcIC&*RNJT3hZCOU*uASmhk{CQd?Y`@1SJYUgwXJ#fJgSSm0ANg<CV0!>PW8c`GJ@h0qOgE+;kRe#?8|Sw|IY-+ZcQFJBBSLCm=1=lwxtoE&vxt<dI3dZ2JfF7jTYMbet%z-vt+YfFZqT5c5_?HB^jazTc1w-Bc=E5pS{7t1_&$5k_KDoefL(LmFQ2WVuw}TvxzQ53YENt)+e+mU*F!QJhX_*!;TW$l)vud{fEKHD%8jbJZVhott7T?vz(fgCvUBZ>N}u*ar-d*DjO6*7DMNMU+-<MK8Wu0`)E^zyd?#Pa-_@gmLRnZ!@!UKb3vZt8{3t6@s}u}j$fx3H@M>5o$@Wz>OnJt(#?WzFStIKD7OHTEfw4Rsq*4naOk#SsOl`G&c>)f5GW*azVG9ms8dZT^<shceKYMVvb3v;+#9PshtAva5xjd$LpL~#@yYe@%b#ca`TNE%U)7DG-^ue2A5JEB<CGN8?Ip25``6Y^+6TCbZBg4b;4IhwX62^3>7=Ql4~8^L?x!LiYb7Gm)2F&P%4*inVdM9=`{l#WKm7FJtKELQK70mWJKJT_O}*PF@XNObCs6GU74Ou@Bbd`RAnC*X>9-$#{Qe)Gf8o<_fgn3PIO;z`er=D8W^~W3>XZr<n<6<|v$V0Bq(aj+g8i{knBw+Uy-3A7ZmPYTRR27tl0#6a2L~fT0NAZ-9_?~LCD%*z6nQdg8_BF6Aet~y;f3XlVfXaM@AcR3>{o6#P{7=_MZ1yBw7cOeui5SQRG-3(D7(H%aU5|w=YRd{<?^@tVw_L8tKY}dviO_U)9TKh%eF9T2y-nAyFy!$sFyQ`qt0YVX{)XPscd0!)rqhU0n7?WFvPJ<I{z`BgRZ_bApm`emUxc5oi}={ohMgVSe1gl?@2Ag;>6PE#5>QB6HmAbXdQvW^vL5ue-hyWa^!<Nx6aDrL)o%hHNb7brOhM>7I69fMt{*hs85SyN^YgJ4X8Ef&VGMg-h(Y<eHC6xBmvfyf`q25S-riex{l9)V)ZnI%e{0Bi^!gBuy%f0u*=8|@-by8_uKCeb}2+H?tgofO!L5wk1`K(Y;j_lyf@zkiM}0Z^DYX~se|6yghCsOcMo{nv%hdk1{nM<WMct%jyzcvbk<8nLh?FxDzjZ+iI#={6GTEhsEaX6bZISX`>L=^7sXKHhg1mRS&}_<&dL^SBBR{K)4f3Kn$a)9AMSrIY`6$xSEHEADkT~+^(YPP&iC<->YAyeGGMPxO$m5PMqzgyf1yJyce`!Bj{W_6dp{#G^I95N<sh=xAjEcOiD5{zI;0kL>zP*cjZQpdhMO>6iXX5M8f{ZpZ0<_o3BNB~&KI^cOsi*j8|&(JuJX!8*g6I}w*BekwwyBfqpAYL&R}dS)StQ+^^+>xWRp-zgp)FEXRo!*06NB1n-UIlNLdHV{-)<LxJD~IXThjLw4#>9AJZ02`Q!d%G7G<rb^1p3t`h~AO$&0a+el}-DN<c_OI%`8<$|xGY6n_tpE1!&#sCeERn^r~u-&M@W^@?jwneTnrwzH}+cW3VwY`=HW2K59+#ssoGLG*%m3*ngt*iBrrJOE~g!)cpWXujoaD22+0|}*{i3xo-9PHknTtXE-_TA|AR<GcAYuzL&;QF_Hp^b%xHGYGL+aKt-4|Jxn#PB-==Y4lhGPuS7T{dJt9Fe^`ZBq_-(E&1(ovhQk^-hUX0f{TNTirJ1NE|azC5$eO=#njDpPu<<W3CCMt=vhYAE#N+n^@Xj<wj(L&0jgf7GSM=*QcVrdcluBUc}GOukvKox~7<axAh)e3Ipqx$hg%-RW(@Lv5m`+kXPfHZ0!+xp|}J>TffZ(A0wmugeQa&VW7L2wn2?S(ah?d^Yj_d_&gP(Z4}E<^OGV)N;80VujgC{iDDG-L$4C}etT7t-ntUyR4wFM40$;Dxnb~3zz`fBLYQC;&3Wj2%?YB@W!_q0Og7l0G{38~w{+q4IW)4>=w&Th-5NktU~Y}PHO3_*Tw73j<jbRr%|1-|;wXB+dV(iL_xe2+9wZCxDOMs@XXK}dZxZjOvq_Jy9t)TCHj@V-0y!*Aov$h--l}PD9ju3<B+@*m{VA_*V%#J(IR99$S)s1;d!)&W2zTsU+BbRONd}@vgvZq9spz>ur2quu!rhOzaX3PvcV98Gc))$`$I)&Ta%5<z_n#>!u#I!dsQg>5YYxYSD*N$p=S0D>a=N3>;v(9x?<yGO+2w#M?RUnm2EydjcLU>G^5dkQHY+J+8J~oYJ+5{v07j!U!(||MW6fNC{P^=mM=2fzCbsOKf1kyKp}YIHLP{O@Z7QvY{s6sq{{=+KvI<bQuj_aCd+Lma0o6db!W;SvqLQZ6RE_BnB2p)65&B7z9w-%^KWyS0uv%wh%JYF4=edBAo6nn=NzcDtjA~sEE(VUfrm>|fRj48L^s&0I7Hu0@TP2epu=jL7Wt!8x5B1L<KmH99_wn8*&1q3NohYMXv1oZJ&-PQJ9Okf47IoRJO;p1vlhKT(HWM~x?&I0JE6HV;7N3$ziakI*ex2>(J+#FH4UN!VoCqochP|W8y0qBDRNpFb8PeMPcvkbtEzJkIoxu2zRypVijZ_*~s*FrPG4|`!EEBzA`y4NPP1dP(2)3aP2l^AIUL*@_gOZKv&Rq62AM>4tpByrj=Nu09<b8~m1L|0>9H7}RuR@NtgPXhpp;D!8?@}<^lxBU?#65}v!HJMMO7SA#{Q`$EO7hKiOwIufK<}+UemTDcjd%CE=Ed%1NLVo71VteKD@fn-O78YqvA<=pp(xra{;s8)v6iWw4ZgUP(vUZVq`JGU0_)(CZ5wHk=k7=)_@NyY1E47rJ@@tu>^-h5nC8@UF%6r|;9DAijdL4E8to;MX$xhx)s%gdor6HC4xnxwU96L*7qE?b^1B+TD>cB$qOjR1m3EPU^K6%zajjf1x|#ss@)GRPpPO1s8NtcbYyk`Yls=1X+>0+vOxOpSUr#F5d1Bed0F3>;`Z;dK24lC5dR%suNnv1xJPG%lC2Nst*3tV1StzGsZR770bp(+V9iR)0Ol|I1_s9+Om)`aNDapX^&~dbZJDJMhH)sN}SzOn}u8=y9$82Zx+X^5n0$lynoz^J&(Jxbj&4Y2X8%^!`;z5DMP4pOHi+i=i*j*ql9IfAO#OpiK^l^t%vU8P|<&P!_Eo-uFXHvuu+Q20IAgzPNFx;O1U01tGQ3(ygPDz|=l4=bR9tT5FOL(Zm^Sgrm>x^XRh880^$j!=QlG|WMG1%IX0ZumuH4?g=Lzhuv0YgG{374QluanUmy1B8A1QsEL@kGYojmO%gvgktw^vTPT<e^hYDbt1)Y&KHW5HD9ltssa~L>JRg#liG_hTe!*Oet9I><2yYJZ(37Hl4bE7+*E9*I1mK#*(ov(NGj0vdff#__X>Ybf;^BE-D5YvX9kVNDvO$2Npbn8f2xK_YHkx-A8Q#%4NB@l?%e9A@)Dz!(BTr#}Ct>m)N79^U6@(=A>QXOPvQ``e#>6hnE3!woNUW5#4p!(nY@vymEeOBta=@#H+a4;yDQ>xfK#vt6J0>dggawos>aM&Bg6+g11OfYnYRDvVh?l%`jH3e}z5LO@VSFF*V2P>AsC!@oPAjEKzta0T+5~x}8#oVYDa2&hAj96}|}F;9+WzvrQsFAvOet6X>%<N;2OZ^%({kR&hx@7|1hC#B}S?$F*6R;DptzaGUjF%6&Yz$@FfeJRVWz)99ZMO?Vx`FrdGTi&mc3Whnl!YR%SohKwg0xJiX|wDnO%6Td$JsU1rvqZlgy*QOme=rag;E%jkEmg+LwVkLzcDs%$0po4%+ox1)IcIeu_Ya98X;C-@e55od6UZN_C2JU1Q!#;~q9lgNJ{ZU!PvQe~MRA@%FfesF%TZ{m;P*1ejCmp4zza2p%c8DcaP@<q<K@;#LMOUx9GwyL)B`a-XoB;Gm#7{)ng>lukL9QvwRZZTw`<+2#r&FVyLI;e3?7(cK-w|?323=LjBzfw!qMU~;F$k=4pGV?p#OJq9%mvfakh0W7Qo~S5!LC9WxJ+ZC@q)mKdS3>$3XD#bK;W~Iv`+D>wE!$>Z>-sMb4gbat}_+)A+2sb2d$VSuL6;LE1<*^fYZ_{Ls7~Haun)5^f^`l3-B2!!?fCr6!4Q=r8+x@dURz)U6ylj@3Q_vXkzZ%0Jl;T;=B@GfZ=Hjol|vQK&y9{6a5JQjiwTQisSGp_h#$zJjZDBaH!iHcv^MQ;?uUEec=PeoM9dtMhQeO0I!H>@zx$47}+E*hr7QZMyJS5(v1jH4`AGLM%(A%)PI~!!oy){Bx{||ws#A>0~{)lZceVp#%^O#^*zj%pfz4^tDu9li>hB_g*S(yhL09WTpe;s&gx+$yQ9<jKKi2c&Py{EPvhbm3)J9nI62!`yF|4BMMB6Sosy}wJFD%+a_%*V_PDm+|L~XiEOrc>u*_V)zo?mGgm1J7AE!fD((P7H7>@)4UkL_Yl*|c3Yf*GFdJtRiQBfubSx<1Uf*%3y!R^KOzkK{#ppCgL-e^jIOl;j}zi8u1RBbKy#-yNaBRi{+QGdOr{I$9^F?<FFy(EpJ#gcgzsJ8A16gjW<DFYT5f{sM)EVd)}+Fwq#)__+8R&Tl*L~m&}SB|@b#KgzS!X=o8YSL8iHoICMA+Xs8()))8XCrD&CqYS}d=_>_7EggrcW6Oq94ZsW9Cd9`y{8vW7LBo){$<!q0n!x3YYaJ(8mFc>Ek`nn{!P-6JT(J3H^Z52)yaFtUX()-q79dvd;g+Xh0%)PmrSx!W|whj%$S0P|FHNiXTf4<;azp&0+hvA*EJzyXnI(QCNym;y`Ee(|3tW|Qml304cx)dPg}dhI$O<si6<Pod`jehSQ8g)?Qsz_G37D%4K{~$@atQ+ujLa2cmiH#-;S1N=+^BmO-!Ca2aMxBxUVqav=VvSBqm#=hZD(ZA%j^a>-HKNxw{rLmVb2k#?bj7iPh+8sL^G=F0Hh7*8^Xbe4Hh>L1ol4oRieqwuov5IRqhB4`%haci@&OCqU9zdrkRJ)RfmH4_7iGulS8t=xB1rShkZ_om~kfr@)|=@JJvCDS-}X-tdiJrsJuz(E*0pGAX50XnG*xeop4h`vm)!Z5Xk65x}Hcz-Q!@ie%O4bc$H}&;RtK#dO+l;PIqdMe+iLTC4Z*XL<o^(OSM1ZMj!3POgb10m=5nh~l`_^4nAj$HmgV!P5ApKcsFPsjw-<;;53+EwXyq3e0Z*D|yJ_^TB2yk)GT}t=#d2IJ*l0)wLh6n>8(K{YO3frs^OD#Ze^c-CNJ=wmf2#b1>nh3eN(jS=<V4)Xh9?%OzE{c8oyewuB{o{^nmk)^C6M_|u0^AGLA3Rodpy?|yv{<tN|sjL&c0;$&*3+v0ae)VL@E^Oi<ckMH(Dvf^ZyJxq6-(?OM{hvVcM!1Cj8Os7eJ?E=Y(4+xvy(H}+S$D$4y_|r`NgKToQIgsKWjzw)U>zI29+puBUqoMLl1+u|l=hxQQlU8k6NhZbV7zd+q4F;tBMjCX<Efpm&?xlqxEb<wo6pu9rju&^$%T}OtkY6754DJY=GS&+niz;IxW`P%%ST1W@PGnfX7`tz^?HcS^*;osak5gI4(HG0Vs;-)%TJ_nig674#2#wBWaQ6zmZR{F3zqnD?+KffHvZX@A`m8#mGQcZ)?Wfm@7E$3t#-fHW9Vz~0!NGZ-+?)`e%Sa}0O+^W_i>|BN;Lq-^fM-3U=hH(si&N7aVjt%a$D(eU>>QqsqH+N0n5L&g^kml8-ad@mz|_O}EW;CPI@x8R^%dR-iG{aFNUnAdu%Zmx3TWh==xNo(GG<w}<XBW^lb|OieAsuLf&BxDVNkFFAeC{S)R5aJplmc8AlUSEOiD2l??$PA`RO!U_Nk7CC4-%whSc`z7et_^$Rn1e;x!h<Yi$+IWC6hSi+6Y`r3AGn4yXCwG!j*oj3=siT{w!N)@IqOsA_hWDx$D}_laE8I4y_Df?@S5lVPjI#VWY`sBW9g+A^6M<?;m2!MPd+*7K>M@VBNqG4f!JP~eQYYb*&)P?ngmu2~nh4Ytp7&Jx3m8FY+RlZ@Brp`|`DRX{50JsQ+SZi63lm60Ti#d%4|nvOu+30RQd7YDHs{pu=e>IO36l)MLOT{S8TTh$5szGO?S_wzYX{B9GbOr597)I*$&xpl)nkpm^~R|*g!eSzl6+UyqgOZa?3wFYu*03q18=S&m2`*3b4TDmh+f?{owo#VM{t@8xFf+}?Ygep?tkeNlIyg($4H~^z~P{t8@9{h4(-_#*q7$kEnHBCks-dBCh*$(#~e1;}bub1(DA5lhv_xI5A?BCEt<KL}5j*Hsd^Ry_32YmXtO(83JcBE3AO>j<D5|iQ9%iNd&C}@vHmF+f}=NoxD+#%-&%(KrmZ)#V$7aXjwTYLAGii&zdBP`fPZ(_DH{-~q+R$I|>dIcWTeJea@Q82d9I-4_qQ2Y%qpei0we;Z|I*r=F=LLpo`f-*7q^tV9|ha?(mhb_vM&^AoE)84p@{y^i>$v~dLRyBw&5is6KY>F7}NPs7Vogzf)h%$SKYd)8^6h-oN-iNEg0s<Ud1dhGDLIry)isMzXhYP7-AreayThfn!nJtOHELdTH3Uenkl}HUY$eL<X!T^VOE13$R<>4f^#l8oMN_tOLL7@)3YZa9$=g+8q2&=-M$thI_0&rtU?v|}h7K2`^s<ab2k2OC*X|nmf=P&xkU}w{ssg+BUltf)Oxn3fM>zXTHiy%=%__>4<4yZNWC4WP}5{vygOl`-N*7;JWTMQ(F)t_ytO4iQps+0__4Sjin8%$QjJIV@du@q4Z#PiXeRg}O3szKaCfaXtXrpSq4MI2pWol64j2V+8KPUKzX1#V_$0&BB6Pk<H#*3CDaWbY2zTdIZS-T-7o8-0?+^I#+JV*hL0W72HU8Qg6(=_RGtG8JX?sMZW^piy0jsiw3R<%ivl3|X5_s%4}a)Z@Q1q{?_<Uz3qW>}^sCN_O<!lj3mS76y8sSEu4$Ps@^OS{xB`sSk@T7vD1ab(kS8PHqHqV>oD6DFDXYs{go!1yesa$MtrXVoG48-3eu>(A3*S?jac%eLx)`mU^Wx6+IQrrPJ_reXM^26npAdn?8oj*rYKwpH4Mrl%o0!u8yCSY*-CdThTF2OM@tqtg+xp_N=C$OAN9_f}9k)j>}-CWEX47h)8)W2ekN1c~#i4cboN)tIZXy?EtN$x$n<5z|jv}5-RobQ81cIG}KHM0ijp~*=4+2)@UN&6>I}m&JlwhM4BdGS(svTU~$`Ff4>or*K8veulHAe@#|`j8Z}Wb@Y>!ycL3ieuqJGsCPVEMOf0Qv!n2dCIH&ywtJwRX=sI)*O%Q!b7N&EJwgkO{z&wm%9h{hBpXfrtccRsp)$45-)Gkf3d>s1az~sY_i#r9?dGFSfP5T5!I|<CXEn0o0U8oHh#nf!tb!A?r|A>gR>f75%NW9SlX|^k5@7$&>1P2x(Q+hh(q|TpVAGs<TM|Fd7%<Wc66Q-Y(&z@u*_?2{tu;mkId(u>~?v$+mzLK&@uD!v^kmW{}wUcWV2M<6}?tRLW6pDlR@sO$(<*EuAJtlMQ<C%5GDqjyk-Tv@9qN6ZP2Q}B8;?L<dK+x1Av<A*jiT=be^x_U&(h{d>bepHs&@kUu*7^%WGk%+f$|j)7hWJU?-73-p-cQ;|rQ$XFCyufh1tR2$*Vor{ZovC)U%R^vq&ce-w6rzpnx@5-od}d}-Gm_FZQwZh>$(_rLUR|>+9p83BS<AFQ$1VYqtIHuctW#LLe`+n&af_vYpGRdrnzh29^aiAwoMYCOlft7mI;j%=H8Yrvw8_9;vyw-=%SAM<uDJf9Fx*Qe?($%KuuA4-c_AEi}4k*Of1X+R~zRl`BhF+QPwRHe-D!oD4x1acow-;`D>chwax(F+fkt5I~G5|EL^6-nx6~LPQm+_`LW;*oX1A7VcK`hQkL624TTGVT6{CX5dfPez$uGDa1gt-D0{FLd<oilf_(vbgYQ#J^i6M~UYKf&vaiQ;xVn(dUsRFDTSFl_>KYRLUI<o5@sZq7S5%ujy9v)r;EK$t2o(Y99d#ZWca)$?63uQVenGW9H=>*dv2J^5OfUqS^v*=4&*ZGKd#5%^YJJmz4j*Z4H*@(^d2KWoA?8X&2)+^DsVq$o>S`evOpzT+pREr`oW_?a^lWa$%FbnryF1|^sN;>*%qVXqgqIjvbCxaxB`Vb_Ls8i&4^&+sY|ra2zAl?|d6>pfQ`^zNJF80Cp&?NCGueEOCfNvn3C1q@^1{!6vVG7}lD!*(G{!O{iV(qrZ*B7@+<OYv$Klg5I;PW9j=*FQ0V4_dzqzSQz9mtrd+Gs2g@7&f8en(K_Gu&nU0?M6xdrE%$oy{)MDW~~vtx2~kZASECO$cP=26CcS$vzaAs%v6QLYIuIoJlgs`Rny1%qc%*FDGtxp~OOhO(a8&L((1dbxgtTIHKc-g>0%6X_CGRHjC@FAKJKWIuHz>LS*UE-#x?@0Rq*o6QsBCpwJ}OBA}J>yYx10{W~kabo93tZiM?sZ$FIFH#L2JZK?SBrDtIDO_6=ri=3l8hp_&wqm0`Si{w!RB7s|JGa>={frWO&~rjl@}xD2o6+^5*0U{|Y-e@k{x@Zp+>*O0Z5{Fwp?|Nd<{3-wYP2?T4ibyv`j{cH(Vca*+Y%?cVhW~KZR%PVvZGUr-kIa+&nF(=Ym4fR;8^pi^9ipAOkzs<9KrHB3{<VrQZtP)tA3w<?^iQXxj0K-MR4De-2~>M@SP5xg)Kxu`xTt7+i*u;|HJoeh!%tH5Eqmz2Ef*Qnli%X)Jz%yF5Z0Lddb8AbJ-8Qyxrj;Y{&Jy#3kfSf>l4;Hz1P*Nb0bQG<sZ1HlG$>XIg}}OcmP~VmDbGj9<5#&TTKtxc&-}oYH-i8uE3NRj&;qQ0%{9Z-(yVKQ-pyW;D22ObsJxe>Po?R8(&quWJX41R_amfAlJt2S1<RNljfmGLrgTh*`w`U}w~SbLtS<T|hyKOW4cqZ|v#$VzWY7ka8%2V-}hx3s<In*v934jdz6E|Fp)BTBw`1rJfU4&HjTmmeN#~b4U|mkMmC))|<Ozt8#$?JnRijpW=L5`Zp$5rRpcZW-oi6(TP1FlVuL&>ZvVU9igP44e#8oQo#SLuGo6RG*P8}7M#8L`jg*eIIfj{lZ~RUvOAJ}H22+M*Hn?z#FdnBj~o*66l@{V2xjhOm3y4XlP3trNLdF$=gz7WCS4t=xgT0-=0fMn?6sP9oT7P*uPb_-UqS|(`^n8calpZE&zY%)oL_;KQPHBgpBvP_fd57{xw-VX2{5K+b@nx3E(WL76j3j|<Ky#K@{O`vyBYGw6{0e3UFcls%n``|ky>P$8Fav=#{CYI6rympWB^Y`p^XxgP?Ea#bD<Ci+)h)W3xH{vD<(&4n1|lA^IXReY3dL&v2Y$ax0@Lawrnc(Hdw*}jM9L4fccD#!hKBLj6!Z~?zSTDJtW<xG5HO9O_gX~s6!AL-%jQx889DD^8;)_?DD9t548_$=jXKOOd10<Oj`bFs#!e>KF>oUYv4IiCg^8o2X<D1coM5EL&O@+s)(3M|9RlwW0T5R3el+xEVo;@qDCxyY##$jH9CjFrb|(ss9&6HX=(+F6vy7?HZZ&k(l?(0wXToO5XyT>&vwP1Nv0U2Y#u$)YUhsH4Ao~(Rbp1t7#ljM;rm&pdf36^C5jI`uBmY^vkmEYo(YO=FTZ|DvEY(hI@RQ2E@b-<PF@KSQqf9BTb7ZyYo~aWBnA&qyYD*M6*X3AZEK!AkLqGC02mXe3EnceQ+@EKjG*|0C@i2{`0W`w`|=y_|1-g{Ta!nQ$Y}Wjrh_4?ZD|DPvmLvIUO<tU!TTpiqlNaq-`^MIEZJ<=OTHn1-Q3o4Nrvdb)~8edNa?-%XK%2u0m90%q`?+?-@TP*CHm8;*kM)oY@!R1LM3mZ^$9J?*SEJR4=v*Iu%pB_<*)mA|6y>l3N<nUPa2bYD~YY!ET<;r$y;lp`VOdH+&&Dy$_7P{#nAcR*L$0*528E$KH5|vZ%M(S9O-hrB}gs9F!1C5T#)DZ#&%_1{3S}L<JT$14X!wMr+f>wdeDrZbhF^w3$70)$}NCoOT{*Ss=PQC9J*~7sya)lvoR_V1PY0q@B4Ts>Qqxoy;z`q-%R_8EbXcy_r_|^q4Rcp1n(Zx&<ze_d~!Yf^5@xp{=VtUS9PQ4ck=whhm*<OI3)#idr2(N{<XD}_5rS9Thw+9ILr0FS-GihI%#U?gCWh5`>BY>T8W7C^r<e6vYPdC*!cbJe);h84?lhQYPTP+51+x;&UTq}Q|~qk{PL~A2~@j7#XB|f2<Eg6NcwPp`t64wzyHVQU-<M}Ajl36j{47#U)v+28QpWMI;BFzrby1#EN$#2snE2IV1H~BrntRTFH-T2n`-YS)jyA^<Pa3<!NEun0Cww|N4s25$@LOFMV^e>Ml$OMh$c)_cwsqX*ggI6d;Rr0`<2@b6fn1K(Qafj?QZzWYj*oR)u%8c%C2ux97o*F`CtEfx%}<E80S;&>i6-qEdHkTw7PTWvMr1n!dwf(uFzH_>gCMgs52Q-+Nvu+DqC1wbt0@o0J8!T3~_9e&VS73psO!U2tZ$=C7vU1=Zzj~=gAcoR;8ftds54=II%Q3@y;{k#1pOpT1Vh8J@R<apG3HT9Qh#6t+Vp@P`2z=4RBj<X){TJMHuP61GM|-{nmfc&Zy6iW7=+|*bS&Y=+1t}UEY-~<bf4_OC$=`l@f)f&{@6VsNRmxiDDHtg%iGX4U5R0ZLoHJqOi*d5b`l)N%-6E4|Z`xE%$$WluQM|j+inJa%^#Hncz3y1&K}`X!9-#<f+5p+Jr(Ii+2xr+_S%MN*EaYF63tcz>Yjw6^7PJMS}D?nkw^OV2PH7kQ2m4Jj{zxOyor@Yx}CO+!sYv<A+p8<5?m;br#E(a3Z7J#?!q({+bao!XNH`FSNJ_Y*(Ya%PKA!G8HNf4bb=Tj_R7J<1}EePL&CGN=B)79g(3!EqA+Zzm6k-d&55?R`Z%1Sp_1p`yfPnXNhV^{5m8Xb?ced_>E44WCoxxf{Guo5iD&}SZp>+;R(MlT+SD^R86aAcpK~L_OkK{N!U6D%C`OK|6}f3mRw1WTz}{+n2*TEvS+$%MrM+ZY^G&g-v9rL+ufDPA|v1cJd!1iSue_}>yYt|a5w<Jxkac9Myb+-*g1`3gvQ(OrV3NlGufn=5-X+5vvbsLX8<qbK2C`Tb4X$b!~R3}WpWp-d^rn_9U>a_4E~&6;gnJCcP2CNM_bD`t#_R|!2DW}g*{rj*kzJhAuf3mo4yx(6jg!H)(wr>STas%c&w^ApMw8JEjOdXAh#`Yr8;fMC10>Pm%tshVHguHf^dWQfXg_398@}{4Y%&rBuj%`90`qs%F&oLkzo61<pvT;zfu*(VY*n)JvoFbd>n__t+w6(^wzjZRKR`Tj+I*$YS#P>5x3va`E2NtH`qOQ`uH{{S{l5MgG`{nC>_K_HrL(bggR;Kv0?=hDrlSkC5CEF3y%iuZjtuLnegTKXcH5DQ^uQHXx%Pl<j49tb3TqkUvgMR)8CF5jpLZN6{N-KVK8e{KNu@3C9>YY#SbE^_MHp@=kNtQ&g$@Jp{zvVY-*Ru2C2wqUA5bw6V76_qlJs@E6kS)wJnNF_%>-67(YG7HRD6=Ekc&nOciYyN4t)2doJgyRny@Pr(M?$7H2eJ@R1(~qxQ35l~s_xW2ij^U7Wg2gRNBL6}EvDP&+ba!Rm9NRfa!s8?X>tx<m5BUZxt{SQ+?`O%cBE#U?>9Q9Hy*9DAH*djaHki?=qzn0J!Jdl+HUBLqYd6KKuSL7Zp;v!0b0wrKSYN;7dKtxDD#P-_31FiS1SZ%4qB8$sCCa<)}oA&-^a6Wcm-JKz50iRLP3od=gnO@8of_-JVQ(xx#_@6I*qLNE=n;`4r(rz^yC_a{ccjzZdbzVu9Xe?s;2Op*T4&XRG?=OjA*vNWuV>mU;}cS(qVmHAclw^*1O)-naHTwPwZ@>6GwWnlJAuR+kxE#FT1Y-TcDmNQADhvwaWFo4!5A8zU3`rw^>{PpMG4?;&Z5ttfs{{3e!DnVxZsgRTgzMI<Bp?`pW_w@}3FttRT$H$E)fLsQ{guiJBcTGe8f?%Qw3pBbzs62xLc*|(R(+I-ilT986Oh0UNdAZQzJey9k+j(Iy8H=`q(TwZG!N7rQnR_Zdg}zKLf7Xgs(YBF#rE09rdd_3X6nyz?>VN+H`43Ee$9ta?d_@v9Ax(lz^Waoo>{+8M;81*uD%ZA4RFWabVnCVgGGT4zZ#;W<CD{OF^GTgVE&(*|6>=l%Qi~26zMG>s5ft|v)?=!*UhxuBwV=dhNcHY<ua=uDcL%^fSbWI;8`N1wSl#Pj*&R@v_ZD?xMpA5_<AHCpUahwOXzFyK=5OkUq-Zq|Jv4Xbc8>X+Cl|at$WXp>x>)D-Ia&_LSEG6WExterJ+vL%<Q)i=5{rG>s~lZg64?U9vXtaYiWh;`FL*FUIhn<d$vL0_2(r&_ORs+kBJBC@S~fe8PY5I61VyRpchIJno!sq<;!jJtp2(Y2|E{M(u(p0(492yzr${7hgU-3-_uAl+Z5z2F*Wrqm`qGYy0npSET}QhI_8wO&m@-4O9EJ5}@>d#wjdL4EE?Q!&=;o`9&E=!)90XEK`nDW%HBO%5{%CdaD+Q@5HNeTDu-OqCyGX#g*kUd2KMPvdQV!kHS$6B!u5wLAaB~01ruJio8CX1<Z}!_9T8X%XX})<u7aIdG_V@1V?7^AFv>$e4Z0j_t1y&h+@RzgnEuubf^!`CB)S)77iu4NoNgSXHv`lU8*h|O_^taJ{|5MI`U-jZ@QFPLk$uD{&8Ff}=243qPtR0{K1Xodu-sSGJPTP!eD;;Ydw42>%YR^{_1qL@!w}TDt-7+|Lfw-`>ehCk+mPgm0JDie}r?hSVZj#WpC*6#TB7V@KAmJZUB`JpC&iwDb+d4l*9ER10IM*aqZXrAlrb>->scQ14EBw1w3tYkb+3cxj`CMde<<ZKcv9oAw`@{jyaSnGRTr#I2<8lI;1ilNjGGxVo1}&WgcUYI0X<4%3DbUs~PeUI}pffM!zLV74F(+ohbNi5tdC;ES)xA*xji?zKIwY8{qG>cD8Pj-`hXFywIZxVT_h#@Z)3&Y<?KKubr%`6?`7>4WK6cGAc%PQ23m@9;f*vOu^B1}dki+nFSZ2YtRH?jaoVx{})e=yT8E{pYE6!g3B_9ae5j&ntgLq=Me#yHod7G2gWUoCGz|vn`qZ+i3sip^|$CS)xs`P}NW;BfcOf0OFOGP}2yKPL9;Fw#%f;Fm@+R$5mAFOUM(DQw`)kN?Xsnmx#%OndjZgCD{<i>ZbN4hCc)+8qFSQXTdwkzfhXPN1@k&QF*W7DlmI!&|PA$E2%ZCU$6_za#(hgED6BMMO?(3}NF{gF${x8p(6B*Q9hHwOcG<~Nuw^!YqCJ1gvDl?FU|tt{r7=cTw?DZ@tyfI8pjQx}qlFbw!!#&VX|aha<B*%U(SJVWN24cw%{I$CI`A&`H~fb?ahol#sCfOymT7IY3m#!Gt`RocwQV0pJ?ERF#M-yk5<CbfSF>tUUrb+mj^z&{zbr)Gf|FQM0>fjjBNboN5}#DHb)x5|>yM$vYq-Hg@-Iyj8lECSR*70BW@=`3Ai><Ak1Ml5%N8U+Odnt(4Ux_akzXs@qTGSW822|%BWk3t(Cd>A!bjz;dOm8(jsrHzKdhLv0AI)x7~3bKP`Bi|h%+ho#uOH$1Nj1^@=WGO>noX0#8Pa{6RSYa-hE>miyCXyO3{EJx*%_oCFojVsV2%PBa%OG8W)+uoWJ}XIC5?{v!U`cypE$%ayRNSDenN<C3ZaoLBD64JN#R`m2y<Ch}f{B+NHR?X}*;fDy@VP2e*=?>0_)6{oo$W*0x>{?OWg~pmG=C#Bu?%j2+jt9c#tD~Zcs2Oe6pI4*;7&`z`yUW&8egb54llW1_72Z$jJ8adD!GB#YUPYC+k#eM54?1yW$tJtu)_e1BjV%OzUV;9io6`Y-V362iUuX05n<{9w0p_8{yd%f&%H^!a9A428t2u1-GbKv4i!kHB=^OpZLs5qWu@nXQxJ`}CG{YsnA#tR6Hn0m-Iq_?9db%;)kBSY6ydb%X}xu%8LQd&a2E@7=WsYVM_Y%4j({Q|<dBw#l?#c#0RHD<Sw{_`J&*0LfBCQYEOr(+VVSw_{&ljc;Aj&*cZcw&`&T_-JQ56iCm47orV|UT$Lr0g?`y$FYtgJHxL0F`aJVae{hy!zpmx;5Y?^}<Htvfr=Ro`0*ckj77au*+3YEUsTgqSW(<X+`K%=+h;^<k)JPYJ_fgg?C?NbH}Fa#Z0-H31<x!3-7vt0;0d04yYS`fXbkXzmE0TL6RHHTZ!4^;rE-EFpxA0e>W2^syvgR>E}+moQAP(BMgBdb}U-JN<68i&e+F-NUBYWMWU$)YhfGrm(H@(j{cvNnbsN%vFJww5Cqm6f%8NZz`EoX5ghY(L7cjJ*&_5uyz@qx<}z*q_mg;kQh(Qf8NNXv~;`#`|IO%ejKV(3ZUF#N|~MqH*0528ZSgOP;N<ip3l0{pMDaN`$K_#o7km;5it+)Ak`T&Q{@E@)8c8d><<O-V+yW`{E*KV(P`<7q6W5$=A2=x0X*3FpENcmpnt4MfWR3;N>6TxKGbl7;svNyrUDvw(sFYaw=pn1+;9MDjqC*t_4NgpC5d4`1l}+)#z$y(PdwkR<CyV1->g|Im?KH8mwnHC#kb-6KV$81Yu+kdiA__;FhU7K+;&J+I*_i=B?!6PFm!N->5=IlQZVJRJ*F0N+>xM2DODp0zpU#bU^clKL}<z-v%2UpoQs)$x>(ayL80;n#_5oc)uQAN5{vvZ6vX&5%8ocTV)KHswCF!c8l2jum9`Cz3Fz|%yU(5zTKEyxX`-$K7Y+9;4Z51>v5xd_u$N_BY}WtXTn5r-&(_NYM$d_Y~L_6z9fj~$&qiH@;HtZmah2fZ6mOV5%38`_<XRLNu&<8p`p7z5UV>7(2x5G)7jHT*#EA%?@|phh>jvuehKUtyIg_}Z%x=1Fwo+{ar3y#DB=%<5D^?{eS^6EsfB?_Ec?Z*JklT?rs#8}EcRKF?e-*+Vmm-0E@Wc4|NhDU^RxZ+Z$JO`%WpsR4*1bnzQ6wV&(&7{<!6%h^_LHjfbPX(@P{iVWt4vU$RVrgd;FnURx$4G(Wi^%RZnN;H{>Md>6%HE$TSETD?SBnZp(NzB{5ebY!Eas>l3oc-I_^?csW<X?Dq9e0M9S<268?P^K0rG4jQ|>*I<BDu*>>UDMHIU8TEWH8t>N^p+jz2NP%{5J@jai%pp3&_KKrX?$O9S@7aNJVZJu*71<IXZET}DR}yRD<bem5tlT?s=^-98ppC<KZM%;3tkzf$i;?qq=h?3za971fg;e)-S)useQsB|vOzvKxw~Z|j^p%}jXf#(^ZOej*m7jH5Wgv9+*q8S@Hc{6{Mj?k-BvC%I;9xyFw<KKmGJX-<P*Ua?WHH+6d3|<gb@vH8{h3;U9>ZDKo~BgCIHfvQGIFw)cy^AuBdCL$o)^)bxxe>5VpI=iv(9@No?+!?t7O|ty%Pxx@0E~i?jC8CD%}ck<Spr0_r<PmS@P&yiPcFM6!Tx~+s{aO0LCRhyim%j61K~I0#vkN1Hq<mqg0BTcy~+)w!K1YWxnj7>=b{bYp?x*_!U)Y)mk~<qElRYtdJ)Q_ilgq1guiVSj*X?<^MD`RV(NdqGlJMVqm?g0u~}~XQ(1Z5BNQC&zj42NhJ-%z|57dX%`c;`ElOSnZ2hoE$-#{zk_o%47HbAhYq^UV=yjdj$h%ldFWI~Cm3AJXV{d<9gQ9H6ud<9VnQKf86_k5O44u2MN@iOA%E#GTX{5o&Iv_HUW?PTk`kA|>k6zOzkm=TXZm6@y3`G<#Bl%!%*$Gw7S{9=>-!_CJU`FpgcpF#A2V&Qnx!5hZ|qq&ogKO00C1;}A+lTO78+-_u&-$J`Q;kgu>pi&<F1)%eP7LaByH)=O!=$zIhfAt&?|cdZw00N06a3H_sH}jp|%idBo4qR`j>Hpu9L5h_Ln-u3xo8IWiHC#%z%h7Mg)!E_a{+jopWoDze9Y2D=7*faf57M&k%O?Z+cQX!4-AKT0!?*u3QFyOd+ld$&}=d1C6tp)}%n2G`Ah*&fG%98a2erM`vDd_T!R(Y$DLlF;^3-zj%OPcl~)poUg9RsDQ9AD<0Di(c1<8sbi+suA=Ss4qR#YE?j9-aJaCLTQa~>{0VPhdR{Trn`J59NFzic6>iBvIUc<GN28}p&KK>&FUq>m>Q=gd;k?a$Lt{m1;Cf-3MMRefXm1glB8E*8APnKX2=6~)cpu`Ur)ucv;Ue-!+-w(6>);@84Cfu@;&bIWppr)1p9cH8SXSeb*aVi@mI&~I5eDcoe}twIvf&2VQ`KJ>a1n1M(|EN$oaDAR_dsP(;JH;O^nw=yqYm(Vj@n7s6^>0#sWuRR8$+_fY|FP8JlmB}QP^j;JO^cUXJc@Yft7nU?HQ?In*Jp8BjkD^8wJG<drlM>A+Cr|^bs0nphAQn`HKT;I?jHTzEe!Qs;NUS#;L(JUu<JgRy^;nd?W51Rgi*<P5KWwJ{D}S6b}uA`O#HY84ds@LtL?ere~laEQF9a=)&s61dtGhidN1X-sQb+CVqm|X4Uxs1s|*nvD{>(6k5rvhgRQ#Z$ultNUH*{5xBL&J+A0!mO~A$yp~gwa>pr^IRO&4p$#;vdooo5*kTm*UYg~m3UsPQJ^z0OU>QHy*JR|#`{<NHm>oC$q!r)yqC=nk8dNy!IfqgQkt^0Y?O`$G!d}Mi4inJT$&Ju&j1ryR4`4C(x@{iOLK&CtaNn*8P5H6379?lLylk=+sL+ot+U^1&9U1+BI%6z5QQy0}RMo!Iz;}D{e*^wq#@!~cp_OhDDZ3A_mbFUr0SxGlXG&HOhc>$Cq^EKvia~1>xyT~o6t0QkxyT`vqTaDYvLwrjQ%*+eL36<z(e%58C6td|PdUA?s5J<PE!~Bfjt0(tY?CM(Ag6*6ZK9@T@(&3ABA75^{^spO&dFErCx%Rj1W&-vFx~&a;PxjB{K`mP^^>@ofIsq^ul2pUsEMP3SBL1eB>T~UJ+anl8r4qT#9o&suv?@Go)&~`!t;wR`0yEM!tW(1mgnYp31SFAf*8p=I5FojQ5J;nM5|J+S8Os+PZcR?hwpN*<in_pKMI=j-c_`fvjel8K4#@FtwP@}8V43d>0a8cHZW5VMnqce?d{|&e$WGHu{FA1tf(VO2P;G-19h@Woj=prawS_w%EdS=ceUDtBPjjMi&UcDN!bqD(t*~CP058zQh|Oa!cFc6!i3OrBTMz>ZkX4dC`ys$br52nQhHVH^q>J|($_KW*>FvJdjSpin?DdIhf*&3z`ewu<vl=9=`w!<XQxDeVx)R=8!icrrOa+Mdm0+%3;kOE!Z7hax}g#dNLvxlgk3%)-Qe@2Eh<~Dc|&oO#aI#{!@Rw|%G!bVJwEn)Hjrw$PSDa<HLaA*HNFTehTWVYp?2Un`Ok4N)(K5-l)cXagGZ3c)TWtR@J69(!ni|=A!6&W%4b-Y#nRNiH)R<*Sj%6J8MaLlpiI5$3^x@TDJ-LHr)Cv*PQ*pZc+o{2&&y$%Ttg^jLjR1!;DDN<^t{YHnTz=y#!xKG0aqKRGx_?cQVGi?;_qP+0>x9e2~RZldXJSwUF!_+eH;ZEzGLwd%)(_f-uzs6eH47QnI8*o!+C5JFHHN6*=nKQOH;TxsYOW>Gy<?`0-UmvqJ!A2$6JKeL`)FY69kQjT3Ds6KRcZ$ZQsS$Fg+n<iIvv?b|c3@rEHHki^6!+#Ux7a5cH5DCb`3}QouX=3-?PPjqI5bx)ii~Y@IsynBZ3uXK`l8K^;jCcAbW`)^jfA1g)^kgH7cAOrk5hiP}X;S6{hMY$feCXAYl|>PCGLmb1zj;X4>mwah)x=t6jyVm+2;+!!)HjSo|J+R}@jt#uW`FA74S3634sD3c`woEUzy%0~pHF15}_k%X0pt}ZloX8JeZD^5OwnD0?nW!T`o*2v@GLZE<XvOXY9yAec_93AJX-X!Z@JUpPcAY3}hk`qybr-Z^0tc2duj3NS{czzsVZL_nMx<n1kyAhC<(1SSFmEx}?N|;YgP$VbpQGI}|zSzf;h=qNx{@1dpdx9KrOo(91Z>zK9+BnjxZB8EPY|f*k`nLIN%0_|6QAOz}T)1#Fcvl%_Rl)}MqE%1G9J+bP#tUV?^_@-deDvr52-wOO{Ct#lJ3BHYR#BZjIX*1d;?eqPLsJ*jetrY9K8>z0P~L1_#Q<U^`7}h~`*fdDkEVcO>-(qJDHLm4S88{<g2IbbqX|!jjSUaWUh@>ut>o?Ee1Z$Us^!}dR-abG-C<p6cB<RA#SoB2xj*=FLS6EFJF1(}eM9Z5?d)tPe&qf)J)K<PUX$4lsf%sBRRx+n#%Z%v-Kc7VQMSoBZ7iznbEd_>go5!Jz&}5RVz*0BCyRp$a#*`{w29?FM<M#n5~F9!jROdJg$`GMvgJ1T99x7|vGM^NBJ;{BG!^1fJ&i%J@$CQT3#h2Ko#px>=yu5x3QHx&r;TS}5U~w^2aW8}+}U>}@n1^BAwn0*3sjN;a<<$`#?75BlTHMUS6sM%Wa5hDw!j?N<Fx<}VH+pls+y3h>8iw*s$f04Lz#y`(vw~!^jUj1-*a0;(aa&-H>Ef6R>t%@SJY#ROZeap0i*hrD*g1^V6Gh-MCCZY!`>sq&7U>)j?Vazv(Oy|?0#>C9KEUCI9>%47;r?k+<xm7W&plEzmvKunq<lg3?VcUKNAN-iOxw(Xm<g-D{kj6E8(%(^9^%_J0fLsg7;duJXyd~Lc{u_JH}h!9`6*hYHSN%^^i*+ZC(;r(D{Wel+z^~y5!n$!VEW#DlS8^z`Fn;p7so;b8$v6{Wm6erm2;{dN1q4(T=?Uqjd`B?)gF79k-{pc(K@OyDVC;sw=tONL?gvpRH$a%JJrxY>rj_KV;eMyR0l_ALZk4`6;W&bm9ujJf|G`bP2W=DWbECQlB5^7v;&qp<7nH(YfO|$8{IT-V1=Yj8iXVUU+tym21;auV^~w_X#+cx6s&@vA9Vxj%4`7PBY5R<sC2_HDFrCrNhY#ya1^)IX7T8k;_!CR^Q*|!(ii@R`T`x`g%XMeA)5d+K_y@LR`nyxGt4v9<e_VIZ)>RK^ts3{hv@vWpHQPAMm^x+9)wwCh6|KRBm_Rfoi&q0XQym#pL)G%QU*{JXbeGE_H~ySV)oV+hZ9`wo5F1f3QplXr%!Zf#oxInh-LlHVWFYzS{=GU%~6qjpCO-Hchd)#E4)z{yJH@EX{mG&JV=}1I^>)KB+d?&d>SknS2YnFsYQ)bmn^Yw_c`1-oblBnXqA!&n;$Rw=I=e`Cb(xQyW7MK0K5ypUsx0dg=np?H2A168k*c$3W6q&*9o>S*?QuWNfOlEDjw5&!bJFU|1Psp1y){!x)_^l(LoX|BnAAnYNIofb@)OpL=u_QG@!Fs<i3G+)-H$-`FyJ#Ev2_`FvrzO6TroThuST69|Vt{`a>OfiJnqQ&m2e%9Idc?2XMLwd8c1a~c1<eJ0P67~w%|U%QT0i;X>K`-+n<v%2alNXA5Nf?pXltugqgj5hg#F>FBk{Noi&`{O%4|1;sTNAXLJ(P(o9=JFwx!!#!JiIu}fFQCY(;qxzNqqO+zb-haB-2Ee8?!YekYdun?Xky#bX?%W|e7)FyKurb&nxz`Uwy{57E3ZELpHHW!9oAG8Cmt6mobnND-_W4^`Rk+0Q;&5%te0_g`OkfPela*%h1VJZER9b6s5!JpFH4uN=A$-Kdk3^XJpLGdlns-h6+`>~HQq;GeOTS8X42<*`A8g2bxXJF1y5Q_iHRToYemT88{4(4@rNkE>TJ`H2Y|5-w|ot`w$Y6A^jN`<AGrIOP>KNinTFW@A_`wCUf$6RB`j0kbBsm=p+jO;{Mp_@AJvq-F9zt`H{~3Wt=}Q#tFqi{=zJU>!EdiQ1P6yPKDnO0`S;%b{&~wEA2rOPn#=1KUrsL%b4l6*kCJ?#-`CboIvco)ZPBi4z=Ll8pOvi|%1zTvpBB<0`J{@>tX-8z#iHiosD-${hmF5J?w4Qw{+GY~^5?q!d4KvFeC-^U$xueOQsN(<8k|7wbEx`Fi$#Jy9SxFixc~U)U;g^*|NH$Le*0%&HxCbv_Mf45?T8l5?4DcADHXa;MP|LGDsw2(ZR%*jIc*fCc>Jmzr0O?r@_i_(Iv{iWAt=<-10z8RI9Jy)+sZ^`Moioyd3x$-$)YC^b(nYzL*-;xRsQ*N{qb9U(Rl|c%q_}vF0zHzZhYr8dwid&!kDp~*EcDSBOd4c|Ni&K$3MOXW4-0BejiWE;&0j;Y*+`Ee__ZKa|IfQ$|sU|v$F?Bo5_$iT|)&@*|zDb&SDz^m|{!N#JR69z;iwaU43ba0QwMZU>&`7e$ZoWEv{{{Qk{P8N$nux#M0=*TNlWiC+r0@j^M%c%<Mt`B*Fz`%O`nmt?I>xvSkm&z+=GWnn_YF;PCrp45NL}o)*_k=xSFUphp;1zj`pQFc<Q`s#i+nUN+R`il!r5yS=C}kk5%?TAb?1y$v0M$mTW}J3lQrWSkOto3bSQ<NGIDF42}QcuXa;SFq!w%tX#Tk6312&UZngDhb-Wn}T%OptoH@;Tnr~518)7A2?-c489lgvj99tW>y8A?NE`Byp5geY!?`!ts}q$kq{5+V$2d<THD?~DlF4QG1PdHDi1%)9jMJ&*<Mqml}CGqHyC#_`bGG~<G%_UuEN;ekat<)qA8<L=_uxYws%(7OdFMf_3Efhz$_V}@HYNJhg$A-JH8#i_rHo48j+b-u*njL$V!S3+g&7vA<^oPS~Tn{)%eX$JY<HOFkXr$*a(e|E^Ib;rFsc}4qWanY}v0ibNFcM?$+h<gd}Vn0}I~qc5@4A8T?VD39&O6#|VwL;Z4=Ds%NrEC?y_EnP=yyZPWld#totp59W}>4u<`Q?#tvZTKRGoj5<Us>KXhwy}~Jf-0w_g;E%SJZ(8p<QGnUBAm@6tbg>IOwL)C-BsLu~_$aDkr>)Hz^T%Wi(C}DQHA@BCje2=The2*z<jRiPkW0S!bS_;xYRfSuUIgI=F)WvH{5YuOOB-(8tx1+nz&H{b2bGaAt2x2;(Gn9Rlzt^9jKg%XHhppkRroj#vs*d7f#a=llc<3Ez8x!HE!3>}8zOGMq4U|$CE?urzJPojWC{dE-XPYo+3G1)XA_HwgtS9F8V5h>p)o}&<oE3`!<)LYt^)05sbTPFrr8ah&mPB{TYTQPqD|MNvU0N3NRC5at~m(TnK?(g;V~RFj$?=GVJr-_#5$Q#oka7fg$^n>5IxN6w>Matv%NH#yT5N4>y*wIr3cexa}TOuWs%|0z{R)KhAW%-*9J7PC)(>KoeX&-9%TB*aqaQfgr0rvYKf!_?h}2qt24L9d#(mJorwh8^n-RsS8x`$f)!%`{zy#y{cKs~as=*AT>`q@ade^Q>B#3{It{kgl46a(-KZV0Fkq|Pir~g!BO&i~I%vsQx3V818!3!W#KuAq9T?3dKPl+VY%c(NA0-!UyewqpBt|*)NDfgH2wJoFrl)NzES>FhA#xPOSMEQwk(uzBR*CD4o3+gkiP0IM?+5`qhxGM>j;6}%=CRg$B6w&0&9{GfI=u?x=fS0ilOH^@L3Fs`HjR18dah9y;01W~o+s}-T_M}MKQU5yz>yy3*)CIZrD>?Vp=msDw6kO?3~;I-f3+Hx%{7Jtn!6-~&C22{`dciv4NJ>{R<15rT=~nh=QJ=mr}rXg=az3L^{!*mW0o08yte1vzVJY6l>fN&seQ0(KK}ai?+0zAng~pQIsg8%7nR7g{Zx2?gYTxMeCQvb-+g@pf{-nt>hW>o36qz>C`!;YgnPrGe?dSq<-=-phY*$qg=Cb`2J8{2%O{&W4wxp|=<;%*$9c}6<nVJ4O9rj&U^L@;aWHU5SmvIJSfSU{%b&FZT(oVZ2CEutv%L0LG6irxoBE$WfBpj#{PEr=^>>l%PROkwpFTL17kkzy*Etl_qC&#$5|xzCu^1?6yG&S{`5VvPT}d3MY(90Bh(dsFzXGOYnQ+lT!(DU~CxT+w!@5<qel1>Ns%DnB45@}c?$vU0CHx@Y02Uu|IR|C05vKP#Sat^#v%iI*m^l{P=Xl`TOk3+$a5QzgP%=67LsEzvNIRN4b34a;&KEy^d61#R>vXY9@N={rP|Qa409t$*7J6tqxXC*ZDkX{gw2V2rv?S6Bic2afrW7v%uV3(Bj8aOA9g}lF1JHn<-<Dqg5_I45-L-5sqo6(X+u(rK54*pE9KP)2ZeJ8jT#6D!CZ+m!Jq4Dvo$X@q%BAH-A{iWX&MimS2A6Ex$Q8K`R}|xyc2o?2rk3bB+C8xMxLU!KkfKF5tT&Ut(g19n+c<L360=A#Q$d6cyX>Rv3Bmx-3$$gct8wyt1&&r1zaEmhQUjbU3Y#5CwTlF-i%rhtp1PoQt+v7~5N5Z2?J7!T1Sj{8Y_dNlwt>a7`3A<#p_PbBn6jOht+6oxV}I|yn*cb|7;VyyjBPbawZJMH6aI3RTw3aFNADlBLLCO=rkJ<Tg~b87K+DwTj{T9`Kz|$E_dn%4_?0}a7LO-gnf%gDl6+@Xn}B&dwsw3*6kJ6udY8M?I?X}Gt#qt;&~A34sXbp!6d2q@EfO}kcgwWh1>(Zi`ejMH`XpU{?r=&@p3=7cyGcUZo^)s~iugeborHf#^|Ba-JM+K$ZmSs;$rx5t;#`wd35oDHm@3WTrP|P+PWSIyB-1eUERu`dtUM-pG<Ft^Z67k=(ak}PgumxBWE@*SlfZW&g;d0S0S#I@8Sk*hG84+!@7=hqU2cp%WI$(LN|&c$bHz=xj1k3WVgfyA&+ZDGs5(c~KMma;%(u@p8u5y08OtC0L9IMbIA!-{=wO=rU;}$8U%-;Ff6-K_3E5@JKzv$UFMLk73woSvWM8N>K&HY|a+#&(QbqozaqiZdR!cxVS!^+_c+!ydU-IFu9hc+DH0ULE>zBNPl(#u)efioC0xbR2HQhlAnQD1Z5=_Z^rb?06X{^IY&cu#OIc~(GxZ5T>2`0G}5?G^J$q&8d_rYo~N76G#c!;-1r8>;nKUu(Vi)I)jH@;&%(oKPKBQZ6{ss?|wUGZx;mrTEnY&4M{n{GwbX`1a0v9mjLbA>;I&)}(a*xn|Qpb#4Z%~^14A34r^JL)q{GOXg(c`%S?-ihfFrO#utvyxO+QNyFx$}YcoUW&Vw@_2;Ir}KS2b>Vdg!+`H)ELwRTm#O-nO$oQoGi1Kmz)dQwqa~6Wn)ufYNRL_C8O2xuxHhfKLFXXkwX}y(rNDd)mUmmm5*Sdb4gxZ5>iU<klGpiJN6RM#?~`GBY8Hs`5~?g3xRYK?XD?>kuL<I9?!@SN8DMP`Yi*!|!>B4FKrK`|Eq;^E(vzmcM}%Pn)I6hI!$&I<@Fhi8@4SNU^|eYy+Qv8m=##NeXybzqqyEg%$UU`kRWZ1<i&5CHa_d~D@Bv0acCc*ZyCdY3Oj=b*DpP>5qMU~;F$j$Fm`CDi#OIe;%mveBO0CpHQUiv6F_)qFWH6|6=i&u{6McOd)GE+AC4s<aB`LAutF-_uX>Y8>eddztA#^p9dZo>+=b#m3wavR&u@tI`i}6Y@@zRJ!-G@HM3Sa>~BV{VP%}4=X$=$58eP~-(E9$bGgRg4rZ-ge6!3}U52O-WY;Q|cLooh|$ynv_gv?S^n02)nW{uIaICHKqT;dzbGmg!PeIxt(UXz^uR(E9O#W6re99jyeW7l2npoFLm59cWpRm&4b4L9|Yho#ZnjOg(^hFBxy2r&IsAH;ESxOCwq1yxOl@@H)Vu0;&4szS!7pEL7i9rP_m25RJDb=pbdK+8>DDPSE__7fIY5a!PL1LnV6@;k4^%y>+A+tJ(N)7Yp>@a5y<fTZe>NfFdE}kd}y*3yHq~{^w#@M-8GqkL|C2`LFmab{05cnYr)&b+QTHXcInnhp?pkS3O}o5)6DN7<eU_6AP`!(aoq;Y{5rs(X1!9SHYKn=fUHLU;pRlKd9IBFq;-2g^l~-i#E{yHa3Q^vJa0Q>32%s>n-K4_h}QuXQ0tra&h#mWS#|b+{BN@?)E7I1{i{l#O^F!NA9)1-E6M`PXyL(x)wz5DN0wjdw|5mXJz3Q^g|VMYImEh)<+0zc0xw~@ZfAj?dc>aDU{E`&d6#OXm_U`gvOyVVa!o$i`qTCak6NP&5UouW-5@T60b4jNP3)_=CmBisQjwsL-N)Q<UAJ6V!KX$W$c9<iV$tM<=p27#V(9i48LWPl`^}GLu1AiG~N%}r6Nt*cvqdc0A(@8bx+tBnlG$GX{5f9-qpR_6RxThYa4ij=V16w+lRzBTSb7$OE`S;eW>tzPh7C=i;JL%sTYG^h;!N}U*E#tT0TL5C*WoF?W#OOmw5LJMBwEg;kZxFR~T?wiM*o|#Wv~TL~<%*FlDlAnkpVFd#(iq=${{abNKimiPh+8XwhX~msYQK_XWNy`#8&PgW9NPI47yIZ4+t+*#u!%4|?^yci@((J3!J{r>1<WH07=2;Z9oQiQlL~N0T$=y6n8F081!26$Z71M*=}e33Nd7hCc{qI^PBx9blL(vr_7;t(T6tUz0h@*}?H`8%Ati1Td+3RvCMxDp_^A-6Gch>;HQ3V!E9-@O+!Z2IK;T)~omVYeoTUQ7vDOx7@o2XHIQ>0+OAH5yf$9?YF5Fj*F#z!_fHBAEFyaE^NxNI8su&BCEHJz#>M#Cl2BB!Db+l+TDg$?)pHi?m$3y?I-MJPup7myXL-29mJqGibVM(zGIAX2|Bzr;aR{mi_5^xmAKX?3breksA}yPf!J+{mGJu~|Ig3%*T4Pz+b_TU)QjUs<8A)>+dn6w{>#ri<LfUUaWY+|$KVfF+_)$M^N~hX)A#s8vwmRQ-J?$zU7DVblW&0K=jobHlK|TVk`o^gHoarKiptNG4jH_snfnLX<Zf{w#XX!WZF2jtC79nAfB|WbhRZWG$OesF-m9@ErP{KVOp4PnPe$Py3`qNhH0Y39E=r)?TMt86<THpAuf5`E0C+TV&)Zg@bdWC(dj)p{P8s`!&XvlTm|5V#B`fz%jB1Dt3uxo;UE8i>J*zd=L*(OB)_L~L^6#purckTCE-MuJS|T*so5|fP^tQ1za=y4xYi;IAu57swu{x_xs|@hU9{ciM(;{ko$XL`6rX%8C796Z+=Q1VEGnNV5Q&Ga~qU!3=_|@GN@T_O_e0u0+acY`F9OE3~T<NCC&f)1OY6qZ>X?i+DGqb<<_F>!x<{r*_8J<|>X3Ij`E4&jD3vZE-T<soUl?>YoXyl#fdDX=>W?8o6T&c53&=V6r?7Pmu{sF}>5Uc=5Wj;GK<@O1XjfM>bo4$=nDMsSmDD5}DoMzkE)%mhzuv62JuD$jLV$f6N5o@V<i$!s*t-_fs0J#0(6P`*rL7j=ivizS$qH4)_LdEOCQ4F;<Wv@cj><m>zVFAA<c2RTLF3EzS`jy$RHSJ;wE<dU}I<xn5rbW3t!*g)1hJp2R>k$67R3}Cr%n=HlHV>VW-~?rf8S9$5u%oeKo^zIHUd*6lw3=kRzDzy($drIo=sh~zMIMcxbIM4P#p1lAq^2V<cLFQOuZx4&h`zdtE_DMLaU}17TUU$9!cui&eSc)7*5~=05Wm}mDbwevS?VFq#-4T4*^vv9_d5j$k-tE<vNpSgeF>jWsMbJ^4Il&?cg+-``)bZ3MN4;P%22G&vU6UCUY#d+D=4W0AXE{7L#7uAd4Wh8aR5f~po}AQoqRd4ztkaK7$kEnH%&$uK1Y4dtsVY;@EMxKy<W!qV?-GVet(9ZtA9fikAGKv9E;lA^R$w~13rCRrjSXV9jg>)6Rb%kF==i)%$*s4iuP!zY>&>o-pI${4mm%dpJT3gQ@_i-;9&i^wa?d5rKl$~!isJ5L-cmRf9kltwX0~my#o&#z6%f96pSsr&Xx=y6o0}SsESwI-)31EHWIT?D1>`QP$mZN{?X{^l0`%NV2iRPv<#E3v^Q_F-_Te(8Q3$}t_IO10@_=|rikH=1b9N&DZ-?VIJ1Yi=BvD=63MrDAMOeZ2yk!^IQH@m7wowb$E#!yH&VeyB$g+(q#uE0wj~0yV1xlG%paktL~6J}_Eeb?1~|l9$#e*<4=1@T&OJ~m={;Kog*x!6Rn)4S&rv%GyTYHzDb)r7aAQdBmhDXzgI>E*+6kY>mY<+J+5Fn`ANs~%XVae1%B4w4Lf1{Mmx$rI=j3Y<B#H<>AEAW<DvkG%zagN+;+%)lcU)<oFLk=bKr$Hp#kQ(s<=pPd$>82mmnXQvq$1vNR$zmrh+-g~kM68W0uQJLaSZ{QKWUjFH-Z&$bcIze39uiG39X#SyUPpQ%*+I<&8j>BN)T8#U%AQJ9kjMo56is+$cQ$2k>Yu<5xCg@9@m&O3v>o|TT6OL`L&cvMvt^+XamjaLQEB<wJ1OAc4Wv}xv7$os!`AXpCMJo5B4<~dBi?CrJ!WT-#uv#_q{OCXTJs&_j+EI)YIaMnM-?E47vE0(XYb{admPdm>a`Er%M4?%)S1PM_5qCr8};-s}xfLE3Hl_r9x%2MeZRP82y1dKrHu4-zvIP#ii5mb$hIT1BzY7-KLMBWo*(IyHBT<GfGi?23N;3B@0$V*H(0lQ)v)Ik~J1wWX);{y2Kz`WXMUe>sSU;l2xoJBO>)$x!}cT+N;8fy+^O7oHkdKwga@1?z%rm17|;QNx0O@sbDmhsHvGO0z$C}vdeh4tk6WjD>xdg9!Csz5NVo#Wnr4lfx+#E{ry5bUa^hXyxt%A&DYglUDU+Az$<(6S^@m%z@Av^G#P5AU}9@U6P_(naZc+GHnI0b({=a^G(q%|6sB{JwgkO{z&wm%9h{i+n5aU*ccN98)vIk7XqSqVkHdF4Sn^@W#UBODdGG4U%GrV0P6D%Pi&kA}7it5GqI56qR+*QnKO!Qn_V#uX5<lpHwAc#SFK*Kjf`b(zQ+hh(q|Tq|Y`GGRBi&#ebGu4u!t|5&*+uHW@1#nEZJ$8PlcvPFC8__u6WJv9-e59hxsj!Ia&O|`30TT~cDYESIEWulDYYnfRnX`$>FXHxY`CU;y#RIl%^!%5LMazL*Iwe!@*W_lbQ!IIvs0o!F$}%A4VSdUQf9Y!It>l;b!Dx8VR*(L-B8&Cq-=<1!md`4Zt!{17L|(E?4LNwVibswC*EFPW$nQG9v^!?8%S|hCur#_(pAdl+D-&cw{Aj^@HTLq{O7nB>xAYm%HC%{!6QgzDbvg?c%x7)U)-U^kdSpavooyA;#z9gnX(KW+~cpu4BI9NP^MmWhL;JA6qeDpF0*P0C*mSya_FLt=jE_Wt{s!|LVreLa6nB_dR|qX%*Ff;TP7CffUAvjm3);`sbt*}@%JzZf#Rv#glCa^oxjSWu5||ZK8^wn-?8`!X5lglYkn@gJ_<hD%#Q`P;XF2q7p8s3Y_;6(r77G9)Z&{7jsVy+0Zv&7!9ncS<Ltpo@Fi&H3HAl#4SsepQ8&GddSSXP%DNt};p#><f2AUiw}wJ=)HNjPy%4OB;v>1Eu2P#jy9xJ8;EL=~5jq02J8GReca)$?63=dCenGuH52Bm~u^xMAPA~+!{LVzC&*ZGKd#7ELboG@B6+Y75ZszbQd2Q4eVdhFr2)>E$R7=wXT`dHIDY9evvyCB%)A%rjo-Mst*;<#l`yw0!I^NjLjPh1Oc!{Akt9&w0qEhQJ6v<9`py~o)XI_8vec9xbhj|Qjl^qRUXN{yCE(8jHCX3I}BpbmmLE9x?Uc57)Z691I$=VG;8e^LhB1ACpy=DHy^PYnBarm^&&eG|UBQRS;z(_*x-&|LUzmh1`JvBj*5U@wD0d~h?pGG3k^-b?zOK|Rq%>OYVg6F=i&XQ|`M5|6Vd6Tm_k22=l=C3Im;vq*B<(hEG!O`GdrH@rD7~G3i_aGDG<{=v|l>OFsHo^1J%k?AFDqmFcQ6uf_$dFh?b!z1JuwaWv>!*!GUBvqN$;<jQx{^M5vw3Fx#HaCTh{EUSKBeAB0e#lDII;61*0!#6>U0H#7pVphp1cqnl9j#YDO_6#)5ZA&7kpJOwqc__t%kcpsnXO_w{MFf{frWO@a2TM<XLM}H>3N8+E?2&+0N?7{cqYXxstmkZ5{Fw;rm{z<{3-wZj?514ibyv`kW!L(Vcy_%MvH6VhW~KyVSKW<UqR?{bq@~zub6yuUFJ?1;<)$gHL!xU=nlE=LnWpVW26Emg;GYS&e7^M_<iE?cywd6~TQ=Rufn%;X7?S3tNbT_B%LTkLJ$4|A+swAzlo+LR=tO41lfWRx-xsbeVJlT)g<e{UZ|xEOkBf`gVthupQTPiA%_v1f#y%Hz2bGNcymgG<vKhTW*{0GcCef=8Ekbv74+8#;-e<&SNjjxc&~2ocj4FJ>=Ucs~sCepg6z7-VDRdpEdTt&3JILm>NdXes6{xsi@sJUeyj52}G9Ge(O~*557LXle(&SWGwZE5VMHigM*>}=F}myyMTifx3HJh-`MQ=X0yUska8%&!z^5$EL<sPvyIFB9`6XV{%MOJ^-wn-L%k%fn)3@=ETv19bIB9ojPq|C)?0>Tsd9k=JnaokpW=L5`fp6GN>fjO^<LIKqaAxeChHu^-E&*GJ4Q)C8Qx{srGfvduGn_NbWx>!7M#8L#+zScIM&MlkcFb}vO1D|G>^mOr>P>Ti7P4dJaS0LCD=lw5X>@4m3y4XlP3trNLd9!=gw*zCS4z?Wt@6x=ECR7thJhcI7R)K-zR!p-a-aj#^UClIN;!y=gg=fmv^9L)U;?Bmk#$Y@P4D7+}wKH1Q=7jT76HL4};TcnyA;W<Lmv{@`bW{s~Pg?3Q-wX7rInFbHp-0q!yWH25qqEaeo3Ol_{KU8Nky~Xrsg=l%%iyQaQwdXQ%1V1;Dh-6_cYiEYs+&^IXLcxzr(MV&OcpZ;xd(*|w?lwZRe=pp^#91D4O+Y23%$%_!u?`ffY&eubn*H;P}d*K~>ILLGw0`0HfpvH|n)G(W%=#4eBO`lNkeJ3r?|XVMtx!ld#~)6MGH@OhaMSp)A8WrBWYcHm?sh?&@J8zNS4Rz<|r`p*OZo{Lm2(uhu7V7cAG9W`R(WBV9Ly3silHZ4VUqJD9*rKuGxQk+Md+raQHNZ)(~)P^xSLn!Yl-P;}iO)|wGZS&}f);{j&nxX#eDJ5ppjk%+O8or-ps)rpsUZVKIbd}D%%r>N7c_t9se*EumDHdFEOQ(ulER}5^!pR#WLTXy+c*`;pcl#)wC5gcU)V_8dt%@4EwDuLxUS@T%R{)HO(*(aVxKm^BPZ>e+1yR_5T=>T;boR%0eEw&GV~-+_9FfuX1<VISs%>cm=(8P%jb1>JnZf5@&PECCbH9HM$|~7x_m6x*0K2%Y^(2|1iEU4(@tM;5^*;Lng$)o^mXZeB=>2@HygJd}Zq*KJs%H~lh!iUM2(52uQ2zY&(dDVfTpm`GIJ*4jK0dz~oUFo)jKGsdr+(DL)}xoD%X#uqny9@4+8-W&3_r>SMbL_&{r?*8qpv=Q?$rC}bA@~)1*f{D+x3zltqsG(kN>qI&+(1z+PwHflyJvyQ;Y{(u@1L<3AMJ-jG**b!H*xfKbVkP0Lzw!ZT_OXSSt?Q(F~=|QtoVw3Iu^dV(0tW-a;SMlu|DS=-fBu9FeWxRphI%+H2^193R1NuX*SOhcQ06p1%3_-v0i1>mMIA%%a}O>la^6CJ%E-8t9IaSfJn6)=oMbxQlJku4}+qZvUT^n;ObZQ$wE?(jvK^ig>J@h)7MJ=HjT;tiOkizdr7lU;h4=zy0#(y8U^7`Wt-h9GA&ZMz>JlAD<eWK<#s=`b~>Gf<7G$l5e>G_~&2#`s@Gu{TqJ!XJE(<503Vqp?B?w7R~IQTg@pIIyOaiwx+akDAJ+nXu&yc6sCCmsvV^2H*TtZD5`!QbIBnn)YAhaK>#>c*D~93L1ouV{1kaI>S)QLClGa*xbQ+bV^}@?`E&j8TYcqr2L;S6TXZh6g;qCw=QVqLpQ=-sF=f{`DUKr^=luWv_s7RSz6N8x<*t4oPs`$O+D~g(2bXPOXb5v942Q~Fk+_$$2S=O9kk(d11yb3@;;Is18v>XLNYKQ&&pQ7(pM$QxG$8<eh_-l+UOPYNv9=c1SXfCxKlh}zVR2$<bmFZG<ir!M0vbo~V0z~9pnnqK0<z_kJhxW$;zQZ8hZ^89;Bw6*2^Mhp{X&1yK4?#iYff&pwGGf3469#Xm)BqmSzpyFC9(h;YC}TP)~wxL)LqACKruZ{_2k}$jzMH|8;qTw7928mgS<^y%Kh>ElP!g4&HW!!$vhA2_$V`xbI&7|*?aR{kf_^%Ht(h&oi^xgmr%II;@tzLd+`TO*#Lv@g={PU&ykr`L1#NuBqVQRr#jmOhG^>uFhL~5gSr^AM3>gK_m2w8bWsd7o}|hM&$8@kb5^!t6KUnqp5YB<*NlD<e)0IP!iK9bb~nUamXv79=utY#ouBQU)iu*bWnjHJni4QehOoPhztEwUyWNg&$M5~G@_t5S=9M(E<RG%vAjEbTiD5{zI;0j2`$`pkvl9=Q;U<ii;t4iFqoWI(&0VQp!k+_|dkb40rp+8a+Pb@yt325V8^^%McD&u(l2ZnMR4G9048}1+<863TJ*n!MY!XU|aZ={lIcje+fR1t3ro@9eq^yHs|DpRbxr<i5oCTu}(TaKoe@?G(${+VTlNtD<t>v56yG|5fHZ91x9xYw$qDZammOP0~mkU0MsvKzRea1{H83QytR#jC`!FHnto6%vA+ZMUPoHpc=FVCDy*N)mAj7b$ixItXMWgI^aD*4ieTX$=crJXL0gvLQ-WXuXkuzj>n0|}*Hi3#H{U98@o96}X7j>GKMR&U^VYuqF%;J$Ci${PzcYyO6a+i&Q6Hgut}#Q43zIi-D$L&xdN$zJgP(p+zb@5QgXadvwH_?xdJtywx%2U7EKOlY**&*xUH+&fAuddF#U-Mf$td~4nnT4Q>J0o<Fe5+cXui-5o)Z9~ZY$Dmo3`yDIs?!N+sdxhi1d2m@J<Ok1@1m$dTo5noTCD$m&mdHx<R|{~Su5fhRpBNV<pjM3YY&#KOX&NdmV(OKSc9x8ZD9<qR#G>KiR>Mi4xl2M1p?m<Mzr`H=u&fhk<?2#Ql(i%yZvfvzntlWA-16<D1{X}Rzyiud>^$#w8XB}lSrY17=>+9J{`&Lp2ijdt1jfzJzyIt-#Z7NN6=v+fcT?vM^bgSQzP<tFd@O$Z@p0q%x-Nt9qG=k!4J6RNASMjTtjXvO$#V>X>NFOKsZyp3pKS6tU{VUB%gcox=TnW6`g7&s4F{tc*NcOJU&dwbF})8Z>MwuR^7hfTk<`s<tj*GPW65}5e>U|$fByUj<^|!sPikKwwyt1lLK;qRDlhh|QHn&!!$;9uyF_KCcr1q3b-PShoB12h-d#zkv}}IHn{dg1+~@2Uf2Z0tB@7FqQJe^hm;<fpYuanP#FQ<*xD2WEC+^j9bCo~976>dpWQ7Py&LI)l>tNX(P=ufs$z_^)w$Gy~ylu7cTIO^#b-GagEcHW@zaKEdnmhAEyDDLpRmkk+L55Js>0-&R=V&>|OpWRRwD{~z^w4&2lXoCgib?yaG(Ebs=$j_CKo9h6VP=}*Md0-d9*j}KbFpJ`4rl=O!1LSE>tBK;aK5{i%`TPF9{O!?KuZeT-@z$ac5=5bid-VO%z_hI{kxuGY1##AG3Y2#si(_uD<+LwiKGoK*|w1@aviP+O)l-I7ywNz(RIw%s8@SjtzcSH%C0vKdo%efEv`syZXCOId`M2wFEnFw`6xRFffUWCtxQ*qlP5<yT3vk8bakZ$I9U`nJ4y@}30N1K$;z#`K<nC!rCUY7ZvEQjTyF#?ceBD2_@{I(j&^SyWoSF%5|(x4-qtn-VC?VR7a@T&jS=JQ$k-;aRST?AKk}EelyFl^40`{d70R7hkM<ABwhM_j9iZz?h1Nx-$STm^M)&<s30l4Z@YVW|q$`u}{|;iam^R9;5K{INtex3+Ek&!SMelNVTBoLP+)Brq2kmAzn%eW#M1jFgSQxXxy<1+7E)W;C)^{`ZY>m7A+~Jgza}jL+Zj#WpCym{TB7W%F^1NKQZIyiHfA`%cK`S2<XvEIBCMoCH@Hm(%s`8}*a-Rm7?^`6(F!d~wi`=X{CV4b=7L9EmGT_n8L5+kh&@^O(o}fwKyFe>L?h9y;Jk%3!q&S|)ym#ZacA2>NkO7@}sd$(Mg_JVuIl*Ql<)-7|QXal^x?oKaRIe=(iJ5PoX*A*$(`kx7_Ja}|o^^!Xo58QR3t)18udz5ejU{8*^Q5cLvL$`DYI20n>2^U^^<f#Z&q|l$Oa)>eSnvq)-%r&BnZ`~#v~~%oCkwbL%oS&^|B?@P?YJCIra>>UTfgLm=icU|MJQ_-8Cd$OtJOsd*(_QM6nW8IR~2mS)Z;ReGg0v?;YK`)yRFSlFv+cuz#7%6605iTK3Ji)7JX@>@7x7fRbI`h#w}pDMKg?%8{e@W>83!rk(ioem5e;vuJ|>aOQzpOHk!zfO}7x!G|hI0*x4PLK*1lvXYf=y+_I8LP>2nI<^=N3NT~YlsLwRXu!=iwz(Af^uB0m)J&(=Kob0VyC`YfA%VzVu6n87-@d%ku=lgu>!s`%*0pH7EA>OBPnX3Qk)wtJZ$b7Sbn^ai$;gp#LQ!lNlXlE2-1>oA$(3j3Z$ZKg2qq(j}{#A6`xGiG|45)Ac0hu;+9ha^@KkI1uq~LurY){PsF<wHI)ltIxD8F>{Vpc~lSmu7KEU|19ZC47-Xl<Z_!!V;3pq8jTU%g3Z=^1KA(1;zvJX%6xBN)&Gd`Zz&Q3Cb)S|uZGW1Il=NyJYeKKL+ftB*$Rsg<j0Nbu)(29Yhd&UFeOU}oJ{xI=TKrAezQiJ>hRE6RDu5`(}vk9j1XMtpvCmRvAhrqoJJBsEyodBA0$6{3%}&Yg=F1WvrHxu#Zu))l*wI<5~xQXC3+0<fgLu@?84OH7C9Y9?ilyo$sXT2Umg0+D<hpoFU8V!RSe{HAgg>OS;2R;+flWTZ@GzfxbDo8V>p(6+8t)MYsbUqu|>2u&=58{j^N_y(_p3oyK*BWp_M1+2iPC1HOGXf%!GS{#R$+%J2F=QT!Krc1>vz-+am#g}bCoyY>moN1XmS_w=q0I#S$?4Th?*s>xohp+d7Xq_TE$!A2EdI0TSGTuH<r~Y$q5-%K<MzY3vwO_a3b$~+!Vixbd*l0;_!62(tdvFS(@wNmV#EriFf%xqN&EI{I#N8pM<W@aYvPTh4yPnotN1CykjSqLRKo1UwlXJ9nNT>xU5<(7XiCDRi_zU2FE|zuFAlmcT{`!~yiqB$affJUQ`|htabByqfHsN!32ur$u)f2`e!N7Ndfmf0_vCw)P-HZ}v7JO96<RI$_?p5$5;Cb-);bA)3`e+`5H=7n9g^l~-i#Ax*Uh8>dQqYc;t*T}8z1~v(dY?8id<Gi5B^O7}O6FOhc6CRf$hzC73>aVtIug6HcpbUd{&usy20RfMDWnSNGOq7H-R=Pr6Q7lZThI^X0dH4brPz6=;%nMQ|M1{!MD6J$C@GZB!p_KQ7HD^;9)!lBGKreh3I52&$)YhfGrkR*sX&@ayvC3t>2YeB({d!EvWJ%s$y+y&^H?~G?K=6Du@`bELbTzQbDtj+yD(ZY{FX^pIz?PTXv~;`#`|IOD_ViU(8jy!#04meF|K>U#?X9W$+MLfV>L#4SNC#HxT;dDZQu=_gW)@E9}?qi)ea*s;qb}#p~CMyaly7PE`lbeUJQQyo@t+aeG7kU`2+!;fS1{~tMUw88PYVu4wrv~<32rKVZdo6@{Ue)l%aq`aw=pnWwLHX^qD``g1VK@5575ke2~OybTzc-vad_4SG)TH-`8}h3or@PMm@thNu6z*P&3FT2)laFtLMD~w@lpulEykU<x{08ZzT_R(jrg%Min}moH5tcDplbqLdmHxs4YAa2trDr1DZGdK`_(#HrVKZRU+4xoxMNeeof{qX9vf(Z5Xk65x}G>OlItrs$|vec8gg1um9`Ci|KaWz;jhvv)zDPpwN2tK7Y+9U@fZU>+zO*_u$N_txrI*Gclq#Zms<`wZd_+v~L(1U;0CI<H&_gITlAsN>^m{wh>s|y7Tgo!{>v|Kq4jo46WStfmq#vfbQB)*v+1{wf=X_eV00jL2(p`s%qrfzAeuf<q~vwYr?bHu5EbOE6vlblPK7(T%xMAV+3NiC04@kpZq^R+h70o^KZZW_ERs8AC0&9>u>*@i25%-^Ng>*e8kCgnI3~bTyf)~49rIwRZZXH56$9zad(eCU36)BI!?X;mY=6<K1~8_7f4QgK-lz-@hU1mS2|?yo@VYJWRttaffV;}uC&SR!<JxvUjPQAJsK|0)F2x)c6qPHo|J0KS~4k4$2=K@YcL?~7t)|ZZn-Fdc5gilVUf=uQoQzxqXFR2$USdcfzm;~JnR+R5jbV+7dlreV`6532bZkeJ29#;i@hIh9KLJYb*yK##(Ic+oXR@SzFGcVRn-(~)z@W(LSIXSMtd{4dxhRMwnokuH)^fTJkNO-B35VBX_Wz9*<)YcYg$B&4;hOZ!gNIZ%YuXT?A($tp37J!a8E@Evx};$N8?v_SHQEL(evq{o5iVV4sncgh;yZzCOe0xqo^H#I;QFA5Y5c~-rI+98<=}I?`3#mm76UKZLjc7NG!ZXLUOfxfK@VVE1;2gqUTi?+n8n9l5?fbCP7b3_^|If1N#RQ!$7bCAeH&-)RfyNKsFjS5N!H3CZ!mOccZl5{BoLYXIJOTmcdR<L%R0bABaIul}D_l;w=`%wYCapvH;-rhfjDa<pgym4$Ja?8i}eU;|Ue73r8{3+LXNtRkJfx5rqZ(p4dgrWxFH`hU!;l!`8HmDY*Qo?&!?k)0r0K@(j<xxf%x6%dJEB+ftnvc`!#PaN0a{N`e!VC1$K^>cWo3j(N^mqIofcj?rq8@%l3L=p$1CQla<ga2I(re$FW)NfwLql9HN^z}yL}AipjSVk7$MD!SASWW<rY2X0+0Dho^1iS_-Fm0F+Yb3*)X6Q)d`r)H^#I2(J`O=m|gNZ#)hAVmHG-OAeR7WO54KA~CzIW~Y0Y}_?dgzl?3j}$H4nJGiDKFiK|9eQ=1;H{vf4uDWa1P+;AB;*AmX~Y2-#e*`A&~@_V!2VK)cwvytvD`EnVfY;NIk$HB`@v^u68Cx;?~f5>B>4RqdanKrO+5Zx^>Hj}bI;RC4iEVBahXCUd3LN)oK3JMmBggE?J##{04my}p|U+X^Lis6hdbo_fPRj-;!XW7_kx4<=hi-7OO>LY&<HEG(GStv1^=nz`qr+Z?e-2lX!tHXXj3q@@H$&EfKdDiZ=fn(aetd-W!Ol}LZJ}u9YL8Gy!%I^r%M(M?Sn1Kme4Xxy3*df&3;2;>11HfV7nSbmk4NY5t|~0I}+dtVW$X_I^xV8;+n7WmP#bw=6$#;EFi$aLEzZSJ6y2mN*u3}J={nI8<AL^*phw(mf4mF%z_aHs4#zorV^>)2H8_(N*Le}Zza<qv_72VwmA1drKI<46%^{gt5#8~az01xB<u=*CZ|*z2*8aYxm&h3SqysZN@*v29$S8b@?`UC&wuC}gPl!#Mk|*lDG6OSxn3fM>z<RZMUW^W{CtEK4yZKVNB)L@5{q*lO5bs%eZJJ`76Zv(^cUNzl9hA2D<^|{M_r!a29t_-$60|5mLiIQcs{zbDhWKG8pJgOX#S*SirffR#L*R2xg@}TFebEeBJVCQa5FO#tTwCi1SmmZ-F)RHYj@DvQavp94j?1i=tYX>!A9U>|9f0x(k##!+-)uCCFR#rDj7Y}nxPFes|ztzl-8pBu-lO#Yvra&Myf_V|9^&589&(9WaJV1=#+wz9e?+vIo$WcK%e~@RNU)%SyE4nD`qb3VKL<5TSmVQGsM-&jbLsJ2c0ejU@`alKOSL08JF(3-mX$i39Pg_p_B@h(H6OfWMK3M>Hx9aD}AfzQWcj@!`JPx{tYO08F!mLhL*8OW9&YiTFxj%^%-0p&y*}!4P9H&F;1mH6iL=taFI2uDd-Y|Y>^=+#jax+Oi5O;ri_TxYvqC$pJ}fOEA}3}o^sk;QQ8jBO1kU*91WcPz$M{QFQ<ahT%x9CvIq#pBFHY|-LgUx0k7a_uzDOZ*g>Re0+xkoHU|c`ANKbP@p#2HV)J@`<Tqbedv#G0_X4l%&1(hlqXT<lt<z+voq~z26-{`yNX0p=KiI_H7fsjUGtdOlOH!E5J=zlV4g&Kqigj>e&SRnq1>cEQVOFoUVW3?qQa%pf<zUH&As2rXH0QmmCo5+MW;+SYsx4Y|rCq2EEQ->-v|D9frv8YCwA$O-Nl5&l2hw6IWWTsgM+gp9h)n6}l#@DtrnBWrG>&wGam?*1r3uqd+GiK31HY3h5w?8-El-*f>z1Vc`%Yw&+<Sw`kmW{}+R43%gC}4q_u1tljp87FJf+m4+*LuN$E2@g+_T}D^7R7L?KgiQJ_@B=^jv$1Kg)Z7pweZu2F^~2{=_i!<~Cf?5=)ug;^{Or%-5B*{)OQge{@4-6OghYo(a2JMY_S~Nn2DZUbBDVD2q`bLY{bgeU-HX?|Xdg`D`G?S)HJzuSi!Zn`=7}INiDlLBiX>aq^$zVyqLIyC{2~0R@jBm8DEGx8RLJwR~}h7DGbT;mppkE{kiaU1!QNba0Qq9y4s4BtV&Z)frwUG*Vbb+q%rEC7g(hl*yrsI-ZxqGP!n4$_xD&iNOIiMd^7}but(8J8YR)m;<gh&Q<bNPNkA{OT^#9Bm|15ZWEqG?sfhui@Mes;QKfVG<?V6CzyrHD6ILp@cJnDY%@O=+=lbmC|;QM9kbPPyO*YLBT$QPCO86M(*!tWB?JetTaU8`E5VnbohR5AkT>|*#YEloF6xEpwkYd*yoReA+5DA?Jl+}#(NWissP{s!LW+;%j=D;1?(8PqFM%tvM@8re(C(;p>fBL+DoH%MnfV3v`aFno8pL|+r8&V6?D9JknLd-V%I=+ZQPR~{E>!qPd%Ky#r{uL!Uxb+}H6i#WzEdqt4|KH<45rAA<<B;TBu?YQ6neJwVr6Sx;_i!Z5a@VgH#5px3E?G%)~xc$K#5AN%TOdc<$<aTgq?Z)&G%)KPaftm)Kzvgc%3zpcDN8I{Fy91N0V#>zXWZUe0lNCfVO>br6g-N1Zj+IN{A4_#P^o@6VH1J*2m$~HaknFOOC*75dk9!y?=9EDgH{LRQJ>bMMA(Hy$0AFi+vi2K-V|De=WheCo=!Xgb1GdwmM6$4HB(7+2l>m<~+)nZ=1iSY>0;(Rg`POB?m`?ca=U?wP0{BTHS+8kei2WyioRA-`NDuM=#fpP^)}V$w!T}vm--d71gPc<HLe29<84?5_J*l=O-`g)96b2<jv-p@e`lMry&ZTqx+P4BL(zX-{Qp1k67Ef(y7xG6kennJb3a#Y)Dr2nx}AWB}^CR6I}3Bz1W70`m`GE4y8&{Pu;#PhV(N^?7^24>XK)zQQeI08){!|(_}lVBlo{)yW~plnzVJuON8%xt(s>nxw}!?$T>(XitBTR#71}a-7ZU<tcod^TJ2KTzK{d$TJ)PG?*4M)@x5MA!xbEBxeY$y6@f|2NuMKFUWI|CG+L^sF=jQM{U3cb6Sa%8{8a?^Em=)qsf6#e@hog14%+YFbUm6o`~DyP%Z7L{=n8RxWHA7?mRrdfo6}{|32^b^1NV<i9I({&(CgbB9>R89&m}G)ZxW39YTtm&79i=vF4E|+mTb9gzR$D>Z<#B$Z^Ul0IvBt1Tsn`vEaUn+L~`oqqx6t(qpWsp5P{<S4tp~UH-FaH12^Nr&0=a8N&CGSa-^bm<9Jm&U?dP(TKlb6!94i-{7&ks;*qh`A41F`eh&_Y{+m;W(Cz{bQryB`R)1r&=bOz6XF<xL1P`-td9rY&oXs{a_j|k}%=)J-e$+$Vd<^xHxN6QXY_XIsS<WR-gfq^+aaeB|lBLQ83h=ZyFnx;iZRx);xhhRP0oHq2`;2z%1(~dKD0k0o;qDkE1!Z`bVV4H}tGZ&_4bw%H_E~WD<{NK*k>OY?|3emvzRT)J_R%~Jm!GDJq$aMU%=5@0A(vnakwP%bC{^xpB2S(m93y2F2%S5tahP;{q?U2&rI`z#E3?*W`r#DyV}76Lad`_FY#EE2d*XnDU!F6ghFso(mQmB9Wn4Pkzrg#AdUA8?aT8!n^=kD!VLl8_t7)QMzmBi>W6KxH?yY9Xrz=EdTwUl=`OFc^0Fhc`o*A^krpNsWlvJj0wq*cMN1=@plTebr_Dkgu2cDg#Ll*$kGFMEF*04;YyUueJL*!D2n2Ck+$i6+6(PZ1E($@w{Sb$a<Fb`NhbEk11b2p=q8|%C6$omzN9^EK@!CuoPnhSLZBIB=<rOO7)$J6`(TM)ZEs_T>Xf$jX97oACCpbL}AKTS8QXT#@ZN@NYZN0bTrnc0Dpl^|wfw{3`6!C4g%Q|mtu{Ch4^xkw{Ab%Et}3wP9rjgRePAn8WuP}sB-)rtDW$(E*8ut;$pZEgd@yC8k@6;K<-=nSE}r*v<3{5Q!IgS5?~CtCZsqicrxv!|4pO*iI_3TpU%mZ=_g@OX*h3)59P_cGg%e&v}!Z2R%Qzol4k$t|5Ka<NpleF!ISj0mY|rQ<EjNZjqCc$Opv4^aEsb+jsK?9$p-JbRhd#a;n0CQcLl%HU3o!9QgL#TP_j19IUXuh7{a-|_jM364FAJaR-v+ZQk&45_xI5und@95#9ZMP>${e>oc^w9oziIVh`Sv)w=P1p(~hw$_tmiYB%_oyKQM@7Me62NX6ySXoLMY@_${wespjf4fyXtf`(&d?8Y(<Ri4cp+Wic*GHG99&>qEQR3+GpZoayVsNqwH!=cG8lC!46I+j7mM-VXM`@z=4rqUP{4x9}8x%n+hW7t!ypO*6Ai7iUqt6xckrbTjmTuQeg0waa6F>gfiaf_Rwrlg^4^hG$zfCb7aK$>@@+H*TMl*uaV+B8c;QnAjZUHP?8n*e1@?xzxbVoCkI!n2;F)9!Q3W=TXXL}2MR8va57@%|ClygM3epivN!fLOf^KpCxzrE(68yv>?<a+w%-+TM}=WTy{)G&*BC$C?8Ihj1nC262LN@9V2Ut2rrY~U`oMZ2y6XSw}<R&Hu2H%$$FT1boJek$Uzb|NA*eVU7-R<r&dHvam!Uw--fU;g&XpX>JL{poM;wR2o1LmAydfq#5za00c@q3Sm+@(B8LG)TVT{^Os2`RlL$@Aq%`?Vo`mJ3Khre}>+*BU&`Gdu}zSROr|g+1Z-X#-T`urlSStv{9Ji@vC-_s^7S&_MxcydCVn;pioZ_j06GTTwTj-%LSEPFY#04$*7|xi=IH#VdBCI<&0tV^ykm@$8YtO+Z_}zw`|e5$QD}N@SWG}@qMaJVaAkQ-=sK>c%1Y9``;fQ|M(h=^_IK(eLO9TziB_MVI5qyg`pwLl`tGCZ$;u>&K?|XCPP|V4HZab8;h$-gl!05Dj-1<=RWKF=X?&j`qG2|^dZ{fIeP8<pvT%;Tw`G+1^wKU+J?o6rO}DEE|3#XxC&?-!Gr0U$AkV!gbT=)Px9Pa)r${h%N}Zg$AHT<lO$Nc;r9#uMf;#VEv`Aa)z&sZYcQ;SeO+FIEo6OFuaw9FY^V(hO<S{edr@~Cp8>`6G}V)P8#)G&&22Dtep+zI*bVYFWhwW^_fNJIqBZw_OeOO?u;Zi5M9w{rSZ43dcR`|V2im-wf^^!Tw_QTv8jE)inC`_NIAsG2z8A8w06a%#Rt25yP?3<ljh*Uj7Z{?gBftca5D)5N%o1H%+ulDaEYn3X)OeCABRtEpr_EW}hE1fEM|*}hm|ZjaMfk<zzX}_!!r0vqb6HZNDWgZ}D0hCgcUIR-8<m0e>S#*9EE&S?HvU3~TJCl`z8$~!zsma=k(pQ0$dZG|T7wYVT_lDf(dv*|H0&!?^vzB@WQLnCUWzB!2#t;|Y&LhLdI^6HT<$Gwd6+hH_-O0yR<817BWxT4AKUSEb4yMc{86O<u`?LQ2#vSlP4%RzXR=8sCB{jaXXmKB%>X*aU7HdQ=8&=uhW&@`%j7Ov`EnMFIz%h#8T>iD!YO~;?@VUkkG7U?TJJhhfZ4Pl=X$hsv5O+LvRm>bHeD|GD5`Rxt@jx-tz-<)@K{w<Jq6p18f->~L2g^*3Uk_!OTIjFE?qlndoU(d1mOm8{g!e3IH=@H8*bgLNtSlHI1(BMm60(kAi?(0It?V0ekCT1!*sEFdvXX>_&5%;TU)(><E?R%sDS&v9V>4v)U5d%B5uE-^V!ga#uDSdAUGd~H7}KL1rO|9+{X6p;TEKD#-Zcp;6ya|e`y{%!$sp)@sPV^n58Dj7K>=SCA54ts<Mkxi9hVb{<iEfvaz6JIu0&~ZChcse`u2d8QL_CW4fszKZQxXEeSszUXH&0l1exn|I~0rgY~)i1=89HQ_0f!<*$76c+40bXro^_Kvo8MOKCLrxSS@}=MNQ(Xl?$&N$^UD_>6#{I|ks&>k%+_p1WW9>3sQ3i(8A8Hld|25j}9b!KO7M`=J?3sP3r`Df@L-Sx>}vyMVGNjiN}z!;*2Z!G{iEtn3>86?vEHjW-W2kC6P}c~GIF1h;9-a~pGwa*XIKYFBk&%+nQCru!3P9|mN)ah`4O`72FB#iUGy>e0@Uv5n@O5>6#Cd^_v+G-&RUP{1kYm*{Wt*%%h`1Fc+LQlT;vW^_H^bV~^rpq*R3oz&8ZY19~mn0N%wyG=X-tx+bl`c^vAupfW@`S&BgSxp4al%9Y8*^7c>y01@#91ZZ@)T;^o1N6H#nt6ULTZ*RR<Hi$DDTDDcZ5qNYgV4Vqwma(iZFGlZwg(kR6q!Y%+(tgx<Z-~nb4Hh!3q8)0OC;HoSH;nFpPRvG#`WT0;7F#-J!MWpQ<9fIYn57P+eos0HP&V^)3Ic#9eg(RKY#xG2WEoey-%tgB7KJ7<wN3Sa4IkMtWi>2sJuc^c)LU;H)t$Ib%S=9ur~8Ip1r%0$+5Ee94Epa1_IBsU;LeFR}nHy=SFcNC@Ll_Mp6qM;w7dEp@_?niaq0AEjL%|35?*t;zQ=QpvWka{k{&C-2p`bZF6_bMTPD2sP1~5Cx~#?Wx7!CGWA1Ju@!KDn>%wm$9&G0u6%irAqaoESmg0JS`N4fqj~@>K3^X_v>n{!9SD`uPJDU`99>%UO%oTr2o%gA7m4CU;Pne0j1k3Uv14)$XaK(0^V`zvUxF8QzPpyqE{+A@<|a6xMP%;pU=c1mx!V^-CzR?Hp#rG>T~B#T?R&Tw1VpLLmN$gtPP(<H+TfCH8@VFa;fl2I(vFG&(9{xLN4p319#<>aNNlDxZ%1z?f29G~IJa@+q9v|kVy1!!8+O@8**OTLh^1{U(rTPM0qW7};+M%#S89NhMPaj}y>pR(b+NSz+<XzVuFX8Vbz|(-uU)lDjNs&M))WN)l+MM`?yaNnct>2qvaY<EfsFwe`+N6gr{GLuRA@UgwrR`N0;}}y{N*eeBGd$l-alxCa_{Y<{ev=UL~?xx=mITMn>#kra0C5qbl?A!lIvT(U#$pCx-$6{KR|323kBE}LJB>DwKMxZ)o2y9=w0qk>r|1CTj^Nypxx|7Q+vLeC@{DQ(|R_zcgx+^1>(Zi`u_Evk$u;nJDie}B(!b+Zj#WpC#^h-B7RW*b@+!=ScPG@Gyl8qw(Lc5k74Nz&NWGSjfcm<REbkAl??r~M1J2QnTDxnkzC|v<uS>lv9oAw`;Y;TZVqZBjNqmrBkc!G0^bE%8FF7hgXE!}cq7H}MCQF4x3$Z*%ZCi;%u9{iG$^E$nT-lI+efU#jE76Pw$tf?Risdb&PWz)zI~?Ah*wN+LH^heiYj?#L3VEjzs5R%$^E^?;^Z`zjEycPU3Z)<>AO{hDSS@13%b&wFk~Ow1CSsbvJWhH1XWx~RfC$wP6Nz#38*IvxGKyQXRrT~4|naj98ab}FR@#{<gG@$%}L7+*TP}2^jFuN0WD;+OgYeCM|WLSqPx?9fsvevZ;KLc#G|;|ZVU+~xfK#vqgvJ8_LkoVE6v%WFKzUlyWpx?+c}>Q3m9(E3}fWRcdSRcDNt@Crsh~hf{(T<ehuf6>9>)MCh}v`Exk8Qv)v(fc89iq@Q3gjJe3ZA#3T|FVnd)gf#5%~Cir&LXPRVK#XXi_AkR#;(zWcK$7W}>ORVZwN3WHya`U_tcPr)b2$@gk`+Vxc>kx(k-^*d?^`~)}s{h%TD0H47^UVfsQeoYPQ&=2Ky)+}Fol%SxfNN6=cRB|lucbYVDh1|au)NzcmcW3TMi7u`Q`f(QC11|ZI$Az;i2p&eK#Z4AWzoQ$^kO=DF{`5&EOWnAmRL55wkw5Zv^LPeVU!;bpcX2!6TeAk=>%a%(1;ykDcoxm6bxtrzNF}?D0+Q;t&)+pF-`#bB;qF!AAA^v3XVqZsg<j$2Jz>229Yhd&UFeOU}mLnxI=TKrAezQiG?{BE6RDu5`(}vk9j1XMtpufu3Ru(rqoJJBsF087jqe!PX>cJcP?HKIMLUaL9GI<QxXV#RuV6MU#$gTNqb{0?lYIz%+u9O3fp-#=qt3MNL~dZ`8GfaRmH`4C7Ae4<tWsB=yR+97T_~drn1|N6!4YY_B7jvwsp0lF3UOiD%<-;Xkr=M0Qc2(NAgOz0K+RYwWf4l!2EGq5{B1+M$<T4#c_Da{jzs>USqUnx>UXh%vLK}eAyP%-!X8^nU=YumB91@@QT{Q4jO`lEi3YJ_<Aph)+w@+d`5(+2hi>%<L&cw>Oc1;@xozgBx{^k`*jOm2RKw9<w4vR8@r8#>U*kGdvFS(@wNmVr2a_z1M%Aln!o!ZiMvBi$*p>*WRD`8c0H}Pjx=L68yyyoV6$t|QYEJ2Y5|IbkV9G`RxTv|0{EYcWgRt$_B^(~{^h^ov)EbSgk|Qw`zy^HBYdMx_}m@BlI~yigz-o)@SR}bm1IsVv>rz{qo}0?A5}6r$a;c%6?_SJ9z1?{cw)AGsK?;VrUgi0<G%Q!4OXY!dfu26w4-IKY8id6x0Ju$r%eo>fkto1#nH2pc^0T$-4Q6V?)E7I1{i{lmbYwPa{Jld?Phxocp@-TIvdhuT;GAZ-2)^hJ}V2ipdYq_u3F_3JMUC{P21=n9-NJ+J)Hz4h4NY08ClH&?e5fr&^S~kj5%s;QM;!%P8N-^nelDdOa;<Z;x&dGNsm+0oR%XQm1VSiNZz`EoX5ghY}d)JjJ=RU5uy#ZocsKs*oD!G;kQh((ka^wLSx1hG~N%JU&9a#hBn?+CoVu)jB(u)HiqU4OP;N?{I)UDySkTq!c~=GZ3A!c91P!S`;ZuCt6C&^35QR<4;6mzi3_%UaS=2z^<wZVwoUuw>s$C+%O?o%1iZ|?U6p6(TEM0ecDVc_9QWz@3Ik3nk#}^W<jaddA~_W@m@-*5O%)H8J=cOt#m^7EIedJO#A<XkwCJ+0ORHDA`vTwBbg2t43DibC!#PQvZJS*-$iHFn2?AdkaLXi$`J9^asnV3Ul7~BKktcqm3LQ<(nCtq)s#GAM<Wv~c79I%%AtlfO%^Ut8nCW~QY;?dXif+r!-XC$lCUcgvgX7yajM%&gU{W=OGxkbVvg&rbMXdeT|MlX<bUSb0xhkgIZa^+jXuW!$zh)G$7S;0gc+0(eaOTw3Cm`9G7*QOz)_$8>;ka1ZHw=w0{UN$><ie&Liz6kaE3$gq2rOa*eBuy3A8ZB^De`J)<*pCJ>J9{S*M7oo_Oz|_ziaNh)Iki2qe#@}Yd!DV@{Ca~L5H^{JPVj+aSgV4x^)r-+m%aHwRVg^?6$;8`2Car=V$xt-+un>m*0Ns#qp!@Hh=x?pA%94<!7Gp^_P!0nJ&{~@P{jIT$F+NRp3-i-{TL>;(c*<k3L;=X?i+Nz5$k>r)xe<0&EvZPJBSv^p5c=DnC~`WbmG5?jK~6yTySN_i(PX$?e0IV18c!2BbY2F3;2;8#H!#ug0E~YRg(ODNe^c8HH;wAng~@phIrCD1mlwJq%%y&yXc*X>tQJa?jgVpmdNg4|@f71Wp<Ih0c}An3!4M!6hsAPK;`Z4GU=F@Lk)kV?C=i)<fjuRMvU+&GPT6s-{q@zAh^i`dT71+MCJUEA+OpHFCbVQEP4HO0I0V5V1O|POA*?${zdjUeh9Ke8^bT5T+yIUlts!XXloL@m$6-fqN=Sm|av|JsQ8dy8@o|jGj*q-7HQ`bBJS{L!2w!G}$>k9YyT`)G<v@hiGQ@_uf8?+rZqzc`w5gtK4i^XnTcsLSo@95|XRk1FVu^TLF!{6FslG*v2f&mYgefHVJxS!iRm=8Q4Fd7zTnB0IAGpr>5LK0kYAsfnd|OF)77Jyc?zc=9klKJG(kxwhVS^8q&4b{y+?Rsyt#X6>qU9uC-M-lLY{`KYYSdDJQ5iaaflB(@0b;8BeHqT{w!N)~4)LsG6OjiYP4L_rxx0F54wpFjT)X8@8rhOu^+xbw_9Rp3bx=muGkm&ebrmUTz)2-<Imc$b&gTfz#%pQxcq@EHPtUQx|qLcFc3m63vSlbc|M$jMtZ`M<1CIkP5v=hr7t5@pDcYNwQd+mz30W1m;d)1^IPx5F61~SJ9<zAR~_CJ#g!4QCV23POR^btkn8EpA+JDn=obiJT*%_#M#)hZaO=1LGpg503q@h=vLNdx3Dka^9j`&$gu&0VB@ZtB6MHPd8BCR&P*AK^;ve#>(Hz71aAc;bpV7aB5=s`A|WpjNh1!xC?1q?gszh>2lkgb#0!IDj^(Dw2*c;7&$+e3-w!@RlepK*cz=v2Bf;;_&~x=~XyWnjs*ht)n|q#Ca(KX}kINJ?$+KgX;%tI7sU#-NZHKut15nW(4VCTDnb#ZnINTxU2lR8y6>sWyxfdL)KezVzTB;QFghp7gjedyUF8EI!*SB^RZMS#eLBn_9L7RfHh1c1V0fgdDcmq}Oiu>CvE5k-&77B%M?+D7o;N3qOJzcVBXdi4*wuF{p(v|k+ZT1@)OD6++2HVvjx<o*Gi`Wz~+>roJ2s=fX)DdU)5Z8Q_w^SneHt)k-VF3XS4g$ws-r<5hSK@e;?BPZ#*oegP#Fq3Uu*|kZU>1xpK!y1uG?hpVH^`nUQ^Ej;cq^F>q4nV;x5c>!DkZ&VtDsN^UbTu^mGe1jCt+9kGdZQ&KmcwG$=$NO$zsrJS4unK^VsqelqZ{Cd;UY;80>7?Gg`ScNlECs$@LO3T=$%OErLW5;pZc?a6qN;KJqsNlvteeQ2LH5?enEhw-`tUqrcczm8_iGT{#)tJL>WTH<(n!JI)GhuoO`Y#PiXeRY~9h)gZ1RK=UUpQ{+alB95-G$|V8zgE66%6M1)eft#6`V6|D5CqM}T>*gyrS-XSQmg-@-cK{jDMlVu44>kf9``_allV*X=;BIS4FDbv4QpxC%)(mZ+SzU;!qO=y}huw}0St~bHGEz0_`TsMd%J{*)CL@p7N2e5&?D)GU&EdWm2KwyRpyFQ7%aVFpTrqQL4~roe-!l4jm?5rCZUl2<IOudK0E@ZT|M3V5%D8mL^>&qFN?@hc38hr1jJC)<Bm<*APzQ+RUg=v!m#VmQ8oq9i^>0A2%edS0F|>?L8e{kA)N)2Cs?Xr+c&22*YUtXEj&UjtqDZpFf{UzKO+l9!WQz<rDRv#pU`n!zHDyGkUMm;8_)L3MSh4r$^_0`*iqdv~R?=Pf=V;*U2QCShdN~!0<`OkElSM!%7D09y@0Jys2zUiYgVp1R!44u#6R<2yvpF!h{jk4Zh{r3o5u4ZhBft5&+N+D2xEFY3Z(b{aA05~eYn>)T?G#LGt!TotMJmo|{lO;ozG%7*pMfTbUXsFe?$MT@cMzC|QLKX#a~=~_DELma3bT5(4Fl~`k@9i)E(c3K47vEDpgHedJy|(BFxyFBR&CL$EA2vUU{RFrrQIs?GWAD9q}ATuPD0`bJ&+b#A^XK`Izn);LS#x$r<~OJGo3A0qH&}fjAL$BDNUGu(muOL9r&G8iLmVxXnE3<Shpng-*+OL<lY-hhAcO-)K2bA96SL_xz8>aX%q+X<0+*U<*o`EJtln}<DL!Il&=?{Zol~h@lhz{qUYL6{8`=u1eGqMHE?!H^e2X)H@D%EmRQQ{7Eh<4VZN@c^)C$1_@f&tn}C!J@l4p&D$)%;PuikV@tXY;M_G&l5%R>_>#M9Cc;Dk=&u0TE&guj$eMP!T*<9O+!0Faa2ol}~j+6f!7h|2!+(p^@3@CU6sVrrhxdm?&s^yD2v=|by4rg|Tby-|X?K)GIp@Vz;^_XGXBmv6QtIqH;p^?He+SX-OE#X95q)ZN7)bYF=mdUkaQeNoKNDL0BDN4_)s*|~x-(kzd!W?k5ajufDaw?UqTO$4*CLvHfb(`=ka<B7OS=6=80N=+^py4|fKfx?qMq$m*h1W;HXPf!4;5MAcM)AV5@0hKY+r2b}8-ZGUGr<u6n<l_1D<L?D-FlooSP8xa?L5K0fV{!aE+*=xcTq1)w?$dk<278}$mXw9<nh)}h>p63M7<Y+6;ga8chpsCb7wc<ehFNWJt{&+fObc%Q|FEnR7v95&CD;T*XKc$(;(JkFU<*tV3*&S$n=?<Rd(;Ri;}Lsa-qUU+S|<>J|(Y>`XbC+sR_Y1@ttaEdZ4R?U@%2?EPu8!Byk!arqHvc7b{!q5_eyOgFwd{yO~kmN(e78v}To021-<FU4|mrDGyX#AneTRZ@w>^eDW}lp{}x{!RxG%w8Mo!;m>68Ihtf6_$6q&<jae92DI&iD<xUGAxL9vQ$mCYCcd}KpLpI=us#l-w%J)aU2+6wiwGD==>41PO7T|`rMjmkC=vqp=rzFZSnShC1iHTI{c8!%J(2l8CPeVux7As4ZIEcy$tG`dHs?{seB1mrWkWpVsG?jGE;%?FysPxFss)34(dr&#g4{f0<At){`pzbJK6<%+gj(f`N<M0&ogEnxtEf(m93K{J@o4?Dk*JGUKR<a{pGH^GCvP^-jGy>4J`GX$9NnkX8!4dA`W7d4e#F|=l}??mpztEq;K7p@VnedB*F1%5D`C1gpWuS8>cuu})Th;OcPLewdg}IVF{GbSVh_HYP?tPwjp}A}-%$H%n<m>?9l8Ha+a*_W*QBjOULt(oYt=ks$=!|8M$SQEQCy!hBsRLU?{-<@WK~ST)M}Ty_Jtg1*P`Dnarc)SkMH%08m{12%Wd!puLw+HPWl|d@+u58rO{G7jWMh7?EmPinW$Zy<*y>RZ^>!`OC@}#jb~vCanODTr|Z$&+4ukOUpB;xL05<iB#QyCwcJX^*qkntPJoLSAGm*H;((>DhhE?A@DR4+dM<GZd6Qt&SNjHJwg5>Vc9BMpwPed}^L?g8c*|U|eIs_0)xr36=hAuXWf|AsA(B%+AEk$U8)da)g9sGoci5X@xcRfj9=I6~ZWdF+NZRkskRuhf8^^2K0V9FP(%Nsm3g*Gr=XX+96_1Ri{t#jo@q2JE^xvF1gmxEjkm45hvicjFJ>P6rI15q^C3u*H%aesG<!rWbx!>a*Vb(uw@uME<=3}Ur#8q>CVT+}7$#O1vBAjvljl+7&kStX$P=Kesf$3A6Z%hA;$yI6U39#PF+Gn(5FUVw_L%Dly3wOsTDJa9c47)V&U)2@cZkR5rw9kUGH{W>kiwwtF`5&@S^j%g*vXAC*xcoF#BsFm*Wu8Y43AqGYh!lcZMyYa-6M6Ck;TS2aK<M0Ajl-ntBejfEFU?%|T$#02(+{VpAM^V}kIP%gV9QwC+!F^J{PLU`HRSRRw2Yb-E#uPR{srD|)RUWAkDCBvs#mM;3G-oaT1^x6`gMH0A6vdqc5gL9K3yRy<LW|}%4d#P28h%m^UR<PHa+f7prkT|vn>O7Itp!+n1qt_wO=ZSIPmN=9l8LRmbqebw1#CG-F2R;7$TQC#7r!lNA~Tpj3(PQmA*Du!UD9?fO)|3nLCa9n7bK;+*sdjN8YcH^yo(M3-+2W(OjrQ5E*}+EL}EWKAz?W*n-&QQC*+34{Yb>yy#3C16`O@{%N{dJsUnRQzC2NJ)%s|&&&>-tOPL=yKO_n3eKvCm|FjN;NNqR%0(K{sS7N(Tezb}Y<z4V14%bJhr*_%s7}-`PPR0)f<=n+XmcAF-UaEKuYlSxMrR1+J*9iQ<G)F!7^H0;J<;079bGfjpFO3-Y`QUbR8YhBvrP4{gU3r0Uzo1axtH07^efK<V%v}Z{Vm0UOK#~@k&C6W?L#<uV?;<zD;;lHM&fQC#j_+ac!1j1uA@~^W0%&x;@QirF7^t5F>#vUR|a=#4E`x2D83*H8;}eCc!kdX_>Ry2OmOT`<dGvX+P;AKU`VwsjR1YN<FL^SC^9qn{L9%Wp?&W6&p}xwo9+IQF9={4x3!)mQ#7&d=`=o5dcWRhKcKJy!pc(8U>m)kua#FP`rEDAVNLaH;tP>NB_E;n4GqelzdpJ=^_a`UiV{bc|J=vt7lV^kxRDWf(&*HWn%H{uvUE95K1vg{cR>5Y<B#D-*`NqoF|_|*<9+ni2hp8+AAPQnkEGyKw{*K+5~Q_ZnE3I(R^&Opv0a-Ne~1$9_-%^ufGgJFmM@{!HkuKX9xM3q1NR3LatmPD(y+~6loxBop*xzP)LF`%jZuLhP)O{2KigaAqnc9c#Q>fArko?P^}C9E6;^u<osZ)q`0X_h-QY0BC)d+A|K8i*KX3ozqlPNXv;-Ot8VnirWRiK9WeHU$P5h&g3%zzgv|-U4f-h5j@~j6+o)5EV_fSPr04R<4r{)(&n$2O}x=lEd>ibetcFmBjpL_u~k+h?uzR|H#D%<cDF6(nJvD&IJ_u-)?{yl8}^>M%d^7p^|?Uz6A!2kaE_{RfH9m?REKr`bwnyv~2|3hT){n^6M#1>6GNch#C7GKe6!2lr44V5=|b3o{A1YYYDT3`+vPc1|PKl`=mIrH#8{`r@`{`&uZU$DRZlW0gI%Z;J3?yf(L`{zBsBieR6_?VCBchhsBVs|JDrhJn1$_9v;cYE%gYE3E=?*!Wvtt`xf5Qmj&vtKs@w+QF3q>M<PR=e$4$qvYNLA3G|!3|+7>uSYT*4kjFQ)9|th}$~Q`Sn^ibZ}3Cw4XUR8`^S7;SsfreP;atjsZJAgf*?npTy)(Py+cfnG}|7is@AAAo_J1#)u5Uuq5QOCMVabReOB9G?WAw<0L}2c8=?+=<?k$(RT-*`{fNDnQxrm^$pGGo7>HNmwB(i%Y^D-QPqSqrBgBy&2uBxTdtB#M|P|G6QT=v9b5{e%Rz2wMd5dkZb=dDs#((us=FV2@zhuBgM5{u2GH=Ny_X(=<$wOXf1N+;EEbs3MCTe8Gxt!m82mcv`7o@-&UE?}eE@{|*du?8Fhx#QrBw)ePP1vS_(c@ETBS%{@3^Dst8ZZoV~seSa<-WapA1XZ%@3LR@)E@M=6M^1@*JrMcIEE(g2E9ru@zm#+s&umM{8cvS*;62PWLvv3n5YA>Q_prtqm1c#2hx;fS*!+nN=HL#mQ&hHu-*D)uwb+QQTHuP3vs?aYa$N6Cc+RpBn^kDh{C~b1AdYf2waw-m^>;pmAR7dhS#R!K~tJAfv+G!SHO~Zs`^upnHE5MY>9|ji29JnZu^OH&HVbeDUy(C^nZ~eI-LYY?hA(2}?DPIg||<cSGJ>CrGDkO5u-0cp_a|xui0aBq$+c=4<>B2`A{h7%TeGdCNS!3VF!Z{JF5n^m2&L)ox#ga7o2>U^40aBBonJ5u8|HS7i)$br7?LG82r@y$>7=o7)EJV)b}yza|SmcPT8uh-HC;H2Q=>3*S1AjgjWN@tbwLspFl-Br39@{}Y8uZXSNTsoNn@=b=@^v<XD2(lX8{BaJ-XY^!f(x6xuf!OYbXyJlsNH$Sf(VFxTK@*TU`CgjUxzEGEu3M1}m?&;AYNq6ERI!1#=`EENNfh$s}ZvD6j2s$Av@X=l&B!|uQUA4J2L|g_kiuTaD3=V>$t()!DbI+HNpuvW@P<MOtb6Xt3js;;G4!uT6%T;D(ro3KGD2(36K{2V|cQpvibEJ-wj_5siiTpmDJs9nx?=&6TvmilE^k~#%2i!EM2C6G3F?%#Z0Y~gp{c(YrRj>&B%yASbjYF}Al|ToMT7z(y>$1a5YxlFY3pK`?GNk2ql}to2(&H>xbNSUz5<55(leA}3J5YzB<FF;j&y2xFSjhl+I36otzbUd6xSm1vnz%9Cis!QtBjfqbIU=2HW8F5@N~yi5JH~P7%LDRM4?9BhM*rtl8OQwllGoXUp!e(4HSc9-P$!oIz^VXK^7L!`23F+U#|B84hML)|aL>rl#*g@TQyBLoY~5l%aKJp#wHAV2pcQMLOyaF16PY}kv0YtE(nwGF+W1uA>a9KQee@D0+#^qMRu{r;@^tfqJut$c2`tGYvV7w-_+CcD|B<R!B>#V$Y+6+hlbeiBxGAPiz7@q1c-3`bs6|%P+(}I)IT#j?ws(Dg6O_ENmL7dH;V3r&)^k*W6isQ#`&6cwg{TX~>C@WFSLS6Q%+$3PV>}vb>uLeJ0d=If!|Kwk%h^&py>70*o+EL-Wirg~ie*uXcbo^8shs+Oh8AdXy|ihxjZ_#nkb0G8V(tXmJNx9QbR5>EuRK=x(Xu&F9mFM9qn~I%!ubeCOG^jFYE$(x<pG$>^U>BNQ+`!FmGS?_EwY@Qk4CQctJKESgW}sHIJS}zl|uc&)%f`9&%f8)4(7cfoP}B#iSbu3;p5RH0m9C^od^UCWKJV8G;4>inJnJ7&mNSU-2?QEsKG3|30n)PPjx1bb>>SlA8=mAVw4<1ZM-`vTRb4-NavI5^|V=&qr$X{tSkaF_YKnncNY9h^bc6cKo5b`<M8Nio^%&8znh*gDb&{($mjyduM>OMr|`8J+9+-NLySt-!KAnFqfbVmGy0}7j6#IvNs5p4Rng<K`3s>hhSnl&(2n@>am`9lBK->xc*RZ_!I4W+$D*QEu*jS|x#vNlHW1;Q9L?X%pc`#pl9TxQ^R^@H4Igcqn6hxR-X<u*r+EW}wyh_*z$EKrvH6JjA=+lANx?M$ItaZ`wXB!Hrv^~Rf_A62FHq&c<T9tKcW7mD0M~XX6yg+?@L*~YoOUlpt9hC7A`JSg&#m{LKY#us$!STR`t57uc1}Tu72C^W2Blc1i&f>H5fJt?TvR!c@U324-ora^uf`OM@CcVBuem6$S0#ArQB7-;*NH`;s#~jT_r<Eff+Jos!y^J?uKAnG3-S4zEQdqe|B;oIj>~SVQ*uK0#EXZ^s9hHz@(x^#-L)pli<;_!_C*rRx1*R$&FU%(kG7jiuF94nP4oR-{y~opjJE3}Eig`tLkrpV)q|}v%0PYS-BCiTAg7Ybpt=^^Y=gE5S1+#EVTy><lA|%=T3lT_xu>#4pZm@{HAjoe_OLzGan<tum82G|Yo~pSU>p#{fv2X!B5N+PvTp9m63I7pzfw;ZO*^t@NS4{4m1jvMQ7}jTqa(S_HswPVIVHh%0v0mkjx@KFyOt_<5VDqft8SX@X3Dh-#-U?nFJjej!2&h8Nu*TFH9;neY_e;mVG2sM%&2&X^5!DHfuP;9yUf6K0YDD)D)ZTNEmW0TQpG;6S{w*qi?%T>A>Y{(vABSwLWu}g=Fzb7))gnaN&2VAwp&QrTWvQUZKo!Vf8Z_&8^`6l_)?o9C96^zCODR%_Egp_ptRYGG-7FX4600KSvNp(3uxdVD8O(~UXhb2!P|&4^0YM8(bzG?4sPEgUuT?Pi-M5_eXb`D46iIY)xuxY=;ZY)C!5B1G-vK}B$p2gB$<#zK+wJ-RwI>uQ2Zlq7-+`w&Fjnz?BfQmMzs)UVd-j6g4Yqh(kqV`Un8O-JVKUdQ55aS(d4~HfZYr)y`X7H*FT#v-EMhVMgk>^h}s!J!7<6xZRpc$(D;J9(sJcd$)j?*jh%pHRvpCFWV{3>SCvV{j#PIm>MoL@oAc{a-XMSaZ@S6rTm(AZ%H>rWS3X9oG(6P7OfOfDNnSdgl|Q&=#6#0<wKZ#~A#G^v#Q2dV#B|#(EyCD1f!xiY6?@;x0!dvv{%gbXaFB-E)y0Jte%vBaubc&$Q{~^ns#tg0TxuYw<%c|4H@-0hp57bzPQ#S6yC{ju#fgH*f+lh_R$0?C!nGrC3d3WtKT6L#8r=Kd!_a8Za<$wIwb1h4i$+t|4m+r~(Ia%}plR6b;!Cb?B6Gl?mV`%(_B<K@E>NhTVb<Bn=Tc?7lBq?>%n(_)_S~h85@EDALl@V@ZVh=5rk3kC+B6oLNMu>hP|vTyw`rVw@)Rcs1I>ts<}jf)CO_3{p;NNYnZqcD{^1JLyQ8qN*uI+i+_LW+Vw=j>%~xJ9)P*Gs|Lx!-d^1aX7{&-gTa+wq={Y}TU1HR+jKsisR|R7fd&)I-d1|r<B^=i2=B_@H|AF@~vs1`jT+`q#M6^RZl(ZF=(Cu8+hCkXlzGI0(k1Vp&h-@Kze@&CE74dyusme(0pLl`#j+gXQwu~{2kt-c8pqCTXt})9@RJBL@0|U$IQ~oV6d=(#0Yfmtbggr2GixSE_{E7W$o<HN|Xjq$0ZLXII4sJe}*8I*hSj-WwYWH?FcXu%gkQHVn2svdbQ_tdjmd`eY59Z?m3l^qW>Q35T46ltHI_(MZvK28}54b6EVMjM=&&=cV^<|PU;b8z6XwsDDqrP$pO0Z&?RZqJv!Uy3z+t>%mT+`GHstlkQ8dGIy6U=2N-@1EYO5_uCWbrFFTBIgb@_=6v@w;};Yv5XJmppHITjK?~y>)?#P=!VPM|<{fSeR0eulPTaXHqYjd#W64yk(1~*n&HZii_<`l)+uFG!TRMtx>JP-B)F_7cg_}CU`AR@P;e7Ocz#i#!R9IG%%3a%BaP2j`L~@YYVcJ%w{UZ=GxOzqlD<qHj|EP%i_MQf%!(WMAc4WI2GMWtF0bOpjS4y%!;#w1G{zdnfP@HB6nKe6jzd*%5Eq3O(Y=!DX=_0Fe056Ug$<+1M_!b1GU)+f-y=W^DnsXkhpDFc8(M-SmN&WxQoI;n8Yhr)Wp<W(P^3N>@q9Z;m!|iu;;n<BrT|ZbM(ZI%pf?^+WctZ`YcW!T@PYft^{s=szZ>bqYjSQZk;#yk_h9Ti6~#a&sCYQIwHy~;*Qv19#|USNy5{BVyEbA#>_LvmGeoo+TxrV+a;(QB)|;{TTF|*WEEZ^*@)QIrB*PVT;BMRqz<ZhBGy~FLT7Sw=&J1o@)ONb!mNZ*fT(jKWYrjP?mDK{IP>hKgm`)h=VIP<>Rs|rWBR;0)VhaqR;2%Rxc;<fvz<WK-qd#F0TvP1#A%txYTeaj@OW8mMs`nHVi-w`gtdqlW4AeNwrk?;yLLu^lpVsH8i{Lbc>Y=UsEX@z0XE#T*!nSXPdzs3-hmET)MiE{k@8-)9k<)Ha_N-7M+0+(A+-x;8(i@}qr!p~v(Ys!%Wb?|{aj^<=$%6ky%37sCbz~4`=Y#5B~xt)gEQypyUlrU<}gSu-v!HTc3CCcc7R7{l-Xg_s(p3{*&_GS7g|SL!1Wk{#T^3F&ahK7SmLAr%d+Zd{HhQTR_Y~@xFF>?bc%o5GT!QKYBJ0<v^^q6YJ4E>9fRl>ZtcDN69c>(x(7~%#wk9+uQffqj`pcMq`0juammvU&vB7!HdsY5m19R#xFdY+D`y|3wsKPOV34JeWmh%Vgaj&$*?~@EDoRE02zWEG*J`j{2#u<8`=CP&R_b%2`qO&$=~kPAx0XTBmpA5#K<|b}H3La}G!A%7eBdfXV3gO6nqB@Hd{1p-&}`$jgXsuT2qC%wBOJZg`()a8T>w1fp^)>M9hG!t2O%O#tjssXC=D<scUe=We^gzo8@Zovb{WMy%FAoM`E-<M7tEDQ37ZRU2q8>`Df>EGW_G?|so;w*;V7*mm}@ty)5Z2y6d2F9xnrQsrv}jpQWvzNWwN9@MuPh>vNmt-Z|NNSZ?4==P{!Y~bRv70iW>;2`9S$*cJ%CLH`dHcfMV+uNaH^R<yz+3)=}H!PsrrE5R>_~_lR5=kG_??Gzy`-fki0%d4)x$u%FU^B}c0fo{yT~-7bz{a0z*=7zf``6xq=&?BTVx*8&cX3HZSZSsyK%x{VUNM-absyzl`ud-jnUAAcca`yZ*)6Y~T8I+Q<qV)(bTP+JrRJpU{L0s1O&pGn&61!e#Yx~La7YcymY)=t3|SU2sC7m76fQn6pA(>df@0vLhid~49*iL~;%W;%TQQ|U3x=9{(03_KC#PNi$hi9*}OW%<l7!52C`Sh*~4zy^2DIP@8X2y33_al+?|TK!tCFpp#EF&dIdWz?AR4oL@*mER2E51LC8<aq^au+Lg_)-E#&#Uliz*0LeTIXaqHdfiW%z0ln$1{zn?kihG3hK-eZ3}`+++o)C)SW9$@<l<pp?UK(3G+Ag~6ElgpHlE{x&3BVEzuCM-K)m2~z>H=WFiXJD?;4Z3;a!>z#M?b;IsV`^e^e-)r(5TiZT&*YG6DP5B6|=J;RH#h4uj9EnMjhE(k_$fqR;0MpxnL-IGL_leI^7y2wV%H6?TFvQpsraTGcH8HxF3tKxaUDn?qBulgK<3+ot#<OkgR~7KU(!!68`t%eNajwXI1Ge3&Vj)?B_Yp)01DHDO#M!P#l^!5Ae$0t62$Q>Eo@^R(yf`Va-h&xyT0dzDTvrWwrhE$^cS0STffr0Q5B&o>Y6-FkM#dLA<2QJ3C7@iTE&`AoNxQABLhseG1D%Jyb*HwBHdZFL6C>?he|^E~H$E?*JSxbQ2_CYtF_I`ZYcwwTm4o0*NOy<()E=fyWDPRV;X`z+%3k(&*)eRX#L=ju?hY+~7GWDxVbxjTUS|I$hmpg$bVmvrTM-rsv!umVxE>N&?`!;`1jNl~APAT*EBWe_5P?m<*}1F@ng;?2lc1;?=BI#YH(MmJ8O(6M)CH4$0O41yEmV^t5FuyP*iDEt$*(2}@jj7ywu{b;b2`Zs6bS?12n9m8%}Cs6HP8+Iw>Lh+Zp9I3O!>(SQbEfCRn)j^$$Z6I6O#`ri9BjQ-LvxNhOSa<~Rq%j_aEgxxcK@s~0jrUBOoiT#!vgg~}qDAbFn5;K!)^f`?t3|$PvpN$kagzs~1rJOivI$sOpvGzL=+hv(X!bF+g;~BO!{NoCLxEQ$4=UM<!ZL)jTR+QuGhQ+6=HkU4E}FwdQNdFDHH26}zB^o!DFB+fBo+#;w8F3ixxjmc^YgO$Tx^^F!+;czYc7+Y%jWRpUhn|&3S{Q$mx$-t9lP7gCh$1T5ZCa=7jb;BPuE*w@l(43uI@0F6=>X$Is{qD8?O>@(S{%?Xx?bgI5bT#*<{L)!5K&?BL&JpwKgG!79=eci!WN8v*vL;uYk7gQ2NZgZGTW#TF}IVY?Lq^Y{&EKMBh~+ye&tg-B1WrXil9jmT%=8gfNc{Hy53&%^eL>tuBk*#70ioqw*JG1}C7Gqq7UC>5W<N$M4wr^r&ox9Oo8TXc?2r+CPQor^H5TXQ57PWc)5{WK(dh@ReOM;7I%l-AbeuAZd+<Uy+ky49aL%a;2sa%xweH0d#?%f)?3ix0g8p$X+r23N6)hG;{Ww*$kwzIJfIdf);;{0BCR#n<GXM>~g~N$`^F(h(c3&54E`q&Q(V16K9JcQenE<xNn8Zi%6v`T#Ih$l;1|H1h|V{kB&vr6JXilJCg8GVYCI%bcMZ2PeQa~LlO#$jOufzZEWRK<asTr0G*eHphblFT!8jVc$OSBJfZH>hT4!o7c%?wkc$DLeH2HiOO^?CiBp8btl0|p0y~*1XQcL+#o-gtE2=GJly+sCWKNx=5q^jWDKS3*8F)AA%-kd;VfRHZQR<1;9$<)l?}|i@rZ2X6u_Y9Zt_t<+h(R+j+-v`t1X2Lrx)#=+(PdScBQeieKLZg-VnVBFORCfE&Pe7$^+o$`mj)5(i4XH&HHwG3Te;k1ku(0n>ETZk_J$@UmfO%#zuPP<YU7<(udGtrCjnXsTJ*EJ!BWasi)_NKGrVEuvyZl=uYCaZ{h*_sS7c(?&K}I~1C6vX%LVwT+|-rK86?~hB_@-67hJR&Jznewt)=K;#$Dmd1sqSSOIOTd`hpLuTekI44p9vju1oPvbTwF2Dnq7>l}*Y<B3l&MX!>x=Jlr_$<cN-9q72Eglwoi;68C229CP;m%sMcX!R7=r>wRgvlUTleh74usqycAkTNI)&$w+Pi^%8nbrv}O)xPQ22>SZW)iX}E*VwO$dfD9|9+bcvt$e6qyL8hFUkvd1?^^gOKsno_=(?MDo_x3CS=33A;9~xq8#qw~%dJxOJ#H;3Hc*Gpd-R($<N@tml4ki1Q+`ClvOF&dFL^VVho2Q~=t>sH)(bR6)7E5(n1t7<G@);ar_hU@$;~;dS0yR$4{91pHP5aU5{9DG!*D}J;dr90=z$k$Z!=K&Lfi-u!DdU{Tl4f1W>6SjHr}GswDk}=UOh|)lpWv%i@yfV#XGeXes;Bqm>9R0d8CM&~4Ap^<YL^Cgi~>x@=<ny~Z~v#+J!SOuGqBdVCw1yZV_r^~iE8;?V49@`wuT`bgz09#zn_pvgj;#U^n3hj4>!Ry*hdl3FqwiZ4C!!p`=gn;tC>bnImkFq?}@^(Y0CNHfanTdXs#TDiSv&Z&c3K3QK1BnEX}SMVAE9IbNh2{3tj8cdwyEn2Qf1RcJ%Y<`r@Fm{WK@vEY&kc&X{$SDIqJpx>h}nXSf{p#7YHA&wZ%U7h)2IkycG$36tEr8x_6NY5GJdl8#OyvF@8PvqUx%RR;UCGHjwc7O}agOOdY61==<xRyZ(}cn%vevc>44?Ms3g*8{CWkq%7M;6sC-Dc_WMluP$Q_Lxt)IuQ(L+Ap$CnZ>RMb#|bMbVW+erNVg)pU#G_t_>!sxQxj>?ARbGBPM4#+Pqy^<ne{4fs^`!?d7p|@&*AVf?L$F$uZqo+5s=pCl~^6)BkVo?RFf=k)+WVs*Cvlx$NCe^bRmHHJI&zt`7D|zIQ*}l@Uq>X>MlDQ0**G7lKMDkqjs4Zf<U#(pGU{5W8|{p8FdLFgJ)dj*jtH(0z>crbuv2!npp>@*X&3Zqf>7%IF?u?+$Nr1^%g6JJmbRem-cTInT2z>2EEc@b+rgJB&x?rL9p#Ykd|In~ev#Hb7F33vB;QrR9BJ+3q$l@<hPAwQ!JV$&FpYr8I#-sv{0n=Dm#`!NV(GPxgGkQvAi8(9*r3FBhp>KnGK@k}C4Hm%gEBuu8}Xsg49PkxXVTgRO{*v^nxEleh?z5EnVdJi0QVibqD9cWjbmlhrYOF8cHiJy5H2CL;tHI!Ivg=NvqZ%m&;^LB)bB8El4o7IhCZEb_T+H4eo>2AJ4s%M}+wN1p@a+t?i?4;bR3)qWCNDQ0mQ3fFzN%0M{8A98Vk@$V|;Nt}Q604P}6rVle0>P3vrB$i3rI`s;LeGu5K&^U^1TVW3BI#B;FJDU$3XTlY7NRFxFF@b0RK0Sg2F<QYf+Og5v8JGDR7ujdkjbV<b&_JpyY9uj(13*Z5+mnsaU6$rT9jQ$x##YqLs>B2YlP}KI*MD6=lJj0tN=iu}q5)JXwUPpj7YNEy=)uy>9l}B(<I7~zqB&xqfYPddh?i(9f`G5wF<O?W6SR<%A%7NLUh=*Lt|Wj(US41k6bGr$_``W&ZNC1l^cR?nWM0H2M0_fpC1?Ud{34|z`Jg!%0>Od7%c@a_I}(dH+$GFxV?wF~JZC2PE8N}I5OtdzduS@OWs=r_Dnb_Dp3Lmq2MaB71|F$WwA3O4n^HMZzzY%WenhX9Yd5|fe~%mVZENnlA<1*tH!$*g$!DTe!nXO=Bad?}X2z;Dcx}!x+&$B37Zn2HIn)J0GWQwjnGmmd<pI>*wH-^My4Zt1INd&ZChdK~s$u{iZ0^XOfa$esInTRP_O+QTtOk~$G*&yfW3*$+!)>eDe%P>OZbuioNYqr!7R{pE?%eAo%g{aD_c?P0K^s2as(3tXt1>V!4G<TSNLY#_N*rPRGOO1TSdHR_v$v?~D<kdHc7aTkpBf-Ad|x#wl)#c?HDC82#GiI0_3L$&YSNvNg}SFv)b%R|OKs_RxJtiuxP#3sg=kT2p)Y$I0VGCCpa7N8G@rR?LW5r#!30SO6(vQascdyA)Q9K@S>X=p(m|C$!*NZ%;+B6C6HzPO&XtxXff*Q?Q5Q*Qgi@$}nsQM8SfYP^|GGYwLP_Yn3yzN|ctu5%E~82}V_FJrA$CpFF;yKVdzy<{@L?&Gg=pUc5p>mVFcV>t6f*4$oyIVn#vr502Sg06Cezll<6H#Z$mRSI+rInGe>_}5=)+Huf+dN-X%UZA)9G`>46gSR112vc*R>7)=v6ogem=ct(1uPBxYJK$Y}GxX8wZqrWwqJ;DNJsZFJMGUBV*-qY<nMLH11tSl{H(5i#prz7U-A6EpUEw9e_9S`fsxZD|=XzhYXJ^U+f#xP=xdr!fV`Y-G#>g$=(<W@UfcxrhI2Qu?uolLg^2$^ckQ!jB4<l*fD`!_6=Iq4QRO{jEN{7*5^ov&ex@h%UJP$VstM8A?>|U=o_`Tdy4EM?ud*d;;VbD!LB&rgF#lD#u*xU08p=khCAFZyZ|BR_87)iZmTU2PGKM6YJi#}rv9=FcV&7Huw;D;5oZ}@*O!o@AZE*I<&Rzt$uZ*6%$Ygbm8wj=j;8tR%@hmb3~a(rGg;j+Q<@&h&;nPqd<)zFn_D}ZaOQmxIXdP*=6@;lj4YWP1(f8}cH{OMOQAE=B94RLD;gRLg)&Ere;IqfPcqlycZ&@eQNnfy#=*7UTxTw6!cxCC#2{=mXdG?zRl2p9Y7`iy0YL!snHtTWsqe5P9i6*r^0S?}bDKGEaz6nOe4|*J^lN-z#}6h2!=)J#Pl_N>d*uy)m{}$ILoZ_jgJzuFbdR@0WmdJyN(hMu#*8s5Sp7A(B!-=&^ig9;o6V*2gp%#;o76vwmr5zz#DcvL?zGBpYC*<Jk;PJ|BC$j>+LypbFD}#<IOj7bZn*CDhLE~R^lYg8ANIsp*<*;-B!rRFeWkpcJ2hr(iRVV^XGW~jwfKbK^`ZIWv`|k%sAb)2ouRG#VW3@OoTjU-CPTrLx@t@SGUX-VRCz?eOFy4Wu5Pd*P!HQ@)E@(Hq0B2SL#nuQnhmp6X!$FC{_)#ypTF_>j}(Rtfp`x3&0{fj(Jec(Wa%FbP<)j1vO@KBRQF(b{p1vUvaddQF3LLEs?-S`WV_e7)q6EW)cQL0(!IR(<(X8r64tOSl8<bQ;-0tpWyoFE1)URVpAL6_p?baJCyPb-@%Az0u|<a$3TYox{;`kG9|q?vm@9A9oS9T{oJ{8|W$_N&*1!Jq`#*vkp?>lFF#IaJPad)uI{&ZrKIXdGg@caFc~S<fcqrpoj&uXZ5ro9e^Pl7HpKG#qdtzg|Vg~*a`Mq>6!f>C<a}<QGedne=7|st)t>;@$3x2-fm49%-@o{_Il;z`_&M6im4WGkM#T7~eh$(DCXzTNL&64RC8;&NKSfF#?%;$=1?S=i%r&xrR$MF%odrvemIE?Yh_43Pq%=VA(>$^X{tDl56{QK(te=Kr8%}L3`Au0_BoE^IoytI^afV<ci7N4U2KMP3i=T6h=UMy*e6ayt_Risu}H<6BQFBn%nc{zWCk-t7Km|y<>m%sh;!*IVpUOp2DQXG$C9^8hoe|~Fl1l9gf@s6ROF`NUEPTYU|>o0%(^?&~Oh2Q^G<*(`iJWr1L&yZs~AfuVwgR45GLOGO=AZcyZGWD}mNjXMvJ~oP5Jm0Dpsd&fO>c;?AF+iqILExkp4@0=v#bf<3s%5e(la%};kpW{K|9*~S(GL(!n5a6!%Bfnh8+@<7eyd-4*}w*3>xYbNq5YiRdCeZbx4YC36TRX$DGnr_=lp;F*T=^{z7}Kca#z0(sAT~--G-)LdzTGhs0!y=;Pk8A7MM94bs9kmpY&^EA79mksg40!``YyD)TYP$noL1gUpj}4zC^3HMBdIfdaSLpD}JeJ<39JKR!ne$X>{VP3uG*lj5}IK;4r=NOwgZ1z<?b2D9<g~P%ucLd~&s)3odQO;|cKP_q!)W`=CB8jF$3@%wEuuuXy<}Y`?D{?{^cjk_s;+;$QTo6qqSJRBtb;AnKELs_a7Sa&LXZBC=;2tX-(z09JEoSxsk0SZtbp8*Qq4EiL_gluV@Gj*l`Aa%yp6nfwsn1ql^nw0XDLRkkXXK^+^5cMo{ni@$J6iWB@Ulz+~2zUem=bk<8nLUPtTH|PS>Z(Bov2_hjL)Wx7By0o^veN|YhOUk6;hg4`*S?VBl(#lq7QH^{0LV2o9aF($#!XF+o*l@j|(@$zc-0w!+Pl+RsN`sE;l|<PcFH6Jjfy=}uyK0|{Z!)!kgc4?7By-QZ@iP&#;Gnen5LfzW9$}dl8bUmJB+npp|IgTKS0zIA#jAK^ZkaECWq{V>IR}-eRwPy$6^H^qNk{DW?M50MU@WRiM3;=lD=EoMP>F#DeihNP@P?=dk_*s>u5-;fY+mkl`k)>=^X2#x7`nbu<({w#Xi!PHo|Q2V-H_)FFhxCvnk%n4v#g`tcf#r&Pu1L*PT?^e*|QwA$gJ&Dp2@7LqX_Fip$t1?_*~gpO~u1pXz@=Ru7I_b1Y@~a^&uyOq^L+lW-(WrT*|nAPAls;!3FUFu+E#^vWVWGO($&Om4MOhCe@$<OKTBFs$%*e<RF)Cc|Lwg%mPd5%5t#s<VZ?#=zCxHf<$FhZU>dFd|6*zM_H4ej<HJN2i2B@s_XdZ4r8AjLml1hJmUe`?N*@Xi%TaxMm+iCUcyH~n{LLY681%wyJ<cRLXkAS_#$M)@4y;{LUjp5?>6kPcoFwIkcgpQlXSKzfZDw#yZNk~O3pvehD}2%3{;TKVraf3;Q;iz+b9?bEjpSPTtnb<6ouT;m6bQ;I?N?o#xc;7q~RuljvRAR`6C&}npryF$ofRhW2{Q7fx1>y0IN>nzARvI{oY&e(WQByrVn+LPU71@Yhf6sHoga1)TU0d4<*(Suio4k#8Ati$z4E;3eSh7p&>VuRix>t{Nk;7hLLA`CSG|AW4mj9Qb0&G%)S$g4tpD_%8Exo&w&pk!mihL?EKU>SWZts*Y6`9F5=kx;t?P5F-Wf-%@i0$n{$`w^=d6$xI4y1G9C?NZ9$EAr5Xu%46rApVc;w<tDp1WD?QlwB|*&|2jQb6$X$XRVlm$mNOxFqZ6hz^Y7+WuxQMDarv#b&(b~0KAc}rQy$&10MX;uGWV<^uuL+6Kprqa=g%-|Ftoo7>^wg&n7@ZgVJ^;ofqGVdEw4HMq>>_{GLnKk{#(@H#`&wPkCqy)jcCUtX97sCN8qQ-;xro);vs#R?KBE^L{JC!0_jxX^yshXxBtol<c(Ihq9Hu4HB22m6`2X>U(7gvRZ@$v2?F}nm3CcBET}f<Rf|HPT-Wk(|SvVhm{r>lohQo@^g``Felfl2FLL$#0m6I`!nq8fqY|PAIlu=^6qSYf!PWPPD+}V>tgW&3YHB<#B0I6_g0*B4-(w@A^Owflq8(mJ&;2$4`;tO6Wa;<Pf5KC}ONG8!hF+fEw$0G-SiT;39eR+`T<+<|bm#13B`tH?CSh*f5r7)}6%}smE(C1v%)yG7agsw`{iKI8`qMv7~`3l1=sBgu3<$3wkc_GZxKMgl3Y6>aw)E6baLBq6{Qnus|Vimq0FgD#u7aD28C#(xKBY$w-O!^2fiK@ynzdl}1q`u=N(>6$a%qojW@z2`ZBSk~?EksAp9KsXbSd^44>v+Ul!qoqTcz;paW9b{UyK93M;`%n}`s)#02^3)PgQ<9cSg^Dfhx}g+F@aK&z=)SIU#P-KW1m~@KffRNmtQTFB+C>s7gh&b<%@nc%uV4?!2uo9M+Q+VJS=`K9Ia0wc+WeqIaQbVsoQf*Y0(}-+%PCm2Pq2?Jqb(T;{$gwJe*dSJIEVQ17EvJWXSmmMd_>29phIwE>ohY4^G;0>(+pun_;($hx}Ry$8(09!<JUOBuDa6-6WPl>YgNODT2wly3Td=Kif9aBG>*-+5W8^6~nVB6I};;2KF9T7EH5@cB>0Go6)zlU&5fm+&I!`KXSQ8RFG?IuF3But-35zf%@8=i;A>#!P~ITev2e^r3L_5;c+thg292gKA7kJU+jDrC*gz9)pQ1zWnqtgZR%4M7mV0LCVxtw#WC*9XPOg+h1|d_Y~h)FTPx7m-@7mAz<6o2=uSK?U95-=tk9C-p0lJ+Qh`Bw{~!x>C}f483`<Y4U>Acu<;c|Lj>`{CU58;C^0h-PdLd@EA=Rq9oXY5Ti2|`%MIV2}ZN7l<@c!h-2q(V@1hS%Yh|I9Orfw<mk71h|Y#xl8-Dqmh7Y_<7ZlXgBTik~wozIP-<WGUo`mJKTo-s`yH^>5KJD6eH{(bbQV+4D$u4pziOc-k=_#mx-#4y}RS}2qfz!_C5R2obb9zC@+@(7QEu_&2Lw`9Jo%=%s<8T+xtNKC9P(S=4}lE+{tF<6$Z2Ph3~ZL8^HV{arvYlj|q)-<hHpZW2C?pNglNRPH(Q}<6i)+R|zA2Og%Uh2S&{g%(}QN0TAu{c2p#?w%<2;vmcB{dWPG<~0OFya+cx0gHnK~F(Xh|iu)qB0-A<o;eWIR_q=T(;{tCo|ZWDFg9oEluc7*9KjbE;3|aq@qEl0@W5;@Ca&W7N8E%GB?(?@bopyuOw7Hpi4vSf6j-yc3dua1t``?o<*vF(y!qyW<*=gmt`Tq^jDXAK`W0rv%BU1gm+!GhSIM_|0U$ONwsmkio2~g1q-!W6mdYMPq?Z@^`vKhAFShZjlM+X{O%ShDkq60vL?fn)KZ}t#>x%vut&NnP;Mk<&roTEOV5*WRD>E{dy%MsxA`>YH5c4x<77{Wo!yp%5nJ$MG;@RYa1sd$u^}*=Kyv0<wfDb>`i!Ftt6&d#u3?MPe9etwU)N@5eZj2OlE<t!Q+MRWO{RA%<?#qnx<>zeY{Kghh5`L$EJ1l)moca%_)1E(ogq_a12?I#j`pdliUz)(faG4&$@H%Jso5TdK7)|gQXfWBDQI&nR#H&nBO)fh^b3T5Or5$WvU10F9V3?&qGZ`#h6Q50L<N^!T~KwiJ!a9OH|meds_l)U?V?OHvJG@_7_EH-sD%n?VxM$c8pU~8oW?K$V8X1j?HFYOzNF~tgZDAMZ>wabZHyCuK8g5=2+}aF+A+vIWx1*&A9ueqi0s@o+9`CvD98@XM*1Bgr(`VZDMdYL7}>Eh<#u8aSm)tRoehOjRIkfiFkRF+DoafyH4NPt>?(wT%RDt2F9@8d_hnG4!01#7L?CP%_qp*EmjEnjZ>+_2b4d#qu9_7$jje7y2d$VTuL6;LE1<+vqSK->V^I<4%M05y6p97-jFfTSZAJ?CNock83v&+j=!)vTH0R*sx8L5`d*>Kb?*_P)J^<&H7>Yd-iC9y0UO<&;Tn67G1T>mTQzwqY=iHmE%X5v<mho0=K&Gt#v(q*Bz{QD<QBDn`1acpMS41>{YmW|$Y?hb9m%kuJr^rsyjR;c@VBALS9z6A5XOr-7SQ^P%=hgOZfp@?Jjc|>#>9J9f9>E}6EMaZD-c~_JZRA7~2Qqf)@OQsR;^B}}a#sKPNMU0o+JAIhyM{Dl@iZEmc7e^VNlR;=s1|rw?X7ClPwC~_qTHvktb+#8Uf1^5zx)=T#g2g!mYM7KucJ-)Mw{?;I)o+NZuNxmsPsny41Aq3hQ^!B*lYr$)fU(ivt~WPy$XH=xChS{Pr=X2vwi`n`^j7OerD^w_(dBJqS0%)Hzoz`7@1VZqyBnL`D=A;V)zUUdP^EdizV|cP;K22D6;Op(j)Ik!9aU0?Cf6qTW4zxctv3KrmI18lH9h(-9uvHYh~dU%tJMetaqDTt&b4c>;oD6!^0KR$?a0W1_9s*J0pvyK&LylAT$n@31g1Bwy56I8z+m#*v#;gw3Nr9c#R=PQf$?f&gDo(A<Zov$*vj5c^Zx`jjJ>Eq8y44ZOT1@z6iwYUNP%2qfD|=W|whj%$S0P|FCVg4ggpT-6m3<xN$=vwyt|ZKic%L65VjxR(kK;{sxI~Ri#+#z#F)Op`W(*O*-9#bxb_r(B=D3;rE`nV2Pw3^kICDA#4o;20Z%pE!@}g2?9I;FSBoV%QN=LR`E{oim#vp#&KWVR~T?wiM(SHvn|rYiR849!7P(?yMRpGUE3Gwc2A-6K@zLc)lj3$eqCB=?XCyDuUha_%WVMV@{~}2GR8ZGzKLoEIRv4O4`%hcci@(>db>Q~mt!KkD0wh?4U6J8TA`!K8B^D#>K_;-r@)}L@JJvCDS-}X-tZg2OsB55(E*0pGAX50XnG^!z9w^)bArR$HjLQ32w=iUgn)m=O?tf5bzQ{Tzy8-ni>W(r;HgtRD|vxJW!jgY83e3FYx!EV<=(wGxo(;SBs&u$isM%6H&ZDb7fbsIOXHXRkh*cC!Y1f8VI`$oWc9WcSlqr}@{q&lgUvu9y}XTDx%&&Tx(fkbT(FznEdl$tKl`TYAO^)zB<j;!&+E3lVw6iT;jIeK0;XBqc7D>WNo~s|Rke1EK;*WBCH(Qt|NLIR{rmU7{qp;FZ5-b!ZS(89KORK+$<I9F_04CTOwIII{Qiy_7iC~R)2Qn4JwHfRob0lf=^k^ssnYavocsh>ej4xTGzqX>AUW{?VbeQ?yQutB)FA_ZnyG(~O^yKHWb4OcgtOiMH}3g{X^)1=GZn}NgI(TRV^12tWhI#ur(-H=oFN<>^!`vW7Y*GxmR7o-VBA{^Ls;Z9NGTrcXBRK-o|mma=^(#6><aD(oHEu6ohG}b4PIPgxvbqfkzoO2?0?p_Yp`c!V=Y8JPGy}YUo0Q)Hu${o^>sBX6#804XmmECyI1IKW7o*}#f`ewW-7{+Efpe&xvM-5?b{&KLCM<B?-ebg!iS7S%^IBAdZNeV)^l=8LU=ACnZPv_CCm=a24GmLyDQ*X&*=H|(9Po1G>16EImD@`n<hJlr=zGGfI6n>=@31c{k^vj<2Eq$a6ZfM#F{(1EVRDD8zHgq775AK?g3VmVOs%>yc0dGx>&|6%a)vq>TDA9#Dov~t~0QIKrsvoRsf_jos$}K`vjDYh64nfzK%)Fu6yi8sek!$nr-J)r`wXjL^utM9@t*}f(Y~!dBn0*yvCw<t*yeDEC9HE@d;0*l%USU;k^8xMxx4+@kAA`3r8{3+AMn&Rn5*)MHCkBK9P%>=IvHlFsy!MGHlhjSOu3K)g6=BTP9PZT%O>0+&{MV4VJE<@VBNqG4f!JP~eQYZ!8H;P?ngmu2~m$40gzK&Jx3m8FY+RlZ@Awv86sTRX{50JsQ+So`auqm60Ti#d%4|nvOu+30RQd7YDHs{pu=e>IO36l)MLOT{S8TTh$5s{>YYEpXYO;_}wN<nL1CEsfRe5(Vl#|Q}X_x03p&BXs)cyZehQK&nHxCAjbv}f{nXon$Ud>=b56VJ2NFH)+X6Gt$k~qC-4<isRJNXkphRzEE44fB5A|{7{!A!j?i`V%Yl7Uhj?L-%(2uo8DaQb^(kjN+<)*Hnnb-`#`{A=842D$L(kQ}p^3)7TYVfCwYleMQ4SCI^l_U)R`Tpfr8t{lO;!?<;nvICm;oqgk4Ba4F`4U)d>rnO^8@BN<eE3NtK16?){m`ydP_w`J)sd6Y@=^twhR8Kqxx1`(bl~K59)sw9<(VKTWFmv89*rhhBr_Z@2I~`vNLQ{%tE0Mt{p*{7<~H2pvPMh4Yk7-WlLxqCf#Xo+9rRXap`0r&tR(>M3)E{?<_V&40j~J6T(grB6UQWJ;XJy<t;^#e4Y2<s<40n2N!{3FYi#no{HjlmF(d{Dp-ib(!`eZBVcA*A}|Y97@)%32~8zZ!ws^h+LSQBA>K-+LTGt7$!&4&fufS$lT}ct1MgZzrONp;svp9x@Mm&L)qw!q7?QhXYm>#G*RCq<gwA8lPf(g{e((7YePgh*Y0uQkrAbPnuA5vh5yN%Qm9IsRC?foPgc1&@HQq=5hJYm&=X03bjw`M6rB1gPNCvCF*ix0Oo!dhx89W;L@&q@StcZ7%71&}aq8NzhqdTi8fd^EBxQ77EpVUl|j$lO`U16O|0_+E4LMtco?(zaRGc$p;S)C_93j*urn>*RNgZ7qcVYxQ|8PP_cW$`@N2)x+;5%-uh8*~PDTTOaN>9x#789k~sLmOyP7h<X@tws4^w<AN==1#SYRD*i`e}+^UFYIeF(ujRdN<qnvzI##}?&rclpY!Tf-0NvsQca6HVlMSz(dXh@M!ya-#Kp;tU~UWtohk*um|OK9kFa1KmgczL?ovz%th76!EESpuyU0Bx1EUY91H@9V^rfQbqPcV$zOIk;pMYY|!*0{ZkQtja#^%$h=8RHQpTX7fladXqp=v8S#%XB~MUpiZJj<Td6m*F}wn&hZV%KpQ%$)3EO&Jj>Z{>y-pDC{jJN6#49&@$1qO~2Ml{EMLIR-fSflETAUOoy&bBTtU$s!;Wiy*s<cgq@01iXS{z{)vdu!Bg`1S|_vYz{1LJM8Z_;_;eo#Nze-%5Q#M?OmfL>IGign`;N~V*-1^)@d@-PQk>|iY7ce%ZhW_f3S+ZZ;Gx%H_!yp=VW0z*Jw-7I|$6fDAvJ=ISq*}6nrOIjaj|khC%JpEX&8CUk*$@47s>dP@VT~J=uItV6v0ItlOg1SK5WzfKklNrd?O&W%`eZNUOfRorJ_UdLS)!h3pr%=?KArg~*hiPC2RbXFNx)ipEjhU>tM1mC}UiC*`weSqJ_gT_SAx1lpc7RjfNF>%SkQY?5nlurg%1k!9`VUd6#9kd*tJ@+^hoAbvciszte~f<}+YT!(mO{k_W98&J1D{GRA2%=1mnwM+atzXu4Kn}pWD*(uSV7>3^5flFHAJWp=(bQ&7w`^s8>VQ9u5(@@z2RM`+e3A<ZGdcfyNJF8T@X8*)d7NbCfJn{Pan%4%r@A<W-+d!JLIzdZYldgH*T-k|0>DEmM65a-mlYgv>VJ9?qG4E{x6g+}dk}}n^1wIO`<%=h@7$sy4%Ipm5vbdI7b!J}r2JZ2fGsCt?0+cDO&d@TUk-{?A(q&dJ;Y3`dL=Iil@w^<C(UoITTIjDx3=XI%O3%BhlV>r#Lzan!IpAvJTqVECX)emTCF1X45(33jw+YW8w<>?li@Mes;QKrZG<?V6CzyrHR9N$K;p!B8j+q||?!b9$6dR^}$82S}-DN0T2-M=63622RGyzUo6oP};twq^`wctz8&J*kl$Q%5eVxn()6ZOJWTa<l0uHouNHh)n?9&ZhW=%{N*^m`##A;m{>M_o~E?(8N!FM%sEry^7YsCU#lHtr}vl_Z+oO#FgseI7(P4Prg_(v)BbHtC&-OrObFW%o{Pl+^m>8y!B<+HU6Zsq)%rE<((eiV*xHzEfG69@N!BFqk4cmOk4Mk~oboQ|Q^!ij}Qpi@PtvK~TpVtC>;WN(e78v}Tnq10^ceDnn7(DGyX#AneTRZ@w;@ba|M@P*dB{z&oo-+Myv(_%qpjjwaa%ehJ1d`SQZgfU<qiQj)zJf;7f9CW;WjgKur~C)|4q*2m$~HaVu#RF1%85dk9!`M<fT%)TX2s(b1IMTLMZ^%`JzEcR(60$pG9{@Q|bPh|d&2O@ax+v=EH9VA+PvWZX5o_Ulp-!|W-Y>0;(Rg`POOAd|!?<#$)dcojX)O8OsL2e$hv7zi;+t~!qM=#fpP^)}X$!CwWb0U4hiptc;@nyjlkL;(8L|w%C)#YV#8r+gTd9!(9{6wemWr;#}bRSbbQb3>eB~I-8h_$VYI(2G6;YF&!gBLBtiezQmJcVnE!gO&yL4z;)#a3+87i)MplqyX<b?3GirJqq^4|+~$N}jYvaWlF;)V|uH$#zyp?tfEu$t}67($*m_5&HMKYM!y=9!6^;=OD2tuCEyq8{OG=yDf3DE2dy-)uyg>A$vNt=$$2={?hUIURzXu2gh2v-Y2{wFo`MYa|FxlFi^EdOU*RKtcG*`gI~==<>D-T6~TQ=b`w~N!go4&7Pb%t?RRjxp2MAd{SV)>AzBQ&LtId@7yw&KH)n*+shKnaT)g?f<0BIXEM-6R@^*)ZupQU)5|@xS308fzZ$KsskknxpY4o_3Z0R;%XIg}}OcmP~VmDbGj9+(}&T}uzxc&i=oYH-i8uE3NRj&;qP@KPEZ-&0}pBi&;GaB41riPKUKbt;BDylb**R=yi0+FP(KYA6+gP+guq^2$&8A<&<#4KWeus7<zIdur_E}$UACG2JQH}>>=v00%kNI8_iF$>L;g)8$pY~yl&#5=<5e_G>5E!55DQZI?C=KR4LOKB?0xuuD4#`ztG^_D)_s$8G|FM9*ir#Ro1{*B31srm`9*~{K%bYd4|vdp18Jhg>~Ba{@h;a&P&3iz+;imf+H6II%0!P%Q{==>(bajpC}*(mxUyCd00^U&XRO%+K^TuB-C$RQ!m!4@KoV3t8vxyOk-d4h0^lyx9<?yO2-($$e#hOw1qE_ANUUaM)xDVoRhzM{wFEo87|nBCkH2ORwNoSACK<sE1l6)jqZr9u4*_-|B`n@f+I0Ap%atFH<3VQ^Ya5%tnLzCVvG-zdAan<0N(Au8k6g)W889FYtVsYRxlK?iJV+@C;6Aqr<p2Jmzg+9)vzC8=w_6bf;`?KBm-0GO7!Vsf;GWgJ{P&vguurVcR^3+It@dz#T`%cfFqgC#7$C=Hkgn9tNG+{e_-DCEZGZY%PBg`~$cX1`&tsS?c#bqFHk+sV=-1Lostet<2AT^`l-rS^gC{G1k@Nn@afNy|S?HLF*_=VeS}4Lm2x1pUnHz{yGwPhz)ah*-l}6%kYEKM(wSZBn^NAv$$|<#r2K)QE+T?PDORM(0r2bSbJ6^^21&O|4*&;xyRY28MS*`sNi->xbwJp}eQ`Y<K*bWQsw`=Ft<acJ8RnP<{4PC1y2^siA`!zMo~PhaEg#qWH$+nj7~r+mL?enV{JA<G+7TvEY(hI@RQ2DP;Q)PF@KSQqf9BTb7ZyYo~aUBnA&q``UH1D{8FL+SWXKnbgHz05B#_6TD?`r-tB98A0)aC~Tly_}dja`|~$G|C!*}v&kbzWVCz%)4`C{wlo6t*^d22FQ7=w;PaD{(L(#&@1KjZN;cc$Bi|6fZf<M2BxCeo>(gm?rSyLJXWw991B8`jNrNr)etIicCHk%_c39Oto9IHMP|0U#-JwPK@%Az0u|-@Sc9b}#{9_-VKMYP*p+-jFNn=vqN@D9V%ehH;^4XfGz60tP&kw_|vOy7KF?9Z4>wV1C2hp8=A8o3T&!pg3j&!@<5~P-482RzP7UVg;v0a%Le~A+6_;rf$fGgI%%ePRg2h9jdPYZs&;QC;q+yY3pRBZE0<;7ZX=#F8i>MW(s#;8CLC?s;epW~gWQ%x!LVu8+mGoLH6wX2GJHCDTZ&d2c)yn9bWH#m&($@TKff6Vre@9X<NzpI}_!;|YT-_9oY)0|Y$9VD|rJJ{A%ItRFmeNh`WAT8JbXC<flxzpUx7fV_s`BO2EwG<I)>QmhuWjX5~apSMg3+9)<|K)GL{4m__kC)Hjd*`@K`gw3W1^)T1!4XvZL&ZBa^a$p33`jb0|M9QC{PoxW`QsOU|5u>M4o{By&yZs~AfuVwgR45GLdm8`&(^GM>}M&_bd2D9Y!s(>zEv+$@s68o?`PFOkICc^80y8tNH73S>slteUQp@v5<x|tjXFlM=m&@<Ok{XrJ!9BD{q=kO^;`YY?FJ5*+qdX6vW2!ceCIWL{GMu5m{DcdHz^Jzp6C33|JTRIKfV@Y?Q&PY52$4UI4!8vuf0pRFp3CsJq-IoT#?9^Gl!#2Wk_wSzCfvLWpUMtu#N%D5=bz_sZBfoHKBv9zBD5MeTmk1j=Y_3^jKSGS6Nuqf`0Bvt;6C3)9A!o7f6aHWCgU2z+rkN@}NJ7fB`x3QJ!0?^7v4?>{$-*TySYKNrnYne!tUSv=8dj;+~XSsci#_4f@q@u*;jUg|x52ONlhV`cje5)HSQO7nRrXDNwASrf|8pzF`sBvklhH&kOb$y+J;vEa(3C{n4(4sMY<SkCKTV*zr;3K~61BEYtVqyCBiH18v?-K{|ENTbod5WAW|*k9+YKPU!%H--UE6fX|U9tAfsYsYpm($4+Is3oOyr5MY8xhzE5sXo)VZZEs%{mg=G)YW$E2B|J;Br%qbgicMsc$9VcTs9iJuMfk%*1{<yybZ!Y@ccYT4#E8eh0GKw7m*QmyxR}ReYe+zbJqs(@rE~oH4BhajViON0tB(t@Fs~~5wdWs%SVywrql6jGSg8<(Q!y+s8)`}DHi&o^BYHCS72uT)u<=A?7+~d(!ENr~s5Z#+Fuc0OpIZvHwZg>~y_8Rb^i^Mwh%KIG5yVCuUv@*+xwv!S8d1(3{ZAC}Rck(U>bgmYXV*02+PkLIci(o0&elj}fn$wSNe?ww<Tn($W-%rlhUk>s=_{bJ?Wfjyy3y&1QcWLeHqSAlS%EaXEP)ZrzHAjZPYs5us+jx$4iv~hmc?_lwXGgw@})?5J#E}OtIQK!UFXdDZTX<y*WRY_k7<j$y~8=KK`2F!pb33F8p&l+3NWdl&#xgq&%<7I&@|JAFMZ#utoax@Y_}+b!#RV&Zj}q=YiuL}{0-o59D^F~1o}1V5QfzmRyrbN9m7?LZ}$8C3WC3d=Hfs5*<NOXVmO@FAW9$lC84qVz9vyaFViA0OfTP@5)}3n)w41@k)(F$NQ2g_s$E{%L!8E%8TuN(GYhRMFm9GE2Ejkgc<3DWFm!Iuc3(6$-Q3B_(-tc^^lka)$d@NUNqXSqmK}x$*}}M5)T-dgtm-I+M^$u?lz-{DNA<_RG$-3MnQp$X`RX*K7^Do-ZG8`lak17E#{d^!02^916QB)zz!xg)CM60v<``uEhhc3I&V(X;wY5ZnikYey2D_;-j}M!oBHf`!BE02vbmL=jE3kG$B$^_0;Lnj2LPy~K)SZ*-9Y+m4Pf<P()3LV;FllZR2prWb7A0ecLa+#K9JUhjUZ;zeqbm=E0uk9rVR$Jv76O>SY9={L!E7em0PKB~G}_oKWKSYSL-mLcQKSV%v-m2fHEJNG>2-+ByMi5qT>U|Y<_QwOwEvnj&LU?19ITJdkt9Bv#(ZZ<uU~WwRbDq=X$wD(o(kTl?tiQNDhlJL-ldF_7oOfAI^6J>hCGcuH>ex%0=#<9lXn{L5b)hsjA$Ogz|&;+8M!kw)Hu*oBRIx6XIcbs`XKjO4UOg!!vVux64lO1<tzFuPHu-yTfrz-H(#fO<C!}RRL$wV2*$bP$4TYuSUoZmM@V?v({5jQU^FTRDWz(kT%C`<e*gPH)+rtYX5*Zn|C~ipcv^oeyuiV4Q(Zpv2k5=8UqBGDRlIt9-7uXK?2T>%)j+sB9Qq3anyDPUF&)C5>J^eP4>n+rKwbW@iF3f}q>U*rH)fpY5=ve_2eD+(S}#Vmt~VD0hlKOg($Xpvpt^jlF3LsQM%HB&Yi%~J9_CDEo6n*C=lAdbz|<(b_ep14REj4`upq}iIF*+?i4-MD!y;SMqPI3t$u}Kl10}7^gpHZ|c=ql};z098c(Z>VzTmz9g(9GqzW}CW18y<F4AC~2s?Dve?)#UTw%Ei}(<^Zq(z^b5R*Oxq1o;MFd`RdVG?Ye|-gU9;2`Ks{Ag>Vi0Ndwy;p<FWL>gPh8_kVVFOtQ%LAghDXKv@3Px&^*7l#ZbUdNjaeP5&HfD}I{2Wat2vyh|h;3n@ts8pHUr;N-or6rM8P-UP|U7Uv(A=YZ`Fh(h*#g552paB%oUwun&ej@F7HM(Q`o6RVw5B)kgpbf)r4fwekcDp795ndDnS7cI(ziVlQtTk>IU28o^8ID9UI8ma2LV`NDWZOns<l5h<BEPkxVgNK{qU&JKz~1A^f+-<|*ZHg2jJ~A-*f_Uwq|p)uN%5qD2pdk>N7)mE0Z=C)`SqUGz%lCCZ;7O?)Bq=o!e*z;+C>7^#U^KRp<OV#y3d*0Bg`KC+SHfI2u>a!*<^oAYy-x#`Krd%p_PbBShYLvTw`MZ#{S-Yg#mD;G1{aZ88aOOW?+T13HO{OmzL_?(fbEksKbEV{6dj>m=x#&BU76@)=Y8({cW&o=&~hA>hfso{!XSc`rVx*`Oa!V0rPmwc6>$@w4xfl%iU>>f+52;H`qKFH@nf)o-ZC0SlmQ|61KQrS(XdLg`@R*m3U1{nm+DuN=}~Aw*9+FLff8HZJrhJL#T5EAFP~9UH@?Ae|MRtuPM?7Lxe|9ZG9!e<6tZ*4R5uF{*=FepOK9H*kU9%xmkHk@)+zS23tEa!0G0oMndy*?2RmD?a%|yn(E_)+!rvQrIGP&mW7+mOuex-DKz?!0e$jPmTc@dx46kw^dJHoI@}-o-7RpU)j6UCYN$tN`aa`e#4DzZEO+*U26|rMls%iifobl84a`%%fhFU9X=71M$SzX`;?s_Mp*vk0^f21UzNpdwnF_Cx%j`dw>ijnjQ**6pVFJo!v5RSiOGE5`&WF2pTrT7)VtR=^dZpQd?q6$j(iZbl=3y+#6Kkz-@U(eD17`2Cyk{&b5~YH;I=^e$?j!CJMfm`971fPMnklpvO_q@=Th*fc&@;aergs#To;ihwc#9NOhr|+@oE^KJYc#`Hx#1o5NH+yj_^5Y|)e!y|`)F&TBnr@D6<cEm-D<Nsj=snXJG(6@7`EWYXyyimoFozyVnbj!3y$qyWA^EP6ZIKK8CJo@?jfgW&gy5*84;A7wW+c?9Uik*68b<LmENtC$0N#o8vXOJ39myK2K1M4(aLpQ#^OJ#wr-7Q$kf@uO)9LTZIddR_}3GVUEb+r6k`S8+O%5-eFh<~r9O<NQqt^LEbq3AOJG3zIta+rsq0u&?)<J}<fDT3$+Eo+3&ePds;q>HY|&ixn8jr4H9@@1eK5L*2C$9UvJG@_7@cMWs1->XW1n=AnlueMA`By-;u(R;@i-;mONy>Ocw623wn|po#yA1!laWuT<AV>QC(SX)J!QG7L0nqJC>+?_HQFh3z$nNL%trbhA*W>2Rh6V$1yeImgxMkB3D$YYBk?ri^II?Gg6X1iQCVstsR6^kn9ERoGg#EA(RgDy({Dm>IE=l)=u`;=J}XJv6~9^wz>@aHT3k1mNa0dzCOu56ThBo&=G7MOVhvPiRa}f$f(I{!Xw-e!AS+An|A3J)&b!S>0Y3??wpkjt9$i^cm*pIMwP=4MG_mw<fLkdDab5{8!0^<$)>NI>72i3gH~1bQpwU#~PjMVR=iY2xo@<P@jJG<~fu~g$Enc<-?I|B9=8VhKFiIeL0eD4339|O+z{qBKIehsGVswh^B;ANG^#I1bWVC%=PW{)}Bs?6JMzYp<wY^*59f)pDwpxytWIi28!5}ND_TVFk*4rxRsEwTHZW6tnVEDUVB=K;_DLJc$mF!W3Q`^(pHKZAfr}5z$3)J9nI622y`$V;X*X5-)eTi7PkoX1gKaFJ_G>G=Pw!i-6xA-h}44kmcT)%%EZNfL&gs;;fEa`TuCyYmef$szZFG}Wwp|vQw8U2eb_-LIq>j~~v@FT!Ic)s}cpWpvMwXXZglmMC8x-Wjw2HM}o#t>5W;n5@YPN}~RdU-XvHZgn#2E8SXqs5YW7RXT(KL)$|J$F80l{{1KEVd)}+TZ*hMqUwEz3FNYog}yIarcmz_*z-G1@pj^HsrymMi~q{Z>;zlx4}O=I2%!GItfY&<+HFevUmz~x?>AM<4~C}=BR6n>OH-2vS^IW3~$3`3XrBKUSr6S)HpT8X*rUS?D5oh%|Oo6a28v2@+)I6%Ap9+hD*+Ueo?H#XvOebCRr)7%Q!S<OhLnc*lsmx(!#sy#04mev95bU#?bVz60MQiR(kK;o~wy)Ri#+#z#F)Op`W(*iFIanTOUoe{e~{zhYG*<#05(lghL<3_ZS`#sU8e?^y^!=ujLa2cmiH#-|m)Y=oasOg9vQ?5sv%fzQTahO5`1rnDd=qA(5OGGMHtu>@gKQSmv%3E#Q&cJ%!E(NvuX!Lya!`b!nxwyB_$i<l`*44JxCa;hdz-woOzs$RP;1dN8Zky#u#QIRTQ!I%~?uqNcnqd3cZ!dBtzELPwJ`rlQ@vs()aVoC1T|!Xtqoqy##kdBbl6Go8BLMh6&X%cPVVd+Vhm?rSn<IVU*0ZNrGoivT9o&nhFYR3xjqu8Uav*Z;a`F?Ht+JawbkfV@DV*6MxznL)r>w3e?$TkhS9Go`jZ0m;t9h~l`_^4nAj$Hmfq!qWJqKcsFPsjw-<;;53+EwXys3M^s;eBuy3A8ZB^X#SO`mAk(XtGf_!@9>u-S4!6U-}UU9s)HC5N0BJM#dnNRF2RJiDm)9AW^o(1sVJ`XiGsD|lB!xeMj&!q!V>=Y=6`;#-~Rpk-+uZ1yEcw*mA3iy-5(F4{N!hz@%rX7PNrshEPj7Sjf*lcpJ`O}_?{m$`v=C;J?3;%rRn83`3bQ6G~Ux`5@5SPa^eHRrgsc?QTeH;Lk9jdQ~w~F+-(k|xQA0wn_N4#1oQg>Fd*&GP<f^T*<i5Cdu!}TtG28plj3wtqtUnq1JZsY4Z7r(iV_(2*1`}L`3zEuS6^{706Ye{=VdEUI>;{%yMj9cr;PPNr=rT3h*{vpC6@ajLN!E&1&p!(S=+9`o|TQY5cxQjb((y!{D<nQDXLYkW`#mus|bzGW_0%oy>09oIls73*V;@)xw54~#QLl{qcXrNd+q1<iWX7fL&l<pFdZrWWx>IEPA=2pJR_OFH5DbyF1oHBgJ0cU0nd6y&!>lO7N@2;#39ZhPDR}`**QENMdbk0F-=d0=*jHwy?q$BfvJb{S%xRp+}UNJ^%dR-iG{aFNUnAdu%Zmx3TWh==xNo(GG<w}<Wy8=lb|OieAsuLf&BxDVNkFFAeHHy)R@~Rplmc8AlUSEOiD2l??$PA`Er_V=TxWLlEF?-Luz~V3nI`{<PpnK@fwTbwYCapvH;-v#V0(KQi3`Yhx77(8i^`P#uHV%E*!;BYqRWCR5d$G6;W8g`$R5knzvhJ!La(3$*@)9VijC|RCi2fZ<$Pua(RO1;9Ly@>!oWb{H>`@j69el6gXq<8%u%{lqDvtYu1GwgB|jmv&8UX1|6f-B;)mEY^je-6_AR0j|O#-=isMYWhBXBab8lgrXvt{0v6==#X)RDzq*Q=x`B*1CGUY+SB=WTR&~O@KeDCP=lPr{ezyrzrp{Ak>LJd?+`93c$c>Ws2L%X`zCd$jZFUR$C44@iS_3&YfDmllHPeLdYdFsoE!~+ZL9sT;&S~vi>pX$4ph_J8p^6kZWM+{lFAzy14!|fLlyQWvqhAi}n>xe`gJh1SrpXAy=c-RR+u{C$&(I|5^)lWcBFaec{uz3%{tZnu{@v>1xTwuNPm6MRz^9Mf6ta?MM=HhH1Z%RAm<+dG=Ee*_L3=c+Y>&xYZ{*`}hnycU&mq^msa@q>aIk)C?bBN-D(VT1uwWZ~6SH0LM;+C-+KRUB9e7axv+$rz!Pr9UY{>vZ@i)AIs(45JZIYc~qhb~cg>dZ%%EaK)KL$PCl4z(MwkTUd+c4=)d($@g1C2{319=8p)gZb=z<6h|DPp)I0iF<ciV&$I%IqPoc`a`#isb9O4_Ac+1UR?|9D8|(3iebK$E#!y7gE7OB$g(&q#pq@+Y*6Uu)+Wp=1yoTks5B0J=La!0S@t2G8ID0!%1$7a}N}i^q#DOLLGS5Dk@dZpHck~c7;EaQ>qRG;Kq>LEnAx`2EBGwX(x0ZYkq>#Wb=E^f9M;7olSeDRxV9a5_R3=dWjgWd#-#ff<zJF=OdJGK&|mU@;3x5u{fW@+;&`PoiBB|#XvGx{l%85WbND@O3C2S(3dB;!DL0eqpZLdOA*CDJRjXzMF~8h8pJ&WX#S*TigW}k;^+$NToPbE7!z7Kk$0CDxS5#=tj+2?0a_4PH{aaJ-W{~JR13?!0mz6p`Yem*!A9W4{*SoFq}iY|xZ7&dOG>Y0F3RXptr^-tle!R7O=&I454#;1vNm_BWuzL^>;E&P%6MU4laWU3b5aUQcJ$qo;&49~2Kt;=ui{=$%aUqZ+!1rB4~sq*-!l4jm?17sZUl2<IOtR<0LI*^|9FH2^RP6>^>&wHN?@hk31z9!JlI9<AsHBbKph~KdZjNFJr~WT)9`hDtp5ZQdmeV1K8DQLq%k(1PBmwgqWTQ3j-QllSPfNM(J@X-gD8@$vEW(utfrt#46;RnoD{o`%V6eY7i-FhNO>zawD?SURoJojnDv;e%@wWf0Ij6C@6R#7$q!r-D)sVFFq%s=)Jzrup;!djWxQL~Xd>Vh90OL)5rZ8>nkHabm|}Baaob^kzY&kuY$F!0_g8-N>uT>BHBm3{+TL6{fFBds6Shv1p>_%;mR2<3*;!Vc)Bb~1?0r*o9lC)gh(0F^)44`lg5E)39!9YaPRwaYbfMro(Q3@<^)?J@mu6W$4*haq@?pruor3DTck9XKa{`l{1ZLe9t-jJO)CP=VZZ_?@GB4AAL_}Kk?d>EazR?3|u`6W1xJ^e04lG2b^mNKeoj>C_a#b{r>IUPO+pUx)Og|}~J<B@q2k8=F%O}wGq^V-vIa&YxAZ3$WdxMoB%Z)5+C-*829)YCX=agqD6bJF+F;y+fRTVUPOy)YoGwbhFzTSYk{o(gSM`50CYOY=4&-pz-(A*@n2F^~2{=_i!<_=ua66bkxo2S#zFyB|!`U^ud{+Nc!CZNiO_(|B^D$)Z!Puf|f;x+pxj<Og9BIJqJ*Vnu@;C;`pJ>3S<oYe_h+M0CD^XAG<1WLDVLXhw_aGd;OT?{*+xr=#k6QJM`q>_}Wo-OcEXf0nnp~Wa6YfxrqSeM1M)T%S{(l>CAznmGiO%k9?X?2E{35^t%!ImzwdI=}uA|-O@qK@a~u#B!8lhQ(eMPhJ3O;LK@Rh>MG=^e66EX)B{8|NzdRZeqJ)-4f#50elmp1MtV7P(dVYhKi~&H&%%QJ~>F7C*r(T&BXBp9@!~;B(CUSa1i<W24wG?K@^G%k3^h;X<Gm-%M}>z@`as%Ayb)#BMFh9;^jlf_9!@UqIgA=M)ot)0?OlrrM(H>v0WNH?sMQD)M-1C`3nHL!#dc!3rrpk~`{(YIA2d;du#MkvSEiB0#;P*0FI%392N~>}KK@RO|B~%4rbmxtFE{L$FEjOl0~@&MLciYNMpqH{a;+k=AxImrs?~MspEju2h8JC-I%i()6IN7J|VP*|GH5hLFT*e3?SemR786EnD1u5e|Yn-dN3y@>W84iJ>*CbQvg7sa6?^%1(Kp>H=YBUVrm-*`&+EG=`emjt1UYRniU(fx@53=5sX3M(|58cFC6)eg>57gO-x)-4LWPwlPtJ2p)WEn?K>+Q?Nb`pSH;{ou+aGCW{CdNyz`rO=b2iiBjED4=5@GY^m1(yJN9WBN6EOqW9MpoO>eke>@PubKh3S<mw>N>XS`;a`w!ljQO_tHf2LR<fx)t6JBy~40u=RW7P`=&!Vn-kO^}0kc|yx@7m5Lcs_c$euP@(n@T==q@5G#6IN8FMvgBFws>SebtLK{)~_xvo73Qy^vRpe6XPd3jW0_Sx}*D;@{t1itS@n5=SQq<UDT;l3kok%4IaE`Ayy<S+vX`;TNI{?^9dS!(J!`QqrO<f!=Y4Z>Zv=o#VGxZ5_`~dLR0djHHw?j^`Z9F7EQLZI&%M;vP*8sU6r;Dd5O@!*H!b3CHF8|8#xDwMR9%2kl5(XzT0hylU*?dQ>!+0tqa-HsYUNB@${FD$M@Qz`a3w*()B*!6@f`iNuMKFUWb9IHCk$>F=jQK^B??bCMp+a>8l9tTe6$LQWU<^!LzW1C}_Wf)Abzg<m-R<o(<7r&>iA}lEnbnTDmzSY);Lj5#Zv@2Ob}pIAAIJp_jKiJcRAIo|m|Uyh*U?t9=79S%9PtyGWzQwPZ`T`8v}gyk)A`z7V^~>R|l3({!GDS;qAbh~$*+qtuYEqpW&u5P{<S4SO^6o&VIBgPYOdW-&F4r2X0SIZ{!*alEb_FcOF)t^LufU>^K@ekV0`@yJN(_aSBx`-8nv|IMjGXm<exDK23zyT7rg=Znn>WkJfJ1ddr~o-ACM&tV&v`y<{FX8+R~KWd?FK9_n)Ts7wp)>ukYS<Wp@gfq_XIIOqy$yVh81$fyTm_Eh%w)AgIu1eKUfX!a^KBE)6Ad_Vd<>9F<JRG5<pbhWR?^3{jRab1iVVbDYJ`2v?d_(6q8IEh^zsW|?57`~bKAMOAwri?LYT`=DxJM2Nc@DM^X#}$jvdTS9<jE6+W2CGDp>t<d3X`sm)G~~%G;^VIW%gQ4J5JF&ruP*+E^i@&EyL{Qo;cv(x97}MLoV+?%cyA4GAs@1U%-E(n%rD^+yod?vs!&km=A-~YKo|r-tql;Z23mnt=$ay;|ft3w=Q%kbmoX;fJiMe%?vtVQ{(;wN(xapTQY#BqtHf)NhnEO`=wBb18%3O&;`J>%oUTPH7w)c+Ig;Hh%|MGnOHcFoZHikMq4(OdK)ZZ0Y+)SJivUWM&UlDZbl(DHg{W*_bVhlrZM{sdrg&SUZ_J58Q)HpCK)gvPxAw8LG1FVt}nF@Z0F~+=u8>|HB4ImX{uSh3O+AmB5U9|Q6}hTW(Q7If_M_UEknc_&Z>x*O8<G_-)ob~MGDcW3oN%=xS~cZd~6>BNi{l$!lp}6ov2@&Y-wr*ixj89<~A_A3(_~QfLcF9X9(pzrDwb2&m>a}QZ|pCXti@kZHDTzrz$b4X-o|r)bRZ*Q$6h9@e;*19@pHsm)VB&JI@5gwjclfdx`~@+|sEg7fT`Ahj8*rh>(g_I@+>~#9ceZlO!>CfZErtqg_#BmDaZA*~_FZ_5y%0ahl*QgF7_@f654o7erwL<-*^t(Al5A@%hgL$DU0dIU=Lw3z!authS{QpwD*fH+lg@Vg{d|oQxLQ=YIcOlvT3X9v}IJ0Csa*%Ox432V0*`!z-ot%Rl=D3mYJ;EK3?}q4(2Uxhm0jU9rQe?%6~aB85smL+cJL%8$2?DUU7U^01@CG36io`21mTvI;da0#6!~`c@KKk6F%5%9GF5MD-m|zj%Haew7W1Ad8{%|61>3u0DwF^!sR2g?uIj$8x0G{gxoL48zEe|Fs~`@r~`uy!cC$P{*%Rj0aq?_FcY(T0Lk+P<mSM^99!j6Xg~_vZZ31Un(!wf<t!<Lse%fbv8x?f<PgW^Zgv}Or2^<sTT`$?wk2sk*!@-<g2mTHFQ3XkKo;V8oI$@j8CqYU;bmZe|%p*{P|sd5ohuWjoZoOev++HnZI1eIXI(y{g}6rE~8vDo1pyVQH&ILY4I?RVXO)?t;-hbAC{j1KWuak2MsD}Ieeg`CVzWx)5Zlqkq{3l|E3;SAr)TkXeb)4e~zLsY*5w4W@q5_dM|5^{|N4XeR=`E{QWO~`{l<?`ClI&|9JTnb`OqAzn}X&E0**miaz5r`^9hrZSl`Z<1Ge!X`-$7hJgpQ;nyP4zK|rZj!(2@zmlTm#C6R=_#nZSk<GMJ2B8jQz*FFq61b)%3U?`kJQwzQRsF}m{_@vf|L2bZ{r<1GrCj+T^o}E=p%tI{dBN;cV!?I%`1RQ9aR!GN;lSK5^6^}Br8-{W@-L4rWXr>OoaZf^dG*!lnj*%8zDjTOQm)(=b*Lx9B9$=l1`eTPsHzht32I5`X4w1EHRQYM>a4<Ctfo`0s`=|9=R&&uqAHVXuMIp}59E*Zj`~Hafq_glJBc4r7zln_345s=PVhjZ=Zs3}`8Q;qwz#90=?)?;s94T}p8dTOw|duXJn+kl+hC_|)-4}Y?dRWnxG~YOU;G4D&{Cpa#q2}eOh=D|2?L7~nuGeqz7))yS(-hC5zR7|Ik)55<+}JZWcHFDkAmT~cS)a4w`2$ggg-sFJycj3cg?4e0-Jr2Dzn?0sD8*b5NYZ#fFVw8AjPZqik#9kEs?_vCjMo{`0MPpH&B8UAld}LaZ7x0j1<R4gfWTMkunT}zqv8^F+R3fWO2-RZKzSHqd*laB{`t*+4#MPqfJ6&F!C~pMx6E>`mXSd5a$%5<z8!j{*=1OOrh>8l|Z&1rv!yT+1C3Hv-Z~NhZU@Y#YAd-su@jWFbTJ}t0K9gU0tXjvr^92wx`9WrfrK^=cr>4Q^WdDML8LxCEJKSmrI2?V71C_vBj8JuatOqE-kyW4iG3)rA`bUKfa1ACRv2IY6d}*C^bnQ&h{21JX#hLuF2lMCeIg;hZCo1KYzJU)y>UXwyLO+DmkA19i20PIIR3(Aw}1kXg<Du%qMJN@$qyki8Ew|JlV<Jq%<F4(tzhOLs$7J?T7*`aJbWY*y>BohJ~+9f`hDq4*A2p<}v?;7Tiyw(*5g}1rQo@c|!Em0OQYONx?n?{wT<XTu1(CvYwZgXp+(Io14d>KXiXMY6<tY)JyGUd84;pnUM3384O+5SdUs^5nppLMK6f!Ydr!P)(%~tw{TvM`fyt`1eQH?gKOCh;f<6fvExK;_d_?{O*ulJlt7$jtV<%1q05zC1Js5p+Vb%2Bb_sSuC<Mu)sj{(d-5ZbMs*u!!%e5EtgYsj5z<UkTbWf|8w%teR;?GWTMay^p%6w@)(M=t?1)uPI~=K$H>HAJEXhInY%)+A`c56LlE~*ALA<>E>b{xr?NIQknRbhVwY_02hpcP>&chla*}9LX!)Lz!@-d0gR^p{ji^>gA`iC+0D@|r7L_*QpPC2$ijY8DnIMhZ=F8p-PAXk^`m3J~=$DzI-L*pUa7@`XG=3NwN>wQf%hkngvoeM0&?68@thKVTvBxD|XgB{LvyoqN3BBnCbPPhoYq>_^$G?ICaij$+uc3`~mDR;TqQt0(iEx@HvK?xUjP-!2TnWjh<h@kUrB+h$z7+h}_-NCeLca?K_S---8zqj0@OT}Q_rx}H>sMr8jJhgE$5@NN&8BzgFyn6Fp7P{-OY2OnptO~Yhn>K2mVZu4Hcx#>o<k_Bye;vcv?wX&Jd{hcd)%-H6xZfnZg7pJU)`+lt-0f}{J3GmYmJ|G#Bf}S_cEd#+dtZEu2$s^DN7FEe(dNaWwu%W<E#i%UAvF@_s2pd&PR*=TBT0^N8lz^iIJ#$6Kj$mF>A~iywlUsu5kroW#C8dFIMYa7ajZzgBzQgdsUjd4jPF(@LO<Mjj@B;v29Y<K$&AVKHOIo08kx_L?(Rri18!qa7gB<6OXD}h(^H==MRH#7`vDl2h?yz1c01=X*y=z`+L;RQXJ7-LtXf^yr@0n7e5|ioIxHl$?S?a1NFMN3ILXwl>czymB^tiab8+SEWlGHRTgz`N0>y-mu`Zb=#L5lF|Bpvx>YMYGUTyDK`A(dmLt}VH*nB8d8=kD2kH3EZd&%Wtyn7+MMT*|teluS~QmZc+*KB~yHI(sSy?oWf;&c0)!Q9z1K);9v%rwy8XrWX|*`S9_hETBPprY)2g0s=84-NkDVJN=gl_IwTf9hfhjtR;3I)EJZ_^_Ta_)GK$tl-K6N}cC=OgGQ0j5`2TGht<Nh`_GOs!CYG+M$!3VkFh|GEWnwOB2VB-l+OSosB+#%^jdQZtnIhI0m{9V(OoU8<h+xDUENmd+XO9>YlW1q}At>ScMPA3jWzV>%U9*b~VX2^6LuK3fRUpu0#QnzlJ6WU>*q!DN1O}DmO@R&Dv`tgwXmLqN8Wn(1}_sO3|P7--JFK;ZY*`T$IjORDA*4aiW7!?QaGT|LdWg$VOztg#re|s!EjI+Jo%>YH+BQJdMn@kj=2_NjS0bbCdn&_wOO~H@cx*xz%Ij8KFVsrl1^eq_RSl=p#b)*n&bWe$5#IU>thKJ1{k=^X3Vs4a?G4XyedVX;p=jRB97!3Nud2>fRBoVKUHP#Jo*|oD8<r=5kz+7$Y7COAu*~Fp<(*cE9*2rHqhpc#u!dkuuxb&Ut)Jc1<+Yr6f=$<Cc&=YES_?pWE8ssa;dbZ60fYWqgiN4mQo1=JROBa}Km>Q{n3@*{{vp;=@&Wl!uk432{tlveDE`;W(@5;l&);6Kk!?B`<ECcQ<5vlD8Z}$8Z;0;f-=;>^scLhiBG%ZDY>3>Tw|4=UM2m*B@B?&9xPg08>{OfIey3yq$xy%GNHl+cBvG0uRK$+Qai^Q%Ya8`4fT_ATBdTNOfI+@%65Ww03VbN67RCRrjYsE2!|6fD#O?^<Ux&%J9$x;~s5UL~sBQDv}_w<k|&3b?%NqPp-*;;~QWC$f@!9YBJ;Z5^SH*{5g@?K1*tR1b}PGOMsA=)O{ZcF_#)~QEGCP#0;n`;vFaL${4BrB8QkO<N4}(;SZ6jSpJC>*u^{B&tevBimt0VqL@&RM_O^)@2tn@cU41qtyWm7ErD9mF%^7xraSF+&&YUJrIT2?<$@NB32H)|Tc*v?j=>IXWxjP*+U8`|0sqUK%ctqAx9me!BS4fteI3JSljn}%Ol?KK(rsW#$jta=VV<=3f}#iUz`!t;pKN$$%p4DJZRr{V)<-u8qb!GGG+SfMg^IQa7oCMO&X9Mz76^Eg3^pT(Lp6-C>+%&2KAuF?;$y=8*!68i4m32VAJfyNX=sBxc0(gxXBO62aWmuVU;4t2-Ix~oK;h&E?J-GvYaZj6@&+dl|6l*|TOuc$RIweq`L;F2ovg_K9pGs!1Y8=9J{0&;K%C})*gCFuQ5PCX9oRbIIdk@|fY;b<w@fpRTTO}BV-$OvwSjD;iU3LLCEG_H`|hp*Cc<FvQY++HSObR^l?q3ZW$cH>*cWY}8B-tj_r}6wKPFWx=0r>CM5pVSr&z<`Pw7582&ju+gn_Z!T4e0!7PlGr37&T-%Sp#VU&XK6WG5iaXsbv#9_nhh9fTLzJxYLvn8!jZg$WqaOh3=7#au-&qCFq{g9{gnE7mT8WU!2dKnk{hKc8LpheOfX>)@p^2UN##=$rT)_U~G5p<#l<;CGQ_sXCTg3~S!OaK^mgFpeic&4XWZ?<`zn{W>SMqCE45Td!>dQ$w5Dq?de6h-5hB<Cl))qm)9SS|eeYE=`scWFG@tUAA?L<O9PD*(x4mODd!I@Ju}jUsu3bQ^mjM6svm>X2Lj+YK?L1T;n8p9-_?tjWpq_S8wcHi$q(+LNFQmhc4SCT|JJ&JM0t6NRdqk98ig0kK<@JvoULQ<x$mgIaPWg=lMBK_V{5E2WamR?F(IKKNcD*2ec}x)LS#pEgh-8QEX}qbS5JePnECUe^S1B9M_f@9TlWFEiwijtb{5V$9Okaxr0l%!@A}N&m74Trg3Z(>jJr15TPMo8ypPA?wV|F8%%-&;^#-$<?dxpZjC?MQB&V2#fNQBgi<Xaqm_!9N=eD%`}J*+5Sd|+6d00JTQRbkFFE`<Fj^)sQ`-s!+Ar=^p~=Ef36eslX%;M?9&#s+am~)7ZX_W$+pUBu!9*kzoRUF#jt?biWRI9}THE4l!fYU(EgxeTr%c;h4b$ooNXN7P1cQ`C;fjD0Dfk!*Ja-L-Nr|~s%bi3#VT@g9n2<U^8f`)Bl;Qx9i!u+kQTpQ11UcnNSR<X<cgHzDk2lOWBV*8l4;Yx>JT<7A(fSPNoH6lDy3Xe^&o;9iEd=vcojqmbW9P+9%#m(00w5-Q1~8!2E|p3EQZ_^!NpXvK_SM-^?;P{o8aYb*0`*#T7Ni336m~mJZ-NII<x9$)4ZwnP%N3Fw<s~88$n-x89VjI^5R5S=Qu>1C4vE%=9_1i4@(T`IINug6O}HwfaE6)goyGVZm(flSQ}G$|fx!Vg!}Oywh}bYGrHDm7i8IHv76d~qcY-=U2_n51Y&O?r7_yT;X(dY{;CsdTzt$qxv%#8(S@CwAh^@i_3<&r%9FZ5B#m{Cgn`LBil8tQ|G+wEZ4)*olh#EcY(oL*7Qq~`xWZl@sst3Pzwu1W?PLQ&0i;JOF$ZQ>bx@QS#4MxxL8eLMi8Laq_GHE6m%bFxO9j$G4-P#I_zAoyk)hIg`>bW}i3f6tHbLCnd*^WrehAsprU#)u<^|z(6X<WV9=O!e2GOVXHEw_S1q6xy=J|+_Hr<1d;jd333f_Q}t54UORxNcb!xgUJP9s2s_R}GMHChiS@kjFJ<nG0EJ`#CzPe*rN`;8VD5IO2^gi>J0eozDaZQ!IoWWhX4&z@>n8+=jL~d!PCYuM_kT&~6Peu5EN%h%nSdm5?;I7(uLlaJ4_5!gLF9`C0M-<7T%O$|@%d=p_I#$P#ZAOc>)T+u}|Ojl-sw%+Z$R8~{s~38MntE4Xxg_j!vJiW&g<U|mTPc?{AALTCTCEhFkp(vuLpt7TXcl5gX-H>{xF3ANP;uvRw+?RTSMfuGP}u7^-<Gs0Knu2PobzPD;XUS7OLNRo?CNN7YoA;L&NDekcHCnpmRMy%VAw=_CU)Fh<=IB3VOddJ&o&6##c5rU%FAPS3lc)Bs5!^l|3bI@ml8p2ol^Dk>O1zsCv@ezdL`rXI)4M}ANrT7pXNG%3zbg%=~hK^Id(Y~ioFgd%Q)^1#toTgvnZ_#NU!RjWQe`yCf?z`@}9a3A!xy}w+YUXj+Idv-R44^63q!ZQ>HG?vW|EJFGFqnshd6zPuy%Oc@rb3H^Jp-=$;Al`tR0WI=*8#qskVTglG&rU+%{oFEl`rxDKU+dg-PEwurbj}`1~sW=>SXV83?07#P?LqOzCg@W2%4ajzNNfG_A4!DAZ+J@jWAKYo#`}`HFMRQ?S@T4O!;jtX@BarMB|SCy{ea~+gqw$7#F{;gDFaVZVOd}%!E+EVv<@aIg*W#aMUF5dUy7{3o;ws%@fUQK_XNWB-e9UTPU>kJtA5b5x>iA|9oCD{n#v%K&vOIB2i;ugFCnLi0LOEBl3|So&iW?zYK!&)2s|Jmm1-V0*KewB7~qW5ZJSe+ct)$XPIs|4L>C2GWBa?u^6xr(t_<hZVz#E`z?X5zy`G?Lh(YJxmrboh<++jXL4fC_(@C6z;jgYQEF>W^jbe8ON55yzR|hC=pW$x4eV#=+sdSbLeJ|u;gjWN%O$N7Hw{C|9}XF-GD=O!nUK9)h}Upf-855x?Fka1N~KR)xkdqigaB0oVGW$7X_#B3Qdu_q;k3Gp8)1N9rkdBAWv6x*Q=Q+CTkUioht=+KjG&lB5k6Q@A?gGr(6XF!*lcbjtrVmYJ~*qL#yQ6bcMWQFHmSv}R?`Vujb$ALdehi7?#o&)w3ZS@LRWS!FHqH-#s+0i6GwRx!PJ}!ITD>ip2p#AeK39+!ZO~|{!A1KA&4%-U~JWin%%NgbwnF3of8YAIu@{d==C(I$`#0hv_LbXYF)s|2VsHH;C2aMAtJ?TPH13Ue!6~CJ;3DZhu*`u=8}zx0%w|<6Z$y>2|mWX`FM;fX97$TD+i{_(xy@MOHh4!S~_A}onck^M`DSo%WJs7Y$>Tw<YZm#{!aaScc0z4ojW{u)m>$x>qR^bwrZM8_zTu<6lfbQ<=y(BX&MuIf=1MKp$H`hB#CR&H08B6uP|xcZI$OK&BQ7NvZwjIYMfL^n<<{Ey<#L?r^VMdPL&#Q{#(Q)B$pd=B<AzUtge11Xa7*{Zek}ym%`T8>49qw(<T*Q9vt(R4M?VGfA6)ynnlqj;T)+A524x4x%zYmQFIyJ4YqLMRLB&uUMj*><j<d@Tp)}NkC;Noh;&z>D6n@WRdH8IHG<-%K1%hZ0~H!a4ZVTl5h6jJ3SBWzCX=W7HLs~LA%|*+s?IpE-C&)WQkxc7*L<Vpi`^+T*Cgf>DAGLDX<q*C<3qEpJ6mYY_#hFZ>zL(41RVctqT}hxO!Jlx6nM=N`-4h{rp~scXv9yu+Viuh@gVjgRx6zBjWaD>ezY|jPDk6Ac}Ys&PD`(I;ej}XK*-&4_!P8ah$!7-?8np=CO#LB*I-8h|By$H%&)LC=)gE9DQ1JM0Q82S9VBkb(M6v9GW&Lc_&>h1Tr$ZIhPot70(WR((10}Bd_~jq)LVVlwoUnAz=+36m)Xx{bI5O(@ScQtOtt+MSIbC0j9fu%T6Vh{3YA|acx$@c&e^;H|7PtHTjXmZ&uph#E@If8+#Dyva_v(mXd=?3!Y5X{pa5bnbd#91Ky=n5o+&AbjP}BQ4qX<$Qu<Pcniga^6a`QfZTBYvSg0sL_6X!T1$~Vjt=?}`X}3N>*F-HV>lWq8wPz^9>tZvA>Zpy0memJX6JNLxJVF@ChNFM0LYB&5NvWxr76MALr$QB}Zk+Q4EPz=KNp}1jBwpmqPS>W8OCkz1b%!51=>>oEa#04bjKM$q7Nr$7-WKfN2F+}}4IilplH)QEuvp$uDm8}cKTPZTIP-@VR?jxr&19+Ih3M%9=m)yB(d;7)+h|Y2czEE32qw>%HME^k@$gR9W1H-GJYttg+|GXec=_1s3uv1YsrO(JWoY1OfqA_ijDWO;M~}HKB6H*E1L`6Kh|rjdK`g>MImLy*lS<aO>gGzZ5QOant&GqZNB8Lkyv4C3z>|5uk5q;;+$;)*mYR=fhbOYAakN(twh(;sG_2Gf<SjU8Z)N^0!1yKjOpYc_5AZor;qC|H9mGlMl6wN<cY2uk<tLGe7ot&|e9I6$rbM1?b<3=LN*#p}6ly6tGj9mo=AM<$nc^&VYf@D~pvvI1>N&=^*iz0`8EbT?+v*#Jh{(RSpB}oUwLzN-HR!-tH(QR^&zeMKJfZM5V+5C!KEE_)-|faGB6;#*o{9{?<#nRflbJi&=Z$+EEnMx|`oN}&?0)Y0h8E>!i`BX|Dv=rsjDIdAp8(+nS@NXrpI~UQOtwpuad&`d=rVV<uCY359K7gTnm7a=)znDuL96fs+xVH_(lKUrzjC$<7jub;FYmyS#Kacc-Lxu%nDAKWZ2%itU3O#^+!vHuJ+elYGHM&ci(Gs~VBIl$E)=6O5;`e;ifrd+W9WUC@xeGa<Ww-l+#4@}eq?LszIV44m!9Utb>>{g6<Bj`(~nul0jc7XFkMBlnEOU<ab{0NF@@J6#x#=}r$656PRnU!8=JZil&A1$YQFj$x&nf=5IEO}0>@|AG+uXDn|lT3ViJ7>U~(=<>VS1Bg`cy?A-S}o$J!Y|h8Zuw+2KqaOe`%tTS`(qf~K3p>r$0!pY+4d#&i6;9Z=C~T~@n?7y}OR>q2{(hfWpvi*g=PoSSF25KpWShpM-34TU<t?=<vz&;|yfCsSxXscniEnwPtA!srW+?c9@E#cdu&zZw!o*-PR^0s;(l!apXW!|3I-?kSO|%nG2>t$41u^m7I!T*03)`Dq&&^~J2_VQEex`Z-&#+?QvS;$6Ag*rJ3>RF;BcEb$_5|K}^B=E1M7fyHfJ2~;y8@^rDkRi0opqp`Dn*%$B+0YM%C{SkY>cF9c_!iD(#^VT1G`_Lg}Pi9pY24UzSQ16K`cbU?dC#8|tK%j|Sm~qUB<bdEu^jzg`r7X&y$H}k9NHjmeD@$`922wQ6w=Q=O#i3W!?4uKWTwG_BNe4Ui^XbOrV6g4PAYh?3uZs)ccugukW10Cp)e?29ca7I884c|tqvr%{(RECzpBSbCrCt-TUXuQHLzq_aY0`P%ivA=uo<ySCmuzO~W>$h}sxiE>g2Vr~7Dvy878I>^5gYZx>Few%RI?{}=@B)zi9Z2^C4{yZ!>D#*;=MH4^idw(eHe*3moNZ^Ip5zJeg?}Y#MD<f82gg%8&bu{iP9%cU;|@ZT^&u9g}@{ncD#^^BPNe>40`ja&!l;#DvAfzUS4@%Y<nYxk9l_PQ`Wlug|My-e9uyp7(#AipiI=HOQxwUv=WpPSY}_t7>q-b&29clZBg^^Mxx66lZYzEP@Ck6nLfLN!~4V2(hsrNRb6idC6}|GClXLs+2vyjv)fm|T2<E@v0B^0ZMC$u&S<ULVyd@cz&@`H2;1WV{mT~KzJDGMb8BHE(TW$l;!3Fv$N3Lv75mT7SoC#j&qtQ;FEB6N8=8QT0t0jeC2N)<UwY{q%K577jZg<k02s+O+4C~E0-{hAG2fZV?;szq`RI!2D)ty{4zfu;jfUHn=^c`xR$ouX@-bwVz}V*;g3T2U!5tdJ1>z`oV4*W5yr`R!A(hX~si7(sHNZ@gLo&H^ZJrDDq|d?eed>;o#|81>2~1`y#VRg8%2nX4LJbq<mnBPcp>+gelf+SGRb;44xMal?x<-s>B$i2AH1*C5ODOb=Vsll1fjYv~|3{cYp<d*eD*h?pRm0UM=nU&?bc}Xvv{ptPX8KP;KFwfZb~T`T9?OMhQC-;L*RHsV2&VK4Sozs4!g+`6ZnLn<NgI7Gv5+<Tw{b~IJ)=OY19otuLBFM&JA_3!#+SJ{nl7IFR(RWA*<CbYQaj9~Sje9}JjuqBI<m@35;%AOQ+RoS^+B94KP71N`u>UYY`*NSy!)A=WM1|pgeSJ%F&H8L(AMo*bX&?Rlte786TsMHou@+`iRBUQ@@2L$q3r?8f++wC0T5$wlVd1$yw2-=X**}K%*-xMBba?7V4*|K=p(6z9C<8qAvTq>1XK^v-AD9cx%S}O-Q?=F=1v=uu!emBrT^>XSR=#Pe8Z8ayOsxIB@sCpo4L>o63uwcpMkYGGL;!gg;1CCyk7UN?FbU}z8-SHiSyz8y7vjIi4k+KZzFpFrsb+QUyFHmDZgtoMOdLJ!&Y*A-GHp&i&G9a^**Nj<+c**hmAq9^VbfAU;ClVg*XwlKeOkvD3v=;1<ktH=gheTx4`jMMZjTun!$jilBtj&!YUzAq6fM=UjL<#V#8Keb(oQs=nH#!pgc7nFackW2x*iUEfiBS1R)`BSGv56O>$HJg|6Vz@mN%6eS540`-0^BF^qqH|NY2gf%p46IL=bY2-P<HvZE20Vzd<s5FAh6Gd-WduZCcXorD;YV!Py2Opmo0&dH4aWLSj{>Hk5MHXmk!Zs{gpKFhzzi9(fb1WSvW+-4_BXCzNuK%x=Ap&DtCN4ylOLFYwt92yFaQGuz;jnciGmO@8}-9dGXR!7`+w^N<`S_&Z{+V4OFZ?*f)G?!SC9Sn1~TOZU=%hMp*dUc%h<IP{rAF;Px-}x)g#ehEiTq#(R2=I<9rVtd8TnjGK69X$RL)3K#V3;cA1izCuaI^svB<y&N$5x#YYV&|&ZmO7*t=Ug*a4#@HO5bATY}OXMwvAYN<I-b{Q?oC)D3y&3U`ZUy=Qr2!aud(~7IE*YKDHE+K>D!YG31L?V*-iL!y-+m7;f92v)PodN(XvDqe{^G;T0msr7g6f!?&u0?U>OnTlTE#PO|QO#sU;i<8!1#=gYsuMWyQSe#jPtU}XJm7fRA~Djf6mc1+y=iDueSih2#+KjWl9mT<-i7rDQ|2c_<i<Eb4(A6sdpLR$sCDfHt*bNiXXwI|@R2k(z>Vb(0e?D`B+xWnv0ZK4)HV7wKyIc91Xfie*|nuf2pQ><q*`0>fGx+C{^c&zsf7`a&(^&IWy7P2Nhbzhu~P9;zaUka@vOYKIX7CD*QOe3PtF&An?EqXTyOQHd;P#SYG*UQ-ZZIik9y;~f>coF_`53X6~+F41<mYTXDk^t6zwAD@N)?(sMU^oVl0LD5s+BZ|qVTm_7cM^6NDnl$W=k`Y6OnibAfYB{YLNY!k;|Gd@k)mPdqz(}^JKpq$S%=rS`518m)Mcbx6_(ICHD<d?W{5|=jL<5$^>H9ok5bAFHI|3jgeFfv7!15`6nJI9<-;vbjNwOC=>nv@Ya&XOMck_o9W`i6Atc0dzGzPZAH2ByUhtcKFkN$7i2YcDb1tK;g>31!vB%7+48s#LAtt2mBITFdEcRNGf<m5&`z^jqiFO~RnJQ>+KdokwVC55upyK?VazENT#u>ZbkzGNAM-y@>uMRLYbx9Smb=Xm&{up=*r7vkgP{l{nV9!>amakae$8W!V{>JCOAL!3N{`vjafBon0n$EFsd7VX<u(E?k*4WXoA%S^rU^jgWL<znTRk+KSR-Zf<WgTtF=Y;aG-TFJtfelGrfIE5uhC{%ig<zTF3EMKW=LLOLCGNUnhn@CATT!_C3*F$yPZo>v<LzV0V~esal&(Ie{9_-VKMW2{Fjw9#I5Vl@I62cyyDXJ~+xpqxu0G!D7tasFud-{ukj2pXf35d1*VQiFbA-i{Qdq@98OL&@8#s<2ifx|%hu2My|Fzo_8{3rz@Rulo`LEUT9Q^mS@7$aPgXY1h^?d7T!Os`0m`)0;gOY_~Q+}(&@s24LN(i6BP~{6s9ET|zLhOlX6Ml|&#x@*HGO<ACzM0Pz+1g9$pHH!f7LVg2c(+L@P#wnj<a+t#KW6*?{lEYB{{xa*CPV')))
_ROUTES={0:_PAYLOAD['base']}
for _rid,_patch in _PAYLOAD['patches'].items():
    _tape=list(_ROUTES[0])
    for _t,_a in _patch: _tape[_t]=_a
    _ROUTES[int(_rid)]=_tape
del _PAYLOAD
_SETTINGS={'hand_align': True, 'weed_repair': True, 'sell_lead': True, 'budget_guard': False, 'room_guard': False, 'clamp_sells': False, 'dead_stock': False, 'terminal_liquidation': False, 'front_run': False}

def _router(observation,step,state):
    if step>=144 and not state.get('day6'):
        shops=_get(_get(observation,'town',{}),'unlocked_shops',[]) or []
        state['route']={('BAKERY', 'YARN_STORE'): 3, ('BRUNCH_SPOT', 'YARN_STORE'): 4, ('FARMERS_MARKET', 'YARN_STORE'): 5, ('ICE_CREAM_SHOP', 'YARN_STORE'): 6, ('PET_CAFE', 'YARN_STORE'): 5, ('PIZZA_SHOP', 'YARN_STORE'): 7, ('SMOOTHIE_SHOP', 'YARN_STORE'): 8, ('YARN_STORE', 'BAKERY'): 9, ('YARN_STORE', 'BRUNCH_SPOT'): 9, ('YARN_STORE', 'FARMERS_MARKET'): 1, ('YARN_STORE', 'ICE_CREAM_SHOP'): 9, ('YARN_STORE', 'PET_CAFE'): 10, ('YARN_STORE', 'PIZZA_SHOP'): 6, ('YARN_STORE', 'SMOOTHIE_SHOP'): 11, ('YARN_STORE', 'YARN_STORE'): 12}.get(tuple(shops[:2]),0)
        state['day6']=True
    if step>=648 and not state.get('day27'):
        state['route']=2
        state['day27']=True
    return state.get('route',0)

_R42_OPENING=[['BUY_PRODUCT', 'WHEAT', 13], ['BUY_PRODUCT', 'WHEAT', 10], ['SELL', 'WHEAT', 30]]
for _r42_tape in _ROUTES.values():
    _r42_tape[0]=dict(_r42_tape[0],market=[list(o) for o in _R42_OPENING])
del _r42_tape
_IMPL=make_agent(_ROUTES,router=_router,**_SETTINGS)
_IMPL.chassis.diagnostics['terminal_rescue_errors']=0

def agent(observation,configuration=None):
    try:
        action=_IMPL(observation,configuration)
        pass
        return action
    except Exception:
        return {'farmer':['PASS'],'hands':[],'market':[]}

_SHOP_PARENT=agent
del agent

def agent(observation,configuration=None):
    action=_SHOP_PARENT(observation,configuration)
    try:
        if _step_of(observation)>=718:
            view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
            units=[]
            for i,pos in enumerate(view.positions):
                units.append(['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'])
            action={'farmer':units[0],'hands':units[1:],'market':[]}
            projected=_IMPL.chassis._projected_shed(action,view)
            action['market']=[['SELL',item,projected.get(item,0)] for item in PRODUCTS if projected.get(item,0)>0]
            action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    except Exception:
        _IMPL.chassis.diagnostics['terminal_rescue_errors'] += 1
    return action

# EXP-154 modifications: Ahmed Berat Ozer; public capabilities credited below.
# Dmitrii Gluzdov Seven Turn Rescue and Kaggle engine contributors, Apache-2.0.

_UNIT_NS={"__name__":"v28_own_unit_model"}
exec('# SPDX-License-Identifier: Apache-2.0\n# Extracted Kaggle / kaggle-environments contributor code; see NOTICE.txt.\n"""Exact deterministic unit/decay semantics extracted from kaggle-environments 1.32.7.\nSource kaggriculture.py SHA256 bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e.\nNo interpreter, market RNG, policy controls, or replay content is included.\n"""\n\nENGINE_VERSION = "1.32.7"\nSOURCE_SHA256 = "bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e"\n\nCROPS = {\n    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},\n    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},\n    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},\n    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},\n    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},\n}\n\nANIMALS = {\n    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},\n    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},\n    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},\n}\n\nPRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]\n\nFARMER_MOVES = {\n    "NORTH": (0, -1),\n    "SOUTH": (0, 1),\n    "EAST":  (1, 0),\n    "WEST":  (-1, 0),\n}\n\ndef _shed_access_tiles(board_size):\n    """Four inner-corner tiles around the shed, in NWSE order."""\n    half = board_size // 2\n    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]\n\ndef _is_shed_adjacent(pos, board_size):\n    return tuple(pos) in {(x, y) for (x, y) in _shed_access_tiles(board_size)}\n\ndef _new_plant(crop, day, turns_per_day):\n    cd = CROPS[crop]\n    return {\n        "kind": "PLANT",\n        "crop": crop,\n        "planted_day": day,\n        "watered_today": False,\n        "consecutive_unwatered": 1,  # planting day counts as unwatered\n        "yield_units": 0 if cd["ongoing"] else 1,\n        "max_lifespan_step": (-1 if cd["ongoing"] else (day + cd["max_yield_day"] + 1) * turns_per_day),\n        "fertilized_until_day": -1,\n    }\n\ndef _new_animal(animal, day):\n    a = ANIMALS[animal]\n    return {\n        "kind": a["structure"],\n        "animal": animal,\n        "placed_day": day,\n        "yield_units": 0,\n        "consecutive_unfed": 0,\n        "fed_today": False,\n        "cared_today": False,\n        "fertilizer_available": False,\n        "pending_care_bonus": 0,\n    }\n\ndef _farmer_position(farm, idx):\n    """idx 0 = main farmer, 1+ = hand index."""\n    if idx == 0:\n        return farm["farmer"]\n    return farm["hands"][idx - 1] if idx - 1 < len(farm["hands"]) else None\n\ndef _set_farmer_position(farm, idx, pos):\n    if idx == 0:\n        farm["farmer"] = list(pos)\n    else:\n        farm["hands"][idx - 1] = list(pos)\n\ndef _farmer_inventory(private, idx):\n    """Inventories list is [main_farmer, *hands]; grow it if idx is past the end."""\n    while len(private["inventories"]) <= idx:\n        private["inventories"].append({})\n    return private["inventories"][idx]\n\ndef _inv_add(inv, item, n=1):\n    inv[item] = inv.get(item, 0) + n\n\ndef _inv_take(inv, item, n=1):\n    if inv.get(item, 0) < n:\n        return False\n    inv[item] -= n\n    if inv[item] == 0:\n        del inv[item]\n    return True\n\ndef _apply_unit_action(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):\n    """Process one farmer/hand\'s action. Invalid / illegal actions are silent no-ops."""\n    if not isinstance(action, list) or not action:\n        return\n    op = action[0]\n    pos = _farmer_position(farm, idx)\n    if pos is None:\n        return\n    fx, fy = pos[0], pos[1]\n    inv = _farmer_inventory(private, idx)\n\n    if op in FARMER_MOVES:\n        dx, dy = FARMER_MOVES[op]\n        nx, ny = fx + dx, fy + dy\n        if not (0 <= nx < board_size and 0 <= ny < board_size):\n            return\n        # Movement onto LOCKED tiles is allowed: a hand can spawn on a locked\n        # shed-access tile, and blocking movement would strand it there forever.\n        # Tile operations (PLANT, WATER, etc.) still no-op on LOCKED tiles.\n        _set_farmer_position(farm, idx, (nx, ny))\n        return\n\n    if op == "PASS":\n        return\n\n    tile = farm["tiles"][fy][fx]\n\n    # Shed operations resolve before the LOCKED guard. They use the tile only as\n    # a standing position -- the shed itself is always owned -- and three of the\n    # four shed-access tiles start LOCKED, so guarding them first would make the\n    # shed unreachable from those tiles.\n    if op == "DROP":\n        if not _is_shed_adjacent((fx, fy), board_size):\n            return\n        shed = private["shed"]\n        for item, n in list(inv.items()):\n            if n <= 0:\n                del inv[item]\n                continue\n            room = max(0, shed_capacity - sum(shed.values()))\n            take = min(n, room)\n            if take > 0:\n                shed[item] = shed.get(item, 0) + take\n            del inv[item]\n        return\n\n    if op == "PICKUP":\n        if not _is_shed_adjacent((fx, fy), board_size):\n            return\n        if len(action) < 2:\n            return\n        item = action[1]\n        n = int(action[2]) if len(action) >= 3 else 1\n        if n <= 0:\n            return\n        # Seeds live in private["seeds"] and are consumed directly by PLANT;\n        # they never pass through farmer inventory or the shed.\n        available = private["shed"].get(item, 0)\n        n = min(n, available)\n        if n <= 0:\n            return\n        private["shed"][item] -= n\n        _inv_add(inv, item, n)\n        return\n\n    if op == "PLACE":\n        if len(action) < 2:\n            return\n        item = action[1]\n        # Animal placement: standing on a matching unoccupied structure. A LOCKED\n        # tile is the string "LOCKED", never a dict, so this branch cannot match\n        # there and PLACE falls through to the shed path below.\n        if (\n            item in ANIMALS\n            and isinstance(tile, dict)\n            and tile.get("kind") == ANIMALS[item]["structure"]\n            and "animal" not in tile\n        ):\n            if _inv_take(inv, item, 1):\n                farm["tiles"][fy][fx] = _new_animal(item, day)\n            return\n        # Shed drop: orthogonally adjacent to the shed; obeys shedCapacity.\n        if _is_shed_adjacent((fx, fy), board_size):\n            n = int(action[2]) if len(action) >= 3 else 1\n            if n <= 0:\n                return\n            n = min(n, inv.get(item, 0))\n            if n <= 0:\n                return\n            current = sum(private["shed"].values())\n            room = max(0, shed_capacity - current)\n            n = min(n, room)\n            if n <= 0:\n                return\n            inv[item] -= n\n            if inv[item] == 0:\n                del inv[item]\n            private["shed"][item] = private["shed"].get(item, 0) + n\n        return\n\n    # Everything below mutates the tile the unit stands on, so it requires that\n    # tile to be owned.\n    if tile == "LOCKED":\n        return\n\n    if op == "PLANT":\n        if len(action) < 2:\n            return\n        crop = action[1]\n        if crop not in CROPS:\n            return\n        if tile is not None:\n            return\n        if private["seeds"].get(crop, 0) <= 0:\n            return\n        private["seeds"][crop] -= 1\n        farm["tiles"][fy][fx] = _new_plant(crop, day, turns_per_day)\n        return\n\n    if op == "WATER":\n        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):\n            return\n        if tile["watered_today"]:\n            return\n        tile["watered_today"] = True\n        crop_data = CROPS[tile["crop"]]\n        if not crop_data["ongoing"]:\n            age_days = day - tile["planted_day"]\n            window_start = (crop_data["max_yield_day"] + 1) // 2\n            if window_start <= age_days <= crop_data["max_yield_day"]:\n                bonus = 2 if tile["fertilized_until_day"] >= day else 1\n                tile["yield_units"] = min(crop_data["max_yield"], tile["yield_units"] + bonus)\n        return\n\n    if op == "HARVEST":\n        if not isinstance(tile, dict):\n            return\n        if tile.get("yield_units", 0) <= 0:\n            return\n        if tile.get("kind") == "PLANT":\n            crop_data = CROPS[tile["crop"]]\n            if day - tile["planted_day"] < crop_data["first_yield_day"]:\n                # Ongoing crops only accumulate yield_units after first_yield_day,\n                # so reaching here with yield_units > 0 indicates a bug.\n                if crop_data["ongoing"]:\n                    print(\n                        f"WARNING: HARVEST on immature ongoing {tile[\'crop\']} "\n                        f"(planted day {tile[\'planted_day\']}, current day {day}, "\n                        f"first_yield_day {crop_data[\'first_yield_day\']}, "\n                        f"yield_units {tile[\'yield_units\']}); should never happen"\n                    )\n                return\n            units = tile["yield_units"]\n            tile["yield_units"] = 0\n            _inv_add(inv, tile["crop"], units)\n            if not crop_data["ongoing"]:\n                farm["tiles"][fy][fx] = None\n        elif "animal" in tile:\n            units = tile["yield_units"]\n            tile["yield_units"] = 0\n            _inv_add(inv, ANIMALS[tile["animal"]]["product"], units)\n        return\n\n    if op == "FERTILIZE":\n        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):\n            return\n        if not _inv_take(inv, "FERTILIZER", 1):\n            return\n        # Active for `day`, `day+1`, `day+2` (3 days inclusive).\n        tile["fertilized_until_day"] = max(tile.get("fertilized_until_day", -1), day + 2)\n        return\n\n    if op == "DIG":\n        if tile is None:\n            return\n        # Removes plants, weeds, empty coop/pasture. Does NOT remove a placed animal.\n        if isinstance(tile, dict) and "animal" in tile:\n            return\n        farm["tiles"][fy][fx] = None\n        return\n\n    if op == "BUILD_COOP":\n        if tile is not None:\n            return\n        farm["tiles"][fy][fx] = {"kind": "COOP"}\n        return\n\n    if op == "BUILD_PASTURE":\n        if tile is not None:\n            return\n        farm["tiles"][fy][fx] = {"kind": "PASTURE"}\n        return\n\n    if op == "FEED":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if tile["fed_today"]:\n            return\n        if not _inv_take(inv, "WHEAT", 1):\n            return\n        tile["fed_today"] = True\n        return\n\n    if op == "COLLECT_FERTILIZER":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if not tile["fertilizer_available"]:\n            return\n        tile["fertilizer_available"] = False\n        _inv_add(inv, "FERTILIZER", 1)\n        return\n\n    if op == "CARE":\n        if not (isinstance(tile, dict) and "animal" in tile):\n            return\n        if tile["cared_today"]:\n            return\n        tile["cared_today"] = True\n        return\n\ndef _decay_plants(farm, step):\n    board_size = len(farm["tiles"])\n    for y in range(board_size):\n        for x in range(board_size):\n            tile = farm["tiles"][y][x]\n            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":\n                continue\n            mls = tile["max_lifespan_step"]\n            if mls < 0 or step < mls:\n                continue\n            if (step - mls) % 2 != 0:\n                continue\n            tile["yield_units"] -= 1\n            if tile["yield_units"] <= 0:\n                farm["tiles"][y][x] = {"kind": "WEED"}\n\n',_UNIT_NS)
_PLANNER_NS=dict(_UNIT_NS)
exec('"""E182 modification: Shop0909 last-seven-turn physical closure planner.\n\nNo engine imports, policy tapes, replay fixtures, RNG or remote calls.\nThe only supported market continuation is SELL; unknown execution abstains.\n"""\nfrom copy import deepcopy\nfrom time import perf_counter\nSTART, FINAL = (712, 718)\nOPS = set(FARMER_MOVES) | {\'PASS\', \'DROP\', \'PICKUP\', \'PLACE\', \'PLANT\', \'WATER\', \'HARVEST\', \'FERTILIZE\', \'DIG\', \'BUILD_COOP\', \'BUILD_PASTURE\', \'FEED\', \'CARE\', \'COLLECT_FERTILIZER\'}\nITEMS = tuple(PRODUCTS) + tuple(ANIMALS)\n\nclass Unsupported(ValueError):\n    pass\n\ndef _get(obj, key, default=None):\n    return obj.get(key, default) if isinstance(obj, dict) else getattr(obj, key, default)\n\ndef _settings(config):\n    size, turns, last = (_get(config, k, d) for k, d in [(\'boardSize\', 10), (\'turnsPerDay\', 24), (\'episodeSteps\', 720)])\n    if (size, turns, last) != (10, 24, 720):\n        raise Unsupported(\'requires pinned 10x10/24/720 terminal window\')\n    cap = int(_get(config, \'shedCapacity\', 100))\n    orders = min(10, int(_get(config, \'maxMarketOrdersPerTurn\', 10)))\n    if cap < 1 or orders < 1:\n        raise Unsupported(\'invalid capacity/order limit\')\n    return (size, turns, cap, orders)\n\ndef physical_state(obs):\n    """Comparable own physical state; market prices and bank are intentionally excluded."""\n    seat = int(_get(obs, \'player\', 0))\n    farm = _get(obs, \'farms\')[seat]\n    return ({k: v for k, v in farm.items() if k != \'money\'}, _get(obs, \'private\'))\n\ndef _commands(action, n):\n    return [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])][:n] + [[\'PASS\'] for _ in range(max(0, n - 1 - len(action.get(\'hands\', []))))]\n\ndef _clone_state(farm, private):\n    f = dict(farm)\n    f[\'tiles\'] = [[dict(tile) if isinstance(tile, dict) else tile for tile in row] for row in farm[\'tiles\']]\n    f[\'farmer\'] = list(farm[\'farmer\'])\n    f[\'hands\'] = [list(pos) for pos in farm[\'hands\']]\n    f[\'unlocked_quadrants\'] = list(farm[\'unlocked_quadrants\'])\n    pr = dict(private)\n    pr[\'shed\'], pr[\'seeds\'] = (dict(private[\'shed\']), dict(private[\'seeds\']))\n    pr[\'inventories\'] = [dict(inv) for inv in private[\'inventories\']]\n    return (f, pr)\n\ndef _clone_schedule(schedule):\n    result = []\n    for action in schedule:\n        value = dict(action)\n        if \'farmer\' in action:\n            value[\'farmer\'] = list(action[\'farmer\'])\n        for key in [\'hands\', \'market\']:\n            if key in action:\n                value[key] = [list(command) for command in action[key]]\n        result.append(value)\n    return result\n\ndef _validate(schedule, n, orders):\n    for action in schedule:\n        if not isinstance(action, dict) or set(action) - {\'farmer\', \'hands\', \'market\'}:\n            raise Unsupported(\'unknown action shape\')\n        if not isinstance(action.get(\'hands\', []), list):\n            raise Unsupported(\'hands must be a list\')\n        for command in [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])]:\n            if not isinstance(command, list) or not command or command[0] not in OPS:\n                raise Unsupported(\'unknown/malformed unit operation\')\n            if command[0] in {\'PICKUP\', \'PLACE\', \'PLANT\'}:\n                if len(command) < 2 or command[1] not in ITEMS:\n                    raise Unsupported(\'unknown unit item\')\n                if len(command) > 2 and (not isinstance(command[2], int)):\n                    raise Unsupported(\'noninteger unit quantity\')\n        market = action.get(\'market\', [])\n        if not isinstance(market, list) or len(market) > orders:\n            raise Unsupported(\'market order shape/cap\')\n        for order in market:\n            if not isinstance(order, list) or len(order) != 3 or order[0] != \'SELL\' or (order[1] not in PRODUCTS) or (not isinstance(order[2], int)) or (order[2] <= 0):\n                raise Unsupported(\'baseline market must contain positive integer SELL only\')\n\ndef liquidation(shed, inherited_market, max_orders=10):\n    """Use actual post-unit stock; retain first parent item ordering, then stable product order."""\n    items = []\n    for order in inherited_market:\n        if order[1] not in items:\n            items.append(order[1])\n    items += [item for item in PRODUCTS if item not in items]\n    orders = [[\'SELL\', item, int(shed.get(item, 0))] for item in items if shed.get(item, 0) > 0]\n    if len(orders) > min(10, max_orders):\n        raise Unsupported(\'actual final stock exceeds order slots\')\n    return orders\n\ndef shop_liquidation(farm, private, prices):\n    """Exact original final worker/drop and market rule, with current stock/prices."""\n    return liquidate(FarmView({\'player\': 0, \'farms\': [farm], \'private\': private, \'market\': {\'prices\': prices}}))\n\ndef simulate(obs, config, schedule, *, final_liquidate=False, detailed=False, preserve_final_commands=False):\n    """Exact own unit/decay and SELL-stock transitions. No claim to simulate shared prices."""\n    size, turns, cap, order_cap = _settings(config)\n    step = int(_get(obs, \'step\', -1))\n    if step < START or step + len(schedule) - 1 > FINAL or (not schedule):\n        raise Unsupported(\'outside 712..718; no day boundary or terminal auto-drop\')\n    if any(((t + 1) % turns == 0 for t in range(step, step + len(schedule)))):\n        raise Unsupported(\'day boundary\')\n    farm0, private0 = physical_state(obs)\n    farm, private = _clone_state(farm0, private0)\n    n = 1 + len(farm[\'hands\'])\n    if len(private[\'inventories\']) != n or n > 32:\n        raise Unsupported(\'invalid/unbounded worker inventory shape\')\n    _validate(schedule, n, order_cap)\n    deposited = [dict() for _ in range(n)]\n    sold = {}\n    snapshots, rows, events = ([], [], [])\n    executed = _clone_schedule(schedule)\n    overflow = 0\n    for offset, action in enumerate(executed):\n        t = step + offset\n        if detailed:\n            snapshots.append(_clone_state(farm, private))\n        if t == FINAL and (not preserve_final_commands):\n            action = shop_liquidation(farm, private, _get(obs, \'market\')[\'prices\'])\n            executed[offset] = action\n        all_commands = [action.get(\'farmer\', [\'PASS\']), *action.get(\'hands\', [])]\n        demand = {}\n        for command in all_commands:\n            if command[0] == \'PLANT\':\n                demand[command[1]] = demand.get(command[1], 0) + 1\n        blocked = {item for item, count in demand.items() if count > private[\'seeds\'].get(item, 0)}\n        for actor, command in enumerate(_commands(action, n)):\n            if command[0] == \'PLANT\' and command[1] in blocked:\n                command = [\'PASS\']\n            pos = farm[\'farmer\'] if actor == 0 else farm[\'hands\'][actor - 1]\n            xy = tuple(pos)\n            inv = private[\'inventories\'][actor]\n            before_inv = dict(inv) if command[0] in {\'DROP\', \'HARVEST\', \'COLLECT_FERTILIZER\'} else None\n            before_shed = dict(private[\'shed\']) if command[0] in {\'DROP\', \'PLACE\'} else None\n            _apply_unit_action(farm, private, actor, command, size, t // turns, turns, cap)\n            if before_shed is not None:\n                delta = {item: amount - before_shed.get(item, 0) for item, amount in private[\'shed\'].items() if amount > before_shed.get(item, 0)}\n                for item, amount in delta.items():\n                    deposited[actor][item] = deposited[actor].get(item, 0) + amount\n                if delta:\n                    events.append({\'offset\': offset, \'actor\': actor, \'op\': command[0], \'xy\': xy, \'deposited\': delta})\n                if command[0] == \'DROP\':\n                    overflow += sum((max(0, amount - inv.get(item, 0) - delta.get(item, 0)) for item, amount in before_inv.items()))\n            if command[0] in {\'HARVEST\', \'COLLECT_FERTILIZER\'}:\n                delta = {item: amount - before_inv.get(item, 0) for item, amount in inv.items() if amount > before_inv.get(item, 0)}\n                if delta:\n                    events.append({\'offset\': offset, \'actor\': actor, \'op\': command[0], \'xy\': xy, \'acquired\': delta})\n        pre_market = dict(private[\'shed\'])\n        if t == FINAL and preserve_final_commands and final_liquidate:\n            action[\'market\'] = liquidation(pre_market, [], order_cap)\n            prices = _get(obs, \'market\')[\'prices\']\n            action[\'market\'].sort(key=lambda order: -int(prices.get(order[1], 0)) * order[2])\n        for _, item, requested in action.get(\'market\', []):\n            quantity = min(requested, private[\'shed\'].get(item, 0), 99999)\n            if quantity > 0:\n                private[\'shed\'][item] -= quantity\n                sold[item] = sold.get(item, 0) + quantity\n        _decay_plants(farm, t)\n        rows.append({\'pre_market_shed\': pre_market, \'post_market_shed\': dict(private[\'shed\']), \'deposited_by_actor\': [dict(v) for v in deposited], \'sold\': dict(sold)})\n    if detailed:\n        snapshots.append(_clone_state(farm, private))\n    return {\'rows\': rows, \'states\': snapshots, \'events\': events, \'actions\': executed, \'overflow_units\': overflow, \'farm\': farm, \'private\': private, \'sold\': sold}\n\ndef _ge(left, right):\n    return all((left.get(item, 0) >= value for item, value in right.items()))\n\ndef dominates(candidate, baseline):\n    """Preserve every baseline worker\'s actual deposit prefixes and shed availability."""\n    if candidate[\'overflow_units\']:\n        return False\n    for new, old in zip(candidate[\'rows\'], baseline[\'rows\']):\n        if not _ge(new[\'pre_market_shed\'], old[\'pre_market_shed\']):\n            return False\n        if not _ge(new[\'sold\'], old[\'sold\']):\n            return False\n        if any((not _ge(a, b) for a, b in zip(new[\'deposited_by_actor\'], old[\'deposited_by_actor\']))):\n            return False\n    return True\n\ndef _value(run, prices):\n    shed = run[\'private\'][\'shed\']\n    return sum(((run[\'sold\'].get(item, 0) + shed.get(item, 0)) * prices[item] for item in PRODUCTS))\n\ndef _walk(start, end):\n    x, y = start\n    tx, ty = end\n    return [[\'EAST\']] * max(0, tx - x) + [[\'WEST\']] * max(0, x - tx) + [[\'SOUTH\']] * max(0, ty - y) + [[\'NORTH\']] * max(0, y - ty)\n\ndef _return(pos):\n    targets = _shed_access_tiles(10)\n    target = min(targets, key=lambda xy: (abs(pos[0] - xy[0]) + abs(pos[1] - xy[1]), targets.index(xy)))\n    return _walk(pos, target) + [[\'DROP\']]\n\ndef _proposals(run, actor, prices, max_per_actor):\n    """One/two resource bundles plus direct carry closure, replacing a baseline suffix."""\n    owners = {}\n    for event in run[\'events\']:\n        if \'acquired\' in event:\n            owners.setdefault((tuple(event[\'xy\']), event[\'op\']), set()).add(event[\'actor\'])\n    proposals = []\n    seen = set()\n    horizon = len(run[\'rows\'])\n    for offset in range(horizon):\n        farm, private = run[\'states\'][offset]\n        pos = tuple(farm[\'farmer\'] if actor == 0 else farm[\'hands\'][actor - 1])\n        inventory = private[\'inventories\'][actor]\n        carried = sum((prices.get(item, 0) * count for item, count in inventory.items()))\n        prefix_deposits = run[\'rows\'][offset - 1][\'deposited_by_actor\'][actor] if offset else {}\n        future_deposits = run[\'rows\'][-1][\'deposited_by_actor\'][actor]\n        obligation = sum((prices.get(item, 0) * (count - prefix_deposits.get(item, 0)) for item, count in future_deposits.items()))\n        bundles = []\n        for y, row in enumerate(farm[\'tiles\']):\n            for x, tile in enumerate(row):\n                if not isinstance(tile, dict):\n                    continue\n                xy, operations, value = ((x, y), [], 0)\n                if tile.get(\'yield_units\', 0) > 0:\n                    item = tile.get(\'crop\') if tile.get(\'kind\') == \'PLANT\' else ANIMALS.get(tile.get(\'animal\'), {}).get(\'product\')\n                    mature = item and (\'animal\' in tile or (START + offset) // 24 - tile[\'planted_day\'] >= CROPS[item][\'first_yield_day\'])\n                    if mature and (not owners.get((xy, \'HARVEST\'), set()) - {actor}):\n                        operations.append([\'HARVEST\'])\n                        value += prices[item] * tile[\'yield_units\']\n                if tile.get(\'fertilizer_available\') and \'animal\' in tile and (not owners.get((xy, \'COLLECT_FERTILIZER\'), set()) - {actor}):\n                    operations.append([\'COLLECT_FERTILIZER\'])\n                    value += prices[\'FERTILIZER\']\n                if operations:\n                    distance = len(_walk(pos, xy)) + len(operations) + len(_return(xy))\n                    if distance <= horizon - offset:\n                        bundles.append((xy, operations, value, distance))\n        bundles.sort(key=lambda b: (-b[2] / b[3], -b[2], b[0]))\n        variants = [([], carried)] if carried else []\n        for xy, ops, value, _ in bundles[:6]:\n            variants.append(([(xy, ops)], carried + value))\n        for first in bundles[:3]:\n            for second in bundles[:3]:\n                if first[0] != second[0]:\n                    variants.append(([(first[0], first[1]), (second[0], second[1])], carried + first[2] + second[2]))\n        for stops, value in variants:\n            route, cursor = ([], pos)\n            for xy, ops in stops:\n                route += _walk(cursor, xy) + ops\n                cursor = xy\n            route += _return(cursor)\n            if len(route) > horizon - offset:\n                continue\n            route += [[\'PASS\']] * (horizon - offset - len(route))\n            key = (offset, tuple((tuple(c) for c in route)))\n            if key not in seen:\n                seen.add(key)\n                proposals.append((value - obligation, offset, route, len(stops)))\n    proposals.sort(key=lambda p: (-p[0], p[1], p[2]))\n    direct = [p for p in proposals if p[3] == 0 and p[0] > 0][:2]\n    chosen = direct + [p for p in proposals if p not in direct]\n    return chosen[:max_per_actor]\n\ndef plan_terminal(obs, config, baseline_remaining, *, max_simulations=64, passes=1, proposals_per_actor=4):\n    """At 712 accept seven actions; positive physical delivery is mandatory."""\n    begun = perf_counter()\n    fallback = {\'accepted\': False, \'reason\': \'\', \'actions\': None, \'simulations\': 0}\n    try:\n        if int(_get(obs, \'step\', -1)) != START or len(baseline_remaining) != FINAL - START + 1:\n            raise Unsupported(\'planning requires step 712 and exactly seven actions through 718\')\n        max_simulations = min(256, max(1, int(max_simulations)))\n        passes = min(2, max(1, int(passes)))\n        proposals_per_actor = min(16, max(1, int(proposals_per_actor)))\n        baseline = simulate(obs, config, baseline_remaining, detailed=True)\n        prices = {item: max(1, float(_get(obs, \'market\', {}).get(\'prices\', {}).get(item, 1))) for item in PRODUCTS}\n        current, best = (_clone_schedule(baseline_remaining), baseline)\n        baseline_value = best_value = _value(baseline, prices)\n        changes, simulations = ([], 0)\n        n = len(baseline[\'private\'][\'inventories\'])\n        for sweep in range(passes):\n            improved = False\n            for actor in range(n):\n                winner = None\n                for _, offset, route, bundle_count in _proposals(best, actor, prices, proposals_per_actor):\n                    if simulations >= max_simulations:\n                        break\n                    trial = _clone_schedule(current)\n                    for i, command in enumerate(route, offset):\n                        if actor == 0:\n                            trial[i][\'farmer\'] = command\n                        else:\n                            trial[i].setdefault(\'hands\', [])\n                            while len(trial[i][\'hands\']) < n - 1:\n                                trial[i][\'hands\'].append([\'PASS\'])\n                            trial[i][\'hands\'][actor - 1] = command\n                    evaluated = simulate(obs, config, trial)\n                    simulations += 1\n                    score = _value(evaluated, prices)\n                    if score > best_value and dominates(evaluated, baseline):\n                        required = {(tuple(e[\'xy\']), e[\'op\'], e[\'actor\']): e[\'acquired\'] for e in best[\'events\'] if \'acquired\' in e and e[\'actor\'] != actor}\n                        acquired = {}\n                        for e in evaluated[\'events\']:\n                            if \'acquired\' in e:\n                                key = (tuple(e[\'xy\']), e[\'op\'], e[\'actor\'])\n                                dst = acquired.setdefault(key, {})\n                                for item, amount in e[\'acquired\'].items():\n                                    dst[item] = dst.get(item, 0) + amount\n                        if all((_ge(acquired.get(k, {}), v) for k, v in required.items())):\n                            winner, best_value = ((trial, offset, bundle_count), score)\n                if winner:\n                    current, offset, bundle_count = winner\n                    best = simulate(obs, config, current, detailed=True)\n                    changes.append({\'pass\': sweep, \'actor\': actor, \'from_step\': START + offset, \'resource_bundles\': bundle_count, \'estimated_stock_value\': best_value})\n                    improved = True\n                if simulations >= max_simulations:\n                    break\n            if not improved or simulations >= max_simulations:\n                break\n        if not changes or best_value <= baseline_value:\n            return {**fallback, \'reason\': \'no positive physical delivery gain\', \'simulations\': simulations, \'changed_workers\': [], \'changes\': [], \'certificate\': {\'stock_value_gain_at_initial_prices\': 0, \'sold_unit_delta\': dict.fromkeys(PRODUCTS, 0)}, \'planning_ms\': (perf_counter() - begun) * 1000}\n        final = simulate(obs, config, current, final_liquidate=True, detailed=True)\n        physical = simulate(obs, config, current)\n        if not dominates(physical, baseline):\n            raise Unsupported(\'no zero-overflow dominating continuation\')\n        delta = {item: final[\'sold\'].get(item, 0) - baseline[\'sold\'].get(item, 0) for item in PRODUCTS}\n        deposited_gain = any((final[\'rows\'][-1][\'deposited_by_actor\'][actor].get(item, 0) > baseline[\'rows\'][-1][\'deposited_by_actor\'][actor].get(item, 0) for actor in range(n) for item in PRODUCTS))\n        worker_change = any((_commands(new, n) != _commands(old, n) for new, old in zip(final[\'actions\'], baseline[\'actions\'])))\n        accepted = worker_change and deposited_gain and any((v > 0 for v in delta.values())) and all((v >= 0 for v in delta.values()))\n        plan = {\'accepted\': accepted, \'reason\': \'joint physical dominance\' if accepted else \'no improvement\', \'baseline\': _clone_schedule(baseline_remaining), \'actions\': final[\'actions\'], \'expected_states\': final[\'states\'][:-1], \'simulations\': simulations, \'changes\': changes, \'abandoned\': False, \'changed_workers\': sorted({c[\'actor\'] for c in changes}), \'certificate\': {\'baseline_rows\': baseline[\'rows\'], \'physical_rows\': physical[\'rows\'], \'baseline_overflow\': baseline[\'overflow_units\'], \'candidate_overflow\': final[\'overflow_units\'], \'sold_unit_delta\': delta, \'stock_value_gain_at_initial_prices\': best_value - baseline_value, \'baseline_final_shed\': baseline[\'private\'][\'shed\'], \'final_shed\': final[\'private\'][\'shed\'], \'positive_physical_deposit_gain\': deposited_gain, \'markets_712_717_unchanged\': all((final[\'actions\'][i].get(\'market\', []) == baseline_remaining[i].get(\'market\', []) for i in range(FINAL - START)))}}\n    except (Unsupported, KeyError, TypeError, ValueError, IndexError) as exc:\n        plan = {**fallback, \'reason\': str(exc)}\n    plan[\'planning_ms\'] = (perf_counter() - begun) * 1000\n    return plan\n\ndef _effective_action(action, n):\n    return (_commands(action, n), action.get(\'market\', []))\n\ndef _recover_observed(obs, config, parent_action, plan):\n    """Bounded cargo salvage after deviation; never resume old positional commands."""\n    farm, private = physical_state(obs)\n    positions = [farm[\'farmer\'], *farm[\'hands\']]\n    remaining = FINAL - int(_get(obs, \'step\')) + 1\n    room = max(0, int(_get(config, \'shedCapacity\', 100)) - sum(private[\'shed\'].values()))\n    commands = []\n    problems = []\n    prices = _get(obs, \'market\', {}).get(\'prices\', {})\n    for actor, (pos, inv) in enumerate(zip(positions, private[\'inventories\'])):\n        command = [\'PASS\']\n        if any((v > 0 for v in inv.values())):\n            route = _return(pos)\n            if len(route) > remaining:\n                problems.append({\'actor\': actor, \'reason\': \'unreachable cargo\'})\n            elif len(route) > 1:\n                command = route[0]\n            elif sum((max(0, q) for q in inv.values())) <= room:\n                command = [\'DROP\']\n                room -= sum((max(0, q) for q in inv.values()))\n            else:\n                items = [item for item in PRODUCTS if inv.get(item, 0) > 0]\n                if room and items:\n                    item = max(items, key=lambda i: (prices.get(i, 1) * min(inv[i], room), -PRODUCTS.index(i)))\n                    quantity = min(inv[item], room)\n                    command = [\'PLACE\', item, quantity]\n                    room -= quantity\n                else:\n                    problems.append({\'actor\': actor, \'reason\': \'no shed capacity\'})\n        commands.append(command)\n    action = {\'farmer\': commands[0], \'hands\': commands[1:], \'market\': deepcopy(parent_action.get(\'market\', []))}\n    if int(_get(obs, \'step\')) == FINAL:\n        action[\'market\'] = []\n        action = simulate(obs, config, [action], final_liquidate=True, preserve_final_commands=True)[\'actions\'][0]\n    plan[\'recovery_steps\'] = plan.get(\'recovery_steps\', 0) + 1\n    if problems:\n        plan.setdefault(\'recovery_failures\', []).append({\'step\': int(_get(obs, \'step\')), \'problems\': problems})\n    return action\n\ndef terminal_action(obs, config, parent_action, plan):\n    """Canonical guard, pre-deviation abstention, observed recovery after deviation."""\n    step = int(_get(obs, \'step\', -1))\n    if not plan or not plan.get(\'accepted\') or (not START <= step <= FINAL):\n        return parent_action\n    if plan.get(\'abandoned\'):\n        return _recover_observed(obs, config, parent_action, plan) if plan.get(\'deviated\') else parent_action\n    index = step - START\n    n = 1 + len(physical_state(obs)[0][\'hands\'])\n    mismatch = physical_state(obs) != plan[\'expected_states\'][index] or _effective_action(parent_action, n) != _effective_action(plan[\'baseline\'][index], n)\n    if mismatch:\n        plan[\'abandoned\'] = True\n        plan[\'abandon_step\'] = step\n        plan[\'reason\'] = \'physical observation or effective baseline action diverged\'\n        plan[\'safety_failure\'] = True\n        return _recover_observed(obs, config, parent_action, plan) if plan.get(\'deviated\') else parent_action\n    result = deepcopy(plan[\'actions\'][index])\n    if step == FINAL:\n        farm, private = physical_state(obs)\n        result = shop_liquidation(farm, private, _get(obs, \'market\')[\'prices\'])\n    if _commands(result, n) != _commands(parent_action, n):\n        plan[\'deviated\'] = True\n    return result',_PLANNER_NS)
# EXP-154 integration by Ahmed Berat Ozer, derived from Dmitrii Gluzdov E182.
# The preserved v27 parent is simulated on a private shadow only at step 712.
_PRE_TERMINAL_AGENT=agent
del agent
_TERMINAL_PLANS={}
_TERMINAL_PREVIOUS={}
_UPGRADE_STATS={'planning_calls':0,'accepted':0,'changed_steps':0,'aborted':0,'shadow_declines':0,'errors':0,'max_planning_ms':0.0}

def _parent_liquidate(farm, private, prices):
    # Exactly v27's final projected DROP ordering, in the planner's private state.
    view=_View({'player':0,'farms':[farm],'private':private,'market':{'prices':prices}},0,_IMPL.chassis.cfg)
    commands=[['DROP'] if _shed_adjacent(pos,view.board) and view.inv(i) else ['PASS'] for i,pos in enumerate(view.positions)]
    action={'farmer':commands[0],'hands':commands[1:],'market':[]}
    stock=_IMPL.chassis._projected_shed(action,view)
    action['market']=[['SELL',item,stock.get(item,0)] for item in PRODUCTS if stock.get(item,0)>0]
    action['market'].sort(key=lambda o:-view.prices.get(o[1],0)*o[2])
    return action

_PLANNER_NS['shop_liquidation']=_parent_liquidate

def _shadow_terminal(obs,config):
    seat=int(obs['player']);chassis=_IMPL.chassis
    state=chassis.players.get(seat)
    if not state or state.get('last_step')!=711 or state.get('route')!=2:
        return None
    # No delayed weed/structure intervention may depend on an unmodeled future.
    if state.get('pending'):
        return None
    shadow=copy.copy(chassis);shadow.players=copy.deepcopy(chassis.players)
    shadow.diagnostics={k:0 for k in chassis.diagnostics}
    projected=copy.deepcopy(obs);baseline=[];states=[]
    for step in range(712,719):
        projected['step']=step;projected['day']=step//24;projected['hour']=step%24
        states.append(copy.deepcopy(shadow.players[seat]))
        action=shadow.act(projected,config)
        if step==718:
            action=_parent_liquidate(projected['farms'][seat],projected['private'],projected['market']['prices'])
        else:
            market=action.get('market',[])
            if len(market)!=9 or {o[1] for o in market}!=set(PRODUCTS) or any(o[0]!='SELL' or len(o)!=3 or type(o[2]) is not int or o[2]<100 for o in market):
                return None
        if any(shadow.diagnostics.values()):return None
        run=_PLANNER_NS['simulate'](projected,config,[action])
        if run['actions'][0]!=action:return None
        baseline.append(action)
        run['farm']['money']=projected['farms'][seat]['money']
        projected['farms'][seat]=run['farm'];projected['private']=run['private']
    return baseline,states

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);seat=int(observation['player'])
    except Exception:
        return _PRE_TERMINAL_AGENT(observation,configuration)
    previous=_TERMINAL_PREVIOUS.get(seat)
    if step==0 or (previous is not None and step<=previous):_TERMINAL_PLANS.pop(seat,None)
    _TERMINAL_PREVIOUS[seat]=step
    plan=_TERMINAL_PLANS.get(seat)
    if plan and plan.get('accepted') and 712<=step<=718:
        if previous!=step-1:plan.update(abandoned=True,reason='nonconsecutive callback')
        try:
            result=_PLANNER_NS['terminal_action'](observation,configuration,plan['baseline'][step-712],plan)
            if plan.get('abandoned'):
                if not plan.get('abort_counted'):
                    plan['abort_counted']=True;_UPGRADE_STATS['aborted']+=1
                if not plan.get('deviated'):
                    _IMPL.chassis.players[seat]=copy.deepcopy(plan['parent_states_before'][step-712])
                    _TERMINAL_PLANS.pop(seat,None)
                    return _PRE_TERMINAL_AGENT(observation,configuration)
            _UPGRADE_STATS['changed_steps']+=int(result!=plan['baseline'][step-712])
            return result
        except Exception:
            _UPGRADE_STATS['errors']+=1
            if plan.get('deviated'):
                try:return _PLANNER_NS['_recover_observed'](observation,configuration,plan['baseline'][step-712],plan)
                except Exception:return _parent_liquidate(observation['farms'][seat],observation['private'],observation['market']['prices'])
    if step!=712:return _PRE_TERMINAL_AGENT(observation,configuration)
    _UPGRADE_STATS['planning_calls']+=1
    try:shadow=_shadow_terminal(observation,configuration)
    except (ValueError,KeyError,TypeError,IndexError):shadow=None
    if shadow is None:
        _UPGRADE_STATS['shadow_declines']+=1
        return _PRE_TERMINAL_AGENT(observation,configuration)
    baseline,states=shadow
    actual=_PRE_TERMINAL_AGENT(observation,configuration)
    if actual!=baseline[0]:
        _UPGRADE_STATS['shadow_declines']+=1;return actual
    try:
        plan=_PLANNER_NS['plan_terminal'](observation,configuration,baseline,max_simulations=64,passes=1,proposals_per_actor=4)
        _UPGRADE_STATS['max_planning_ms']=max(_UPGRADE_STATS['max_planning_ms'],plan.get('planning_ms',0.0))
        if not plan.get('accepted'):return actual
        plan['parent_states_before']=states;_TERMINAL_PLANS[seat]=plan
        _UPGRADE_STATS['accepted']+=1
        result=_PLANNER_NS['terminal_action'](observation,configuration,actual,plan)
        _UPGRADE_STATS['changed_steps']+=int(result!=actual)
        return result
    except Exception:
        _UPGRADE_STATS['errors']+=1;return actual

agent.telemetry=_UPGRADE_STATS

# EXP-154: aurax7 Reactive v2 day-end storage guard, adapted to our v27 view.
_PRE_ROOM_AGENT=agent
del agent
_ROOM_STATS={'changed_turns':0,'added_units':0,'errors':0}
def agent(observation,configuration=None):
    action=_PRE_ROOM_AGENT(observation,configuration)
    try:
        step=_step_of(observation)
        if step%24!=23:return action
        view=_View(observation,_int(_get(observation,'player',0)),_IMPL.chassis.cfg)
        carried=sum(max(0,int(n)) for inv in view.invs for n in inv.values())
        needed=sum(view.shed.values())+carried-99
        if needed<=0:return action
        planned={}
        for o in action.get('market',[]):
            if o and o[0]=='SELL' and len(o)>=3:planned[o[1]]=planned.get(o[1],0)+max(0,int(o[2]))
        result=copy.deepcopy(action);added=0
        for item in sorted(PRODUCTS,key=lambda it:-int(view.prices.get(it,0))):
            qty=min(needed,max(0,view.shed.get(item,0)-planned.get(item,0)))
            if qty<=0:continue
            if len(result['market'])>=10:break
            result['market'].append(['SELL',item,qty]);needed-=qty;added+=qty
            if needed<=0:break
        if added:_ROOM_STATS['changed_turns']+=1;_ROOM_STATS['added_units']+=added
        return result
    except Exception:
        _ROOM_STATS['errors']+=1;return action

agent.telemetry=_ROOM_STATS

# Incorporated upstream attribution and change notice:
# E182 Shop0909 + terminal physical closure (modified 2026-09-09)
# 
# The active public parent is Yusuke Hayashi's yhay81/shop-router-0909 v3.
# router_parent.py and actions.json are exact original bytes, not newly authored
# routes. The parent credits aurax7's Reactive Router for sale timing and shed
# projection; that attribution remains in router_parent.py. Original payload
# LICENSE.txt is preserved unchanged (Apache License 2.0 text); it contains no
# named copyright grantor and no separate NOTICE was supplied. No additional
# ownership, endorsement, or upstream replay-data rights claim is made.
# 
# Local changes: separate main.py/policy.py adapter; bounded start712 planner
# copied from frozen E180/S78 and modified for seven callbacks, exact Shop final
# liquidation, strict positive physical delivery/sale gain, and observation guards.
# unit_model.py is an unchanged frozen E180 copy of Kaggle's extracted semantics.
# The following original E180 notice is retained verbatim for attribution history.
# Its references to Thomas files describe E180, not files supplied in this Shop
# package: no Thomas tapes, trees or policy are included here.
# 
# ----- Original E180 notice -----
# Kaggriculture: Last-Mile Harvest Planner
# Attribution and change notice
# 
# Thomas Tschinkel is the author of the parent public state-router policy and its
# published decision trees and action-route data. Source: Kaggriculture: 93.8% Win
# Rate Public State Router, notebook version 3, scriptVersionId 347936183:
# https://www.kaggle.com/code/thomastschinkel/kaggriculture-93-8-win-rate-public-state-router?scriptVersionId=347936183
# The public notebook identifies its license as Apache License, Version 2.0.
# Original published main.py SHA-256:
# b87a27ed614a33329be85f1b662e51cf4078a019fee937afcebbbbf2f51f8522
# 
# Changes to that source for this distribution: compressed route/tree literals
# were decoded into readable tapes.json and trees.json; a read-only planned_action
# helper was added; descriptive headers and local data loading were adapted.
# The original parent feature extraction, tree traversal and agent behavior are
# retained. These public routes are not claimed as newly authored or trained by
# the notebook distributor.
# 
# unit_model.py contains deterministic unit-action and crop-decay definitions
# extracted from Kaggle's kaggle-environments 1.32.7 Kaggriculture engine, licensed
# under Apache License, Version 2.0. Credit: Kaggle and the kaggle-environments
# contributors. Project: https://github.com/Kaggle/kaggle-environments
# Source file: kaggle_environments/envs/kaggriculture/kaggriculture.py
# Source SHA-256:
# bc8a54879ef02c7ea64b8b333d6a976f0ea65c4949149d01f463f23bccee653e
# The extracted unit/decay definitions are not a newly authored game engine;
# market price dynamics and the full interpreter are not part of this module.
# 
# Additional work in this distribution: a bounded last-nine-action collection
# and delivery planner, observation guards and recovery, a settings-consuming
# factory and entry point, standalone examples, and deterministic packaging.
# The full Apache License, Version 2.0 is included as LICENSE.txt.
# No endorsement by Thomas Tschinkel or Kaggle is implied.
# 
# Data provenance limitation: Thomas's source refers to public replay data and
# an upstream provenance.json. That original episode-level manifest, replay IDs
# and individual replay-author identities were not supplied with the public
# notebook/output used here. No names or episode lineage have been invented.
# Notebook-level licensing does not independently establish the missing underlying
# replay-data rights chain. The package supplies usable readable routes, not a
# reproducible reconstruction of their original collection or training process.
# 
# Packaging note: source inputs described as byte-exact above are
# normalized to UTF-8/LF text with a final newline in this standalone
# notebook package. Route JSON values and parent policy behavior are unchanged.

# Final public-entry guard; measured separately and compared on captured observations.
_V28_CORE=agent
del agent
_IMPL.chassis.diagnostics['v28_entry_errors']=0
def agent(observation,configuration=None):
    try:
        return _V28_CORE(observation,configuration)
    except Exception:
        _IMPL.chassis.diagnostics['v28_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_ROOM_STATS

# EXP-155: prvsiyan V221B finite tomato investment, adapted by Ahmed Berat Ozer.
# Original public source is retained under research24/public; Apache-2.0.
MAX_ORDERS=10
class FarmView(_View):
    def __init__(self,obs):super().__init__(obs,int(obs['player']),_IMPL.chassis.cfg)
    def inventory(self,actor):return self.inv(actor)
def projected_shed(action,view):return _IMPL.chassis._projected_shed(action,view)

CROP_MIN_PRICE=70

# V219: a finite late tomato investment with dedicated, observed workers.
_V219_PARENT = agent
del agent
_V219_FERTILIZE = True  # Builder changes only this flag for the ablation.
_V219_STATES = {}
_V219_REPORT = {'commitments': 0, 'hire_requests': 0, 'confirmed_workers': 0,
                'hire_shortfalls': 0, 'plant_requests': 0, 'confirmed_plants': 0,
                'water_requests': 0, 'fertilize_requests': 0, 'harvest_requests': 0,
                'confirmed_harvest_units': 0, 'drop_requests': 0,
                'tomato_sale_requests': 0, 'budget_declines': 0, 'lost_plants': 0}


def _v219_fib(n):
    a, b = 1, 1
    for _ in range(n): a, b = b, a+b
    return a


def _v219_native_day(native, day):
    tape = _IMPL.chassis.routes[native['route']]
    return tape[day*24:min((day+1)*24,719)]


def _v219_qualifies(obs, native):
    farm=obs['farms'][obs['player']]
    if len(farm['tiles']) != 10 or set(farm['unlocked_quadrants']) != {'NW','NE','SW'}:
        return False
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    if sum(s in ('PIZZA_SHOP','FARMERS_MARKET') for s in obs['town']['unlocked_shops']) < 3:
        return False
    if any(farm['tiles'][y][x] != 'LOCKED' for y in (5,6) for x in range(5,10)):
        return False
    if obs['private']['seeds'].get('TOMATO',0) or obs['private']['shed'].get('TOMATO',0):
        return False
    if any(isinstance(t,dict) and t.get('crop')=='TOMATO' for row in farm['tiles'] for t in row):
        return False
    # The investment uses spare land and new worker indices. Avoid taking over
    # any native tomato or land purchase obligation on the known own schedule.
    for tape in _IMPL.chassis.routes.values():
        for a in tape[432:719]:
            if any(o and o[0]=='BUY_LAND' for o in a.get('market',[])):return False
            if any(c==['PLANT','TOMATO'] for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True


def _v219_walk(pos, target):
    x,y=pos;tx,ty=target
    if x != tx:return ['EAST' if x < tx else 'WEST']
    if y != ty:return ['SOUTH' if y < ty else 'NORTH']
    return None


def _v219_home(pos):
    return min(((4,4),(5,4),(4,5),(5,5)),key=lambda p:abs(pos[0]-p[0])+abs(pos[1]-p[1]))


def _v219_request(obs, action, state, native):
    step=int(obs['step']);day=step//24;offset=step%24
    farm=obs['farms'][obs['player']];private=obs['private']
    # If the planting-day transaction could not complete, abandon investment.
    # Later purchases would miss the finite day26..29 production window.
    if not state.get('committed') and day!=18:return action
    if state.get('requested_day')==day or offset>3:return action
    planned=_v219_native_day(native,day)
    remaining=planned[offset+1:]
    if any(o and o[0]=='HIRE' for a in remaining for o in a.get('market',[])):
        return action
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in action['market'])
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires != expected:return action
    fertilizer=bool(_V219_FERTILIZE and day in (24,27) and obs['market']['prices']['FERTILIZER']<=30)
    # One watering tour: at most 2 entry moves + 9 between tiles + 10 waters.
    # A hire request by hour2 leaves at least21 callbacks after confirmation.
    crop_workers=1 if day in (19,20,21,22,23,25) and offset<=2 else (3 if 26<=day<=28 else 2)
    labor=_r53_labor_assignment(obs,action,fertilizer)
    if labor is not None:crop_workers=labor['workers']
    count=crop_workers+int(fertilizer and day==27 and labor is None)
    extra=[]
    if not state.get('committed'):
        extra += [['BUY_LAND'],['BUY_SEED','TOMATO',10]]
    if fertilizer:extra.append(['BUY_PRODUCT','FERTILIZER',10])
    extra += [['HIRE'] for _ in range(count)]
    if len(action['market'])+len(extra)>MAX_ORDERS:return action
    # No assumed sale proceeds. Reserve 3,000 for parent obligations and price
    # movement; the qualification separately requires 12,000 initial liquidity.
    budget=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+count))
    if not state.get('committed'):budget+=4500
    if fertilizer:budget+=10*(obs['market']['prices']['FERTILIZER']+5)
    for order in action['market']:
        if not order:continue
        if order[0]=='BUY_PRODUCT':budget+=int(order[2])*(int(obs['market']['prices'][order[1]])+10)
        elif order[0]=='BUY_ANIMAL':budget+=int(order[2])*{'COW':400,'SHEEP':500,'GOOSE':300}[order[1]]
        elif order[0]=='BUY_SEED':budget+=int(order[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
    if farm['money']<budget+3000:
        _V219_REPORT['budget_declines']+=1;return action
    state['pending']={'step':step,'first_actor':expected+1,'count':count,'crop_workers':crop_workers,'fertilizer':fertilizer,'labor':labor}
    if labor is not None:
        _R53_LABOR_REPORT['labor_requests']+=1;_R53_LABOR_REPORT['labor_hires_avoided']+=1;_R53_LABOR_REPORT['labor_day'+str(day)]+=1
    state['requested_day']=day
    _V219_REPORT['hire_requests']+=count
    if not state.get('committed'):
        state['committed']=True;_V219_REPORT['commitments']+=1
    changed=copy.deepcopy(action);changed['market']+=extra
    return changed


def _v219_worker(obs, state, actor, role):
    day=int(obs['step'])//24;step=int(obs['step']);view=FarmView(obs)
    pos=tuple(view.positions[actor]);inv=view.inventory(actor)
    targets=role['targets']
    # Actual cargo differences, observed on the next callback, verify harvests.
    previous=state['last_work'].get(actor)
    if previous and previous['step']==step-1 and previous['command']==['HARVEST']:
        _V219_REPORT['confirmed_harvest_units']+=max(0,int(inv.get('TOMATO',0))-previous['tomatoes'])
    if role.get('needs_fertilizer') and not role.get('loaded'):
        home=_v219_home(pos)
        walk=_v219_walk(pos,home)
        if walk:return walk
        desired=role.get('fertilizer_quantity',10 if role['kind']=='fertilizer' else 5)
        if inv.get('FERTILIZER',0)>=desired:role['loaded']=True
        elif role.get('pickup_requested'):
            # Never spend repeated turns waiting for stock that was not bought.
            role['loaded']=True;role['fertilizer_available']=int(inv.get('FERTILIZER',0))
        elif view.shed.get('FERTILIZER',0)>=desired:
            role['pickup_requested']=True;return ['PICKUP','FERTILIZER',desired]
        else:role['loaded']=True
    todo=[]
    for target in targets:
        x,y=target;tile=view.tiles[y][x]
        tomato=isinstance(tile,dict) and tile.get('crop')=='TOMATO'
        if tomato and target not in state['seen_plants']:
            state['seen_plants'].add(target);_V219_REPORT['confirmed_plants']+=1
        if target in state['seen_plants'] and not tomato and target not in state['lost']:
            state['lost'].add(target);_V219_REPORT['lost_plants']+=1
        command=None
        if role['kind']=='fertilizer':
            if tomato and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
        elif day==18 and not tomato:
            if tile is None and obs['private']['seeds'].get('TOMATO',0)>0:command=['PLANT','TOMATO']
            elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif tomato:
            # No later production follows the final day, so watering then would
            # consume time needed to harvest and deliver the final cargo.
            if day<29 and not tile.get('watered_today'):command=['WATER']
            elif role.get('needs_fertilizer') and tile.get('fertilized_until_day',-1)<day+2 and inv.get('FERTILIZER',0)>0:
                command=['FERTILIZE']
            elif tile.get('yield_units',0)>0:command=['HARVEST']
        if command:todo.append((target,command))
    # Final return has priority once only the exact distance plus DROP remains.
    home=_v219_home(pos);distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    if step>=718-distance and inv.get('TOMATO',0):
        return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv.get('TOMATO',0))]
    if todo:
        target,command=min(todo,key=lambda v:(abs(pos[0]-v[0][0])+abs(pos[1]-v[0][1]),targets.index(v[0])))
        return _v219_walk(pos,target) or command
    if inv.get('TOMATO',0):return _v219_walk(pos,home) or ['PLACE','TOMATO',int(inv['TOMATO'])]
    if any(inv.values()):return _v219_walk(pos,home) or ['DROP']
    return ['PASS']


def agent(observation, configuration=None):
    action=_V219_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V219_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'last_work':{},'seen_plants':set(),'lost':set(),
               'targets':[(x,y) for y in (5,6) for x in range(5,10)]}
        _V219_STATES[player]=state
    state['last_step']=step
    native=_IMPL.chassis.players[player]
    if step==432:state['eligible']=_v219_qualifies(observation,native)
    if not state.get('eligible') or day<18:return action
    if state['day']!=day:
        state['day']=day;state['workers']={};state['last_work']={}
    farm=observation['farms'][player]
    pending=state.pop('pending',None)
    if pending:
        if len(farm['hands'])+1 >= pending['first_actor']+pending['count'] and 'SE' in farm['unlocked_quadrants']:
            for index in range(pending['count']):
                fertilizer_worker=index==pending['crop_workers']
                if fertilizer_worker:targets=state['targets']
                elif pending['crop_workers']==1:targets=state['targets']
                elif pending['crop_workers']==2:targets=state['targets'][index*5:index*5+5]
                else:targets=[[(5,5),(6,5),(7,5)],[(8,5),(9,5),(9,6),(8,6)],[(5,6),(6,6),(7,6)]][index]
                state['workers'][pending['first_actor']+index]={'kind':'fertilizer' if fertilizer_worker else 'crop','targets':targets,
                    'needs_fertilizer':pending['fertilizer'] and (day==24 or fertilizer_worker)}
                if pending.get('labor') is not None:
                    role=state['workers'][pending['first_actor']+index]
                    role['targets']=[tuple(p) for p in pending['labor']['paths'][index]]
                    role['needs_fertilizer']=pending['labor']['fertilizer'];role['fertilizer_quantity']=len(role['targets'])
                    if tuple(farm['hands'][pending['first_actor']+index-1])!=tuple(pending['labor']['spawns'][index]):_R53_LABOR_REPORT['labor_spawn_errors']+=1
                    if index==0:_R53_LABOR_REPORT['labor_confirmed']+=1
            _V219_REPORT['confirmed_workers']+=pending['count']
        else:_V219_REPORT['hire_shortfalls']+=pending['count']
    action=_v219_request(observation,action,state,native)
    if state['workers']:
        commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
        commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
        for actor,role in state['workers'].items():
            if actor>=len(commands):continue
            command=_v219_worker(observation,state,actor,role)
            commands[actor]=command
            name={'PLANT':'plant_requests','WATER':'water_requests','FERTILIZE':'fertilize_requests',
                  'HARVEST':'harvest_requests','DROP':'drop_requests'}.get(command[0])
            if name:_V219_REPORT[name]+=1
            state['last_work'][actor]={'step':step,'command':command,'tomatoes':observation['private']['inventories'][actor].get('TOMATO',0)}
        action=copy.deepcopy(action);action['farmer'],action['hands']=commands[0],commands[1:]
    if state.get('committed') and len(action['market'])<MAX_ORDERS and not any(o[:2]==['SELL','TOMATO'] for o in action['market']):
        quantity=projected_shed(action,FarmView(observation)).get('TOMATO',0)
        if quantity>0:
            action=copy.deepcopy(action);action['market'].append(['SELL','TOMATO',quantity])
            _V219_REPORT['tomato_sale_requests']+=quantity
    return action


agent.telemetry=_V219_REPORT

# V221B: labor-only ablation of frozen V219G; not yet publicly scored.


# Crop workers own their final routes after commitment. A private parent shadow
# does not contain these obligations, so terminal rescue must abstain there.
_ORIGINAL_SHADOW_TERMINAL=_shadow_terminal
def _shadow_terminal(obs,config):
    if _V219_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _ORIGINAL_SHADOW_TERMINAL(obs,config)

APPLY_TIMING=False

_EXPERIMENT_PARENT=agent
del agent
_V219_REPORT['extra_fertilizer_days']=0
_V219_REPORT['reordered_market_turns']=0
_V219_REPORT['errors']=0
def agent(observation,configuration=None):
    try:
        action=_EXPERIMENT_PARENT(observation,configuration)
        if APPLY_TIMING and int(observation['step'])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT['errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

def _v224_sales_first(action):
    original=action.get('market',[])[:MAX_ORDERS]
    orders=[list(o) for o in original if o and (o[0] in ('HIRE','BUY_LAND') or (len(o)>=3 and int(o[2])>0))]
    for index in range(len(orders)):
        order=orders[index]
        if order[0]!='SELL':continue
        cursor=index
        while cursor>0:
            previous=orders[cursor-1]
            if previous[0]=='SELL':break
            if previous[0] in ('BUY_PRODUCT','BUY_ANIMAL') and previous[1]==order[1]:break
            orders[cursor-1],orders[cursor]=orders[cursor],orders[cursor-1]
            cursor-=1
    if orders==original:return action
    _V219_REPORT['reordered_market_turns']+=1
    changed=copy.deepcopy(action);changed['market']=orders
    return changed
_ORDER_PARENT=agent
del agent

def agent(observation,configuration=None):
    try:
        action=_ORDER_PARENT(observation,configuration)
        if int(observation["step"])>=144:action=_v224_sales_first(action)
        return action
    except Exception:
        _V219_REPORT["errors"]+=1
        return {"farmer":["PASS"],"hands":[],"market":[]}
agent.telemetry=_V219_REPORT

_V31_CORE=agent
del agent
_IMPL.chassis.diagnostics['production_errors']=0
_IMPL.chassis.diagnostics['v31_entry_errors']=0
def agent(observation,configuration=None):
    before=_V219_REPORT['errors']
    try:
        action=_V31_CORE(observation,configuration)
        _IMPL.chassis.diagnostics['production_errors']+=_V219_REPORT['errors']-before
        return action
    except Exception:
        _IMPL.chassis.diagnostics['v31_entry_errors']+=1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_V219_REPORT

# Apache-2.0; later cattle transfer from prvsiyan, Moon (2026-09-10).
# Bounded livestock substitution; confirm owned animals before redirecting workers.
_V231_PARENT=agent
_V231_CAP=4
_V231_STATES={}
_V231_REPORT={}

def _v231_new_state():
    return {'last':-1,'confirmed':0,'reserved':0,'pending_buy':None,
            'carrying':{},'pending_places':[],'sites':{},'milk_credit':0,
            'requested':0,'failed_purchase_units':0,'picked':0,'placed':0,
            'failed_placements':0,'extra_milk_harvested':0,'extra_milk_sale_requests':0}

def _v231_controller(obs,action,state,cap):
    step=int(obs['step']);seat=int(obs['player']);farm=obs['farms'][seat]
    private=obs['private'];shed=private['shed'];inventories=private['inventories']
    positions=[farm['farmer'],*farm['hands']]
    pending=state['pending_buy']
    if pending is not None:
        gained=max(0,int(shed.get('COW',0))-pending['before'])
        confirmed=min(pending['quantity'],gained)
        state['confirmed']+=confirmed;state['reserved']+=confirmed
        state['failed_purchase_units']+=pending['quantity']-confirmed
        state['pending_buy']=None
    for pending in state['pending_places']:
        x,y=pending['site'];tile=farm['tiles'][y][x]
        if (isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==pending['day']):
            state['sites'][(x,y)]=pending['day'];state['placed']+=1
            actor=pending['actor'];state['carrying'][actor]=max(0,state['carrying'].get(actor,0)-1)
        else:state['failed_placements']+=1
    state['pending_places']=[]
    state['last']=step
    result=copy.deepcopy(action)
    workers=[result.get('farmer') or ['PASS'],*(result.get('hands') or [])]
    seen_harvest=set();cow_available=int(shed.get('COW',0));occupied=set()
    for actor,work in enumerate(workers[:len(positions)]):
        inventory=inventories[actor] if actor<len(inventories) else {}
        x,y=positions[actor];tile=farm['tiles'][y][x];site=(x,y)
        if (work==['HARVEST'] and site in state['sites'] and site not in seen_harvest
                and isinstance(tile,dict) and tile.get('animal')=='COW'
                and tile.get('placed_day')==state['sites'][site]):
            units=max(0,int(tile.get('yield_units',0)))
            state['milk_credit']+=units;state['extra_milk_harvested']+=units
            seen_harvest.add(site)
        if len(work)>=2 and work[:2]==['PICKUP','SHEEP']:
            quantity=max(0,int(work[2]) if len(work)>2 else 1)
            center=len(farm['tiles'])//2
            if (quantity and state['reserved']>=quantity and cow_available>=quantity
                    and x in (center-1,center) and y in (center-1,center)
                    and not any(inventory.get(a,0) for a in ('COW','SHEEP','GOOSE'))):
                work[1]='COW';state['reserved']-=quantity;cow_available-=quantity
                state['carrying'][actor]=state['carrying'].get(actor,0)+quantity
                state['picked']+=quantity
        if (len(work)>=2 and work[:2]==['PLACE','SHEEP']
                and state['carrying'].get(actor,0)>0 and inventory.get('COW',0)>0
                and isinstance(tile,dict) and tile.get('kind')=='PASTURE'
                and 'animal' not in tile and site not in occupied):
            work[1]='COW'
            state['pending_places'].append({'actor':actor,'site':site,'day':step//24})
        if (len(work)>=2 and work[0]=='PLACE' and work[1] in ('COW','SHEEP','GOOSE')
                and inventory.get(work[1],0)>0):occupied.add(site)
    result['farmer'],result['hands']=workers[0],workers[1:]
    market=result.get('market',[])
    animal_orders=[o for o in market if len(o)>=3 and o[0]=='BUY_ANIMAL']
    shops=obs['town']['unlocked_shops'];prices=obs['market']['prices']
    counts={'COW':0,'SHEEP':0}
    for line in farm['tiles']:
        for tile in line:
            if isinstance(tile,dict) and tile.get('animal') in counts:counts[tile['animal']]+=1
    cargo=sum(int(inv.get(a,0)) for inv in inventories for a in ('COW','SHEEP','GOOSE'))
    stock_animals=sum(int(shed.get(a,0)) for a in ('COW','SHEEP','GOOSE'))
    milk_shops=sum(shop in ('PIZZA_SHOP','ICE_CREAM_SHOP','SMOOTHIE_SHOP') for shop in shops)
    if (216<=step<=227 and len(shops)>=3 and state['confirmed']<cap and not state['reserved']
            and not any(state['carrying'].values()) and not state['pending_places']
            and not cargo and not stock_animals and len(animal_orders)==1
            and animal_orders[0][1]=='SHEEP' and milk_shops>=2 and 'YARN_STORE' not in shops
            and int(prices.get('MILK',0))>=int(prices.get('WOOL',0))
            and counts['COW']>=4 and counts['SHEEP']>=2):
        order=animal_orders[0];quantity=int(order[2])
        if 1<=quantity<=2 and quantity<=cap-state['confirmed']:
            order[1]='COW';state['requested']+=quantity
            state['pending_buy']={'before':int(shed.get('COW',0)),'quantity':quantity}
    # Sell only additional physically harvested production at an existing sale slot.
    if state['milk_credit']>0:
        stock=projected_shed(result,FarmView(obs))
        total_planned=sum(max(0,int(o[2])) for o in market if len(o)>=3 and o[:2]==['SELL','MILK'])
        extra=min(state['milk_credit'],max(0,int(stock.get('MILK',0))-total_planned))
        if extra:
            for order in market:
                if len(order)>=3 and order[:2]==['SELL','MILK'] and int(order[2])>0:
                    order[2]=int(order[2])+extra
                    state['milk_credit']-=extra;state['extra_milk_sale_requests']+=extra
                    break
    result['market']=market
    return result

def agent(observation,configuration=None):
    step=int(observation['step']);seat=int(observation['player'])
    state=_V231_STATES.get(seat)
    if state is None or step<=state['last']:
        state=_V231_STATES[seat]=_v231_new_state()
    action=_V231_PARENT(observation,configuration)
    action=_v231_controller(observation,action,state,_V231_CAP)
    _V231_REPORT.clear();_V231_REPORT.update(_V231_PARENT.telemetry)
    for name in ('confirmed','reserved','requested','failed_purchase_units','picked','placed',
                 'failed_placements','extra_milk_harvested','extra_milk_sale_requests','milk_credit'):
        _V231_REPORT['cattle_'+name]=state[name]
    _V231_REPORT['cattle_carried_pending']=sum(state['carrying'].values())
    return action

agent.telemetry=_V231_REPORT


# EXP-167, adapted from Dmitrii Gluzdov's Two Coins, One Sheep (Apache-2.0).
# Reserve only physically available stock after the final parent worker actions.
_R36_SALE_PARENT=agent
_R36_NATIVE_LEAD=Chassis._sell_lead
_R36_NATIVE_SUPPRESS=Chassis._apply_suppression
_R36_SALE_REPORT={}

def _r36_native_lead(self,action,view,projected,route,step,next_sup):
    if step<288 or step>=696:
        return _R36_NATIVE_LEAD(self,action,view,projected,route,step,next_sup)

def _r36_suppress(action,state,step):
    _R36_NATIVE_SUPPRESS(action,state,step)
    due=state.get('r36_debts',{}).pop(step,{})
    for order in action.get('market',[]):
        if len(order)>=3 and order[0]=='SELL':
            removed=min(max(0,int(order[2])),due.get(order[1],0))
            order[2]-=removed
            due[order[1]]=due.get(order[1],0)-removed

Chassis._sell_lead=_r36_native_lead
Chassis._apply_suppression=staticmethod(_r36_suppress)

def _r36_reserve(obs,action):
    step=int(obs['step'])
    # The final planner forecasts its own parent, so keep its full window native.
    if not 288<=step<696:return action
    native=_IMPL.chassis.players[int(obs['player'])]
    tape=_IMPL.chassis.routes[native['route']]
    end=min(695,step+_R37_HORIZONS.get(int(obs['player']),2),(step//72+1)*72-1)
    if end<=step:return action
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    view=FarmView(obs)
    # This projection intentionally abstains on ambiguous animal depot returns.
    if any(len(c)>1 and c[0]=='PLACE' and c[1] in ANIMAL_STRUCTURE
           and view.inv(i).get(c[1],0)>0 for i,c in enumerate(commands[:len(view.positions)])):
        return action
    stock=projected_shed(action,view)
    market=action.get('market',[])
    blocked={o[1] for o in market if len(o)>1 and o[0] in ('SELL','BUY_PRODUCT')}
    blocked.update(c[1] for c in commands if len(c)>1 and c[0]=='PICKUP')
    blocked.update(c[1] for queue in native['pending'].values() for pos,c in queue
                   if len(c)>1 and c[0]=='PICKUP')
    debts=native['sell_state'].setdefault('r36_debts',{})
    for item in PRODUCTS:
        if item in ('WHEAT','FERTILIZER') or item in blocked or view.prices.get(item,0)<2:continue
        available=max(0,int(stock.get(item,0)))
        if not available or len(market)>=10:continue
        reservations=[]
        for due_step in range(step+1,end+1):
            future=tape[due_step]
            work=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
            if any(len(c)>1 and c[:2]==['PICKUP',item] for c in work):break
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT',item] for o in future.get('market',[])):break
            planned=sum(max(0,int(o[2])) for o in future.get('market',[]) if len(o)>=3 and o[:2]==['SELL',item])
            amount=min(available,max(0,planned-debts.get(due_step,{}).get(item,0)))
            if amount:
                reservations.append((due_step,amount));available-=amount
            if not available:break
        qty=sum(q for _,q in reservations)
        if qty:
            market.append(['SELL',item,qty])
            for due,q in reservations:
                debt=debts.setdefault(due,{})
                debt[item]=debt.get(item,0)+q
            _R36_SALE_REPORT['sale_reserved_units']+=qty
            _R36_SALE_REPORT['sale_reservations']+=1
    return action

def agent(observation,configuration=None):
    if int(observation.get('step',0))==0:
        _R36_SALE_REPORT.update(sale_reserved_units=0,sale_reservations=0,sale_errors=0)
    action=_R36_SALE_PARENT(observation,configuration)
    try:
        if configuration is None or all(configuration.get(k,v)==v for k,v in
            [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r36_reserve(observation,action)
            if int(observation['step'])>=288:action=_v224_sales_first(action)
    except Exception:
        _R36_SALE_REPORT['sale_errors']=_R36_SALE_REPORT.get('sale_errors',0)+1
    _R36_SALE_REPORT.update(_R36_SALE_PARENT.telemetry)
    return action

agent.telemetry=_R36_SALE_REPORT

# Ensure the Kaggle-selected final callable is the exported policy.
agent = globals().pop("agent")


# Public capability transfer: lucifer19; Flexon is the same Two Coins asset set.
# Apache-2.0; exact functions from Kaggle kaggle-environments 1.32.7.
# https://github.com/Kaggle/kaggle-environments/tree/master/kaggle_environments/envs/kaggriculture
import math
_R37_MARKET_PARAMS = {'WHEAT': {'base': 25, 'I0': 10000, 'T': 400, 'below_func': 'sqrt', 'below_target': 0.8, 'above_func': 'log', 'above_target': 0.2}, 'CARROT': {'base': 35, 'I0': 10000, 'T': 450, 'below_func': 'hinge', 'below_target': 1.0, 'above_func': 'sqrt', 'above_target': 0.7}, 'TOMATO': {'base': 60, 'I0': 10000, 'T': 200, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'sqrt', 'above_target': 0.6}, 'STRAWBERRY': {'base': 120, 'I0': 10000, 'T': 100, 'below_func': 'sqrt', 'below_target': 0.7, 'above_func': 'linear', 'above_target': 1.6}, 'MELON': {'base': 250, 'I0': 10000, 'T': 300, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.6}, 'EGG': {'base': 50, 'I0': 10000, 'T': 332, 'below_func': 'hinge', 'below_target': 0.4, 'above_func': 'log', 'above_target': 0.2}, 'MILK': {'base': 160, 'I0': 10000, 'T': 122, 'below_func': 'sqrt', 'below_target': 0.6, 'above_func': 'linear', 'above_target': 1.6}, 'WOOL': {'base': 200, 'I0': 10000, 'T': 105, 'below_func': 'log', 'below_target': 0.2, 'above_func': 'sq', 'above_target': 3.2}, 'FERTILIZER': {'base': 100, 'I0': 10000, 'T': 200, 'below_func': 'linear', 'below_target': 0.4, 'above_func': 'linear', 'above_target': 0.4}}
_R37_PRICE_FLOOR = 1
_R37_HINGE_GAIN = 8.0
def _r37_shape(func, x, T=None):
    x = max(0.0, x)
    if func == "linear": return x
    if func == "sq":     return x * x
    if func == "sqrt":   return math.sqrt(x)
    if func == "log":    return math.log(1.0 + x)
    if func == "log10":  return math.log10(1.0 + x)
    if func == "hinge":
        # Degenerates to linear if T is missing or non-positive.
        if not T or T <= 0:
            return x
        u = x / T
        return u + _R37_HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x

def _r37_market_price(item, inventory, params=None):
    """Floor at _R37_PRICE_FLOOR."""
    p = (params or _R37_MARKET_PARAMS)[item]
    base = p["base"]
    I0 = p["I0"]
    T = p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _r37_shape(f, T, T)
        price = base + amp * _r37_shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _r37_shape(f, T, T)
        price = base - amp * _r37_shape(f, inventory - I0, T)
    return max(_R37_PRICE_FLOOR, int(round(price)))

def _r37_similarity(observation):
    """Empty tiles cannot make two unrelated production layouts look alike."""
    farms = observation['farms']
    own, rival = farms[observation['player']], farms[1-observation['player']]
    if own['unlocked_quadrants'] != rival['unlocked_quadrants']:
        return 0.0
    matches = total = 0
    for a, b in zip([t for row in own['tiles'] for t in row],
                    [t for row in rival['tiles'] for t in row]):
        sa = (a.get('crop'), a.get('animal')) if isinstance(a, dict) else (None, None)
        sb = (b.get('crop'), b.get('animal')) if isinstance(b, dict) else (None, None)
        if sa != (None, None) or sb != (None, None):
            total += 1
            matches += sa == sb
    return matches / total if total >= 8 else 0.0


def _r37_quote_priority(observation, order, stock):
    """Revenue exposed to a small rival batch, not nominal headline revenue."""
    item = order[1]
    quantity = min(max(0, int(order[2])), stock.get(item, 0))
    if not quantity or item not in _R37_MARKET_PARAMS:
        return 0.0
    inventory = observation['market']['inventory'][item]
    params = {k: dict(v) for k, v in _R37_MARKET_PARAMS.items()}
    for k, patch in observation['market'].get('params', {}).items():
        if k in params:
            params[k].update(patch)
    rival = observation['farms'][1-observation['player']]
    crop_item = item if item in ('WHEAT','CARROT','TOMATO','STRAWBERRY','MELON') else None
    animal = {'EGG':'GOOSE','MILK':'COW','WOOL':'SHEEP'}.get(item)
    standing = sum(max(0, int(t.get('yield_units', 0))) for row in rival['tiles'] for t in row
                   if isinstance(t, dict) and
                   ((crop_item is not None and t.get('crop') == crop_item) or
                    (animal is not None and t.get('animal') == animal)))
    # Public fields do not reveal the rival shed. Eight units are a scenario,
    # not a recovered hidden quantity; visible ripe yield increases the stress.
    batch = min(24, max(8, standing))
    now = sum(_r37_market_price(item, inventory+j, params) for j in range(quantity))
    later = sum(_r37_market_price(item, inventory+batch+j, params) for j in range(quantity))
    return now-later


def _r37_reorder_sales(observation, action):
    """Keep quantities and purchase barriers; rank distinct contiguous sales."""
    stock = projected_shed(action, FarmView(observation))
    orders = [list(o) for o in action['market']]
    start = 0
    while start < len(orders):
        if orders[start][0] != 'SELL':
            start += 1
            continue
        end = start
        while end < len(orders) and orders[end][0] == 'SELL':
            end += 1
        block = orders[start:end]
        if len({o[1] for o in block}) == len(block):
            orders[start:end] = sorted(block, key=lambda o: _r37_quote_priority(observation, o, stock), reverse=True)
        start = end
    if orders != action['market']:
        _R37_STATS['quote_reordered_turns'] += 1
        action = dict(action, market=orders)
    return action



# EXP175: bounded public cash-response probe inspired by leoprovorov,
# Two Coins Mirror Counter v1 (Apache-2.0). No hidden rival inventory.
_R44_PROBES={}
_R44_REPORT=dict(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)

def _r44_before(obs):
    player=int(obs['player']);step=int(obs['step'])
    st=_R44_PROBES.get(player)
    if st is None or step<=st['step']:
        st=_R44_PROBES[player]={'step':-1,'money':None,'probe':0,'matched':False}
    if step==0:_R44_REPORT.update(probe_matches=0,probe_four_turn_calls=0,probe_errors=0)
    money=tuple(float(obs['farms'][i]['money']) for i in (player,1-player))
    if st['money'] is not None and st['probe']>=100 and _r37_similarity(obs)>=.90:
        own=money[0]-st['money'][0];rival=money[1]-st['money'][1]
        if own>0 and rival>0 and abs(own-rival)<=max(5.0,.05*st['probe']):
            if not st['matched']:_R44_REPORT['probe_matches']+=1
            st['matched']=True
    st.update(step=step,money=money,probe=0)
    return st

def _r44_after(obs,action,st):
    step=int(obs['step']);player=int(obs['player'])
    if not 336<=step<648 or st['matched']:return
    # Positive all-sale probes avoid mistaking equal spending for preemption.
    if not action['market'] or any(o and o[0]!='SELL' for o in action['market']):return
    debts=_IMPL.chassis.players[player]['sell_state'].get('r36_debts',{})
    own=debts.get(step+3,{})
    if own:st['probe']=sum(max(0,int(n))*int(obs['market']['prices'].get(item,0)) for item,n in own.items())

_R37_ADAPTIVE = True
_R37_QUOTE = True
# EXP-168: adapted from lucifer19 / Harvest Nocturne, Apache-2.0.
# All rivalry features use public occupied tiles; no private rival inventory.
_R37_PARENT = agent
_R37_PLAYERS = {}
_R37_HORIZONS = {}
_R37_REPORT = {}
_R37_STATS = dict(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
del agent

def agent(observation, configuration=None):
    player, step = int(observation['player']), int(observation['step'])
    state = _R37_PLAYERS.get(player)
    if state is None or step <= state['step']:
        state = _R37_PLAYERS[player] = {'step': -1, 'streak': 0}
    if step == 0:
        _R37_STATS.update(quote_reordered_turns=0, three_turn_calls=0, nocturne_errors=0)
    state['step'] = step
    _R37_HORIZONS[player] = 2
    probe_state=_r44_before(observation)
    try:
        if _R37_ADAPTIVE and step < 648:
            state['streak'] = state['streak'] + 1 if _r37_similarity(observation) >= .90 else 0
            if 336 <= step < 648 and state['streak'] >= 6:
                _R37_HORIZONS[player] = 3
                _R37_STATS['three_turn_calls'] += 1
    except Exception:
        _R37_STATS['nocturne_errors'] += 1
    if _R37_HORIZONS[player]==3 and probe_state['matched']:
        _R37_HORIZONS[player]=4
        _R44_REPORT['probe_four_turn_calls']+=1
    # EXP179: four-turn reservation; retain stock, debt and purchase barriers.
    if 288 <= step < 696:_R37_HORIZONS[player] = 8
    action = _R37_PARENT(observation, configuration)
    _r44_after(observation,action,probe_state)
    if _R37_QUOTE and step >= 288:
        try:
            action = _r37_reorder_sales(observation, action)
        except Exception:
            _R37_STATS['nocturne_errors'] += 1
    _R37_REPORT.update(getattr(_R37_PARENT, 'telemetry', {}))
    _R37_REPORT.update(_R37_STATS)
    _R37_REPORT.update(_R44_REPORT)
    return action

agent.telemetry = _R37_REPORT

# Export guard: normal decisions stay identical to the frozen screened policy.
_RELEASE_PARENT=agent
_RELEASE_REPORT={}
_RELEASE_ERRORS=0
del agent

def agent(observation,configuration=None):
    global _RELEASE_ERRORS
    try:
        result=_RELEASE_PARENT(observation,configuration)
    except Exception:
        _RELEASE_ERRORS+=1
        count=0
        try:
            count=min(64,len(observation['farms'][int(observation['player'])]['hands']))
        except Exception:
            pass
        result={'farmer':['PASS'],'hands':[['PASS'] for _ in range(count)],'market':[]}
    _RELEASE_REPORT.update(getattr(_RELEASE_PARENT,'telemetry',{}))
    _RELEASE_REPORT['release_errors']=_RELEASE_ERRORS
    return result

agent.telemetry=_RELEASE_REPORT
agent=globals().pop('agent')

# Adapted from prvsiyan / The Soil Remembers Rain, Apache-2.0.
# V233: bounded, financed six-sheep SE discovery investment.
_V233_PARENT=agent
del agent
_V233_STATES={}
_V233_REPORT=dict(sheep_commit_requests=0,sheep_committed=0,sheep_hire_requests=0,
    sheep_workers_confirmed=0,sheep_hire_shortfalls=0,sheep_budget_declines=0,
    sheep_capacity_declines=0,sheep_purchase_shortfalls=0,sheep_feed_buy_requests=0,
    sheep_wool_harvested=0,sheep_fert_collected=0,sheep_extra_wool_sales=0,
    sheep_extra_fert_sales=0,sheep_rescue_feed_requests=0)

def _v233_eligible(obs,native):
    # C150: reconsider after later public shop unlocks while at least three
    # SHEEP yield dates (entry+6, +9, +12) remain through day 29.
    entry_day=int(obs['step'])//24
    farm=obs['farms'][obs['player']];prices=obs['market']['prices']
    if len(farm['tiles'])!=10 or set(farm['unlocked_quadrants'])!={'NW','NE','SW'}:return False
    if obs['town']['unlocked_shops'].count('YARN_STORE')<2 or prices['WOOL']<220 or prices['WHEAT']>45:return False
    if any(farm['tiles'][y][x]!='LOCKED' for y in (5,6) for x in range(5,8)):return False
    if obs['private']['shed'].get('SHEEP',0) or any(i.get('SHEEP',0) for i in obs['private']['inventories']):return False
    for day in range(entry_day,30):
        for a in _v219_native_day(native,day):
            if any(o and (o[0]=='BUY_LAND' or o[:2]==['BUY_ANIMAL','SHEEP']) for o in a.get('market',[])):return False
            if any(c and c[0] in ('PICKUP','PLACE') and len(c)>1 and c[1]=='SHEEP' for c in [a.get('farmer')]+a.get('hands',[])):return False
    return True

def _v233_request(obs,action,state,native):
    step=int(obs['step']);day=step//24;hour=step%24
    if hour>(2 if state.get('committed') else 1) or state.get('requested_day')==day:return action
    if not state.get('committed') and (not 12<=day<=17 or not _v233_eligible(obs,native)):return action
    planned=_v219_native_day(native,day)
    if any(o and o[0]=='HIRE' for a in planned[hour+1:] for o in a.get('market',[])):return action
    farm=obs['farms'][obs['player']];market=action.get('market',[])
    parent_hires=sum(bool(o) and o[0]=='HIRE' for o in market)
    expected=max(len(a.get('hands',[])) for a in planned)
    if len(farm['hands'])+parent_hires!=expected:return action
    initial=not state.get('committed')
    extra=([['BUY_LAND'],['BUY_ANIMAL','SHEEP',6]] if initial else [])+[['BUY_PRODUCT','WHEAT',6],['HIRE'],['HIRE']]
    if len(market)+len(extra)>MAX_ORDERS:return action
    stock=projected_shed(action,FarmView(obs))
    incoming=6+6*initial
    budget=7000*initial+6*(int(obs['market']['prices']['WHEAT'])+10)
    budget+=sum(_v219_fib(n) for n in range(farm['hires_today'],farm['hires_today']+parent_hires+2))
    for o in market:
        if not o:continue
        if o[0]=='BUY_LAND':return action
        if o[0]=='BUY_PRODUCT':
            incoming+=int(o[2]);budget+=int(o[2])*(int(obs['market']['prices'][o[1]])+10)
        elif o[0]=='BUY_ANIMAL':
            incoming+=int(o[2]);budget+=int(o[2])*{'SHEEP':500,'COW':400,'GOOSE':300}[o[1]]
        elif o[0]=='BUY_SEED':budget+=int(o[2])*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[o[1]]
    if sum(stock.values())+incoming>100:
        _V233_REPORT['sheep_capacity_declines']+=1;return action
    if farm['money']<budget+(3000 if initial else 1000):
        _V233_REPORT['sheep_budget_declines']+=1;return action
    state['requested_day']=day
    state['pending']={'first':expected+1,'initial':initial}
    _V233_REPORT['sheep_hire_requests']+=2;_V233_REPORT['sheep_feed_buy_requests']+=6
    if initial:_V233_REPORT['sheep_commit_requests']+=1
    result=copy.deepcopy(action);result['market']=market+extra
    return result

def _v233_worker(obs,actor,targets):
    farm=obs['farms'][obs['player']];private=obs['private'];step=int(obs['step'])
    pos=tuple(farm['hands'][actor-1]);inv=private['inventories'][actor]
    access=((4,4),(5,4),(4,5),(5,5))
    home=min(access,key=lambda p:(abs(pos[0]-p[0])+abs(pos[1]-p[1]),p))
    distance=abs(pos[0]-home[0])+abs(pos[1]-home[1])
    cargo=[item for item in ('WOOL','FERTILIZER') if inv.get(item,0)]
    if cargo and step%24 >= (22 if step//24==29 else 23)-distance:
        return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    missing=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP') for x,y in targets)
    if missing and not inv.get('SHEEP',0) and private['shed'].get('SHEEP',0):
        return _v219_walk(pos,home) or ['PICKUP','SHEEP',min(missing,private['shed']['SHEEP'])]
    hungry=sum(not(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('fed_today')) for x,y in targets)
    if hungry and not inv.get('WHEAT',0) and private['shed'].get('WHEAT',0):
        return _v219_walk(pos,home) or ['PICKUP','WHEAT',min(hungry,private['shed']['WHEAT'])]
    tasks=[]
    for target in targets:
        x,y=target;tile=farm['tiles'][y][x];command=None
        if tile is None:command=['BUILD_PASTURE']
        elif isinstance(tile,dict) and tile.get('kind')=='WEED':command=['DIG']
        elif isinstance(tile,dict) and tile.get('kind')=='PASTURE' and not tile.get('animal'):
            if inv.get('SHEEP',0):command=['PLACE','SHEEP']
        elif isinstance(tile,dict) and tile.get('animal')=='SHEEP':
            if not tile['fed_today'] and inv.get('WHEAT',0):command=['FEED']
            elif not tile['cared_today']:command=['CARE']
            elif tile['yield_units']:command=['HARVEST']
            elif tile['fertilizer_available']:command=['COLLECT_FERTILIZER']
        if command:tasks.append((abs(pos[0]-x)+abs(pos[1]-y),targets.index(target),target,command))
    if tasks:
        _,_,target,command=min(tasks);return _v219_walk(pos,target) or command
    if cargo:return _v219_walk(pos,home) or ['PLACE',cargo[0],inv[cargo[0]]]
    return ['PASS']

def _v234_rescue(obs,action,state):
    if not state['workers'] or int(obs['step'])%24>14:return action
    orders=action.get('market',[])
    if len(orders)>=MAX_ORDERS:return action
    if any(o and (o[0] in ('HIRE','BUY_LAND','BUY_ANIMAL','BUY_PRODUCT','BUY_SEED') or (len(o)>1 and o[1]=='WHEAT')) for o in orders):return action
    farm=obs['farms'][obs['player']];private=obs['private'];hungry=carried=0
    commands=[action.get('farmer') or ['PASS']]+list(action.get('hands') or [])
    for actor,targets in state['workers'].items():
        command=commands[actor]
        if command==['FEED'] or command[:2]==['PICKUP','WHEAT']:return action
        carried+=private['inventories'][actor].get('WHEAT',0)
        hungry+=sum(isinstance(farm['tiles'][y][x],dict) and farm['tiles'][y][x].get('animal')=='SHEEP' and not farm['tiles'][y][x].get('fed_today') for x,y in targets)
    stock=projected_shed(action,FarmView(obs))
    shortage=hungry-carried-stock.get('WHEAT',0)
    if not 0<shortage<=6 or state.get('rescue_today',0)+shortage>6:return action
    quote=int(obs['market']['prices']['WHEAT'])
    if quote<1 or farm['money']<1000+shortage*(quote+10) or sum(stock.values())+shortage>100:return action
    result=copy.deepcopy(action);result['market'].append(['BUY_PRODUCT','WHEAT',shortage])
    state['rescue_today']=state.get('rescue_today',0)+shortage
    _V233_REPORT['sheep_rescue_feed_requests']+=shortage
    return result

def agent(observation,configuration=None):
    action=_V233_PARENT(observation,configuration)
    step=int(observation['step']);player=int(observation['player']);day=step//24
    state=_V233_STATES.get(player)
    if state is None or step<=state['last_step']:
        state={'last_step':step,'day':-1,'workers':{},'work':{},'credit':{'WOOL':0,'FERTILIZER':0}}
        _V233_STATES[player]=state
    state['last_step']=step
    if configuration is not None and any(configuration.get(k,v)!=v for k,v in
        (('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10))):return action
    if day<12:return action
    farm=observation['farms'][player];private=observation['private']
    if state['day']!=day:state['day']=day;state['workers']={};state['work']={};state['rescue_today']=0
    for actor,previous in state['work'].items():
        if previous['step']!=step-1 or actor>=len(private['inventories']):continue
        item={'HARVEST':'WOOL','COLLECT_FERTILIZER':'FERTILIZER'}.get(previous['command'][0])
        if item:
            gained=max(0,private['inventories'][actor].get(item,0)-previous['inventory'].get(item,0))
            state['credit'][item]+=gained
            _V233_REPORT['sheep_wool_harvested' if item=='WOOL' else 'sheep_fert_collected']+=gained
    pending=state.pop('pending',None)
    if pending:
        funded='SE' in farm['unlocked_quadrants'] and (not pending['initial'] or private['shed'].get('SHEEP',0)>=6)
        if not funded:_V233_REPORT['sheep_purchase_shortfalls']+=1
        elif len(farm['hands'])<pending['first']+1:_V233_REPORT['sheep_hire_shortfalls']+=1
        else:
            for i in range(2):state['workers'][pending['first']+i]=[(x,5+i) for x in range(5,8)]
            _V233_REPORT['sheep_workers_confirmed']+=2
            if pending['initial']:state['committed']=True;_V233_REPORT['sheep_committed']+=1
    action=_v233_request(observation,action,state,_IMPL.chassis.players[player])
    if not state.get('committed'):return action
    result=copy.deepcopy(action)
    commands=[result.get('farmer') or ['PASS']]+list(result.get('hands') or [])
    commands += [['PASS'] for _ in range(len(farm['hands'])+1-len(commands))]
    state['work']={}
    for actor,targets in state['workers'].items():
        command=_v233_worker(observation,actor,targets);commands[actor]=command
        state['work'][actor]={'step':step,'command':command,'inventory':dict(private['inventories'][actor])}
    result['farmer'],result['hands']=commands[0],commands[1:]
    result=_v234_rescue(observation,result,state)
    stock=projected_shed(result,FarmView(observation))
    for item in ('WOOL','FERTILIZER'):
        scheduled=sum(int(o[2]) for o in result['market'] if o[:2]==['SELL',item])
        count=min(state['credit'][item],max(0,stock.get(item,0)-scheduled))
        if count and len(result['market'])<MAX_ORDERS:
            result['market'].append(['SELL',item,count]);state['credit'][item]-=count
            _V233_REPORT['sheep_extra_wool_sales' if item=='WOOL' else 'sheep_extra_fert_sales']+=count
    return result

_R46_SHEEP_AGENT=agent
_R46_SHADOW_PARENT=_shadow_terminal
_R46_REPORT={}
def _shadow_terminal(obs,config):
    if _V233_STATES.get(int(obs['player']),{}).get('committed'):return None
    return _R46_SHADOW_PARENT(obs,config)
del agent
def agent(observation,configuration=None):
    try:
        if int(observation.get('step',-1))==0:
            for k in _V233_REPORT:_V233_REPORT[k]=0
        result=_R46_SHEEP_AGENT(observation,configuration)
    except Exception:
        _R46_REPORT['sheep_overlay_errors']=_R46_REPORT.get('sheep_overlay_errors',0)+1
        result={'farmer':['PASS'],'hands':[],'market':[]}
    _R46_REPORT.update(getattr(_V233_PARENT,'telemetry',{}))
    _R46_REPORT.update(_V233_REPORT)
    return result
agent.telemetry=_R46_REPORT
agent=globals().pop('agent')

# EXP182: finite-harvest wheat/carrot input planner; original adaptation.
_R51_INPUT_PARENT=agent
_R51_INPUT_STATES={}
_R51_INPUT_REPORT={}
_R51_INPUT_MAX_WORKERS=2
_R51_INPUT_CROPS={'WHEAT':(2,4,6),'CARROT':(2,3,4)}

def _r51_input_forecast(obs,route,expected):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    pos=[list(farm['farmer'])]+[list(p) for p in farm['hands'][:expected]];targets={}
    for y,line in enumerate(farm['tiles']):
        for x,tile in enumerate(line):
            if not isinstance(tile,dict) or tile.get('crop') not in _R51_INPUT_CROPS:continue
            item=tile['crop'];first,last,cap=_R51_INPUT_CROPS[item]
            if 1<=day-tile['planted_day']<last:
                targets[(x,y)]={'crop':item,'birth':tile['planted_day'],'yield':tile['yield_units'],
                    'until':tile.get('fertilized_until_day',-1),'watered':tile.get('watered_today',False),'water':[],'harvest':None,'first':first,'last':last,'cap':cap}
    access=((4,4),(5,4),(4,5),(5,5));seen=set()
    # Native continuation ends before the reactive terminal closure planner.
    for t in range(step,min(712,(day+4)*24)):
        tape=_IMPL.chassis.routes[2 if t>=648 else route];a=tape[t]
        for actor,c in enumerate([a.get('farmer') or ['PASS'],*(a.get('hands') or [])][:len(pos)]):
            if not c:continue
            xy=tuple(pos[actor]);target=targets.get(xy)
            if target is not None and target['harvest'] is None:
                if c[0]=='WATER' and (t//24,xy) not in seen:
                    seen.add((t//24,xy))
                    if not(t//24==day and target['watered']) and target['first']<=t//24-target['birth']<=target['last']:target['water'].append(t)
                if c[0]=='HARVEST':target['harvest']=t
            if c[0] in MOVES:
                dx,dy=MOVES[c[0]];pos[actor]=[max(0,min(9,pos[actor][0]+dx)),max(0,min(9,pos[actor][1]+dy))]
        for o in a.get('market',[]):
            if o and o[0]=='HIRE':
                counts={p:sum(tuple(q)==p for q in pos) for p in access}
                pos.append(list(min(access,key=lambda p:(counts[p],access.index(p)))))
        if (t+1)%24==0:pos=[[4,4]]
    return targets

def _r51_input_gain(target,arrival,day):
    if target['harvest'] is None or target['harvest']<=arrival:return 0
    extra=sum(arrival<t<=target['harvest'] and day<=t//24<=day+2 and t//24>target['until'] for t in target['water'])
    baseline=target['yield']+sum(2 if t//24<=target['until'] else 1 for t in target['water'])
    return max(0,min(extra,target['cap']-baseline))

def _r51_input_path(obs,targets):
    step=int(obs['step']);day=step//24;now=step+4;pos=(4,4);remaining=dict(targets);path=[];quantities={'WHEAT':0,'CARROT':0}
    while remaining and len(path)<8:
        options=[]
        for xy,target in remaining.items():
            arrival=now+abs(pos[0]-xy[0])+abs(pos[1]-xy[1]);gain=_r51_input_gain(target,arrival,day)
            price=max(1,int(obs['market']['prices'][target['crop']])-2)
            if gain and arrival<day*24+23:options.append((gain*price/(arrival-now+1),gain*price,-arrival,xy,arrival,gain))
        if not options:break
        _,_,_,xy,arrival,gain=max(options);target=remaining.pop(xy)
        path.append((xy[0],xy[1],target['crop'],target['birth']));quantities[target['crop']]+=gain;now=arrival+1;pos=xy
    return path,quantities

def _r51_input_control(obs,action,state):
    step=int(obs['step']);day=step//24;hour=step%24;player=int(obs['player']);farm=obs['farms'][player];private=obs['private']
    native=_IMPL.chassis.players[player]
    if state.get('day')!=day:state.update(day=day,workers={},pending=None,placed=[])
    for x,y in state['placed']:
        tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('fertilized_until_day',-1)>=day+2:_R51_INPUT_REPORT['input_confirmed_applications']+=1
        else:_R51_INPUT_REPORT['input_application_errors']+=1
    state['placed']=[]
    if state.get('pending'):
        pending=state.pop('pending')
        for actor,plan in pending.items():
            if len(farm['hands'])>=actor:state['workers'][actor]=plan;_R51_INPUT_REPORT['input_confirmed_hires']+=1
            else:_R51_INPUT_REPORT['input_hire_errors']+=1
    if state['workers']:
        changed=copy.deepcopy(action)
        for actor,plan in state['workers'].items():
            inv=private['inventories'][actor];pos=tuple(farm['hands'][actor-1]);cmd=['PASS']
            if not plan['loaded']:
                stock=projected_shed(changed,FarmView(obs));q=min(plan['quantity'],max(0,stock.get('FERTILIZER',0)))
                if q and _shed_adjacent(pos,10):
                    cmd=['PICKUP','FERTILIZER',q];plan['loaded']=True;_R51_INPUT_REPORT['input_loaded_units']+=q
                    if q<plan['quantity']:_R51_INPUT_REPORT['input_stock_shortfalls']+=plan['quantity']-q
            elif inv.get('FERTILIZER',0):
                while plan['path']:
                    x,y,crop,birth=plan['path'][0];tile=farm['tiles'][y][x]
                    if not isinstance(tile,dict) or tile.get('crop')!=crop or tile.get('planted_day')!=birth or tile.get('fertilized_until_day',-1)>=day+2:
                        plan['path'].pop(0);continue
                    cmd=_v219_walk(pos,(x,y)) or ['FERTILIZE']
                    if cmd==['FERTILIZE']:state['placed'].append((x,y));plan['path'].pop(0);_R51_INPUT_REPORT['input_application_requests']+=1
                    break
            changed['hands'][actor-1]=cmd
        return changed
    if hour not in (1,2,3) or not 12<=day<=28:return action
    planned=_v219_native_day(native,day);expected=max(len(a.get('hands',[])) for a in planned)
    if any(o and o[0]=='HIRE' for a in planned[hour:] for o in a.get('market',[])) or native['pending']:return action
    parents=[_V219_STATES.get(player,{}),_V233_STATES.get(player,{})]
    # A parent may retry after a full market queue; its headcount must remain native.
    if day in (12,18) or any(p.get('committed') and p.get('requested_day')!=day for p in parents):return action
    if any(p.get('pending') for p in parents) or any(o and o[0]=='HIRE' for o in action.get('market',[])):return action
    owned=set(range(1,expected+1))
    for p in parents:
        actors=set(p.get('workers',{}))
        if owned&actors:return action
        owned|=actors
    if owned!=set(range(1,len(farm['hands'])+1)):return action
    targets=_r51_input_forecast(obs,native['route'],expected);plans=[];total_q=0;total_cost=0;all_units={'WHEAT':0,'CARROT':0}
    stock=projected_shed(action,FarmView(obs));purchases=sum(max(0,int(o[2])) for o in action.get('market',[]) if len(o)>2 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    # Units act before market orders. Preserve the native next-turn pickup,
    # after the current parent's actual sales/purchases, before buying tour inputs.
    available=max(0,stock.get('FERTILIZER',0))
    for o in action.get('market',[]):
        if len(o)>=3 and o[:2]==['SELL','FERTILIZER']:available=max(0,available-max(0,int(o[2])))
        elif len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER']:available+=max(0,int(o[2]))
    next_native=planned[hour+1];native_pickups=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [next_native.get('farmer') or ['PASS'],*(next_native.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    topup=max(0,native_pickups-available)
    for i in range(_R51_INPUT_MAX_WORKERS):
        path,units=_r51_input_path(obs,targets);q=len(path)
        if q<3 or len(action.get('market',[]))+2+i>10 or sum(stock.values())+purchases+total_q+q+topup>95:break
        quote=_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-total_q-q-topup)
        cost=(q+(topup if i==0 else 0))*(quote+2)+_v219_fib(int(farm['hires_today'])+i)
        value=sum(n*max(1,_r37_market_price(item,obs['market']['inventory'][item]+all_units[item]+n)-2) for item,n in units.items())
        if value<1.5*cost+50 or farm['money']<total_cost+cost+3000:break
        plans.append({'path':path,'quantity':q,'loaded':False});total_q+=q;total_cost+=cost
        for item,n in units.items():all_units[item]+=n
        for x,y,_,_ in path:targets.pop((x,y),None)
    if not plans:return action
    state['pending']={len(farm['hands'])+1+i:plan for i,plan in enumerate(plans)}
    _R51_INPUT_REPORT['input_hire_requests']+=len(plans);_R51_INPUT_REPORT['input_purchase_requests']+=total_q+topup
    _R51_INPUT_REPORT['input_forecast_wheat']+=all_units['WHEAT'];_R51_INPUT_REPORT['input_forecast_carrot']+=all_units['CARROT']
    changed=copy.deepcopy(action);changed['market'] += [['BUY_PRODUCT','FERTILIZER',total_q+topup]]+[['HIRE'] for _ in plans];return changed

def agent(observation,configuration=None):
    try:
        step=int(observation['step']);player=int(observation['player']);state=_R51_INPUT_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R51_INPUT_STATES[player]={'step':-1}
            _R51_INPUT_REPORT.update(input_hire_requests=0,input_confirmed_hires=0,input_hire_errors=0,input_purchase_requests=0,
                input_loaded_units=0,input_stock_shortfalls=0,input_application_requests=0,input_confirmed_applications=0,
                input_application_errors=0,input_errors=0,input_forecast_wheat=0,input_forecast_carrot=0)
        state['step']=step;action=_R51_INPUT_PARENT(observation,configuration)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):
            action=_r51_input_control(observation,action,state)
        _R51_INPUT_REPORT.update(getattr(_R51_INPUT_PARENT,'telemetry',{}));return action
    except Exception:
        _R51_INPUT_REPORT['input_errors']=_R51_INPUT_REPORT.get('input_errors',0)+1
        return {'farmer':['PASS'],'hands':[],'market':[]}
agent.telemetry=_R51_INPUT_REPORT
agent=globals().pop('agent')

# EXP182: project the final hour's actual worker actions before automatic deposit.
_R51_WAREHOUSE_PARENT=agent
_R51_WAREHOUSE_REPORT={}

def _r51_close_warehouse(obs,action):
    step=int(obs['step']);day=step//24
    if step%24!=23 or not 12<=day<=28:return action
    # No speculative product purchase/worker count model: these hours abstain.
    if any(o and o[0] not in ('SELL',) for o in action.get('market',[])):return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={k for k,q in demand.items() if q>private['seeds'].get(k,0)}
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:c=['PASS']
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    post=dict(private['shed'])
    for o in action.get('market',[]):
        if len(o)>=3 and o[0]=='SELL':post[o[1]]=max(0,post.get(o[1],0)-max(0,int(o[2])))
    needed=sum(post.values())+sum(max(0,q) for inv in private['inventories'] for q in inv.values())-100
    if needed<=0:return action
    result=copy.deepcopy(action);orders=result['market']
    # Grain and fertilizer have native input obligations; other products do not.
    # Additional commodity sales are bounded by actual post-action physical stock.
    for item in sorted((p for p in PRODUCTS if p not in ('WHEAT','FERTILIZER')),key=lambda p:-obs['market']['prices'].get(p,0)):
        qty=min(needed,post.get(item,0))
        if not qty:continue
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL',item]),None)
        if existing is not None:existing[2]=max(0,int(existing[2]))+qty
        elif len(orders)<10:orders.append(['SELL',item,qty])
        else:continue
        needed-=qty;post[item]-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
        if needed<=0:break
    if needed>0:
        native=_IMPL.chassis.players[int(obs['player'])];reserve=0
        for t in range(step+1,719):
            future=_IMPL.chassis.routes[2 if t>=648 else native['route']][t]
            for c in [future.get('farmer') or ['PASS'],*(future.get('hands') or [])]:
                if len(c)>1 and c[:2]==['PICKUP','WHEAT']:reserve+=max(0,int(c[2]) if len(c)>2 else 1)
            if any(len(o)>1 and o[:2]==['BUY_PRODUCT','WHEAT'] for o in future.get('market',[])):break
        incoming=sum(max(0,inv.get('WHEAT',0)) for inv in private['inventories'])
        others=sum(q for p,q in post.items() if p!='WHEAT')+sum(max(0,q) for inv in private['inventories'] for p,q in inv.items() if p!='WHEAT')
        # Even if every other carried item deposits first, this grain reserve fits.
        qty=min(needed,post.get('WHEAT',0),max(0,post.get('WHEAT',0)+incoming-reserve)) if 100-others>=reserve else 0
        existing=next((o for o in orders if len(o)>=3 and o[:2]==['SELL','WHEAT']),None)
        if qty and (existing is not None or len(orders)<10):
            if existing is not None:existing[2]=max(0,int(existing[2]))+qty
            else:orders.append(['SELL','WHEAT',qty])
            needed-=qty;_R51_WAREHOUSE_REPORT['warehouse_extra_sales']+=qty
    _R51_WAREHOUSE_REPORT['warehouse_projected_unresolved']+=max(0,needed)
    if result!=action:_R51_WAREHOUSE_REPORT['warehouse_changed_turns']+=1
    return result

def agent(observation,configuration=None):
    result=_R51_WAREHOUSE_PARENT(observation,configuration)
    try:
        if int(observation['step'])==0:_R51_WAREHOUSE_REPORT.update(warehouse_changed_turns=0,warehouse_extra_sales=0,warehouse_projected_unresolved=0,warehouse_errors=0)
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):result=_r51_close_warehouse(observation,result)
    except Exception:_R51_WAREHOUSE_REPORT['warehouse_errors']=_R51_WAREHOUSE_REPORT.get('warehouse_errors',0)+1
    _R51_WAREHOUSE_REPORT.update(getattr(_R51_WAREHOUSE_PARENT,'telemetry',{}));return result
agent.telemetry=_R51_WAREHOUSE_REPORT
agent=globals().pop('agent')

from itertools import permutations as _r53_permutations
_R53_LABOR_REPORT=dict(labor_requests=0,labor_hires_avoided=0,labor_spawn_errors=0,labor_confirmed=0,labor_day26=0,labor_day27=0,labor_day28=0)

def _r53_labor_assignment(obs,action,fertilizer):
    step=int(obs['step']);day=step//24;farm=obs['farms'][obs['player']]
    if day not in (26,27,28) or step%24>2:return None
    # Do not preempt a later price-gated fertilizer request with a smaller unfertilized team.
    if day==27 and not fertilizer:return None
    count=3 if fertilizer else 2
    positions=[list(farm['farmer'])]+[list(p) for p in farm['hands']]
    for i,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(positions)]):
        if c and c[0] in MOVES:
            dx,dy=MOVES[c[0]];positions[i]=[max(0,min(9,positions[i][0]+dx)),max(0,min(9,positions[i][1]+dy))]
    access=((4,4),(5,4),(4,5),(5,5));spawns=[]
    native_hires=sum(bool(o) and o[0]=='HIRE' for o in action.get('market',[]))
    for i in range(native_hires+count):
        chosen=min(access,key=lambda p:(sum(tuple(q)==p for q in positions),access.index(p)));positions.append(list(chosen))
        if i>=native_hires:spawns.append(chosen)
    groups=(((5,5),(6,5),(7,5),(8,5)),((9,5),(9,6),(8,6)),((5,6),(6,6),(7,6))) if fertilizer else (tuple((x,5) for x in range(5,10)),tuple((x,6) for x in range(5,10)))
    choices=[];remaining=23-step%24
    for assignment in _r53_permutations(groups):
        costs=[]
        for start,path in zip(spawns,assignment):
            distance=abs(start[0]-path[0][0])+abs(start[1]-path[0][1])
            distance+=sum(abs(a[0]-b[0])+abs(a[1]-b[1]) for a,b in zip(path,path[1:]))
            distance+=min(abs(path[-1][0]-x)+abs(path[-1][1]-y) for x,y in access)
            costs.append(distance+(3 if fertilizer else 2)*len(path)+1+int(fertilizer))
        if max(costs)<=remaining:choices.append((max(costs),sum(costs),assignment))
    if not choices:return None
    _,_,assignment=min(choices)
    return dict(paths=assignment,spawns=spawns,remaining=remaining,workers=count,fertilizer=fertilizer)

_R53_LABOR_PARENT=agent
def agent(observation,configuration=None):
    if isinstance(observation,dict) and observation.get('step')==0:
        for k in _R53_LABOR_REPORT:_R53_LABOR_REPORT[k]=0
    result=_R53_LABOR_PARENT(observation,configuration)
    _R53_LABOR_COMBINED.update(getattr(_R53_LABOR_PARENT,'telemetry',{}));_R53_LABOR_COMBINED.update(_R53_LABOR_REPORT)
    return result
_R53_LABOR_COMBINED={}
agent.telemetry=_R53_LABOR_COMBINED
agent=globals().pop('agent')

# Local 2026-09-13 research derivative. Upstream source and licenses retained.
_REPAIR_USE_FUNDING = True
_REPAIR_USE_PLACEMENT = True
# SPDX-License-Identifier: Apache-2.0
# Local research overlay, 2026-09-13. Append to the immutable opening probe.
# The builder sets _REPAIR_USE_FUNDING and _REPAIR_USE_PLACEMENT separately.
# Only ordinary observations and the agent's own predeclared route are used.

_REPAIR_PARENT = agent
_REPAIR_STATES = {}
_REPAIR_REPORT = {}


def _repair_new_state():
    return {"last": -1, "funding": {}, "places": {}, "counts": {}}


def _repair_count(state, key):
    counts = state["counts"]
    counts[key] = counts.get(key, 0) + 1


def _repair_unit(action, actor):
    if actor == 0:
        return action.get("farmer", ["PASS"])
    hands = action.get("hands", [])
    return hands[actor - 1] if actor <= len(hands) else ["PASS"]


def _repair_set_unit(action, actor, command):
    if actor == 0:
        action["farmer"] = command
    else:
        action["hands"][actor - 1] = command


def _repair_funding(obs, action, state):
    """Bridge a 1-4 coin hire deficit without removing seeds or a daily feed.

    The common day-zero route leaves three wheat for dawn. Sell one ONLY when
    the last two seed purchases are funded but the three dawn hires are not.
    Reserve the remaining two for the two cows' early feed. The farmer's sheep
    feed moves to hour 12, after fertilizer receipts can replace the sold wheat.
    All detour commands occupy the farmer's otherwise idle hours 9-14.
    This deliberately does not attempt to rescue a different, already broken
    opening. Such cases need separate research, rather than guessing a route.
    """
    step = int(obs["step"])
    if not 20 <= step <= 48:
        return action
    farm = obs["farms"][obs["player"]]
    private = obs["private"]
    shed = private["shed"]
    inv = private["inventories"][0]
    pos = list(farm["farmer"])
    tiles = farm["tiles"]
    funding = state["funding"]
    sheep = tiles[3][3]
    orders = action.get("market", [])
    if step == 20:
        if (20 <= farm["money"] < 24 and len(farm["hands"]) == 5
                and shed.get("WHEAT", 0) == 3
                and orders == [["BUY_SEED", "WHEAT", 2]]
                and int(obs["market"]["prices"]["WHEAT"]) >= 24 - farm["money"]
                and isinstance(sheep, dict) and sheep.get("animal") == "SHEEP"
                and sheep.get("fed_today")):
            action["market"] = [["SELL", "WHEAT", 1]] + orders
            funding["sale_requested"] = True
            _repair_count(state, "funding_sale_requests")
        return action
    if not funding:
        return action
    if step == 21:
        funding["sold"] = shed.get("WHEAT", 0) == 2
        _repair_count(state, "funding_sales_confirmed" if funding["sold"] else "repair_errors")
    if not funding.get("sold"):
        return action
    if step == 24:
        if (pos == [4, 4] and action["farmer"] == ["PICKUP", "WHEAT"]
                and not farm["hands"] and shed.get("WHEAT", 0) >= 2
                and farm["money"] >= 4 and isinstance(sheep, dict)
                and sheep.get("animal") == "SHEEP"):
            action["farmer"] = ["PASS"]
            funding["deferred"] = True
            _repair_count(state, "funding_feed_deferrals")
        else:
            _repair_count(state, "repair_errors")
    if not funding.get("deferred"):
        return action
    if step == 27 and pos == [3, 3] and not inv.get("WHEAT", 0):
        if action["farmer"] == ["FEED"]:
            action["farmer"] = ["PASS"]
    if step == 32:
        if (pos == [4, 4] and len(orders) < 10
                and action["farmer"] == ["PLACE", "FERTILIZER"]
                and orders == [["SELL", "FERTILIZER", 2]]
                and inv.get("FERTILIZER", 0) >= 1):
            action["market"] = orders + [["BUY_PRODUCT", "WHEAT", 1]]
            funding["wheat_before_buy"] = shed.get("WHEAT", 0)
            _repair_count(state, "funding_rebuy_requests")
        else:
            _repair_count(state, "repair_errors")
    if step == 33:
        confirmed = ("wheat_before_buy" in funding
                     and shed.get("WHEAT", 0) >= funding["wheat_before_buy"] + 1)
        funding["rebought"] = confirmed
        _repair_count(state, "funding_rebuys_confirmed" if confirmed else "repair_errors")
        if not confirmed:
            return action
    path = {
        33: ([4, 4], ["PICKUP", "WHEAT", 1]),
        34: ([4, 4], ["NORTH"]),
        35: ([4, 3], ["WEST"]),
        36: ([3, 3], ["FEED"]),
        37: ([3, 3], ["EAST"]),
        38: ([4, 3], ["SOUTH"]),
    }
    if step in path and funding.get("rebought") and not funding.get("aborted"):
        expected_pos, command = path[step]
        feasible = pos == expected_pos and action["farmer"] == ["PASS"]
        if step == 33:
            feasible = feasible and shed.get("WHEAT", 0) > 0
        if step == 36:
            feasible = (feasible and inv.get("WHEAT", 0) > 0 and isinstance(sheep, dict)
                        and sheep.get("animal") == "SHEEP" and not sheep.get("fed_today"))
        if not feasible:
            funding["aborted"] = True
            _repair_count(state, "repair_errors")
        else:
            action["farmer"] = command
    if step == 37:
        funding["fed"] = isinstance(sheep, dict) and sheep.get("animal") == "SHEEP" and sheep.get("fed_today")
        _repair_count(state, "funding_feeds_confirmed" if funding["fed"] else "repair_errors")
    if step == 39:
        _repair_count(state, "funding_routes_rejoined" if pos == [4, 4] and funding.get("fed") else "repair_errors")
    return action


def _repair_placement(obs, action, state, tape):
    """Finish a missing structure using an existing PLACE/CARE/PASS window.

    The worker remains on the same tile for all three actions. No movement,
    purchases, live crops, other workers, or later route commands are displaced.
    Confirm the structure and actual carried animal before the second action.
    """
    step = int(obs["step"])
    if not 0 <= step < 144:
        return action
    farm = obs["farms"][obs["player"]]
    positions = [farm["farmer"], *farm["hands"]]
    inventories = obs["private"]["inventories"]
    used = set()
    for actor, plan in list(state["places"].items()):
        if actor >= len(positions) or list(positions[actor]) != plan["pos"]:
            state["places"].pop(actor)
            _repair_count(state, "repair_errors")
            continue
        x, y = positions[actor]
        tile = farm["tiles"][y][x]
        valid = False
        if step == plan["step"] + 1:
            valid = (isinstance(tile, dict) and tile.get("kind") == plan["kind"]
                     and "animal" not in tile and inventories[actor].get(plan["animal"], 0) > 0
                     and _repair_unit(action, actor) == ["CARE"])
            if valid:
                _repair_set_unit(action, actor, ["PLACE", plan["animal"]])
                _repair_count(state, "placement_requests")
        elif step == plan["step"] + 2:
            valid = (isinstance(tile, dict) and tile.get("animal") == plan["animal"]
                     and tile.get("placed_day") == step // 24
                     and _repair_unit(action, actor) == ["PASS"])
            if valid:
                _repair_set_unit(action, actor, ["CARE"])
                _repair_count(state, "placements_confirmed")
            state["places"].pop(actor)
        if not valid:
            state["places"].pop(actor, None)
            _repair_count(state, "repair_errors")
        used.add(actor)
    if step % 24 > 21 or step + 2 >= len(tape):
        return action
    for actor, pos in enumerate(positions):
        if actor in used:
            continue
        command = _repair_unit(action, actor)
        if len(command) < 2 or command[0] != "PLACE" or command[1] not in ("COW", "SHEEP", "GOOSE"):
            continue
        x, y = pos
        if farm["tiles"][y][x] is not None or inventories[actor].get(command[1], 0) <= 0:
            continue
        if (_repair_unit(tape[step + 1], actor) != ["CARE"]
                or _repair_unit(tape[step + 2], actor) != ["PASS"]):
            continue
        # Avoid simultaneous tile operations by a second worker.
        if any(other != actor and list(p) == list(pos) for other, p in enumerate(positions)):
            continue
        kind = "COOP" if command[1] == "GOOSE" else "PASTURE"
        _repair_set_unit(action, actor, ["BUILD_" + kind])
        state["places"][actor] = {"step": step, "pos": list(pos), "animal": command[1], "kind": kind}
        _repair_count(state, "placement_build_requests")
    return action


def agent(observation, configuration=None):
    parent_action = _REPAIR_PARENT(observation, configuration)
    step = int(observation["step"])
    seat = int(observation["player"])
    state = _REPAIR_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _REPAIR_STATES[seat] = _repair_new_state()
    state["last"] = step
    result = parent_action
    supported = len(observation["farms"][seat]["tiles"]) == 10
    if configuration is not None:
        supported = supported and all(configuration.get(k, v) == v for k, v in (
            ("turnsPerDay", 24), ("shedCapacity", 100), ("maxMarketOrdersPerTurn", 10), ("farmHandCostMult", 1)))
    if supported and step < 144:
        result = copy.deepcopy(parent_action)
        if _REPAIR_USE_FUNDING:
            result = _repair_funding(observation, result, state)
        if _REPAIR_USE_PLACEMENT:
            result = _repair_placement(observation, result, state, _ROUTES[0])
    _REPAIR_REPORT.clear()
    _REPAIR_REPORT.update(getattr(_REPAIR_PARENT, "telemetry", {}))
    _REPAIR_REPORT.update(state["counts"])
    return result


agent.telemetry = _REPAIR_REPORT

# Kaggle 1.32.7 selects the last callable by global insertion order.
# Keep the public agent export after every helper and alias.
agent = globals().pop('agent')

# SPDX-License-Identifier: Apache-2.0
"""Complete a weed-blocked structure by consuming an existing same-day idle turn.

Append to a frozen c110/c111 source. Only the current observation and the policy's
own route are consulted. No episode IDs, replay data, opponent internals, or RNG
state are available to this overlay.
"""

_CP0_PARENT = agent
_CP0_STATES = {}
_CP0_REPORT = {}
_CP0_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}


def _cp0_command(action, actor):
    if actor == 0:
        return list(action.get("farmer") or ["PASS"])
    hands = action.get("hands") or []
    return list(hands[actor - 1]) if actor <= len(hands) else ["PASS"]


def _cp0_set(action, actor, command):
    if actor == 0:
        action["farmer"] = list(command)
    else:
        action["hands"][actor - 1] = list(command)


def _cp0_count(state, name):
    name = "pasture_" + name
    state["counts"][name] = state["counts"].get(name, 0) + 1


def _cp0_plan(obs, action, tape, actor):
    """Return a route detour only when it has an economically inert idle budget.

    Moving/WATER can be delayed within the same day. Resource transfers, harvest,
    feed, purchases of labor, and every other field command exclude the window.
    WATER targets must already be planted and survive the complete window.
    """
    step = int(obs["step"])
    farm = obs["farms"][int(obs["player"])]; positions = [farm["farmer"], *farm["hands"]]
    command = _cp0_command(tape[step], actor)
    if command not in (["BUILD_PASTURE"], ["BUILD_COOP"]):
        return None
    pos = list(positions[actor]); x, y = pos
    tile = farm["tiles"][y][x]
    if not (isinstance(tile, dict) and tile.get("kind") == "WEED"
            and _cp0_command(action, actor) == ["DIG"]):
        return None
    # The target belongs to one actor for this turn; don't displace shared work.
    if any(i != actor and list(p) == pos for i, p in enumerate(positions)):
        return None
    commands = []; current = list(pos)
    stop = min(len(tape), (step // 24 + 1) * 24)
    for future in range(step + 1, stop):
        if any(o and o[0] == "HIRE" for o in tape[future].get("market", [])):
            return None
        nxt = _cp0_command(tape[future], actor)
        if nxt == ["PASS"]:
            # If the first turn is already idle, the parent's queue can finish.
            if not commands:
                return None
            return {"start": step + 1, "end": future, "pos": pos,
                    "expected": list(pos), "build": command,
                    "kind": command[0][6:], "commands": commands}
        if len(nxt) != 1 or nxt[0] not in (*_CP0_MOVES, "WATER"):
            return None
        if nxt[0] in _CP0_MOVES:
            dx, dy = _CP0_MOVES[nxt[0]]
            current = [max(0, min(9, current[0] + dx)), max(0, min(9, current[1] + dy))]
        else:
            target = farm["tiles"][current[1]][current[0]]
            if not isinstance(target, dict) or target.get("kind") != "PLANT":
                return None
            # Avoid converting a decay-time weed cleanup into a delayed WATER.
            expiry = target.get("max_lifespan_step", -1)
            if expiry >= 0 and expiry <= stop:
                return None
        commands.append(nxt)
    return None


def _cp0_repair(obs, action, state, tape):
    step = int(obs["step"])
    farm = obs["farms"][int(obs["player"])]; positions = [farm["farmer"], *farm["hands"]]
    used = set()
    for actor, plan in list(state["plans"].items()):
        used.add(actor)
        if step == plan["end"] + 1 and step % 24 == 0:
            # Hands disappear at dawn. Each prior position was checked before
            # its command; next-day worker indices must not be treated as ours.
            state["plans"].pop(actor); _cp0_count(state, "overnight_completed"); continue
        if actor >= len(positions) or list(positions[actor]) != plan["expected"]:
            state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
        if step == plan["end"] + 1:
            state["plans"].pop(actor); _cp0_count(state, "routes_rejoined"); continue
        if not plan["start"] <= step <= plan["end"]:
            state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
        x, y = plan["pos"]; tile = farm["tiles"][y][x]
        if step == plan["start"]:
            if tile is not None:
                state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
            command = plan["build"]
            _cp0_count(state, "build_requests")
        else:
            if step == plan["start"] + 1:
                if not isinstance(tile, dict) or tile.get("kind") != plan["kind"]:
                    state["plans"].pop(actor); _cp0_count(state, "repair_errors"); continue
                _cp0_count(state, "builds_confirmed")
            command = plan["commands"][step - plan["start"] - 1]
        _cp0_set(action, actor, command)
        if command[0] in _CP0_MOVES:
            dx, dy = _CP0_MOVES[command[0]]
            old = plan["expected"]
            plan["expected"] = [max(0, min(9, old[0] + dx)), max(0, min(9, old[1] + dy))]
        _cp0_count(state, "detour_commands")
    if step >= 144 or step >= len(tape):
        return action
    for actor in range(len(positions)):
        if actor in used:
            continue
        plan = _cp0_plan(obs, action, tape, actor)
        if plan is not None:
            state["plans"][actor] = plan
            _cp0_count(state, "detours_queued")
    return action


def agent(observation, configuration=None):
    parent = _CP0_PARENT(observation, configuration)
    step = int(observation["step"]); seat = int(observation["player"])
    state = _CP0_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _CP0_STATES[seat] = {"last": -1, "plans": {}, "counts": {}}
    state["last"] = step
    result = parent
    try:
        supported = len(observation["farms"][seat]["tiles"]) == 10
        if configuration is not None:
            supported = supported and all(configuration.get(k, v) == v for k, v in (
                ("turnsPerDay", 24), ("shedCapacity", 100), ("farmHandCostMult", 1)))
        if supported and (step < 144 or state["plans"]):
            route = _IMPL.chassis.players[seat]["route"]
            tape = _ROUTES[route]
            result = _cp0_repair(observation, copy.deepcopy(parent), state, tape)
    except Exception:
        _cp0_count(state, "repair_errors")
        state["plans"].clear()
        result = parent
    _CP0_REPORT.clear()
    _CP0_REPORT.update(getattr(_CP0_PARENT, "telemetry", {}))
    _CP0_REPORT.update(state["counts"])
    return result


agent.telemetry = _CP0_REPORT
# Kaggle 1.32.7 loads the last callable by insertion order.
agent = globals().pop("agent")

# SPDX-License-Identifier: Apache-2.0
"""Use a 12-turn physical sale reservation only against a sustained mirror farm.

The parent c111 policy reserves physically available, non-input stock eight turns
before its own tape sale.  Two live losses showed a near-identical rival reserving
the same MILK/STRAWBERRY/WOOL batches twelve turns ahead.  This overlay changes
only the reservation horizon.  It keeps the parent's stock projection, purchase
and pickup barriers, ten-order cap, due-step debts, and quote ordering intact.
"""

_C115_PARENT = agent
_C115_NATIVE_R36_RESERVE = _r36_reserve
_C115_STATES = {}
_C115_REPORT = {}
del agent


def _c115_state(observation):
    seat = int(observation["player"])
    step = int(observation["step"])
    state = _C115_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = {
            "last": -1,
            "streak": 0,
            "active": False,
            "counts": {
                "sale12_similarity_calls": 0,
                "sale12_active_calls": 0,
                "sale12_reservations": 0,
                "sale12_reserved_units": 0,
                "sale12_horizon_declines": 0,
                "sale12_errors": 0,
            },
            "due_steps": {},
            "items": {},
        }
        _C115_STATES[seat] = state
    state["last"] = step
    return state


def _c115_debts(seat):
    try:
        debts = _IMPL.chassis.players[seat]["sell_state"].get("r36_debts", {})
        return {int(due): {item: int(qty) for item, qty in rows.items()}
                for due, rows in debts.items()}
    except Exception:
        return {}


def _r36_reserve(observation, action):
    """Temporarily widen only the already-screened R36 reservation call."""
    seat = int(observation["player"])
    step = int(observation["step"])
    state = _C115_STATES.get(seat)
    if not (state and state.get("active") and 288 <= step < 696):
        return _C115_NATIVE_R36_RESERVE(observation, action)

    native_horizon = int(_R37_HORIZONS.get(seat, 0))
    if native_horizon != 8:
        state["counts"]["sale12_horizon_declines"] += 1
        return _C115_NATIVE_R36_RESERVE(observation, action)

    state["counts"]["sale12_active_calls"] += 1
    before = _c115_debts(seat)
    _R37_HORIZONS[seat] = 12
    try:
        result = _C115_NATIVE_R36_RESERVE(observation, action)
    finally:
        _R37_HORIZONS[seat] = native_horizon
    after = _c115_debts(seat)

    additions = []
    for due in range(step + 9, min(695, step + 12) + 1):
        for item, quantity in after.get(due, {}).items():
            added = quantity - before.get(due, {}).get(item, 0)
            if added > 0:
                additions.append((due, item, added))
    if additions:
        state["counts"]["sale12_reservations"] += 1
        state["counts"]["sale12_reserved_units"] += sum(row[2] for row in additions)
        for due, item, quantity in additions:
            key = str(due)
            state["due_steps"][key] = state["due_steps"].get(key, 0) + quantity
            state["items"][item] = state["items"].get(item, 0) + quantity
    return result


def agent(observation, configuration=None):
    state = _c115_state(observation)
    step = int(observation["step"])
    try:
        similar = 288 <= step < 696 and _r37_similarity(observation) >= 0.90
        state["streak"] = state["streak"] + 1 if similar else 0
        if similar:
            state["counts"]["sale12_similarity_calls"] += 1
        state["active"] = state["streak"] >= 6
    except Exception:
        state["streak"] = 0
        state["active"] = False
        state["counts"]["sale12_errors"] += 1

    result = _C115_PARENT(observation, configuration)
    _C115_REPORT.clear()
    _C115_REPORT.update(getattr(_C115_PARENT, "telemetry", {}))
    _C115_REPORT.update(state["counts"])
    _C115_REPORT["sale12_due_steps"] = dict(state["due_steps"])
    _C115_REPORT["sale12_items"] = dict(state["items"])
    _C115_REPORT["sale12_final_streak"] = state["streak"]
    return result


agent.telemetry = _C115_REPORT
# Kaggle 1.32.7 loads the last callable by insertion order.
agent = globals().pop("agent")

# SPDX-License-Identifier: Apache-2.0
"""Replace only route-10's day-6 COW pair with a financed SHEEP pair.

In live loss 108323339 the rival shared c111's route through step 149, then used
two sheep in the same two pastures for the exact YARN_STORE -> PET_CAFE opening.
This overlay rewrites the purchase and its four matching transport commands.  It
abstains unless the route signature, cash budget, purchase confirmation, carried
animals, and empty pasture targets all match observations.
"""

import copy as _c116_copy

_C116_PARENT = agent
_C116_STATES = {}
_C116_REPORT = {}
_C116_SEED_COST = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                   "STRAWBERRY": 100, "MELON": 80}
_C116_ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
_C116_LAND_COST = (1000, 2000, 4000)
del agent


def _c116_new_state(step=-1):
    return {"last": step, "phase": "idle", "targets": [], "counts": {
        "yarn_pet_routes_seen": 0,
        "yarn_pet_switch_requests": 0,
        "yarn_pet_purchases_confirmed": 0,
        "yarn_pet_pickups_rewritten": 0,
        "yarn_pet_placements_rewritten": 0,
        "yarn_pet_pairs_completed": 0,
        "yarn_pet_budget_declines": 0,
        "yarn_pet_shape_declines": 0,
        "yarn_pet_aborts": 0,
        "yarn_pet_errors": 0,
    }}


def _c116_count(state, name):
    state["counts"][name] = state["counts"].get(name, 0) + 1


def _c116_abort(state):
    if state.get("phase") not in ("idle", "complete", "aborted"):
        _c116_count(state, "yarn_pet_aborts")
    state["phase"] = "aborted"


def _c116_command(action, actor):
    if actor == 0:
        return list(action.get("farmer") or ["PASS"])
    hands = action.get("hands") or []
    return list(hands[actor - 1]) if actor <= len(hands) else ["PASS"]


def _c116_set(action, actor, command):
    if actor == 0:
        action["farmer"] = list(command)
    else:
        action["hands"][actor - 1] = list(command)


def _c116_budget(observation, orders, animal_index):
    """Ignore sale proceeds and require current cash to fund every purchase."""
    farm = observation["farms"][int(observation["player"])]
    unlocked_extra = max(0, len(farm["unlocked_quadrants"]) - 1)
    total = 0
    lands = 0
    for index, order in enumerate(orders):
        if not isinstance(order, list) or not order:
            return None
        op = order[0]
        if op == "SELL":
            continue
        if op == "BUY_LAND" and len(order) == 1:
            slot = unlocked_extra + lands
            if slot >= len(_C116_LAND_COST):
                return None
            total += _C116_LAND_COST[slot]
            lands += 1
        elif op == "BUY_PRODUCT" and len(order) == 3 and order[1] in ("WHEAT", "FERTILIZER"):
            total += max(0, int(order[2])) * (int(observation["market"]["prices"][order[1]]) + 10)
        elif op == "BUY_SEED" and len(order) == 3 and order[1] in _C116_SEED_COST:
            total += max(0, int(order[2])) * _C116_SEED_COST[order[1]]
        elif op == "BUY_ANIMAL" and len(order) == 3 and order[1] in _C116_ANIMAL_COST:
            animal = "SHEEP" if index == animal_index else order[1]
            total += max(0, int(order[2])) * _C116_ANIMAL_COST[animal]
        else:
            return None
    return total


def _c116_empty_pasture(observation, actor):
    seat = int(observation["player"])
    farm = observation["farms"][seat]
    positions = [farm["farmer"], *farm["hands"]]
    if actor >= len(positions):
        return None
    pos = list(positions[actor])
    tile = farm["tiles"][pos[1]][pos[0]]
    if not (isinstance(tile, dict) and tile.get("kind") == "PASTURE" and not tile.get("animal")):
        return None
    return pos


def _c116_controller(observation, parent, state):
    step = int(observation["step"])
    seat = int(observation["player"])
    shops = tuple(observation["town"].get("unlocked_shops", [])[:2])
    private = observation["private"]

    if step == 150 and state["phase"] == "idle" and shops == ("YARN_STORE", "PET_CAFE"):
        _c116_count(state, "yarn_pet_routes_seen")
        orders = parent.get("market") or []
        targets = [i for i, order in enumerate(orders)
                   if order == ["BUY_ANIMAL", "COW", 2]]
        signature = (len(targets) == 1 and len(parent.get("hands") or []) == 7
                     and _c116_command(parent, 0) == ["EAST"]
                     and _c116_command(parent, 7) == ["SOUTH"]
                     and sum(bool(o) and o[0] == "BUY_ANIMAL" for o in orders) == 1)
        if not signature:
            _c116_count(state, "yarn_pet_shape_declines")
            return parent
        budget = _c116_budget(observation, orders, targets[0])
        if budget is None or float(observation["farms"][seat]["money"]) < budget:
            _c116_count(state, "yarn_pet_budget_declines")
            return parent
        result = _c116_copy.deepcopy(parent)
        result["market"][targets[0]] = ["BUY_ANIMAL", "SHEEP", 2]
        state["phase"] = "requested"
        _c116_count(state, "yarn_pet_switch_requests")
        return result

    if state["phase"] == "requested" and step == 151:
        if private["shed"].get("SHEEP", 0) < 2 or _c116_command(parent, 7) != ["PICKUP", "COW"]:
            _c116_abort(state)
            return parent
        result = _c116_copy.deepcopy(parent)
        _c116_set(result, 7, ["PICKUP", "SHEEP"])
        state["phase"] = "pickup_one"
        _c116_count(state, "yarn_pet_purchases_confirmed")
        _c116_count(state, "yarn_pet_pickups_rewritten")
        return result

    if state["phase"] == "pickup_one" and step == 152:
        inventories = private["inventories"]
        valid = (len(inventories) > 7 and inventories[7].get("SHEEP", 0) > 0
                 and private["shed"].get("SHEEP", 0) > 0
                 and _c116_command(parent, 1) == ["PICKUP", "COW"])
        if not valid:
            _c116_abort(state)
            return parent
        result = _c116_copy.deepcopy(parent)
        _c116_set(result, 1, ["PICKUP", "SHEEP"])
        state["phase"] = "pickup_two"
        _c116_count(state, "yarn_pet_pickups_rewritten")
        return result

    if state["phase"] == "pickup_two" and step == 155:
        inventories = private["inventories"]
        target = _c116_empty_pasture(observation, 1)
        if (len(inventories) <= 1 or inventories[1].get("SHEEP", 0) <= 0
                or target is None or _c116_command(parent, 1) != ["PLACE", "COW"]):
            _c116_abort(state)
            return parent
        result = _c116_copy.deepcopy(parent)
        _c116_set(result, 1, ["PLACE", "SHEEP"])
        state["targets"].append(target)
        state["phase"] = "place_one"
        _c116_count(state, "yarn_pet_placements_rewritten")
        return result

    if state["phase"] == "place_one" and step == 156:
        inventories = private["inventories"]
        target = _c116_empty_pasture(observation, 7)
        if (len(inventories) <= 7 or inventories[7].get("SHEEP", 0) <= 0
                or target is None or _c116_command(parent, 7) != ["PLACE", "COW"]):
            _c116_abort(state)
            return parent
        result = _c116_copy.deepcopy(parent)
        _c116_set(result, 7, ["PLACE", "SHEEP"])
        state["targets"].append(target)
        state["phase"] = "confirm"
        _c116_count(state, "yarn_pet_placements_rewritten")
        return result

    if state["phase"] == "confirm" and step == 157:
        farm = observation["farms"][seat]
        complete = len(state["targets"]) == 2 and all(
            isinstance(farm["tiles"][pos[1]][pos[0]], dict)
            and farm["tiles"][pos[1]][pos[0]].get("animal") == "SHEEP"
            for pos in state["targets"])
        if complete:
            state["phase"] = "complete"
            _c116_count(state, "yarn_pet_pairs_completed")
        else:
            _c116_abort(state)
        return parent

    expected = {"requested": 151, "pickup_one": 152, "pickup_two": 155,
                "place_one": 156, "confirm": 157}
    if state["phase"] in expected and step > expected[state["phase"]]:
        _c116_abort(state)
    return parent


def agent(observation, configuration=None):
    step = int(observation["step"])
    seat = int(observation["player"])
    state = _C116_STATES.get(seat)
    if state is None or step <= state["last"]:
        state = _C116_STATES[seat] = _c116_new_state()
    state["last"] = step
    parent = _C116_PARENT(observation, configuration)
    result = parent
    try:
        supported = len(observation["farms"][seat]["tiles"]) == 10
        if configuration is not None:
            supported = supported and all(configuration.get(key, value) == value for key, value in (
                ("turnsPerDay", 24), ("shedCapacity", 100),
                ("maxMarketOrdersPerTurn", 10), ("farmHandCostMult", 1)))
        if supported and (step <= 157 or state["phase"] not in ("idle", "complete", "aborted")):
            result = _c116_controller(observation, parent, state)
    except Exception:
        _c116_count(state, "yarn_pet_errors")
        _c116_abort(state)
        result = parent
    _C116_REPORT.clear()
    _C116_REPORT.update(getattr(_C116_PARENT, "telemetry", {}))
    _C116_REPORT.update(state["counts"])
    _C116_REPORT["yarn_pet_phase"] = state["phase"]
    return result


agent.telemetry = _C116_REPORT
# Kaggle 1.32.7 loads the last callable by insertion order.
agent = globals().pop("agent")

# SPDX-License-Identifier: Apache-2.0
# Local terminal harvest-only proposal; upstream planner notices retained.
exec('def _proposals(run, actor, prices, max_per_actor):\n    """One/two resource bundles plus direct carry closure, replacing a baseline suffix."""\n    owners = {}\n    for event in run[\'events\']:\n        if \'acquired\' in event:\n            owners.setdefault((tuple(event[\'xy\']), event[\'op\']), set()).add(event[\'actor\'])\n    proposals = []\n    seen = set()\n    horizon = len(run[\'rows\'])\n    for offset in range(horizon):\n        farm, private = run[\'states\'][offset]\n        pos = tuple(farm[\'farmer\'] if actor == 0 else farm[\'hands\'][actor - 1])\n        inventory = private[\'inventories\'][actor]\n        carried = sum((prices.get(item, 0) * count for item, count in inventory.items()))\n        prefix_deposits = run[\'rows\'][offset - 1][\'deposited_by_actor\'][actor] if offset else {}\n        future_deposits = run[\'rows\'][-1][\'deposited_by_actor\'][actor]\n        obligation = sum((prices.get(item, 0) * (count - prefix_deposits.get(item, 0)) for item, count in future_deposits.items()))\n        bundles = []\n        for y, row in enumerate(farm[\'tiles\']):\n            for x, tile in enumerate(row):\n                if not isinstance(tile, dict):\n                    continue\n                xy, operations, value = ((x, y), [], 0)\n                if tile.get(\'yield_units\', 0) > 0:\n                    item = tile.get(\'crop\') if tile.get(\'kind\') == \'PLANT\' else ANIMALS.get(tile.get(\'animal\'), {}).get(\'product\')\n                    mature = item and (\'animal\' in tile or (START + offset) // 24 - tile[\'planted_day\'] >= CROPS[item][\'first_yield_day\'])\n                    if mature and (not owners.get((xy, \'HARVEST\'), set()) - {actor}):\n                        operations.append([\'HARVEST\'])\n                        value += prices[item] * tile[\'yield_units\']\n                if tile.get(\'fertilizer_available\') and \'animal\' in tile and (not owners.get((xy, \'COLLECT_FERTILIZER\'), set()) - {actor}):\n                    operations.append([\'COLLECT_FERTILIZER\'])\n                    value += prices[\'FERTILIZER\']\n                if operations:\n                    variants = [(operations, value)]\n                    # A zero-value fertilizer pickup must not make valuable\n                    # harvest-only delivery unreachable before the final turn.\n                    if operations == [[\'HARVEST\'], [\'COLLECT_FERTILIZER\']]:\n                        variants.append(([[\'HARVEST\']], value - prices[\'FERTILIZER\']))\n                    for optional_ops, optional_value in variants:\n                        distance = len(_walk(pos, xy)) + len(optional_ops) + len(_return(xy))\n                        if distance <= horizon - offset:\n                            bundles.append((xy, optional_ops, optional_value, distance))\n        bundles.sort(key=lambda b: (-b[2] / b[3], -b[2], b[0]))\n        variants = [([], carried)] if carried else []\n        for xy, ops, value, _ in bundles[:6]:\n            variants.append(([(xy, ops)], carried + value))\n        for first in bundles[:3]:\n            for second in bundles[:3]:\n                if first[0] != second[0]:\n                    variants.append(([(first[0], first[1]), (second[0], second[1])], carried + first[2] + second[2]))\n        for stops, value in variants:\n            route, cursor = ([], pos)\n            for xy, ops in stops:\n                route += _walk(cursor, xy) + ops\n                cursor = xy\n            route += _return(cursor)\n            if len(route) > horizon - offset:\n                continue\n            route += [[\'PASS\']] * (horizon - offset - len(route))\n            key = (offset, tuple((tuple(c) for c in route)))\n            if key not in seen:\n                seen.add(key)\n                proposals.append((value - obligation, offset, route, len(stops)))\n    proposals.sort(key=lambda p: (-p[0], p[1], p[2]))\n    direct = [p for p in proposals if p[3] == 0 and p[0] > 0][:2]\n    chosen = direct + [p for p in proposals if p not in direct]\n    return chosen[:max_per_actor]', _PLANNER_NS)
agent = globals().pop('agent')
# SPDX-License-Identifier: Apache-2.0
# Local research, 2026-09-13. Existing prefix dominance remains the default.
# A terminal detour must retain all final quantities and acquire enough extra
# non-fertilizer output to cover the initial-price value of every delayed unit.
# This is a conservative scoring heuristic, not proof of future market prices.
_P0_TERMINAL_ORIGINAL_DOMINATES = _PLANNER_NS['dominates']
_P0_TERMINAL_ORIGINAL_PLAN = _PLANNER_NS['plan_terminal']
_P0_TERMINAL_PRICES = {}

def _p0_terminal_value_dominates(candidate, baseline):
    if _P0_TERMINAL_ORIGINAL_DOMINATES(candidate, baseline):
        return True
    if candidate['overflow_units'] or not _P0_TERMINAL_PRICES:
        return False
    delta = {item: candidate['sold'].get(item, 0) - baseline['sold'].get(item, 0)
             for item in PRODUCTS}
    if any(q < 0 for q in delta.values()):
        return False
    gain = sum(q * _P0_TERMINAL_PRICES[item] for item, q in delta.items()
               if item != 'FERTILIZER')
    delay = sum(max([0] + [old['sold'].get(item, 0) - new['sold'].get(item, 0)
                          for new, old in zip(candidate['rows'], baseline['rows'])])
                * _P0_TERMINAL_PRICES[item] for item in PRODUCTS)
    return gain > max(50, delay + 10)

def _p0_terminal_plan(obs, config, baseline_remaining, **kwargs):
    global _P0_TERMINAL_PRICES
    _P0_TERMINAL_PRICES = {item: max(1, float(obs['market']['prices'].get(item, 1)))
                           for item in PRODUCTS}
    try:
        return _P0_TERMINAL_ORIGINAL_PLAN(obs, config, baseline_remaining, **kwargs)
    finally:
        _P0_TERMINAL_PRICES = {}

_PLANNER_NS['dominates'] = _p0_terminal_value_dominates
_PLANNER_NS['plan_terminal'] = _p0_terminal_plan
agent = globals().pop('agent')

# SPDX-License-Identifier: Apache-2.0
"""Conservative late feed abstention from current public prices and complete shops.

Do not remove purchases, pickups or routes. Abstain only from a currently valid
feed on low-margin cattle/sheep after all shops are known. Carried wheat remains
available to other animals and the existing physical liquidation path.
"""
import copy as _c124_copy

_C124_PARENT = agent
_C124_STATE = {}
_C124_REPORT = {}
_C124_SHOPS = {'COW': ('PIZZA_SHOP', 'SMOOTHIE_SHOP', 'ICE_CREAM_SHOP'),
               'SHEEP': ('YARN_STORE',)}
_C124_PRODUCTS = {'COW': 'MILK', 'SHEEP': 'WOOL'}
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    state = _C124_STATE.get(seat)
    if state is None or step <= state['last']:
        state = {'last': -1, 'feed_skips': 0, 'cow_skips': 0, 'sheep_skips': 0, 'errors': 0}
        _C124_STATE[seat] = state
    state['last'] = step
    parent_action = _C124_PARENT(observation, configuration)
    result = parent_action
    try:
        shops = observation.get('town', {}).get('unlocked_shops', [])
        if 504 <= step < 696 and len(shops) == 8:
            prices = observation['market']['prices']
            farm = observation['farms'][seat]
            inventories = observation['private']['inventories']
            positions = [farm['farmer'], *farm['hands']]
            commands = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
            replacements = []
            for actor, command in enumerate(commands[:len(positions)]):
                if command != ['FEED'] or actor >= len(inventories) or inventories[actor].get('WHEAT', 0) < 1:
                    continue
                x, y = positions[actor]
                tile = farm['tiles'][y][x]
                if not isinstance(tile, dict) or tile.get('animal') not in _C124_PRODUCTS or tile.get('fed_today'):
                    continue
                kind = tile['animal']
                if any(shop in shops for shop in _C124_SHOPS[kind]):
                    continue
                # Optimistically credit three product units plus one fertilizer
                # per feed, and demand a30% grain-value margin before abstaining.
                benefit = 3 * prices[_C124_PRODUCTS[kind]] + prices['FERTILIZER']
                if 10 * benefit >= 7 * prices['WHEAT']:
                    continue
                replacements.append((actor, kind))
            if replacements:
                result = _c124_copy.deepcopy(parent_action)
                for actor, kind in replacements:
                    if actor == 0:
                        result['farmer'] = ['PASS']
                    else:
                        result['hands'][actor-1] = ['PASS']
                    state['feed_skips'] += 1
                    state['cow_skips' if kind == 'COW' else 'sheep_skips'] += 1
    except Exception:
        state['errors'] += 1
        result = parent_action
    _C124_REPORT.clear()
    _C124_REPORT.update(getattr(_C124_PARENT, 'telemetry', {}))
    _C124_REPORT.update({'livestock_margin_' + key: value for key, value in state.items() if key != 'last'})
    return result


agent.telemetry = _C124_REPORT
agent = globals().pop('agent')

# SPDX-License-Identifier: Apache-2.0
"""Fund imminent grain pickups only for escape risk or productive livestock.

Only own known next-turn route, current observations and current cash are used.
The engine executes field actions before market orders, so buy one turn BEFORE
a scheduled pickup. Never change movement, hiring, crops or existing orders.
"""
_C126_PARENT = agent
_C126_STATE = {}
_C126_REPORT = {}
del agent


def _c126_buffer(obs, action, state):
    step = int(obs['step']); seat = int(obs['player'])
    # Leave opening, daily hand respawn, router changes and terminal plans alone.
    if not 144 <= step < 432 or step % 24 >= 22 or state['units'] >= 12:
        return action
    if state.get('day') != step // 24:
        state.update(day=step // 24, day_units=0)
    if state['day_units'] >= 4:
        return action
    farm = obs['farms'][seat]
    if len(farm['tiles']) != 10 or farm['money'] < 100:
        return action
    market = action.get('market', [])
    if len(market) >= 10 or any(not o or o[0] != 'SELL' for o in market):
        return action
    route = _IMPL.chassis.players[seat]['route']
    tape = _ROUTES[route]
    positions = [farm['farmer'], *farm['hands']]
    commands = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
    projected = projected_shed(action, FarmView(obs))
    wheat = projected.get('WHEAT', 0)
    for order in market:
        if len(order) >= 3 and order[:2] == ['SELL', 'WHEAT']:
            wheat = max(0, wheat-max(0, int(order[2])))
    demand = 0
    urgent = False
    for actor, pos in enumerate(positions):
        nxt = _cp0_command(tape[step+1], actor)
        if len(nxt) < 2 or nxt[:2] != ['PICKUP', 'WHEAT']:
            continue
        command = commands[actor] if actor < len(commands) else ['PASS']
        dx, dy = _CP0_MOVES.get(command[0], (0, 0))
        future_pos = (max(0, min(9, pos[0]+dx)), max(0, min(9, pos[1]+dy)))
        if not _shed_adjacent(future_pos, 10):
            continue
        # Use only a pickup that the known own route connects to a FEED today.
        end = min(step+10, (step//24+1)*24)
        cursor = list(future_pos)
        justified = False
        endangered = False
        for t in range(step+2, end):
            cmd = _cp0_command(tape[t], actor)
            if cmd == ['FEED']:
                tile = farm['tiles'][cursor[1]][cursor[0]]
                if isinstance(tile, dict) and tile.get('animal') and not tile.get('fed_today'):
                    first = {'COW': 8, 'SHEEP': 6, 'GOOSE': 4}[tile['animal']]
                    # Do not fund an immature animal's optional early care.
                    # Rescue imminent escape OR support an already productive animal.
                    endangered |= tile.get('consecutive_unfed', 0) >= 1
                    justified |= (tile.get('consecutive_unfed', 0) >= 1
                                  or step//24+1-tile['placed_day'] >= first)
            if cmd[0] in _CP0_MOVES:
                dx, dy = _CP0_MOVES[cmd[0]]
                cursor = [max(0, min(9, cursor[0]+dx)), max(0, min(9, cursor[1]+dy))]
        if not justified:
            continue
        urgent |= endangered
        demand += max(0, int(nxt[2]) if len(nxt) > 2 else 1)
    deficit = min(max(0, demand-wheat), 4-state['day_units'], 12-state['units'])
    # Preserve a cash floor (100 only for observed imminent escape, else500); room bound assumes no benefit from current sales.
    price = max(1, obs['market']['prices']['WHEAT'])
    reserve = 100 if urgent else 500
    if deficit <= 0 or sum(projected.values())+deficit > 96 or 2*price*deficit > farm['money']-reserve:
        return action
    result = copy.deepcopy(action)
    result.setdefault('market', []).append(['BUY_PRODUCT', 'WHEAT', deficit])
    state['emergency_events'] += int(urgent)
    state['units'] += deficit; state['day_units'] += deficit; state['events'] += 1
    return result


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    state = _C126_STATE.get(seat)
    if state is None or step <= state['last']:
        state = _C126_STATE[seat] = {'last': -1, 'units': 0, 'events': 0, 'errors': 0, 'emergency_events': 0}
    state['last'] = step
    parent = _C126_PARENT(observation, configuration)
    result = parent
    try:
        supported = configuration is None or all(configuration.get(k, v) == v for k, v in (
            ('turnsPerDay', 24), ('shedCapacity', 100), ('maxMarketOrdersPerTurn', 10)))
        if supported:
            result = _c126_buffer(observation, parent, state)
    except Exception:
        state['errors'] += 1
    _C126_REPORT.clear(); _C126_REPORT.update(getattr(_C126_PARENT, 'telemetry', {}))
    _C126_REPORT.update({'feed_buffer_'+k: state[k] for k in ('units', 'events', 'errors', 'emergency_events')})
    return result


agent.telemetry = _C126_REPORT
agent = globals().pop('agent')


# SPDX-License-Identifier: Apache-2.0
# o159_feed_margin (Claude/o-series, 2026-09-15; o158 + abandonment restricted to structural no-demand cases after o158 abandoned cows during transient MILK price crashes and lost 13/17 animals in episode 108735977). Overlay appended to c150 (parent untouched).
"""Marginal-value FEED gate.

Engine facts (kaggriculture 1.32.7, _daily_refresh_animals): animals PRODUCE on schedule whether
or not they were fed; feeding only (a) resets consecutive_unfed (escape at >=2) and (b) lets the
care bonus accrue (cared AND fed -> pending+1) and be consumed (fed on a production day ->
yield += 1 + pending; unfed on a production day zeroes pending). Production at the end of day 29
can never be sold. Hence each FEED is worth roughly ONE unit of the animal's product (the bonus
it enables), plus survival insurance when consecutive_unfed == 1. The parent tape feeds every
animal every day at ~$42 wheat even when MILK/WOOL trade below $20 (live elite-loss audit:
we make ~24 more cow feeds per game with MILK < $20 than the 2750+ cluster does).

Rule: replace a scheduled FEED by PASS when the feed's marginal value < WHEAT price, subject to
  - never skip when consecutive_unfed == 1 unless the animal is worthless for the rest of the game
    (all remaining sellable production + yield on tile < one wheat) -> deliberate abandonment;
  - never skip the same tile two days in a row (bounds escape risk if the tape stops feeding);
  - day 29: every FEED is worthless (skip); day 28 handled by the general value model (LAST=28).
Only removes FEED actions (turns them into PASS); never adds actions, orders, or moves.
"""
import copy as _o159_copy

_O159_PARENT = agent
_O159_STATE = {}
_O159_REPORT = {}
_O159_SPEC = {'GOOSE': (4, 1), 'COW': (8, 2), 'SHEEP': (6, 3)}       # first_yield_day, interval
_O159_PRODUCT = {'GOOSE': 'EGG', 'COW': 'MILK', 'SHEEP': 'WOOL'}
_O159_SHOPS = {'COW': ('PIZZA_SHOP', 'SMOOTHIE_SHOP', 'ICE_CREAM_SHOP'), 'SHEEP': ('YARN_STORE',), 'GOOSE': ('BRUNCH_SPOT', 'PET_CAFE', 'BAKERY')}
_O159_LAST_SELLABLE_DAY = 28
_O159_MARGIN = 0.6          # skip iff value < MARGIN * wheat price
_O159_MIN_DAY = 8           # never touch the opening (tape is fragile there)
del agent


def _o159_is_prod(kind, placed, day):
    first, interval = _O159_SPEC[kind]
    ds = (day + 1) - placed - first
    return ds >= 0 and ds % interval == 0


def _o159_value(tile, kind, day, prices):
    """Expected sellable product value (in $) that THIS feed protects/enables."""
    price = prices.get(_O159_PRODUCT[kind], 0)
    placed = int(tile.get('placed_day', 0))
    pending = int(tile.get('pending_care_bonus', 0) or 0)
    unfed = int(tile.get('consecutive_unfed', 0) or 0)
    held = int(tile.get('yield_units', 0) or 0)
    if day > _O159_LAST_SELLABLE_DAY:
        return 0.0, 0.0
    remaining = [d for d in range(day, _O159_LAST_SELLABLE_DAY + 1) if _o159_is_prod(kind, placed, d)]
    interval = _O159_SPEC[kind][1]
    # value if the animal survives the rest of the game (daily care assumed): base 1 + bonus per cycle
    future = sum(1 + (min(pending, interval) if i == 0 else min(interval, 3)) for i, _ in enumerate(remaining))
    abandon_value = price * (held + future)
    if unfed >= 1:
        return abandon_value, abandon_value
    if _o159_is_prod(kind, placed, day):
        return price * pending, abandon_value
    return (price * 1.0 if remaining else 0.0), abandon_value


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    day = step // 24
    st = _O159_STATE.get(seat)
    if st is None or step <= st['last']:
        st = {'last': -1, 'skipped_day': {}, 'skips': 0, 'abandons': 0, 'kept_survival': 0, 'errors': 0, 'day29_skips': 0}
        _O159_STATE[seat] = st
    st['last'] = step
    parent_action = _O159_PARENT(observation, configuration)
    result = parent_action
    try:
        if day >= _O159_MIN_DAY:
            prices = observation['market']['prices']
            wheat = float(prices.get('WHEAT', 0))
            farm = observation['farms'][seat]
            positions = [farm['farmer'], *farm['hands']]
            commands = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
            replacements = []
            for actor, command in enumerate(commands[:len(positions)]):
                if command != ['FEED']:
                    continue
                x, y = positions[actor]
                tile = farm['tiles'][y][x]
                if not isinstance(tile, dict) or tile.get('animal') not in _O159_SPEC or tile.get('fed_today'):
                    continue
                kind = tile['animal']
                key = (x, y)
                if day >= 29:
                    replacements.append((actor, key, 'day29')); continue
                value, abandon_value = _o159_value(tile, kind, day, prices)
                unfed = int(tile.get('consecutive_unfed', 0) or 0)
                if unfed >= 1:
                    shops = observation.get('town', {}).get('unlocked_shops', []) or []
                    structural = (len(shops) >= 8 and not any(sh in shops for sh in _O159_SHOPS[kind])
                                  and prices.get(_O159_PRODUCT[kind], 0) <= 3 and day >= 20)
                    if structural and abandon_value < _O159_MARGIN * wheat:
                        replacements.append((actor, key, 'abandon'))
                    else:
                        st['kept_survival'] += 1
                    continue
                if st['skipped_day'].get(key) == day - 1:
                    continue  # never two consecutive skips on one tile
                if value < _O159_MARGIN * wheat:
                    replacements.append((actor, key, 'skip'))
            if replacements:
                result = _o159_copy.deepcopy(parent_action)
                for actor, key, why in replacements:
                    if actor == 0:
                        result['farmer'] = ['PASS']
                    else:
                        result['hands'][actor - 1] = ['PASS']
                    if why == 'skip':
                        st['skipped_day'][key] = day; st['skips'] += 1
                    elif why == 'abandon':
                        st['abandons'] += 1
                    else:
                        st['day29_skips'] += 1
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O159_REPORT.clear()
    _O159_REPORT.update(getattr(_O159_PARENT, 'telemetry', {}))
    _O159_REPORT.update({'o159_' + k: v for k, v in st.items() if k not in ('last', 'skipped_day')})
    return result


agent.telemetry = _O159_REPORT
agent = globals().pop('agent')

# SPDX-License-Identifier: Apache-2.0
# o162_goose_only (Claude/o-series, 2026-09-15). Overlay appended to immutable parent agent/o159b_feed_margin06.py.
"""Goose-only harvest arm on top of o159b (feed-margin 0.6 and all its feed conditions unchanged).
COW and SHEEP CARE commands are returned exactly as the parent proposes; only GOOSE tiles at
yield_units >= 3 are switched from CARE to HARVEST.

Behaviour (identical to agent/overlays/o160_goose_harvest.py except the species table and
telemetry prefix): when the parent sends a worker to CARE an animal tile whose yield_units is at
or above the species threshold, that worker's command becomes HARVEST (worker already stands on
the tile). Parent commands that are FEED/HARVEST/PASS/moves and every market order are returned
untouched. No cash, price, opponent, seed or feed conditions are added.

Engine facts: GOOSE max_held 4 with 2 eggs/day when cared+fed, COW/SHEEP max_held 6; production
beyond max_held is silently lost until harvested.

Telemetry (prefix o162_): harvest_swap_requests_<SPECIES>, requested_units_<SPECIES> (units on
the tile at the moment of the request - a REQUEST count, not realised harvest or revenue),
errors. Parent telemetry is preserved.
"""
import copy as _o162_copy

_O162_PARENT = agent
_O162_STATE = {}
_O162_REPORT = {}
_O162_THRESH = {'GOOSE': 3}
del agent


def _o162_new_state():
    st = {'last': -1, 'errors': 0}
    for kind in _O162_THRESH:
        st['harvest_swap_requests_' + kind] = 0
        st['requested_units_' + kind] = 0
    return st


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O162_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O162_STATE[seat] = _o162_new_state()
    st['last'] = step
    parent_action = _O162_PARENT(observation, configuration)   # exactly one parent call per turn
    result = parent_action
    try:
        farm = observation['farms'][seat]
        positions = [farm['farmer'], *farm['hands']]
        commands = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
        swaps = []
        for actor, command in enumerate(commands[:len(positions)]):
            if command != ['CARE']:
                continue
            x, y = positions[actor]
            tile = farm['tiles'][y][x]
            if not isinstance(tile, dict) or tile.get('animal') not in _O162_THRESH:
                continue
            kind = tile['animal']
            units = int(tile.get('yield_units', 0) or 0)
            if units >= _O162_THRESH[kind]:
                swaps.append((actor, kind, units))
        if swaps:
            result = _o162_copy.deepcopy(parent_action)
            for actor, kind, units in swaps:
                if actor == 0:
                    result['farmer'] = ['HARVEST']
                else:
                    result['hands'][actor - 1] = ['HARVEST']
                st['harvest_swap_requests_' + kind] += 1
                st['requested_units_' + kind] += units
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O162_REPORT.clear()
    _O162_REPORT.update(getattr(_O162_PARENT, 'telemetry', {}))
    _O162_REPORT.update({'o162_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O162_REPORT
agent = globals().pop('agent')


# o171e_day6_goose_4 (shop_rule=True, four=True) (Claude/o-series, 2026-09-15). Overlay on o162.
"""Day-6 COW pair -> GOOSE pair when the first two shops show no milk demand (route 0/2 only).
Leader's first divergence from our lineage (r000 report): COW->GOOSE on day 6 in bakery/brunch/pet
worlds. Route 0 buys 2 COW at step 150 and places them on (5,4)/(5,3) via a fixed worker schedule;
this rewrites exactly that block (buy, 2 pickups, 2 pasture builds -> coops, 2 places) after a
signature check at step 150. Each later step is rewritten only if the parent command and worker
position match the expected schedule (otherwise counted in o171_mismatch and left untouched).
Variant flag _O171_NEED_EGG_SHOP: also require BAKERY/BRUNCH among the first two shops.
Telemetry: o171_mode, o171_rewrites, o171_mismatch, o171_errors.
"""
import copy as _o171_copy

_O171_PARENT = agent
_O171_STATE = {}
_O171_REPORT = {}
_O171_NEED_EGG_SHOP = False
_O171_SHOP_RULE = True      # False: substitute in every route-0 world
_O171_FOUR = True          # True: also the day-7 cows (steps 169/176) -> geese
_O171_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
_O171_EGG = ('BAKERY', 'BRUNCH_SPOT')
# step -> list of (worker index, expected parent command, expected worker position or None, new command)
_O171_SCHEDULE = {
    151: [(7, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    152: [(1, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    153: [(1, ['BUILD_PASTURE'], (5, 4), ['BUILD_COOP'])],
    155: [(7, ['BUILD_PASTURE'], (5, 3), ['BUILD_COOP']), (1, ['PLACE', 'COW'], (5, 4), ['PLACE', 'GOOSE'])],
    156: [(7, ['PLACE', 'COW'], (5, 3), ['PLACE', 'GOOSE'])],
}
_O171_SCHEDULE4 = {
    153: [(6, ['BUILD_PASTURE'], (5, 2), ['BUILD_COOP'])],
    159: [(1, ['BUILD_PASTURE'], (6, 4), ['BUILD_COOP'])],
    170: [(3, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    177: [(3, ['PLACE', 'COW'], (6, 4), ['PLACE', 'GOOSE']), (5, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    179: [(6, ['PICKUP', 'COW'], None, ['PICKUP', 'GOOSE'])],
    182: [(6, ['PLACE', 'COW'], (5, 2), ['PLACE', 'GOOSE'])],
}
_O171_BUY4 = (169, 176)
del agent


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O171_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O171_STATE[seat] = {'last': -1, 'mode': '', 'rewrites': 0, 'mismatch': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O171_PARENT(observation, configuration)
    result = parent_action
    try:
        if step == 150:
            shops = list(observation['town'].get('unlocked_shops', []))[:2]
            orders = parent_action.get('market') or []
            sig = (['BUY_ANIMAL', 'COW', 2] in orders and 'YARN_STORE' not in shops
                   and (not _O171_SHOP_RULE or not any(s in _O171_MILK for s in shops))
                   and (not _O171_NEED_EGG_SHOP or any(s in _O171_EGG for s in shops)))
            if sig:
                st['mode'] = 'GOOSE'
                result = _o171_copy.deepcopy(parent_action)
                for o in result['market']:
                    if o == ['BUY_ANIMAL', 'COW', 2]:
                        o[1] = 'GOOSE'; st['rewrites'] += 1
        elif st['mode'] and _O171_FOUR and step in _O171_BUY4 and ['BUY_ANIMAL', 'COW', 1] in (parent_action.get('market') or []):
            result = _o171_copy.deepcopy(parent_action)
            for o in result['market']:
                if o == ['BUY_ANIMAL', 'COW', 1]:
                    o[1] = 'GOOSE'; st['rewrites'] += 1
        elif st['mode'] and (step in _O171_SCHEDULE or (_O171_FOUR and step in _O171_SCHEDULE4)):
            farm = observation['farms'][seat]
            positions = [farm['farmer'], *farm['hands']]
            cmds = [parent_action.get('farmer')] + list(parent_action.get('hands') or [])
            out = None
            plan = list(_O171_SCHEDULE.get(step, [])) + (list(_O171_SCHEDULE4.get(step, [])) if _O171_FOUR else [])
            for idx, expect, pos, new in plan:
                ok = idx < len(cmds) and cmds[idx] == expect and (pos is None or (idx < len(positions) and tuple(positions[idx]) == pos))
                if not ok:
                    st['mismatch'] += 1
                    continue
                if out is None:
                    out = _o171_copy.deepcopy(parent_action)
                if idx == 0:
                    out['farmer'] = list(new)
                else:
                    out['hands'][idx - 1] = list(new)
                st['rewrites'] += 1
            if out is not None:
                result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O171_REPORT.clear()
    _O171_REPORT.update(getattr(_O171_PARENT, 'telemetry', {}))
    _O171_REPORT.update({'o171_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O171_REPORT
agent = globals().pop('agent')


# o170c_day10_livestock: COW only when all 3 known shops are milk shops (Claude/o-series, 2026-09-15). Overlay on o162.
"""Day-10 livestock substitution from observed shops (route 0/2 only).
The parent tape buys 3 GOOSE at steps 241/265 regardless of demand. At step 241 the three
known shops decide a replacement species for that whole purchase block:
  SHEEP if a YARN_STORE is among the 3 shops (route 0 means none in the first two);
  COW   if no egg shop (BAKERY/BRUNCH) and >=_O170_MILK_MIN milk shops;
  else keep GOOSE.
Whole block is substituted (buys, pickups, places, coop builds -> pasture) or nothing; the
day-10 purchase must fit in cash (2*cost + _O170_CASH_MARGIN) or the block is left as is.
Telemetry: o170_mode ('' / SHEEP / COW), o170_rewrites, o170_cash_declines, o170_errors.
"""
import copy as _o170_copy

_O170_PARENT = agent
_O170_STATE = {}
_O170_REPORT = {}
_O170_WINDOW = (241, 300)
_O170_MILK_MIN = 3
_O170_COW_NEEDS_NO_EGG = True
_O170_CASH_MARGIN = 350
_O170_COST = {'SHEEP': 500, 'COW': 400}
_O170_MILK = ('PIZZA_SHOP', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP')
_O170_EGG = ('BAKERY', 'BRUNCH_SPOT')
del agent


def _o170_choose(shops):
    if 'YARN_STORE' in shops:
        return 'SHEEP'
    milk = sum(s in _O170_MILK for s in shops)
    egg = sum(s in _O170_EGG for s in shops)
    if milk >= _O170_MILK_MIN and (egg == 0 or not _O170_COW_NEEDS_NO_EGG):
        return 'COW'
    return ''


def _o170_rewrite(action, target, st):
    out = _o170_copy.deepcopy(action)
    n = 0
    for o in out.get('market') or []:
        if o and o[0] == 'BUY_ANIMAL' and o[1] == 'GOOSE':
            o[1] = target; n += 1
    cmds = [out.get('farmer')] + list(out.get('hands') or [])
    for i, c in enumerate(cmds):
        if not c:
            continue
        new = None
        if c[0] in ('PICKUP', 'PLACE') and len(c) >= 2 and c[1] == 'GOOSE':
            new = [c[0], target] + list(c[2:])
        elif c[0] == 'BUILD_COOP':
            new = ['BUILD_PASTURE']
        if new is not None:
            n += 1
            if i == 0:
                out['farmer'] = new
            else:
                out['hands'][i - 1] = new
    st['rewrites'] += n
    return out if n else action


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O170_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O170_STATE[seat] = {'last': -1, 'mode': '', 'rewrites': 0, 'cash_declines': 0, 'errors': 0}
    st['last'] = step
    parent_action = _O170_PARENT(observation, configuration)
    result = parent_action
    try:
        if step == _O170_WINDOW[0]:
            orders = parent_action.get('market') or []
            goose = [o for o in orders if o and o[0] == 'BUY_ANIMAL' and o[1] == 'GOOSE']
            if goose:  # route 0/2 signature: the day-10 goose purchase is present
                shops = list(observation['town'].get('unlocked_shops', []))
                target = _o170_choose(shops)
                if target:
                    need = sum(int(o[2]) for o in goose) * _O170_COST[target] + _O170_CASH_MARGIN
                    if observation['farms'][seat]['money'] >= need:
                        st['mode'] = target
                    else:
                        st['cash_declines'] += 1
        if st['mode'] and _O170_WINDOW[0] <= step < _O170_WINDOW[1]:
            result = _o170_rewrite(parent_action, st['mode'], st)
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O170_REPORT.clear()
    _O170_REPORT.update(getattr(_O170_PARENT, 'telemetry', {}))
    _O170_REPORT.update({'o170_' + k: v for k, v in st.items() if k != 'last'})
    return result


agent.telemetry = _O170_REPORT
agent = globals().pop('agent')


# o174_tet_funding (Claude/o-series, 2026-09-15). Tetsutani-lineage funding/order-sequencing tail (EXP231 r97, r124 funded planting, r127 urgent grain slot, r128 service order) ported verbatim onto o162.
# Source: public notebook tetsutani/market-smart-farming-kaggriculture (2026-09-15 pull), lines 2725-3173; upstream notices retained inside.


# EXP231: protect inputs using funded current orders without unassigned cash padding from observed physical resources.
_R97_PARENT=agent
_R97_REPORT={}
_R97_LAST={}

def _r97_market_stock(shed,orders):
    stock=dict(shed);buys={};sales={}
    for index,order in enumerate(orders):
        if len(order)<3:continue
        op,item,n=order[:3];n=max(0,int(n))
        if op=='SELL':
            q=min(n,max(0,stock.get(item,0)));stock[item]=stock.get(item,0)-q;sales[index]=q
        elif op in ('BUY_PRODUCT','BUY_ANIMAL'):
            q=min(n,max(0,100-sum(stock.values())));stock[item]=stock.get(item,0)+q;buys[index]=q
    return stock,buys,sales

def _r97_delivery(stock,private,night):
    stock=dict(stock);lost={}
    if night:
        for inv in private['inventories']:
            for item,q in inv.items():
                q=max(0,int(q));take=min(q,max(0,100-sum(stock.values())))
                stock[item]=stock.get(item,0)+take
                if q>take:lost[item]=lost.get(item,0)+q-take
    return stock,lost

def _r97_budget(obs,orders):
    farm=obs['farms'][obs['player']];cost=0;hires=int(farm['hires_today'])
    # At most ten 100-unit purchases per opponent turn. The additional 1000
    # own units give an intentionally conservative upper bound on buy quotes.
    prices={p:_r37_market_price(p,obs['market']['inventory'][p]-2000) for p in ('WHEAT','FERTILIZER')}
    for order in orders:
        if not order:continue
        op=order[0]
        if op=='HIRE':cost+=_v219_fib(hires);hires+=1
        elif op=='BUY_LAND':cost+=4000
        elif len(order)>2:
            item=order[1];q=max(0,int(order[2]))
            if op=='BUY_PRODUCT':cost+=q*prices[item]
            elif op=='BUY_ANIMAL':cost+=q*{'GOOSE':300,'COW':400,'SHEEP':500}[item]
            elif op=='BUY_SEED':cost+=q*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[item]
    return cost<=farm['money']  # No current sale proceeds are assumed.

def _r97_supply(obs,action):
    step=int(obs['step']);player=int(obs['player']);day=step//24
    if not 144<=step<695:return action
    native=_IMPL.chassis.players[player]
    future=_IMPL.chassis.routes[2 if step+1>=648 else native['route']][step+1]
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    following=_IMPL.chassis.routes[2 if step+2>=648 else native['route']][step+2]
    next_orders=future.get('market') or []
    prefund=0
    if len(next_orders)==10 and not any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in next_orders):
        later=[following.get('farmer') or ['PASS'],*(following.get('hands') or [])]
        demand=lambda cs:sum(max(0,int(c[2]) if len(c)>2 else 1) for c in cs if c[:2]==['PICKUP','WHEAT'])
        if demand(later):prefund=demand(commands)+demand(later)
    if not prefund and not any(c[:2]==['PICKUP','WHEAT'] for c in commands):return action
    orders=action.get('market') or []
    if len(orders)>10 or not _r97_budget(obs,orders):
        _R97_REPORT['supply_budget_declines']+=1;return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][player],obs['private'])
    for actor,c in enumerate([action.get('farmer') or ['PASS'],*(action.get('hands') or [])][:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])];night=step%24==23
    access=((4,4),(5,4),(4,5),(5,5))
    if night:positions=[(4,4)]
    else:
        for order in orders:
            if order and order[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    need=sum(max(0,int(c[2]) if len(c)>2 else 1) for pos,c in zip(positions,commands) if pos in access and c[:2]==['PICKUP','WHEAT'])
    need=max(need,prefund)
    if not need:return action
    original_stock,original_buys,_=_r97_market_stock(private['shed'],orders)
    original_final,original_loss=_r97_delivery(original_stock,private,night)
    if original_final.get('WHEAT',0)>=need:return action
    result=copy.deepcopy(action);proposed=result['market'];blocked=False
    def project(candidate):
        stock,buys,sales=_r97_market_stock(private['shed'],candidate)
        final,loss=_r97_delivery(stock,private,night)
        safe=all(buys.get(i,0)>=q for i,q in original_buys.items()) and all(q<=original_loss.get(item,0) for item,q in loss.items())
        return final,sales,safe
    # Hold an existing grain sale first. Preserve all order indices and every
    # originally funded buy; no extra overnight overflow may be introduced.
    for index in range(len(proposed)-1,-1,-1):
        if proposed[index][:2]!=['SELL','WHEAT']:continue
        final,sales,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
        if not shortage:break
        sold=sales.get(index,0)
        if not sold:continue
        old=proposed[index][2];proposed[index][2]=max(0,sold-shortage)
        after,_,safe=project(proposed)
        if not safe or after.get('WHEAT',0)<=final.get('WHEAT',0):proposed[index][2]=old
    final,_,safe=project(proposed);shortage=max(0,need-final.get('WHEAT',0))
    if shortage:
        last_sale=max((i for i,o in enumerate(proposed) if o[:2]==['SELL','WHEAT']),default=-1)
        index=next((i for i in range(len(proposed)-1,last_sale,-1) if proposed[i][:2]==['BUY_PRODUCT','WHEAT']),None)
        if index is not None:proposed[index][2]=max(0,int(proposed[index][2]))+shortage
        elif len(proposed)<10:proposed.append(['BUY_PRODUCT','WHEAT',shortage])
        else:_R97_REPORT['supply_slot_declines']+=1;return action
    final,_,safe=project(proposed)
    if not safe or final.get('WHEAT',0)<need:
        _R97_REPORT['supply_capacity_declines']+=1;return action
    if not _r97_budget(obs,proposed):
        _R97_REPORT['supply_budget_declines']+=1;return action
    if prefund:
        _R97_REPORT['supply_prefund_changes']+=1
        _R97_REPORT['supply_prefund_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    if step<288:
        _R97_REPORT['supply_early_changes']+=1
        _R97_REPORT['supply_early_units']+=max(0,final.get('WHEAT',0)-original_final.get('WHEAT',0))
    _R97_REPORT['supply_guard_changes']+=1
    _R97_REPORT['supply_grain_protected']+=final.get('WHEAT',0)-original_final.get('WHEAT',0)
    _R97_REPORT['supply_buy_units']+=sum(max(0,int(o[2])) for o in proposed if o[:2]==['BUY_PRODUCT','WHEAT'])-sum(max(0,int(o[2])) for o in orders if o[:2]==['BUY_PRODUCT','WHEAT'])
    return result

def agent(observation,configuration=None):
    result=_R97_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step'])
        if player not in _R97_LAST or step<=_R97_LAST[player]:
            _R97_REPORT.update(supply_guard_changes=0,supply_grain_protected=0,supply_buy_units=0,supply_early_changes=0,supply_early_units=0,supply_prefund_changes=0,supply_prefund_units=0,supply_slot_declines=0,supply_capacity_declines=0,supply_budget_declines=0,supply_errors=0)
        _R97_LAST[player]=step
        if configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)]):result=_r97_supply(observation,result)
    except Exception:_R97_REPORT['supply_errors']=_R97_REPORT.get('supply_errors',0)+1
    _R97_REPORT.update(getattr(_R97_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R97_REPORT
agent=globals().pop('agent')

"""Original funded planting and first-dawn labor contract, Ahmed Berat Ozer."""
_R124_PARENT=agent
_R124_STATES={}
_R124_REPORT={}

def _r124_labor_reserve(native):
    n=sum(bool(o) and o[0]=='HIRE' for o in native[24].get('market',[]))
    return sum(_v219_fib(i) for i in range(n)),n

def _r124_seed_budget(obs,action,reserve):
    if not any(o and o[0]=='BUY_SEED' for o in action.get('market',[])):return action
    player=int(obs['player']);budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][player]['money']-=reserve
    if _r97_budget(budget,action.get('market',[])):return action
    result=copy.deepcopy(action)
    for i in range(len(result['market'])-1,-1,-1):
        order=result['market'][i]
        if len(order)<3 or order[0]!='BUY_SEED':continue
        before=max(0,int(order[2]));order[2]=before
        while order[2]>0 and not _r97_budget(budget,result['market']):order[2]-=1
        n=before-order[2]
        if n:
            _R124_REPORT['opening_seed_budget_units']+=n
            _R124_REPORT['opening_seed_budget_cost']+=n*{'WHEAT':10,'CARROT':20,'TOMATO':50,'STRAWBERRY':100,'MELON':80}[order[1]]
        if _r97_budget(budget,result['market']):break
    return result

def _r124_atomic(obs,action,state):
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    if not demand:return action
    available=obs['private']['seeds'];blocked={p for p,n in demand.items() if n>available.get(p,0)}
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    changed=False;kept=[]
    for actor,c in enumerate(commands):
        if len(c)>1 and c[0]=='PLANT':
            pos=None if actor>=len(private['inventories']) else farm['farmer'] if actor==0 else farm['hands'][actor-1]
            valid=pos is not None and farm['tiles'][pos[1]][pos[0]] is None and private['seeds'].get(c[1],0)>0
            if not valid:
                commands[actor]=['PASS'];changed=True;_R124_REPORT['opening_atomic_dropped']+=1
            elif c[1] in blocked:
                kept.append(dict(xy=list(pos),crop=c[1],birth=0));_R124_REPORT['opening_atomic_rescued_requests']+=1
        if actor<len(private['inventories']):_PLANNER_NS['_apply_unit_action'](farm,private,actor,commands[actor],10,0,24,100)
    if kept:state['pending_plants']=kept
    if changed:
        action=dict(action,farmer=commands[0],hands=commands[1:])
    return action

def agent(observation,configuration=None):
    result=_R124_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step']);state=_R124_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R124_STATES[player]={'step':-1,'pending_plants':[]}
            _R124_REPORT.update(opening_seed_budget_units=0,opening_seed_budget_cost=0,opening_atomic_dropped=0,opening_atomic_rescued_requests=0,opening_atomic_rescued_confirmed=0,opening_atomic_plant_errors=0,opening_day1_cash=0,opening_day1_hires_requested=0,opening_day1_hires_confirmed=0,opening_day1_hire_shortfalls=0,opening_contract_errors=0)
        state['step']=step;farm=observation['farms'][player]
        for p in state.pop('pending_plants',[]):
            x,y=p['xy'];t=farm['tiles'][y][x]
            if isinstance(t,dict) and t.get('crop')==p['crop'] and t.get('planted_day')==p['birth']:_R124_REPORT['opening_atomic_rescued_confirmed']+=1
            else:_R124_REPORT['opening_atomic_plant_errors']+=1
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard and 0<=step<24:
            native=_ROUTES[_IMPL.chassis.players[player]['route']];reserve,hires=_r124_labor_reserve(native)
            result=_r124_seed_budget(observation,result,reserve);result=_r124_atomic(observation,result,state)
        if step==24:
            _R124_REPORT['opening_day1_cash']=farm['money'];state['hires']=sum(bool(o) and o[0]=='HIRE' for o in result.get('market',[]));_R124_REPORT['opening_day1_hires_requested']=state['hires']
        if step==25:
            actual=len(farm['hands']);_R124_REPORT['opening_day1_hires_confirmed']=actual;_R124_REPORT['opening_day1_hire_shortfalls']=max(0,state.get('hires',0)-actual)
    except Exception:_R124_REPORT['opening_contract_errors']=_R124_REPORT.get('opening_contract_errors',0)+1
    _R124_REPORT.update(getattr(_R124_PARENT,'telemetry',{}))
    return result
agent.telemetry=_R124_REPORT
agent=globals().pop('agent')

"""Fund urgent grain at the first quote slot; avoid unwatered last-hour plants.
Original safety contracts by Ahmed Berat Ozer, EXP258.
"""
_R127_PARENT=agent
_R127_STATES={}
_R127_REPORT={}

def _r127_fields(obs,action):
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={p for p,n in demand.items() if n>private['seeds'].get(p,0)}
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:continue
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,int(obs['step'])//24,24,100)
    return farm,private

def _r127_last_hour(obs,action):
    if int(obs['step'])%24!=23:return action
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    if not any(c and c[0]=='PLANT' for c in commands):return action
    result=copy.deepcopy(action);changed=False
    # Removing rejected requests can unblock the engine's atomic crop batch.
    # Recompute until every retained request ends the turn with a watered crop.
    for _ in range(len(commands)+1):
        farm,_=_r127_fields(obs,result);original=obs['farms'][obs['player']]
        positions=[original['farmer'],*original['hands']];drop=[]
        for actor,c in enumerate(commands):
            if not c or c[0]!='PLANT':continue
            tile=None
            if actor<len(positions):
                x,y=positions[actor];tile=farm['tiles'][y][x]
            if not (isinstance(tile,dict) and tile.get('kind')=='PLANT' and tile.get('crop')==c[1] and tile.get('planted_day')==int(obs['step'])//24 and tile.get('watered_today')):drop.append(actor)
        if not drop:break
        for actor in drop:commands[actor]=['PASS']
        result['farmer']=commands[0];result['hands']=commands[1:];changed=True
        _R127_REPORT['last_hour_plants_dropped']+=len(drop)
    return result if changed else action

def _r127_prefix_bound(obs,quantity):
    inventory=int(obs['market']['inventory']['WHEAT'])
    # Both players quote one unit before either commits. Before own unit j,
    # at most j-1 own and j-1 opponent wheat purchases have depleted inventory.
    return sum(_r37_market_price('WHEAT',inventory-(2*j-1)) for j in range(1,quantity+1))

def _r127_priority(obs,action,state):
    step=int(obs['step']);player=int(obs['player'])
    if not 144<=step<695:return action
    orders=action.get('market') or []
    if len(orders)>9 or any(o[:2] in (['BUY_PRODUCT','WHEAT'],['SELL','WHEAT']) for o in orders):return action
    native=_IMPL.chassis.players[player]
    future=_IMPL.chassis.routes[2 if step+1>=648 else native['route']][step+1]
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    if not any(c[:2]==['PICKUP','WHEAT'] for c in commands):return action
    if not _r97_budget(obs,orders):return action
    farm,private=_r127_fields(obs,action);night=step%24==23
    access=((4,4),(5,4),(4,5),(5,5));positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    if night:positions=[(4,4)]
    else:
        for o in orders:
            if o and o[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    need=sum(max(0,int(c[2]) if len(c)>2 else 1) for pos,c in zip(positions,commands) if pos in access and c[:2]==['PICKUP','WHEAT'])
    stock,buys,_=_r97_market_stock(private['shed'],orders);before,loss=_r97_delivery(stock,private,night)
    shortage=max(0,need-before.get('WHEAT',0))
    if not shortage or shortage>100-sum(private['shed'].values()):return action
    cost=_r127_prefix_bound(obs,shortage)
    budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][player]['money']-=cost
    if not _r97_budget(budget,orders):return action
    proposed=[['BUY_PRODUCT','WHEAT',shortage],*copy.deepcopy(orders)]
    stock,after_buys,_=_r97_market_stock(private['shed'],proposed);after,after_loss=_r97_delivery(stock,private,night)
    if after.get('WHEAT',0)<need or any(after_buys.get(i+1,0)<q for i,q in buys.items()) or any(q>loss.get(p,0) for p,q in after_loss.items()):return action
    state['pending_grain']=(step+1,after.get('WHEAT',0),shortage)
    _R127_REPORT['priority_grain_orders']+=1;_R127_REPORT['priority_grain_units']+=shortage
    return dict(action,market=proposed)

def agent(observation,configuration=None):
    result=_R127_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step']);state=_R127_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R127_STATES[player]={'step':-1}
            _R127_REPORT.update(last_hour_plants_dropped=0,priority_grain_orders=0,priority_grain_units=0,priority_grain_confirmed=0,priority_grain_shortfalls=0,priority_contract_errors=0)
        pending=state.pop('pending_grain',None)
        if pending and step==pending[0]:
            if observation['private']['shed'].get('WHEAT',0)>=pending[1]:_R127_REPORT['priority_grain_confirmed']+=pending[2]
            else:_R127_REPORT['priority_grain_shortfalls']+=1
        state['step']=step
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard:result=_r127_priority(observation,_r127_last_hour(observation,result),state)
    except Exception:_R127_REPORT['priority_contract_errors']=_R127_REPORT.get('priority_contract_errors',0)+1
    _R127_REPORT.update(getattr(_R127_PARENT,'telemetry',{}))
    return result
agent.telemetry=_R127_REPORT
agent=globals().pop('agent')

"""Observed-input service order and guaranteed first-sale funding, Ahmed Berat Ozer."""
_R128_PARENT=agent
_R128_STATES={}
_R128_REPORT={}

def _r128_commands(action):
    return [action.get('farmer') or ['PASS'],*(action.get('hands') or [])]

def _r128_future(obs,offset=1):
    step=int(obs['step'])+offset;native=_IMPL.chassis.players[int(obs['player'])]
    return _IMPL.chassis.routes[2 if step>=648 else native['route']][step]

def _r128_sale_credit(obs,action):
    orders=action.get('market') or []
    if not orders or len(orders[0])<3 or orders[0][0]!='SELL' or orders[0][1]=='WHEAT':return 0
    item=orders[0][1]
    if item not in obs['market']['inventory']:return 0
    _,private=_r127_fields(obs,action)
    q=min(max(0,int(orders[0][2])),max(0,int(private['shed'].get(item,0))))
    inventory=int(obs['market']['inventory'][item])
    return sum(_r37_market_price(item,inventory+2*j) for j in range(q))

def _r128_next_need(obs,farm,orders,advanced):
    step=int(obs['step']);access=((4,4),(5,4),(4,5),(5,5))
    positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    if step%24==23:positions=[(4,4)]
    else:
        for order in orders:
            if order and order[0]=='HIRE':positions.append(min(access,key=lambda p:(positions.count(p),access.index(p))))
    return sum(max(0,int(c[2]) if len(c)>2 else 1) for actor,(p,c) in enumerate(zip(positions,_r128_commands(_r128_future(obs)))) if actor not in advanced and p in access and c[:2]==['PICKUP','WHEAT'])

def _r128_field_safe(obs,before,after,advanced):
    orders=before.get('market') or []
    if not _r97_budget(obs,orders):return False,None
    oldfarm,oldprivate=_r127_fields(obs,before);farm,private=_r127_fields(obs,after)
    oldcommands=_r128_commands(before);commands=_r128_commands(after)
    for i,c in enumerate(oldcommands[:len(private['inventories'])]):
        if c and c[0]=='PICKUP' and c==commands[i]:
            item=c[1]
            if private['inventories'][i].get(item,0)<oldprivate['inventories'][i].get(item,0):return False,None
    oldstock,oldbuys,oldsales=_r97_market_stock(oldprivate['shed'],orders)
    stock,buys,sales=_r97_market_stock(private['shed'],orders)
    oldfinal,oldloss=_r97_delivery(oldstock,oldprivate,int(obs['step'])%24==23)
    final,loss=_r97_delivery(stock,private,int(obs['step'])%24==23)
    if any(buys.get(i,0)<q for i,q in oldbuys.items()) or any(sales.get(i,0)<q for i,q in oldsales.items()) or any(q>oldloss.get(p,0) for p,q in loss.items()):return False,None
    need=_r128_next_need(obs,farm,orders,advanced)
    pending=_R127_STATES.get(int(obs['player']),{}).get('pending_grain')
    if pending and pending[0]==int(obs['step'])+1:need=max(need,pending[1])
    if final.get('WHEAT',0)<min(need,oldfinal.get('WHEAT',0)):return False,None
    return True,private

def _r128_food_need(obs,farm,private,actor):
    farm,private=copy.deepcopy(farm),copy.deepcopy(private);missing=0;day=int(obs['step'])//24
    for offset in range(1,min(5,24-int(obs['step'])%24)):
        cs=_r128_commands(_r128_future(obs,offset));c=cs[actor] if actor<len(cs) else ['PASS']
        if c[:2]==['PICKUP','WHEAT']:break
        if c==['FEED']:
            x,y=farm['farmer'] if actor==0 else farm['hands'][actor-1];tile=farm['tiles'][y][x]
            if isinstance(tile,dict) and tile.get('animal') and not tile.get('fed_today') and private['inventories'][actor].get('WHEAT',0)<=0:
                private['inventories'][actor]['WHEAT']=1;missing+=1
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,day,24,100)
    return missing

def _r128_service(obs,action,state):
    step=int(obs['step']);farm=obs['farms'][obs['player']];private=obs['private'];positions=[farm['farmer'],*farm['hands']]
    for item in state.pop('arrivals',[]):
        if item['step']!=step or item['actor']>=len(private['inventories']) or private['inventories'][item['actor']].get('WHEAT',0)<item['expected']:_R128_REPORT['service_arrival_errors']+=1
        else:_R128_REPORT['service_confirmed_units']+=item['quantity']
    old_pending=state.pop('swaps',{});result=action;cs=_r128_commands(result)
    for actor,pending in old_pending.items():
        if step!=pending['step'] or actor>=len(positions) or list(positions[actor])!=pending['xy'] or cs[actor]!=pending['pickup']:
            _R128_REPORT['service_swap_errors']+=1;continue
        x,y=positions[actor];tile=farm['tiles'][y][x]
        if not isinstance(tile,dict) or tile.get('animal')!=pending['animal'] or tile.get('placed_day')!=pending['birth']:
            _R128_REPORT['service_swap_errors']+=1;continue
        if private['inventories'][actor].get('WHEAT',0)<pending['quantity']+1:
            _R128_REPORT['service_swap_errors']+=1;continue
        cs[actor]=['PASS'] if tile.get('fed_today') else ['FEED']
        _R128_REPORT['service_swaps_completed']+=1
    if old_pending:
        proposed=dict(result,farmer=cs[0],hands=cs[1:]);safe,_=_r128_field_safe(obs,result,proposed,{})
        if safe:result=proposed
        else:_R128_REPORT['service_swap_errors']+=1
    if not 144<=step<647:return result
    cs=_r128_commands(result);future=_r128_commands(_r128_future(obs));proposed=copy.deepcopy(result);commands=_r128_commands(proposed)
    swaps={};arrivals=[];prefetches=0
    projected_farm,projected_private=_r127_fields(obs,result)
    for actor,c in enumerate(cs[:len(private['inventories'])]):
        x,y=positions[actor]
        if (x,y) not in ((4,4),(5,4),(4,5),(5,5)):continue
        held=max(0,int(private['inventories'][actor].get('WHEAT',0)));tile=farm['tiles'][y][x]
        nxt=future[actor] if actor<len(future) else ['PASS']
        if c==['FEED'] and held==0 and step%24<=21 and isinstance(tile,dict) and tile.get('animal') and not tile.get('fed_today') and nxt[:2]==['PICKUP','WHEAT']:
            q=max(0,int(nxt[2]) if len(nxt)>2 else 1)
            if not q:continue
            commands[actor]=['PICKUP','WHEAT',q+1]
            swaps[actor]=dict(step=step+1,xy=[x,y],animal=tile['animal'],birth=tile.get('placed_day'),quantity=q,pickup=copy.deepcopy(nxt))
            arrivals.append(dict(step=step+1,actor=actor,expected=q+1,quantity=q+1))
        elif c==['PASS']:
            q=_r128_food_need(obs,projected_farm,projected_private,actor)
            if q:
                commands[actor]=['PICKUP','WHEAT',q];prefetches+=1
                arrivals.append(dict(step=step+1,actor=actor,expected=held+q,quantity=q))
    if not arrivals:return result
    proposed['farmer']=commands[0];proposed['hands']=commands[1:]
    safe,after=_r128_field_safe(obs,result,proposed,swaps)
    if not safe or any(after['inventories'][p['actor']].get('WHEAT',0)<p['expected'] for p in arrivals):
        _R128_REPORT['service_capacity_declines']+=1;return result
    state['swaps']=swaps;state['arrivals']=arrivals
    _R128_REPORT['service_swaps_started']+=len(swaps);_R128_REPORT['service_idle_preloads']+=prefetches
    _R128_REPORT['service_requested_units']+=sum(p['quantity'] for p in arrivals)
    return proposed

def _r128_credit_supply(obs,action,state):
    step=int(obs['step'])
    if not 144<=step<695 or _r97_budget(obs,action.get('market') or []):return action
    credit=_r128_sale_credit(obs,action)
    if not credit:return action
    budget=dict(obs,farms=[dict(f) for f in obs['farms']]);budget['farms'][obs['player']]['money']+=credit
    if not _r97_budget(budget,action.get('market') or []):return action
    result=_r97_supply(budget,action)
    if result==action:return action
    assert result['market'][0]==action['market'][0]
    _,private=_r127_fields(obs,result);stock,_,_=_r97_market_stock(private['shed'],result['market']);final,_=_r97_delivery(stock,private,step%24==23)
    quantity=lambda a:sum(max(0,int(o[2])) for o in a.get('market',[]) if len(o)>2 and o[:2]==['BUY_PRODUCT','WHEAT'])
    extra=max(0,quantity(result)-quantity(action));state['credit_pending']=(step+1,final.get('WHEAT',0),extra)
    _R128_REPORT['sale_credit_orders']+=1;_R128_REPORT['sale_credit_lower_bound']+=credit;_R128_REPORT['sale_credit_grain_units']+=extra
    return result

def agent(observation,configuration=None):
    result=_R128_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step']);state=_R128_STATES.get(player)
        if state is None or step<=state['step']:
            state=_R128_STATES[player]={'step':-1}
            _R128_REPORT.update(service_requested_units=0,service_confirmed_units=0,service_idle_preloads=0,service_swaps_started=0,service_swaps_completed=0,service_capacity_declines=0,service_arrival_errors=0,service_swap_errors=0,sale_credit_orders=0,sale_credit_lower_bound=0,sale_credit_grain_units=0,sale_credit_confirmed_units=0,sale_credit_errors=0,service_errors=0)
        state['step']=step;pending=state.pop('credit_pending',None)
        if pending:
            if pending[0]!=step or observation['private']['shed'].get('WHEAT',0)<pending[1]:_R128_REPORT['sale_credit_errors']+=1
            else:_R128_REPORT['sale_credit_confirmed_units']+=pending[2]
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard:result=_r128_credit_supply(observation,_r128_service(observation,result,state),state)
    except Exception:_R128_REPORT['service_errors']=_R128_REPORT.get('service_errors',0)+1
    _R128_REPORT.update(getattr(_R128_PARENT,'telemetry',{}));_R128_REPORT.update(_R97_REPORT)
    return result
agent.telemetry=_R128_REPORT

agent = globals().pop('agent')   # keep 'agent' the last callable for Kaggle's loader


# o177_tet_grain (Claude/o-series, 2026-09-15). Tetsutani-lineage EXP226 grain retention (keep physical grain two days before trimming a buy) ported verbatim onto o162.
# Source: public notebook tetsutani/market-smart-farming-kaggriculture (2026-09-15 pull), lines 2657-2723; upstream notices retained inside.


# EXP226: retain physical grain for two complete days before trimming a buy.
_R95_PARENT = agent
_R95_REPORT = {}
_R95_RESERVES = {}

def _r95_reserve(obs):
    step=int(obs['step']);player=int(obs['player'])
    native=_IMPL.chassis.players[player];route=native['route']
    key=(route,step)
    if key not in _R95_RESERVES:
        demand=6  # Physical buffer beyond every scheduled pickup and sale.
        for t in range(step+1,min(719,step+49)):
            a=_IMPL.chassis.routes[2 if t>=648 else route][t]
            for c in [a.get('farmer') or ['PASS'],*(a.get('hands') or [])]:
                if c[:2]==['PICKUP','WHEAT']:
                    demand+=max(0,int(c[2]) if len(c)>2 else 1)
            for o in a.get('market',[]):
                if len(o)>2 and o[:2]==['SELL','WHEAT']:
                    demand+=max(0,int(o[2]))
        _R95_RESERVES[key]=demand
    demand=_R95_RESERVES[key]
    # Reserve full feed for a possible southeast sheep commitment. Do not
    # rely on its future discretionary buy, eligibility, or existing cargo.
    if obs['town']['unlocked_shops'].count('YARN_STORE')>=2:
        demand+=6*len({t//24 for t in range(step+1,step+49) if t//24>=12})
    return demand

def _r95_replenish(obs,action):
    step=int(obs['step'])
    if not 10<=step//24<=11:return action
    orders=action.get('market') or []
    if not any(len(o)>2 and o[:2]==['BUY_PRODUCT','WHEAT'] and int(o[2])>0 for o in orders):return action
    # Preserve all same-turn grain trading/arbitrage sequences unchanged.
    if any(o[:2]==['SELL','WHEAT'] for o in orders):return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    commands=[action.get('farmer') or ['PASS'],*(action.get('hands') or [])]
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,step//24,24,100)
    held=max(0,int(private['shed'].get('WHEAT',0)))
    reserve=_r95_reserve(obs);result=None;removed=0
    for i,o in enumerate(orders):
        if len(o)<3 or o[:2]!=['BUY_PRODUCT','WHEAT']:continue
        quantity=max(0,int(o[2]));retained=min(quantity,max(0,reserve-held))
        held+=retained
        if retained<quantity:
            if result is None:result=copy.deepcopy(action)
            result['market'][i][2]=retained  # Zero keeps every later order slot.
            removed+=quantity-retained
    if result is None:return action
    _R95_REPORT['replenishment_trim_turns']+=1
    _R95_REPORT['replenishment_trim_units']+=removed
    return result

def agent(observation,configuration=None):
    result=_R95_PARENT(observation,configuration)
    try:
        if int(observation['step'])==0:
            _R95_REPORT.update(replenishment_trim_turns=0,replenishment_trim_units=0,replenishment_errors=0)
        if configuration is not None and any(configuration.get(k,v)!=v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)]):return result
        result=_r95_replenish(observation,result)
    except Exception:
        _R95_REPORT['replenishment_errors']=_R95_REPORT.get('replenishment_errors',0)+1
    _R95_REPORT.update(getattr(_R95_PARENT,'telemetry',{}))
    return result

agent.telemetry=_R95_REPORT

agent = globals().pop('agent')   # keep 'agent' the last callable for Kaggle's loader


# o182_v43_overflow (Claude/o-series, 2026-09-15). ahmedberatozer V43 "Recovering Lost Harvests" r148 block ported verbatim.
# Sells existing stock at hour 23 only when otherwise-destroyed dawn cargo would replace it (complete shed vector unchanged).
# Requires the r97/r127 helpers from the o174 port (stack after o174). Source: public notebook lines 3192-3329; upstream notices retained.


_R148_OVERFLOW=True
_R148_SEEDS=False
# Original targeted contracts, Ahmed Berat Ozer, EXP277.
# Uses only current observations and the agent's own existing raw plan.
_R148_PARENT=agent
_R148_REPORT={}
_R148_PENDING={}


def _r148_same_stock(a,b):
    return all(int(a.get(p,0))==int(b.get(p,0)) for p in set(a)|set(b))


def _r148_overflow(obs,action):
    """Sell only inventory replaced by otherwise destroyed dawn cargo.

    All original orders/field jobs remain in place. The COMPLETE warehouse
    vector after dawn must match the original funded action exactly.
    """
    if int(obs['step'])%24!=23:return action
    orders=action.get('market') or []
    if len(orders)>=10 or not _r97_budget(obs,orders):return action
    _,private=_r127_fields(obs,action)
    stock,_,_=_r97_market_stock(private['shed'],orders)
    original,loss=_r97_delivery(stock,private,True)
    if not loss:return action
    # The deposits are ordered. Recoverable cargo is the discarded suffix in
    # that same order, not an unordered product total or future forecast.
    remaining=max(0,100-sum(stock.values()));tail=[]
    for bag in private['inventories']:
        for item,n in bag.items():
            n=max(0,int(n));take=min(n,remaining);remaining-=take
            if n>take:tail.extend([item]*(n-take))
    released={};best=None
    for item in tail:
        released[item]=released.get(item,0)+1
        if item not in obs['market']['prices'] or released[item]>stock.get(item,0):break
        if len(orders)+len(released)>10:break
        proposed=list(orders)+[['SELL',p,n] for p,n in released.items()]
        after,_,_=_r97_market_stock(private['shed'],proposed)
        final,new_loss=_r97_delivery(after,private,True)
        if _r148_same_stock(original,final):best=(proposed,dict(released),final,new_loss)
    if best is None:return action
    proposed,released,final,new_loss=best
    _R148_REPORT['overflow_turns']+=1
    _R148_REPORT['overflow_units_reclaimed']+=sum(released.values())
    _R148_REPORT['overflow_quote_exposure']+=sum(n*obs['market']['prices'][p] for p,n in released.items())
    _R148_PENDING[int(obs['player'])]=(int(obs['step'])+1,dict(final))
    return dict(action,market=proposed)


def _r148_atomic(obs,action):
    """A shortage must not cancel every otherwise executable same-crop plant."""
    commands=[list(c) for c in [action.get('farmer') or ['PASS'],*(action.get('hands') or [])]]
    demand={}
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':demand[c[1]]=demand.get(c[1],0)+1
    blocked={p for p,n in demand.items() if n>obs['private']['seeds'].get(p,0)}
    if not blocked:return action
    farm,private=_PLANNER_NS['_clone_state'](obs['farms'][obs['player']],obs['private'])
    kept=removed=0
    for actor,c in enumerate(commands):
        if len(c)>1 and c[0]=='PLANT' and c[1] in blocked:
            pos=None if actor>=len(private['inventories']) else farm['farmer'] if actor==0 else farm['hands'][actor-1]
            valid=pos is not None and farm['tiles'][pos[1]][pos[0]] is None and private['seeds'].get(c[1],0)>0
            if not valid:commands[actor]=['PASS'];removed+=1
            else:kept+=1
        if actor<len(private['inventories']):
            _PLANNER_NS['_apply_unit_action'](farm,private,actor,commands[actor],10,int(obs['step'])//24,24,100)
    if not removed:return action
    result=dict(action,farmer=commands[0],hands=commands[1:])
    # The inherited final-hour watering contract still governs any rescue.
    result=_r127_last_hour(obs,result)
    _R148_REPORT['atomic_turns']+=1;_R148_REPORT['atomic_kept_requests']+=kept;_R148_REPORT['atomic_removed_requests']+=removed
    return result


def _r148_seed_prefund(obs,action):
    """Fund next-turn valid own-plan planting from already available cash.

    No dawn/shop prediction, displaced purchases, new land or future opponent
    observation. Future geometry is obtained from exact current unit effects.
    """
    step=int(obs['step']);orders=action.get('market') or []
    if step<24 or step>=695 or step%24 in (22,23) or len(orders)>=10:return action
    future=_r128_future(obs)
    commands=[future.get('farmer') or ['PASS'],*(future.get('hands') or [])]
    if not any(c and c[0]=='PLANT' for c in commands):return action
    if not _r97_budget(obs,orders):return action
    farm,private=_r127_fields(obs,action)
    # Avoid predicting geometry changed by a land purchase in this callback.
    if any(o and o[0]=='BUY_LAND' for o in orders):return action
    access=((4,4),(5,4),(4,5),(5,5));positions=[tuple(farm['farmer']),*map(tuple,farm['hands'])]
    for order in orders:
        if order and order[0]=='HIRE':
            pos=min(access,key=lambda p:(positions.count(p),access.index(p)))
            positions.append(pos);farm['hands'].append(list(pos));private['inventories'].append({})
        elif len(order)>2 and order[0]=='BUY_SEED':
            private['seeds'][order[1]]=private['seeds'].get(order[1],0)+max(0,int(order[2]))
    available=dict(private['seeds']);intended={}
    # Simulate the known next own commands with virtual seeds, solely to count
    # physically valid births. The current atomic repair drops invalid requests.
    for c in commands:
        if len(c)>1 and c[0]=='PLANT':intended[c[1]]=intended.get(c[1],0)+1
    for item,n in intended.items():private['seeds'][item]=available.get(item,0)+n
    before=dict(private['seeds'])
    for actor,c in enumerate(commands[:len(private['inventories'])]):
        _PLANNER_NS['_apply_unit_action'](farm,private,actor,c,10,step//24,24,100)
    short={item:max(0,before[item]-private['seeds'].get(item,0)-available.get(item,0)) for item in intended}
    short={item:n for item,n in short.items() if n>0}
    if not short or len(orders)+len(short)>10:return action
    proposed=list(orders)+[['BUY_SEED',item,n] for item,n in sorted(short.items())]
    if not _r97_budget(obs,proposed):return action
    _R148_REPORT['seed_prefund_turns']+=1;_R148_REPORT['seed_prefund_units']+=sum(short.values())
    return dict(action,market=proposed)


def agent(observation,configuration=None):
    action=_R148_PARENT(observation,configuration)
    try:
        player=int(observation['player']);step=int(observation['step'])
        if step==0:
            _R148_PENDING.pop(player,None);_R148_REPORT.clear()
            _R148_REPORT.update(overflow_turns=0,overflow_units_reclaimed=0,overflow_quote_exposure=0,overflow_contract_checks=0,overflow_contract_errors=0,atomic_turns=0,atomic_kept_requests=0,atomic_removed_requests=0,seed_prefund_turns=0,seed_prefund_units=0,targeted_errors=0)
        pending=_R148_PENDING.pop(player,None)
        if pending:
            if step!=pending[0] or not _r148_same_stock(observation['private']['shed'],pending[1]):_R148_REPORT['overflow_contract_errors']+=1
            else:_R148_REPORT['overflow_contract_checks']+=1
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10),('farmHandCostMult',1)])
        if standard:
            if _R148_SEEDS:action=_r148_seed_prefund(observation,_r148_atomic(observation,action))
            if _R148_OVERFLOW:action=_r148_overflow(observation,action)
    except Exception:_R148_REPORT['targeted_errors']=_R148_REPORT.get('targeted_errors',0)+1
    _R148_REPORT.update(getattr(_R148_PARENT,'telemetry',{}))
    return action
agent.telemetry=_R148_REPORT
agent=globals().pop('agent')


# SPDX-License-Identifier: Apache-2.0
"""Route non-YARN shop worlds through V42 production tapes.

The route actions and ordered shop-pair map are derived from the public
"Kaggriculture V42 - Production That Fits the Market" notebook and its
yhay81 shop-router lineage.  The notebook is Apache-2.0 and is parsed only by
the frozen build tool; this runtime block contains a compressed literal only.

The o182 opening, routes 0..12, day-27 route 2 closure, and all YARN worlds are
preserved.  Fixed o171/o170 livestock schedule substitutions are bypassed only
while their action windows overlap a newly selected V42 route.  Incomplete or
unknown shop observations retain the legacy route.
"""
import base64 as _c171_base64
import json as _c171_json
import zlib as _c171_zlib


_C171_PAYLOAD = 'c-qvx+pZ)@k|g#o^_&lWzwBFeRcv=*t1BCI;lZ*oXbi|979f@&mixBgzcVwBdqlXIsEDY=X<`-_pkq#*jAQ0*7gbSFk^k}C|NXE3{eSx}|MvfU_aFYpcYW7=_aFZL_kJHf{g3bdkAMAd|MlPg+n4|UyI(&4`uktL`<GAO{g;3Jzy9|xzxekrAOGvW{<r`0-~Rj8-~R4TfBffv{C2zj_}!=P-u`m?{`c=bP5<)g@8A99r(bX1eb|S8`G3EB?)ULBu)lo&>;H25?f2)Q{r$VY{q)0s`r~hp!Hi$O<n8^}{{G$V`|?Bi`}5Zyo>NBu;Qhn(8T@wp`R6ZR@gHx${{GX?KmD(_U%&g*fBoI3XY<?dzkdJrr`xZ;{^#SrT_!eNCidIsKdw*wX$Fr;KaJ`BU;pFRKNig3@uSD5_kZ|2nPWinWk7%X`THMkUncR_pML&N-+fvxBfI~}>X+(2^yR}3-ybiwd4%`J{r-pg;e676`}OmWfBf)!@$Q3naQ|=L|MJsczyJDmzy0NQ`?3&*^PMc0NAOmywEIl%<Nx9F&p+RO`28PG>)<+f{NK^E$)|ezfr%e;Sk)Zxh#oVl-`3Ns`Tln@gX+J6Rkn%Yfi-e}n2-N<UxCki<MHR8J{A8l^Cb7{P>=6K``~f392+8h-S?;a<u`x%{klMdjZsd<IETJXVCXt`IY0hHaW-E6W3<@ObH9IjyvFPs7`k4)0kxRf8UjChUQOqT953dfyWX0|A45m@<8j>A4E@p53&HE;F}jAwI*MUeQ-}BIWA)s~ntgm%eTyE$nRx609}rll@=OM2R~-}FuY};<=TCN4Q=zA8y=<%3jJH<2LKit8^|0zg4!n-%jr07uS`nFtxvJd{4$HrN|J!eBnVwtfv2=n>cAn<%Yl5!fO>C+16bx2C(+OKdC17;B7#+B_iYWU2Tpug)X>H!hQ?}goj~~g~>wNuvmw%*ayRc!R-vZ-22GpyF9W2B81K2%}KmNRT>ecuDqTv%f_RerVyg`jMSZVY<KZ2L~w}LHn|0nTdz1~L0SHmdfh7-8Ui2QjyT_)@wgAvOM>*=vn=h0(DfK4~!r2@Y1{e#?1^SK~q@sxl3_4D84h~p37Vb&x3Hk5f?#Zd0w@U)-KHy)o*=ox{36@2ew|DY#&$>h6lf9=?IpFe;3pY`b{&jZ|_et!G&pN|ar#5w95_W9pV|8hL7T`e~71nyrHoO_Q1zM6lKtrR=1eydw=XG>tf&*8@N&}I63A0dc3^s78FrFk1P%5?ur_jyE58Ae6&jxR3{@Q5e%h-=6tS`+2}cb`)DL0>*wfxR3*zCUD{Pva+7FJJKbi(y6~DZe}6@Q*8XF7Pq9Mo>r>AQU$%9()rscpC1PiU0cf_Zo#P-a>(Km9a2<8_#&(x8FYgmPYcx<jVAgy^>MPMP>-k4<Dc%=+los{h7SC=bwK2O#)Lc)kSe1xI)3|6h#4zC})oo9gsDHcU%6bK9cs<JxyOh@)KS`)y@3v20nK4Qeb0ML>W{*#3ldy^P%PEt#y*6gvw-*WQZ>)SWkHhuTWIQ(E9Od##K$^`f|LP^T_G`iU;vXYH$!fBnBOVrvm?}jof}>i0)D#cgMMmVk}rQ0;M99=7D+2_-`qYCU`vt%dHOgHLw&Mhdj0dqh8%LQoi2_XKL<~t-};BxIGb-Mh`^%_w%;9#)BZ`FX1K`T$gwEBR+YbT>+=q@f0Wm(ZWw$Q87ZPW2h2M0kKjYk=EzUtMSpSp7EG@#*ej9gVg6bvCAhs<bGZ#C`=O5GD30i+V4NYkqDj#Kp6@2@;?6Y9OvSmF0hgqhS~*6SpHu9uGom*SJJ8;`JP!x6q*g{12>XKyg#1$gd94U%-o*^-=Po+tRE*!68Nb|p6AfNn7UlnKz)OXC8DlU63#uxuSb9vtetZk41<~NJPlA4c2TzS1gxq|M*MmhFAU?q*L<gbIhTBAm?-EfBhx8}Oh@+fm+4>2Fq>%_-pz4NGwC0~3IaLxr}EiPuVpb&ns_{!#m0r-oJ8PF=7Hf8`=I1zSnU~+Dle*;aFDyerNO4({6}5a=2c*hvICGDfxUl>ZWlQrh1-ps3T~&W02CgX;~<}&SKXGw%jJZemvoJe-fKSKiaU4XI5z|$xcpHTNnjk{@egG*av#1*gZZG<66a}7c^HxFZ3eN&F@s&DXehE{^em43`XLKWgpOfPou65vrwFSZZ)A|(Z0v<It$sZ8F`xJ;Ad}7QIoW)MH=pk9uNT!hKXtf*I}#q_@+$T2;P<-={8N`*({HqTeTQLF@yRi^MO^U9ZWFr1?t{q>z<xkJq>I8^b;#@ifL;IQWI)~5gKHi0aa{eOTqcY6YqNLkMnQhxSBq(QW=A|ui%+oF3Pb)~k!m42gV0t)u<5(5Q;b1EW0m_0O!fSe#Y6e_<73LBPbfk+@ulMTZOZTG*ztz}HwVo1`LWh`OJ-748g$HZ&Ojdbq27r}HT$goaQ|iaRW{OrRt%m0<9Q!*U0-N(Ac<S_J8%|v9HzSAHjLraxvF{oAE+li{#VID#q4{y-RlS9JjOTk23V`dvmJAgq*Rs(GJ5y@NB0$c|6nynMTz$Faa&;%1$=Q#@rq0y!%%%`iunR&T9+Fx<ce>9m%uGEUc=EO6A$RzH}m;KHkYtS4y5yBJ}Ml?@e%ygAY2kSDmaYs$@TP?zs&Z__w`->ttE8sOw#!KH!MM7;%ABMihV-ZV9&svyY(fJ`SH7|&+pHlKmT@n`Yn8<9S2oE_b&6isS3?|Qs0NFH+jeB(w%cr(Ny_|@m>X|SrJPZjU5BOAo^K`L4W$=r=NfP#}A*6Jp~3@Z@l+^^X2Ei|M6(OtK!1JZcONBMWsH!|M5ft%nGuVdZf?ut$QiwMGOSMyp&{E$B}R~rW<e1{@O)7IdH$n9U5kb_K}y+;W3tBU#6|M@XjyOtJTQmMXzsJEVv(OKYV^GF0ya)Joo*2t@j*<EH3+}4zWZ-GiruqE2%o(;IVh~Gpu=F#)VgEl$CMg>KT>o<-K+73`LkxzcOPugQm09-4PXZ<!*P<dtC4Z;Hu##Rb8yozf||?482Ris1pcPIJjRi52}yVKQ!3HL{P(ebb|>V1?dWGe5ZqAA3pIT%CI+78?Zwqf=Pt2{c~b743oRRPy^B>*qvnCGwYVPj%v0`FJM@_c*xIqurU2HP`%7rBrimn>R6ZOnP1dl0f0oCs^18uiz-)`5l=DNQAV>h89xvJKs%^@?oXsmiF4J%R-1oJwZHJH6@h5NHqo)6Zw35CR^NMKI}-5W+GsnbT2N?x8)BChhwu4)Eyuv-mB{(*Agg-LI{-8O^6y9ej#ajwsQUKj!(N1D68?_c&!2xeHG|Ls&r_9(;>a<$*)HUO`<=2Ja7ti(keG-JPGwp*EDIxPeT_QlLm<i`MkfNeh<%~1R2F-lgzMlEZW8rt8bV4TkcfO5&#!IfD?EcQE&u2_)E#MsN&su<ByEVL)<DCxcdp@8#uli~oZu%^Hyvt6#00cq>r&6XzT<)imQZ#Au}Unb62?&Fv!@itVH@o$AM|5YqXI%8tW}cET{Mu~5u^%z-_N;CK5>Tceg0o#sS~iwW<^Fqf2&TQ8M~B>TR+WXm|I4x5*`2RKS`}}ETpX7((PK{kP(erNwp>TNXKq&6Ac8K8@TA_bRu(|JHETlhU;TGi!GG!xKqk@0C3V-+ppSJV?VsQU>7jek6pP%r&tY+#GEq>l!DV1_7$gMHXMN;8TVLp1Az#fD-+cBCP4U#&{VOe;yqUo_`zv=?a4HhA)RyMdAj$nr%a!t3_gwua%W<J5Q-+84c@LUSIf#O|FU&_ENHC?y=FXO84rpMxt5^zTw+BDp8>Y0=4%OO6nZ_p3$Coz(}Ku2?;k}jZj;q(VT-MR7WF=xg(^;bg_QY)P%&DbxTzm_5iI?S`oRhZri|%F{Bsip-3YH-vqZM(ocQ3DdC>t3?>0lV4B*sZ;}Uxu=N(u;WJDn%U+?mSFai<Eaamtv)wDMH)WlZrcP-JVo|6a0WwS3$t)U7+fEq9Hq=PcSbwT-lpV+EMQrC-tD#fdXhoVXht0#Mz7tS&m3#hLG!QoXzrCzU31t&|4V406M&zNSF_;j7X`@MHG4Xq<WGL7@uJDPm;TE9MDv~cS3eRNSpxK^s2gp1;ho65WL9a2o3GX%Bj^Lm>TsD83dNt0CQ52KorspeU!cV)tb`-{sFT;L^yC~cIpXWUxFZB0Uk{)~L~E+MBvlL4fWSxpC&65Wk;skn{1uVc?>m*TF4{kJdZXLS5PC^|>#1HqJpPc?SGkxNJ(*h@r091EF4n*@f{KUsSph)636((|c2iJ4Wu8<#1ju6KJvymA9WP3bpe`d#YAKG4MZ{1m!#wnKv$0(f`mtt|R-i`Bn8ovCo+O_jFZBai^x?t0jST_n2gV*Xe{%UI2Bmf^bTr~`lTu7^Z+D<SY*BEPBIlUkOuN>ghXveLG3nq^~LCQ2kWz(!=05+L0^4RfQGKP9}m`e(6-LlrVk8qyXgJ1x;7p*oW+Q4e)gv4hZ_AHt?%3IxSUI-@|zb%A7P3}vTrPsD%BM5E3dVUXqMcvd*_`%tGop_g%^a(@Y$DhOgN`dYPM;`4bLTIExjJUWfh*)At(!zLy&rlqa<jo*?GDM&LQ+Dy|d&^m`Y%t&5!tt6=IU0)1WZal`mHYcP8)kR#e_h1_-$KKKj#6+R2Y3?8_SA;{#(2P@*vu&%=YcL<P6@92wIZNYS7^~AgMJ7Eyn1bR;3icAr8!E^zgcxeymZxZxSHDs2Gy7njhV_G6siwZhGRG}mHTStpspBH@5pjq;AP)C^U1*yz<m6AY(W>BrsoDi1Uu9O{5Po0MHOcBOm3$mWj!@L6SyB`0h#u42GN^NHRi!JgNd8ymep4>gd!Ng)JBR|zlp*m490Ud+T*z#=XwXB58x}R*XSjB+D0&f#M$i-B*L)3#VYMY5SQ4F}l|=bd9fPhaGp$?0s%Cb-E(dl)`6E_B2-e5B1BxzmS2etD#H8AXv0H(0vunM!=bxXLOwkD;u9(PN!E7n0S%^()hldWrF@eqH)`N9lgaB90juNs>=)Ih~b?fX)fwhtSlUU!=*5thddhC>Mp{F8g7E}e8nWIoyIMX(y4_$bl&tdRF;{fGnZL5J7q7TR9Mw?y{2PuK0VA92030hCvWRDdbR)j$Y#^4cQ!59@3bFHYu1Bvw!GTW1<GB!^VBPINME$x`g;wlfAp0uCX^xJKcKw9G_`dd5t#D)7gWnXx<M6FI!(L;pqZ~S=cL;}ZHn$CxeM8Qz^hJtH=G}dD$Dl1kng>txpPr|f^5^Ca_hf(k2+>x{QISf7u>wLU}OE#o8zuD|M?F}8wfnjWY2M9V1m)(yKn1bx%w`35EEt;L-MdYiAp1Ja_dIPC3e4;H}+B}ebeGFA9^#bf9JS7z{4Nq=9UohmwVvG8elVUow^H29O(x<(;sTl39qx>i|^-apNunet$nUAT+E_#3OF~A6RVAKrr>=7exTECf#84)r%hG0UzyY6<KFNCD(;YM8r{==x>0F2hSRt5VA5iRI>&aD1Sf02p;82eCngS&$tWep-vaNQ6<2ioTQSXfKMb&Npa?VPprLThTf1E83cP_jKij*(9kPnuJ`*<<y{hL6RUX35=iyoV$A2cu%r&WIE9QdDPnDp0CCxEBEkAT(EDrT%@$eJ%>+_B<9#gfV`3ZtQ}@>p8di<yJLNO~9{?sn^NI1<pX4`=y~u54z?UJtvc_$_Q}obKnUJB&;<RMuRAat*uU9ZhkuQ(76z2CAip&Z4K<U#ji?nmR7z73npv^4y)&^#aH590M4)R#W#*=t*#S-bZb&~I{Zh>4Y9g}k0I~AD2Tz4n8Mlv&7{ooOU;Kvr7Ka0DXqM4+uQro88fY4c8_~P0>qQ)HjPj2vyv=f^v*$GL0ACf8|>{g`t8Mhz`$ajCCxNOIEFSiA7JuWrhVP1PU8p;nx&y-gvbjh;-;Uab9)S7QZ;UA%Xp_b%E+w4r7#V)Ds*Mf{n*u@qNunjVdEZw9As8ogdmcxPR&rBK@dDtMBcnvP&j0z9D|;6#4@H159**=HW@6E)jx8nZkQFoBJn%xT$uJ;i3iyj#XZhmyPSzXoeZn@fzO=_F?sqQ8HZ{rH68$3^`kG?>{QK3vu<B5Y`0m-UR6BjnIDbKt;PNP0T9v^jX4H9CaFrQEzRv@n}T33nM+nChC=$9N<Pi=<VrrV799#hg?(DaVIMK5kHH%hM76USgQwP|w*fRRCv@Ea$7D9QhhFJtXVji}TTsSugo_)a882O?S5}?XYNmE?Z<0?vp0ml+c+l-#FUj+_WNP4{xpg%oQQ(o<aHOtdzq<OL>UJU7Q$MO@IJU|CJ+YJ7+caCdJ=w_n+n8*5Uk3217ejkJ{T*|RIiamxBd!F8(B!ihl*2yJG-Q!7%VceHZo(9l)jvR{-OCS0aUeLCZ@mf5H(Mw1R5VUP?+w?F&Hq=$W<ng`<u45zkQ&e#fiJsHRYLt!f+`3)Q9{s~jCKwCsA!wXy!Q4<myrg;5DZok<FkxwJL{M+Mmjgf`M-GO&~sS$3Dgxtm}eIqOVIULHoV#?IO4USEP|=4M!D%azowq-^evljr@jtXyO1PwSjGUCki9g_Lo=xwn5f4rkvrkM`ZVu|DOAJMkNcN52S*Buk@HkM;}dAuI(s^py&{|E!1ZbXL}EEDV6ASw9p=!oYr)C4JK!0i8jN;GL?);M0pD?W5c(k--TR11I&Y16iO(MdkPZy0xzbM@B5r<`0y<esx;-S{lMj}D+%aOor`hI2Zg0W&RF;T+kY5h=!;<D^a)XUT!1bbqwi{|~Ya<a;h4#@~^JP4OugZw8obimZeS&9alS~tHgkc9TO_sO4vHWo}AX=VrS=~Zqd9(=;aFm3RGq3Ews2R<<CCxelFBARp{l9*GI{b>Bu=DsheodOGaN@e!N3!M3>HVr^G-ML9tMBzDn;ck!b?kLfAKQC_jNFa2qTvEEK?U)4q<77pF!c)v4|#M;2{}jh@7417lrmYH_mm+th9*rtQn08bz}Ys%i%7=2H+W80kmvoV@Tge9&&q$w4sU^7?kUS^dX@4j0Nz38Z{~_M#f#a}r-O=h5CG#KI~8{M^uEE5`1!HFN|E@OPekSGx|Wu%N%|x(IOlR?5XkYIvML=`*Eu_KiK9`_(hV+$PhcRH-;&e(<EhgkLgG@%qKAf35I?5m2uhPMp(rM`i(lV-&TJCh2do1GB#W{shBQ<a<10^wrOVNABhT2oC4vwa;V(-dQ^LLVavK*c_hYh4s}?dqjWwX%nx&gt>prX1Jryu_s*>MvcND3@frYkdS5gf+$u^LBPuN-=a4`+%L*5hUr{q0y=j8-2tp$a|20_<M--%LH<NT`1?o;^U`^@4E>WAvb9Q(E;!%@!_IVx<!^anopLiJ=LG5O3_(}cN56RIhUnP*?4wRH<2mElSwR;ewc+uFx-+LQn0lDKM>%s=leiGiU6BUxTqYog0paasB~(F!JNCQ1jJ_Wj$yY85}6w?NSW>@?A^G!9PDOYh5o<fZ+XXtAJKJ3CbBt;(k$Hep4SMLn8JzxjEu7D96Er{W#>6l=xV`qJ+&g59zc>PC%3FDthm-q1B5*GL>YdumZTs|Lh+8TuCiE7(hnPbSD_wY8|=G|r1<7);RW>G?`p8o3iZK+5|O42!^;8~?omSjYG#N;{IdoD{nKu&$j8IcOQE7ppYXh%vS)Cwx0N9stXS0Bh0B0fhFKLY9D%jVjB4x`-;UHB$<ZAyo8=l;o;q*cv23?RG!M0phybG?R)VBg5{>QA%k;6?lVrAj~L-?2Jn9lqYX-rC-x}2$EBXASlQXnI%?`Q@|IqnK}(1;W3%Pw?g9VBDF#qc?DMU|0Cu4L{Y49^hxbFh%`VMz=Y!noi5nj$8Xp^pmT)aO;9(o%-y)SBqvQrxk({}ktKkD;ldhrjrb^Z&P~Ve6Il|XuEe8-6}Z(d;a(E{X|URg6bXUp*y&XH5lV~f`#ab&nG9{7^A9AE95uawT|p5Zb__~mIBBz&T3v*!Z^o%hn20jt87ia-vt%(Te@}lRiZUohDU4H@5nqbx&E6mt&ZBu`Avwb&{OIGBy~C3C9-?OUUYW*5qdgN*5#%T?<qjVGWZO@92F@P%<~BL-N3DcXGj4wVe~*=z%wB<IT2y$;&QnHWbZU9vWP1Y0eWvzMtIr+NTVHEM%YV`p7)fzDX(E%#PJyZkOq?zArZ>%tigfdA^|`wHaYed;@Be4QHFw7wehuk%T~?fsqLO(*bzEB7s{3^}I(XlIbFyoY=R;XXAI^zCl*?pEh(PDKn3op|*t5^3dMIMKPyvB3^s*0$a~yOvUzAb5(bq3S?z)b4sRcK#yT1lhWbM#H`S#;u%5n{GtB+bv;oCkw|8Q7l4GSSeS;Uysr;?0$%yLfk9-KqH^VVvDQT^fm%kZmgeH*l5==>kg`<SarQc-O%-rn+e;4JPns1d4XIsS;|`G0UI=<&Z6^en!yg+mN;XuY*OtIJ`%R*&Z(#IBNd#WJD#1AyV~D;Owm+0ZmTZX<^DrQEa@tgB-fXo{5Or2)qpIKI?kzx`bz<1phj?9jl)13LH3d_IxQ)hi$e(zTcBJU)V-#@|<bp!?oBxt{*=m)U;#zP=m3epx?vS`6c9>`RbL_{f{KgasAYvSsm0rt{<d<of=XpZ@y&*MI)!&!2z0NpARYQ1!Fz58cWh24=@+WcEH(y~#U1m+qX);M#{AfB2J7y{!vGQJ#)pQhY)5vkZg&^v6#>|M-s|J|BAu47A>O@Bik@&wu~p*IO7D4z|N#KhNqoIKKb!L@BN3{-b)N&-1O&ntooyKmb}z`|9dA60S!0a?8Fm;0WF?>dCQM0hMuJ$~Z^!7#kjInd{56H5Ljj)2r3U<pn+ZjKr!V?T62AsC)6;_v>WaaOMs%SHA%7GrE$h;|(5r-{v<=Ei!=SHhAL-M}86wH%fobU~_L7-bYUN1q_}Yo4H{TOlS-j+<yN2%Qr4Aqg;QB&DQ8L7#m!&hV8>Z#+0;-DSO3ky+KJ^=r3A6fO!U=YS97>YGt;B-do<chdWWiy)|v;$lLXiJpmA|(qYQw0oU-y3^rm9vP53hfqOGonst7{g7b?sz*zcIrdzOxkAxps3n#Qd2!JlCvFjV9c0Ah-OO8Slj2^?CUVIS%S&x2`su%xL-o@M|5e7s8l^wk{_{|8QR})$6K&C#Ahz<&PdD`w}>?D~MoH2yjaUVr2y#@y18wsbVZZ&|My}z$2n`41!*7=OuSP4@>0tE$Bm$3jV>*0YS2xheycvQHg`r$+3n+(Z38Rv}s;x|{l-K3yVXhd*j(HZf~(w!q*?aplKWJaic6rN+d;XcTr^F`XYZ`G{?!*kMxRM@;fM?0mcIlS&hc`?zE*?tW!<2ebbEN{}9>hYU&?uNVXG5Xc!rEyXoP3LK&hIqVtvk@L2u%oG*5Jd={Z^8Nn8aw_ey#14s%yC?8=V8-Ul9U3uB9RBW2R~Qk(qpz;PTs`Q)}t*Zq>%RQG94q4w{cRfE%)R3jT3VKh88v8WX5?e^C{<`OiyURyI1|Ynqd%MNYj?LS_DBj2QO)cY8;L88T(Fq3ui^5KLn-#^is`JxsSIfg!$LKGOBz_ITW<t`Hz{5xg&(xuYlkSv3Oga_v|-q@oV0O78{JLo|r44#PT>VK5voo-`Ps3V0>dUuIJG)`#mu>pZO*KscL|mV_M3vFe+}9(rP3b&GU`Do<raN$)$zY9Hy%J-=|dMa<G2J!jTSig(njB5fX7eFlJnO7uo~`h{*0D=yX=Lt-Ci_-z(&zNHi{!E5S&n%B&s}s=@UEbZ(NOvQOj`>m(mo>E5)@x+kmi7~p1S8PUN<s|<06<Wu#+G`fo-fbG0nmz4O7W7c(Tg>nQEqY4xCnm8x0j(K`4E22D?jIL!e4&<u_m#43Rna3)FoO;xLH@Y2p$`;g7uc=j~;lA$!)<~>#mN2EY*3j13F%K1kij*9|G7BT=57^V2>d~}iqF@K4WvSMH<vqr4SP#(+_({0LKl%XN8e~iN54Xb^x3Mvc%!wB{ih06vecY&Q&{yP3DRswfW)f24KaB1Y(~Rw)EJy6_ts(w8OBe+ihtcNXiA=F+yXGRhjq5<{jN`X<#2O#~;50-N%h*q9`1(GVqAjXs$axLNB8HPbD`{73$$eY+Ayd$<h$PY*Y4iq%zhy!fbsxQO$DO;YU}e?2ivvOUmDzkUuv(08qhmVr<$-ieb4%?(h`6u?O{-m1!%5|JY)Y(7oPj%az1s@KU>&qxg<rIE{xRFUI@G~@%x!4USi@Qe)jL>p5D*Jk%SrL0W$Jv|G%t9Ymep^bBj@X9%hW0P2fWQ(1oUppPWGjd0C&t2_QaEp3GGRDm02M@b=9<jpq!R*iT_o6of$M6GX2Y|Ax80K=L_$pYzDl|9lZ>?Dq?kIBThThrKuqF*!umRxEK#^jBqU>m(bx8XN+^jsW*z?Z=}Wl8TT(+5V34}f<i272_z>u?~i`BX_Ns~QA#MLu8p=eI`nO8R1s<;n+5QKO`$UfFq($R?q+x+ZOf5DKY02C3vPKGlIx`+dPeu6T4%93p7-Rpmb)2j{5L}g04ezjtYj*9UMOt)dd}H?!SoY>gspXb8P!pvp2n_mad3Hsn!}R^F#<jAX;kUGuxlSe-52B~rxlps?>#fhWZ<*6BTv&f<=X+7*aQ&~3E6XF8iczqzuA75G&3i5X-aLv@4!4+3DdY{>S(+TGhwDCDHcv)^F9YD2d?rRl-_{=LQas<+hYOuY1|XuGjCMdFl<f9+P`@ek#p}(ox69<DosO^Bu8VNT```s=@Sa6O>9HTKZ}3VP@Z~BYO<?^6kY@OzTD1AS*r=}DC90ly;kViI@+kr4D-#)8LRQHA3&{Vcp^hW?jR{L?z;&oiOB=_DW`Cn@+QUx1wg<8GQUh@CHIN!EoFG~cCS13Fzs3wmG0x6I~nRPK~2KVzSELNvUNNU^cEUMlzyv=@R*Z=EYE<bX<iqX?XO64_9A~W%~PZ9vVxD;w)7b?^}04Qj1yp*4Zl7&AI<0@yA;+`C(Zjy?jl9HX;x)JPgsYc+N1WqVU3W7X|`60tz_vg*Tr+j7;|-}f~#9!{q=Qi>u^w4?tCZRcAiHCV;2xaUH1siz+fSpaZB8XtD>uv@vYuJak748G>$sZx-b-{WqYkB*AuG1(=Kq(7lPjV%HN$f0!i{?R8r%`7O*H?P!l-k-siGTO%9S~ST7V1qHg_Z-Js(Q@S2l=c#R!;q$tq;a*Qp}iGdu34AqAexuhQ9*84&NfpHow&%$d9ZPo@-o~~}ys=;$`<t?nt-P|P6aVNlOQ#rmWOu>S&tnv^?7_dTArxs5)Y|)97k4qzBw4ImCw&$^kxZ^;_qYNwZP>6Hndy}=CkuZ^=!W62larl#ZGyCZCeOM)s?iQ{^=oAXaFmyhqF*neba8tU$$TFxRPE2|I6URiB1oOdyxD{zIDc$94`!gEb{j)6L%0%Sf!2Y5Z^U268T7_rCwo6?qq}gs^b)5KWxiI=&4AU+HDS+cdTn(n*6LL@qH9UcV9Sd>pI$IsdbPBaj1NQ~tU9_Ep?`^d+-J{qbKp1yCk@Rwo7FbRCieQoZ%NyHl5oz~KQ`2<@6psa6=YnGkXqt_!)K6xAAJ<DgOX4g{8%%E@n97VVF-<wxwopr^N_qJ1cO@RupddF1oW`x#w&qjD09J;Gdv{JvA#*kK(AIy!?sFois}_NE3O!~!HMLoS15{ML>zm}HkjscG{|e`qy4J{8h2U|5*O+)kyAN3!(0&Y@P}JC@K}8+nJvC{q3(1dzs5+`#1&Q~kR}cX?n}!p>B#qSV8Vyw^TsMHNJdei&&_*d(#7K&N1H9Qb$4=~=!axMR$HZJh_NZSqd3#O%?u>j2Mkha9+pzaH^3Tmn<QVJZUVETgFOu$>f95^(V`OtPGe%y<U_H2`keJwCFP?KfESVBVbi+J#cuetyOG=%_BVQB9an!y*x^kV}XULH}9zxjqe#}R)i#$bowZ|xY!LSN=c<gqFUGJ|@A6VG#=|>-;D6^EuOzljc`^izYG~H&1QRMlYX`ecgczrmN?%=}#on1l2h9ZFX=?!_|O@a;MLBT3r1do|QGoowzN;#aT(S~aon=l+S!q_N1(Ki>rZ@I~@0DI(JCPozMktIO#d6HdQFs+uivXrbPir$d!W=dK-zn0NQ0q>7v@!uc>#czg+R093;v@OPS^sAqC#EuuvxXuJTIyvPlJO;e^kGsx^K=G0sfR=yF$Kh7fo|C~vj--`nAFUHWqQAF;=4;IMm<z)ME-c8oCN4+J9J}dR`k2=JpEuf!4d4GYGYF^G`zuv51ajtuja=90)t@usVTB1NT|(s<8hO871DMC8)`V)6bejvO05K9Q4q5`}$K+G;jm|;y*E~<IJt%9Q0Y@#R;+lxf8T-w?lV5!e7#j-=KT)&54}PguX}hVPrG$I`B~ZqP{-&70=f&teY(fe0yt#r)>Lp=!q68s4>M`<Nt6^8vJnyZ55ex03xT%cpllDC4pclzLuo+**`w-JNspd`wa~^O7bsxTz`>0XeT5rDdw-SOUymS!BdwI#peWrseE6%84;=TIl2-s#m3~<b7Y_mz^i3nx>3Gk)?Xj@vmp7U>rGV4LokN^Yj3rvCmkLP$-93vgA@QPNTSt92T(86f@$lRW6g4#B`x-#E#4ZylNxCKq)u5$C@#3*sSy-vMNp}oc}cE7{ywhsl_5|MeAvnoN>1UG$NB-fEjekWCK6bUy=hOYC$=jAyIYTc@IDflg&kf7tb7Ei0%)7w9W-`nSYM%+j@OgKGOC91&#+ja0YH7H+!siZp6hWb_T?X;%Yn&+{0{;wxP|H%V^1vCIIs<GDWJ*TDAm)cy@<qksG75cB`;^pqdpH2vBonP}VauiMcS1Ita!hxc;D+ad72EP<Ien$+aP{)9aV68yIRrS9OOzt$L95%1A#g{X91*d7uwImLp5fuN568ABwVC!ycHAgZJZ!x<_NDDACsSHExqFym?ojoP|YJ*O-xDnVx`N}d-U2ocYI|X=SotTzVy?}byXoGO-n8c8X;R6e$H(sBRl|bM`#>DEc%cn8vSKJ<2(S)gJUcu{_fuHg7qBi*d%1U4T0r@4gSmT_NnG^V#CC5c!3HBi&!cNkPZLyO@s*-v$HA&hFdj{wc$LwXRHfYRB4JHtyK(4-0{n@8BZV3U9SlT>yWHBQ@N>|wS#v<^|sOoSW!qwk23OPf}!P>hf(GT5(Zp-rO4ne(9zWj|}KR+GUdk+tU<JTm+hYPE!T_OE@1jVPC%#g`&ul(fA?cfy+2kLDcBOTKkf?Rm-x}<`BCA=<e`C1{Bb<C`d=l3!!Otpzs4D(n>6d~T{%n?BQ+m&hq6X{HEby-cjD)SwawL=AB0e?S7T2#QI27!iv?!>_MHFHAHOO@Bz@b&`snx;!fh*5Cw==;jeYnG}|2;pBTU=yqn@FRwr)#`(YK(p_!($hZXQ;s#wG!~tooGQxi4`J!3Nw~*t+k*#PL1z8%3Z-r7`Xr@oh;wwI775`*Q$RR+Un$%4HrcH1d{TqkEF@4T%Uj%06KM9P8_p?>u4y_f`%p3-rR7;_YLN*YoXO-Gt20w_EgTXVFSxMmTJ67F7h`ZyJlqUV6fEJhAncDt6=BWif0tk>zDSpD$x+t<7^pY^AAy;en#A{WWOdIG%mO~Amfn5r?UI|Q=W<U=x7n&f1Ve;|&V1)JdL^E#FK+0Y=W}X%0^yd;0m0UVF7UJj!KqczjVU%@IrqM6b2XC<nzuM4^*fW2l&u)YSo*##&vabm1bl%?As_NC(KhW9)C#gsS=+cJ{Lf1AvoW`eI`GnunYUL%{ZC#Om6VHMXubjkF8$=cjU;?tAvn()jLU-6{~+fc(cfRooKRO0#W5w@3{bYGJJL}K*ut$Nw$zfA4`2y7oIUuxdZiYmIuE5PbJtI-rFiKREu9p~VFw79ESMxjDcD|1G<Rw)pJixGMfVt3z4ZHwl@Hlg&%`#IK9%Ryv1Y|Vm!WH@fdE=x`k1SE;;H&|d=>3s9J%i2r27|<(94NX=QiTNFp?a1PXW8)b*CC$C|e%}6Cr(?ge!yljBwtGY!>>-e%)^ih#)1n8ODDHXeqtWC!pANjD4asL=)Pqj9x0@+{<0NOCkFg!?DVS*^<ng7<01rcvV_=%Rd9s>;=?0Y&NmZFF*qZ66_W&v}p}tr0Dz|@8_@7OkyOvls*xdNO@qh4L9xr6B`%5PXoQ1isjL8)N=b}Ru!#Y(Q+<1DJ{mS?rP2PB-QF0EJr+b3I9*#8crocVN}EJdk^=z9LSq~J%zMYy@OQPsoFi+fl|FP@BOG=1sb>Wh~Eshf*zR0Ei%oCHYGoBQ2(9Eoxfi}b_?-iE{i1N6L`?+;9>tBY(f*nKab&QeXV08|0$um9!B4|OS8goJ~7(&GO5cHaQvw(MCddhyfar$m$4Zx?{upu9#H!{C4q7-cyXQUwo8VWM70uR;YGkqjX7_W78AKR*240fc5yzGqIr&npYexsnJfuCeq9wCqZiv(i)nb?QRo)FFe^|7Q*bT$$qyPhFWr#ec$inI<*uW>6hYMF?ymtIG97v--+p{dS*`)D?^*ZBzq4hIKMY_wFjwVB?oX=9c#m1mDH82D)O)$VE}zyP?!OGbN*iiHaqg~@FZJ=fkGZM{AHkaO_Ljc`XK}}|u=rJ7_^wlL^Zfs|^+$gEuSJ2GZ)_Z56G3O^F}hX96=V(XbC8ANH%EmUoLUbVoO1;u->91zx8dV9f}t*=duvf6K8As&h?5`XHwwBEP;&VGcL{nlQ-1}DwTTCG?wk31BAeTUOb(=LQ^0wA1V4?xulPXsy>)Uu{pByS{qlW%H+}uGe(rSp`_tH$AlFD6-z&fn=8boL%a=sx$NS0k{VzZL_4}{?{Li01|8|2c7;sSah3sTKbBX?WEGnps_&(HxY8q_>@8`jFaytI-C!zUVi<{W`D+9kE`dNlSfBNI6pMU(v51)@c1qNDgy!U_e<>$Zu@et~&;=(~c@$nqytd4`@`yWr#=+c8DeV%VsKJ5zu$9f=uHAfpk>NpavMvOlfxCrR{=oj_mn4>lAIhK9U105b~&gsjvH5T(M)2r3U<*OHRokUstxF2ahe10n~vgdy9ew}Rlr`#cy5ak2=%;pXYg8Hxwd2trwRt2fjBYOy%sH=@RECx}F{iW20+<U6ShGWQrqlM9d+s~hWIlD4K#DIrlV?&j5Pz}sFL|#A4F|iohz7Y$j1)m!=^N@7D<<y3Bm(!uFHFk@wuK-P5qpni0w<<KFT90Ev90#!gcxXf<vm{gj3<L~fvu#)n>MoK;2iRqXvap};ZWk9TJq;oYK=E(t4}k*ASY*xh@BkWz3x)m>4n{FF92%87=;ahyKKAe!ht3yf;O0!X5>5!+kn(z;{W;pzu9NcWFbzs6O%E3l$8&&tvuhe3u%mmH&{{6aDCh7;^?aFd02kudrGY_LO)6pbAWgM0)v@p=lMPUod;%rz6Nu^Cwnw6y?_-rVU-xbI#!FVWn9gl6X@YT{E2yZVyG(|f$_@BT;O<~$g9k($A1L$wQHAD&!#Dp&a^bH42Y;W<LOY|sM#RR|6UNQ!2VXr)@9Lb_n~N#lnZ*6N-kPNUP2qc3$9ye@c_BWtaIdjFmlSb@Zlldy2zP?ufb83pk0({;B2Y^aHPni+XS}+qo6VQK!Yze$ks-V#sP6JP;6gr6MG|?&3yyn9-x6phKZZ&fz+dlmC3q0iOJu;ne;6VEDP`4u3XM)%NW<?Bt*F4)aFR!n6Grh;mdd_?YLq3wT{yNm7HEZ9*H9vXJrEk%SGBRKkG?^YAGBahUGG+Hnc@t>FN9}-RNBh;mXu_xV{StOeI2tqt9P*Ib1Uu)mXliO(wsWQ0L6>Z_2|2|NRib`;@L{U`HWnS!S6|>nOPZ8)rnmd{WyFtZ!%G4_w2Y`MU#<o_46M&&fBRslD#)V@_IJiDT~mB(6p;Rl@OaEx6`>T``yMbQx>mQ+d1vica;6lWjyq4x(I<OJRGM`f-sGFoG5M@ww5D>S%ecplD224Vz;RPtk9YKm9lKB>C#UmTd<z)WmM-?JIY3pj4cOoQnAHNi|?o(`lw<*Aqq5v{8Pj2(ssoh{4%$LAMEYH@-)u&1Eb=Zk-n5cE%SZ0*7+RunrSxY`m+haDR`vV%BaO0icX9+KwEoY;Rxg&t|Psko3Svd9nLiEc2gYF3lBQ7s)`#%K8<<2kG6JRM$t1&Al)lG&71?#?5ja|L4`xvMIb(n_5wzm02dwg##q`qHHOBs;7F-9pw&zTMXd(@TdPH};1#T5+xK!8@qDMkIk%pQM^|F$#;7}>YYL6*w5i$V)lK)@#&o&dVB`JqJhlXGR!2&P>kv}*kSW{L;D=KRFHW<cjl>}iYgj||A+#9GI;A1L_&%|s#!>^x^@{@Ki-gN@MjP`OVz1OX-41kH-#RcaW`i7Z`1Z}Hld#sJq=UF;zI<L<%jl+gtV}?NS3*NI=^1?=_M|o`GPJgBkWw;(Z+QuwV-l+3oYFWnovZP|a;eUZw$MGQy-kIUEu+&$o<mJHe|=af@uDKCUUC^jsMpA{2dZGIU5KS_-9>4CTDI3XQc%8x`fr0Xp}flNJzn;cKOQm{YY57l$elJ}iK11(M9b9~7Z<Lw$=2@r7$*C=#lxmPr&hbi=Z$DDCTJ#vdc{33r*+W&dC+DqO32_rkD7j>Hw7N&XzP!lRC&m85kMdff8^UDZ0EC{niL5gb6^}LgX=lGTi4ls$XH&Ja|~n{Y@949cf4a(i+yy2x1m{WMJ$HkpMj^pW|}&px`u0%UGsK500b^-+sGZP<7gtZ#9#N!P|Kuam<jeDAkO=mfvR;zI;*^ox9~NkDzPx3U2-nEW9V#^XX3b46pJ)1u6cL0xWN2@a(-uEyD5bQ4!D9tTzkMb^~@!l)TeECd2!JO)maAfVugV_Ev=p-*Ww;7Z^|K}7}{7)Y2x}Pj*0l|3K4=_<yK0qqXusVS?HLF>|R0=6GY6Ps}jcSFAv>~BLwZU1)$03-eS!%ArB2puxDS)>6P2{c3YV)B53c<Dt<r}STcn|H_<Dh+~+z`RDJeTbVKEU>0?>&vm~84R#lPEmQf<eGPk&<e|1?`Qg1z0Fyjwt*nI@Xs1n7&4h6SUq~Qs)@-X?Bdf7edh@oP!YEXE8dSjQci{R9d2n;ogD^z$eXZ5v}Yh+9W$CNffa2Wm#aJOy1GItzE$M%>Qb4Z`^i#V>rld|O;mDwG3n`$Z%fPYSWxWV&RQWbSf$H*HPQh(FEEnsAGGu=j}mS921C=x&5GJpga;yf-HTq_c3eq!2Aae_hM8sm|x@LQT;aS1qQ``LK-*N1RE;4N*BW72l<Lnf?Rd3x;Un59xY*+*eNxe&U0YljMF*>;=SfqrisPx-_P2y1h5p);<I7ha^YThGI+0v$vKwtLKFu-SVg7ZzAdVC#-^wy-rP)lO8tve8BdAXM|96yQN4+CIs{bI#Al6eb^LWt<XfDNA@V5&k<D&FUazgjEfBYd%gYS*;^<rp%+}ZSM25_-_CrEjOdNHBqFD1pKa}Kb`KUggII)w&RTJY|)C2Ir(yq0Vgcc>a+tuq~ri&V*S}`;=Ww=oG=D6QLPCKcEg-UnAxsG%R2kMkWlBjb4ycpAD3;-Q^z#8zYM<6$b+DmUjM4+Rl8?%s>rLalygS>o{!rLFDYvc!CaEq`D4Jmc}zB8s>U0)S7!=fmV^mGPs?f#5${&FtosUGWWQE*cHn+?arvSviq;9@u`kt&HcIpAG+>=C_g?}96YBPH9d+6}zPJeH&23{>F9V`K85%S&%t>gI$0^agx8f8mE{%eQ%49u9+&u@q$eu@7KWYqD73bKa%+_JjVt9k!$A&_)dMlm3mFQ}=#O^KeUg}0UFM}(0#A?jq4f+{-(w+^7E6<C%?V954n4hKrg$9IYnQR&XWACarMEQC#AscKOnX^8gR&B~lY8#q1?Yp#6F~|GzSv1QuT-LSbb9Jq~<r-0SlWGf$BNFq)i6iO_alTmMfX<2Njhp8F>TG_W0tS(2Sqbxsii<?|z$V&#n@?1$$_W4{>+%+q@M;|ws7B6fmoUJoZ&Pj8P7gDH#kh)e$MAdmY|dyrXxg2_t_DVpWXBYgdTM7%tJ92s>=-wyS8)t?%s6MA$I<z}c;}jH#VSod64csQ=6vE)Ua#NyiQE$?d!bGe)P?3$-M*Lo*7-HXQl~ZCe{CUlgN!ea39PQSkw|aHh?jrYvkh1)%pZfSww1axVy^PQWU5jcDDx`2&^S{}@KnYeHGBZNSNK<0a*?3-th=o`7xhEF#Y7UJJiz2;4b~5qc9^%$o)UhwvSk8<js}8O)*b5WVe9SCoqE4t$L)6(Gu2Bl+945SKh-Pn+7UftTI-FuSmAZjm}e^<2d$OCyio6EoaStPlFbXD;QuSjOZ5lcb85M3Z|7v@1Z))oHn`Ur<rw4xU29+?EOy#PMc&+={q|Cl0X4+2_9orKbAt)mTTwT$lu-0}X<MS}9Gvs88&p5+fIFe`g>7#vJKl^M2uB2@vKd+^A>C&0n%Z$iY@AUK)a?~|L)`s1&sp_w;~&2!i6Fe0RIPrgL2aUIeOIK|)hvgU-SdTAy1A`If*0<k*So9}8@<H=hWC_*Tig&=8BmCPowwuOM)rCcqNTcz>RfoNB#PGVbLMcMJ$1?{2CTLWHRejg`;?n3uVd|Y5J4>E?k7)+*i^*(ZiwklirKzqjt+X=^6D1ecfe92rO;l(5oZR$n>O|>eGaJ@3Bg|}q!KI<@FVRqDB8K_eSeiH^)a7bd*|7ooLk{o0ZT_MgS=kJ3I^+klm@WLu3EZ2$*vmWG+hWsLg>)!_N&g`O1!|Bc$-u~cRnfAjKyWg0fma=+YwHcThU;bE}d%Cs;gF%CLU!Dj=Ew-0CVYbom|1O`Y<dJ3L^YX3E<2Szhr^;(k(f@FaX0;k@_Q`1d?Zf%W>&ex4{atG0&-`cN2SCUbGi>8H0dsDLiLEY0|;gpwtuJVLp5XSKs}J*c0%sq-Y2G5PE)5pq;y(lHJsIZ59}^yX+Q6Sbh^nk`Tn^*|%j=j^&8R(ybb^okNkm)hEjSWOI4$qH(J)t1ZvQ)GpGCOFw2_Tn$^-R(c?kaIWl+$bpY3P5ygIg2xql@x1N0Y8c3b3`fhN;J);8LjFM%fRxrUz?YuxLH~WNv>71^AmI*N(rwZ#6~!`#_3zayyYzwZz$nj}Z9ONO=#--%20L)TY{4v>ZiGbNoaUxkCUjJ-FDT6{{r+N+KsFmQ@c>kzZa@x3v2lj3p=N*#2eJoX&02Q5B;u=UKPT0{i1R^pQ+yVJ>00ee{=ON3e$X+`!36f62ImUNq3g&4?bxqZ$&t*{2DO04|2Y7@I!ilm@ade%L@9F_Xl@EUNj{<hav5e5PE;;^mSoq&Sbnwn8WGa^C;+Y(z}%?xM0kLIBZ}T(@{nZS&E-2C`$j?kng)-6gbM>KNpXp=t65^TBnlY^-+_uVccdOn8w0@BQFtIFAsu%aN52&Uhb<{bPEIQ$M(M|B4YhQj)XWeMaLE(57ON-d&e}c(J-@`h2wPu2HTG{%J9@Qz4lAr<W{bagnE3*$58Gx%>1}b}@T;vPl(1$5ONO>HdrYfk+%gd??V<F~84(l*9WnHo?<!OEP)bm@!Lho%upEd9BvbFxnmQjxqJ9mLAYPn6iP`$7`lm`@<(OM9ii#?$^*pzfW}&B*zZCLd%r}uf)`UbN1r-WJC9_uw2{09a@xYpzKf!w?4oQJr%Q8*2WyqU#N)ZwEAhXtG3H89|MBAjFM5_O88gINOCzPqS6oOx<S%@63P9Gur_uxFUc#+GrzSi89|HL<Sbm&)&Q=sX)inpWY-DB!X8WXf0Q6-qr?K^l?u5z;r&-Ar}>KYiP@?0BaFAL|jExNy(0o+l+2_zP*T&0Ur8>R3?ZnRIT>1O@^{h<^+y{z4gd?=U6l8~d<KFVYCVrzA(;dw`qOm_&us)8@hk9p8Nerd)2#wEWhW_KO!{0gq+7Wngi$aLtTeEab+Ww{2p@@y@;aY(Jb|6x!=0duWWe_qFoCsl!)$1LYmBfvS-JK3rxwbUQ(zYM=h+wwq-^{$gI_3^xqxvJ!qS$h)G!#6`sy?QC*2qoicpu5Ih&GWx<;s(e6S}=n6#>QC-kra0xqf0AUqik!HETA_>2OXSR53Q_o1tU|Qgti(uZn<68bWZV_P#(iTQ^e6dK2g9-YgqY0zW?@jQzoRnTUHSd=-fB+`9wBX8-W~1*T$yv_y~R)e_!!|?tAOxdiu*>X8Yy)`fmREWqpxunY?b+m}Nw~Rr1j<>&Gc;piq$*9vu<QzZ?VE6&@KyS*sD!SNrEWqRWB&{VzZL_4{ux`tw_{m@gyVWV#8MULMGk>oo5-sV;Kltxv~r#<w|?->KJA(Gyz_#U-Xhf|Kqu*=@;Vru_b91v$=x*(C|XZ1kg0D%fwwpI^kyN;Ow2Mg1pbVYB_4u>giT7J5#!E}QbVzuazrd(xxC;nT4ShJqVr0Sqooz?v}XPMdn&mQ(7@DQ&Kgj~GAKS*Znugu?@Te<Eld3R0Oud6`OlU1kq|soEaH(7S}mIuKSBrP^ayB}&Jb26s%Lh3kDy8DzU+6@S1x9Y)*lrV8JZBJ<W8)-mdHfIbYiPZrYbs@<EYCD!}5Q{Kigs@X2rf?**n1AQ_Vre8XaG@oDBD6Vh*?tE0TSd9J#OL<-S%6PlPqa8=LXu;!xU<Xn61<OXcv?t-4e@v+bh+rm$8US8+{QZVTealY={W?pcFA6KexV8}(K;aT%a3$U<&%Z-$bSO0aukqb}8R4J)`03{#|MBJffBz%w(5YM<8`XJgl8lDY`}1KhqOS#i$L;6OzmP8OeoS*j5m{m=q^wy%0^IMEW*6kN&WEoX{mWMQu}*^j{Q2{5HzPQ`9&$iAeJG@_LDb2UvRc`n)bf*H2scrXXF4zd8w&AT5C+lh-sW1sRf<ux!ROaD^A(=K7x2N8nlJDQCX+>USBh_Gx%SRAyvo=j2ElyS2*K10I&_AuOFegJ%+6sVyWJ1$I@2hS3zq@4grQK1bdVmVCry19nuMAfBzpF9Zqth%cIJPLSxI1-CCnIDnTC26#p5;sz(Gj~>f?X?FxUHQ4Sp>2J>Jrt`{0lfJ^a+)(|n|3H@9iB0-0)DymB;?cpE$4T^FVOv0H3`*2kSvc5@-II%oS;`)cfmR~PJpz281?<rZD=H8>J;r<56Y2uF_Tm<>nZN5(x4ov$&<&7*HI!bhtXj$zEX=Y~ZKl|ac&E@G?B4d3?W9Pd%i9Y+PZGfheE3aA-ZgC?U@0!Cis4<e7TU~Ve(nlbrhJSf_zTY}nii52dk46sGM%a%YOYI(B)KUokN=l!GjvzqK~{-e~wyL1<g3)QCk3Mm^dpcCd;e&9v0^lhPlT|S}AUrP~$vZmH7A!|A(KDayuDD+BwO=F`EfK!8_57VE!sOygfL`Jmo^7SspQ7O-lItnTXDRrS*Hu^Ponr6&8Az7N<jsw5t3vV%YX$l!|Aqq&`<=U>0kh=UnvBJ%&ew~G#O3g2jSTT(%eS2nV%|#pB#{%lBKyY{!QPaBXQ^Cp7n=J;PFen^XiBH!Fyx;sy(@@o=3!{0*=LGrfJwIQxaO(2C$NXt*i`e-2u#I+OpZlriJTf`1h}Sf3a{|>*w%cfu3jJYJQ!)*(3=Ll$oNhUS3%rC-^92CU<Uxrw%Txq)3bKrjO9ayn0JTiU*#V_QcVk^DZe!8@QC~q`|E0KVrQt*J&guApP;@}l2Li`?Gv4ylWWYbL7a-Jr%w=mMfr)-yswY-sH=(6&gAXnM3#P7jdmFrR14B*eH)Q%Y>IOB?j0kk7rf%^2?pQqny_F@yh%F0*@;xqe<4u*y_#=?GMjXMgZ%V<#aH4kgb{l3l%WxfSKGxTbEFaizB?P`p<TrJDvV&q)X=)8aR%&5R)2EQ%0%ybq*ocf$Qpi4idmMu-%X!K;zFkXRAmtdTgtW!UPD`{%gx4fX)I%Lr>>xC`hOl{-0zqLLJN&(8lw21`hQ?5K8uvu}_eNe{oj1NILtaV~t6y88+QJoSxB+m2rV3S!4EkENVB+(68d^;UnCTpi(b+B+Hq~q*4Q60Ma5A3|DM&LQ+Dt|7UX9i{)M3{rleL)?wHJm!uIGban-fyclZ;)k_h1{D2;9;M#6+R2Y3?8_SA;__XR;~Ewjf%ZWWE}+&Al((sBtfh)#;w1R~i_nd9YQs1iTfq%?QL$yZpVi=<T0@>Fk4b8rBbPrJDL0`$Duh8{X$KHOg>RxV|LzfH>SY$F>Zni{rs)RdB)7j5d~AWj1ZziuWa3fvxsv$;aUxMM{QvQc2Ae>P{Wg+%l+hCCg$|T#=}|%>AZZsP{gXWp@w-m?=Zz4>$-iCbcA#0BF!VL>vk@z0Yv%UQwn3m~yP(lBoF_5QD5<T3uraT1k{Y)iLNg+LD9lnj3O;Ij|ebAF&cbus+Tmuue_Z5_KacRTqtot5QZ1k?t7Kx0{Mi2yw+kK3ir>LCr#Rr?*8K7gN#iK)Cf_-4`Lim9s-{4)EGEsb$(a`%+Mz1pfrq_p~)Rd4e9hsxx0xrwn9iNR&pImjI(sSvb=+qz~Od4?hZCXdIwy&uu@3LiFL7+-TD);vnU^u}G^NHP<P4%wVjOJyvj75e6Bw^>K)>V2lcii4EiHqlP{%VAJp@WAh|YD5oyx!e3nF0l?zO346a}E(+2bH__kP(I>9(%qjcAw=HUQnu;DGe1GG|TPG4Y#?o{?WqoxFb#ExR21sK)cA~Ok1yd-8+m$U0ho>?*4M}wJN6y~oF!(5}^YIQT$Nqw<KfzD;h7RWIWXT;M=rrX~=N>To*w~UmFt%uRo?+daO8`73pn3yAdN0=p*SGa7FTh5a6GkZVlvKbpJh}ON!H^e=E$UNFis{hKKi$hnpZ4meVzj%C@}tnyH!07;GPD9_KBgkO=>5Hy_0Iqd^Xw5LZ(6^Zi#azlI)-3EejDiAb-oais)rkOl{adDu872QXI!g-eT0Y>^gL&FzXT$f1K4Mxg}S*L+#UQVYY=&Y>xKaOjW*xM!dfD(V+0Cs=d7jIT2tE{0L7$)l5Kl&jC`Va(wyqeMz*CNiZ9KQyT?@^xr>2OF==PSiFqliGdvY2RUY|*)gXWn4ThEa_aXPWD3lvuSu7F8_~p5=3lgvA+~${C)j%}?zdEK~CmR<y18MG;hAKVinq%~wOtLB?z`4(XCoGV#)>Ie`q8zq1uztDu>BvLpLY$T0VlTEeu-g{DD#ck^`5G*kuo*b4p0gHTiF*M!zs48eIHt9_ivH4dC}S@ccC?WfbYEk;FA8FCB&M+TKr<<`{8IDbQ0Yn(VoFOY-1heVbjD2Um)+x@kO1*yx=jO*`>Z5O7`<~4SP&Kf`38GCjedJEA8>tF(WF_+%Fl(|Yvurx$1?5fPIVebaL_DGaHYc{m#O9T33+=AVNz8Z;>No%_E*IJQ5xw+OJN#pRp`fFk3AQauPUdvOagL{S#1%5NV+-_#(|2Ic&LcHd9$E!$Vxc|J>`gHOdTH7LA7i$SR|`|<Wk)*D}Y7fch<Qu?YR;UfR;#)v)3+X;!h{T>V4p|?Rw(re>l{-s-E^n5;+M2&b_bZq*=Ew7q)Y5saVBxp83((+*;hv9{?d;(U@bvW0I<*+S1%kwkZhqlDTAM#wVn&spQi<Pp;$>Ytf-FRM@9w9QF}|`WU=HK~y`NF?ecSdK*CFazfV)a7<=%d+3#Zc1G=qw*_SkN4U5#nsFfqCwgVoS*>Pj_x2|F)Z;muOpOQK-u03^e@mtY9-3QMGZF<JsSQW!I`*rp|EX>ll0EgKT83kr+}{&BnY~T3wcC@8yuXdfmiJ`<uX-`G*VErI$Cwk^+BM=za0pF4dqFwu6HP-FDYH!0Hs>ZxL0SC+WZJ#_a1;lEbNSYr;C!=n5>G|rB=p{J{n-3}Rct220bc&numPz7oe}u5`&1>=KP9Mwpc5qot;uNDu#bwinapc%pL7{%Fbu(96)`@`xVE#78Dpe#W1RnsR}MXgg`YrOL4<jB(Xj+-?MB0^oq{7?3(6vxx@wf0uJgwk0Oxv`>6$qPXBU!$4$Bze60(<ud1xk80~7U_C2}X6SD)q`F@<WF`f>mA=HN&{k+~`38J|GI*4fj+>=oHO2d-BGAQH=I0c&;Z?J$RyT?<aW-2u-C)nK$kA~Hc82>6b}gU}Dz=-x+6(s^slOMLzyfOKF`&6R%Q5OMRf6wt|9((NJno_w(M<BkyvKFu~Ka(fHDr?N!sgZy%^AC@#XlN)R#0<IiLod(s;P-|NoiI^(1kKURu;}LvSMttRrXO!&|JUg3YnwTRDJAi4jyzPzUkDCF}@{G&s7Ani5O^AS_B#fMSW&cIZXwEHZ))9D_=$G&R_4Cu=SM-FP$H(z&(oBUD*VR6fEpJZmS2d#{lbBt7uQ%D`z#6P$uZ#NF-Wz1(Zmbmz7mx`mh_@rXYxabxUqE=sqgzVIIkJDRmdB@*$=bZ9452YJY3h-JMI`~wwkcjjGUmO(bGm{&??;74#R`5_{!?~%3+!@FSyt1llve@p4my7`SF9;s%$7bKRIGyl7zf#@u*;|S4SvMWkNs7O#K(LhDqq*Nv~*3<CxO8^mm`Bfj^~tB>9D%a*^x^eje?eLa5;Pe1F`&;oaP@-ofZ)imr52rG?aq)F(pS(nuG~OF{xer`sQ<HljuHR9UvfClua?Dp{f{Pc`__rj*c67#@;Ovgt!QQSpu07?yZ;GxL~;-lU-W1kO69}0qxc--P~IDS*`A=fVoqZ{EoY$NEHq&v`xE`YS2lxfz*4#*6M(ZX*eJ9o<Kh(?~yw%CxB@!C?qxrx@P)Ll&Tu%S5<bO!WZ9X7H?2LR6pj}w<Q^ldalS(VH>7D@WB_VCmV^$XTF*y%te||O<~MD`x>pSTL`HPR~oTOZ5iFxKAzK_{5O}xRjXwFd1pxs3?&%J^2%BhUCxTj($9%jFi|s6I@q-D-v(Bz_~E<-iVk3>iH4<daEe}fUj`&E?Z-rm1<l&op;B*EJ_WG}E21pw(Omk?&wI5Hl50N|@4%;6E6&!Jet!|{mYq;HY9xADx%Kddt^v75;@H_!i`rQ=AlA#!zX({tUSfPQK{l(cMFppEUM$04f>uw@SJKkRo!|jd-j85d1lHX6?-js0#y3&gk<8_!(CvqH?Oez~%Rs$YrJ+WQu}wMQ+rjYwSUv<;i*61ew7(Rx1e9!4Sq9WaRDrFTQh*GhqF1COS1rTVAPH)>`#BB}*WIR>R1_H*c2|y4N*k)c8_WY?Mmc0>RC=d8d5bIkn$|;*oI(UaL59dIv4WfezL?F_X#fe2$qc>~5@#2w71GEnu$uoLDc2{8VvVCuYR5sO0m=X-97pJM!R|hO!}bB4BLr`Px{+n>#>FK$X*$YH3L%Uv0R#*e*05{DN1=0WI(DDPk`Q$z9xbfEt#%3blJHN1)mEfP2u#OLr^=5|T4dkf!IsHnX!D$ZAc^Ft=>_Zxitw;wP#VKYo4wTPB4m9tPF=!8lo`)ZAyt?qi%I!=`V&!<K`}~UoXU*&QdDpD2B~l!%_9rR87ARJAGhosmb~{6HM951G&UOTnTU!YM{y~4@aQMoe#$d&_P{r{$$>v=C6t<R^Yj0Eti)vY3M|v2!drHpG7_Ux%L6Cd6F}}WwTD`L?wH>CS}R)qldix>iqlCGnN)TPR83&wY?(K`X<k&Mn`f)f)!mOP(hYq7KNGIGJKpeXNVn^<;)E2H%nPdH($ZGlue;H~`~I7gU4uLy$~yXRPW+)<CQCvDI>*JlyjZ}VeKyrY5zB=N2!x@ReMp?+psV?!jQWkfei?Gtb+k(@xN+V6HJ~DEhaSqeA0JbeYk*sQ)N%^n_VM|L!!m1F2qDTM#-u)#WXxlhbE@~?9O|97Ruhcs5BFb&UuEmtpcO;s|9IZVTvd{aYJ>6imcIjMaj!v*P(91>M>Nm>gF``&|FxiJ@r^AUVwgkgt>sx=4(qjgJO?3mm9#6C3Dq9}40m6_KzYlCrtxtbF{Cf$rnO*Q9m7CVq%1EDIM%@Nr55|`?-Ch@8Lwf71}+}Zxo_t4iEOT30XdMay;SG%5&Sg%zTyMj_twev^q0TP_RIJ6-SYLz`bqdidRO7g1{i&j*O^@gj6QEf-c@Sc&x7m3@x$l0Xvrhh8-w{Is)W~$;C`0T#Gn57>E|E+@#Qc7{zp~zs|R*p!u3Bx5!R4&%Y0T~>F3GaYSqRn?Q$#49*Z6cTM1y^-p@+L1fVob5%|o~pROVmi#;19_l3$>JsyU{Q;`IwJM*vte|l0CFc3e*Qj02U@B9%IjAJCbD+pQ+ay4>xPpI(eab9Au?|=E}uiyWC94_}~w>K!zel%s}`3V*+ll2)%)kG^j?I%NoSNbvT{Ltv&T&k!1+h1<CzsX*r<24Lj=Zh26dk{R6D7t;&av0CCszqL>h!_DCULGWT^N-k}V7*%Kn+u|`2Cupsu?BO?#nO9=r3fa8?Tr{eZy&5BuquGEo)TC!G^HB~7OX07gw<0>GYNmG3eJY1cRAnn)>5_9`~IXdH(*S5BPgJpy{{>Q9bBy94|u18>iH};c^rfJQZeKW>kRHWeI16$-Csy$?vjp8Q6f>);mA#XAJuG=7QnDLDUX+F!NT+j6o7$aORU*+uVY<y=cC$ue^Y&BX1uTB?Glf69Npp_*X{^*5OrUWXl6ZZwfV=Cu7_v<h=I6B`DGXzL^rf!NiaYLF<nyXVO-m&JD_3@5$duUA<w^q3_Q#$F_GFu(hm#8R}-p65v`gpri)Bx1J|&K9z6UVx1T@%az^=~Q)>$u|Dtt26iGHK*Ma+;GEoBtxhq%kWvl#H=Zk;-{Q0+=5uCF8{h0Y;C+ZZIukqj4A-Z%j6i@d&3D?2pr6(u|z9&U|hGg!nwwYr~`U@=O$?X?N7SpaH8cM~tv|M}V8eU~=f!G8Iib*XL33@RxXMfnb)N`-zxZr_hh%vFQS}5Y55u*qFJ3}G%%C3B%e?z=oEgy)qgMg3_yU1`4TS60#?|uGXV=^9CW(hM2R>TB(`diXskU>96@lzlF>xZG6SD16`Cf5)q*l^&G5ppBcEzx|WV>h?SDg$A4T-tRc(|E5;LW6MZ7F%Qaai^61u}DEO>o4#=oPKz9!7gB`AG>l(2m1;fiJ67Ux;2C&$8^kwBk&{R9)|?l&fQUOF~a8vXjA)~bI%oC;80QtYTa@jYISbNmhFlaaF89wQ9<rZ<du5`YChtishZELWo_%EJtB{>U?wZ{nzgXVcu?p*v;?*15-Z$68DNVj36|C;YWcJRKUokN=l!Gj;WE5!aqyB0?;;>H7S4X4yPjVN6>sT@f&76N!P2*d0(SX?^5P3_2EorGymD=H{T!v4AI1B*+i7e~6N_I<txH7p7?;V_<;>T+JmJxxy>2YL(P|2SY;kRD#?DxO!d3!$JMud9SdduQr5Uv`fF;845>Mke6I>U>{`ZL$9%S|FtW?TM=7z+IX;kTZH<J)8>PtCyQvvl=AUJos$1&#fQ^CoSuV(JqH6C-3_;j7X`}znp4K?{H*J$2xEJ7xOK%P<XsiTXEm{TVGspIou8|{|XoXXKBfmkYI_HmmNsD82;O_NmU52KpW%a(0MxNv`QIf4tkgb=k7fM@cc#1@Szg6hx6$FXN&Vj57-E#~ZiQlh)DE)}=2XpX9{Ag}FM+_lneC3)v`{6HxBgX#l;<Gpy;GW{W!kUX$!^TP88FZ>v65}0UIe`BpBHFgsk37d+d6E9OtUGH}Oc;yC$n$mB`bTt9F+qzZv`6+bgY=;JsG0bVN-pZmcx0o<5-{V3z-c&gnJOYVp#1Raeu!}@brK98U^6X|AuA|MzWDSr$Cflvjl>WZN_GDkrtkTpPhOFcpot9`JZV1kZ4X_azr34sKOoJ@TDU30cBQrFaWBH>hWSlglElze?qD7+OCRw5$>ZoD|;Rri~t>qL53Pm2^?>(dBx<E2ChO*PRC*r?1svuM5jc>{xn$pDT*H-8iag8Q!N1dRlf*{tSulfB9(=@c2n=mIx8l$sau1wO&L>e6W=#Af!5asPdj=|3Yt#hcuuB;SmGbw5>41rwF2fsEaq@JB1yI}9ZHu5{Ur4xvWLRr(?L0GN`hhWZRQ<QC4z&Oc#HD;T8U)@yWUKp#>Jw>l5SWWX_>&ppvD`uM!h@tQh51fbPdpZNt*$3-1tRLJ;UT3hm!1^xA&8MQD+Si}M?jwxY1LAPs=HBUoFOLVKRlx;QGtzKwm05v9_<gCKa<8{o@^KuQZ&9CSNlgT%jOR4B4C-8Uq#6}h<YggqzbO~$z0YOY9Yg_U%8>X24uXtBGzldl^P@hLH+!Gq+P$LN1~BDV-zZV@H6R9Ay|lW<610*if2w29b+nZ>(KR>Z>T+N=ls{5(1W@wvn9J1Ug;O_TQoY^SW6!wRwJP89&reLI=!6hgOk@dYwiMJXM0a{yWR*M>{SJg%&&9c+o(eUHC|{c<wM<+0ni2>VGJBaaHEm69$Dqfq>de>FDFay=5~We*)WRrK7S6N{=|eYg!i|C#8V3YXknmT<0Y!amZ=+4Gh=Y_sciLiLS^hJ}SSNd|;IJYLGB5^@2n)ujpqRi65*{`5aRHkWX-lT0tIk^5F_*<v9sn#3i`5p9irSfSxek(PYe%2Bv^l5j<21Wmy<l~1#{G>SZ=Fcs7)#UnkZlea>fTUr4Uooq>_lb73Z_sFw=3f#4o_ur8j|SbkDR^FVenB{=i?pHh#<H5&1TnWZ|GpYPL|vOf=*K&b?yPPkBu!E1Y?V4M*~^v?nZLuUG)Zn^j@wHuKw(qy?~7{Cp>}VDXD;IcyjyZn#YhAi!JI?PKxQ!&OhDDNT2rVred_aj`E|>)Hf;5!ZNf1W<I7OyXgJBmvxQ-4D;*}BX3&2nTwgpGdhM~LVg?Q+;zSXlB$Orb(OapGlEk@;<+=fRlz<&L<@SJGl@b15zGPXGtolb+zsvyev~zcJi&EC02N4^?_*&t5!W#Sg|~Co(vGmH?GAuqQbLLT9k3!NiYLvf-s};ZZhaiSG)wLtSApanA4bKboe?MIrKryERG?IO<cL>;0G{IRHB5LPa-WMrxh0&%5@C#Ao*TO$@p{f}ez{c*R1@&4W9oIXae*_C=6-3Y(u1x!M$gG4t1<$d`y6<}0tstPh0!3&Vei!5`Z#WFeme5dxe#Y1xY&zr4eYkXuS#*2R=x%cCTs={tLLo6SK?j(&ad&sH;!qot_Z*M<jT0~g&l3$TXi0GUlhdPNK9evfo4)>`K9K=q0*Ho#FU0@xb5xz>5Q4yFT2M*Apzpaber}z_gP7nFnZ@8uple|@(uQO8vXWSKH&PUqDeE25ssnF%?Fq~mT6yis?#`vgJx+39U<}pin!@#>D(Sem{gTk(D81J?M3l_lory_QkVu?75cH)WA9PrD9q_ClYks#R$GK1lCDm@dMaaz>aQ|e7Y>C(R?0ExDMu`0>hPcrs%4YGB3b<-m+FRD0W1=~v(ANS&y{!pv_yKGy>>Yhf4bNo&2#5MOrHLSL#?aoX>TNvlQ3YxW~XXSnsxhfVLJsI1uCBN++efgv=;aC2S7+yH0Buan4~JHwluesZ3=?DWG-1*RSM~AD)}_elPmeeT68E374~TvhkeALJ_c`45Y^6R44zt--UiUPoX~Xx9Fy7H9(tvpol$$@Z9y5s5iV|wW?aa@iC$TCR;!uXy}e03^?1%EQ{zFmcfBOf-;$|;hvwGRj6{J)YQvGbj{WNDf2!MsWKaF5mf_eY_xHq3W^dDM?e=6N?{8zW<$W2zt6mK4_4IelG3JD}c8$0a972=NUQiDEMAMK($}E$$&AACvP*(o{nRYKf9L0g)T)y=tINxlY#8c5Y3B5O5KQ{kg6`KihfS12CY(Q#2X9T|NK2-_zPYJ3Z=tK!YYckq3?4zP>CiB|cCtXGw3_~zjMU2lfuI;R2#u(|`80Y`ul|#>A;U`d65MiEObS!~dyV3A!r{IX!g0cvvt{Ua0>-?H}veUP0zMc9yT<t=V&|w(^TtfEJFb~b7YG9%svqbKM^Xk*QBc@OdQ$Oxs-W(h$C`Qgx@r+NPVe9PaVD^e^o&(pb0T7Ahw1Bm`^>&y;%dQ0{-|m2CglaI_ArYCN4g`G1;X&w!Y;^A<Ch5F2<|RIV5I{OGsOCyPafrD2SqkW6E$Q}<d`~`D`f<mI1)pY{6S=(w-&0v4_CbC**bhsZo5>9}5&>5Zq)vlsXQ;KUjYLcp+DC8Am+=U`DkHvf#xu(H37(xzGEK}8h8@5(S>E=>^2g19XnDqEbqkf{(I!N|Q4&VZyt4nIW;ExPH0ubwO!Uk5|N8mq@GE-4&g0|wHEE{8iR)?~$(A>#_p6%GkV(w0zSo;<a$pVCvDZa?Z0`*+ayQnBh6~696~x<--Zgu|)Gr`B<k2l9<Q&<*SIgs5%4BWcQ-;tOnl$xD!J?7?XWJAnA{q1E;5l7Ep7*1|qhbX=EB`4wyajf-r!1@KRm!UXcn6)onJd;5FJ?=h4l33`0E~m|RM_Ry`vyPa=g0mkMdD*V5tXm&T3Wg$>65_VoXe3xAjfmcs&rUg=j_NOjz&RCH@F-=fq__lOHT8Tr%sCqiAyDm9vVtP{Fss>C{4nIqL|b!etq*fvq^LxunrKAEXt-B(oj{5uRIx+E=R|WJY(;c2tr(hzbt`F3HR2^ZCtS2kI62rTF3x3)_`_vmTqpX`>a;?RKVP+N`A-PQKSk77TTs=Nj2ys+d%3)VQY23#Wb7`c~799lK04+mlMFW78DX21YI+ICrVX~^Q$VmPvML2GmAH<AF3a7?AwwIM?F{MsIU#wANb%4)sv0H<TGDQ6XqgKsHQMxo_&qh)-8lohAWL&rM8T2Yah>PPyU-r;;L0L|Gcv#28I%hWO-$+i7scwW$EWcE10O6C>?Ct_iqEMRs3+?0!0U~(?rA4I5<Twy)Ofjm-b_##e!z->`<w<DxZSbgcVU1^=K~r=I6ay2+6gdig(~stQBYLOTWJecFRtv8#NNWtlWBdL)U;@BXR8PsYUIq8W8Jc=wAe^U@tK~nIN0h)}n&bI4_oAFhQ%Q=PPMx<WBGaDep%xECOq8{PzlA9pjrQ?MUWwQt0->x^^z)pk<(5tkO^;#@MEu@a^Du04yH@tVK5m5ZYe~SprHnsw@NQBC5dFOesKyP|+(=lB<?sYmfxB+x;8|i0f|COe%_u47)2wDWwfn;0@-1Fryr@Gb+7Pp1j4CeogBkNKPSwpddqJmRLbf0bk5!>NJ3a$7BZI3W>9e)Cy_j6<E#xkCf{ZMX|=wC$-}s(g0-u6OJQvx?p!7zhV1;&Jlt)LEXqQcjMxcoHQNfCWR12mH+~V3v1Xl;-k<xHyyiAWJ!p+5|0*E;8weYdrA1G!D=f~Bm|~or&HxeC@r$@?_kShGPHTlKafOn)bs*&1x0w+F({4Uq|IJxbrG_@8K*8`BFc<ssE{hmlEtL_J^hI&%AgpfFivGgd?~6odxKOskLHnu<P4MWqmNtm4olv9h??1ZWf~ie_Dn=YkfXSiJ9zYyZ9nB1ID6om+vLC>wGv9rxcT}2Jyv2edj*zhQQ<8+PZ^2PspWx_?Fk_Fnc73GK6gxSeXSKO|4CP1B*p2ZiA*Xx1*#@6akk8x-ZU>N(#^Bg=j!gq73l`P|DOrh+#PTDHKf~hS#d&&O6CRCacOC*?$_Pu;C=ti$*w`34`m&FI4Ay4E|Vo80-fVxUS2F<&pw;#p@`)|1q8y-%RVH|anRL#QAYhnU%w2w>pI${7Tmb*{u)q`wL=f(+mDYa%Qe8QK599IZ~OTC!(o{<EQAnc5o1!HN;2j#%Q@A1a1Qm(TdN61^@sZ}!>_XSZP1FL^M5?=W3DPmMYX|rd&}Q}v$)rwMyQ_U_#>L<|G}Z4$NyT;v-rjq4l&H3_15yNE{FA6J)VOQyGq&>%Y^C=0EWA-V4%EZL(}-UjTq9Ga?@I{u8v`#DN>e~1{`bP_)?4g_IHVl!;IIkLjxBN=-fB+`9wBXuYep#*Iugg_y~R)e_!!|?tAOxdiu*>X8Yy)`fmODWqpxPne2W>TQ?%!Dkbfg_2ZN*V$0n+S9_d#*M{4^jACQm!14jDMrbeCl9z+|`(J+g>-XPY_~$p$$<)hsI?8O%<swE00)4tg*HwMMQbEE>lJ`kd{S`|0onrPW82(bdli&VwyZueJBOG_*P|&-qJk!k<Stmo?c2mEra!S29rOows5aZ{4GPTxAm5Ce6PsA=mLHANPURWl8_0;f}s?%^7dY9Z-$3v=UP&<uV>UP6mcRT@Z#rv8vXmG_U{(yHnsOBbM!VXf(oF)Q!!#Y%Xj?;!=a`zXKQ@X?*Q*?6|fHR54?xULR>KqsrXP@wT1X!4Ur4W>wZ7m_2*Kn-M?tE06Z{)|)MXIEbJObm<j-!iG^CtCR2T_@EnYP!%R-1oJHLwe&Yn*XL5(mTB&|R*j`GWznT<Q{j4ddEYqXwlZ2*s4Jn>_yx*4r?z#4TmNjPOr?{PgpW|M>F#zyA?7(o}9MjcPG9F+!uMXQ#rjh-MS~9k-u9|8mBnp(SAp>+~Y(JQSL>43`G?JEdF&DUI8g{bj5CSm!{0{`~p3n-QE|54mdv>zMgM4I&5e5Qq`y>p8JY91YHN&`CI~4SwK;<(w<N9-kqZJF9Kx*n9cuS6yA{%Rk{FO++lD_?DJy?_9&Hj4fg;#Hyv%ifEwe2$NHXtxG-k`i=`8Sf&CT3kZd3)fv@gKvW+JRYP{=1EB|EVrU7Tr=_xmR?bClcGwc)M||(|{~EJSz%omyt~0bA<mqooFD*j<7?iY~KK|DavmCybV#jWBoezQy2M!t0S5Ixh%ttzQbDMrBP!Ps73`ZM?lfn~XTVuD_Vxo^brECO4QfXNs?f2pI!>bE+0aN|hm0MahSKvrYp-~=%AsjiTV>TRt9~t*JbiU>#w*kDx2%n=AOMN2FJy)3CLhTSJ>c|CG)wv;i6RYyqQPmsA)poo#?Mz7tnk!++)v~s=j2)53IOQy+8CP4zgQCH?C8#}@SYd<509$0-Xo=dP-X<&XlLe7+-am>6slBfotZL-KyC`Lhg@qMpBjp!DRiJ;O+I`?fu=H)AfL%VJ1kl1bgy829Ub!~f+l|t-isJpY+jHT;5UadOQMb$EIPbt^as}w}^)63gFX$r~3tmE9sFuB4ja`Qsk2}bjrMKh2Z~4MGh+UcyUl%M9hL?C^o|)jfV6eVVtT5ZDUuPx9Q}PQWR!pNx-=x&^j(?uzxtmtsavZh3z!>xSso-SEm+kd@$&R^5e7a8H{YGHrPW=|QnFZ0jW6goww15toAPz<s6>(up8nMRb!#3KzTRAz8PXe)24#eX&Cs6%l*M%mj&>u!MrI)>ljBw%p;&KERcnKj6J^;_;L5aP{R0P$Zk&oj;z`DjQx9^%t@pNjr8|zYW8w;9VeFb^_b>gm-wgSmJr{f1gL4>al1djLOVaxP~Ttf1|u3fs$BfJnEw@F~4BlC@MsB7#dbj&oR^Cn)Vn7ZDjxO?RWhMLlE$k6wJu4CPk_WTsObGAc+nhx%2t=`I_FSl5#RKCZBZoH|I?tTOk*N7t+HenZu<{_tH`Q_QoGF(TSkM-{&Avm^MrTg-IiS0=u{jAc|8iuTN%ADRmq2dM3hz+n28Knd$uTO(4%PEX8)ZH<}M`N9jDrB5Aq%BT%TB1ejxh7en9_pxK2Vs3UggulL2nxHI;qN`8<hnpIG={R%xF_PjH!77-=8bR42bI#q>ep5Xb8s;d?z@_xse&NZqOU=l1$;hFL#v8Evpl0QI@{&S4VX-%!HSCB_$>)hUMK$;{4CHqhdS))r?57YqV~cN$n|{iYjZ;C`DU>T_8x2_VgFk?ftV<iHO(D_<%)0!=1ew4+19^`lgw9Rwz>CZ{50-`u{zyT^omr=G!M3rl7P2jwi$sK3bWk6VpG1SGccWfuujAJ!L3wNUt>=O#~?V!&8K;46k5VE`;6EF;&9*3*%7)gj|Zbw!39$@8c1%HS%E|NeMt{^t2<WmaU4BcQJ-c>O$4Tl=QOtr>RhRF7!_9}+AedyDHrO!&t=&iL;+^XkoW@*f{Ya^2_+(zk3Q7#d7t6hy&_NqFy&atBT@4;AO=~zw7SL;w2~-)s$<Y~v?b-xH8<qya$q-<KVl_>V11lBV4a#wAL>R-Dl8eBNf|f0mY;h5`H9ICoe<)RiM+4OmV%mv=uU5oBo3yc-+^%Jxe9H~*-=X9<!jTVmTBwkOM$hK{gYVV)7E6`33}|R&U{UsGLWSqQ5t2I1dKvu;Y{0*K6C@i$0&HAaey-1_Kh7zaBOd*O|OW9lt5tBVqjTD3&&U|d#vEFA`CJx29F2}#;Bl}*si=jYUtwvdi>IV2S%`<mUhf#ag_%Ei^F2IMWmv3rd+OrWZK%%C$8bkDf>9hE>|yDU7K-#<HuVk5;(@vbUx${0fxFa6kG$Ou^u~7S+RmCl*8@H;e*3dnVg0sI{71K?{gS@6xR88hg96oZGN-ab=n&`n6Hy1cYvVNlt-O=!0cmVO9sK%qS?_vmf9GRTzOZ$fgrt?>x0XjdaedwBg_f&3wcT^U>cs>zKh&3<i%o(`jnGmI<)go_cGF_y}GFw?XIKzC^Yp=%CoQxt$>-2smLyRfA3{25&*+Id&J0_)^FxwuE~s!A()Wg20C}0FNCD(;YMBMje3$RBJtcA*Q#J2A)*C6&za9Ife7XR_L*p*Ztezm2S3UhM4sTfA%K3P&G)gemWb;Zfx_E4Yw5ey)OH6zF)5)${|;D@6UCF}RB!f(-DN%wUz#O%&yf_3#O#fVNjoD>%u7+7;i*8W^2qv$DYW|R%J(7nxhRx-A6YCB#`xvAu?rHf=iKI(Th%}{0lzw?UMCwDI0I?!mxd}m=$d2noJ_JRBfz=OfhR1Gu+~%<4Wb<OPVKFa<JRV<BM+SmaaMwhz1Y^kZd?4S6lZDWYp`I#X5g@T&RTpW?gild8ee?lnAYkFyG!$#jEz*-(WXrV=VA9nK@5(>6xJSSCS{giYCaq)U5P?W=}d&%-rk?im}&j8d)yNeAf8OO>Em#pm1GH{cMbvz!U7=QU~i|<Z!hKpuJ0<EG}9R27~0%?fXQQ-_I0N^jUzZ{mY$~(A}^qbn|_wg?J<N&Rq1&e@5b0i5C2E$l^QLDX|PqHAA3DE*;Ce;oZd1C$U$bcMF=A4>PQ#|DpKO1BJ$?Vg2Evy<rwsoBbG6Bcxq)4$tHtEvie6Z)eW-(SR{UDoeR^REAaqmiS#&o?Q$mmbTX{o2R?T$#N_FJIMlkTp7ur(ISB(6Y<8;Vq*=Ew7q(NdQJ~^E&-`d?ZY}QT4}g%aXv{I-F-cWYZE0>N+Y|(Q$y~DXWE0ZYRPt$_Cs*=`wdhb7D(urT4*Q5feGJ~9AgZ0s7(BHuy$zsoIic$YI3}~XJ@iUHJEQi*+k!HNBV61V&3NfDy|U`8Rx`DGdy{<X@tjSj#)EF}dP$zYB~t?r&8@2$i2{$*h9h+y`_<L|RJRMsp88QO!?8{7?}?qv-lo~w?a4;o-^OIi`!ax6y%^f->F=0h%n5Dn8gV5!geIT8pd9vzrXh=zSte_na}%bZto{Kq?OuL3iUYy9eCthczS%m7r=oEZdT+RXZ2rG0HWT6iFMny+fYgA_2wYpF16U6vbLtGJn;g8hzS=Q9ifKWc$-MUVNtclZ!w?Ks5!1$>xVE#78Dpe#W1RnsR}MXgg`YrOL4<jB(Xj+-?MB0^oq{7?3(6vxx@wf0uJgzFz~*|G>6$qPXBU!$4$Bze60(<ud1xk80~7U_C2}X6SD)q`F@<WF`f>mA=HN&{k(ue@8J|GI*4fj+>=oHO2d-BGAQH=I0c&;Z?J$RyT?<aW-2u-C)nK$kA~Hc82>6b}gU}Dz=-x+6(s^slOMLzyfOKF`&6R%Q5OMRf6wt|9((NJno_w(M<BkyvKFu~Ka(fHDr?N!sgZy%^AC@#XlN)R#0<IiLod(s;P-|NoiI^(1kKURu;}LvSMttRrXO!&|JUg3YnwTRDJAi4jyzPzUkDCF}@{G&s7Ani5O^AS_B#fMSW&cIZXwEHZ))9D_=$G&R_4Cu=SM-FP$H(z&(oBUD*VR6fEpJZmS2d#{lbBt7uQ%D`z#6P$uZ#NF-Wz1(Zmbmz7mx`mh_@rXYxabxUqE=sqgzVIIkJDRmdB@*$=bZ9452YJY3h-JMI`~wwkcjjGUmO(bGm{&??;74#R`5_{!?~%3+!@FSyt1llve@p4my7`SF9;s%$7bKRIGyl7zf#@u*;|S4SvMWkNs7O#K(LhDqq*Nv~*3<CxO8^mm`Bfj^~tB>9D%a*^x^eje?eLa5;Pe1F`&;oaP@-ofZ)imr52rG?aq)F(pS(nuG~OF{xer`sQ<HljuHR9UvfClua?Dp{f{Pc`__rj*c67#@;Ovgt!QQSpu07?yZ;GxL~;-lU-W1kO69}0qxc--P~IDS*`A=fVoqZ{EoY$NEHq&v`xE`YS2lxfz*4#*6M(ZX*eJ9o<Kh(?~yw%CxB@!C?qxrx@P)Ll&Tu%S5<bO!WZ9X7H?2LR6pj}w<Q^ldalS(VH>7D@WB_VCmV^$XTF*y%te||O<~MD`x>pSTL`HPR~oTOZ5iFxKAzK_{5O}xRjXwFd1pxs3?&%J^2%BhUCxTj($9%jFi|s6I@q-D-v(Bz_~E<-iVk3>iH4<daEe}fUj`&E?Z-rm1<l&op;B*EJ_WG}E21pw(Omk?&wI5Hl50N|@4%;6E6&!Jet!|{mYq;HY9xADx%Kddt^v75;@H_!i`rQ=AlA#!zX({tUSfPQK{l(cMFppEUM$04f>uw@SJKkRo!|jd-j85d1lHX6?-js0#y3&gk<8_!(CvqH?Oez~%Rs$YrJ+WQu}wMQ+rjYwSUv<;i*61ew7(Rx1e9!4Sq9WaRDrFTQh*GhqF1COS1rTVAPH)>`#BB}*WIR>R1_H*c2|y4N*k)c8_WY?Mmc0>RC=d8d5bIkn$|;*oI(UaL59dIv4WfezL?F_X#fe2$qc>~5@#2w71GEnu$uoLDc2{8VvVCuYR5sO0m=X-97pJM!R|hO!}bB4BLr`Px{+n>#>FK$X*$YH3L%Uv0R#*e*05{DN1=0WI(DDPk`Q$z9xbfEt#%3blJHN1)mEfP2u#OLr^=5|T4dkf!IsHnX!D$ZAc^Ft=>_Zxitw;wP#VKYo4wTPB4m9tPF=!8lo`)ZAyt?qi%I!=`V&!<K`}~UoXU*&QdDpD2B~l!%_9rR87ARJAGhosmb~{6HM951G&UOTnTU!YM{y~4@aQMoe#$d&_P{r{$$>v=C6t<R^Yj0Eti)vY3M|v2!drHpG7_Ux%L6Cd6F}}WwTD`L?wH>CS}R)qldix>iqlCGnN)TPR83&wY?(K`X<k&Mn`f)f)!mOP(hYq7KNGIGJKpeXNVn^<;)E2H%nPdH($ZGlue;H~`~I7gU4uLy$~yXRPW+)<CQCvDI>*JlyjZ}VeKyrY5zB=N2!x@ReMp?+psV?!jQWkfei?Gtb+k(@xN+V6HJ~DEhaSqeA0JbeYk*sQ)N%^n_VM|L!!m1F2qDTM#-u)#WXxlhbE@~?9O|97Ruhcs5BFb&UuEmtpcO;s|9IZVTvd{aYJ>6imcIjMaj!v*P(91>M>Nm>gF``&|FxiJ@r^AUVwgkgt>sx=4(qjgJO?3mm9#6C3Dq9}40m6_KzYlCrtxtbF{Cf$rnO*Q9m7CVq%1EDIM%@Nr55|`?-Ch@8Lwf71}+}Zxo_t4iEOT30XdMay;SG%5&Sg%zTyMj_twev^q0TP_RIJ6-S+j%`XZk)+5L>RZbZCQO4={$$0=FFmb+w~9eGS&Mz676VEJHHBcvBB$;*NK{VzZL_4{ux`tuv<VCpxSSORXI2jJvV+<udaA4i7zbPQ`01aY915@}zw;?_f<%pve2-fSN~lie0|WiI4zR*>U7m|YTW%q~QS6$JkLB5qcyL|JJuKZ)tT!sWkn3#(Y@Inlao%HRHSyZue}p&YAVD0qDqz~I6Jtc9iSx2o4|Ii=p5(&id_i1G6VsaoWxf?(<?Rqsy(twX`{QvhyQAA*JS@RzFXF$}%SYOModRV}J5<}F#nVX#}>0IBAEO&R>hVikYDI~`P4+Y=+U4BwJ6+SVJ^G3s-GJ`9t)zmSgBCE%Q*kgcdRknrd}s@X2ff?;vm5idl6h3S`w0mr}=k+KOb$GYs!N45D5jtnQD5*o=PFdpqVy5$KT7X&+q>dQ;KrXIH1{9{VFKm;=})DUS~3}b_=fc9hv2FQ}=i;U1Pu5IK5P?LlhT#2{J^Y5TL4)aQEa`wvz|MbUCKmYiTFW>+BA7KYoWwX;L6I3%|G>m?>s0@qfGQ!_+`}y-PXDk|eQMS;HFKXUHAy&)^65xKPT)QBrbsO@(Y?UADB>2ytKmT?!g463EcP(8WGhe7P=%A9a*n#zRFvMjH2WL8HAsyBRBY4AW&{f@!&ydWW)i!f%x_tp3JVEgSuVCt2L?x#9mX>SpT*Ir3En*PNDx%j?c%a)1vyz9cOFj4cj*~Ev-FyjlT_{tYk=q6x3PT}h=^#DK-jRywe}G215J|cS4G&vF^@{I({$FFd5m;skxqViq0eSjc(nO5_fP>OB)W`q&VP4bM8vNKzuH{99Hr9uX5LBRkaONW&ySYs`7Dz|q;*}!`#k&C#Dr;l6*ebG*JEiOZL>hTn1@-sg^uwzQb^%lU*p*v)bXVX=%$-u^lp!2Breii7fgc(7ICQ?)DffT8#R#7x5ljt2&OKMS9YfI=sOHI)cGbBdn^LQ~=TXib$JMqvH+^gg_kc^F$<?y9^$H%5$2jG@#TiLo#)G1>y(OqUmssI{$N*d9*lDR5qNX-0@RJ3Rao#_Q0jo{V8$62S!n;VMjD>d@=pW`6LdDE@;#hv*MX>a3p@3aJq0HaHF^1sh5nj1A`WlYXu8iXSw#|28z7fm&N;SXB<2diYWpb4V^Yt!IS}|xK8Vf>7U8t5#e2wj<8FNEOmZrDkz;F4&GKyWA5m6f~5r&s|Dz2H}x}Yw<PpoiRs$XZN!&LGMBvwqLO5dH9glG}-{@hKg?=_Elo?wjm{8VtV<m)wihIGeVBtBgy@O}rlvL%0u`wN3;-tlBXHflhCPB2D2=1*f=1osIUx6y9e%jvj$5{RYZHI3VxK=qUDHkzbDe;C!2UN)sN!iD>b%Mo1QC4`zU0C*-3N^C->BB=h1d>jJ`CKq7Yyw_BUr&G(_SeJ_1ShRoCSCH3ODehY7Cy~5!I({G&9T4?_!0}!@Y?=O$OGqBrwLRN;gcpkQHVI6$;=VERe2v|NR;i|D;>61oQ`ft_4PLo{p{Dd3GJP9B(6eqve0~buIoqK@MhUkwS8rv>Fk;IBp?r@E-FQ=_+5QM5t`SEtY{D)QU1LtC`pdJMWw?$uA8Xu33V>|4O55%G65Ep<6thZGYZ$T;sB@Y=g?t-0BR0TBWRwyhxjzlEET=F=#(!6;v$4QS6*5j5(iSH>Ezu&`WRomW4|P<rgYdi@!sb~D1chzv@b{ika$O)98bjG>+!OKN8`a1t^Ts!2fJ<p&^=m5>S-1)fH{4CoR6!7H(bu5A20ovsq1C>DdEL<%o$YdE15GB<;6X-j{Fa0$Z;)^deimq*LmhU7b6A^6QF~zs<a$2%wK*a64Aa;Jdk?meqr)woKui?Mn&u9|az!`<b0(XjYzv>oN#?6D+uZy5jT-mDSe@=EdZmGJng?4!OTb$(+l)XAg-deatt#Ks8JNyKSf^qA;8v=sudx}2;|v|-=F>biDr{kY1xD-vaky{f?Km8i$Ai(T;DV_c@hi8=tiU1szGN$~)gCSRIF699s86$`CIVB&bDCQQb*^MtjEXB#>zBFTlneFV=d$b$q5v~xNc;f@LB<1@gc6axOCJh2z0Yv%UQwn3m~yP(lBoF_5QD5<T3uraT1k{Y)iLNg+FF9>nj3O;Ij|ebAF&cbus+Tmuue^GA9W)pRTPa~#EhF=>yADD{KRC6P6%<uM5bqEOF_*-bf>pP8W&U1??AZqTz<Ib>?jHR^0jGF%d~a&rNG+A{z<IwX>0Ox1wD3EXTGLR8OYL*D2*~N3Pz!_aHefYAG(3pXB529I6yhA`;HzXIJURZrdPy4N}#N3F|aI$jbp5nJyvj75e69;gGYn~V^mN~>{DMKHS}=-BL-=_1S42bOFQPWxXJ^7#bL49B2rO1Q!dv*GHvbX6Blphlzp6Lm#Y`7uFbf=@#C!%2^?c-Iv+9y0Ylvz3a$atSdX2ktXRPm%Heip?ZV-yOin`*o&1rr_c;tc3hR8lLrSgZHow{II_(V|%-6}1J3!EB%A?LbVD_=GC4*pW(d=j-OZ}@zuDq+>K#<<c^}+RRJv$4q5$1&Ji9970Fbz*`-#+jd@?x<?eacBO9oqS)dl~7|UfooTcGppU6q@=b<ylyUR=~{1RAd*uzxT4<7=U4(J!0fd>o;>TyKF|s5KPE#1D(6h7eZ3?aHFpBM$PCIk$CQmYgMq15Yd93=geT4Km>CD`%JV@H+O@(gCAuLB2RGL5J11t=KEM!OT=}IK;iA2wKQC7YP$oVn3PbWe+R6{iQ-AKhbM)CLet0MOS9zeaTQ4JVqjEEvW&PVo=8;meukSWAB`T{L-2<*?0)mNQ45<wjEUZuCd~H4atN6awKjLX?C!QBF@9$?Kh9&O1;FlgOtgY~a;=dt1fJYhu930#&EQe2MY0|cnn0OlwA(gtM2&vu8UKql%ZSEPao}JWK5z-ac^p%aUQ4m_jr?=WJq<#v(H08@WhlXNt>GB&sUIVon~^qoAJdM@R1aX8pj=kZxgM5GbufxrOIcPNED)Jr<B=;})Ck`biOnss{T#uL`$IS%@a75)$8K!KUZTi@OPbivG4Hl!1%WjI^3PmE-WtHP^HiG@+L_vce#fl~{n%n`$8>TI*mWM0WO~2d%-$G$yfWx~o(5ab_z|7NzJSW@lM^$hgjSx&%*t1$DA!2b1*$6IK_dd<t-+ia@+^)iB;@dz);Xx^St7tuOUpdT<{Jn#7#^ykEJ~ENAyOb8HJ78Br{zUK!kZ!9nxIYz7t@FR!u#k~KeDH?WpZ3dcMrdLel%_V<0i#A)Z%6^a$|`K`_|iYwK9Owk!Eqb?@(=k(}nCk4-T{MizNR%+YU3H)`~-8tZJ7?);$If!ETAC*ZWIP)1O~v7&x0Qdd=sI_&pypoh~UWmxSr(j{)=MF-aCvje%}2;S|6u35VAnV8O^CF@6*t8a2y4()#Sk2p>>^S}M2`kA10Lv_TP7rvYPF)xH7T0t7-&iy3&v7ePVTC+Y|4Wn^@^cte*{qGuxaMSMN)tvCgXOQWEn3{7btT|DSQZcy}MtNTg454(3fN6DF&OzjYbX7yG&e@lkwu3=4N>dr;gK!4dRB?x5%V7x&;V~=}qjR$bdXlzrH<ncCGS5!HmkuG%}am!@ONi%&G^@eC~v8N1jj5nd<ei!Z_ohtBZRd9_LnRCs$d67veS=OBWG6jiglMz6hm=O1oy01Pbj;J@p`C{vwk?IrTAV1GBoEN*nL;-_@nF23UMjUc7r(^uP&w)d=DuLsI7N=X*l}s$JYu{3!l|Qdt!d<++O`Gg$sO+?NaNLLA+h=n|JP$*?SZB|CT~FB$-Z6#PDAhKh)#;q=0y*y~g0+qr=d<%TI{z2%Tyw2hrRhh43ffwaDNKr3V>~|_141M=^d7;UpsjMJvCO^fx6U7D{hd=U5JcJ#pE@1Z&k3xqalA-x#{fx_op#J&m#nrG%d<yHVHJI+>T>gNllybqq~#=KiV2>|$Q9J!cNd*m_*YnRk)Zdiey2=CwtS0;Btl;y5}`F&Ke+RC-a30q_|?iDWDq(U2wGWpsIP~uw?p?g)(KX0GTFKztPKT>c1Q%-sBa4gaCi`M5|-x4b)7Wk**@JG)XHF9sCP3?b2dN8=7rF>SBZSk9iNuF+ewYy<^*hIiG@)lfPJ8A4QzxZO=ahPM2YA-S4uLVhB(&V)<*8SN>-z{<|`j1cxl__bDpVgcj9acxf3d1*!IS<<ISjna6~}*C~$AeV(mC`>BxRuHks9w(%d4{DfH7kzx<6~KR=znMf2;q@sD4VL=fJgqgKD{?KRQ0z7$ulW;tY%)+@VolO0}6T>`8Kx?T1L9nBl-#Vxvujy&ArhPXZ?LVE7J9rre}*UJzs)w@^c!eb>-w055}heN<__Eeg|YRgb#D!HS~WO*HHw}S{`?tDLa>^=qbvx4>85YwF$vwh7R9rU{8)h)d5&fm=GRx&u^%piEv#=fP`Ar&Jb_$!4}f+Yfe#6YuJZ4n6g&HMf;Q|e<rz4p$tKRLI;u>zKks&9F{k`)ZrN3hra3cG6QnxwdJnl9uqA#`YV`$bZ7Ktr>YOVx2}v!xqdqd-{o02C^YZ$~&)ZbgG#x^${liwSLmEH=s<>dYtCj<{BfHP^`%8G+w@ZiHeKe^UZDgAnFwrx#1NwCdXftY4QZTA>8jYvG*L>NZ$mHfANM=I$o;w!COB>@o%c-O_E^t6F1g&?BDjFdx2xtM7h9><M^RQnZ78SO;hdXy+zBWH<GyXx})8igWQ4PWeq7NkR~tXWy1hIpXOeOSfvwb`C}MR-Y*Qlg-8YT4`d$PK{@w2r;#bzVgzKnHN{X)=$n7$F`ypj`4x=5jpTNrOAI!N$|KrFP^s@7fS(|kYk~JEx0fJoREJI1t8^tz_czi?`x&a2#(0}efCSbO`4^m@Tq{`t5^2@Il$C4b+&v8Y+{x^(J4nk40hmv*@9U%-3W=kIn7P8bi24n5iZRv{r+N+KsFm&8ilVR2cy_HL)TC<K>iEa1F&W-yIm6T)wQ3K>R-h9F5A9NUc{+jwJ-VmW(4{{$2<oU*n1kBB(sw1$OG-zuUE;DXS&7~@c2Imz*lE!=M6rcGnpu5E(6U?%(~^}2FPWYO*m00LtBzv6V=lfZZ^w51AyxVFgGea5gy>jWpk1|B$;<}`A)~2Xb9?Bub_~CWtFA4#3lj?t0hs$IQY(NoVg?QVA>b}wvNIBDGBMg%Q*V25IAfxfC9iY<Iqq*<y%I>a|UQkGQ<Ol)|Qz-s6xtF+sB~im)I9!>+7e+{tfE>u9nZYEi|4pTM}B*#2Sj#ht+Oq-xl``zuHPd2}%3dTUj}vGU~`OZkY&{_E7rgOx`p4@9L1<Ri^5pl%Q^dV|9CBIS>;_rrxJDbqNb&W_v|toM8ebX6vKspDKZsV{W}|_nD$bvsXy5Te?pQc`#<@Ngr!MB9Vd$1)`GKE7REM<|({yiI$USxr7`380=&_+<6}H#3nY#taVvJJ@7fvHt8pk>c7W2jiA?%GS!ws@C!8yk>l0rBV_*`oM#p<a+%iGn%nZ9e0A}^hvufZ>AQ-zsp;S{DQQg5dPJ3AsEyp4X2e9w%`QCC*ZzbnYLAn-_JF*%D6ehN{oM@UjtWl5(b2Saz(uKzQurdT$0yZvv;P17P}b4+nu<S^%VbH&(X(n~4N6~LY^_c;Jntxy=?)=SwGWA79(0diTCu-z$*+ppT}L~=f@`@2{=6SD9eOC=etb+>t^uw*Tgz@7Qfu#j7}QX}T<g@I*D>QsRp90^%Q@8ua1QlOwyH@j^@sZ}!>_WPi_waq^M5?=W3DQBMTMw%d&}Q}v$z)|MkpEQIJKJR{{cVH<9{s}L40EiuPWvheQSAEm&1CEvaMCJfZiM(bZ}}tw6e|>3^e94+G^mqjVcZot;)3^03E|XQ^e6dK2g9-YgqY0zW?@j31B=^N*yh$hzE4;oB4bqo2!jL4y0>i(|LRZKaIby_(1o)b#guZ<u9}S@_l``fBmw45{|XkKmBr%sxQ(zlSj@P!Hfvo+Dpd(=T1wPJiW{%$hmxoQoD821%5rdpC8)S|MDeK{PBLofB(x*fBpX3()s-M^gGmBx}OKvBkAk628Tc$k<d>3U{1$?WEl0QKYsf8$A5hJ3%~zS^|RLlxbNNipP|rls8i>Dp4_9OIw)Y_lrbpHw*P*f)tHVEoUhGjl!gzf_=!vL?q{V%128fsn16yIPj|csazW2Szo=KqF=S=G%$)MBm8-sx=z}j1P1tHYWqqCKd;RCPew;)S%K1&l<a3dgVtHnZRrB>$f*-N>wTU0`s|<(o_jCTYzuazrdpwLnkxt&dKBSd}z^cjDXX@I!R?4n~LRIUF|F)`MfG;DW`ytp5{&KF|0Aw0m8GKVN0}OF`u|*=d`f`Mf;7eK^?Rwq{*RQH7q3ZtkP4K=a6K#EVI(Uq9f&O;HW(Yk;5HLM+5z#-1Qgg%IUY%R3uf|g2f{zC-*Gzm-lIVQkfJnb?Hb@lhjQadwz!L2{d9<cKg^s{Ds9$$`*pxdBY$|cw5}C^OTi2p$0X7`%*6|HnSZ_-agl~PrLuBtZcy^&MDR`Pg%hNPvcj&%3{{CqDK2>Ifk5|e38|;iJ^CG8~u$Ebb@?F5+q};sQY`4!AoiWZDi+2xr-3j+A)o1Pc)dS3oyjhio){lxL=~OJe8rLy`ts&(Exe-tEVjvM+T7{-q>Z!2u69qQomsBW&u}Ab+L{%Xv4kgPBI3DFOp1vI`2Fs`(eE5fl|G(hcBC*|#zEf_4{>;zd*B<#~FW`O3H`Y@%B=3GX{`j2fiYFo($=mJt>kDzX{wfdCEXHVbb1P-2Ybj?yC5jN$UL?|CV%kOB7PPkL49QGDVFneyU?W*Nrm*Gpi=Q7-E*4JOcU=X(`h9m5acE9qJ;$JVVd%OSv~0{fR&x8JCp2{ZM+nx`VX`TB2N|b=$PdEKp&J@xQ^_CC1<Wv24<7p`Jr`TXNk-0ZE?u=mU2+dUuhvAl(*9&J5B?bI{7+i%x^#f`@<0*x80jK_Kcqu*3u9x(U&%kkRV-2FLT`<YboCrV*u<g}6f_nLhlfFKTkNT&W<xIZ$Q8vrSHK<mE+4_N*ITDKv3q&_qI*@2sne}D>m@6mM34y$y{ggB?-S38>bQ|q`bt$8`dl>!oL;#{sM5zlOYI=a!)QM@i3+&!?a<Gvj8TT^AChtV1D(!+E(wd|k4wmhe$86a#OB2&g*-*Itg36GMC~MQL+@ujG^a?V{JzU=cvJV%K!+8JnHLVKZs-d4Fi4#{SI{oua9|cU>60u(WbEp5kghWig!I5;IBFOai_T(-1E)!nT4bK;D2B&Ejk=qk1m<Pz4VLC)FHL5Y;&+CNM|X^BZe%?)lrq4NSY~((Fd+xP)!w<X<8wZK@o*4cfg%$RYX8Gvn6%dWgSL0Gt>%i^AA_^4ScS2w*%C=p_6FReoQ~|=Q@4VZV*p0U|Hs_7>_~DP%l^<T^8Hv+VnK%h$q^_Ky|@eg|6knURAzN$gt?h{RLwa81hCc9T^*4b4|j8OvzQEgAK56~+7foDEGrJ1s1k?i*xL<|6l(--T)^BmO4!CBp*+bqj=v^LRW^4c6+$><BZc{i*jUtg%~AG*jHO^Ulf3}!eUx0Z@v@K>=8S~uksP8d5R7K=H8bm6SZeL$QsgL$9}~i!ne-Xm$IhdpdGom0^ct4FgK5mKJkmlS>^{`p_n>dc;GOk1b^q(-^dgO)dY3T%;rO=cf1^`6#x&$f?72a`058C+_dI#0@fG^L`xT>^2dwE~@?AJz85&4$Ts44WoCbA)x4=MdfRFdOmZ!&XmqfR5Moe3{9KsIQc$BNl9#=9>ESv_)dA7jHG0rVNPO7lX`hi(xC=qQ>yM5saB}DGIC~&3UZohv0{h+86F9H)_&Y!=}V(u_!=kclV0tbIP_P7sz0evqtR~hZj)#Kxa6DFT~LlmhR2zPBkzd=AVrM+iNryoKjqgP1AJlKFe0(JSzCc#17Bjm|FKmVb|8Rt2JlEcqIESa=I)ywO1eeq%7lyKG_7g7}}ntt7qi?)sI$||0<Y4|+Ma{{2d5B2X~zy1>w{PEr=+GwZ|Pc&dLceL_UUhKC<xz2_KBgm)2B2|5H&jw0bFB3NACNt~ssBv+idGo2Oq$vb+^4E3&l-{Q%sMWMSuZm!*ieV2eQOb_Cc!^=InSB}3uKsvdOXoKABZJy{@gZT=CqGn%kX|2_Jpsk+uVE;rSjG0aP-HE>s5kvG=9?ngzDTy_2CW^{ow=RQd`eI#P(X$XuVWgPfn%HrRdi4R&@#8W7>+J(@(zSbwZz>;WR58<iL!#?l1hpx#fw1n3j)Tdq_o&MIR`WV4Y*QNm-9=|eb2aS*=$BZ<gbcPP*fp*2RXcu#<<??i(-k(rbJOmDSppqwN!7P-1&>aE0-c1iDGatId0+31SQ$Fkt=fTU+EZsX-CBXXljYBgFOR#kE<2T{p@c|t<1-4Mt`LN*f_Uw<f0`Cj^a%P88)1<kFqBS1E62vvUSjN@^l4`QO~~Vjk;0;oGeP4otA1B30N1KoXLf5!RYGV3b_!?)bla=)qe>n@`#fYHDvOu^j#d|-h5Tz>d;E$C9JcZd$iaXfU&>#gh^#&8|0dqm=-PW0xM)pc;u|Dx0u=;y?@XObr_IaZ<|Zh!=ykL7@6AKv0{>&=x>7?|5MI`Z%mRgGjVUkV=AL>d?U$sc*tb&)U`CQc6>$@Ttzi{m%Gy%#X*K`ZdmiskT<^3)SfS16nMDWZ=?p+5aeqqsk=a2I9e$XX_0*xwq^Xd!znp=O565-O%mGnq-gT2h#%B_B>X|zFN<Ngv;Mp9b~mFU84E)+^i|5&Av_MoqUR7iHx61}p3M5*MKbnd%OZJ^o0Z2TkHJo2uyr5<f^H6KBosf#KBL$Ih6MhW<;WBdXlZ1;L-#b+C}YRF@mQPm8GXorzIoZYJocO0+(f;FC_dxahaKbD-3BMxodX>+4DC5H_8A8wUok~wd9WW?U3!gE_H6nFrnwI`ut@m@EV+_KIwmvNmnj4Bso`H3PS*>17;R)<bZIa<O4`Y#pXbP=rh+vyHTRkpOF)Gzb~CLAX~<mWe7bAr<@jY9^b&jYOI|_B+nm(uxzvLIOMi7mchEwny*#K0rrLYPq9d_UScj3Ei5!<w+=!pzZj0>XeI$8GU_I5M{m@%})o}|iY?6KFF1VuWFem?H0mC(#VLZ9v9qW;93RD}3sX0^}`(nT`j*4Hyxnw#vve86-Y#P_xF`>zx5Ieg=HCOmW7zU4XgY0b*2@0_xFq{SF_L1Vu4@Z5*QKnT~Iu9oDOgk~{8~Xfgc4ks#ISn4OR&x1Ocq#5y%Ht7jK8^AD*o4<13<Ji?xM}73T*l%bD_6C~Gi2&);3k#UQPZS~CjR*bq{b|rjAE<+T$_4z(035>TI$27=)ipP?RIX<xCI7y*Fiw0E?xf=dV8Ipb&Pye@IHBLPs0K^UZN|DChlYw<2j4T)@y=zoBLw4Uj|qkv$ZzR!D0B!2v7^Tsl_qrBsFOobVL|NK*claHGGUR0bf#d^@H2mzP?t;leRHV0QzL)6YBinX86w>gWOXqSJ}g*RgA)c&0XU<g#j1^*}<}raYx808Fg1Bai##zigF&Z#31mThddHbGd|yVF_%owV``-)iW)Hei@6NdCxeGNH7;I|IML|KpjLs=sTK%)RuYR9zgr8ylJ>@0+%T88htSnb989ZQ&p|8Z)fVq!W+}8QF2*ati<d$)>OS;2Rsaj|87bqu+l&<OC%Kw+b`JIE%8t4$=it*K{f*GX(z^+6r69z4CA<M6R_8jycZ@--sm?E;@;fdGX9Ga2spO#I%zVy$^VJ7-OmBS2rw+Wox{dL&QK-p#EL3!ic4`<cki!6sBcc%rW4&OVgKa#^3*|G$5aU(^DH(d`as`;ck`V@ax-y=pl?abm4GO-BaNw&QBZC+NCmh5(DiQaw?Rmtbf{<1;0m7FOy#cE~gt%1IU(~O~jklNGZ@&0&NH4ja0XyVL<`fn(*RG+ES-hZ|yO5yD2QBhF{tg&<pXg4Y$P2jwBtk|-uQa9dTu$qt;k)N&{_`*Yh*z?+7dXEyc<?O$SVx<9j&|?!<Oo~4eV1_Nr3B@70?HRXd}1ZGNX!}L$&rUV+d;D?Wx<UO{v?P|9$)<Y$Jc*SDeiu<-^PUqb(Jrf&)2c|%_ZnuFt(A9+-H=hV~kRvm1Y<<NwGDsqJSS?JzH}1v@CpH#fsF>No=+5_Av#XI|<_y&VO@nHx_kloh_l@^|sZUwXO|_nti4{X)Idu9$oxTos(NIA!Sxo?^0Wh03pnl5pgkYI`hFll{g(!i&_az4kh$3_h&e7K}p@l7Ocu4bz$^1(PdSi4jbps#&Ff}Hn^(5t%`m=2Bt~bS5vQ-Lpg<nw~TPRW+dyef)-nd^OM9NI>ZR~h^z43KPVQabflHXEmOah1$Uh1v%E?->5tn>zExU_SRK*;L^7W1o=|o)gSmuTRNIr@)t%mwU#qHfjTwM=GmKvMKJlC_Ut|(=hf(BBwNdSfE4Pl_IE?BC8NN5^xQ~9z50BG)&IC_jWI^)Pjuq{C?|Ww8<sZS+PoXbNauXohKHIuQoLf(OJIu~u_L>T6FnuwLjMS$v_#n0B=xV4jbH7!uT<vZ)vMWVBOM!$c%V%gfsk3bp4IXj`Lct%*3c^Zk0t~@9>y$;Cecc7}K}O{D1Jb4?%~zSaE@z5MSV{%%wS`9lfo{!OQbl+DLg3q}>uqF#fyqo=s?l!HNYZ7FIz3-Z_lYm(#D}+SB(bRxmZhw}7_0wzg8RNi$9XmLZ+CJRwLWwws6BO~*q0m@s#T4j#jyr~o6)XECmy-{wJr`qS|84oIuQu&b{29J8?Y8Cr=mdwLI2T@#&41$9rj4CPH8(wJ*RFv8hS8IPhb&Gz^7Q@<H6=?5tnoKV0r05tnPz=I^<7~&Yl(kPrm!Q$oIB~ur)}9e;-ZvgD}OZYijmlFd{|Ke8+YYzC7RH-x1d(c=Q{df9&cv4ZF;A{z5SkFO`~4#KyN4PRE1iV4)6GS@a;xO+`nz&u*;`5z-27XK}QCbWGseXZ-QC-e~{+`rA+c{#t#TY}iwJ|N7nU%c%Ux`#G?$6_T-UOY0G!?RDAtMM=Yt(z<$ij~`?%q9<hI%;`m8v8My~M;vkEYtmw(7$T6i_z-kkll$S-s>xKe&V#&$3D%G;?)q6Nn&VWo)7KdW!DK%HCdkV*gvqI<I~eTpURem@E|^sjQ(bJ+Xm~B*f`RY-LLa#$`~}9nwNThay@_;>))yR2#E(Jld8HLpuJbz@ui%@&kz<M5sc4KR`YZV1l9l^Gw3Uc*5Ex_sqqbecdRA-9m1FSrJEzI_clc07u%f~Gx~vceVf9VY*^KU9p|_3Q*6H`->h`dy=&-khvzRroGb#f_w4eR_UY#wf)ybIp5H2;zlV$w9o|9V=T8SBz51S^f6aWLG;A@I;&SrJD2|WB+a|k_!vxSAI=)3p4)=;$mlbyuNhg8u*9ozJ@h;GdNy|)qLqA&q`KFja~n>)L+xxUgHvC8mPF`Fjh1FcXJuo4`3M|yILu@YalZ+|KT21pVV6Ljpm&nU_O9w<M$u4T4kQe$qPfX?S|fMC<tIV#0Wyc;Hj)$V89c20GAS@qhn<)mw`{(?17T+iZC?V!e{c)Pg5oh)R&{^AZ-sd9E9Z+6UR`L9N%O4WlzBf1MuF{Iw?)3$qWKAZKO#~0C%!1qtwdfr~@V~6e9Oi8e6d}mF8ewKGkW^b8Hje2>S{oq`M12#~_b8{_SLnC`#>tLMF98Uxq+@W{5fPhGfLPXrb1V@dDOE<B{r)9{q4HM&xxs!}g)o5xp6*>-P7jL%xnRN*TeMPxhOu6=5QZM5iwPeSS(mn%=%lD5$6ji^Ak8TGuSUZMn=sX1ab~Pvr%^k%iz^gLbK|Lj8A8dA=sgqW13I_TaxXgKZzoPc=L2*kYw$a=h{z^~gwD=vRJ}Y0NO*X0_)H$a$<MQ}9u17(cZt1LIU-<lG`}euz*1okZ83Zh<jRvstBDQjy;P131dRRo|i=#%0RhK%F*U@ip_csMZJA>MkFEq>-T-D)weNX3GnsSSdM>IY?n7d4Tc&JT8q6x`0=cN5mftYf*UG}u)vf<b+R3bp{N9;1n8vPw<BJX7#<6M&+^JLuh({C(`)TCS&N;`40LOtTRO&}!-%y`Jzv9<eFT*Wb+yXlPP3ZV%?el4h3U&P!O{G+C-W6=3NZQVOiv;Ie+W}5>0W%i$d&EijJCb51}R$mcyoTLSG)S^WJBQCN+`73<-$DqfTL`&+xF{&w1zcp>CIc<|a(6}L(;R#N}6<s%AytCL8F_e=4h6txeXigFfhFV?}HfI&m4|R2n%Rd9!AbbcMPI`yj{ZvRksFD~L8p6^%miWCSZGmOBB@)Eo2?Ok$N3p4LbGSkFlphg8M&hkxN&%OLliU{P9w_u7Jh2c3iipI4c@pq<RKJ8>f$ZdzsuKvfF(l)S0PQY1x2rx;A;ns=IF#t24e~`wWbWCtXIeee)GpB)L#`LHQBX>;=bADjfESUaZlPWYvc|mSFAgxR$HJT24lz$AkDYljDh_t}V(Z8<H^&d9+VRm~%N5*fQvJbE5n&HYaqIvd5Zz>j+ykI##1<m7J_K9cLI{duHO#mOF7Y)$m=;co-sQD!7Mz0BW*N@_2NLT(oI7dVL#^dnItCh0k7%RMQYZp!1TJjx5nIff{=C7BCu;_Loy~<b1nS#E8)#D3WU3-%(WP4N%(+vJv1(Ay|IUCc;|u$ij1-w4lbYUvWergi<eRNY=1$@0j`u`TxADhfS@(JMDtY%LYN_1JD>_T{+1BThbVjrf>+!`!gTQ=@X`M<TVDGhR(;gw_JS@%Ngzc$LxysZ_m34^~d$w-dp3W)SS`;BQ9Q}Yg5-mGta_}4t70Wq`?X{DwzNdZwSU(TDO%kN^J<e%uKEIe7@)xh5A(8sIkXv8{i>DhN9rUzsi~{Bw@}3K6g8Gc6*iwuoMryhgqK|u3=R$5kolum3k_x|G5YjZYk)Z?mG3zncxGk(Y0gI>E$Ltv3<Y!_DlMDGO7^^56YNl9%z&Zk8GZMBX>jLN%^QginhNFmTRKP|tl_J5zZLe<lCSjhLPtvvuKKadWx_)(06KM<D(Ff0s{hYv_SnIUrYgd|LT~rf=o~0ZC^;50Dgcm&&U=(Q93g)D00asE?kXs0D#mMo&i8&1kj~c!cEu(4At2Jn3o29k@49mfi50f$;6jbNE%ZQrK2~2jao4Lo*%6-;99W08ud1=>eni+Q@k!aPow;^rF;lF9I+oeCbTt|`)R*0-z>dKlrf5vm<N<aWLk;YlM+cr<Ak5c=7mZAV3#OuY@)}VIFsm|>=DF*OCdT6;Y3+qXj8(B8e2EChzTR+cILl6SuW2$wSOKxa5JcX>B>H6Hi)&~6ocJB`#w4wJ%nDo37=NC2lE-C5!9&BiC66OQPsRV>#?0Rztu3?^8Q3jcOgMhqfMsEFv;Q?_>LzN&<6G{9gZ1<V;fP3@(oI%yBXbGAh6(?wn4Z^7QZh!JTuMHsL;}4#(2sfdYnULeH$nME`a}`bkwQIM2N@y-P3x8Bp;`5?fdvVe??`@(dJW*9LM%CK}p^%gEv6(GKhhT$^1H;xV3abb89CPR!xZR&o6x&J(G$^)T_AD&oUA7Fiw4UXso=DA<2&doO3ABXfWpu^Dl!d}GG=wvJS~iG%huo8Jncg8E#xgK)#d2O4>quknzjL7zAWIV-cp~6NbwimT0Ba(qNBp9q2?kL=&JYbavWySb4Vj@j@6+dp$~FGD&w!sP?lgFAXRKcP^4iM&$;+6y+^xj~6m$r%#gxI~Txbe_bhJfyhFO9p8U|i%osJlw7a6a4?QBAE6CcG?A5Ghv(Nz7IT5oPEg=VQ6PZ(06P6U&1m-c%+w_~Aa;A}@cOM$Sm*oI0`1o7iKHttA4hb0>KOrJ%_02j1K{odB|^-KvqXp=IaD1-V8WpB}%kl9%|UFR1pi_)5i{=?MRpf}Gms$PX)GK-sj6m6_jItaS3A*N2zFiZ1r2$31%!xZAUwBn0vY4iEX+X%Y8<7|b}e?mx(vBy>!rcl0DEu|GTDf6`31rPTmc)0muhcX;v5?f6c%{MMqP`|87LIEx%3OXk(JZZI)qsB6OJ2%KCdo)Bi1Z6hiDm1)ToRObV;5H`uV!^6u^-~oYOeoCbq8!`gth1)B7$Xk)!fO@HlbZcyMw=N@FD+_JZEPT-fX=qqhn-0KeSeFq8}hC+z8I1rIvlpuS(J6A%&t*Fsj@(Lm3|!~-~5%A$H&+rV=y~EtB;ZIiY=ggq40F-Mi|M5;C<U!rOtWp+KxDQ;Ce(41OPG^M?upMZ^d&;ePWrFrK{t^g0mr7V09YaRyBAI;MoiZw{cZop`Kj_5mSA7V6+l+jC@Q*ZUMX67y7ZQSW+|^%w_V|8N0s)tn#E&S~2p91Kijm6eKV78N@LM_ebFcUU8V8mdl4j#FIv34YOQ~Ug)S$3u8DmIZuJ6zJZg`+`ifh>UI%M9vY@jS>i2*oK`{b>qXm<7MoyP%n!p|%{h+%T+yNqe0e&3^(+8JcCsD!-FC81`u7UjAlx?+0bJ;NuD>Ie&7)kgbY0%T{Iab2S75=V>wOwF!sZxe!U4e;&x=e;hV)Eh6lyr<KlnX%RIAZaF%tC4q~Xa@=u6PSv!sit?!SXpIOLGQrJH;?9zXCR(kR;eGHAF><Ah5$XY3T{LTkhexk1WDKC(F`w!qTkBmRIVyNz}5CN6^p?6xN^-D+RYOgkfK4MEi74TbSz<eM*MFOq+z!S8!RFvfD44|=Y*$Jr<Gj}Himl~J)YxTy2Y`Y9n^&LwTvAV|5N`p$owEQ-&_{xigZ8;SVS>T}GtdXIVTL@@8s`uM3rf6p<IrB|2;7;JuHHdz|AxPyR@{*EjU>Nyxf3!LMI_A7uKxCaNjP5kxit5{1Qhfsz=(8-o~hAh_CIoTO_^+s^=5$`?Iw7Q1yD3#T||N13y|DAuj2C$kM=MuGL6L78iXRDRCCQnk1wLGmR%>Co!boo23NW>R(?6Suo9W3b#FX(YuF8lCgQW$Ld;?7*pS?<!OWL3dIz3-aZ5OR!9*CgjY&7t$1=3`9^{Esk&NUHJDl{oY-$KQ&KDelHhtY_KjnaE$wGoFK8JD$%<s$ax~V0lt;?3>xt*1sr$!QJq8DlxxdY;ErlI(VitcMPAJT+b9M^6}26_ccr}Zy`l4!|YZqeFTVGKW93rmv_LNv>34rOM{po2u`V!0XJ+gk>S*=R$pT3X7IsH>j{gd=FP)<yN~&9qCJrYGObiMYNm~(e=z;mK!T20?yiQ3C|@%XA3Bu+jIeR~Lax#lGvVb;wC7?PmB~A(5$i(45(L<$h#&wvGnZVRSa6Jga5qQJ#7XWCh*-IBn>oqH3L9-TXc`K!dKQX~EVM0LSyQ9zDAQ)7SSWi4JQ)(H`Z1x|_l`H^`+4^r2fQ+{^J5_`P2z?=lIg<`g1`8YYgKr(B5^n&skLd+Z0ORZJ>=~+&f7VoL|Mp-@l513UH*Au)UY?S+wyD7?pz@RRPwX|g1uN8FH(+E-I2N7#oIwXw624Fek8>?bL34!dLo2GNZe{R{yE<%GyOv4lhJD!o(QSUSHQ9#qT_;kqa`IAoaeEp3uRJWlpc(AfJxU9HM*cGOu``L>8(!<#+o<|kmWnJzHvD2RQY<N_q=+GbK}-$``0%j3)=O0Dwyj0%^d)Y@VgZ1r>JUC>A6zvUq_-_v_k~u)ypIqF&_T-xjm_?HdVbQ@2eKY^wbofy5lmbD5HR_Omr*wmO&L9f?s7-(hG{R0a=1CSHSVFzj6Pc2`N4dg*hIl1y`7~kL=^8Ie~BE({J=Div(BhKRHF*UvOI7AId7pn;*BlD~oNUZiPQ%^kVBHZ+PBJpHbl#*hmDyc-cZ^yKS72(bW#*zTKa8*tvdaMBwf(FxB%<77yk7w~r~0Ee;>h*5{b=_kDc+VQ?G^(MD$UrziEL<Z&OfoSWo-ABK1J#ZiCp_+j`_w)q`eF?9Z)&-<9GUwUv%m)dlAAJx{e9O?GD2UD&2GV<epEvTA&W4ppr{v%4TPwGPUfugK^mpA6D2hGT9j}`p*!lF@Bbt7=xM$Hu$v4^#wW*);(J&=lD$9P{5<&>K0GY!CL2Z?w<=f0WGC$hEc6@A)uUeomB_z1rHnvi*L7~_-c=`Vkq?YGbC`|hs~>nCA5mF)LuEzb7~x8oa9T~aTNWFKDa(R#0z(@^j<>z!({KWNpStTRyK918a3|H<15pVyjC=G>HwHG!1BFkT<$dC&gz`!B!!^w%@^$Jej_x;?>VwCX<$3R?ses&hd1zZ9S4b?g-tBtOUata=(p1H-WRvQ{+!3PO9yhL0d@JoNC5usQ91jhyw7u;?c63>wC+;d%b;&tHE1`9FXEdcI{TOBy#BSkLtsYTxph&R71qW>MMc2Kt%HT;@KCqV|%%-+q)v-!Q3WTn7>G*ez&J;4Glr3j;r$#%fZ7J1Li4)$G{O5>t=$bgx|#!!-VHOt5ahwchG6#K~@IbjR~SxYVKL?yO${eAMSTJI$F+qO@v4il1%uLm$IlG9o4!gNo>D)T9|Szk%Vdt`K`rrDha%*4boIs=$c1{D?WS#?n@Sp~cH!e`S;+sa6m1yhVSz{rdIy11AQI4vGms{VLw3lhxoq6i#RL(9knM6R=R==U<>7QitobMVmdNVItQCjwK%tr#Bj!s!32~7yb+Ej*)>OFRvVbus@T;S*mS-45bFSpXUL+8;D~R>tiRhUb*%kug~c1ptVEr1n3+kPqmskSq^;e#|)>I&ii`G;215^k`G&G?XyHsKRviz<E<GM?T0zj9$QR>FJe%zb5t*tS_v?{vKBYgWgO<ke(&Oj1l$9nw^lD;@bNZ0@z|$E`)u(J>+JmTE<dZKoc?L=QLC5a;vYK98@^Q^mKop*0XcOsX<+8ebs5DBJ#Vh3@;lj&N<s|w&KL7$7QMW0Umi-ulg#;94TUdUJv)$ZeID^O0L(XFogI*8MqM!+@1vnGj05U#bq$wPf!XO1i9grs_@_`LC_tf^d<nyx!Y&TfjRNu&|AJ}V)it%^dDZDi;r*6V;7fgxYz2rbUB|$u278SQfH$_FbBkZ$pyg>x2ivGf_!3Gn(0#0FAcQp(<u^s=1jO7h!lrSWFY1;-^ua_QyLE4y=;vH2a!o=*#1vx)k0bQzR%Na6DDQwRUel?c6Nm4|*3;jNrlq-M%S)?smGWOHi3OHdN#*KWT%sZKp!egpy;`GKepHcSXJO_dw1Q~NVq^uOh&x?q-v>UHvXZyZhC88)Vk;O^DIGH=96QxuDDfIa(qXojc2iI}>cy@;)Cg2$uWZWmRMEp&2s{D|3ar*!+;#FnK-mZi9y=)lEn7ftvFaAD+cNm_YS=bP=AH`SQq5}+#J%3F^^@#Xngj^Hb#KMvJK!&u@i!PlZ}<J?qI!q@bqry6^}<+j%f$O`j<Huw>T!Dmb@ygO_tESN9xnIgIpDdmK|LIf=;9E{%i(cS5S&0X1W*emQEO|3DQ5LCzD*F;kONm$ZbLOW(eG*wZ>O2vm~tZZb!4fiN2^Y5arX|Ly6w2yTYb$va)<hwH2Z1EXcGh>kg(Xzl4@0xHi%OU>lkn@cT{>OxgtN8F})AaS3jXudoCI-NowP`*gGuN!y123N;8g%A4+9W&=F6X65!AC`pjj&C%Ems(ad)|fi0;>N7!bpm#<`)nvNT2$WlV#6Xdut>F5uaYokxM=^R?$sQ2XPQ<C_=KDG)@-b;d1kz#e-#S($lq}Suj-KRvO+><-iADrJ>ZpG;h5^2t4rZyHE!-PS6M<sddBf8*Fu_Q)v%EHXga5fz0$yM}4&;*n}QVenQqhMgW@2<wbQgHxJmFtm}wZeK`^XrwLxc!^^F~+5LkvL#uP%%9qiRPN&$1z2Zo0Tm8@NsFNHpk@HF%(H0l|*4^(qyYEj>{~rQ&mXKxe1vygJWz<>bjB{*e%UfFon>;&}}ZQ_Qgz9QDLkD8!mb58Tfw|iCa-agI5|6Tm~$s>yc~-*+=%KunA;bRrKgd#5NeN(0>O59Z0!l^i`6gdr`>d<O1NHGRVet%s0o^CQo3RRS}98GCU2W+Vbx)k6A@1^{9PGCw10*r~qo~6B>?mohM>p8q&CxqHS#K?=Ymz16`1iv{x(}@R(&7uiS)w1eUSQ36{zW@U-)*#Wy8q*H-}Vfd)s7e@qRr-D4>(K5%OJ*t-qIwO)289c4YKb3U7W;qfLZD*OGCEM>jL3M+Vc9xz96Mj{4OTR`V^g`_T2+;Jaljs&)6Ct@PGN6Z`v3HownP82dlbr4JS_CCx8H7J0n0zda=DRg-}Nk*aN?bjQ?^NB9+Jx9BP%Ao8e&{L}tEqSIaO(q*13!zN{&fO)|pj7vai7C>GN&L=LoCVmpPK9kUkprsDC(*c>E+hSfjMULJ8lSZFF^veTr}g}{7af(wMg~%+X`#vJ)G1dNylI#~%0-~)kZoYQEJ!=2Zp$mlyqk=14H&0_<MW}q)$UzVEUc+ZV^{FZR462%T^AfC3v&+FvEluJIChl{rDlG?Wa(bK_u`ny+Q#0ZE*^D+n-MNHaHo1-KjyO~`tO)4WqH0=mjmdJQQ?*3s_MefH1r9fJjLIP03V-vF3bAUkP<fFd`%Xhq`2JiXjj|qE4tFCTsxEb^YN2cZ@*!4Z$DZ{a57m?bX2IxG-xNwzm9ia3^IWqg2J)2jkO^Uh0kg18aofvF01=VNXwA=uz)8z6%tIY7Au9-o)oQA!M#>TjK(?IKFcu57(zlZt-8ff%P6=$IpWTtne2dA_wTi#SkpM=B}W+eKon}Zj7B?hHH~`$1mX!`$m@?TR$3vfSFMzSqPZ(eKoYm2SAYV8UwjWSW@m<bUQGYFsB#If$79^<8#tKk#jsrGagZVJVFed1K#TWtXTuuWBxyPfKwv?O*V@7pA6G4On)U{#G)^)CS})3RFj!E5JW&yYLF~|l&UIBEq>Z;^$RYy8IYG9*rV!j=2I_WGB^b)1pi>xHyubvQrFB=LpcQ*b`l03QyEx{U;s9qr2Cb^mX`1Kv)n_$9P;L@hXFf)}=6a6qF&PEPVSK}>@{;E|8Ac-<`dYEHdEM1C&0C^ETqjHhLk;AG8t|Lw{tv?3F+}m^-EQ-Y69~q*mEaj%CuaWu9MTg0%L-P0!3nL;Mmrz%r_7X_ol?ay^1h9VSdX07w83bZ<##yTMlwBPHZgY=FGT^@R;p`zT1FQ~VuB{5yI;^OUBxIe14$$Ye?tPjs8!LRMBS3oAYh%%Z5vwg$)v1Bs0j63nYt`ffH!N_#I!6nMdi7RHDWW`0T2NX91G<lL0i_wrs1eQO{%`~aEQ(k_XU+ZYJ07l6n)Q?%3wakiP!X)N@?)-`A9hAaea8~5I6Q?ovI=e`uZ$byH_0boc^6gzLDBF$MAa>mSi}En-$nwJP1IK6;m*=!81qijwH`QGn>6Zx%7`At2?}QS-2`>rHIK)V<0-PO=qt2a9yWNp8*JExjJVJx*$@ax5Q`r(L>}@8Gz%TZ4te4Pt0|(&zyScGJ+FpL8rjX^Frb;W6j_eQN7#+lWK*8(1=kk{Ox@BmFm{zX>cLF;L4&U_qtgZNaOH_o@kdu?!W%&4n9Zzwo=rYHri8}=&1Y=q^+XG0~Db}eRSdcEGDBvn-~Z8o3bY}0<<HKmbM<wX&dlsmhz9_j6zUx(EJceSVzcMLjiR#j65%kYIF_7qT4*7dkG#u2wB7!9oV)?<xlaZAoV;7;Xr$rYqK(Kvy*{5B^WTcG&@sm(VH5wV~OF(T-%lmtt7gc1g?N=9VA-gmDd#UHjaumW%$dBgOr1%-F*xoFvOEKnaoSfKnYKHp@xBdZM(p}WYnXPAqb{`tsXp;deFP-F&5-VlAV9>Mw!S?0F1GJ4_alH2oOcOLBvhUj>Q1oKD4+H8WnJ|cwkMuQSrGrfQsfUrmjk*j_6&;EwZYu4A$9XH=9H&iwJ+{BNIzMN&SXNd)K=iZ%&&`oa_?Fj<w}q|JX65B|)R7G`d9DBVn=^5}3f-@h{&*EBkYu1FKEr8;u(Gfx$}+VB`dEF}MU$;n{&kbOdq~$&4TD-6*hN8kAvsB0Oiq9V+L0B#Cp^+4`zN&WXT@R$n8$fUC7NcfGAIt(in>n}E54_|Py8hO25W`V>WziE8BG<tA3j4jG;#aGkrcEip0)_X&_p{%Aahi4ulpPw^sD7n|OTjm@(C6T(wYN214m%C<Cq8gxm}>pMKQfgXWDJfEWN;CN6=qr(e<>4~nFldjW9l7U%EwF*{9;st<ts%8RWdt9uz{59LX`Z^`B6?5tUbte%x#6&?d@y?9naL?(?rm9?w(Lq&9GR?Jzf8gAA8T2I6pb6gsQ@=8f@V<BP6ZfyvbP>g?;BmMSKw)lB11U_(zGko{;~Y!MA<saWOFIOmYKV}Y56J?=sD;-g5~m$tg=w-~12n|P!Ze&chQ!>@w)D4z6O>nX7&a>X4zh-phK>O<1Ws@TE%6!f@Yffe*Py-=swmW)dJvsFggpXC*zf4rXb;zH2^k354Zl%9z(RNz(LaGVw%bZjj0?`!7|D?}tTGRZ_b!`FV)5b3ZQ-ZvY=aMq3tw-FHi;^Rb>Zzz@kcVFBwgM#u=O=9LmeNfbxI~RCiobrdu)*lp7agyr*Y0R)sn`02j^jGk{AV$k;&G6Vpkp0v0!34hxsK%L^3pyQ8A#e<%n3C`=9yYVR802)Lin(z;V4QuVmyU*Q^H}94FG14Gi3Gqf-{=KY$@N5Bp2{r4|Qil>JmDYw2?I%&;q7N@~Oc8grTzHjf$MQCrBrr2#PZf97S3iqaQPdMww@m|z#un3K@>`6mQ0YrP9cUml(RMW!;8>nEi8=*OtX#P!+MS;DXzMyk^8L31H0Lt;`(fI)Cx(31|tQ|EDRz6xceO#LTQqV6R>3N)L{<C1A~h{B8~mAfgv6A5jfJ@TNcFs=y#rsNZ`bSf#1|Np{5$hf)0SK6wpb{fS_DM~f&c1~MwpwOpLNY=F`cvFV<rd>~L-vrL}XbQ2<1(Gy$<M~({<g8F2$Kz|BhP=lY;Udw${zY|{O)m5#^`y(UHQKBorhXKT8F4+RoRXh+pYdm55l4Gxn2Z5ne_I+2QPMNbDl!zAq~e~xB&=JHnx0dO|BN|*l|0%6|H2#nc#eMcV|3beA;)#18oDkUuA0q%(sk~@^hzCm57?5)g_0~<Gc#+@WZ~+LgFznytOd)W=0IE6*d|}Iq85?tCzI*@#iEJ)?WSq3?c8%RLtgLwf^e(>E9gQOx~FIJdw`>POzOcaWmH!ZbP8|}&!29rpdi7C@_?XuaxETFO^b8{&_daJaGjxgwX;oQ<$8VO=DVC&<X3&!E70XP&r*22K5;VzGS-S1XQE)7YqOUCDMNy&4p7ByR$UZb$2a1<xk~El`C^;Ogw9wfmFwnq^WKWIuqa!w2g4oYj(X`bq-b@Ut0yn!Z)*G2+oMo=gU|jkHWY`}o8<hd1Y59-E8VzI+W(UH$9^L|mH@T_1(g<c(KlrVv}Mf0HSFg<*}Yke{G?umX*+-zNZ_H%EBML2zTzX1dW!B3X0=#))GS)}C|s<Z_AmvxGOLi&e*+WC-)@U@X~)(7I&r0TysRQ^zam>5MgfjQ|Ckd{E#xo)2o~8mMjMKft{AE>F&bqdy2kB!>YFLUf29t*%H(5Sd;4HC65)g}0X-^FmMqln=T-K8ne0c#Wnqxf4V$xoXP#>GI?sypzj$w%>%jpcR%Ha@JQf>0;!WaIDS{l~PdLFjtJ%kj6bC4$qwX&7W1LGK2D-@KO+Shz<S3&BL4@vv!v{vhjA6dW%1QeIglz#`Xm>j4mOMtZN+A{AaVTjoDXFdju;8iBbXIeHh!@jti#%{WNQj*YrGBOlk(59~op)Pj&ketADK7{@N&~41+u6VrdOMJ(^v<N_7rfhI-6JsWArX(G+!qIYfq6`$qLeX>#(dipVPT4LLfR<Vj<-#(hL_RqFaKXzE33Z<`hK!AniDvb)oRB*Udb0yYk`0Zg$f%>16il$hudA)UTEXIFE{NiwbyveolvX})UwrFxFa-saS2^@)E<S@{`7+{&-$1U4o18;R%vfWF@r-6vD!xivup2~1f{h?m~GjqcD(K1@$C=&@%8CYE2Q1d)8P0qNp#`5$7)kRC`2l1`g0pnHl`OQ?3UI=61S^5oCDVB-e49<9q_J?H13lEtC)4qIa6t)tG$f(f_G<x7RD;0`0zew&J3jwMtj}CN~A>4m#1b&5STD|Jz-j$n2>q1^&YQz{3zy`iyYXM%gbSSi#_(H5FwxUyxXS=a}Xkz!bHJqM&FWC+h65*z2_@6(4~8W5PZM*O>Hyt0&E5PmQoS!W~pKc=np#}LV(YddxtPwGmC3DCqK9i9s<N65khSIH?(lOgm`=3$8TCSmqGFkquX*g|AWxIlEB-Hwx8-Yt1E4k^{!Q6V=ts28(O+t-&t@(*S;YMJ$-;9;?0{D{Vc2HMJ&E_OKS<i){A-v&>(Z#rCZ%o0#a9fDk0xb;{AoA-)wRxfzf2QJ)p2TcvvR<ew^BS0{4|X^<dA{;us2)ug@Dl_`Xl9S44uw$y6+kr+CcoNOAfzbJ^4}>%J{*q79a;1&d}C>35c3B9Q&XT5O&1`Wa9!j_pEzPP~p9sjhXiKuF+RyESU&zm&;;DM=s03V(RsOFW^df5F7~>O;Ms6FL;4@T1&?sgAfY)Fs_S%~DD@1@LqA;>$=O`YSEbZb#t)b^w6sanXwOEE0`)nyyAOa!s&v-pMiS{Y8*oHY&3)xsG^PEoT|J2G||&)Y2zVO&11dwZCGj^z&LdS%&^a2n`A_1&u`Y6G%}bGU3V?HkL2LV4`t}qn|=&Nu-S(9|a>wvh2<yV;KMIVY+bW(kxaJ@A`^ewnw<#@D@hiQpnQ9aHG-ywIsYI#>mr;dRR+N-TDr^u8_22WUCJc!1|CFX83I01J^CpTV8!S+0`-@7Rm+qNWD}{2HY}i{!6jz#6ZO%TRH<Hm2x?Z-j<T5Nm=n}5NA}{IXrE=5ts8YCDm=L%h>7?S9e|@5b8oFbSY6SG0icXCIh$@Nuox|hme#bkl8r;jWjqYPPt)lg5ihKBU(no&K*f|5_k&)nsvSje~85Ng|1wdO2ZWEn|g+9X|8I0EdKgHhj?}Ih{&8twzpu2Qd~|LRM-q#r^B3`<6E2U6UeUp!$Ra+(eoBKVWB+-kPi=SW@Zf{*YnRL(0sE@oevUH-()K043l#)ua=_7q?}w7)}hK&EQmw9BI3I*(_nj3(1(~%*`%nGr0I!`Fy;JOcyh)~b8gIxhq@S^V^!^b^qFyt&je*SH%&e3IniqC0}$%pL4k=Zmau#EF$<Z-vZK>!OJ%<gPOwCm<>S0rUu&_<f7K+ESF``l@vB@A00GpZEyN2vpdpm^X5M2LoN245WEBWATvsQNhq^wu(4+Bqn7U7&l{caiAc*i;0Z}W+Zxpnvy?~y7a*71ks-HX`O40dkfmPZpa!Hs{YU%DVda->iiu^30{~3J%P&`5~3vxa`yg`Bc(yRZSxPKXP*L6tFq#;g;k-P#>KK^9!P`-crn6g|0T%EX<NjdBc?td7-;9#zG5>8QaGO6M?na)|xsjiE2s1IIS%`&RLc>FN@D0DaI6Z1MHJpa$<eauy5n#@O1QV2~#=%XezvexzUID){tdH#Rj`XfL7*KSX2Y@CM>t$F7$nv}(hZ00EnaG!(ZUVS(M`QX(0R3JN7FtTs=stJ8?++H_j%_u*ncuf(HVW250hNwXOYOMCs<naCPlJ21yui<Eti3fD<oB4bqn`<&e4y0=r*?D{f-;F=dDP#tRF+RDT{_?lke*3(>@BjL+eiD|P-c|T=MYEqftv&Pf43{8z@nJk_<NMis5zrfsfBBYK{rosVfBOBG-+uc3X1;zvazwQ_FTeGVuV4Rldz_>FJh%?!_g@UQACla<h6mn3!)PA;EF+u0{rStUKmX_NUyp4PYWh6yrTg!E`~JWG{NomedV`+8cn))NcX+j*VbPlrO8sImga!ISh8K+W7}@9B_j=6hr&@fc0_pnYMHjR1P(J!YUpY6*Y%|tgE{DAuDYz$!d!I*#C=BJ9a3A#ks^a&11)hek^Q8sq@CJl1QQ-E%Su>tvRWH2GelVg3yBMCBa&cthZ{wjLyuP$`hBv?UBH$qwU1FE;emDw`xu>OG7d54_KDd=ry6t0N>KVObT6R}r-FWn`|GC}%Nn-dq=YHER9b^reDc}dUE^o2Ey*%{t%)URr$6g*s7pdnm1afwsBaS~+d^Anni;@5PZlU5}n(<ct?e^=}-@k|cu-&fuDHAt*{ssCWu%p?^CytLBqD*xT7v+3D5<`Nqj_m4d__5`ign?>mhl45~GuVg;XFtH$_VWOH%%n&p04JPwNU4eG`Eb+gVG-R%Y<*ms+%G$AtWc1#Wn(RVG(s`A8r<<Zy%Rp7oj#|J7f=;oE;C*eCaSW*-?ph4p6jkp1GF8G2_bG+?6?hWZ4xhhrjimysT1I!^p<{w!};d+6q5o>tENQzo$_@RBCfu~yqu^u_*^g<3dQg`!UJb^&6JH<cj59wQ;Xro;`B>y%VVld`XaRiO)(|ru>zYO@W*^UIj*aZR%@X_PT1rLHiPeVLm9}?blP6wC=MUf#;T5X{o|6JN#<reW;5k9IqFpvj9N2QXzye2q00Cne^<tV%qmStbOQqwE2{xaN+~0|^BAzS`}%NQmMg&v{646#O7lCqV(UX8z7B`tx!HsptG+vka9ery+Ivw<Q<9-gfi=0`m|$DO20MnY3D5{`Gz|WXgYV;(H7`w^16!9`f1r1)^@L>VjxqnS(ZOiY!siD3r1Xli-Vn#ohBi@fywXfoFS@=za?V4KB{bTCkw7S|dc)Kz?47PqWJc4Aw$SFk(l?|juKPLMgrOK?v{1*(wCM~#c9wR#Vzzi#dsph5k&f2G_BK{@%89t~jM-jAgV!Gf2ao;m>d=-7K3m>BMwJ%DWNysUM29Xyo=hZ7!S}~BhD0G4MfdgX5A+Istd$G&jw6RN$IKe}VXJpk2qY5{=Z@K$`8{Y-{PRO#OT`jp7>k}psq<*bsndRTQm22~>Hv5fi>AeEMPf|!X$2AlR7|;|=&Nn;yrw3l0PqPJ@?HwUia_X~R)N69pRs62tl3PCDgjvTv0y;ZbUT&}hXV1T;SDp^{$!(9<N>Lezno7k(J=7j2>Yn&2dOz!FsT<nQVUN_>ai4zc77PRka7}|I6>*QR<Rh1rb4%MwhobjXbIR-Swr&k>MObioxWKX11A7x>Z$~u=lbe?Qz*E%MLAe$KlaU*766F`HRdq=(dF~rTbhg{1Vh}LL8MxUY1E@E7#^Tp!sI1ClAa4{r4m?ZoO`j+cxYhR;6WE1PbLUF+T;bN>|MORdGx*#Py5_o^Oy@C8T<zhSyW)~*X;BP{VQA&YzYTHYKr^r=R=)+DI-x*R5By>VP>AYk6pO<J;hX!f~{e+4e43CP}7gU0xO<>^6sVe&57uuitj{!n)#-Jn3n{Db*uGLTVYZO@J!?u<J2&iJdt~c_Wc-nyM92dHQF!FOrT(u5xWlZ?&^P{4ka}RA;ka2Wp-USkX$a#;9PlQlJXU-w?^ZQI*em-=jt*wM!kyuFRB04s4xd*+N8-MZKpdfdEP5A7Q8lwltrTeo0gTifiV`P^OCWr)Tc>VAy7QbbScD&(e)}@6_P~nPVgte`6JRcFOMv!WA%0@w2Lob-jZ`?M#oGlRij++V?@Wa1{;G!&sc_+K?#`e9Ti_vaQ+P0)-kV*P@^cQeYJkI4D8U}!J!Ds6~jz&#b|jX)>TysC7u}NxXPHHAXf51u~S8>EA}i?9V1^d_@LjBMKqv4h<qA<%Br^GQ;)I7kVUkYwj1NR*=Qj+TUc6~(cMe0;YJ2HG>iyNOA5V^-T*f)*g6|9r2LP_dI}tr3=?U9WVSicGm_LXlch`k%_sn>e~Z*5`X~Y48#2<zLt90?i{~^jyJ3}(y4s}d2*)kAyI}ngw$-tYEF<NR19#lm8OtYR$Q#`rV@7W7_>E)Ky`o^HB;`NSEz7E09T0=YokgfYFQ$+rmECyivW(mgj7oGN!dB-Ip024#I;FF{-OyWf!{IY}m(iZ0is3|uh@!Js{Gw>WSjeh*H5ahF+IAFJ0HiJcN&5q@w=H$dLfc)o5UCA(C1X=rwwew9T_AWl;l9+1T;BabOkMA4s(EByM)IVe(5e^LAt}^jZbO6X306z4UeltZ=-B*HPKtLkPo0uj79uJ_ZRO!cMiw{`sl4p8NejauSyTp!a|C>H#aH9tAd=Gcjo{~~+%xrqTkb))Bxlcj#Q5+B0fdi%NrnPE1ZAel(GpapDu1jVYhi50+IqYl&K-=XpXG6cnR(kZs;x_b8<b&E`U)}SO;^3<a|(+;g&R@&01O<)YIu?P2xzg>xMs=&5R@=0>Y4<XBg9SP_P*GXx-^@bN`f?Z40=!Ghz$O#6KlBoGvygq@~Q($dH2~(om(2@ufqp?KL}qtNl==mK4G=e#FT^G#*x^;i}=`75Q-&bi8XriD-0)+Q5UN{{?YU+<)T*f_>_yqE*6^9r}doNWW%pCkpi(23{qkP^SBU8U(W0n7@G8)0)81IPFdC3DM3%h9SYT&Yop3yE`!TpKjyMF1EpRKg{2^m44y?ZUcDAexkp7@+%q#t0yIm;S%HvwfF+7dVb(G2Erl2}<gJ0^fH>fogHM6{U6Hm!ILys~(lXh$x0FJOuHrcqd?={bl(!ny{FHaAmN+$d7G%>!Q?G-&PCSf3RFp&`d2G!ExJPyM<02T*rA{A#p$(CjPIu0HwC@s45DTsma=n*uL2i!Etxr=y#I{?Xe3!D+ElKeYiA&YZ#WhkzoPoCUnXI|S=|GoTvU54`Ldr*!q&<aq>b0?Yntjj<Vhw|8fkW+P=s7q&#;r8vX;E!Gb%<&61*ud{jl#L4<!Mn3J}SlpSBS&-C7oelkd0ldj8Mlsp*%=~^8MqhY#Ak$Gb}rT?46K!1LO5Jj_<U{1|TFvXro#=xesr*fR&^&O5=|w;z(k0RdHQ?Liw4{98+3s4l``*X$=wTqbuKEI4!yCGUEAKA~tfLQ&T7IrFqO|drd!tsdZv307PtvLT~T!(h2nQA#?O1;BERiH$0&n&47#1<W#E3=G-@(rsYQVP9{w_gF{LBX9jWU@Rv)gAlUvK=AfQABB7J4Rmh02H%O6%b+jFyQQ|k`Sm2=T7JQ49L#}DnF^4HrN&|7G=i`p>HtF|_L5^eGv;FLG8JIIIWYla274A{F`aQXzgEEfZKFG?a;00UwYbNuK$ks7)05}J=v2l*!?!Iyy7?e3qrS!r^U3-C62L-OkY_j?%tL~JL!$i^;i`wCvLk32~=ea+jt*Na!Vg((KaKMaw*%%QDc}lKBkmrUN!jz!l1E;=eQ*}EfZ3=6p(RG{BYB~luJ8@#rk|L@J^j=b_xb}2@ETa^$L!OC<w8AP|2K8iD&8dPUOM=)B&d$CvP3&{KAeW<a`{roc(G|@FE8K8usG!`Fb)^lwU1GdLXN@oPC>QbHhH~fTcIyiFO9~T%u+5HncPWmJY^1GftEoTiE~|+V#p76VmjMsJzM~_F$&rRcc<uw_zObWAK6k#DxUN}gJ+KO6h#LgW*5|6A6~4Q<lZT$KQw$>4ME2ei#~z_ccTPr@qqvMebw6QrqSslo%Q=Ou(bELbE%+ieHOfSlP84Y7&fs#U1n}i(y|5+xDNaoLLJaP|ClLo=F!x<1KFi3^1(cLna-sT2_YR)>-X*ZPgQBq!y8S?qZ9*J#(L+JZju7lv)jE?0ywwn8tht$=-=%c9dtPKtf-v*4*ka^+av`qgEOqfNVY0=7cgAE($Rr-ao?q5P0+?%XE|QzzqX{FN`=x=q!wWuC9VJsa^)U0fUtjbg<T|85Ou9uO?W1K5o^PyFSABd~l$`r51D9eHgI`D>VoJGh<Pi8TxN<xft!S(noHf7kB}r_i7?bio!oe5H6?N-6T*+KP9|@JH_&6AP*SYk?9&VPK<HNvc27bc4$rRrqzw4H~84y$T);3pqX59rT2&0R+{$W<j9|q7(k_SS+h<7+8OoKr}P~ZDvZ$8zIj_H_z9+|^zlVZ$M>l~Wj%)^=<T27Cpxe=p2S7fwDt|N|_X{odMoRCrplKq=@`#t<6i`rZZ_8zhhQHgIJcAo@f(0Ajq9wk?r)u-Ac=H$~<Y5B_qygv5Vxj(tlSA*mNQsCBSve?xL(Cid+;%G(pd1kN5Tb}B4rnC!LxLitsofBIVmC2B;cT+SYisX~%Bp{?8V^_^v9$gsxBR+nrbJAE=_mLJo!fN^O5TOlfQCSVw{<=t$%+rv!4Iu?F9LqwILsagdq7q(%&ROe_4aBG(42?zbP{DEw3tBq#3nue;Q_?9DW+w9dk<F*XNY+j2MV+STW2I3%wI-BPI3vXtt?&y3KJB^Qdc>u#L?h68s+Xg)y=UCSca@j?Jbve{-O^Om0BspSR^_n{g~v5>&Z_shYPxByU8=sR3|I%T{eI4ipV``Uv?}auLCiF~#ouF|$E5z%s2wJ)Uzvj5G(#P;<MXrZKjvAAJTUC|7JC~T?(Ck_Aqn|sdEub0T&EE*kohFP+CbP-8O^*l7jG@!5@x|DO6m!x*?Hbv@j`X~XA~)TUq9id+0u=131ChcTEI&fyd^=JC>F8DHj3v^w06QdJpMKcTIwZu{#1fZKr6K0Z_|~c4~Y<Ou{Hk~-A=4vKiRU@D&V`#OTw?dE{Kt)Al>X{`e~Czx9Db|@JVtUeTqcN2+kV*8*k_P5|<6Z_XWdXk?cMyXs@`>pV5leVoa$wMBl%nxND04b}rZRznD&8IxOlAjh-bW>+FZ_3RKPsZt(X4q1Vbw>X?I#p^LtfG02WS(ej`#A~y9NQmrDE4}ljEue+^B9Cbt!gG`~w5qbqu{p|a|H$zMhW%PLDf}vo_%$u^`7vQ4oUm+ZN&~bR3Px=4qF6Z(K5<NZCSLlJg&56LtqI^+3L-vKMlYdd#nYX<Wl(-qGhG~jNLWnJpL5ib_eaKugXYlaUgXXaNzwlI<XvNp^P{o~d%wqCiO8{r*105=GY|iHC#hjW(J>Nq6oXMYPn}{MDg15&PA<HP-=`AjnNj$`lzttw9Q-u36oF#KvGkeSQ97pLSK6AeRWGXJLbHw^OLSW3kzY5j9;VUx_j*2$5?3nYN2U7X{K`b3LZqA^*do7gtC4~bHuVB7Q*C#RGAr6OxY#I!I1+pvNWd&0i)8_$j{FIO9HMkXU?n~x5DDz)60c5oCkI9U#DKw-)QNWw4t@(ld#9lW%s=hE}Xz7+#wQZ0G>P)uDpvq-AEZyp^MqF~a_IxMaWF5FFyo<e(&8}cXsfuG&06=0lH>l1Z5bvBPMBlf?ZIm8kIHNW~RJeNa8N?lv8hpup@{XA9P%<*BS%uHdO4j=8)uhMFn`DN0HS<;Qh5Ycl$6+0t)|{}m5Y{qE3=)~aDon&tJVwVz(JJJS(<-hMN+=Mo{^{rHcS~j{q>Q8Zbycr)Z<4f9?tOH*mgiN&spCN9C<q%c59aYw__2h@*WkUfoUDYP62+eK)eZfNxg#WI2c`RZmM>UJM(50U&TKH1{-1{9N@hI$N+ksL{BOA*Z!y+EC($tex2DMfHGM+Y=rNaxmPh2Xn##Ymu)zIg64NrwW@fG$46QDLiPd$;J@7hrX-MWpL-PBN^J(#&DV+@Q<L3A!z~`Leu4i+_AMyRid9d2gFft~_7nmrd6&cT~JsHceHMo@83{x(!Z?zi1LGP*omUU&N`bv<tcyS}!!yfxaS?8L}Ky{7nqFECQu8elZ!FOcg6+iVZa=?q#25_SObs)P4OrU6H@&Z=09C>4CooCxlRia0^n$Rw7O+iF`Gpw3;KeG-MT|nxXNa2LYy#$%8A}j*aw1Uk~xp0wJGp(<2a`Im_sAg5XnY!K<f;PuA)v*qu3V5%`;KPerLW32zMX=wha@>k|OsUB5q1efTJk76T$ervhri6h6)U{Oy?{4r6xsO&KR!0h2o)!6OH}AzY{r2x$^kVDU?$CL@N<)}h6%>-1!w!)@R7g1KCD-2Ot_y-FDv#psFT?>n{$%k`zJL3evRngP0<@;%-h1DVKMZsW!CdPi1`ki-NnuaMMGLmVZT;w&sB19w7mpu?A7w*NXvNU^e?ISHuBv3l^!Z4tn-YR~KxHFq@p=MlYLvh{|0|VsaQv^`p4iwJDke((&SNx%dHcH2;c)s``_65!0jX*I1?XRWtY9RS>m}GdcQ355xC7QWrg%*Wk71xGQit}ii>8JgV03%`yCiv-wHC%?ASvJho%?1!pUCENx5<HY<vO0nNATVF^NKI%zPC=Ur@#Ddw%<Ol?}xuWte@3Vzm9!rwF|TQ$Dfe5>ycE_Qom(5KR-^cpML-4x1av{^?!W*`mfv5PvIl&IH>yBw)1J?UBHvz5t-eGYNBZIT)J~EDw-<)@E0M3Py;`xd>+4~_=4zX83z6B&tHE1`9FXETA5APqk3$-`|o`F{=fhH;}*t+zUf0>w8Dbp;Q0K{C+bO|)gyhLZza0d&x;rc0LCdDw~iy>YJ@Mh#BzYQP`{`r$5bh)aRVdQ-t!VVJjT22m)-5#F4L>k$mLBz?dnMT`_~W5t-TMru%BYOYPmx!p`i`-8C^+<BEe9|om#+*3$N4wCu5)1GkUzEfBnzx_RpshHobO+BFrGFlVbdw6IwTl8RC6-yT@nwP;f<5VF8>}b$L(!P<2KQL+{dcY=_@ERHr>gU`#f<7u4YHYs%oz6s!0R?{pY#k=H8hO$x$TZ&=6n&xy@2Oz!?dy_lC^cZ$f>4r8Yn)og2Sfno7#CO_lB!d&gK5Oe6X%YqWtJkR_=+RJ$U2ad;LL&Q^zc9hYq*9sQwAgYukajtsUYV(h&MloK_A`nev2tAAqom@;lhjN1%_;6`>9LDukSD9KGhBXGr^Y3u97z#z3t48Mzva0921GJaaF4&@EDYE_YGG|1x^I;dx=2aOLf5z?CufKo)kYIt2X(kvFPaKNmh81$a{hsI~P7PIJA~HCYY28priGZk+J_O*{417`?VJMgV(uX(_%VN)yu&_}kRG&l{+t*l%&ydWW)i(1Lp21H)il0O6nQ{3Q-n~v5bBj-Dx%SRAyvo?ZbgQ);3PQt$`tIAh)N_Y+a_E62+{;p~7p4Zh=z<)!(Z2FQQ)ABd@D18T2tlgQ_x+q(LSlgLebX6{ma>mACFHDFd5iIJZF!&&j~kRBtUmsiS4rRjcVQ^x2EY@vMWR0PZX#SX0-pNQc8<JV0Fn7v3PV0_T*;G^Y6cq#co%$J)V+h`wt1p%8Q)>mtaD7?2R;^E{zMHgZ}sZKE26(MINa!>8V!5Vyk{sovr%S$Q?eVM!<}Ay5xy;`?VR(zccE}5?KHwIMNNqt)6wTk{FWA5vnmdRP#9CcJbFbPqmfM);EW**W#Cg@Zc#9Z&9?E)IgnP2tF&OsCF&Uq3Q%1DR2wT{rboCFH6nf=Ucv6EhX+`Ln2~J|IKm~>4{wQYs&2UV#W`cY_!|8m#DNO4yy_i;uzz^mE!{c7)mD1|qMnTRpth1$wR;S5=zIqv?r?I8OHu`v(kw1Lmh}_cGLGv*v(vCRGTX1gWjrS#a~z7^gaJltUz2tBeU4sLy)DZxMFXJ?ed6)%&3;OJz>aQfLmN^t{E;J>W9Agzeo&G*j;rmpTSKedM?rTC3~@7s*EMp?Vaw?wSrU+~C7thA<OtgB?qe;Qx9Ym_<Iw%!{VBIVrNnLE490mb-YMq*OwU~fVhTx*79{q(W~MD~LIpx=VQI<oPUFCv&xm%~TUs|HrbEC70AuQQjmLQBclf@V*Em5d+i&vEnT)w3gsIqrkSg>PPd@M2Z$%b09v3j=zmm5MKF{oV@!R*92_ju770c7ujO%%H%szibMIKO-Fl`!94R9;2?#~AK$fY>k{Yc5&z$J?_Q-(3?IrRNq4Zj-DHh&33A6OgaK7)m-ss6?3N~G8$>@|5~l(+OQ7zs)Sk+glFb#Y7R-;v4sZnGB^^l_P7flxA4=Dze1bs;&2%ees-<x~wy*SC<uN~O-KO->J&#{f4wFNh8`S{JD22kH$05y8FPxAWdyQd)Ba-wo7A9QD+wCPW<z&Iznzz5|q%J)Vm^*TNQu-j(5eWGsDd&Q%65^{9RQ6g#Sv8l9tFQ>#jxeOB@*(RW=`7J*6Yz&{4Obv_@L)&8%eq$WnqWDa9bZ@qZ_g3-?7MbDwA0e$-%zv22qH{ciHUHjSU?p6(31TMI#%2=>&{0!0k3YShW^EvW)J%&0bh=)lf72QWezZu;nruWj(l^ZoMZ&CbpzQfJ#{&G3n;JQk3S)5?&jMcYx92sQr;KXyABtoTO2`WG4QmA{>Ew~73s1I=wr$L3T7j#!gtlnK!72|`XAVV>p>@CJHzyV+A%DIHgDCD>Av9oMfaHZ<q#ep3B%50VwSS?0K;Rtp<4xM9~TU!esW_mGkCUDnR4P=$Uq-pc?X#qZUy(`|~@j@BdlzxIEOoHUKj%f@H`k3JPqbIxQ>pON3kne&Y7*prF(edIkz#(aJ@rHseJu#+&d{wVJym?$)@*x;bcAJs9c1%S1M1qb9?MXwQSz$DFg|Y&V96d9mKdPAIj2$k+uAk=*n?DbiUMd*FTbXeft#uIld>Qf9nc7SRU8Y{3iMEs)<KjVz5q2fi`vTkJG0y9z-Y7;}y<0#L=NhXt5OgJ`Px6QJ#^`sOq!<tZ)hKfpMcW!3`nENy=&H}-#5jqc=x8eB=X55!SKx!FXg%*c3^df>bE2Vzybj5vQjs|$Q&AOMaON36`RB;DmfIL?{0~Ey4(X{2Tw^L&R47pU>zqSNg>OlkjxZx7Gr&7Lb*HgwTpV2OujbO^!HBw#`WUiG(}gkj5Xz7u!$QN2U=(~UU8EecqK;=IKJE$gCYHSu@_W|HuBt5EhdT8MY3(Lb5T%L4-}0nl<7{XeS}g>bJ2X`wU>-mu%-F<4M$@53SR&VpDgoksq)DR3;AgjH)Fg)xSR^pkjOLfG=YwD0K*nV+hvjn*00)Fol5nu#oGj!fO>-x2%q4*6Y|)aekfrQz%p)X)G9_h`>ADjx!)lc=Q!po(!tfG>9phM0&A--fs&hqDB{f{;j@gU?3U1}HgVQ;mPkFBQkGbUfJD!UwJjZ3|s9$ogo6$7v{Wu;B@gg@~)=ueps+(zRTfDDT>5y7_lMGKAUB{%DuRbXZEvj*j=QOuWk+%}Khq3yoQZx-UPPtI;K9^;8_@9!&!FWPOURC7LW)bkH4uw`2_ZhC;D;^&Xp}$3ZneMM+;I`;9!!Hut)+m3fW6)J)rnOjHC2#9fu2^5BmgtVw$GHOvU0T;e79ao&AVM)`gKKr<;PU+a`JC9Axnd%u(G(e~+dSRr)%HJ+H?z5FI}&@WVH)bSmr#H|ck9;Kmx6LA{Q)g{)7B@;V?i5Ut<_sH!Yp4YlfM*S;!74tnmn9o8`6g^ywB$_c%gBCYACdQSPL2GV{)U-oQ;E&>&7BIkF?>Qbo3r$o$RrK!;0|pSs5Y;#cXqeJ{lZIjF`&`4TyWxVmWtK<hI4tA_lxkBgD&--SubYWV)uU9ev_eI<AR;)9iBfg4LBN0tdSi){Qb<7pPeQ40UfH00l^6J$9nIZUs{)hub@wkD6$g)s#oqayB}0_CANfM`4|hcgUK1Zu6V+m($*$X?mS3xdQ}ql~)<#17;r^``rn~7R`<ZvW@{Z%9VGeHwMysxjwj4U|=~-_VqDT>D>q0(t}e{0n_m0=JN$ZUaW2np8{D-hc=^V2{ih&S2q=d=cdKEMN{9TU^~mu3YhtriZ4wj_Z|a`P*4ze%GpPZylH)<jIgOqFkwWC&-a1OUFTaPsCu|jSAoA6(Tl)njcZjfViD1Tp68H*sNwfHfPE%fsGAFpHrc_Xc|WSK0B1;>YGq+9)kFm-yq&Wi8}&ZThB05h!8Z#(Mm|wIX>QgAcyd#JAHFn8J~{V=;(pLZ#Ux9>)*^(*yi{k6;HiSbFSr*02q0Y8V5R;(<USXL;x1K@oJSE8E36U<gPhxX&TW2KQ2<mEgw|--=+w+Wn){`pN*{?EsHnq1Qd9&u_c`!{1rpYp3Zp@k!#>(g>f^Yz`S{2~=Yr!+aIqJ==-6#bq{>O8u<|uHEX{COJ!h@e95<a=5|M_5$}z3g^+t|P2)i8|{t}bZtuEnX$h)t)YH%c`u=YSRDYN_%$#e9XLd^3m9GPw$<oLN@Zgc7{r!320)NRQRiyU&9K4#VXg2gCyAm|pj460ACx6?Qf6N51^;E=<wMjT#Ag#ldV0F%cu7?A|J@WBwlLG!4z;UYv{KoK|nES=k92$QODbKOFzSpxV+m05>NVH)xhouttb-@FXbsS;GDCoalrix5Q8)kPE5CkTRvipZNc3krv<lw;6Sj#$S0VnH1=ClY-OY4wlX*zCX!V9%H|iZa4;VcK&g9sn)X!e}u;7gh;P{OM#^-3LB*F2rPaol0t5-GFza-LM=6oO@qVQnPMfE^Mb@qrl-}p83(3I+!j2!u$pZ>59f210Iu9CDoSZcCt-Du$RmwpXa0`*IAf+JPlQnV_{!?Hgcn8C%23!h;Z=j9$uD=X6;mK187`m?YaSu$!xAzi*nS&)*>o{j;XP}y=ZKAh-SRVp4m)YRLvAacj$J@>P8*2$<%nz?OiX)^QRKJ1g7apzQD5#t~@W3U>2{AyM(3HsMUmznT>5mVNdL2_BLUn5uG(=opxS)<si#G&eVBm)T%zloN(K$5m$mkX!2RJ70?ip<BvH>iFmTMIX7X7EHqv>ZuRoRQ5*=)<y&up^Uc;tyeVQ8gi8(AkInyA#b!br;N>q38;}~%8G$dmPgO$wQ#l<8%Jm?lUBf;q+GaAZy?xSU6gDsfgOx9{lDa3bvPyOU(lk5&>&g3O9ER%(BFwXkjwMiQZ}Nwg0VoPZ(ZA|0*mGyB^J^9kPT#WmcIxYJwF^l?hh+?K3E4{%_Pa;5nQNh;u^xk@4vr_{)4U_5P-I>6MK%YA782JdVa)gh8n(`!4rZ^&<~eY^8UT@4P77G8TW^OswCrjL*@Ab%2-RS;Ln1N>>=HgW_9nqv(Di5Px1LPWd27r|eEuMSbYM`;m44z7ar3hj(8*fT?IHP|d|?@Zo>FN%*4^erZg0W&RF;T+AwL}Khb7I;<c4R7fGY=5r$Mzd)GB(fd?Ka_?W4Em%XkDIl@VV#<C&smixN3vnbh3z#SDDh6YU)S-dO&)84xYcxU6oWvOL;^2<%-`zrXIk@co!Y9;X}$zkU86U!M-Yq9^P;K8_!g)_$D0uJ(~^d2@Qdsu>NL#Ox|^yU8X8)?gi5g4f6P-XJ4K-9T{xnF%t(?MUyMee(BsKzPWbTgo>;7$JNvk1wilb1}-D_c^oIF*IpP!Gc940nWB5UPLnH-HsiIm+RxG@Tge9_sU;ohqu5k_ce0>(5sYJ0q_nwe==9BDPGK$J{?r7g8-P6!zOs&;9LCs*k7ecyyq*T@^xKHOV=cQf|E%hM+Si$p+pwxusZY!W@}EPprspJ4xhk4EN@Gv`NvbIMTEqq=<*_Voe)2!<OoWWFrg?WwToZhe9mlgEk2n&W}+#EG*lJiD^G@{%h7Rz!|u~&M~I8?mnD#?kDDKG6fE~+vP-KLGC++rpxv6Kn_KHKtJOUfFn6kw-*I;osltJUwy8R`13Jkzka|zpS{-mP4d+AN6X>VpJqEi7x`9$)S_=w^4T7$jzH4*H@Z?c&`0`=1DDejML-k{heOr>@sOO3t6}Dme10Q^$da{w2eCDfZ!d#>Y)fC3ev#-(Gx`mL+aHSEe)Rxh0?c+J^$$xW6T(wH(pLdqTz)*sbEU&CJ(dDeTEd88l1rs$BrGriT{%v5jiXYBfpy&X0nrK)W2dC(z_hmrx(tb>|SkSDU9V+!!<x>!wup-K$9?hlS{Jd8SA-Q&l@eX{7wc>1j>Gv1GZrKUNwo|ck>){Pu19FYTv9qTZY?E&bfR35;F9KGuml&T+kj-jqQNd}P7t1i1pw-j!m9#W+CwPFA_bnI}fi*Y&w*pwl_$Ep_lDV7|x_w*M&V?Mb4AlBu8fwHC+msW&9UKpU<t@NkbaMcq{iTp4pk$-UGN3M^3T(}k0%Qmky&@&KY8kc$Nl?4p&vAgb?l#S&qR7awyK<CL+E4}FU>*oF${{<W(mUnJTU_bav>t-w6e0);GDP0I7337~#cZZd14wvGX7H_$IJ-!#kVamC)%^dNa($sF);Rj4b{s^e%uzY*?ZfXQd5qt%eL&|3!JD9NWSP5haY;^^j&hSi2qQ}XVMfWk|4pHDZaVgu$dV9sB_1uTz^!%(_mc2WgVk1~NC-^FKC{Y?kRTStV%jp93~iqC4<wNsHNAjcK@lEy3`%1-X|tDFU4*P}#;Hq~h%)0DDx?atWHBj!Pk$kbGAKqVj8mBrUyAC@-XImuqj_W@Im0CU=;M~X!;<$NqGtA9nZ`z=Jrhw8<R~uX4j%nv+fRL12bBlDxlIoIQ7fU;jGLeT@39h-*(<P2iwbYqdCEwPPAw0dY)=5W&(t1j^|@nu>uarO`LA>ZMpB$kn#iQGQ=n=B6KBi3=|l6PBHcV&eXj0)T#;_z{eLE0^KiW3*N|@4WyJ|8Dw!8l$EBsMx?gvrgZKWElU;*6AIduVa8CS1xlERX2y~8%d3mvbJ^O5`ha#2>6%YtRFZ+-<$3a)~MH%%wef=`zuIp%*T5#jK`)fc&)($<C@83SAEY|?H`l#g;zVGAn4~J#eun<C&MT|*(Dan|}Eaz13!8z0iZ>=U6)n7b*7=DzkZ-Z70o&V?aKIW>DR8$*`x3~NmIEzOOYJ}=pjz6M#{vR9)di<{iJ&SK_;Sj?dT5m1S>T+1G)#Et`v8$wAu}rA`0>E&O6%3TOY-k!Ew-H17Qf^uc*3~f#G)2nt(tu+P9A9d&-~TR=ahUNMc4*+@0iFA1KA*_u>J^X!>Do(m9v{JX<IgL;p!?oBxt{*=x7mLCyuKg*`mlcPv>3+I*q0!g@R2ud2@5K)Wy|8XOy}pv$@SCkzx?*oU%&p3uV4Rllicv*pz3GaAG(!249t$t$m~AU>r?nE7(a$KxNacF=X?<&wspNHO1tqhkI(ylmQl^${`}?Fpa1jsug4Yv1FiSb{dc~7|KET9aSOw|!8R=H=UMIU<MThCC}rt9zEzL(dA=3+($9++2mqgHn_L|hqQ!+@ZrMf#48HqCJvj#bQ&k2gbaV8AvEi`}xW3FnW8Kd(TUw3OT(F(bz^Xc-{{HpjelH!PTqoN`Gj|BN`U7}l1?SSR40+`w<B|iJOYQGld{J$zVHq=i?f&J9hn0Hl0as~Q1P>V}>$hLO{{Ec_%LvarG8!8^ss^Rbpd;4x2idca-Q<dQ(l_J;GKf7W44J}HYAkxbYzZ77f`!9yr@fW)8WR2DW4G9PIG-ivlFNv?{j*wd_u=%zs|$7kQ+@BsE#1bd8z4r3mCZ(Y!;Lv#AV6KbKZ^qf8Hdi7ZQ)K9w=zA>i5*d?({s-izD=<G4eF9`%^-DdNP2CR!5xX|SWqFDX`AWDLr@gn%q>^T+Qxc3V$E?{8y%qQLY?p9>eH*-W4%bK0oxJ$@%p9E4i7}nvlL@xW<1XOyJ~q&?x0Qh?HV<EjfDz3U_$c?p^BuQszq<S2$sGr6adR62ys{qv(UaJIa!4Nu8j^2qZD5Mpaw#&VOb#~8VeOkU4qNwIPbt^ay1m}7si|$ED@k%Wb2DKS1WNgW77c3zVvqF`TtmmU$;1&f+fOq**ra(OmJNkVeb=L6>N!pK%b&li7C*i()Zah?GK-4dG4mwcg;iWEf`}yKNXxT`N~tCwEi)dSw+WntE$gsR|abzHx0I3qj^VN774;*M`Kp|iY_W*B=E8??YWJ%(WW2fI?@8JN+j}DpVu301p6z7Q`$>3W#o}Q|7KLvd0AfD2p1kNZf|z21l?cMX<QzZSWaI>Q2iPC>=|cPnhX%bx*F(xI<?%5b#Ve33nEK>1$h)vao0*^%;cTZ@dII3PW9Yo`9=3?@WkYST?@^hM|h!~r}hYx_hN63)}yLgcxA(4sy|G;C3Na~m!-kv{!l6|tZbwx>4)A)lvert6uNV^LqkI-CT3S}Wzm;gthOWH<3cyyRH@HFr_*@Y#Lq<V-yF{U%d?whxQ;fT<udy0BSm(rG!T0%u|28uIIA?Zh9Rp~dxyR%8qvWSu>s-}>%|A+fzu%UycEV5wvHP5IdQ966*5j5(iSH>b#6lfP*R~KsL4#DiXDV|#}Lwh4U1CS%5)Id)Fm(-8bjG>+!OKN2krJL^TrQl<wI#&^=m77%XmK>w+>2B6F?BltvZ-eC_bO3p;d^IsrJ(to$YdEXhkN{pr%f5{Fa0$FZFl~eimpQ^$|!qi!;sFqV~cN$n|{iYjZ;CNx!oT_7Q9&ZOU6ZftV<iHPsH~C?<nB6W<#!60<c-$`kR`n5|%jQY8wFdts~&3CV$0vBqx0sbG+@USI)l86J?_=kqRw@o{VDHar8<*$3-1tRLJ;b+2tKE9!V$1-bcD7?S(F!dNMi5qm%!?pu;MT8-uLFlQKezBQrxu3KeR;1GUa(#Fsth)O<=BgrJ{(=4fpz?AWv=9WR7s|GWp;)-+!W$riSLcRN3mfb-VV5SU-Kgd)z;pRg^iAbon4_i_1GhDk@dTarv9QUFnYQ6@<u-Z)*EQwCgN}~L!jzQPaRz*P9+>oowf!$Dki<J<9^>OZib!yTr1y;yR8zt65H*R*_K@HrJr*+L-F_C;bEzms)<yI_2cY0f7Ycs93DK{5Vf_~Lh%rDV_b?(-!vo8g*_xm5j`kuBXXBr@!p^St*T?ezEnpV{m-oqMa+J^L@8@QH4!3&K8lxLi;O*(>OdmC+fMI59A8bKBV%hC!x#yZ(!1&0-3kbyCHL|8CJ1;xaUd-YL69~W_fRY_v?0?S(3F_%T;jo^$`Ek5z|+YM(xTH_}ATRZy1WvDo1AE(*U^KmMAi17U#c+*yi1dg#ZoexQzf}!pW1=j#+tjAs_7XZX3(FV%l_Rj7mOlT%*9)>Fo8yz`&pTppzu+GOjq-b1j^P4Wt(>}N=$kB=-cYvVNlt-O=!0cmVO9sK%qS?_vmMU?RTzOZ$fgrt?>w_!xc*2}uBg_f?R(VP)U>cs>z7fJP<i%o(`jiuGBhPp`aiJXyeRWeY+FeKaQE2L$lnG}US^+a3Q<0*x{@%-~d;*4f_K1-;t>4VWjK3HiLogxl=B=HC-6#c{YRQ7S$_KU8Q$*sqGp<#^KH}cyU`;WrC;}180qiqzo8xY9ckpLfqk7y?g#{=x*?b=hYl*my5h%Q!vzF5FO>K7o6jPKm{&&ENoG6|&r+TwTERg&@d})^4J;#?f(ql9#Chd$kF)u}RhNl9h$|Lpi8UzrsDX>z1A9A0ILb-gm#S&qRU(3<maOykeHox4e2C518)zukk`R1A#NOQk5ROvz29HZxCl2sW2&V3F%VS$9Trow0t<**NGZ+#rMHa{JC=v=t15nSxWwgz_F;#Z|OODkW41rs&{ht+e|;wy140O!~E;v2`bR#%%)>L+KE(8G>4?SnB7yDti2a3rR%_CPZ!v;0!?;ZW&H6k<woZQS;De>!8P^~>&YPe_1xy5y!5>0?&CZ(oXH2ZC;a%b@xMdpnJOdodp{FmYx{GmR0Bq0P+)m^_wgUw5k0ID&&_Y1<Pa@&byu>1XNO9z&Q^m9{;GpRm&$Wn|XjQkVwY0;w_!1wIkdik8w_CILCfthNY2Bwd~AnLdLcc&LcHd9$E!$Vxc|J>`gHA+H?QLBWr!lJYzy9HXgjm=(Yx@jL5WnD$(W2MG(uJ<eXcoQXf346FOV=gx(gJpGT1OD9X#B0#Ht^mG5JVeeZD+bP(n_V7FA#E-`2*5ZDCpS|ya#vB74lT;<umgaV{O+m1i%q1&ZfhP0c>3kZKEBVA)bSMlJ_GuZ1eZ-(X25(Rh)y`%Np2rUX09pWOTu$h^0glORZV$aOhs&rv@wOn+uM8yxfyNz~@zP~_Wz|`&W@`8LCi&FkIh#z42O8g3OY;0FnHqR#Ze7ht6nLaI9I5Nrude=8-7X}1>PNK<$2PgYCw4M>n`UdbCmZ>A8<Q>X%K%>WVrZ|YzhjOu%O?KM2UH`j1c%V%vlo=ZzR)yekuu9<ZF6qI6qMB&(<1!0mi%xO2ZD3?)|=pbvvm?rMdKv&-f;cc{C`z!Cd2_={?f1ksR5l4xOVviu%2($4mwdn(3*^PH7xx=o5{TP_DPqK2Ez~xRuSW~jB7jVnDJjbH^%v2ymII{Opz>9L4<ksI_0e;jPJ+*6osO(X^E4YuJdc^$xh$0`F85-aJ36bLWgAxa0%H<!<<!;s)31m%n}))&8tuIj+jC<O#ONP^5)=3K{4=?Au~RKhOM)wgV`&xc@A8!20$d1(*oA&*4tqYExQ(+e7ghQ^{YNcJ0v0#)PbP=a3xq9+MU`=(s^slOMLzyfOKF`&6R%Q5OMRf6wt|9((NJno_t~H#~mXUe41@e<n|VPPi2YN7xKfwepu4nOm47|2)JG}#d1TfZEYlCs?a`qYrc#}@KG7@l{21Ewok$jG9lB%9AVf2Oq1npZ!CY@42YIzTvoRbFeuF<0*;a}@*<Y~7r@3fwWL``;ANr@H`8-QJv=^+ACqP(oVc#`k!*Q$dcUd}4Jl*ni|y(rn;ck!b?kLfAKQC_jNFa2qTvEEK?U)4q<76e`FlJdJmk?WCFC4AtX9k8OUh(z-sj9-$IzsyM+z2|1UTEKcoE5%cRO~#l#uID;Zd=I@0GvG4sU^7?rY`%pjRoc0^l8V{$#FLQ@ofheLARE2LUh+vQuG~PwyLii=Q9+s}za%d_`2gu4`%Onxs!~GAZQ9AdurZWmP(?4t;{T#L*~d=?0g>ComApZ^>!?@ziM%A#tf>(L+Nih#ymO1f@xsP!yBe#jkHZXQoV#SqBJ67G+ZmX{aj3SDp+@m!soGp0N*01R*ZMUzR|ognR4dHZEB1$7GjQEo6WiYe2g-OE<UHV^*tsDq!wZCBNhDC{l$33vJV`q#AURZ6NiYu(dkiVj9keyeH64$$R9^%L!mw3kr!1g07jq6Q!!g`BjzOr|`x1nZ+B_57m!3_H9Xqqn;~rRM>{;4}9>2>d8i8@|mxu33HJqR8tr;&%Q=$>lQ*P!<9y?Qd>s1wU6htC;!bQan&lBf8JRV149W$vb?g^M3=MTvh;JJ6-?AjlnyrS`?rDBDt<U`fuaN0X`*3i9Gs$;-j@N%OZzd=VnMTZcBs@_l}|xz!ip%1dNh}Q^YdOUgyh;!#XImR){3+BrQcr!yJaWTjT(twR&G7Kp=&^{kvMkt)S`A)4T$wJ^e+Ndu$LI0OpwiLYf-^zoEOV5n4s0u^OdwTawm9zl=m$d7J)T4{<i{H$M_~nJCeDa6uNy|*Up6;v<%dXRT^r<7~7N+z8xG7faNW~T6A*&q5Y+hC7@)Z$}*rXq6%!ylmcW36}=)QxoR1<21!u6-Oq7=xb8O1q@u{ku)A`UQrb`j-e4XGGs+=5qtZL&$y;3M*R&pj<P;(Z3Nl1yi527&@WpJVP6J4IOlI({kT|<Yt&m1ufz|x~nR0!hDAqXoq;?!c8lVhd!f}L77wjJ6H*6o!IYRIzs2f@4Zd_cFlcuBGq!7Z$5<tLkVGX-Rd=xt8relwZED2Fp;?cqi+-jF_FA4uNSZzg$gury{bgKLarA7AR9c-CQhBnXn2a-sRnqI)Jpa>5;2Bk5awAo9oE<)Bf<J2WgM49mn6;g#+vY3>=r@s(I85E-w#;MGRFGclcZ;%S-(LAz{oM94v^l{7HVaa<BQ8Rn5Ok<<bo{6Xkauk<x2akTT?Wa5gXAgXHn;iI~Rzj&6H$VU1V<jfDS74bI72dM*l#v*nS{^vro&a*6sXf%{bI0`7*ILo?U+D^rq&S^4kx6BzK-B~$&X#%8hvr2^x_P$xT;2V+BHh6I|4g{%;dsNZA>FRaiW5>)GB2o(OG{gIzwSl{@BJqyy9Rkaly&ssocN1!nJftr=o}aG@?rsd_SsYqMJyL8AP|OL_91bOgRbU_GU|8w`en#n*U>Ju;Kp_L*MN$w9eOC=zkN(ut^scKQOhZO-^b@44$G`zA%rN47?b)^k};22&Z*vmbEpsAT1_yjzj*vG{3u)B2CW!6|Ig=r%vB|+s5TgHZ}~HD7LOX#2-UM3e?;^AKR6Wh_+JZp7T?&yA%;1$-ddj3<*;6>$8!*3S4q2KnNa-&fZ-l17$|Sq&@?`7BZl;)+_V;~t78~wij?K00mm9RzSLsB|6L;EFyl4s(7?q5I`_?dK9SAUD<B8bwU_EVK7#MYpI3ZA_q}y;J^kfxv;FpYeLwy6Vf`e0BE75dWdn?U?zAY!(=%Lxq{c@8wKXlM1edLo-!iVBA1CNfzyI>vPv76n*AH3e>#N`T$Jej_x;@U(ejZ#$kozwN+Yc%57%VJNvAlLC_p^*_{`TiDzyAE6zkfZp2^eU-m+rsw?fd`!^N(8?>J7GOVLwmq4zKoe>C#(C1zD_2*uendf_|RWSdWo?zJ1CndVH&Xs>OFIyr?gQq_W=3;h}sqe7$mRl-Xvi?^zCeHBxZSYJMJ6bO_u>xi^T&zMFOO^wfr~^Be8!cm~8QQKa_5;WD0MRd2XXcQBeKd?`pM;_us`;HAE_SKe$gH53sJ@nR9%g7>shJj}NvQR|{6Kh`I;@@cYVu}vwTcTCIfEUcS}{`Eh%+doOrUMJaa+oi*j@GC?HgXo&&jmfu{hhCo9_viQ6%j4)m_Pk?X&JJj<H(?n3XqvhgL;d&NLdC%}_3kBZ`E}@j3ut^7K%`t1qUH452s1vGe!Knp_4n_23v36he#!(rpMQaV2<*JJlA+_{hA7RR!woi{kHqLQq7@c!z!~!E#`#_yK#ym~9>oG$jgFb>#v)n#34q%ogEG$yDExOk#kz6{-XJ|u9DVva->757$Gy~~<y5~-r`B=IU?cWS{eZotAB*rY6OgLblvCQwr{<=ow1{`Li-Z#PNfi^W8V}ILC)^@~nUXA&O{>t@ucyUWg~ErH7)Ao?v+KiZ7jGFBafq;^sSim)BkqsPUe$}A-%!}T#)l1k2*r)mq2BSttD@~?imPA)U=?LDXy0+=TyjqXwCx7*LpkPTr+(<*B`L=z{3M~*8Z;wP=c!jXoNsP_(PS00j`->sb>%Xy*v98u#3y(zvJPt}0%mZd)>QwP?;9>ZG_|-yQCv*PZFx+!Nq(pncq*pE%+Z*6aPcw4Rbsu>bG5F6+Y^(ZKly$*w1*;^PTMOST@!F_uT<Z@{&7jqBy%$!vzglb!D~KiF=|b1qrLUPhhFIsFTYV5xvbIwMK=vmZNR$dLD{HecOC;??0n7a{HR=liuXaqmYUzuwH`N=()(yAo|R6xvFf{n=p&YAue}$=G-a!Wscb0s8&gVb*kH%-b%zD2Sa`^XC%Pp0vTf(U)}_{8-C)psLNYDYIIZKsOuPWKZGeGbe^IjJEp70_HoPvb4`T&(9-`}8?vG#zjkYc;&`Ye|FtsLY)#OdiD4`t8qcr}n^bKiF{C*BM;bz8Ia3Hob?^OFfcs${y-9VQu9@c!CI%n8>IHvHnHj0#aM&lW?y;@LOe^5nf>?YUEQGylfi6S|f>Kr!@iLnp?wU2G!iiA&cNAH-|SQ7%`W4G7_DK#j|<lnRAVE5tl!>bE+0aJbN%I#IM9JdAG!V$WP5gwUhW|Yb&_h)hN;>RIDFQUR%b%iMBenY)4&pkIRS`QT(Rd5p-b#6$#rHayf)KkY%0o2T)fg646W}-p&Sv{|owM_=+h_J_^tx$n23<K~JAzyF9J=P0S0D$_yAFp2u%_fjui)A6oNXp0X_a7XUyk@^E7v4qvb1X}SwKNvL5UQqwr}n`&UIa_u77Bo66NEUFa&axz5So0{5VU4{jiz(rgUbej1}n7I7W+!Z&NWh~{_;4^JFuwY5>b8oh1EYuT>}DbjIpS1)|~}XpQces2@(U0pXImBdDL=Z?pRbn*`*ovAcG~s08!7NBoka0UAgy(6$P^TbygC?PZXEMV%X5A5@(e5nf){lFw1i{6}7VKB*x$>qBZU7Qwd-%+lt8ZT0iD8tLV4}PkeDRnueML{cAMu*o`8GaG<R&njxc$iU78L$3M5g9JkTdqsieWfp|fLAl2vfHYX@INhJvx>GN+&s$r|&vJoykUR;j!A=qiaN*)y=Ggj;}g6hx6$MIHVU?db{E_EI2YU<Oe<!-DCi*hWK4eBe%(+m=Kt+Yx^-Z>pV5Q^sh`as|?JRY`8f5;^y5A51`{5--7Gc~nGpx+aFbJWMLYNmWXm8XOqz{E9zr>=L~_PyE<Lrv)?WF!fIS4FL}^ZXRLbGAc+LNHe9s@}??FSpo!MZQPQRGun3vd=&Qv9YUR-(n?7A&BCLu)RFHS%&Lq^D#{_ByP`kE75(qM1GTQy+lewEKRLp$Vz+N(K8at<lv0hfD#51X9sR_)6hz9VoUPFHB^b|iB-rrX-Hd~?6h8v9Dz)>VLjAQ#SWlRrdFsyEm8*QI!DfSn<a<FP<9&kMEv(b<sZwu5e8XyD{TGRik3YtuzI6?*|I(YuA2B;FE(&b)6nWnNZSrsjLvpBNgFmXkp_EhdgHewM0xMOWAL*;>!`83A!!S>?NMd#`eGOYxt<SxZB9r%-VwWCAHg;<E4-x>h>1d3Q_$>MghMcA;(G%|Vz#M8c_O|Vv(3G4O`vfvjMZuFg;(Tfr+Ki&p#{7Z)0+sya3PO&MKtQm&z^zl?1Ob0)(>u_nv)s(Olq;YF3QcPd1@4o#@2z1*aPBlQ`o|kjVg}^!*9?9Q!~2GZk1VqL->8IN}0)05|Vrz$D>Eor&&@HfhprT%`JmESABCv#T6OR$=q+sg?jh7EW3j!z)Tquf51Ut0K$c;jEe@{A>vS*_&&q3AuuPp3^3(boHSAMH6R9Ay<{4oEwqv-f2w29b+l#j(KR>Z>T+N=l;2_{gkXJ~J7Arfj4bQMSZbCL8)O?dyOz{`{{D%{tZU|qiTu22fv%JYYk@pBAbWRAU~@_9+*t=USW|bmgcRnvTet2tbu+3${4!-~+M0TWK@0z*a2pglJ)wWIpqjQ>WE3h3XWEAJp$qTxISgKC91ui7Aw_i}0Y!amZ=+4Gh=Y{CG{$0JS>}<)SSNd|;IJYLGB5^@2n)tIC*&}K1Br=zFn@XNDGVc6P)j@JvgBnjsIL4MHhl+PwYzlOM1N~XpSUlP+oR2l8^G$?jQblu-a3)MF_xzDA<s)N)V-nL8X%4J*z4p1fcPZZKsns5TuV7TmC0#HqLV*z_CANfM`4|hcW4#0)aExEh^M_l0^~Ybat8=HO?lM02h2V;wqy{DEt(w-WT`bX$(4828wk>Sxjwjci|5n`Ho}}R^pvNh0;b`~&F2e-yjW~epK?-6hj#wyUPk(~S2q=--F1{7g{Hnq-)NSh6)^KLl@@7?$SE;t`v@53*&{~Yv@HrbAH-iKZ7TMCpmWzHRF6eH+^DO-UyS+<z-WzYRj`i`(Sn}mOp~2J1akoUOterpcZ0iwE1e!hjlOOOAbW4~eJrdc;yOm4@OI8xdWko+-3fKfe0v{QkrTy}=2UO?h#hm^hcC^NyT{e?xj~;%F==PSiFvKAKpRdMseT(%x#9jAxKe)~azD1Iu)!nOVu>)uFVBr#ka#`kHox4e2C518)iDuz*|@+NNOQk5ROyN6E{!@IBt=DlbHBbQAZq9{qGr6hQ~+|=2er38j$50bjy!Z8dKVXav8{pKw)j;k&eF=)V8MjVz+v^AwfIWh3&8m`zWBy5t<|-%l7_k&YwWP2jl7`88rywQ5Q8Hzg|!EoNtxxBnh%FcSE3M8x-H|jxBJr>Gp%2Ck9$G_#51ZkO;;YXk}P5L&Ou;7SODY`?CmuA?Zte+^<71iW*Q?LLz|lqFnKJ~zV1|~aRdj=qq4}25P1Pb-1M__ZjT{Ms>aRrVFGX=<qWFKI$R2q6vhB%kFlB^zIhp<QzfVba*$bV5rRm%IyJYfj9jX}ipZNc3krv<lw;6Sj#w7*%5fc(S!M;bleu7@(<7JahFJkD62G&~g=x=~c#y+u+~e%E%bEDo$*{T)eD2ysCY8K~ZAbS(5;+M2&b_bZq*=Ew7q(NdQJ_{j&kY8fPHS;LzX3wJqA|yS$0SurwWYb8Y*P^IC3DHjXP(SoN<Pi=<VrrV79G<@AZ-*MGN_Ni8x%yfvl)Zu@k0QB762NT6S{7IV=|lDL$3@dGHOq}Er|3h8}^5Tm~kNoCwgVoS*>Pj_x2|F)Z;muOpOQK-u03^e@dnX9-3QMGZF<JsSQW!I`*rpe^s{&$)5UAEyJ-*?(d16%-*Ki+U?0kKHkP;%lk5bSG^e8>*?>9W6TL%^BQp_ID{sjy`UWSg{C2klvyTgn{yMU$Sk5oGruK29L0g)T)y=tINxlY#8c5Y3B5O5KQ{kg6`KihfS12CY(Q#2X9T|NK2-_zPYJ3Z=tK!YYckq3?4zP>CiB|cCtXGw3_~zjMU2lfuI;Rn9f0&>&i~?-L(gG~WT6To%(IJ*B~WWO8eZ)b9PwIE7Qxh2qug|zUsF$Z`j*YNQ(uRxT}To-EMtI6$X=ST-#xDyn5f4fse|K*_%!c`DOAJMpZ70s4vrKQBggW1#wXCQb@p^Hdqp<Sf$P-(h{SSQz*^OIOEpsto3&jy`F009BUFRY4vEMFbs*q74i7><WTSf@F-hlbeBDTj^9KQ>1A}U=^b?1Oo1dkCPS%oc56SoB3rj!l7_s2fY;z*Fx8Qp!OT@mA9}f1zlICV|gN;PMl>@2MpxPN~Y4@hwKq5-NZ66Oo(qKKyBjJo^l<kx7)J@1VF-I770Mlf7+Z)RtHv^*O8JE>9RF+4Z5CKO?7#z2{|Dt9z=aw|<2)s=6+vorB_37{{dcw}*<M=UYroxHqY9Gm#H>dZjn$eI+%uaCTDQ}`p4y?gC_PVH#?Y%)p?#5ctZ~>X1f_OX9yJk;#Ee3>#CPzpr<c!WKxIDh3OxEUo&g^vzO`3Y7U{Ohcvu%nOk&Jn_V+Z0w{5UE+Dpv5l@>kj6EwIad%^U!xmocgW;2m`SWUg3KyqGP0I;dC&0Wc1-Q(>1+?;CuJpC9|H6p8nIrR`dewX}3i(kD2X6mnz`$nl)ADjimbKEYh#XcV+`gUjI)7>MP!<TU?y>a>WExKy&}p`jGSk108V(j-hMib?I_*EgRtn?&~k>i_}CqHKyG4OPYX%9CN~a&+9tGxlMLAjC!Z%M!?xaBscb#s$m$nC#N3g$z(*4QRJ!>E_mY%xZN{1<akQ<agX1MXGRMp>5igRD({k4W!-^wpIsROvCw*_XPSWd5_$AIRQ*-K_Rh0&^6O{qEyv5zpAqP6u$UAvv`C0q53h$zAedc)N@6S3fnOKfe*e=J=sW1KJ(QyVJ^~yY6@fK+1F@o-9kuZxYCGKYRl-h_VJwd<iEKju39DY&pS(EU?{;zmRHuA=yFzEmVQpOf{B`m(!r*E|2D8%#SiB#P;>x0O*AZxgH!a<`!XPTX+I`fENIrw4wZVV@+pW-SP^AWkLJ>Ee%`BvkX-wzcn3bkT5-0%^!tlox9o(vQ6tgI%B_btbPdQg635P-TGY;}0kK|&{zbqF_7dZh39?yjEh;#T^I{nW6SR7IzLJ(k?gS5z^1cPbBCzJh|5gC&7~e!`M>3a_Lbq@0+PRQ}mVtV)N<)npW1Diqw}ayWu)GCWi*61ew7(Rx1e9!4Sq9WaRDrFTQh*GhqF1COS1rTVAPH)>`#BB}*WIR>R1_H*c2|y4N*k)c8_WY?Mmc0>RC=d8d5bIkn$|;*oI(UaL59dIv4WfezL?F_X#fe2$qc>~5@#2w71GEnu$uorQ?4%*#TrMS)Q*El1C#+wIF8Wig56{MhV277M+n{obtB8%jf+ci(sY!Y6hatT0tgr`tYO!Pk3#3%bnG#aB_ZlcJX%<RTkR6=CE=e2tF1_p5SWggPL&^_w8(zEgDsQE(B?V+KoZGO(+k)Y6yagVpfrY)HhZbnMacSQoVtXGC^Md+LaH!J7L)S#^cSKigJP7zIF%XkrKsNQ4N~DennxCrGfcvdK5p4NEP3xCYG&`1X>2swGZ7U*j^a}8;L%UE{gh|m?167?lLLR$N+>ns=I8%=ti)vY3M|v2!drHpG7_Ux%L6Cd6F}}WwTD`L?wH>CS}R)qD_wz+6sMCWGO6qosG7jU*)nhX(7dQfH_uj|tGgdpq#Jnup9$AI9B=qFq}z2_aYBkp<^|PpX=$tO*WKvgz5nE7*C5Y_vW`BS6Ms=IlO-Vno#SF&UMyhGKAY;Hh~+{B1j5kEJ|xa@(A9iVM*U7-zYMwSI@+Zc+_>)k8c>n7Ll5Qqw~r~yHNdStYB`1P`}q9BVVN~7gb-yBV^UvAGUhSMIn{e`4)wuXs|iN+7mpu?A7$&?pcO;s|M|R+xvC@;)du73Eq?~i;!%Sdp?a3%k7%C%2Zw?l|7$_d;u~8y#4v}}Tg$V$9M)^~cn(7BDrr|N6RN)eFx+DW1LZ9nn#RX%#E`y}o7RGLbqoVdk+Qrr;8+94ms;%ize{8sX1s<S8n}2s=f0WGC$hPE1>``w_EMe4NATVF^NKI%zPC=Ur@#Ddw%<Ol@8`chte=EWq<0m*Y=F@(+iU)>@2Jt<N3u5vKEAs`{4}1SAZ^t<)wCF<EJ?D?Ks9zK*jN82Z!3CUQ}^PE{!u2v!_>Q4l$I>D{<ol7eYy94`u&&Re)@hl{?G09PuW>9R+AdsNpTV{{|crwT&ml<MaO!&S8!mE^3iXZAn72Hb>LxYQOo0B0WpNSuD}vaf}&QBx<4QFoUvTzt;sFeQMx#K413Awd}c_r+F%wGMn(U}P(XFWqgyzr@E&+jyY*ZHz=*f}h<Pr}0#%VU$ID=UWt1X}RuA!EEOGnw>+c6L1lUd#1$z2byiF&o>u#up%!{GHjwmnz3-@{c1^OYd`4mv1sPWAGgNKP+8#o(zJe=OB15}fUbrrs-Uto8PWLgVF`}-d}N%_MpDLjvNaE~@Hto1w(+CR!<QbJ$iwzdCweMZL&trmbMU`UA@l!nTv0xSnU_hW{-IYt&Rf@Ab=fBy38&;R+BYyA69VmBb>2_9gmTZwmPSfm@~IpG;!&xSAMkBlL!tjec__RA#>g{FpivERP9Cmm%4X1NhIB3ZBbn2n*~TfatFTD{sfHOfxuV@eCL5A#MWrTPK;VL$fDV{-Mp0Zo=RAgW1vu31mTH?lEz0nWiLuVU&|+XPyO!s{}abNw(?>qs%d!YiPjAY(@gKV4#c2`t>I$HrcsB}X$9)&ce8YVJNO1F>U7P?+j35CSbUl8UIOa1H>#aeWdR&@ZUx)laAXBIt`53KszI4#?k2eUYPA6R7(bxQItg`{pcISE%{3iaiL)DH&bCa`6}EHv6`qehv}5-soU@TH#lE&oOx)-=)R5I=MDfU|d4F=&A{hCLpsg6vYSIoEP2vb;ceCtgm!Yq$c`!ultKG#GtpzmzObHN5Zohy}Gp%=<K632YY|Zo|}sK{`5D6|C4fiZC;(L^cB&Ih$`-dS3YBO*9Y~w+qyCs?6MlBRL_L+FsS%iaoDoq_Ug-$XmHUemQ;q(7z<*C?klFk@SwDJ^%1=Opt{-EO|CVQiZSG~M!n(GN|&sku~77~1<rxR0p2jV6#K(+l?l~A$8NE!Om$|$v|O`JANS$(!>bE+0aJbN$}RMD>L!Pn<Eu=RL$>Fbj+@Fh=KHfaNN(fM`J&w1r}$QqpK?<6)X3`GbHk!9A*edd72*AO&Fn_(4~S|k8r^E{Ig?xFuAQ10JZRYPd9|!<J?+O8GZuwM6@9X1GBXNDHP5=odQsj2z3kwR*Dr<Y_n_u$%MXm@eaG<kcXevWc%{WlPcFQRl-F3|X0^@*zYr=0;S(JB#*1L-+d=`bZ0vFX5_BMq>y+KQHu~?5O9MS9CYX$-Nfa-aQq|eZ<2diYWpWjA?H9&;c`b?eV`Mg&<IS=N853SeW1+X>z;F2iuwj>Gf<nW}$)4JHCb%wIZ0-{)+yLv>S?L8n)qWPM21TPv-$h-)9blH{ZdwOYz#4<Ah=Oj{r-G9u-&ephPCe!#Vd7ed&{ry<X=oi0l4+dJ-ti7YWoaOkDmoitqEcuRn{<kg&xdWao6B>0V_yW_nz)-DBbyV*da^B4M*94ll5o*#o@j&%j~AB%s70|BkP#97nekPX5mbLhK8{fmleJ;o2rwN$QE)fbg<dcgZHo03<Ou+XyH@%hCGVV$9|%RKUVR`Sx+u7OQc7eW<Pwqxc5Nei9^regS_MIO_U0%Zyy|qSOtwvJ--!$UO<nKy;4w27l!^<Za%nmBp?4B(nty%@-8tK#LGBOBZd7k&(U)7Sr7qv&LO0%2d5e4o5{RZ$4V$=CdpvEbsPgjcW*M%d&Bwa4kWww%t)z+j68TL<W3Kk`nN^xv!;qDbsv}MyWJbXmv4OT$rnCxp*wfHjRb@-^!)@${g~+OqaT-$XC7xmr41+{kqH8kKsA31<%{+u;e+mSJax3uXo>6jLAQ>7%*=gJp@!tp4aw_x257i$;nVI!#D;g8IS{m<Ta*c0s5X+62nGX~`pQoYKW{9@ou^650a*{S|Vj>M*nO-+=A|c8f`5c3v1zJa4Vhw#dC{&9od)F7k5Xkj>@N08I>KS{o3-%FgBj=%8I)Rudlr;ryTSYhob0)qwU?gTMRC8ueK4#MmSWy`cmf;~*hipOs%dt^QZYuh$n9`$ww^E%bXhqzGjz4Y<T5@M#I{RQ<u1l6GDaLXLS~;eRa`UNZp7NC-u@4X<_MjeMb@|q;dJ+be$3ts#wk@}qiYUC-_5=>$_q8hSKDP(Zbmr3IG#1<!^=X#WL}1EzPIJqk&K1YksJJ3m8JYV{xlr#umt}Vl1(+#A;tx0oGG6T@l!$D|`cP=_KEsmJoKsMgiU3XvR~CFd2Hv~HXqH4LXeCkpRL7v}Xlvf0Yi`KZ<-l$zzr{)j!TLCNz&bU#Qq?4Ws(c;0T^cvL*2jGQ{)x$~YvziH%sEXxq?(23PH&4$%cpg7-Q>AUe$ClYRxRag)1;PZ>s}LaqLP9yQ>Lb^$#)#|?mh~)L7~%A?KKOkY0o4^p|WtMZAc%wfhTnoywErxh=PREF%Br|V|yEIdPN+h1PbsL1Iu!PI>tKLV+Ds5VUU3_ctlt*Mg_$Lwyf}|@f11gFI19Py}+`TcFbiFc_TPuRg-Ew{dPNXkk+_~{??8@agzbJHH@h+gVnVq<THX@2@7EvIv+By0z=&!3a$atSdYC<E&zy6q79V8?aG3T!&8}@h9o-qBWLe(7<?4g`FMxcl1XiTvx9Eh2iM~+T2bT<5OkXIsB;gPeQa#WAQ)RTI~vGRpGA@@@2WQtr1x@taP2tHb_r~RIpNMFPe}z#!;{;$xjlxwSZq<Ba#Bo(cK+#JM*6f@Hx;AZb(9~4roKrNNS2`$F!M1LX({IKy{v~5V3=o*7<tqB&0Hb#S<o>A6Y~2&=T5?Il!8s2!a!XG{$kW`07h$EtAc&R#WKN~f;31Czs~{eGtolb+zsvy{w!-$k2|Wc0Ns6??_*&t5!W#Sg|~Co(ipU<?M_HU<=gwfikv8(H0L#YYWutQ;Y+jR?m@)IblWj1Chd$kF)u}R7AhQ|@Qb`DYY?FN%Ba-ehur6)P;Sm>u|yc-m*>VVNW7kNn_q5K1Jwll>gtTNd~?kVq`6-js`Ny8jz%30lA<EOxnExtJ2GVDP%~a#DgZg`gW6jk$F0pzM;<y4y^D*z*w(;qTl}gNXKCeYuwcSw;4oWAo8})3ToY`b*fMDzR@Zq(y5nVhF2jyC?Q%R1yDti2a3rR%_CPZ!v;0!?;ZW&H6k<y2MBMgve>!8P^~>&YPe_1xu9K!k#$#5JC5+xVGX!8#!k&06+D@b2Ud#tv-&HherZK`Xw7K~JGtCpCsbo5hBRFW5rtA?SFQAB<ewNPdF@#A~Y04h&#@Of=|D!Z>kCuY=&8gokaRFA|-kjbt3CKZawM7Ub>FP)r2k06{Lq+7xn+1hKR?0ExDMu^|dF8kc3VvLbl;?tdPLEuw8)gNtNc_$^7p6T|;sMYS>2dbj<xKqPWLVt?K6fs}<mrE8)X`b876DrIqc7O(RLx1VZeK2Jr(mP<^f&{Jxxs<YX)W&OH$X^NH0Buan4~JHwluesZEA9Yh`4N@rm<xHQu1k@Cs*=`wdhb7D(urT4*Q5feGJ~9AgZ0s7(9<30syoC(72q?bpsre+1ws_rJJ8od*W?Dq+gk-lmi1-G~+@JPV~yEvs%s6?(I$TsmF6RnHmqez3U};{*+7&JT$kiW+VzcQX7ucb?jGH|Eg{ml0EgKT83kr+}{&BnY~T3wcC@8e7ubo6UqFGp}n5|jyc9GoA^H;P>r|}972=NUQiDELer2%$}E$$&AACvP*!J5i}2rC^21Ra2+rkOZ-Vp9)=4}Sjg!!O!}VkH|6Q?oKpf!ZFAW=z8qgVmFS}1wLj6;MDhN7JLeQFwb`ATeXq(Br_V!7akp{yM3|0~2vy5vyt7Hct{h0H=c;(P@*t5lasvyEVyXaT~wRWT7)lR_?uLWfhOkFj~P1pG~^<<}S*?c?ob-3DvB%#AH2DpUmrHLK8)2e}qdJK{}IG%`4^NyH8HB9|^|MKSGNI@|&fQn~)0u5VdPY1JCWb+)jUJZaqET;vm)vdR~99niQIQe!5JR?+t(GH2o1a%<bI}Q&*KV+kOA2CVituZh0`GcWrX9ObTq%Y>p&r(1qYe~0<<a_dkr5|^USnz4KIg#62@I93!VqeG)2m4`3b2GWYMk3(Kfz)YG?F_Yw-YcJosY3hct@$z@!AE7pSI&4w**?Luvq`3jIl@>jxF}iP_QvwZ&46fm#$|O2mF3YUM8HuJ2FI=Lzo;3_xh2gy0xuK&_W6H&eLDP#p0M-yIDSl;sc_=D+DEeG&FTHBW;A3HvlE<o%A07D18cC3y)NowdvB1DyRlX@TtFtMU}UsR?wWn__jo{f$fH|I$T_kiua?J`l*!t>&zZfBp-EGZ6f7zUaJEhHB9bxhcI<#DA=jhAqhcv5b0eM;*yX-v4gh+U@+tt{LFZ5AiZ#WH+0v(jiggeG;~+Z~cKP(a!MFJNvA;@@c+Xcv<?FhZmaa+q1SgY1jtl}ho>Nw(!|Ko{m`fauf|hP@IeY>GvHX^t<{wX;77-GcN)|mdl!Ev%B}Y)2gb774sa^c~=5uC~=ssW_ARt+kO);dQsu*8+GAvz=jvIN#J}eQ0xCnn)0+|x-t(V)lV7VWYU0St}0cxxP?f=i*x9v!h9J&5bKg7-B@;ECMqya|Lf<{6;oQM7Yzc@Wz5m_1TG?M073kX<1wKdsU?h$@5qtVFTEZy8%k6CT*serjtjr@+gqevAFEVSLW#wMVXYy)Zcgss&97t?e-<RgK8O5P)PUQPhhT2M%A5OmFqgD6#X&abKLK7}v7&n(`ceyD!VaqLSn9Q9n0qrx^!f8diZR8KY%lh1rLO(<2G&`e>@Jo^@{ZCePb3|AVlN^Ke4);?d;Ui>$g#8sPQ{&{Cf3=Ab0$@0q95?!u}%Q}`sE10O6C>?Ct_iqEMP5f}(0#ygF(?rA4I5<Twy{`k3m-b_##e!z->`-a9DxZSbgbh&^^=Pi+?&rN)2+6gdig(~stQBYL>v+5fcFRtvH)<q$Te<D<rlAA5M&j7nQ;XVJbs*O3G`<K}!Cqo~GC?-0twjZ=aa}CaWP(;t&sWmY$erK;Qr@p%SOnJG{ND;-o#R_5?MUWwQt0-}x^`~lpmm~NtkO^;#@Lpe@a^Py0IXjEtVK5m5ZYfWSprHnYAgfVBC5dFOesKyP|+(=lB?Ef?~nww+x;8|i2H8SOe%_uOouB+DWwfn;0@-1Fryr@Gb_DQp1j4CeogBkNKPe!pddqJme@c}0bk5!>U4mF=VT_|3W>9e)C%e36<E#xpDEWjiek;PPin_OqyfqRCLBlTbiwX1e#7<wog)Nqg1V7)?#9I>IcYk|O)4RbECB=z7uK*_#7CiXZaVgu$eIv!B_1uTz^!%(_mc2WgUwc?NC-^FPN&L`P+DX^-oc*9WN7o8e;|qEsOtqB3X1TsV^A8yNt?aY+9G6oGcH5IM3foNP$5;AC5uV<d-@wultD2{Wt_^4_)=7F_6DhN9?c^w$r&c$M<2KB9hSWJ5H+*+$})Ev?U{&*AV+a2ckt*J+kVP3aQ47Ax5<G&Y9*AKar5*4d#uD{_6n@as=`}#o-z`nQ_BM<+Y><UGqtByeeRsz_F5}i{wH05krbzkCbFpP6sVfO#Mv@$de^+DNH@<`pKH4xH>4Z*@qZ><^KiW3*N|@4WyJ|8Dw!8l$EBscxnB>XgZJZ;i(P}f9?CZRa8CR~y-e1G2y~8%d3&*dJ^O5`ha#366%YtRug8=)$3a)~O&Rqkef>7%VHjwaT5#jK`)fi))&V_~pT9n*EY|?H`e@}8e(vMz4~J#eun<C&MT|*(tI3$>EK92Q;2P?Kx7HGj+8-VthF@jt+n^Og=l}V<&$+5371ajg?JYk8XYr^(%}_nd@kcbz|C2*OkN>TrXYq|K9AcP5>s!yWx*gVA^LS1|>?UbfEE8&f05IHR1q0<R8=A()ZN!kim7BJTb#)E{O_8#^G~n0*$G2MS&%aA#9132;4h>v9pljch>xt~HUI96f?!8pk@e%ws{=Vu5y6>%%>*+85nC*}68^`s}FB{9C#W0@6z6QyJkGyG1SWtnjTNZz0I)8nfT)+JO>py<^^Pm6i`}aTIBscs#sK#RZL-(?Wf!XmDnSBiP{uKTU#?PTmt{cetJ>P_gZCme&(r*0B<MVzjGOGEX|NQ#fU;p<n-_I=q2HNhUkAL&y_y7LSzuv+yZ?X*w$5PbpKEMC-iBgu%<5%rSpXb|vFJoE7Kmhnm+vM7?5G^kJa_crSVDLSz>d7(apQ<u2p_{W8j17-<z>Rel8tZ=6+0tgD=7Q~f1y;=o^_TDOANSHZ%5AZ2G;@cLt3QA@R&Xv&6+O|yNnEspb>g&bW9{00JmWw9{`U4y$+H-*DebO5i5Nfc^J=w<8YIcxuJKtsRdhv#Lx*K9$Oi~N)SPkCG`i&6Hl9~Sug4WZ^+>>&?2bLa4f<G9292{?#b5AFC)J$yMC`4j(4-o;^@eq*{hVh^)8g(gBnNhjJ(s9qvMQL+(DEErv8&5qSe!k@k8H3o{Yp2WO4wRhHZSK~m&5g_cHfAS!5vfyBzXkJqn&5B%ECn!f*nL<@+Iul4qI*hIVHd#nA$O75=nGSbB8*Dww4G6$gqH$8qzdxeH;r=T7^(z4I9hz?__OGWg~7s2gr(^^9ESaySoK-svWh&9$gK%I&G#^G)v*{c>C@9??1of8?n^vVNKse$)_qgVRaR7zf;O!K=pNX1t>%@8YFX`mQ9s1Gl)9rLm)=7Mx(yV85G24BMZGw!mY#4-mpw`%>&{yBy(r=%^Z7&KYi5IMZf(ME;2^MZmMtTx%RF#yvf)Cm3<RjfL75DG|gdh^|TME=ic6N!2`=M7-9jeP;EV<8V(vQrb?BQUHL$$gqUzzg8gZ!ccJxk(@UQAgm@R<`~1JgtSPX}60QNP+640S_oNpb!P6!s&8Uz6?aM5)?^J?$SX}3hV8ek!M(9FNTRZcS&O_<bzXb}|xCZBFTk)obgjn1>thN~L=bchFG9szJtPuRiaK`D?1-pW&e(lPwt;QR0B&L8VkIfK{oYOHIj=;~1d!7bgvz6OezQqWiqjXGtPOd#ynKnc18z@T31%uVOA$x0^^6gobp6AVWY&Y$A359|yxyjYC^|d^nk;lB`EYex8fs6-5gMLp?do8i5qRs$YRI{~28BuSZ75K@5$Xt%EBJyhQ_71Bhx$tgEFLPzV2HK$ch0qX8o~WW<coD2)UnpRgPbh)8GQJ`Bd4yMPo%W2gbX}u(zwK6Dd5FX+#Zr{;_BgIPa9vyh#eBWXQ-}=upytZNDo=9h?V8PaG(yfdy&ZY+f3BRb*rgfq&A}33c!?)Qn+dKf2KL9qHpN+L<fNYP<JH27X;kT(?2-^IY9P3FQw8-kAUL-r$1&#fQ^CoSFFWn|>Ya0u_;j1V`;F|%UH$z{Gi~nCykjkc+~9zYo*=$P7Zq_4Od1Kt=fghRy@xqDnr{NJR1VtnUJ|H&vTI0_ROm0Gn$pYOT1L3=cyT#`3%rC7C5>|KGPZj%f*P;L$MMl%st1-^eM_ZyI<?%5b*s3|RToQp1$q6U;;xmp7|A<l;0Hq0$k84M9Ph=$mgx_<gyezUy3AcicqN=~lfXnr@jL4QXtA5n@zs=mTzHvc8Ai87!z(v1)RcZhru_uylD0jS&re~vW;=DLLE*0K=B=#ya*L&Q<$GM|##<Wc`OiQCaI@QC6Lyhkesdb`U!Gl&;X2xUtp6Md8M56f-NPSC>`2-?6qTm7Fl3{%=k%@$6*_Q6?0}8PC?&u-V3}lDPGO9pZj>RO8|&0GA>*PUZE>>G5-n1HHpvq0P-hi82<y%%>;a}gP}q$RKlhB1>jKHt8Okp6k%<4^snkcEH@+($UrG~eUt1+C!^L#CZ*YR93W8XRz6NbV@cFz<y)G2YvX92-Y?muHYci1zD>ZuK_asDlpNDhsMWA&Kb=cMaVQnT=?S&zb+x6hL?u69yePb8wBiKg96mRJSVxdshQU(aiRpAiKnQV%3wu=;;h_A+MRa+>Pq13n+#_DuW(JN9zOPOpTFadAHY%>BeRA$eCMXY>JS72IvuujAJ!L8I%Ut>=Z$KX21&6l!t3WZ^t2uADyak%eC?ie-H$Ai(T;DV_c4KKIKtiU1szBbi0Y;}i9K8~ZuEb7xNsfoap`I_dQL7f|Q8KdHgOb2A{x8y>-kGZUegDAjE84`cML6EWXC80#*QZt4+R39_khF1i(0Hz!Z(IjfV2E?%0iVG}>PS8rC{HcvWx7n6NMAzJutIL7iQ2&aR5Q6n_?SO6RGA(HvF{v<WY=&ms>{>qU`S%wlQ*}a!D<<-8Gg}H;7NR@7J@T|&s(uH;t>-GrEoVn5`6uL8uHCv1_NBnu$o`L5-^<=*OAC7Jn$CPpoidQ6DN!0_mKuygW#LTwls<F=%hD)#p>cpRjQ5R6W^iopvrVsvgOorZ*kWK=Mj_`|7kjMWup$gHFb0nZ3&yCRn839U9yRoF0Y3@p9|a>=P)j@KvbxFxfW=|4+9Fa>KT|H(L9*=q=o8nV=9GP$X4k71tghX-zwzU36A2t+X*wVBHvvOEIts1<(%6ojsH|AQ6w2X_!IlzA7$#^QhU*Ix9XZFC!{DQ^&c{2XVtj7%o6WAv(b2(tpDeip1f8Zn>f8h7m^)iC2*wu8js~*ShKuCNhw2Rk>AhSZT&CA^<p3L@B+OgnDXD;IcyjwLi06=3i!JI?PO9n9&OhDDNT2rRred_aj`E|>)ORV*!ZNf9W<IAPyXgJBm$mo+4D;*}BX3&2nTxr8GdhM~LjD|R83tbnN!7!Ry2|?-bL>(?;xZW5s$d@>q6IzAnNKu<2uc9^EVNKphRNN*pJfdqPjKH5K$h9&`&d{@#C427;r*Jm^o{Fky91z@lu)972dv12;z=ddn>}N9q_4x5isbHb6-aKzU{p-{8F6A>is}qc1xl4i)@3aSAT(29rT$~cV=fBi-dz?;gfV`3ZtQ}@+cmfHa;qAsCg4}c)azv90%stVaqXzmgRVJ7&&edKG6F1P4m@Fjgtex^Xb|PF4{C3F9QQUqoq1@f#90Y0_F`KDyKV8SQk<oYufd85n}NgHIcxEixEFx)YkcvIb6T5gOd!pZGB#*oN1HamEYsnOf*2f$C9FNrOv)_3w0t;Jx)Oz$+F1*?y?s2LIn(-O_qZn{Ks=dl(}(0SE6EZ@?;Hdcgatsp!QM`@-(JiI+}>3*X{Is4IkeJ!fXQQ-_I0N^jUzayNYCB~krz<Jn|_wg?J<Q(Rqfdu@5a~%68}f(^&2gPWwKSFKlgfU5~-|TIlW~Okb}%>s}Mxe)v1}uGYEo*ipZO978DLyDd(V<9I=e4!-G1gmQ4nWWb=<)svBknut@yQIv18BSK>jgLUE6?*Dhz`PZz`LW8h_QAtq1%!=ctS^|W`A$VnKmVzW~<C(XKjxv-srjRF<VQuxu>-C8`BFMyElXv{g_IZ0JgZE0>N+Y$tO$y~DW6cp0eRPw2m#g%+wEjkp23j4H-!#-kApMy6jh-zmu22ZO?Zv$vtPUyY?&dKa<553aQ&Zs@{wxEpR2p2a-Gp^*|M6awmtJO^H-rgjidcJ0psqvuOyIqpkr(|m2p}B1}BT?Xy+Hj<<W52rgpXzoY*;7BOWjOcA{XMah+1oT*yFJ;+$J<zJd0z(bsux3hJ^dYXjya*N-6F08htTA+7nH-k(KKY0GRtIbb8f;Cl-0jLrrpaAXK^4nmv6fXt~c8z@l-TULhl{dkInyA#b!br;N>q38;}~%6@jmZPgO$wQ-Uf8I#EK<nv8Y}`>1G}N!dpGq{~QyVF(7Ri1As*wViFw7$aR9<N9B`a_BiM`~=zxBFwX^jwNV9EE`_!6ddtdP!_?|RioT=E3c_1JAKRM+i9=E%`PMf9hN!3C1fuR^UzGH1}5q;YvfK?HlOAlF@;)~`t$zf&B2j^V&ps(&-elw_Q9SGX0OQRIdHui0FhWuD_E=hXooqp>{@a1?GAWGs0O2*5|Ih&K)`n#9)y0#M)y8ql9s(QFY)<<0Mda$HCOtHL&V+BQa~qbO}B^Sd-8*&A9s#e@M-pv$n7oop2`xjALN&V{jjFFncQF_5pccei0y`2`_@UsRH1$J)_fU{;Hxs?D_1<DY@guS*(KA&9AVf2Oq1pP=q!J{84xYcxU6oWx;)y22slc@$eCC6U$l(o+>&M;fwzhN`2K%=e>(iCp0MlqI6o%MR5)>6?IYRp=Jb9wGnz7q+1>YgmrV|=!8-Q3XpilqLq_h6wW8qyGC>9LcBFUBkudcO2oHI5O9?qg_V3N|_?9wRD@V!@8bgz&9w}H<65#Bc;!Px@937t14dnSaDm*Gy@Vok-vcp?omq*I7nqH;63V?Ue^~qeZrg|}Z`gBmS4gz2tWT(L{pWZk46+b_YS1A%-^Al0|y04{m=#oAO49>Y683b}Xr>sVY)pgE}T;gaHv<{QY;S(5$<+tQC|9I-Oh>*B8vgo0q6vU4yIfBw8Oel&;?c&#0u9+>O`+#+TfMiiN#gK-oYJBy{unsvoZsZyJutX5zBK&0uWJ<WV-frWH<$g|f?bSjCsIdmLd$V+NYdvPQxu*i=PBrp7?v5f=IIz%m?MkXaC)ozl?g?9~11_fNddNot{gk{%?!24;rnR7u*dXYd83$3S>YQIw*?kIMe4kmoLH$tuoa5M+WH{=%B1eU7nEt>gU#OmJBqpEvYMM~0G@+TooO$*wTHCe|QW>r^VwKu5x~+Y_roH%YE{Ur)$^7%qk{B3DFp}k!ttGl#6_<4^iB>RCGf_I&wC~>rR-5?Yx&^8ZV5f<OrEzeIUV2{#Brom9M2iK@+S#GfZdE=7u?ZWZEb7r*$KB6+wGfhPKNau5r&ue_*4OcP5$u+oP;b;o^tN)_;Y~vaa*f2Xv!@odv+6*s*J*qau!6nB_+)}?R$Ge-PUE^*rpW}Yo}RCyrI9<q1EjoP!LSIdx%s~pz&gjbP}-5q<)qN<mv!yj$U*Bwy;!B8MvSp7IpN#M@c>xA1Xzo14j{C@R<Z<?Y}8l=v_({bt(j7Q456Y|q$F3Z)7~KoYPb724iNX<rkPX}8JP}Oj#5e+s=yn}17SuvWM@`-r#yL!EB%_*Ly(+G1VKTD$SkpeoC3a>&D7}t3D3z)z7-N@7pWD}$t$p$|36c%ZxqFvXP?xLgGd9E0ZcfK(CLERWBi8g13E_t-UM|c>)eftOLEe5l$%sS7+C@c7%r?~w}_8I=iGGcF_ASP>PkFXSb<yZ67D78p9Y()NRbejj-5`GAEC6!e!PP{lgZHLIsZTs$x+t}I207&VaK2}hLbjXskKGO_GVm$go!9Ko}ogjFiRGb^7r&Nq9}u6l*%}j8S$m4-s}xh;XIm0R+2MJ!jC>~**h$G?;&bt@0DflG}<!}6+w>TQtsf<FSh-ZXW;CCZ*G$Vf7D7SHRI;z|Mysl$?O$amsN$g>^x;8MyHksPPQk2+-GV}t@_+Kz3sJDwER!H0wXC-7fobQ*(p#pfr+za-t?|{QIT$*tv=UwKW<1j@Z<kXxaQ$_!>=LTuFHxOQdBZ8sE$iZdvm`YMhEZ5Cl|X0c|DYE_TilPhkBW;2@&WV7xVUF0ekk@R1ZZgH!2_yhF*^;agKwo=9@C=Px|_8$ipzuF16ssb@$hVimU^AC_jIFPFb!2ZuQa1Dg4~W*B=hctYIO9D2o`A`c{)M&smmK@4+?H2XCz<7_~n<J`BIg*0(_`hR*-<d7pDtNh+!h#@kzd2F~J9gPNgwmgA3Tp8qF@f*$`{MbF|JTR6lpht{{AXLUQQx90JjgxF2eu2?42{s3UO#|j3@TQ)R}kK2eLeJeL@73=C82AU#ed1=701&(jE*q?uw$T$?dh8-HXctF>_Dc2L(UA+QwAl-YZuHz&4ZTx-J4|LyKC)d+o{xRDh-#3oipI<gs`IO1-XS8)A;%!pWvB<mefBy69Z-4#YAJ608|7nU?Z8_udLO%Z4U%prGrz$a;ws&J?I}g^#`Tc+S{vJM`MrNj+TJ;<7ybcIiKb>#j;XR&$-`pFzyM<|Q6Ay<?&Eu*RLVWd-*k-wXc6EXhOG4Ibe>1W+L4>{Cxxf7W>py<^bFKaD`}aTINSoSNxv-P^DHz_zw__-eu}RNAt-3?No)X%!!M}LCL_Z8ahq(G?S#3#)W*5<FZ(rRx6h9<<78LyXI6mLg=Y7(?Lx)5O0<%%8&zN01Y;XY{Kkidc+bpY~w+}5`!MkjDXfq~S#%Ct&AAj-~d*CosFb&&Xz#moED5rhkkdCP|K{cgwEUOp`m7Hxv*PmQ7UTNBSkcgY4=NVDC?e9PS{`U4y*>HAlvZ?B=QI&xB+QPzgvHXB}AAgK;l;(n@bbpI6upSrwWEBB5Yi1f%NeGz45LvL0tIbt0&arHHNZ18-S<_+LAxrL_b8U{^+HBdv?Io;?%~W08?>db1V4E!|0EcPvnF1sRPej7+mOAG(ykfN2(DDMfWex3d<6X6f?AveOe-CMWkN-;hY^uqZga><-q_lA7^9bHE?xwQD%^Q)y1K_$j_wv$IRG!l&fS|g^t_nH9_N80hDj(xtMY|MxT4Tssn0tBCH(BzjQe9@16%goC(qNFexyk}R*5hA!swZgX!7YAWQI$3`xN7J_AXc)kqdM#?7s1J@a5x&Hw^<!HKV=cQx*uMg+4aJ<Ed|;Th4U)1Vsc?bwx;?Py#+!jXW9-s#lm>8MV2<bxnIGi#`rSRBBAt*X1+`o=b;Ul_k`j+t5krC@;&JzMna%@7(2xaJtH(r;7cZjXXC|O+yAynNJz_2zIP$6IBU2t4uEIfGz!{Ym@2)k#1|xTbJfj9sr+pR0;76pozS|ZeU3=J)m8^eq%z?mgGf=&;d;H`xx9pve>sin9MxufNt;HYq`1p9rX&Ws^)+Lix7)m^?w<#k^=_&IwaedXBfo{db4B<C>w-{;TC;;U(G%1zfhA{Z&8BZ&?Y+T!yt$U6hm~XQ8sSS#5HVNFVs`KaL`mmNM${x8ER=Rx6d#eX6(f3llFrc_U&Tz-X5<~-LBV<TG4{$q40Q4Ojm;l?mls=?q4VH!jdpY`wAzzCv?mBUQ&~4|(zT&=<i78)3Sl6ybbHVP1JO6_E=`JA^SXY8OdP1mK2BmTdq>nv!C+JR84i?p@8&R|X%J0DC&i|&d72)9zALcIl^$1cq*g9LZ8@#d5o(KeDvCvm(Dzg|606O3LPt*!>Z3$!0o+;{HDLhh-XpJV&J#abGRsPRXfyDJjcTk*E=XfSG~jFiGbOl&GhPYkwolUU{Z>cWyXY*OrLB=quEHvV791OmZdW~kwhR#pxM4Jwwhy}^?|trEm^q0URXd4}++B9K$NDHA?f+jDYd!T%%zH_I{>io?nQ-%8hBe_=&9{tru4T?$*G@(LVV63`W9gCSgGFz_#ywJ-0m2KgJEn~UWK4iv0)v4&ejrS}0SbuKNFb;Mf2PHv{p%d&nDJuv%0iC5EW0pUniUxLCYCQkCqQ74lF)f4aTIeWY>XFg5#ZA3jDKExfKK{ctXYF55Y~sTZhFf;s~JRioh^f6-+8xZbj?zCQlq2m7Gy2Mk)-_><t5)jyG_3BbSlcLA!<J@(1+0zUt1hu)RtG~SY}2F(#(J=MKD?_C82iR2|vUsygE>oO1C(}&piYDMlW9e`ahq=k+_WBiGD(hhP<mcO|Jr%%DyaPLb!wjq6tbHC;;a@5!>E{rXTT~V~6pR7w9K~oE}yBJ1=0nrc?5Sl>~Jw&|yQ__8m-Zf{7(ruffZTy&QHyJZfY}M&C3%|CmO>MAquA7QA;`*4CC%v}q_{$3#~3_W-IS>grJ2-q2Unoa9a!ly6c{<ks@El*yJe5`aL8A&OSh$A$FXVX%13WwynRv|4^}+P9fT$f$5UdZSRuqV$>oO-8H7ExuU+WIVeq$NmX={v_GQ5nv@b){H`0>Pr5Ype%Q{hT^R}Fd>81O?=T4a5y3D4YsO2$Tmv1i!hXoNOXYDk&Vh~$`wwuoda9NKTrAKio@2~%~%;G-Ox&(4EcB|F=_$9c}`V^ZC`!LrA8ktu{=kcpM&L)urlTW2qQY;xmD-B`+#MQk;!rNkR+l^tbLl>Y%A8G`+LgOfEZnpwI&13_fnOM#B~{=1)Ny?>Fm*%zquFw6=Ck9Z$J`gf>Q{HF<-IZxL<!@y*p3PWG_u50--(%K1(Pbc0Sle<h;0i-Qo~2xWwwU<cc`QxAw`_HvUC5IuC^^6aMVg6L1f+L)%omIlfzv{MS}7Nb5X7W3R<gnZg2Dkv8D!0T$8OxQL1m=|3og-w~nHnvNa-a6Z47d!KKlXfWTfWR0Zw;PE)WgpmI{gf@?}2hRO6s1=w}o0prK;Y8u53@omUIZgqWdA0yK7M@ulUe3|&Ia@80$~oHPqOT6fNX%G?_)Sy^7uSpadb88oja{}+L1use<YWdVnhIH_!%qkd6d{hLXsT#(F<MG2(hv0Fri&2s@fhaP{Tk(RrCi1oGYmxe=kT{g7#A@WNn3^>qo^jfR`&Po;V#Q$bMhPKG0<2ieeGyIwt#O}NGe9k&&jER5@^uFeX)3`$Y3@~felm3bI?bwaf5pfH#Bo5V$K_<ZtV9`u*V><B?I`62<dG03^;tB)wA?Ex?P)PeAU9P-&?!~+-{Gd!gsT-u$QlE0YTw&nUnOASvLh*|6~c^X};n=)pEN$?H=oDafJn0@s^suhi&qnuc0xSE8Z%_?keV$Lelnr<2SLIg3CMobM&SjUMZ`ZV0*k~!f4u5A5pNuRyP1db&j%h>+vBf$kwTTRLbruDXXUl8Lyd2PU!CBDJ_R|gi=yXPVh<>#zP3_h`z%lQIvJa5MtGpt=@>3ze`$bw?|cWgAe~PIOzP_Y?A9!2|PoHzGk=|=d>obm68PM>Rs`A66>-}y2cdhwQ=L?msN!hGLfTinfe$7PWGu2uM*2*z_TS`l2D)Eoch=hs;mhend|AYG9J7pB{Mt20W0fjL(dGC3sb)L9Py3)H<K<jQ+jz>oj9Of<=5+KVRSBa>%t=R9qn%FDBEIV<`#!=EmVW=jl=iU1lhOhOaz^uMlW9K#C`t#mDO)U!llDDE_E4s0FLo`TCYoD8|_0j)8m9uEnFN6iH7d(sQRHP(;KCN$jiJHF*1DP)H^tbJ7)^S*RgZ`FW#l*BJq}gOFBPIFRtgUTo0Y6XJcGkOFdSa&-fXi^D3|Dn>aL6|E<{y%SAR)Gv)EPa*Fh*gAP?!(cEZJ&6Gmcu%5R`(iks01IlIdpnPu51o$2JBaWmj;H_#9N_!T(qa2wRTUvrE=JGO08UuX#n87~SGr;dwa>GE-XP{Hefb|@?yklE10-K`W`d2(%@Pu9LIoc@^9zO~82yft&QL@=Qb*}BbGtpJ{;Z%$gW@cP^&Id0ZMc&=dfk7Y5{iW3ZUtQ>G#g|mhYs$V}wT!(a5GK!qnkDM&ha@&uar#*PMI~unVoZNk3|7kBKziRg<z-dY8ND@M;U&yN!OKbz#;J@#54ZB2QWn5qkIo9}n^B11seKn7@hu8M9rX%CNQ2dNuHuthggP6DP0~vxcF`Dv!}o-45Go(-oC2hp;m>ADIm+I=7I)bc$W&^<o2T32=xA(ic0^3@zLIH6@VZ4Uz<8G)SFYC)QK~eOTkzky0+gd<wtY|*02id^VV04i>z%1lak;Y2!wwUOm%!s}>1kvO8GIdK+l6o*TjtcDH!3eJ;VpN4(iN9ExX61s_Vm%B!kfTZ+(!_>y9d9D_H!`d$IX1aO49n8p9r8;Z@9<*0jhIMXnZi2K0L*TvB!`X=c%Ig7~*0vL23!#Si%&C3azh$DtiN8q^v)2+?PD{@Tw+u0{c+cIw+e}$b?}Q9;TgVAG#%<#qEw+hedTq6I~O*91~Le%6obp%2y~Vx4oA#{X#EDz+Zm2aL#Sbk&HoZsEWd0k@csTSXD>DInm8MIWT3kL6O{j#9kO!YrD;=Y=3C+OMe?^U`np3$02<rpjJuo4t5ii#-*UQD<)KLkx`YxJEzc)7oK9Gcbft(`$@daA?`z1$FVOLLXD;@!=v)hNlaiJ6UB3~k-}bAm7kb3+EQh0&+p`#$((uoOjxu^IW(~?L2_%J|KdOYB>LJQ2+#Y5hw3Q#FzJd{LOH12QW6S-qVA$Zp8%>u4KTv2BSHqEF4OaBE!Uh^_ik;;Wegucwlq(lYuB^1Wh6)6y-|48rfDYJ&W;c;DKME1gm)cxKRecBt+zi6gpLX?5@pYi#dHM^<MATkE;|odD`hQC<u>cB)6jvaBNL_U>DJP1Q{~Ni-Av<)s2Hmo>n-iH^Lkr*z9ux8xY*MuBo!0jS~Z!NV_xjzMidvM*4LEh|9WKXIkkdS^>tb(`zzVb_EH1m6E&%l^f`x0Ef=IDWemqH`j^sh)6%@Q5V&tL<3@;GCCkA0P490R-&xvJ2p?JpVAsslcv4qXG;Kb!E7s9NEM87a1F}8{t}8h-1=JkYY4_i)T^<I6A9_;@rCB!oLm;Y@ww6+!0OO7|sqG2O%8!g^tug6>WW;o|=di{UUdr53kku$uyEZvc9SG?>`I^d{xTO|JCjrE0B!XbwH;~(&Q=a{n794J;)SzI#=eQo6qg@i-3_QLjac!HqqO4EqP#xDJE-x`~z_=iL!0ya>PvSfitzuq`f^)8`znqxKIO7!9;<<J=PIC_UrnLz}V6cdsmUKZhTIan_tr6t>{_!I+!}P&>C<Mj>&Y8QmNJouhjJ}3tNSJjXf+p=<qzHkSS;scN<21`?tM8{c^6YKV3ITr+ldZ2$pK3xbjN)R|xn%E&B`06V(@p9P@E#Wd9J=zlEVd%^yLAo`)xiKj>Me(z6DWxeSRYVP{~grIQYzi+A`@<QY&!j*?B9d4tBUHuQrW)Bfc?vi+6j)*G|YjD9%$T$6_s=TDi5WW=NTNt15lI=sLoGYnZd0_&!$f@oCi9cV_O9#q1*9UK_;qxB7JpIJJn@_o$_z*l4<oP7n{?2J(Q|9+XCUV)bN^+G}c<zbM#_?aoBSamL#-O<dVBqEd%^;2krm2minLV1b2VBVF*y4Jjp@P=&sy-Ko8~Tug@vVH9#8bp(e^H-1_l{!<t`M{vlqJ#-y-)&3cqnFUU322RW~$P_;iiJ`BGK-7SWr;cZHI{-4kLoa>f1nJ3#@eg@9sQE!`DH$ScpoGd!DRTyymZx#29Z)}{R5Mv<cF`6DbW6P&FOJAELoUzoX{Q&@Nj};6w{md%K$VuxBA^b-7-6~GmISe#KN^{kaVha%8nlOI;T|$y6cnv$OckzI(eN(O{vb$;*<UqRjwq3_Z@Z0$NsvqdSw@$97zx-piKfZ4q_dmaEEQ8iuc^dl~q!?*8Mn`!5^GJGreSiL!ANkK;A1Bu@zyJD=U;g~(fBXLZkGH2!Q7785*k($-oay!?ctmC&L)Dvn;By(SxlFDZ#`%Z83B~QU5ES7g_$9>`#8_k)^gsXk^|!zN?_a(*Zlvv~9vkoD-~9OfzyI^Ew=gc8oQ(1urt*xvzW?)y(ysEyuiBA5&$mg=$4Uja9SDG?X>(&6N5a(zUv4dd2Mo2w)ppyZ<T3EtrL+A+hsV_W#`SQeq3iT&Gje%R{k$Tv=1BX?_jhF6eC_*9HSI{W_r-n?ywB)LYK}K}?EReIRB=EpV8(@4SU*$Sme<bc@s9rZ``g<;pZb64wKG*=262QD;}_c7jkHz+UAfymKFg<yE2_|Na8k8QBmJS~jGU&?<v-hAqiv{8C1k*u>`qBQEc#ee28Xs<#b5AFC)MVN+zi1Pkdk2`Z&=6n&xy@6E$;q8>UFnZcZnKRtFnzYw3sS}BCB14VR0fBKjXo|^y}!6fo<-F@KiUiGk=nmbHj;DNx>wKz<9Lt>=t{t%to+-sK1KDx!Pf?%|EAPH+b!wKs1qi(=>M|U1%@pV1NvKxQP%=^VY}a00mx%U0TNCcYD*1fmPlUcX!VNWL3|32P`bs?x0-)RxM*lmmkLKVXvZd4S&bmZ{L6a`6a;upL@yY*RwbWSL{L#xZf!i5vK&UZUe<cWN<3ex~bB02T><|2<>ke=fQ~UeN&KB7JHq9mH0E^CMW9KzAZ|8hGg!nzL{_E41W5kYnE{PCtOL62p3h~(sS)yYk1pjPl7)FLMz1Ra8y4Aw-2f34$Xtn1Iw^3V)e7oqama12l`W{N@bN@`9L6s*q&N09)=uRhs4!!%`G9{#`nGu?hgrEV3{SXL|A!?x@X1XHd$1YQrpzW|Mmq9Xo$No4~uL46Kpte$Ox4U>fvcV(s?L-dd5Jo9T)u^ZL+KxL(8dIuj#C|hH<M!%yb@|?bqz9d7NHduq&AA*RI^!e7gZhV$PXz?+xL|IUTd%2>i^r=V|a|cu~sI-kSj7qn2$gYbxGz)2ii!peilbc{bhH60#a+8GN1<<j&++xj(38s!f{2cNaYS=0^S?@|Y{yt3t0?XM>Cfg*rk{P<t)0s)Ww~TU7J41U6CApB4DYg2-HsuOc7ojsWu?r54`JjCrn18$la1zYrQm%M&;C3on9o><b0#@(E>3`x-eBUb%HT0MF94k>dT_;W)Ou0XTKoP0k+2bq7`u8IhvQ*SkDr&Y<gLu1xUqteW0#+>HAyB$?COk&_4J%14h~ni0VrED?s6cw)kt;JTuGe@tvsB&o`M=!PG!7FJB7O5co~deTvr!CXOo4G0deB5KZfe=0ax^2NrTc=L*BHi=KS3B2DRPt(vgA|%tep1tD=MExLxh0~Vrql=1okNWK-J3k-x+3tSKY5RN=h-Edq_PpLp0@Y8pDftHR$~B&uedVp-jBw%c;&KERcnKj&8|Ca}3^8Q{b%`X+j*$wLRzUh@F=q#q65Wk;tGLZo+e~`}d9AAAu9coB$vbD@2SU|3(jEvL@5RHm8=}DzlLz)1kr3y~_`oKCiN0nk6WC%mp-(iKS@YSrOtB23+Y{oI8yIRzzai7_(l+*iCeG)lFkG{pI)tTggLv~+R(-j}%Ej_Mu5{xqjfnqeAOX1D?XU^ENOapdZT~ONuE=m5Z9diok1SKzZY2c1TjaM4N76>4s5G^OAsanHr&(5r_klBF$67ogr38r8Et4$EDU2~x*fE5RJ++u~q!Q8=Cp#_CA|-8;EYS{iR<VOHE}p`sV+sVtGKjN4$&EhM&QNxlk3{_UPF~+<qisV@%(_m*^jUNTSBf`W%!eCeC)le{`H8XG1Vi9#R5_>A;Ya7Cg^9%Cy+iO9YIZM+-TKo-D-5IuQO)dru(c;cvi5^l5qml8qIv|a$S%XGieKxe3=q1iLI#*u*fid3YbQ80di{!*sQABB-J4VtQlmx8lu;?X`1)#MvQv0Ul*yL*67W&X<{~M4WzZNH@NypYrH#E59}3f;d2qP5#L|`k;^q_M5Ve{t#URVOa9&2s%B^!6EOKaucg}9haYcegM@bEFREAZBkOkOFpj5I{g=cVte6E@>IAlcS+RGq%0uGO&y}?#h_HSii>|!9bqpJusU}U4Rl5@2}ZGY0BPszaT&mpTsfe3`7Q>LxXafdvQQE`Rx>;4)A3d&+PLynaEZYQZb<jq!FVEJr<;Sr@W?Q-2_TPP9Th*Pda2Fe2UujHz|;)05)FD{_Ssm-LkxAuuXB=<4gee@lD;EB6(aECDuDUD-tf5|SQJx@vb7T(Gs?1T=lUGb3vwr-Qh$HwMh|F^<E(FWVszV123Etta!g3KZT4=H#29<xn6rT`pNscwNd;%-S`)@yN8F3mv4q>W&rlY&}YMD-U^wj|J98AiKRN9PGD-~eq%;COy9nLXb~ks!U}dK}3-8f3IC=zH^;CBd;@2DJiHUIo6C00oz=0{RWyDq~LinM;RT2p5aatO!qD&0CcIm1%T!6kaSwvlcE~NU)3*olcVL%~lnS3>erx1>Hmw*K|3K6IEo&bolvzk(S576wSR%UQSCVK-!dE*mMdRe>{b`biYNpS}92}MVpKI@`|*#kjm;@bAjj5l0?wfIM2#uSteUgq%rUVD(BKZl4fIzV7)O#$ou!4lT!s6Dx>!d2;iY2XXYpYcD*pma^yVanOAqq@$%>b6tepmW*OYhUytpa@iwEvD!+V62<mloyEV)Bs`H~$Hr4Tx3z@XXP~p2-7pTkE`93m+?InMD-Qi_U(n)6Bux9;}C4hnXPWTjP?lOaXthdE&XJJKBQ2U_>u&GeIn3H+D!lHX6+aeVK;05SPv3r-A{O9ORyTDQ;bEZ9ZGto6|$&cE4z!6};it2o2Sy-!u<S3V#=u9cQOVm_PG1F4S>*|&a5)<UPm;Fmgd33|8UU*y~_#^rbldMqIAwwKfSGjs4Hqnj$`*wR&<t_N|AA>^z4(%qnK9ztud_PUeu{ftSxvCZ<cvtU=SD7LhxOE<tp>U!0E|-}3IrF)%8MgI+7b}etA6u-$J@MAX#-kacq+TNBZo$kU_Jb>HLWSl*J0`_Fcuh(oc7|(J*40L&si}OJ3%=(VX4EIoB<67Sin2P9K)cSb7uMqIv}@7^Oz2zMZC_VKhXfC}t$tbVeBVS9BiJ8@Z`lembH$x*MQ|PYo7AcM{QE28--d)ajBTCkvfltyqqfP7bXd00K4>#Nd>HY<b+eGv=kAZH*_o24Q920t3t*psUy(DL?u2d5RFAKt=lWl~Pt9fGZGb21fqUoW^~4u#u@cB;fhQ^<Fj6j7{tD)$aa<ECuPL`UtWN*61?HBema~j~eFXbt4&cI8YCk3%yxO{)D2uFNX>U91=Dz2B&+7~=R}#}gqc-kH{x+WRbt><JJsn(GmkcQo;uvU*Br~;Zb(a@Rn~h^n`dg!f8Xr6)>smP&?UaZPQ5L5yKzqnMX2b6|T<fPZ{Zj_+R5%ajEBU^na|V6_2%0tSFQoqe>grGXgVn@(j+pCYl)WUN6^lYaGgS72{Bp1#Z1H*|eGQs66T#$*K0a>rxJx1Y+(6zj-4NtYawfr7Wk91Vu-Oy*YO0ixIKJA0ogKim{JS5WMaVY;v*#Ibz#x?scrF`_Ch5qTAi9?nHw4a=sU=;fb*|riIYt|~;MWb+Z+6ZS!3XwdG^M<NZ{|C@>|tX<q_N;$du$&aJ-E$IiK)|9CQ1NTydCLXb0n0-1MW;-30<klL>^Sl^7xigdM-!Gl_r4HJy8U(sH8qy-xO~xp5^E;zG<o|2yL-js6wvW3;6Mo^39=FDKEC*9dv!tRMo>TW>23ED%J@s-KBJTgC%pojh`RKt3;)*`HA&+-qzAOj7fseL|m45BPs-PJh|ScLDaSH(f;co3R(x-WKdurmguX~m|&=Rd}}(V&dJQKsx8FEDT|5nnM^1unoRuq$~7}(O31V<1d9m*2&CDg8ee@ftV51Q9T`_N-GVX$LN7}oQ=;^7yNxTd`8nA&$CL$dld4~SMV4-Et;ei3_f)`S#%pTn9Yw05V4>|c-H(7y(2|7jiG<7zSWMIPkdFlVDe1`E{v`oSEBb}pAn2MIRo%98eyr5)n_b`y>WAv*9LK&SBi1Sutp2EnBR%j$MVD-(us8Dy(u5L_w;xlOGta(7YoDZ*?jgUXTJ>Wb(U$opbBp<!_Ts;}B(CbQgh;P-lVBvvD_bi%dR1K3u_UDEM9oCW1yPYS8(94on3b;M>Rz=i2a2Wb6)<L`_jN$>(tg~0r3RX{vqPobs(cD!6GrynA200jzIH$F)pR3Q12^7*Pq9{<t*_(pBG@gP>fWfE!ENQX!<&W<<Qfo((x(>H)a^j5*J*qau)6JAE>HkT!*t2XX<Qe}G?}2))AN-~L2@T}fRy(uX<c?sasF=wu+H%<ly>AbPYK87uj#V8k%QKW8bV0b!5Cv(^e<a=wHO`z<T$+ytVK5m(4bwX%_kehl3|EM$!SwWbd4iaW1mOfdd+w55Q4Y6a2@SGtlShcsVFj1DJ2kBZzT>Y18*=7gc;?Koq15|nKXHeEB%_*Ly(+#OhJZ7vAuzu0=}5d)ad{T&&f=_vMgs8eXYS+DDO^-CqoeFU+398`+Ww!b!FI0$Z2oyz75u6{EOiq1<nzIH-V_G&E4RKO!jn?n^XcOSpo<cF05hOeHHK7s`q0etG}qwtr5E2CBjvx#*t45q$&%46Y2uwsSLp1rBBb}9qfIgdmy{@4<wNsb-jQ?K@lEy3`%1-X|tDFTZC+H#$`xY79iRnZ8M`;vY3>=r`zM|8;wyan+B#<o}zlQH%M)>X&zar7co6@`nYB5w&cBssF}T2mYhNz&)=w?I=0t%bC29}xQi{k>$%8y;G5gzz#nx<bTax#gl)^z;W}^*d{yBsJ5L#j(W&Kulg;ivi@Xw^Mc~$D`zkl_FLNE&6sL<OvZ(Box@uER9Hw={`qQYvr%qd2)wr#Fb3aW8e7FW!*r97kcTlt9L{uU~V%em?s7p&b6{=_yux_7R>>A|tP^xBH3g^T>)XQW|2-N1dn3XAYL(+UU=Rgt5jS6^&2R|N2MN#MHIOy2EbwU56uixFehJkje1vjp{za~^<9neGh`RjAaat)9UXsBfIb01%SI4rY<g%DyHXiN&bd#p!E^&VV9{j`g22uAG>j}ODIvK?d5ilOuWeBS3=Rg%iok=q~SXW%RzHK@5B=`OThlW_f$?@N6AZxua@Z)}{A5Z@H%F`5=6<JLT$lMuT}+7-)$+8>xZI*?+sq3Lf-RJCD9-^xu}#kx9&fu=}VUK((0f#X{(_UGRv@(u;BVTT4T9?-RK%JoEcSFeB^NcUc<>-Y$M8-HK*1Ks!5$@TP?f6VsB_l@K6=a-FT&>|U6V_$=0B5hXZ$cTR)Np;KOk4)#UkCW?{-+%qbFMs~?zkUDy$D8Dap9j@gY-gNa_HcU=JR-A?q3TUO@VN}vTqf7r;QYhign)8eAd2#I{F34eVk|NY`k(*&`rBXs_b=ZYv&ME*kB#^7Z+`s#-~aj7TNoD_x*zj3Ol7HgegEeZrL>;MuiBA5&$mHq#!9@j9SA_HX<uC%N5a(zUvAxZ2HcUx)ixuggemaa2?+lr1{4mDwaks{;VSyp>D6ZB@`4_HMPkj7_LuMPsC)6+_nYc(k>Ku&`UQBO(UsI3Z}8arIlrmmLt4O$3$L)&pSDk}ozdeR{qgs=w|`1v$9PR?cl|xY_=RM0BaYNSSMGL?&+@6_M=IbutgAr+LinNPjGU&?Wdqw*jBTh+1yI14>=r>lM*3J&25+=l#b5AFC)Evztm(iRkP;CgZ&=6n&xy@6E$;q8`eV0XcZoVQs|t<wCzvXBA1h~rVR5<^KjXo|^h@iJzh~}-@PrbtGk=l=bi-Hbn`e365%E-`ooBbK!&M!E9YpOiB+k_iTW$V1rT8GI;W0!LX@X31ha7{p$_)m{z=xas(ll><qz+Kah1jL#y9{WeQ)L-&_i8*qR`r~Bz!GBZ_1Gn^)G~>5`Qd8qnO4!Ag}>wNx9`9I{E}dS&%HG5>sg$GD|R6V-0zg57;uYSAp?quj0UTnr*%^$!wsTN`ViXRFnWU#*ZW=$sVw$72`jx`!dOler+qhz_zcP1S$#9#;2He%QCH*s_D{H~8By1%zNP2dyVmfw+fwp<<bzg15OnEbHutm-spk%@V9^81P$pu<t<VWmKYQBQF;z04?8*nqD8$6lGG8#%w=xDFcctcOPpF0Qy)U%ZLz)&?W(fxfR^FnfNAb8#zSN|&AocOTeL<@h;x5d?;yShj8x9;YLWqJ|GMbNc9!j6!E|A;~oXrg}t*m~2s7^NztF6BKd8gE!lSo_8*?!Hwn#bwY1-pW&e(lPwt&|&ZB<7qcGu9A}oYOHIj=;~1d!7bgB$jqnzrV!@pChgOlqAJ_Zd$e24pc$q3dN?0mfsySo@MZPR**ZB|KzrgnyEHv65rhdu&c-Nj6CLwv#QW**4!ZDL7@oH6VzTytSaF%z!uefEfq-A3}^*@vLG^-<Exm%+WXx6N2!H(la`q)uRYLr%`b$8(elJi{lbf29s5E7yL>_!)0O!VwJiP?zkm+o)>*pkQM{iU)5fMHu`IGwK}2=mxq`@uVq?DE<w;TojaPH!T$X3m^tS0{OhX~boZgO{JTO=0XYA692<~8sFucT5zs&^K73KS5Vw)mKHTqRg`0;9C#Wbq)y|t;07-bpE71Y;&;P5J<j(Yc}f|Dg*=h}%kub5_&_;j1V`<?SN4Q(SrGL7rmJ6<-_!Y^1jZTUXBs3Ke|)lS0wRpx!Rn;modH{S$eS<S9JulJHb^^<K%zOT13`(_4Kc{48~TzI^=9Ki)%LWt5vIeQroLm5GhSLEXucQBa+sPq+cc0ei7-B`DZ+g!EHv{#VVkSgw4>BEt{a|V7ORGlO3fxz+Jj5$4Zj_?ocH6kI-l~TV=0uwFF@2u&d#co1(UsG#x;bn?t7~P%_uiU^;Q~C{=eitBw+BR`MKZW6%?bIPZh1<ZJx3cQXE!Osx?{TFYZ)vpdKLZKC?QVxn*hQk-&gt-fd3HsH>uB?_hIgc#$aX6s@ZBQ6WjK<)5=Et{EezQR`#H_BLiP@v5j$WbGD-=sDp)32mQxsGC{$&r^~S<DO~|-tNL!rjv_y;KrcJU$JJeal4#F#R3Y(585EQom!_PgV<hnpIb%wIbd?ez(cd9K?=Z){mL739S+SgVo*>Lq9?pU0lse&NZqOU<;5_~={Q?Km>^9ZCdI@{$WZP>*`I=tKHjo*_H<&7oI!54wnIn-fSaEP^;RJ9j|KyKHA-?|f0&uETau#aFHIbpn|6NrUESxXrpELVj?FlVwU%GtJ6a3a1MvsHblRQFQjUKp#>Jw>l*8!ctBmB$3U6|>C<#8A0Q2cER@Jzarm@xeL`>j$?|OMQ(^OdLn;AU9vi(y2^_eJL2R2gKpN0lMQ1Q6CRRtAY!rW<<l>DzgHI@cY_S*Rj=ID)~5$0JNx2v!o^hQ|4=$dj@rG<ZO(JD{?uIx!;lt^*-jZ9uA@aGi6Bp0S7_GJD7wLkuA;`3SWK9a2sAx^a7Z2tbCKG`5F+zW=lM<BsxJWiSnm52Hj>`gArYGQ?4!tc0>IuRze8Y$F&2trOPFyZN#KXtg-u=akFc^w&&kpm`v3PA+DInEY55xXjzEv^!CU^cd7av2)CZgHn*G|WgU>vd%1S&KG>H6Ya{zVVtp@rmk%!Jv1>Z>HFe5BmZn5$lzDhC3YCR3?Nj>D4Lnk#;DyEk%AwwOLYcv_z0WqiA`VglMPiGAWjT|aV_odAg2Re1$iNspA}koAf?@)jKzP*9#{~>5q+u0|U_mYIoXhGe4*(X2#cGR4Mg2^<TnEXr_oGi-^qN!lahhGPUa-1$<Nn5vw@oB)jHT&($WR3g_2?+L21sK&cA~Ok1yd-8I|f^ODB;kcc^Iw{O?2cOV-ACl!a5)CkP`K|&2KilE=NZP^L?`94iI#j`lxdcm}Bm2$sib8G&>r|Qr|C<D<7&i5Ty5VeQ;f1&jti+gpzQJk*A~rrs2u$+b*6%UM;q$PdTZkLp%R;FC%^0o12Q!?mEhkLQ~(RJPXUvDwz44itM8I_g>ah1Tf6AM~u8_{bnv^GtTH3f(iL^pk)|*AtY4~H|i?yZ_FZ05sAxST&se8goqaOJZHw#1R^K_?6c59T^S~K2Y;3|h&;i4LjWCUo9|;`EfLo-0)_W$*3zi1tL+YeVp2kh{vEI)7m6p9RB!f-?U=p}Un-Kj$5kM?`-4$2>1V`=c`2$hJQXNa9(kp;Ab`+Zg_Zh`A&<Ezl$(WFED^@|<+-s75^vYs%FC^4pqhYR9aFE9jSHNCRK~TVN)Ni`7(FMGtjY+mj5+Xx1rpYp3Zp@k!#=3J?Qz`O{B-7_r4nZ)xY&zr4eYkXuS#*2HogWcCTs={Yv-)RSK?j(&ad&sH_mBot`mZEYs&bpg&l3$b+b%|FA8FCB$lxDKr<<`{L=E_Q0Yn(VrnZd-1heIbmmO!m)+x@kO1*yx=rJg$E+kv7`<~4SP&Kf`38GC&3=0^A8>nD(WIHi2<OmB_W>r4W!l%B>NJkvpdw9zBSc<65pVigI=9CZCRMdbaJ(C1<4OD<rMYml6qd<Wh5p>@u`8wWn&tGCML-TRtF1y1Nmr+4D9<1W9x5VlzFAN>WTl*gUUI}TrVbD4pjtK=ERxMXa;a{Z6~H3#JL_Cnj$DZc*%-w=&R)Bmi9cNotB-+~!G)MS{SSv)*VNPANg^j<z>3XI)tofz_T|EM3N{K<JWJt6V|Q!uSiS&4x}!1YfafGtNwuZ9ooq`G>?L!_#>7xaUsK7aQWjV8iM8lZ7%J@3G7kHQL46M1pdhN9%@{nbF1-z)aXF#;1~@0PyFK(uKRcuL#M^>0h9g|u7|pnngA={7>a12XwR?M$eCqj{O{T_!Ztr$UUZ0YwfrsX{)r>@eM{2{7x{m$o+JCCsg=A0ttd`;2C-?WnPG)b@Z0+`BBOh;LvE_Xkz^h&i?e+9`%sJ+SwswoS5*$L4&t6at`$p4{Rmv=rwavK+OHfw-0-1I%Kb*yZ;9S1#Cb-^go5WMmI0?OXTt7DdUlp4Pae$Y<G;Ba>Kvx959zInG^-l?^Am~I1L2EMFE$pMBZ6;+K?UODe4Td2YtRlu|8P|5UIb)1;ZH()G@yem+u<#RTD~K@9t~!>W>#=NjwNr4!Ye88AQ&)|0)2+Owp6v83n{TJR4mZ1yBy?Ej0GE)xG|WRYsT!E5$E=Y%VcC3|cf=HGVd~HOmp2DT3W|~QR6OGgXxImPI+(p8o9DpwY5+uHIjvx=?xP*%(6VdA$+tV;8KD}Cc1lDhr~?7tad;5=AsgNMh)G)Z&b-9u4+2OB2Gv~YCk_#JKT83ftTo*plJCh6mVVqhV!@}`OCq<o;Cm`d#D0)p4)(*E=4Nt(jYPopqJ_2_YVBJm5mSZs(OdInJc6&vh_77njIw=#XJ?m86LW-N2QW>R_oK7?@n%4@Jma#uh3fKX7b4&&2_t7-*?-Y8nsZB<bp+lf`s4fm_5JDat9rt&<Kz68G*jWkb+wOV%bU~t)y!zhBxZNt>s>ZEum<bc>!Lljj}95RH`a=V3&;c&#M_bHHAlkKFCaYR(Jdw99NE7&%i~+hWUU-2Lud?5ntG&QQAvQaZ;CgOjB<2%PB)O}<EZecSi$e=f65MTfn6Rc%W8U+@+tt{LDwg9#hU8H?CH}%#X1Opagdz`yL@`z;8*<oI9{ble9ccp<?Ftd)}c%KBrrJVa%2$5@tm?69ah&lJ93GmQP4U}E{9KGAeP^f)BNM9(;`CR+Q_1ZhEfnersN1plQ5wuCbf%SU%6(si0%W{0Roam*%U(>s;cqTC&N1A=(v$*?86d4h>P%-C6FoM-g>)@E0+5?*|k>-8KA}*(C*FB&8_vA)#jcGm^;<T@3=dPRN=rv+qEmH2AyOZNV_L&tq!=Drt2Xe3G`F)9=Y>!0+`l<LSloUYi1losj72+O=b5feDQr|@doun^>dD6Uy|Xd=ZYK^wqg1MpM0TuvXPj4=BsH!snUdI3UlV!w`gtKLP%w}(uh@R%jmZD`I`3Pzqur?+9dPOJ4<3<D8WdUSGJbua#dW`u_Ri-M9oC$VAH;T8(3}PhwB!oI)I%f8kWYvDSGLB9gw`V9}_JWG;3#vO1oA06vQTMh_a|ha~*d-@6|#`uKiTJ1D|58I9p%G<3+Grc0#>TBhlN+ZHG4v9mq8j$IhNw)Xu5{v0kU~MZgO7662EzvRQ2{DmabnVwolrw0e5Jl9op91P_q%eg(rKu;%9fRsic9-$H3eGMAG=w_nz^b0Y_>6ZK-1h8i)(w&a9wC&vR|{Ssg;x;cQ*{#wZrP_j{D8PFC{1-52N0WyS&UXhYqwN877B&gl)=Qu#zcbjHXQDkH~TscZ9ZKwioFb{+o<&d3O>7DZAEw1!yS`R^TDiH()86va92677cVm4E!10*~rGx=6XoL!_=NGGqrYX1LBxxP^pYo2{lI}RcZPzEsJI6|ijc8~EJwh!nWA$SwijjVGwE-uMQ(@}0x31MUjAYiz#hTS4Q3Y~M)vByN#gs3a=Xki6zwM)2{gnt@rwjxDBU^;d>ReprhBKz?U_Dm*2o9FxkNhC*IFW^v6goho2(il$K?4{NgA={gA84@O<%y@<hslqH-Ov>NW--x0Nicu=#RA$7NqI$D8NQLug9$87wFbO~UxMlCK<h_TenY~w*xzlLRL{tPhic7hJN59ziQ=Wmd2fn#Y4*XFoq123<pa0)uB_^|1U|m)f-m>$Qkr<s?9yr;a0CJzHJ+<m{=k&JMTG8@9=?aXbI9)W6MP;Wz)dVKamU+{==0!!idA9mo+x@s9-N29kGvS(t;|;%tbh|DqPDoM7yr4QRE$z+ydKewNAD>+88szm*w%Lbs;vec|vL-~Jb6m{Ziv{f2XHz{CvD~PDKp1*Gro=f8x|(mws6XlJw;>P1K)cj}8`s@m6DqO}=%M`l^*Lp^2DsHnE2r>tA76hsEVG7%5TYz%OzK-r#yn?PQoRS)P#?UtmSEKW@c1zNDqG(Mtr$B0&*y#4RVAsYHW+Vj`58EiM-6I*>RFCIqIv$G9142;Zxua@Z*1WZ!yH=QdY;wou-=--a}r`VNxNd1Q2PUb;T|g(C~w)&G(K)4hV-r6v{kIDa~Nofl;x!X#}+ug)nb4CT_WR9@EUe#;Nk&Y`=(q^WOwxn$boe4rMixf;J5MjRX@;uZ=GCEfBDC3e|+CK4S#;wSmjeDyPwh4jfl5NNyl~jIwgzPa+j>LGmjbT=rz_0tRKu~g!F<Xc{`AQ`Tf^_{POcfe}5+(Oye#SOTf+Z0GwQkJML2P<IGT>j$w_0AP%%rA|0z%+;%9GIRt*io9*Lga@eA-%!T~j3UZtWb4a3%*@ft^g210&#m!2UC>t&2Co%n3xcm=pVG|2ICt9~n`N!Yi-u@~3P|j5_RlGh6U~pjq*22>ETea)9p3-PeX?Kl1#Q1rGR4ek+Krro;n)fGy)~Vw8DF8RD55You_@QQdOw;JHTH8QaRf}4Sc}v!Cn(S6LK&tszQwIOBTE$=RPAApX_QZ&-!?&c2w)KW}jQSj)Pt)S=FQlV&3pkf3WUDF-Bs_YIs@P>&Ff2|x;)N)%F#QrS;278<QZ}LGT$jW3sCM7Mk>LbXLL+$u#-p8Qw>-h)f?x+xeR+x3w8K`Le@-bEh+rm$8X|3rY3`5}(4Gvz09g`!lM$Nct&f}lYLXCxtMOKO{+)Ekscgh1=eUjVfBy69Z-4#YAK(A)|AZY>jm=J{Oi;^+(J=beqB5<b%LsqR+i%~0zhcqQi?WAqd{gtDDzRc#kO22P<=O=~t=o|QW2^kNO@jaS{rewpMsRvR<nE=*bLJ~`2Axz=7CW%M4u-gl;owXMEu_=dVFYh@4Z5oP@fni2v-)O^O}B60gC{6n;T24si>Sm@-_mpKU2Axgu|*7mSw-|#3J-LfVOH|A52@$g-f<EpvYRi#t_x+#GjiLYLt(1qEFGkW**j7({V&i+7a~bFq2Xyys9y2C&;M&oHv-EnA-B)UG$2oZPnxI^0B};8hWhy5zRYX-UW1>9#kIVM(8l(V5rPWT56*m~^HBPPV}W!uE?zmJP`n!;p|Um)tF0pYd8gDJfJh@RtDycdoN;<}!LDGcU%PT^kM0H>iMdnCoHB$X=XA`5Bk(iho~OYVJLUe5Z!yB>NCZ=ZkZaFXZpTnG2C8{-rCoJy$fne$?s=AT=XtZO&P^X%!ad*;XmYh|eZ7Kb<S{QfZ*fM_m+_$JZ0`wbuO(LbA2PreId)oVhN!8{3jAb2WG=^7F<`and51@lTzEH$l)3UQ1O3DNLTH#7PaMlHya?8@FBGuLCzSbHImQtDJi;rtPG7@W+Lckf-?sU#%r|0rU#aGIdmPstxGt{pV7}hvNh<~oL~}(*X$#e|iLbNWG-GZE$<p+8ocJwYSw^u-Ga_n(CBpC$PsKG8TvycPkBL<-OYQ4ybeL*>fy9bwRO!3Zk`OIo-e0?E^S$O#&l8L>pPvd&mVCWt&yen%i^Qkf1m5oeSGMHuaerYD%{!hf$VLqa&<Vz<$NcGRi{L&X^FG^6dpRAKZvwGYyry|C2~<DXZlg&m^p{ah>19(YBV2gAxE#R+UP7q(0)S`opu{G0DuNoX$j33DU~&PL&3j9wcsjM*jdiQI%~ktHdj)xomEx|IeiF$$XW$1y)dA5S2psRl!<Oj}xrF3_-P*HVM|h<;Z<D}8EABfZ&$rl3Xq9SeCN8{8u?(Zz+u)TO7-~wtA=9@31U=hk#OJ3lT(g}zWR!3_bMsc#3?sHK5X$$s(v7z?n(d!~#698&hE3Q-qHE0QRDXGPMTYBW^RdQlqyWfvtF+yIEU_cmK~Yqi+QN{HK%LX{DdgM08L<O4BBPW5$^B)LWjTd0GXA?#os9)vnvikPkhVD4X^9reCYxl5cBr$89farQ6gJONASi5Oho5^!$#sEb>I`L<`AEcn?^GkB&KuvA0WPJ9wXdyGWZ^0_+;BHRQw2e+MPGyd8u)x(re6C7=5<G7bhgWt4K$fZhX)zG@p}@Yyg|Y__#)6chdS&E=dd=Ds`kPV$nARYTX#b08K$ud_7Q9&M~Am`0<lmiYbgVS<*IN9=1ew4*%m&Flgw9RwlezqjT-mDSe@=EdZmGJDU+?BCE%@?ZAKu5$|X7QR+aDR3QUU+)@fKjxRqM!Yi!2hI70`y`BIing)Qu_z=%B{4)=|`9fyPZcraQOTrf2we&tq~6*z?7muv;L+M^{O#}P6X^=X#WL}1E%O>@tn&W$XKQE^3T{WAAka-rVGT-L)u6kw(di9g^V$avtAP$IH-8AAc5j~Q;mE6P*=Q;ro}5;b1~VvyBKt7|MlD~a-_HU`~hTT2jKb5pJ^2X;gKD^@}X*2lF2wx!GMqiw{bilVWLm~pdf-LdE2UzkkQ2_deS$n?x?DQH=U?)3IZ<6^1$9SFCc%MZ7l9VLNZzcx*3S@yxc6j&SC{}JnZ*}ME)L62S2nXjo+2C_6IN~6q+f>Ed}oN1rZhi>5Y83ivi4p2_(zN5zsj_rN6=@oI15-96h3@poG;~eW^j};tNgh2+z;1OZL7!?!~`_#8b4Sig|h(Q`J!3Y-A($2Z8uJQn2aagRjh*Z?il*@IHEPFrt#KoIAWgn;6_38zyYd7w1{CL|$0>@aI&WDUaz)+8lf@^>@wqqwMD^@Uta=1fTyKs0alhcqyCx7G|V-ACl!a5)CkW%Zp&2KilE=NZP^L?`94iI#j`lxdcm}Bm2$sib8G&>r|QvWKFD<7&i5Ty5VeQ<qS&&~pDgpzPQk*A~rrs2u$+XtRQUM;q$PdTZkLp%R;FC%^0o12Q!?mEhkLQ~(RJPXUvDwz44itM8I_g>Z;12D|9M~u8_{bnv^m(A!Hf(iL^pk)|*AtY4~H|i?y)QnyciOXPItAc%mh!*rbX9mjzA}9guv(Q3a876lJf0i|fJi&cK0R2Xr?_*&t5!W#Sh4*XL(r~S-?GAuqQbLLT9k3!5#}+O}%F#w<Q*HK{QLCkHmSxCMYpGgTJ5G2)q;=gqm&<cL1_vqS&*uvZ(r7RIlw!!#Bn|BHQbyUc?x)Hz3;^WMjCLi1zi>`sbZIm0py)A=E;rdK6`$VY<emno1k{jtl1w*?98TBV69<+|a_&1XGABV4>N7@wrBp2!;&#n)>5SkY4TT!eT6TQ!PHzvtvAo<Q3hH>lxkzpT+BiVg*4jafX%~f{C8YqOq=8!*bMPe#<q>$yGBAW2J?QlCd~<`jowDf4xMymZ7}ntz5{Q^mI%2&(YB&GTG9GrD7!wTTOEMC3bM)QH<m+?@))<H5Y;8J2Bqlx%D#>k9?Rc?Sjpb1IFd*j}zdkF;Zizlp?^1l^QL(i5u+gTSsQsR1#ibX7%GEb}Xv+-zVO-P9oB-o0-r<s{C^8-Tcay^T#Narm(=C<wm_xBkE9NoPTA8R*f}x!~$Hm%RIcyISty34@Kb(rJ^%u%Dq0O~DlGcnFlhv^8pA7kEtk~Mrb-AW>`08o~*>nj>92Al^c`R*XL11-tYnn1xF3{+XOQ)CFR}n#v5XA0Yk13af{ByqN_)7N<l$SNta7n3(xK5JC)5MgYK~$F)1&KHPs2u@@1@^sMW8Ynqkl0BX|3?L}!^QG3sH*)=trUL8_kklS4{-z}u9JG1Y`=?7@>c8{t=!-_ad#2L6z05l|DJPlsu2%K{z0v6JXF+{@@5tJ6MWnGnvCp$hPi}cWiQxi#P9?iNIU|qTJ&hdO~qB^XpuUwdzjwv>E+0AVnBpRL}5IA0nxH>{@=%Vi|r2Q>7+R=2o3Lu6<MquUS9@f^p!Am$I{EBz*NcY{{hp`>x?S=0M<S4g*o&#?bk0;y-S&sRBzSR?<xT-0ofaG5<VkK53`iT)x%`{%d}J)HnFGd!coXwiWXOHyGDt%h$xb>e=1TIHIuEoFiKECz<#Dak*}&<m#VLih$N|-IwR-F`@Vr7O^*L@U6SR<v^l}+61)(>J#Zuf5_4EHEFBbHw5#p<RH7)KE3V&S0J8X`v@fCMsN3HJH1REpR^U10gcnC!Eh62EnyilAfml1zZ-G1|4l*wRvit>pEuvrU-uBnTFyg#h51&Gd`g#S09dt;BIAMeO1P*3pn=@W^*Q&ez7gGi()k|Ows2lkjYWX^M^PE6~e7r5ZSo_FdbFgt@p+z+ZIfv{gWIn=4<x~$gZM4#EUZ`dBTU{cy<a^965&{X4iflheZy)UGU>|4MKn${NBheGf3DNWR(LUj6J*DbPvQ<D>X%39m5Ys}a1YSsj0-+zWp<sg8^ktv>tQdR_HOSmxpupA6;#<&gIg4O5&~gMDkjM{~hUPh9u4-2Hl8BBidK{HzV?W3*2m4`7^V7M>kT_ua!6uOj#3AUub&}Cl<so`&zLZh$RT*l-am{k~Yp_(PJ8^uq2Rl1}19bl!{?Q3zz8UyMyX|AHq-A_HMM=*$I!Q-O9r4R$4_e#Rkz3NNEBZFkAK(A4?@xzc)fammALqxUp%ic4QTs@?{W_GBW=2yc)4B4}Cjf#rdNGlS*zc!3wvP@e%{RvXs~U?!QW98{#uGmWoiH{HN~8J2UWwVGa|$kxZz-e6a+J(o5Bh67!Z}z}nVyHl6mLR7<*;K1V$}RNDm<P_@Vok-vcp@zGsl)W0O(c9i>`PFRiwL=Cfno1?CH}%#X1NscLW|Aa>Ud72EXFx$MI^Z^J{)0N{9Egv<_YJPdJ$rl8g|@@!SHtilNLYlSV=7FuC+4fq___bNrun)D&->u4`ir5t`~jb}Frb(rTy)MKQT?{QAl@vqkWUnMk#$i9!H@NNrZ*t51e?$k7xd-|UAij1XAjFH0a(f{A~-jVprcIoY*W4<4Y#8u#wa(#@^)nAPT<3Yh=UNRYWZiu5yrg|^$|0RlQnmN%&6x_U)$F-_M)J`(7s<TP>j`2;YnMb*RxLDx*xKHbs^I_K9kJ3NIizSlP1pnj-+&T;HZG8_eQk)y(nUVq?|Z`MIJ5|a>qHBG3yrkg3unP=akwQWl$l_E?dR;ewcr9I|r+Kd0@lDKM<%s=leiGiU6BUxVA;*#t-mV^_IsF^4)0IGdr1FKE^aNPn`Q?}DTz|uH4MK8Ut1Cp2aV}e0Vvvzi<v|E)=L2SZ%AQW^dujB6Ly;{V;wcv|);8Uy>XY1>Dya;y7o{2YVrhHqu?eM0d1Gz>90ohZFHeYri*6TFB2w1^ZL3}bncAu@s2d8meEYoCyR!`4YQlQA4-~m$JuVhpFImP+E6~H>jw@})V%;lum_v_;7h#a&|)Q?)43dI=Pk`w=)93PbROMtcL<^X0RYt?m3$wrNBN?Sw~*qSMa$`C4gMM`qjI_({@$aX7_<AQVFZJJ3%k&)?eC3&U1s|viqJP>A-Lw07R`OK5IxYDm_Jp{>_bN#BwFt&l50=}5d)ad{T&&f=_9UNyDsTI=6EAU#MA1T*2iek;PPoTy@WJ)fO)7~uczk57C8`d}I93glU)XuGQH!iTtUda*WCY3-ymH@)E(s&1n*%od?qw|^&wkAGRtiY{y3HQ_SPlL_wT~CPY$8OKcla(MA)neK+nGE%Y_75bH9Cf{bLqQQ9cFgnx1=wPoa8YKw3<)D;X1+zmq+ymUCgtzx_PC<0l<P9uW~3>qH+zFrHIC+y%Veu6(#LIRAPC-jh??1ZWtlt8MomOTkfV}nkn6J87JQzGy$8OzO%D7~7cusXqpAPjV-Xs&S72RM72dM*l#v*nS{^vro&fSb8OmoNjdj^x>sZVGq$@Cz;&jnO7L}cX{&$!-TLyOTnin+%|I`(U8e3<?4fXCxwS)<|e(`Haw}!Ifgw%}7n@Zr)Qrl>Kgl@3)Cl|X0c|DYE_TilPhkBW;-p5Lwi+OvofIa)H35Oz<8x;^JjjYF%ILCnm)lKs7Cw={{SvL%{OD(u@-TejoUI+A0e*XHLvRnh)?x^h~|Ijo%|8Q7l4GSTlJwGw2Z#5b7oMlP%9$Z6x@YY&_QTxN=!|<zY&t$Y>==?vQ_c>RUq%xxgVg_v~`qnRHo|#w>^@ugk|C2*OkN<5r5*u5%WHFcOx1MKpJFK_n@tlO%P13GdCe;1_V7SK$2C_6ZH2sZf<~0oITe)egSXbvT&=e`lO9PHAaD1!9{`|W{52a|0)5WO3fCqH#n{qvo-PJ1~2hzQl>N-Ax-^Slp{XqA<b#guZ<sY;C@qObo{`qBNl~0-Menwk2BHkt?9oOya1TSLSak9?NJZ7w;*H{*;elVL6(q{~ke);{^fBf?EMSp)M9Zcgc6HCC&^8lP&iaYL7@#D-;pN?VMB!$Ubx9h2D#chW|nL|t#Gx<yoTd*-y7lj_`LG~*j%pr+3W*4Hv3IczA6*nuDX=_wlpLDQa;qpJYg-tB<oM_!P<sW~4d;6#CLpfK$RPp*OfWd_cSPM(rZ`H2bdP<`?rQNl`5aZ_!Qmx33VJ^_TKM}M}70*urxM6(=7Sh8HHQQsFMwivv2EwXZ^w?Qc$ODYYZgm5snvXSQ@E@yH`~~lHnr+vaCVWdu<XUf7$EeQ%`ZO)>{z5uhw}5krLbj^XK*f5`Q5Cx^3x>sMN4yXP7N%b!1{{NK+edZt57(pGeHUAX6Hp0_<PjK;cAnkx1dj`X9YnRGC0^4GTW$V1rCcC_nHXw_v@NE&Lso#v3sZU-OQLTwLesqUkrO~o5@K*Q-YU<(lkPZ`jd+M0w-Nr&e}4V#umAhw`~Ur)u!E}cAnB9|Y8f#aM!#BArd4zq;qQ3+?fdUnEQ%KR+)FpUiD6Ea04pm<fcu?t?Sh=vZOH$zRsPy0!GHVy{f{>zIK3Zo_tND#^OX^;|BO0$QWm>VzYd1DjN#x+2Q8%2Ho45(M3L1OrjE~$%$?OY^9`QCH}C;HhgKY<!Yi0M7g33+zNP2dyVmd~V~ZFBvx?}g6kg;2+1`Eokb3Uz9VcNTyZO?x;k2drXotd7$yqu`5A$sUG#jQ`la_}TB1so#_MBTn^@{I({$FFd5m;sk32|1Y0eSj+);}r+04JqssE_~c3tEm)4SpULS2sRF8{0!h2r5wLDD#odL+KNa1=7*Dc;$#f@os>G%Gx}vwu<cMol<uIB8|MPB>Bg1#_81syMn2H?aHm~-WzZv=1wWoz7UR_(=i*4z|V|(o(5m+lw04u#R#7x5$qV8%$1EP6pevuo?K~Hog0Qzb5-{|%enKs*{1VtNY5ROG~;U0WVGkivi0=}o{`7A<lNmENngf;qO-jxsJ)h0@omD9x1XhEh??50z)u!L=5l-$16G^$ng1xY@NN<*^E%Khc~KWa!_0W%SbpI}u#SD9fL%VJ%-_nLgy829Ub$rnS<5x?$>k|P6<X@a7MpLx^1f2d@Af#ZJ8)fG<-vTt%ac|N8i?kKkkS^aWfNa#yJ^P%3zDVj?KtsUe%<X$Ga_n(CBpC$PsKG8TvycPkBM!gc%6+7Q_U}sSTT(%eV0ko@B4X{*KXQ;BW~351Y^wSr-G9uU$5DTH?NpxllXL-!22EG%E0(N?k^0YdB>BbUF%SQPB2D2=1*r^1osJ<_t|dR%jvj$6NshaHO+fTp!&&n8%<K7zl>^1FPl;s;lks^<p?hD5<<-v06dciC8T=G2x`0{AIE@#$pu)>%`KJU>C|#J)~(_;SM49|734Kmin~_&NhI%_fgcD}2Sj@yaJ&}}+x994PfQ-ztv%aygjb65HVI6$;=VKTe2d+LE|I2Y;=;=m%P_jV4PLo{p{Dd3GJP9B(6enue0~bUHQT8}MhUkwH*aOlFk<Thp?r@k-FQo*+5Q<w+#`-)*o0jqy2hMN^_OQ?WVnttA8Xu33V>|45(3{X@>_-@*+EfMn%csUjX<5#^eN=qz!|XvHX@^x0LlGjl4UuCF*5$UQk{(jUYd|`(U7({*=dOu$tIg*iFT;7iXDXK<rFs0QXnX7V~3x6M#*)7Wa<oMm-$G<fA3Tyqs|-Ol}|3EiM6k-Qe@#OG~AarK~n`mtVLgg{u=mvUZ!6A2Ih4~V|2F5m7hA9NQVa*z43bzqP#)EIrt*bI)^&!3g@skldAT@5XkL%@LP96>KUf73-%FgBS(j~bONzZC~GMLgypJm2<A*SMcEcUi<8V(W41E-`i&a*!dRW|DSD-WaVe9npe5j~m~BQNhRP*5@K%-Y=?YAX57uc|Ke&}z>T7Jq;W$GFx%pC-PK7P(ufT{sAP)D9yd8&w`gkx}6<jbiBYx#pnH4yM-<NC!w%Vg5AIA|g7WHYC)I?y)d`)xDpw5jfi&1e!YW*_zTXLb^$6VIKK@?!742eJBAjo*&l29VDcNs$gr;izK!z;>E08@??ToN^317eWXORH-vK`V*!r#1%NW?M@TU2{{eE(dl){VP^N2-e571Gc5h?W1kPq>7@ki<oh<Yu&Nu-(Q$a)d?Z4n8@_ZY$<42i0<_ENaJFu`W*<jp34unoE;^BU%xg@YFYNdz7$v++5Zvid)d4ETtSar)0wZSQwFj$B}${ri-J+8ESzbd(uZ!~^%(^(G!9Ts>%ODM436!6w&@jdkP;~CS_~}9VdEU@VviLZR)j$Y#^4cQ!59@36Z_P+M-6>kz=%N_FTn^F)Y8tmtgi9^U~yQiwun^J&y>q`kSu#Y`ozVXIb|QG+4brLt7|vzZ~S=ML;}ZHn$CxeLBLRtj)H4|G`3?WDl1kng>tw<S-Ws}DwETYL??gb9AgfHkHR`1?~qdKxy^4jyDmpZ2lIWh<PH#Yn);}7513=_Y{?)PTQoZw$Ws3*k}DsoHxQ)va(!@pThGn{Y=n|<J&~uR0;b`~?b`>QLtZVms82bmrb9dbbT1=)+MAn-(e66Rk3v)5r92DE&?=buoQmwC_xE1b8v`)Rvqy})Y5is{W|z(A7=j7;bD(7yd?6%N4>#&6@6?Q55sAxST&se8goqaOJZA>W1R^K_?6c59T^S~K2Y;3|h&;i4Lje6oo9|;`EfLo-0)_W$*3xjTtL+YeVp2kh{vEI)7m6p9RB!f-ZH2xLUn-Kj$5kM?i-A!w>1V`=c`2$hJQXNa9(jJXAb=1JhL!q{A&<Ezl$%~zED^@|<+-s75^vYs%FC^4pqhYR9aFE9jSHNCRK~TVN)Ni`7(FMGtjY+mj5+Xx1rpYp3Zp@k!#=3J?Qz`O{B-7_r4nZ)xY&zr4eYkXuS#*2HogWcCTs={Yv-)RSK?j(&ad&sH_mBouA;wm9m@EJg&l3$J+e%PFA8FCB$lxDKr<<`{L=E_Q0Yn(Vrok&-1heIbmmO!m)+x@kO1*yx=jO*$E+kv7`<~4SP&Kf`38GC&3=0^A8>nD(WF_+%9l#+HFJQ;W104Kr#g)zIH*Xo+X#^tP{f;lmd@=lg-KOyb{p@;*gz5gM`@B9Ern&WRiQukdhD*KJX1NnWf72r%xbF;MAFrfFb-6t#6v~o%{L1Qhpd!y&`XY3#?;|K9aPIEgGI9WM=sS3vjSKoerKHv%aJSb0BDKyID74KCjN9WtUd-_Y}XS{|HGlyHTAT2lE_IIu#CQ%lV;t%T-Z**MuCcFDg0>cZY>_m7eGjNH0B)eoTMtLwluesZ3%+CWG>m5@d@c`D*05(;z~ZT799#hg?(DaVIMK5&%qlMM76USgQwM{w*fRRCv@Kc=VW%bhhFJtXVji}TTsSugo_)a8CP;}qE}X()oP}8Z*P)MJzulQ)OgVC-7d-NQ!+L1(A>6~ktpy;Z8%cbv0q*LPj$PH?5UsCGMxM5{+`&$>}{H@-JWdZ<83Uqye|WI)r+CMp8k$G$DGjCZV^|4Lum5Z3(8^NXd1FgnPsxJIX7Vm%IaSr)9&Smvp5i(%eUPG*PCsVcq$qvq4$pK$L9a5VlyEQ@bZ_24M+{>ion;yrz)ZTDM1wkohTt_O-8$geN?o~q->*o(q*K<Fa(2D#P}@Z+Rip-jFGO5as4k|IrJPBegbU;5$4%d#}cTu8x5~^3XXU!D2rg~s!?vbm9H}Z&h;?UHFFNmE+h#ZmN~#BWG@Z#&`hcZCh9S3<W5+&UE0M_mIqLvX`WN8egwa}DjMUD7&0g~9qh9CeD;VE)#CA=fd=n_j-(=)Z8Uzh7oxHc_H^(IlwE=#jxdlgv2RweDfiKi=V*PoYCf=A{TXu{jCM+dU{B3Ucp-^~S^bcSOu@BMI#Vs55(!W$m?!XE>!UXp@3-uJMh3ce>(&C;XwVw9n4TP#Ez?zg+e-q+uu2tFf{FbgzZ`6dHO)iiW+I8;G6%?~0mLh;+_z5BsY+v_x8_Th@TM8?wsxPHLREKrj;Z&=L3?x-Zr%)Vndge#eNJJ$*U>sg-odg%q~%=a79#6eyv^~)_y6nr6BJQ(tzDb`{Ft<R;naGy`ejp|^VXUfO_|j3?##W*HVoDR9=mb0+v4aDx_e{Ia=64za7(=H=$UgQYzG5MMjn4tQqz$^eX~5ibp<C!%DEb2sHSi#SX&Z_{eqcdQy`dT9vwE?4T}3XTRe7I@Vok-c7$zLPI;tUxanoe3mbULU7vKj2@dYHUXDF|w5ad~;Y$v1)j+dP?;iXrI_|lIdO40)xglTk6OlKoH{AJuKgYigT?#OP&pTITgLsx_7}m(qx(4FZEN>kqm$E335X)Z5>2>nNc;m{}+GxRtE?N*Yr;HHF4S5-sD(rnD#_3u$!?jHqtPuv}k+L_4^p#ce=XLn94mnnGWS#qPh7cMn{PhXkN|@MILGL=Oy#mkxD%U7}Z@O-7uo1K{ob%k=(*je-8uZ8AW26`f7TT`OS!-abO=V>_OuHv+$r8Aj9!K(#z(ytglN(ScU~8?bL^jAch{{~&JeorGQ#j+>>f)`L3i!!=G>&~Kj3Xi}5@BEZxp`reuhmaB5mOM&rxo}7p;U?1^ZU4FF=rlqi{rM9lvIrD74)ll0gL|vlBj8u^gnMJ9%6$$!k2g+2eng5qM=QcNtBv5Q*AT7rJ{|$wfASaX1Jz1gjf;>XAVBsuHHKCNS$(b^MZ9uw2#pAot+k7Rxi!w9Qy9(u3E*(Qj(#v8A`M8)*ic#$BTHlZ0EAHwCwHjG3sgPz`T+0clI1>shKauG}HJZZUwuf@o5ESXe0z~HDbPIG?~!V(=a6Wj$9cYEX6(!yFV=i;hOUN-wIxx<69`#s(rPQiZ4<0|C&~%8&thc)PPpHh{TB6l2iMg9OHxa1sLs{Ora6%R%tO%;!)$1(AHlC!e;6pTEwZ`d>?1!-l2nP_c%JX7x&$!Syg;GhpWLU^&C}<4(5R{BNy5E82_w9UU|9}lLSaA$Oe0kYD@uy$RV-;n2=0whO*NQ3C@%6|HNrVYK3%C6}aL7#HYT2jP9K6>@)ds&}l$3fGfxGxX9~roegUXbZiii32I~3DI6EjG>GAACGC+VjDW$xVs{JRC;-mQyxLmE3@YH~WY>h0Epet{HE^{}xPyj&9Bj4@M?zLR_IFh-i~(P4o%c*qLpuch14!gaUC;Yan1qKIgTfci-|Usuf>7;SScZgCDs$JNYOyd~7L)4P=6BGda)D*8f+;#Tds7q|XPm3G($8Ufg!Hk>Mrg@x4`DKUPb_n%YoPGhB+@gYcaT5&#rD$j+^C7RV1TQz^O8SmrTUt&CiMS%EGuQUXRpgDJDJG2$@q>=r4F26Pk=aEE8A=Ra`~ThaU}*Fr1K0B0t8NN>!Q+8pxpv9Wy_-KUDKW-bwFEVukG>N&_nt7KNFt;PZ#CJx+$5JDWr5}UN#<s={x0(Mt#a3pImG%>h(~z*~f3<AL?bYCZw)&@*uYtJGMr8&y`4$-%gSI^?FQ+10M8l-}GO9Qs8ex9)^Los0CNCyT4#6KcI*5^VjE;<r?6ICaq}1&wYIT;jj)H7Db4DiZQ8gHP`Z-Wl8lfTtj`((pvsd`@`eI@T+VUAGBiV{6C-fIaigGqT*q^z2#@%EFMLu8ES+%E|BK=-=GcP_}?n_72nvx2Z#C4zV$q-+hN_(3{F<)CfQajMQVQlxZ7g|1AVa$mLX{UY6#G``qEaBs?K4cDN=HmMi^V9_|`n|^Y4<z`GVK5!}1mn=-M~sdLp~4%0LdJdq387d<4IZzpwg%?tAOxdiu*hX8Ys&#%cQV%f>3vGRgalt!_lTP5v>i+t=xJ#Kyv8ot>$`SVyn1Dq{U$HY21L<jC8B{LAmZ{^OUQFZ%m?wU}=s-etxKxOX11lgoX_UFw>gsq51*tl<$vaaMY(W7W3X4#lMyMUuhpGdXPOTIRL>ZUs5cgE=JW#_VLI_-Q14GgcjV?afN{HXFt1C(D3W$ouETGPSYLbE0+Ilz;sF?d_lEu9oJ{Q^oMJ00tK(U>z!LJ5{@G>nV-qly=v?M2w&JMYU2!4FtnDJhwKoFle1BBA`Nc!+H>`oQEH3w#PJ$F1@u4gjKodv9qXz2N;vx;RaYVA8X1WNLH)(3*PCZ+Ss0mjdl2z6brZBu#Qom1N3QH-2H{r!fpZQ5`}D434(-2k5Lu73=4+Ec}BcK1s0}X5(X>-TS3ZZu$=31xE|H+`&2TVfXZ+rkHC1e^X%3wcw7+dAgZD-@tStnYV*%2*#i;G#85+|k1@?1N(0(?A{Zb`qHh8))4cVu6F{*NVsJIyD$l=DNNy?{F#|eoBmAHL{QBEp|M$oD|NB2-lT>3S)TtfRGGH`}K3)%d6&*<UJKlc#{`(b+hK`#({NkHt`BX_Vvw{S;-zm8+$Z6ev`yX57uWb_ix9{Kocr$|2`ymI4eN!de45Ch+l*K-?uY)06V_%->pj%|xI_&NZM@83LAU;DfcUIrbv9<UOeDGw`E4+d!c@g25>RWoQy=x6`GPa08FslmRir|61GfYFC_96A$+dEFeM0R5)*ma>8dq!6cv?NTG!li@sFcV8^8Sn*4@Rr2Tam_8EoW=J(|F1C*2`saOsQ@d}fIR&@X%$BRz)1-m>f?X=GDq!u4SpUL*VrRM8{0!h=p|6sJM)pwL+R6!1p?W)c;#qA+4O&~yDr%BoX%?N$F@4KOlL2v6aO)sae8&Zu3)NPyK-wM@&+7<xl_u5GlV1Obj*e$@H69{r@>c1<t~?RF~Ucy7LE<dwdX2NXQ&AS6+yYit~xjT{?u!{XE}GCH`~zNbn7MD1Fmo;SIfpK*iwURUUClVjHNH*LDBl&6VzTyta5o|fGzSRwFC}P7n>FM$%4pSj<2H7YHRlnCnmY@Zbk)j<<JHihWUliFf*PwmS1=gtYcp&V3$uQ^S2U|rv4A#;up~2-Z)EBHj4M#X6BW}NGuU7<@;`r<GKUa#g!V&*SkDL#h`;|t_Ue@p;|Wfb@rELEF2+On%<5RzvU}qEOu!|L~XD{7+&Iuxn_dvin{zUvC2!TeVvuvOUo~iSTT(%eGgs|qD9R6Yd2L;Uju@3*K!<VK0g(lEcs&3p6%W_7l}`|3B2F(t<2Zo;|9YZns*FYkXhXG^Q9)?p9E=(`P11JvGem`pY3kGoN&uGfmkYD)4Z1is-JAP(Igf6%c!RGvh|h`E<9dbj^F|>A=G>Uz%zMJVih?RL5)}B<Cs`5!2rw5zNJz;om%e3x>elfs{NzAg1nAPao0*uisYR$@B^XhfM^c{j`!kW%k+m_Lh`_FP3W#8yb_+bNnoN!mukSZ*iC2%YpTR8yiBnSqublyl^YmpO1~k~x6wAJfo8<#r!ZWzojP=raG!JYR@Mw7wk{CL_qfuHw=^Q{pMk_Z;s}OK*hQji%xPhNd3HsH>uB?_j&5XG!FH=O7k@0VBiTVwRGQktkd5S=)AT9y+Q1pH12!U~lvIlKKOe^=%W?{1Wc+ufN*fEhG$G@nA#HK8(-JL`MK;M2?NDbGI|#$eDQuplKv3Am4nOydlIsG=)EUYy^O1=E-l=#-oj1NKn_o&3YhPO>)xu?HxUF!4rV4^si@w$@nD~5Nre41W=8H#TbhgWt*)^F+hmRS(@p}@Yy#K*D_#)6chdS&k>aaGGs`kPV$nARYTX#b0nXa)5_7Q9&!-ltX0<lmiYbgVS<*IN9=1ew4*%msBlgw9RwleyHjT-mDSe@=EdZmGJDU&U&CE%@?ZAKu5%D^u$XqE5j3QUU+)@fKjxRqM!YwWe5JMxDpH($!qDZSO;`jXfK;&9)^JK^T=I3A2v1s6=ssA9QQW(5x6_a$3_t@dci$8nU4MSYqjH4&IHU(?((sB<IBVpLp_Zoka^mRzX!F_-ml5CxbiL*frO2r@ppB$NPX&<8{u3OIeta2sAxrUIC9tl*NU`5F*|tX^7OV+mSGls~mG=r-FTgXo%@a&<Yd8|q)N5(1ZjTehXk4y0|wq>`esNtki7e@hwZT$oJN2_deS$kWVhDQH=U?)3IZ<6^1$9SFCc%MA+?c);wbUz;YiEc;+z3apLn|A_Uy>|J)PpvSK1%-7T@16i69rBP-+!6;M~&a_YILpQMUjDi;$2Pn68-@;=C$M!zk^olr02_$zd29{;1agKGd#|jQB!XN`<@QAQrj0%d0z3$tihCVLfydX`OT-nrfE~~3N09YIrt1TiG^)uyi9VE-%k3Ml#XHMA{PI^(R(^B;i;rkmu-ZqiIF_xzDAtw+p)T5)|8X%4B*on%D6-=QV?oeJX9G=SLG$hf<A34XE!{DQ^&c{2X277Mvo6WAv(b2(tpDeip1f8Zn>f8h7m^)iC2*wu8&NCT&cL{*!1XOPzNblwP;QF?np9R<mCE;=+Pe}z#!;{<h4?KswT5M6Da#Br)cK+#JM*6fjHx;AZb(9~4roKyg7M7t^F!MPT*+uW~y{u^lV3=o*7<tqB&0Ne4o6#`@6Y}Rk%P{ytNU9!g)K%W8*SsPUm%+GJ1^WmQE$Dg9444T-Py*Ozp@q6KOzsZ;ENc*Xg8PO5`i(Z<$HH17u44oW@7JuQ!&+C{9RS6ogcAKbU_~wzPbwas6bcG0UyCml$=%~Bkle+<sF-9KaZfyvsObF+H#I&QBesX&4{195=5M1GwuBfHy)jLg?TO_OG9g-R?snNVUMwwsXEi^TInx4Q_c|t8!9BUwNEiZ7Zm-wKJo>iqDApob4+u@5%re?-J2;|dzw?a$#g=76<Ec1sFbp5KgkYKH6r|Tv?0hHx9CJ^D5No!@LO~fyuv}X>#(V1L$VxZTChud~ahd7?tP_;m>bcg#nyC&(QEM&Bih~6r^J_eErHdNjdm^!UOKd+!u;cL%t_QrkLc_65o3WQD^5Bvtj%&<^tyw`}O@RC}7m@c4Fzq_k7KL`EcA(#J>q0-a7~46WoaJ?!$0V8F?{8*r3_e~NbY7Op)-(Q$PGZAAWdq8I8B0PdPh@8GD^rwfB<=!L74e`E0r9QFj2QAP&M741@R-&)sOniFz)?#}S!DAKgc=NURZ$itO4|@AkdK<nQI%zVQIPP>5N}OTr-Z%fr~Sgm=r=#Ir?O>oTu65hzj=N%?f&B?#X8jDW-xMNi3<DHJ94!$fYFg=al7wOZGg*#>?02jv+tWEe<`-ZjHk8Y&={NAC6aZI!9%cH;^~e4($n<kml+1mri)(lH6wn{$4sYN%E~2S#_}~_UYV0*G1VC8_7W}u%#v_;9RU`M91`P4;h|AQ_K~({M@IO73e-};op|hP^P&xks5%W8!>aWS;1(bddRooEGrkBa!ah+yP%k5+)5ROQoDw|~xv%2ua`fU9EG~_LhB`E*eRT1lE4e|@i>>Y_^*-$0@f;<mteM&&3eDQBbbU&O=&oT6<iCH5MAfd>Gr3C9BzjXX%TLbZc3Wev=Zxk);Yc1@gC#^o0y>#d*J-vcwsJI+Vo`61wh?<GAm?}!lI;(T4$_nYZ&8KJctJRqrz@+>KgqJ@M3*JVLAx~n`*ef2Wz=K!IUz&4A+8tOriWCD5XbX*I$>GuUJ``?5)ul$HyKCBNs`X-A3og;m8Aq^3%Z%!vIb;gdEHx-0$KdB4GAOh_TubvrlAVc-of!0{%D`g8J#?g>S9Sf^L0HXI(Wxax}sFZgchQ64h!VGr(o4KXH3qn<LLTdymQU9VpX9(b5YR2dQM?c92(>K*>DfytD*M@_5|&UyF6qbVdPf6&gDBNR3JFBAry6)sb3S=T#tB>$<6_2CY$P*nJ!sv8&+bEM8O)SPSeo#1d&|NW|t0<l=vlRCo>mBgWp{>TH%kd1R}xK+5E<rh&%Zn^FoANLZm5cl6bCHxDWOm@Vk^f#2_9t5U{##(4P7GXvgF4tdpziM6z{1SQ`l#?Uaa|QQsAg%J3lMB$#H&wJ<ufWuG4nid!(d)B6=CE4!a6^U7u1Ttt4*Et-}c+r?$xO9E%I)V*jv&wikb3#|M#%{}J^LWvkUSNkylgE(T|w@$LTN;#vq=1UbNh-CZjla#5@cH%G!$qp*&-;d5Z;hRyk;Ca0?KHz4O)!K3N&5>WY><Vi+pt(h;6XB<M{`edJ`u=qOR^6)C#y>wMnH#*NMy-C?jB8?KW37hX%yP=4o_9LvE?csg90XVqbh{iK!k2HXdA4c;I<sku%;6e`2(7s5c0BsnSuX>vRG?m+3!f{AVy;KZ*FK;ld$P)4wPm<0jXqIkvX7+lu;T?{y!<$1>>dL2yNZ$95x!mYuVc%c67*)}<tV(xu1^~H$0t-Enk9}seVnLJ2Vqeu*buya@GFF1aSMfV9IsN6zUC+L0w4cZBU$GQTL&sq<+T(x5YiYyM#n28q;=?0tisu_P?3bNo7of>DY5~nNlH0-oPO&tyY_gn004+X9O{kGoy_i72i1$jl%zq{7e(4_rjYBm+nQyTYgLMzt{+A&LK2C;6oD*3P;axt@pV{x1>6C`tpWPp)Y~-^xMsDv9YmOJ*l32i8;89uFFI=4Xs;>l+ILyQPSEe1ZzdnvfeY<%8XO6zQ__vOxqJe2=7u$7<BX~*-8qMbRPYp{_zek3#tWP0*q3NHLf|5SwTh^2dT~uBQNkwsh_z$VoPnJM&-w;p7IWsMv}o;<1H!pwsMKJ5SbRn5cTQ>XUrZ7+ZIbrqEyYDWK<40BJ>RRv>sS&p1)}buwECGQW9EHrkTn0a1lM$vE=$PZT*2qs_4=3{q##85=v&}NvW|(CESizCBLYkeOsMO)PBds~W|Som#no_dNnst27r|}W)oO|1+0e)Qx$>u>1Hne}{n>M=Wx~27`y0+yrS9jX#uuTe+rDj61F@~G?iYVI%s_tToabcXQ%{4F1W9sBc-RyBc$0cqo?X{;=l^bmDpn1;?$G6$$wC=d8FXr4CLb@i%B@o|5jCYDY>7K9RC!(ao~#ZA6}29n)18%&1P_tp@+%3ylN_y5zoI#(7J=H88;BsF=VYl8v3k5hA4ya&PrfA=XMji{kiJT?-9Y~dD}?0Cb)J1<JPsp_tQs(uIF1r<z}DF?8v){i3?6`LrF9S<%1?3*?>Xr5QWZb!dHmMN=BKvbYWe)!Li07VH6bEQJb_s8QSFBQZSmOfn=K)e&@zurb(QrcqadvFo{2qaN1cDp<jsQrpE_g@l{tEl9;j#FDBE6G4rT)~o{woQL&Ce3`5jUHUYPob+4>Olw?<jxoZD#oJf=9c>=ja=lkSsB7mE2f(#M+6#-mAog>Yo{$})G_I11BKBH|+&@Zg3&2fNtTW}Z1X@dpiZVvXUe2VN3Qbbd~#{(CIYhlvU?<7uswo={r}IbNNvGWPGmd1mqJ)@6IG)hYjzFDw23LRU-N0^G#g)NO8ElqMo*QlSzc)IaQ9b37u+UKdyyTVuKnHA_jwm<gFKQDW7qyL}np993|Tm7l5UkE=X8?JtW={+{Hr&ARx<L)m8EWGMcjUM6cohn&^(S|$41i*03zrso|+GTkY}o{lMT%!6LyTVw7|PV!wUc^GKRP;f10fXn8P8PG%d`RjAaat(0F(N=`v)Y$s?!=R=C=GvzIyf7F~s=+GHS(X%`{2J<mgw!%X+8-VthF@h{)}j?d=l}V<&$+7P6%~f!?JYk8XYnW{%up-LvFJ3<{}X<o$NyH*XZXezCPmC7_^szz-45$5%C<I1nR#~vu)(SIDUx)pU?47*5!C|6ZB#(Gi4<-XTjm@Fnj((w@reRv+QP~=X7|s(O910S9UEwsL_DBt-<0c#>~5z#IgsuRGS~4D{5Jl+>Ib^-t&{8NFaMbBkMA3&`OhyKt8~j`DzgS3BjRn6k8$0;PG=!@eP(5tdr#X~N3pScW&MCQBeZY!(S2mMgZY==fBnZVKVSIw_i9l;J5G<XKZ<gebGZm~z)3vas!66jV5#O}qp1C)ENXU>vfA#{UWw1~_U)bg@%Oj4e?IBaQG@2Gq9Ubzwws&z>r9ZQicVzZz-}hX`15UhL%WW^7BC+6?mCQ!(Q^d}n*F=x3}d+DPH=l_xjc2!g9*wGr#)Zz{rKcpOlxw<c`XtC&&3c2C~ZPvQ}gAZ*MvPF^7Ct7oobqUdwJ-=$#v}(ZSNJ(PJhnjdKE0+VaBu{W0+?bIOWZ(@(Ft`0==@f*CSnoHjVfFUvk7(XMMqk$v@tH`~LgSTMjm$G@mkondg5%zXW!=Sr&`u*G&r(fPx$2jQ*!e=#v3-VAAyD3}QRyhd+n>W6A%u4F>=A{rewp#$9+{p+Hx5TK%AeCgN?z_j+;=Nu0*#8<^;|A2;j+{Pa;*i1zkRxcmlb@~*x`FP%`mW!e)mwG6VL!tF5;!<00dlst<*5x4)NBXJ%US1&pUjzHEan!l*Yk@-mHq4eoo0RcY@<TwrNJW%0E12+xQd01`HtIz#ZbCQt&h$Dj8L?rV#y}DpmY=H5FE4ON~YV(}9j;I_7!^~$+CpV9w-=4(@q|ejf>o#!*y|)@*H95JCl=ijfrd4;iLK!1245rQvUl9Bn?-|_8v&!w6P7k+6(bdOE7iOC#cQ3aAz5H{<Vo-b?#%lA;=zVUkd#qOxI&*16=5v-33!;BpDqs?OnalB2T#_z}^R8@ei<q|aN|i_ctUnl5NDJm0eBni~j(wp3ST;e3!&op@yD6<8ZrS4Ga!q`4v3e+;<+^QG6377S0IDoVj^zG0t~;=@#vsxu_6uY7M(<J0u8o4K;!KOyOVWF1*G0y$2oi_r?KtsUzH(h)m!^<b6v8pYccbqL328hZ6RULo+t*o%P`5=ENh_vNrSDNkO$+cWuidoy{_cn;3}ejar^39r6RIkXb<4a-Y^qJ*{YEI|wfk;JPTr$=M=TmSkvu<NYA5=M?FSbXF|hF|f;&GS_Sq)6yFaz{f2Q>Su9kCTC4uNAsi!j1=f8{~dD9xeP-xS^X{EcXQUrJjA-o%aXY!!Lf*2}-x_XUgM|qd^(OG7(E${H@)N(i0tyO2PxC-qR<n<zmyH<+mChweq9|#p2ussmClTXHAlM1)`2lm>eJl7Fksbi`=0#*Iko1>zw4V$X5W$JJU17N{2j4scQ33{SbTv(_{o#J=BlPEF&`6&$7Y$u<C&SX^3TUqtx7VB)u_qfuHw=|-YpMk_Z;s}QQrn*@Tk3LtZtz&jYhU;kaxenhCtroId2~qqO`7OhdWD^#ZrnWF-BZT2JKnP_Ca7OId(7X*eV7d9@aZIu-=XHtu64?1>;d7*G#?97i9)w|#NK150W|>v&AoMAwkgs64eA{l|Q-*Ogb%wIbd?ez(ck=q$yzyOGl~FcX``W4wX5O96t<e&G!mz{NFyL(#Ong2sQ?D>BGxDG@I@{&Kz>iI&!(c&ZDdiI)1!)E{ZA-;tZ_zr(WYYB>Vtm%B_QDXz?RxNAcS4#m)Wr+!5o{y%*|&58u}~;$37BV9I0SPhzBgbbCit##lKE=PRz{yqsc|oi)oJ>&;d@J_FxiR|0^Tyrhq=G>NB{PFkC^Kfm=+(b)3APUE48$@SWvjfE#@(orBjlk!SyAv2gKpN!yt3%!%k95G4y9$Fg2qS;Z~UyIE3Gqv|zPbgd`sa9hG%`R@A3iQnQ2_4CgfW4C>spC>s@5Buy%Fza<yyeavM&97F+T%8>YjT+I{4UnG<OXwd1)9Ellx%&_t*PpUKkOgZjmPSku2h(T5_b>~5jRubh;Z4A22w)_sd=B8X-4(x{dSFD5(tdDC4Y)hByaVtAXm9}EX1LJ1b8XQ3DWvN);;);n38fby;NeH=NA-dDsqdw22a;+u?V_@A^A;6upLvIeZ72|&Q?Zaywk5sncWy;jDclk5{K_+E_?kNMA1=X}nE~8LcIMY6*58Xf;HVR&79H6WuZK>g^yY!sgY||^^ASJN6wis9;j~R@0vBwGyE5aaylJgD`7K~9rF|i3}d(_a!MQol`k|<Qf)@$LfZWA$JapXiUUoxNqX^orc@BQc#S3BgCePId$u9$PUyK#R9=F?3gfnzL9=To)}=TMK1f@^>@wqtLT3jpGiXanVNhmuI=@KmpvvE6|l9XZFC!{DQ^&c{2XH0cWpw*)^u6e=fI6uAQgorX1VvjgUsJ6kdc#um-aGgEnY34rGWRBs?i@8$a7T5q2GGuQ|vAqp-}Nd-*9lbg>M40*NKqCVxMnhx#!)4h!JX>V>SM!V}MKMGBKmnIb~L#trsb1G8W+~0dyEos0o&mJ-IruCb-nB^a%V+bbXhY|BIB&0(`J>00Pyi?~)MI<hRajgpW5h7a9^PG9f5s07!u+PHX>4(YP!JlP~=5a?A79e6}^L;F=CE_|ppzwapTKbN3wcP<wOi|K&3Fvd=3&oR4sy7>%Z+$7gR3vxL(N&8SeT|AqKO;`eOHrNSsX(dn$RmTv)cNenk0Fn_D3qH)SS%67_~p5=3leYF+{(+XYM`2cUma6Xl8p<TfmFt|qe>6D<`_LEldQ@Ju#7qIgas1TnhK*ql*6_*j4wAooq1@fTo?&1_F`KDyKV8SQk<oYufd85n}NgHIcxEixEFx)YkcvIb6T6LZYve|Ggcd6M;m!Tk2QAqq96uGVhL*xG?OyRFD)Mqm99h~rnYCmZEqh>XU?>K**)$F2@p>Y)Ko5f%xd&ajZy4C&@FHo<Q+?|?KJ!C#eBfPsGTLvG)6dwR=N)`c`Vbu?o_971P2vq2q)c!xH>$qPsrP23X`hZ9M13=cbcP&%sN~O%VeADH6Fphe@Hr6Q+mrHAP1S%Rw0O_t0Q3?sK$qfipZO978DLyDd(V<9I-6qm46d@-tU3GCs-s2A9<=9W(BZF{LVTTmLpf<0nifZarWBfO#JC$SbYq<3@*gv>3=xXx~87?P7*l@1D5esZ|*NGZ0DTAurF*W{AlcMEgs7kKuC8q<{a>xq$;VlG`Ev&34*<3F4-8<2-#aI`Bci{N<Og`9STE*eOkt0A2F!U!5b7rwX+$6=kX!xqG0!fM8NtvnceN7R~DohwI|*dMEaEt{q9N3cpWmmvg)i>GqrnrlYHv=noXw0gKqD3NnW3lsey;)w$+S8fk$e?k-Cok>e_#*+l6FL{j8SZ+$Z<<#7<^!(`@bbWFsGMW3lCZ8NjPv4DI#wcg#8Fgtm5zxDp&flh0mI4*N#akX6boleNvc2}@8`XH1LmzxCvYvp5i(%eUPG*PCsVcq$qvq4$pK$L9a5VlyEQ@bZ_24M+{>iomr`EP(YuGN;afw#mV3>uYUuqnH-7nUrm`Pr8gW7=~c5ikNmk!?m4l&Nz5p8{_(4ymII{Ec^u83L?z2H)VeAG`!j=IO4USEP|=4M!D%$zRnCU*TYQL%sDu_kR)_i<^Y$Fy)?|OE2$cosK>04m1fy|ns>w$YGLZn`<FKdM+%C}Q4r7g0vh(go(^WO$mTh4y&3?KSWYWgtNUn&IkfCraq{gBct)rOqn#3w3F<)5j_MMu4GptxCTZC_^Aevw2p}C8RCA@DI7Hn2ECqD3)^vMFz9&Ce`f=xo1)pXwiQL|T@2M;i`$2v=*bi%(o5>9}5&>5Zq)vlsSE#jbokUC(+DC8Am+=U`DkHvf#WTwG37(x@GEK}8h8@5(S>BJ%^2eJ2(ejMT>J|bP*Lg(1Q4&V(j<Wv(7=fpjH0ubwP4wZ1{r{_bmmW!uq)G6<>^TqqejM4&oUe&#vIss9z$^xR-P;VX=l$<ntaOhIHxm^RwTSBN1qd*a8I@^oGZhsTIeXN@<Ky_4G*jWkb+wOV$(vLARrP4d1ZG#$@l6&vumbDY>!Lok_XZiccUFpq6UYP=#M_bHHT&f6@qqA<N4J!aGdic>@_0*`tj+tJ+3OgZH1$ZqqLKh-TNf`P8S`$x9f(2W{iyJ$Si$$of65MTfnDxv<^bT1!ZZtjchLFCT(YK^m@R!esJ9LRU>szp!Y&`?8+?nOAN#WuiPwBZRKBijY3Z7zPjE0P<j5e9<2hwDIo>muIQj}&I@^w1U?7&?l2iQSsna4t;!???hlWxRKc?geN|P|5C?>Uwr*A%cHi_y3RsjNnMOhR>3aX0sl_$f}<><JPXYAb)L5Pd+$r8wvaBscb#s$m$=<L#}g$z(*4QRJU>E_nD_iA-d1<akQ<agX1MY3>Up>5igRD({k45Z!@wpIsROv5?IdjkEGyhrZ5oB*b^ppe)g=$h#}k*aF!UzOQ?c)s{Pvv`C0PxYgZeOr*>sOO3p6_#Q84Ig}=da{w2eCD%Z!d!$2RTsw0*w<)nT|!7@xYCGKYRl-d_VMiY<j-6ZSFM8i$DJiHFce@U(<^IDbU8CFOFt({!9>nP>0r~ke;Zh>-Vf(3P*earMKmmogI)B(`|?5Z)P78qSkS1Q9V+!!<y{b)up-K$8qKBO{J2*OA-VQb@eX`=YsJy}((g}#-Lewuof?T=R&L$Ap=&^{kvMkt)S`A)4T$wJ^iKj-u$CB~OpwiLYf-^&oEOV5n4s0e_)1zDxf47<%KH|47J)T4{-*+1NBbs9JCd=S6uNy`)y{<+v<%dXRT^r<7~7N+z8xG7faN8?T6A*&q5Y+hC7@)Z$}*r%q6%!ylmcW36}=)QxoR1<21!u6+|O}<xb8O1q@u{ku)A`UQrb{Gyg@$@W|TvAMx}SkgSR--uW3C5$tgq-6l93Z5-Z3l;EUNzod%Hb=*-|-A#rw*S|N?R0;~A{Gvs=sDAqXoq;~v>G(Z`^gyRUEPT1YsZ`eMdbA;ecP&cxS-MF|UCrwAONg;%hC4hkD!W?#u_$YMF4ae>sSrVeI#G{2JxYaJ<UK0Lku-b|g34!U@=~Vd<N{j6K9Bi3Lh8EBH2a*VmnkHaZP=tpagVY!f+U%uPCn4*baq1E#qRe=P3aP><S#-+Z({Dsk2E9=V<5XtEm!f*J8KlB_G>$AJXPAT^9d21WEP3xCYG&`1X>2swGZ7U*j^a}8VCW~?e#$d&_P{r{$bk>F5=zau`T0MOm6*(0fn{3M^Ol{bjKt{V^1#XV0Fe7k?V(nmJG!?%SBjSZN@rjs#p$GpOe#7BswOaSw#=Junim!6=Gp3Vb@k(lbOS&BGvS)M;|;%tbh$1|PDoM7yr4QxEp65Px*HX|AD^7;9OOAD>*&Kd@fYPXSrQ`9IWFd9VgY;h(Nqt;ST0mRAPl|iL*g6<Rm~S=)Nl0lOOv~<qg86bjqC2O0VP>GG$`M`eRNr_0dDnC%PD-@$LAjo)2v}4geZ#`oq8+Dm`5+?RPDjp)H`pjCK%OU+&>I|m91}sRt)X`=Xf7|RY5As4aVDBeg^j9o`V{pdY0plXrBKEhk_peYeCQA8(TQUFo)Lnma)1V)@wC92O)Nqv?~?~)n5P@?!JP7@|F!v<Ks4BNMF)TYr(oYnt{4VSza1&tbyZ8F815sB{B{(Uc(LzTnx~;Z{~AEHdn8J97xw%s`K~=z8n9(;tRU(t&{8FFMsXr*WcF<(_g==FXAba-Op(2#*4QKN&97eosvatxl7jB5y$l9>owL3EC*&ap7eqxc{z}O_~oacfA}`hUv8v=so!K^3AlM4fRhVx`%Nl-91-fnF|1J##DP{yq<v9}TQ`L=hrqXZv3)!yyDjR<T*z<MBgYw-T@r1~Dny4B1pfRYZdR&9S!pppi0MDW<-c<atGCc&pmo`lzyIU?{a0Csa;$=(;PqJmg9{U|5|+B&s$REcmwK~Hn``VL+RqE5YLTA`f~mVy&7XL*4h7Fo0k~m)2qx0Q4^`V^7<!l0T0ewUwy3t4w`2{6!7g<Jq?(U4W$+)1Rs4cE9aL4@10%M4z9nU}tr^yD)W-+<Fih_LLONQP2j>($*@{d9c^=(cHQQ-f&@4_n;)y7*F#QxU;278<QZ}LGSeM;7RGaVM$Z!HGp^-cS<JOL&o1WnBf?x+xeR+x3)Xi3#e@rPCh{sF}HALDL!`L7zpgkFa2C^XfA|o`6Ya2NM<Rl>mSK_Vm{5$B5!@Lrkoc+?mzy0~sKY#q!*WdrgpJ4@6WwX;L6I3%|G>m?hs0@p!GQz*({hwccIp3n87iA0G_@d@L6k^3JAp!1p%C!q(TDKto>sI-(4ub#d%a`BZjmPQrkh`WXkDf2o8FWxVS?s|2JQ(6KhJ!O5l#mW<gAu&pHR!7D$7e|9&T8v9Hr>8}51ycSfmbkfE}{}s{Fat$?_9&Hd|SjIn3Y7YrSL$t8D=F9TbCO5`i_$@kzITVc3mh_o{`%I6$(QkXXzk4%-)fT>AyfDU5F%IgocMLp?bylKL2S<Hv-EnA-B)cG$2mDB~8=_05~X3Lw)?OFY}td=HSO}axE_+w6Q*9grEZTgENP8?B+J%SRfsZlUI%?6t4zIsH~0MVyno0-YI1TAkxUoDyV-nryrhOunXwwYgcaR(OrQfF?ULtQ-*Nln0~Y27x)ozk3;8+opS%j_ZZ=GB!a0y$hqeVw__+81Jyja(ylr;WKn9B_dL?M<G9*Z=cbP>;T~`aG`U*VwpzjC<uOh<Z*fM_m+wJQ+1~P~J(pPFf5-q^<k)Gc8KR;#>)|I8BICTjiUF%l&l^07<ifj1q>P1k8K@uT7ed9%c;HyR@FH0Hwx@udKB3It!ZC*6=Mi4HHu@Tl(yol+{kF|_VZIT|`${#x%W#}`;4-<&gZX@yC#@J15RC;PrA}1KBEH6Q(~P+xBumrVap1RnVHw3P&4{QCmI%X3JQdf><GP?Oe{`&HS*oYA(qSt31rjT!uS(yYmORlS=KZ;wR^MwL)jYvB=HsZ~V9D2O_6+HczDRt!4&eO?aAiw=i|Y%6*SzD&f^5`)0G(irdd#23vIy=IGH#<?w3pLyc@v1G;x&!ioIv%H<u;n6Lcba1l%6)FGM)?fiOUgO;3b5LF93KZ4@zu8r(RI~`SNiLD41M;W%FKBDIQKOcVk^LZevmYQC~q`VWqfhrJqFd&guApP*gzF2Li`?akFLkLoOkCVAu9+=Mi2g&f6p~QHpzG<oO!A39V91&BTePDW<M>Ya6_D14B*eZ^+bb071{X81Zowy0f=KgNza`XRc;t$uMHe1fiVAg>Jm5(ro{HNL*hWL9+?FNK}nEmFiFTZkEq=wE0-!Hc|j&yH(n5-<Q~)te}`xm|DY-l|Y?S^eN=qz!|XtHX@^x0LlGnkZC!EF*5$UQk{(jUaBYKq#<o_veOhTl1(<r5_MBY^>z@RmqS=QOM#%Uj2(XN5hd3NlA-Y_JB@qd{dc1p8D-pfQwF${CRR^dp~%8jXt?2Sf~E={u@-#|`fK3xc^X>n8<^J}eWSBou56%5M;biH=#AeJ5akULj>gXdt#hcuu5b=3GbwT}41rwFfnS>gQqM4rU9k7ZHga@$PX`bag|eo(gRorj9D*^EO;NUm&*C8S**DwV`}&O<_rh46t|@w^fN`1!TR}^}TQS>=Kn#UTa^S5h=jnWy&OTVDVg2A%s;RHB8HeKx9mM9-JT)q8VSfci>;dm^-^kl>I4F+?qg25KQ#0aMZkAbrLwLSqDX>)@E%`W(kg>>5v!EsdQ^vEKTLyKmWLb=iD^ly1vEP(?>V5QO*&RdyM#_-*0}g_W2QGO^MD{LyDB$$b!?k-xnF?Uav4Tq?=W9R=GJ9!NjU{L$QT$ZDLD$jN5=7VBkju+~-B5mur4WMkaqfV1YI6Ii3o)spXzU_p-0WI+?D6|2CR0>Gh$|*CJu^!RY8Il~y)DwXn2LG_!ma1>!!>6|N#K{$rb#W+*4dW=D<k_(tnX=S@^b|>c2#A*rcN2i(vV1vGA{~7p|WtMZAc%wf!AmBc%knA<+ScQdW_)M-bR~V5kFD_WnGJbWjSmdZJq44g2Re1$UqxBA}na5f?{Hy`ueD$!v%~Or127b!Gc`c(U-+l9sn#3i`5p9irSfSxeAhLYe%2Bcr&N$<1o8iy<l~1#{G?lw+<xm8%xvqkTD2o>fVrW4UopV?L=k8dQ71hZdcYW9G=R=G$hc;A31xU!{DQ5osV}&srB6EH;Y}Ty`h5n+F5c32s%x9)VT-DJ~ozQ5R5JA9ev1B|0)tI@2WNsg!giNaD7|P&H`+NIpKODPe}z#!;{;$4?LQ@SZq<Ba#D1MR{rT)MmpN78;a5DI?9hiUEicU3yaVSnEB|6tfKe#Ue+4}FwC<@jJ#?6VlHNv&FC0{3Hhy|bJzJoNGcz0<W+9ej9w9m=gzoR1^WmQE$Dg943-H*FbA;DL=$y$H@G|aGp#}739cIg=r`JY9}8=VxQ-Dhyq&$4hHFh_cK{TV5=!*%fE77WJZVnVW{=ob=ymwgEV+AJ1(LfM7#Wi+Bd)q%AHk(n_qWf*lI&bXkvzK&(IfuOZLHU00|2{GYQsGECA%Vl%wOiVOpTrJkA#J`>FiqXq99L_*xA{N35cpxBIN8>kk4mthg`fu-OfIHVw;}dLTav4VzKfIZ<rF`9FugtnQVxMWXRDS^6bd1&%HZ4HQTTSWo*}N#h?&buTSU;-Fve%19J5~)bcNJH3Db&=(5Iphjw4x!yr3MVG@CcL}nhPCbk7u3zfmdMUBv^T%X5G{gz#*p3w2|w6-HvAKbaEd=-q6`itftq_s(EpZ^B<RN5RToU;plIWcbuxa3)o97lt)?H!keoyReirfDIt+{iySuk)j=wg5Ds7KqA)8e;bb{b<?Td|1n85v`(6)peJk(`E6T>tV?-KBDWel-kCx10vmS47t*}j&e2vta?xEK7!td^+ZSOH&;SF_SrOc6vdQ%<*uX6yB*q)gcZo?GJmLBLz?7l@TBrsseR~cDY&41MrIS6aExb9`_%cv!;(yxsR|<T`D-edeRglKb?rYNI<Y^ja((6my(yuYDiFE?JCLO}NaPEu>*7WuBKmuSNj>b<(S?L8D)YPm><&u|-dF!$=CjGNJQKnhhRe1f&JZsKh$WLiC4i~GM2$8Q@;N}ulTx?uhAeo3lq>wPKaG7pTEF^X2NlGW?LvyKc*QWj$UJTSa1$B`DxNlKJ!0{rClJK@g}mno8UT_Z3MF>2ySJyhBYv-e#P~Z!e`nk3%oF```1BQt2KkG`Su9qibAQjD-Ru38s_Sr`rn)(MG<>cfJ>m}y{ZyVyIB0oI3TYmb6lGP8?pCl*0Y2oXP$p=?8~59{-vx?q^E|mKkgRGKoT9J<)kr{q!lHSWIt%qNm&vJ60r$jH>FP^UE=i+=LLE|!fn59QaEmO6?k(o}Ob95R-QQf*AT>!DeM?>l?NHk)a4^ng&U-5s#NP4Ilc;>k)B5wc(S=N}&@fTgshSU4bH%2z25+e8Jm8iL8wWi}>&<t5N`^G91zbo#N$$JPzEe%BSxW!P2amA=e9$D;zHlqm=VfeDaputoSeI0>r;(<79+Asr+c+>?G&Mt1)5BHd!kcbAdy;Tgsp%#pVWmqCe7*lVXL+rBd{Z7ipS=zo8s<ep0c5*yHtQ6?0Zqm}mfQgMcbFIFeG_vA>WG}`3geh4UmGwlc44T(b_t^tUgnJO>jj!{6VCTdxcjVjl&KW>Jt$g!&-#o;fLpX5L&)y4@6lE)O84vcC%^NXZ0e}pgnK+4&F}5IAtRcLp?$2cYfkDzNQ!q{Au>)i%_y-UXSYOd6?$ycNcetsWXyP>o(J9ee|#pGtH|Otd;)F&t=@t7#nG)v(Ql2>wgEasbw{%fb`UM7Kkeu4=-WC!=dR-D8u?Rc<iXGT^?rg$MI2z`t=Z0?;#pUdo3yY8N<*X`TCu{a%6AXwx{uN(ZKx@GT+p9JuBr-ucfrNRA7Oz{f;G1K)w59n#w{iy3C*QQm_AD;yQpEzTW5C(Pp#A?0nbtcH7qkmb!uws?dLzGj~3O<ww4%UCCi7{`HXaYDNvRPFDW6^Bl~8_qg|IzBQ)SwW&vaz2CRCM<H&0BaRHtYkIS0L7g`*`D-<|8GbivkOIMVF7wikV){H>q=+KfbhU1QgiFbT12WUVe@vFTMyzr~vRM;F%rmvltU_ox1PpYTRABiI?WZfuc!?ri(i{Fhb5yvK6Cnkd`GsFZg$A|@-sk(f<CN}35rxzI>{rvhje*5xpTo<w$=Yep1OcH^3?XTJuQZ+=dfvV07nHcv<W!_|oIFqM>WmIIh><vQP@2q67C`-n5Sa@CLjLded2OVo`%zGPc@M(~kI_RiZ&F9jhIPyMc4uybQ@A*D}<(Ea1Wv8fM<h<LD2TWYOo-B4T4EkQdDsOn=oiCz&&72wZn&tU9yy4DIX85=l;pkYJm{T0~Eqwy1#}UHBQeY=oBj8&MNvlT#QFQkGS#H~FzDi9xopa|qAM0WTpxrSpOGl+VGhDg71kI*r7;;P3B;tvqb|I_{;l$MJr24CHLQ05Ry3sWhhFKEIgrl4|%lx>ms*T8gfF-eXsvwYAbb#nJiWusMCszx*R*N-PFBqJvpALCKYm(2MfY%_<xw7djnLU>`MSR~Z-O}oz12P3V(a{Pvn0`+8MY_7Bewce($+o&Xk<DxBw2B0`FA3?T+f*9V0p;%9_4i^1_X4XjF0UK!m)@R$j3qHY*v$1SPht9+(L^?2*~eb-2^#xV(McYjX@2!jk`WaH088Jug=3DNi-`LZN$!d1+KZV*H)WsTD3IOB3bknr#*UpwH7n7z>xt8knW?M+^I9T`>P*Kcl0$sS&*;&~$)C9-VqHNbk6V*#yn!g}%9>&`-QOp0P6(ffWR$XQViMh%AZxY3txoO9C9MI#!eBTm;B)m_zmEe9n^ULFTi|ZD^ocS|ilDF~2=o^8(%Y}Q+LwtkO-;751W38sBF+#k{r+T5LRQOLV#_(ZHil84tu%BEDGFpHl|2$`vbS5d5?^m)Tu6KGZ~r7Bc{wBM;7J@IRtcK_Gy~2HTZdISW5jM51{1A(=!m2OlY7oXBH72QKrW@`1oy%C{}0r%hJDVb!Fcv$qU1n1Qq!x@#R9o0L<VF0Q~6?8dUg|a6N<h3>dGsp7`Y8->;(WhYz_VwcA2|lcbKrih(!#B{p`=~nlDHpfAua09VriM>ZiF2z-?3lNj%Jp`57dHOcFxpas!SzsUswVQ6Xvp%P&i@iv6xsq)*<Nh2|hN5$4P>DR9+BDY1oFE`VDQ5ssr@<AWcj27m;ZjvQeO_^``p*dqctbcTdMe}yvo3kCCe>A=zG`6)V2SZ)5+SaNh@Odk9&W((@uraE5{<B~8!A-<-JqM-Ii`$mZ`qq8P%kt&FM3f1k((LIonFqPdvUE6)iwoGV43z_|sOGHaSSr|RGcZGL&csNKsQl)XdFdgVJgj}c2M<c1{D;3g)LAU5_D&13?hTzJ$d$)V>=2IYv5*Nst<+uup_YMr|rRO0Z3FTP|TNNl?W@k-fqwzgI%$PWxsB(tK!_nBuHiN!dXBx3f2ml&=IJ3ly*cWr62-$}o)X!s0Tu`~|3m)EkwaAh?a&|kFy6oSB!_uy?MnT@RK36B2|H`-X`9Gti*laL@t}M-EQgJyb;-flJ)TH^QS!0p3z6<vC8)fF*3r$m+X?JH^jtpq61(t`2GNs5b-84?a%VeuA^F3smzhx4#1y1=fDC_7WS@9R;GFcL4Pnvr_MiblDR`QRC9tqBe5DeXi#PJU_8ZLqd-wG|RwhLWHizS1b+}&Rghv?9teEas%Ww{2p`gbjY^KBoWe;6e8KwoRLf~VW#PE{cJ(aSkiC380QPDrfjT=f_C55r%D?hwPMqwD0PevbFiR~15|>}b5b<!4|o?y0a5s%6$`lN!Z0&;J7-p~wGP5Z?I47EZ84r$io?`Ua?hgrlZtm4vpN<46Hctxw&&a|Hv1N>hQc502X^b5&r*M;EVQ>Cp_-MH~>|69x3NM#3)zD&PJt!MJDbqcj=WB``qezM0Pv*<4K#av)u+{?6kg_-_3BiZAHCw@$8yzx=hgUw>ae%zyo|z6it2+6Pv(XuNnUIJ{rh*D2DVry|MW9WR>yc{F5qMS#nJS&b)swSTTHx*W(q{PNS!KYW|$FSlYbUs}A$kP}c8J*X%r&d_gCmFI|EAC6&-u0T63VLaRy_2P9?T((psOY4rwZtJ)+KaHF9$Z-Z{m-HXA=#^r%k^OF86nWM+D^+Z+d`cd4D@|zx#wj6gIn}28{U7h|zrqRt@F*Gz3Zn%uxG(`LRI01d>UCRosW-c{xsGb0{amrA7UB}VIk+5yKU#-^>8OBV=9E!01Hung+hZ7dm)BcAgjLGwzO$&L3~1Bfwh5Fueyk~j0a~o$7tHA}+MZ+8^DXI|Va>39qdq>+hrxC%L|S*Xj~+EA{P^vZYI3w{wv)!7S)6gjQ(j<U`U&hv8UA^_^7`iQ&Y_aoX!JK&$m>eU#@i)s?KrxL3;r$$b`Z6ck$4TVXyTiHOetrG$4m@00KD+{`we0imP;A>I18dLDnrA#wlO3?t`lN#CEhB}zeCe^C>%kq@4Nld!oU6b(?5Uw*Vo_w$Dd(oS!J)=s9aUEcr=WD>KzP=D8ItL<NcpsemUQwXn~Ju4l?4(423K`OGtqGoiYQ1nAZ8?uZ{k7tNd68!T<H;%kS^T<MevS0iBtl5TXaKP9Bui{vRa$p9Dja#Nv^3_dE#;iD|+)PUK^KubKD^$=q3OJzwD&d;uRkLx}>fU=ngfo2d9LE!W<;hFAHvh(R#lTSkyegR-$<>r&%h-*FNqva3?Tt~2ddxp*HaA{q*DRR`%|s_oQWrAf4`LB?u7`!+r4<7xghCNhC#mM~UfX&UNy7Ps3300$+rsgM8l+47?x2S0X`>wOfVjrAcTBr2$DvN@z<H@C?c19^9xymDm4xFQ4JT^B!#v0H3S<Ig*#tPMm;j?VV0_SM)A&o0;nboI3>w~%kB!I79dg@ICV+Cn9-)SC^zz>kP~96Dcr7lkbKy$KLLnzf)662+by7A?^OWoNm-vpP4@<pKSX&K*Yuxii64?tZEnSA!;_RU%*B%OAWv#)77)&}&vIAm4+cw!h_3doHoU@|Xd($j#mo(L_~x*27OGM8<i46<JpE<IR7RT6mZ8r*WZTjekMP{6eUh84n!G7hVKQ-}V%+(<hYqYYEp-*3_CMWKCzs2bZS+MUSa}b8L_UaB7hBVXBQ6LyED0$cVyZKHtSSD&_f6zk&)vN}Z^dwTX?zu^CHWNS3Cz<G^qE!U2$7nnEI92xk(n$F?gZq%MDStniGhr?W67s`&*HE2ghX-*evd=LB*IV*&M5AUM2=sI}yERB*6#%Nixn_vZPgStUMQ2k?HqIt@cpg~jLCJJvwR74va?(ZZ?I_a5`7u`FWa=fgJIwSewdHRqA3#znlQahnsUezM#~lT_$8qnwgy99IcnXPyi9iOUgO;3b5LF93KZ4@xYpr(RI~`SNj`QkdKU$YnCl4oD@s8|#vB8;kOf`U>(&HpN{lO;3_{PR9>~q5`5m5IEk8n{Af|gAtPl_5!>Nj=pSdBrs9pOGWN#>?Sn0HofX5o~D?(-mPu$(hUqXrN1Flw^0|Ufnr3UYBqI4gMt(;l&)rF$uMHe1fiVAg>Jm5(&qnsNL*hWL9^eL#E9W4@5)Ix^lp~Vb+q|dy*IK&VY`(O_%1KMsoRqk6tfCbYZ$VUr*n!vV_YT*BsMHi8&XONrK)ekG03!>C+6c@7v&XLj+RPDTb%4PMT^v<O|nGY)KR@1gpAk_7SB>3C@f=#pL;~fb%JDQe9BJao_PP=$n@25<4qY^Q<_*kZH4v=m%QP|*$J8|)K)U+Yt@2@&*y1qwcB8ZjP#Apb~y<fHqns=r#vBFnh%H+q!|!xrlNMQM(Z5vuxl;L%1nyf3qv5+bKuwJfYkHnV;AiGv5h=3-qQiZM4_x{?jS5zJcnS+WK)!FS++RHeD=*Y_rBVs#=S6Br)!FyDPWxD!Pe>$@K($=BM?LF!gq6xB2erz`(T}h^@CffroP4&CpqWAOKd*PQ=@WMh3iXV4|s?BHuIJzdvQD%r3x;Xn$gU1v&^OwVliK`6xb?{mV6vX!&&5~Sx^&!DdXAAErU8&vMff%6*&#a*l)@`^*;Kt><*#;BV|bZ0S7_GsF^$^02=fG5p%2HY3-g-rUIC9tl*N!`5F*|%wAemV+mSG6hGB(&~>y`3ehz;<nnT0H<aIEDFp67Jgrlc-$`AFN##ppU$&IHiQ~9;VlqV~gt%fN8#%M2pk^Vu-P<CKi>au0Al!Pe?u#eDm9wMN|I2C9q?T#x>`Os8Tzm)C_p~*+-GUmssxn_wrwn9iNTf!YGX<kiSvb=+qz~Od!asVv(04%a3KEW=_(4%0+uLZ<E8<7Wbz_lIIqLXS@R&hcC%diSup$gH=r!dKVL=-e6cb2i!=r`{7jTyNOk?{JuP~Q(^ks3C2LOvBryTy2tu6>_+(3V8N1wPTG^gwfd%>vGX)0=n@coU4w+<xm8%xvqlpovC)V(3$8X%2z+lk7G^_W62+^(E#I6Re!X-J@xKXUdyhrvhBIv?+l3hqzX1`zyoZ>V6tc9z@$f=*K&b?yPPkBuc61Y?VO=ea1}Tms<H0aY6a!h5+sxW29DsR1^^oN#K9r=$X=;mOVW3!1!GY*C+bQgnw_{^?pqI@+rniqYyi%8x=_-=sVXi_i*~`RIzQqWAY+)`bHw%(F*~ylMSnE@nc`=oo?t`K_UI*ZD$7Dj#m-Rc`Ohm`f3f=gzoR1^WmQE$Dg9T&W2}FbA;DL=$y$H@G|aGp#}739cIg=r`JY9}8=VxQ-Dhyq&$4_Ha#QcK{TV5=yqm#nJMK;z@I=HhaY8xUa*PX35>-Dv;d8z{r@iGvY+Q6xA7?3Y033jK^vaK!^szO#Mfb``jy(J8W4j5ytrCv9SvhuV>%pr%Tm9HUUo^Q?HYS3!H&8_e(>T9#qXSdQK)-l`p`#&w(fGAz`hl@HL2H*xFV7>Efp&4xI~eR)UK?S=PXATRc^Yv$XOxSTJETa9G`EExr=h0&sqfFTQbfYjqX<rRz|}b}X!DBNKFAW4kX3VsIp;F!w+sDKq_2^WjkHN+e=RODbIU_AxqRru56MaZgBqcrx9lfycd9k|m7h96T%t3xNCvdpnJOc`<KreOJ+-S<A}Lh1_fA0F%cut?N!z8b@%@EUkE@DI=Gu<@pJDdkkSvRXXm*yD|1%#6Ofyz0p#b23r;SbFas~i^`pq(_1D1ImoECc!Ef}Iugc#ij=sih`jl3LE(^<ax{9%5zCl5JjjD;*<`RtR{zMQx?$D>7Kz_k=fbq-Qak`!A~nulxtxhVoeZmwhR?R^iKqYJQ0uCE+KmKq5(b=mU(HFgZl6wU=d4k&iswA@qp`WP_``DbNeJnR#vBbElT;;DmgZKnO~GR?8B11Xd_ww~N<Pi=<VrrV5*-Rdg>_oSVIMK5kH#AmM76USgQwP|w*fRRCv@EaM`t#-hF<AsXVji}Sy0Asgo_)a9v5<OqE=R&)vBj<ZEuoKJ)XVE<ap5ST`$S=Q!+I0(A+wkkx1}JZ8(zGv8S&7r@CB7*3^$`8IEmoe-G?rHk)Q?w<jBUpN+|u_hkUDniyK^>F=1M%?WMo8gV5!geIRop&a%`!;nSFER(g(xd~H{R)2v^yB8mh;y`dN-+B|AGg}AoR5VUP?+w?F&Hq=)W<ng`=`Rf%kQ~tY0$+BYs)XvN1XU1JqJ*F|Y3&-;QPDD!dF}0!E+Y+wAsDP8#(Np(cGfXtjC5{{^Z$6|&~sS$3Dg-x7-tt1OCZ;76ujCYIO4USD1xc0MzQHSzs>+SSHn!#%+WYIktB3j#sHU)wKU8_GpQPw$j2;^JK?<gH1CKhRKwJt_b)FFjuaG`n=<b42{de--5tzck;QZ1dNlwdv78pLR=3`M=Fqfj!O6EP;2EJBw020mOi%>^zT<Es^dKA6`-n+8Z;f$@&mRPk4t!K|rJwkTxcN~EsAMha_K<u}zOeM;jus0(%{C`udkem&vPA3)`OCq6Skl}~Zm^MfaOFViG^lnywYIg9h^e0T(X9D09>K55h_9UQ8D;wf&(0>9Cgupk4qzHAZ+m0<<K2L0dBkN^3zg~7CPctd5=PFvvi_oGH0PEys|dVw^y}~c?aRaASJZ@^$H(z8X{N%7>uMj#k~gRJtLo8^3Cym(*PASIU<KB(*F}A7?+r3?@2nIJCy)s$h_@rXYxabxUqE=sqgzVIIkJDRmd9JlWNqG4hR_(AH1$ZqqLKh-TNf`P8S~!YIbA`X_oKq2Vg=tT|0z4X1$McoEUW2N%Ci7?2c4hHC2NX_+0v(jdg~wn#zA%}?DAp0!MFJNu|G?Zc+FQt<?FhZmaa+qBrrJVa%2$5@tm?M9ah&lJ93Gmub`zHTn?YWKrFu{r})QHr$vOsrIJMt4W%G{Ovw?HCSgKROllWT-+cCL64eK+0t5t$vM7cWR2A(jPllz-(QzZs*t;cy5EtQ-C6FoM-g>!>3zqxQ*`-wr8KA}*&~A;=&8>Cs)#{!Km^)R;@3=dPWZ}R<+q5gG2AyOXNWCX)tq!=DhI5ej1o|m?kKB1V0ZeN_A+bTwHPd$@Rn^$PDzp3WeDQr|@dovu>PH{@wjje%&lNE$EW`90KKMfQWFs;8%xA-dxd;=gE{vJ6uhH7NgpkT`r4g&tmeFPH<Js-WpSdKiS_SiuJ4<3<D8NXjSJs;7a%NnXeomBviJXbj!KQWpHn3W~AI@8#r~r0~Xjm8ryXb}Y<%8s@{g^1Rpiw(JRO+qDyC61UMU+J~noGa=ajzCaa_y($9r*Cpilg<V-=74#WhK-*H4?q7+`4%~*MM9jaqR4=MeVE_5bI^=p9HL6EipcsAe+_JqJrHxFP332L92)Hm9#W+CwPFA_bvD=0&8ykPX(}!_Dz&_Bx5-#bo;WZoeMc=8K@VlG}MSOwkaokJ2)Ny%S(W@=;i=I`%589K*>gxWk8)o71)|71;`L8dPPcd)iP`ilAw0EpW^^=-EEplMUjzVcjYLhw4r)<gMJ{)D2MEfO7D~hZ*ity(|QP!Q-~la$Pk$&R*+M`7qgi<4ItssnZdV0;_M=|LK=AmR`LI5$n{21ta0>7?f4OCfHHsy#}PW6u)DY4uzf)12*I16Ze$s|adAmbnvP<VLI@*E00GT~IqVwoQRti-j@>)5Bt%__M+-}Et6jpqB>dB0wG}B60@Jb6sq!O~7TNbX*fNm}EuQlaBoQ1nO~9_82oF03sWBY1*-NcXLe@9q)Fn(rnehx2QiV~n=#;;w--x0NdZQG^smzEkMfGMgNQLug99c-tFbO|8+_H99^4>$#%-$>0*l4t8A}WF$#iiWA&`-AglxN`Vfp2b+10QN7l$vq#^M4*IF`2aj%e1KHEjv#ciP6dBfs^e4AorQtL#;k{bZ>pG6fOUi&cH~D(@7JVRCEedO<>?`nK#`uFDlZ_v(@M7>c<u727df!!Zmlt8-5Mxa$T03kfM@#L3Ny3+N%3?H!65PJ~`Pr$a7HE(T8*5FUn=IBt)QdT+GYF0`}~qsUCW<T&RFR7<$=<#5oSCnlH+z-{|X?CU;#&tJH!U*WF(OO0srnP`-Wp=(1b`-0Gv2Q~0)z&p#ZdS;IsKQ5G>e^;VKGk6zBH+Jm#Hcivh}Fsi?}e;EEMTi*t)7~22O@jm*hf>e|njJLP^4D7`{2Q@<VEXN<wJpT_41wH=Pf}X`Uws44H4z2GkV|6*K*J^kULhLGOS1b~$zW^}YeFX#MEgPD~$8E%rzNDMhf^~H?19g$Iyfolg1IL$K?6<#5WE^I^h8-HX7@%|C%;$(~u3iB-kgl~<=kXDIH~xLa7j)lSC)dMY{@UBGzpo#bzkXRi37^Oy;niw%(HHTXSxvxb^2Q6>+Dk_R=T57GJWS>iL{~l(sXcNhKb2V4c76>Bf4m>@Km793&p&)yI$v&*Lf@a`F}ThofBn|r5CAUjj0zU?>1dFAM*Z#2pZ@vdzrOy3KmM%popl55d$;~)=xI6BfJ#44?$J>l6s7%dr9s5$o*~}Q&$DXN(Smc@C@Jawt$L7(@3<+|epdQ00RCc9%P0KtaK|Sk9?#XasHx<*u`)gNg=hOhdJRq>>abPs%8E|W@Ab!TeVrsx?452evQh&rWYs)<&mDhncjabH{D@y=_$hxs=YRjl`}?n-gRyqGyVr-bvJe=p7C0K)yNnS}%K_x{;=et(u2oE^p@GrSuZ`wYN}S~-^o^s5(~~tR!PS>zWdy%Ovrh=Ej~r|3?E2bA?L9Za$DT|SN#>YJ{klNIk!S@4;|Ly1kAzh8PomJ=b5*D3*6Pc`)VSd1fXg-GN+K2o>u-EQHX9_0b_TPz3-!H8lS^_EC_U@f-EKCm`2i+D_}vl-3HDppBDn!J9IdAE6MGfnA3wskzF`pA+y-M8`h<be99l-xRP@oZkbR;02ACPJ*Tq(5s`hrol$pq><yp%-oA@qJLb+n|ZnIs8e7>>kB^0i)c=v$mUi^VmCF`zBG{DTr%&IW79x4)~QxR-jvCwZ@L&ynYBOd0(Kq9)d3MsSHsIc@C1vcYJDn!TF5PdG9Dv=aFCCdmnZspOQz8xzLoer%(Jp8-h+9I&sjY?r|KKv;8!mquoi!WNh`;-?spxRB|{c`;AIU`ZPOlWhr+ws>IVma6kPpC%HWA_%M?+D|dA5e-SM70-*beNcSk+%iKQ943015g-2#S?4<OGg*By!i6tAm!e|7Ad`&uX|f}S6_(66xKKfgy5m;o=^fZ?^x0ZK0-s+ze4+`ekPmZdyq^jh?(HoIdnsVek=Loxd(ITUI2#uP4~qX#gZ@Qo6ASF6&+!N^IBJw1MPPvGw?@S=kK)Mb?N{stVJTFLm^aE1Aol$o;-<fj&-~m#Z@d(W+ZF1tymRccsAGG9iKMrF>IQss%^2SmYNN@)Gb#W@>~LU=)3$2mQ8OR=ET0Y^+fk79aD!}H*1m=Pa=qfhF;}p=<gF_MJ4exuY5SCFqh2%r&n$WRrok);Uh$O80~SBsDS&v9r{_NG0JE9OCoN+q0`yWCE*YIx`2G>Wm3d9Z8a(6DXL{Gnt@Y2PT)55e$+!_id4w&+k=KTbuXQNShARz_@L~D&TtQd6c%(91QS*ZW^$8`WFZt}XP<*`omnrW8y>?^!=PAn7E>Hp36jtvGpeI#9yLO*Dv!y-{HFZdhhegpCUbM~E5OCj9j%%hSq}}V4Dc-$86FKx)c$jAdM>B=7>{3UBa{~(kHmxA|1cOXob~>oCEaYRiMYFXq7Syirtr)3iyGsQy#e<qyCW<2)U9B}7=Td{lYu{4HcG2Gtr=MFIJ(gD1m*KE9ecX~l46ZOtqFLQMgiM6B(y&H#_`vrEhJg2yh06!Y@{$g5gUuz!xizC&sYk2GuaEk-bcwr8!roKQq4%H9?2n!0zqpQU+<LZyEUv(KZ+j{qO6(l8QsUu(9yVg+-!Oc3*SLE=4XZ!m@^FH?t6<jMDWh~o4S8{I=u+vr`{!u-yFL*{WIF7qfJAe#GY%^6Yv7Ode4)08lR!xyI(PydBB<;Cf_RbnWlm8##IA2+G$W1cnJ*T2Kacd>&tpHcS%$mXXMMHufb8xd{~cGt}c6ANi?zNG!V<9_abQLmTxB&y=L{mEHjjNZBM&>;R!iJZs{m+rJvvb`Q?{`qC#}LKM64B=RbNecbKzt|E=%>2Y(y%v8Kd7{sZ*A(57azD_4(SH=Ho}+#B*oRYSP{4f+=ZG`qEkeP6rN4<VA#D<oqcY``9Yx_q+9<Djk)sz#Ns(DokZIfIhJ&p|91v_gr?>$pBS7&s)Hwd06Xg^Idgm*k>tBdfBCu{NElhj~r_bRSLq`<E}jVuC;3`$Po|72=5kEXb!1PUXd(HOh51JSL%!LXf1YFYehuN$X|8+T7%-9Ue6<4m58*b(Iu_fJ**a0i4qNR0p-1RzHXnK{4#1Z%tXz7B8{L+t|DeX;pvRtEF>``jMS(z4(xr>Vx4cLrAZKWp_X^`)e4ADORz4F4R_wFX~OdjQOI7wl9*Uxj|`1b!Tqpm`@1`1$vO7#Os)bWndd;LKPj<18A9B{UApdH+cm@rAp#HL}ZRGEs3;(;*v^=DaDJx>lZv2qm<HO$K)K)05srAK3(=NLH9l1UCU-O3Wz%`I6+Z{{1xQzLK@?Gw=aq%E{hUHCZ+gyKC7jgeRAh72CrO-aAXv2ap$<<JQI{;+eWU)wST5!{HYxk1E8rTx(;>^>^-hlFeRkeP7ts+qrcJsY@FLTa?uh6M=?`DgblmwqwER70H_zZY#lUCp02>r>e+X`QCDh!lSN^(Q&R0B0qbIuGr7<$XkA@f;rc+?tzZ2~KrfFtI8jX||CG+f(eBMx6|N4gL|nou+qoBujR6?@dr!EC)@K@{P1=#MU5!#KutLU!znmqPma5&+`v<L1hXJ|uwrfP)ObT>?mZ{AhD<-*t{x-Ppf695#)RX$mbLlE}S4Q9LMw0JvlgZ+#b7^4h_>3rO<i{2kyVDxQL56K^So5IW>_$_2zL+R5xY}8y2G$VdYbmL_KwQ{bDG+IqeHgZ7eB9xboIIs%%aDW+7PY>NG<0R^jNK%j_>!<&4^Z$)<eHp*D)wi)6)+}W=dkLMomcE8a&L~eD&9Z3v)Ew=ptRKuV|2^vg;i~_u^*mYunXwwYgcYr8d;TZ(&Q(tkO)!3F<sPE8vK5Y#bN(24xKM|K>gis@1-q3SPrKATjD)8EV`cf(J9Rndy(gcv=y(E>yLAH994Nc6&XY_@}#s1exBP2J+79u&F%S!4aR~XW)}*B@I~P-=p<3LvhJ~7u$X{mZzy#kj9{U&-Tk9F1aqoO$9aF1hgnk@Pm^!W3Jh94dQ+xiiO5lG^gdyitQTGcOW*bs0L#WBez3<csbPzJZ`Q1(&UALXg=HPGddJYEeN;kX53eSNBXdf~9=(`cnH+n<n6~FFa+;}ML4Jbo#fIUKZ()3v-!|t_%V{NJkrrf^W`g3(WX?VGCiA#1%;!Ejw)V0_`SD_?(u)RtiM}fRdQFue1id_WQ;~qWc4AbJ4t`@kj!IxpK~_Qjy?MTAbXKEgu1nPcNDMO62uU~2vEPh>NrXB*jxQzZe_Gt-5q96$a^vU2Hrlq!?pLNZjS!|D3#<)1$dyYJ4H@}MpMO(wW<Qs{dav!-=fZvBaynM<5<<yAs*_?nusbiP{(SlDsZ0n928ihfV9tM@TJFX=|H;wr(bj@v7E0o-y#!;Zs5yD(bo@Xlv{35<f!G*@&2C7F_y_h<g*@jGUWlTqJ#t?w!c3jBf-3ChPNsP{l_$}&>a(#I$<+0(JEfP0W2h<p4H-G8+F}^kNk5K4clLJhos$`Z2F=Q%FSpoxOwQv%H{MhUjD9{O5X-%4HjzpdqKi~)g1!4Py_;P{Atjp#KX_&%*ls1xZ<m+f)a^-6%GtJ{fD!rBM(%yYWuic01BS2g!4cQxPlJ?*@Ht+2{b6w5N5rW~L)zkG2iFg+s&+|ZbyLUDrt88rGlb+WL*>u?+#^b^6C^|9Q+6tZANc$4_HJ-?YOYlTZqUM>dfEzk21>2C@jCN_JRW$&@`|d+qCP&KCnMSo?hK~%z~1O=mpkHNK}QtJl_q}KeUk`?Br6f~Vx~fEfhagP)#IUDiO|nS36<-EZ9NBmZ4OA8`zT}UeYW@h*be2lQvt+8p{yyW&M%%rLTZoCVA?NQGN|)!HeI71rQu*29%6N<<`f7{HHv0WMUj2Ip?EY)Y=vpfF<KFQSG-1f_8Y}Mvk%tgR7~P`KUEl$4ez@sHlK<Lcy(Mn0#pUAFNr-!qeWf5brC0d29?J{qh^lsKUUvu<B`_j5S}mPiw5706d{36P%h{|B*i}S(=4coz?AXq=9WR7YoRoqaRunBj{T<GQ}3fM%kCfwFj9uZAH-VKfN&wt>!Lv)5ODwo9hJh<+W9=<_ZSwb!-YC@P2_wHh(TsABPrTeT8ZPvdo*pdInL;s8*+I$R@}$bX!!a#cR*491y5pdJA|^T_=<>YWsRF1cOdH6iOH;M=8C!QXF!_ecTmkjbh}r>PxqOzrINwAFP;DuVV!dCExD@e-M4l2rN9(Gz7y+vlCHug`SCMx8zee4jFd>I3NSNAp|WtMM2XKkyU$}EOZpCwKG^8a4;~ctv0Wtc8NDKYq+B-^snMmDlm(9&v~{xE3Jxp6AOmgih_IlI3W~XA)Zu}I>NekF3RV4u3KFXcEOTi`Ul!Mu%dcpQyYIlO`gi6kNT#hFeIhlgQak~N+2!g5t7}Wy7{FZ#6JZ%T-@_h(%j{_C-jHw&kVfKM0yeDkm_jk!uDm@tJe7%QNT8EHataq|iNQzDIv?-Qa)7DLZ<an!yF%sUiXwM_pwnc_wa)`)Z}e`v5sWSB9ev1>+m*)3yQ&QY;k{fRT(|*;foxwNO`U!38huJCU>cs>z9#I^<i%o(`jnHRJGAmo*D})4UfocPR@YH}6zcjWt)*FnR=~_hS2o+RM(#ZZ7{LmRnqi(jV)jN?8;|i69)Wnu;`05uldv15U_%lHE8s`}Fse5Itu?My!9GGn3r|@@K4~uy!5qLo6HV03-QezEqOlQWSnlYLpY^VRRd*-X^<_0Eyq&!s<z{awyA!IT`SL!nA}5L`&8gb#u^O`BwfNF3xqA@tF;yFlj7d8qPV`Gro#ClKsq)}nqz0ZoyYi#SNe5wUf+d3U=*8qIK6(0xk9}LuzRgdUs)1|*p1L|BEoZKofi(9^LzdnV)Jd>I7|*djkNUOE6Wvcq;bOcxRRChxJGECin)=00M;tmA=CK49d$O#7-L`nD6lZDWYp`I#X5g^8&suyXt_9%y8ee?l=$0fQAQ_m8XgK<SB3^_QZDfM(Yi##LK@5(>6stqCNXksV)O<LUx)O<)$6Gj(<KB<a88f9{c8z;N0))96aw$31tKN4AL~jRzZc&4B_R2=vY4ppBd4ub_iU!SE#&RxvDKiIHi^Xz6j1N30K=W4twnd1%fFcY%YUlPC!l0_~i@Y^@#DX8H$U0mK+I}!r!v%(^%2JKfTP6WH$f&k>f=IeLbyllfi>klM{Mk7a4p}Kjqo*9PEaa6dL+;453oMd^DJ#_tvmUTW{LVTTrahP90nieuarVmPO#JC&Sba3Sro0nJW>3A<HrHXnS_Ej-LqGSvnv-VTKAqT3!A9ljaXvKWA@7vplot2%3m~K`8gn#wOj4CpS(;nPHU*EpWGwmEr!D0l10<j3d2%J6ScwjWp~5;X<FJny)JNkD3ZmNCjKOpN5CEVBfX3y7t{dR!%;wh6E1RZ_+7mAeBK68pQV?j|kscRvaH3XLoz<$Rc5QExPd%Q!$>ey@?OiX)^HVZ3@X*{kn~_NHNNqTh*RiLr{-?TJNY>PkY8j4ga(@r(WHy^-X}2dEd7q6I@9zA>&{|J_#~f{zMf{%wR3okghtTA+CzQk9Xc)3cnPsxJIX7Vn(&~(95&o<tJ{-k?;9S1-COBu7c!cv}RN}~;ynbx{ze+X};s8&7Y1n||fX)~Avinperuy%R{Zp<7Y3&-;QPDD!dF`L|PhzxKa>K-DpUE+tSIG`Q`Z4GK@yem+Fh#OZ1`)>DMa2@xwHpPmb_kAmE!<;WSHYe;W1XK<Pj>2-&Dp81!_`hC2_2R(GDuOiG-17aUNtb0k3mug$B66=Ze0qm{=9#Aad4!d7}=S|JwAbkt+Ts>*(<Vmj=3dSj!kGeEnux~z5UFgY1e|2Z&$!GLN#dZka(G(3Iu$|;YR2|Hmdg#lXTu1;}V}g2p}E!sBZL5pSOhfVO_~u((NJno_t~H$K8FO>05W36S2Jo-&0v4_J#cAU_UHrZYDR_NIbZ5Aaxp4JD*zG!YS8~h|&)V_f=1VUzHJGIo~te<`X%nNNwWyst<N{0MlT3+Z)p#?*>H6BQC32s7#MGAp(w)FgR{?{YA}a&Mj$H5qRn7*Wdr!mxsfzs0lldkK<#~OobEI)jpCXZ%*x3)uSO3n4RFvL)_#TBMZumEYO_y1{t|`R*Hrb$OIL{+mYTi`{eKOfbft<x0H~xa1Q@m9&ag=wRxX2dmTfQrXDF+R1)B9>*7TuW8Uqz1Ez#rj|z{96@0J!r|j?+*yX-v4gl_lPO|`b2c4hHC2NX_+0v(jdh0MRafa+v*yY1~gKzQkV}F(+@tUuQ%GY%*EnSoJ2@WQO92o?1Jg2Nmht;7^Fqb&`3R=3s<?sm%#PVBmihn$HT0}@(Dp~Z<PzvJ5lpH~65+)SIq;~Q2&1cUhQGLKFKtQl4i(*JYRnflkWLUZ!9XIlfy;~v(aS=XQ0+|x-t(V)lV7VWiU0St}0cxxP?bayW+*<cut?sFSxl@(=j=Q5s77i@5O}mn6&`Fko)O*6#>VS)BI0t!8pr4ZW$eouHz_b<=5*q|vGkqsgRgL|tGP@7Y7vE<VZ&3fKe)O?#3o;z_ToI$fGEBeWgD+H1HWHK1d^Sv&i!h<;!k8KR8m+BM2&oKL8nH@k8C}*sp531OnM>lTRWSd!vm^$F0*qvOWvz)WXU1je=R_%($eAb|Y+Cnk1FO~h;k*Tk3Sg&*hJ|ski(YtNK1iP0kBJfs8nv@SrQWK%3t|&iL|Ig$x%8VK_i7;|*M2JAfe&x3I9gx&{YkJ}Rzkf~Bhkyst(!M=4ahYT$IhNw)Xu5_v0jG$Nx%x$662EzvRQ2{D%g$lVi^V#w0am{NlPPlf(J->--6E~u;#}9Q~>K}-$ZFgGM1A<w=b*OxsZdFfqJn@LyZ_?n{vXpgX00PyaZT_ZVn){zZ9|rlx$R42GmJZfvuTRfDECcSEM9YEyLCz32K-7ISvrl-KLpT6d4(ISB_Fj8>)vl=m)}#a>&l8^iFy37H9f3t%o2vg$ROz43Sx41vv$LF`KE=01_UZ8GI`w&Ms0bq>)!(75{&RTyGS`8b_bhjvtW*C<B;q9HG+*yL<Z$+Xr-x5WETMMwYP~7nkIu=_ocSgfOxM5YSwh!>$n@h0eL**u5i5Le!Obw6FxX+9lje!aogGTah9mFdaLcDnCMLk$s<oEfdMm;yM3762Vc^1ndfm@UUZ$8pA=Gz0~R?WPLMEUBX0^8P8B5RTw3UPWgNKjVQ{XH%eig%8d9@RBtweR5*{uk%i<8lklU%Eo+A*?>$7#?7cFLjYfMWq9VvqT*@5`{bbuuc?QlN_~sTl@S#>hsTnsv|L3t1lUXaUOpAKnvh$RY7@b@mIN2Tma-XR^)ar9b_txi1(ehvE42+~Woive2MW;a31P0EQdDBhvq9WZqTYavseq51m;KzR^TyuB4;n$EZ*Ja5GDJq#4RL7~Mt-4=#qk{M2larl;JO^bReK;rnqFg3RLIgU;#k@=`V9!39>Y*3Qg$f9Sp_hF~oa3OX`J#;ajlO<qa@TdVN-el?-TgJ7Bx{ET<=eN9F3UB*tv+fwg>U=#{KH|IHB5vMWf7xOZzUP?=;fTMJvf_s=dINQqxy^chvBcX^=;6Kq5c0H@1w6ONJY89czeswz+T*QP$N{&a{Lj^^Z(#b(BpqC=vjPY3x^oy(E8poR+qzit%m0y#IBNd#Ui2l3jo92S1?fCvY}~w+(r!POS)+-SXW0gP!}o7O9PHIaD2(de*3#b#$m>5*r9=o0Xp~1e2&QG>J^X!=~_#59v{JX<KI_&LHE6Nay|Uzuf6^H`}$%1>zDPD@QDl(UadwKeG$Kz)dY+tZ@jRry>v8i?zB3{!(=W&bmc>l+9P-JQ;B75=hu+%$NLfg!!JMm{KL1U^W`Qf^!+&=gX>K4*KZ9D0pQ}!s9-^#jt0qR)ZhO6>7PIT>+4_m<IgJJSvTOmck6$Ko|Z!msPyyX9v#&|QQH4j8bqA#8R8B7JgYVxEjXu*l9KM<st2j~j+;{LXQdAV;4db%e8L|OcYH$P@myVtno5ovE7Mb7c(yO3*Wd)A4qNrEtmqW|UVr@7*GUq^-s$!tD>cwUR?XA*-0}BzS8mqCkN8!FpYr!}{`Y^pzyJC<7;BfidwobN3xUyUfupg#%NX&r96(Ml{@a7=TE&DK8W<h@+Gswd#93ZK-#D5$Jz0|yTzxrKM(|5C`-IT?$g#H0uCIO6-g6Ut?8!utWR9uSuM0FBiB?cBj^M%cNJvHhBnr(vS9N-Bt-dTwjSGGbxLh-?Bw|sp{>CR{vq7S0XE1xaP~V$0xg;ln(zAZu?Pk-OA7B!M-z|}lV83-Ok{e*d(P}C`u~#Af@gsce8wQchZ7_DBPZ$`@p=C5pMIS8-*%zvBfSCb%U2J8hYHvqOnTecQp0&)giSGg>lq)vxHrs{B=Nr3TLg5;VcMq8E#UD6TvhKP>1I&!ftO`Txp&~&#6~V?83;nh=gq$EY;$dD4B%({JkTOe+3QIpxU^AYiLUfD`(dQzn5=rq>vW$S^Rvzu?+p*%%>CpPa!@mozEdtx!s1)Yr!;g|L{MyU9_@V{8PkE68s@>$>FUKFBGZF>Ngf@4(9e;fxmV^E9glZ%`c5gxYjxY}T0i`HHRC|#~hlyzyd0S8%r6VLW0EH1$Ji$h=baY|Mi!VP8QtmBmk<zRAy0>+A^@V6mVU1%z2p+ob2_+!&jwOxYBQ$jVE3|*=XR;~22g#&@m<gVpLpL<&w~{}edoYLY1z_0UbYE;yEctT2xqMVx(GfN{uXRN^(0*q!1Anx2{!Z&%rw*{fS|n0B6hc)s@W%}A$&>izSjVeTT*VS)MzU7hid6xIXLIe{@oB>z!={O<+7^3iso9WA-Ezet&n0k&zRSO0+4R<7PV9SIPjs)+F?G0gvnE;bB!Wn2=v9t}{ys5QR1#0~%7=3bbJ-kldgX>tg^z<4K0=g-(H=L63b^mvp`TS6qkN{nB;xiPI-Lz&68^BS3&@9FCPjSHR+B=WqFTnH893GB1a3p`M?EyANQL~qJ!p7S_tN=?C5xGf56W)n4EHcdVL?|xFk!V|CO7Fw7D7RG_BjaGne{@t;V~RF42nf(F~xzEAPFrpqdJP_Q6u!K@|Zl#Z_2-Y7$$pZGB+2$0$dE;(W<$T_0W*Y0N-Mf;nBcE?LXJ1=W?2l@%Y6yLV5A=NIb~>4};;tS?>>8(#^J-h`Wm?`d~Y33cpOhs4))N8*q=ZJF;?5-3nHW0T?AQ8Tg}RqqLgSnt}C>qYFJxP(BaSv9}8#Db@(ont)en6tIm$LhF-n9DhyPLXySGE7WkvMhfE-v9YK<ToG^ijHRGAlf3}!eUx0Z@v@L6)r^GdksP8Z5VU6T^-h_-Tf++Vqxdl)%9;tE(S7U;9gUmE&8F9|@Evqxer8C4Im0mSzPETo1n;cBsr$F5(~B^E>RrP4&9RHqKcihb+BD=z?72og0WZL-_dI#0@frHP`xT>^2dwE~@~uLjX&MM`Ts45Bod$J*m%u=7fRFdOzN|-cmqfL3M!r1y8XVQkhxKUX>axd`L=$^X1F<}MFM@V%`F2v#YgP};GDC^i_O#m<o{&T2mW~2f`uY8zUw%0#Dnz&YlK^vm{-YOjhdDd<-wH2q@V7x9YfAj%KS19LZE8lla`pIi!wHkmy&->8HH7=$pnpL?vs;VU_q99y5F#19LNeyT2J8{2%O{&W4(b}AYE=0OZSQfOGblOy9K@1AE0nmrj_Z?yfkVPsJB~<IsHppONiNzpvMQ?>Ytxx}nCApQ_tDh9fBEt&CivsMPgKxQA)Y9}f_(bmR9@^^qg-dhV-or(1WBs;;+_qZv|c8x%}uV_;Zft_K=bBPS4mL_sN}B|z$v{?bx^Bm^@BJO6vH0+)|3@(@e+%?jm^uDR`tidS~|C=AKB^Fiw}vZJ{Z0-g!DRCb_W!*zlNchVinuxLT$D9qTck&m@kTG`yyGI8<cibcjk7E`IMkgpa&UBypCyD2DWh~RM9~_fR?${4{~&IlUE>AswD11MCRzyl1M8kE~%uLQoIPfe!+t=N+~UNOwIufKm)Gi(`Ek>bl>ycwQM${fVk6w6BK30UqKEpq%p2{`=VIlvM5nxQi^})vs$XzCwKm0@XDnKM@Hcmca9s*GeJqVZRCnv`)4Y~pW0C|0Ge8&>tOf5-s5ToQ$mXE1Oa<9`YR2<#<`6n7cEh66f+e>*s#k!%AOz$fO>(;)<NUs=?WaJo_*&Vb)^P4Srj%qCDkqxur4+^lMCH~*44EYt`C&m`qiHV^zw*<6V+t$Pw8A7?cRJ<;p)&z#3ih<oqMs^7=W?A_k@dReWo$mq#YUC)hNXRD`ZUg%UN=1soEXAf6xkb7?4|UyGGQ_q(B#FncCd3Vv-x^Z-e{(r<?~(J*m$;m#$)WW%SK%B>4_EnJk_<mj>33&xoQ%er#c}JFQV1WZ340H4oa&ZZx&$i-`h*tDQw^U=2aOmXf*)#D%Su0+ANkhhbaB#~n_|$y3_4|F20x+ny9no)z(fx{rh(r1i2GhCB1W`)*e=Dw44<J40Wkd>z8$U@U45!MOQ8!yoeVuUjNzKejBAC%IX9O!8>#BpO>kWWb}FgBl6N&#})awtyyqzh!wZ#SK~-8Sl^;jTOq+@7=hqP5O*JWI$(LmM)L|<`y?mZy}1$c>Z8Vdv>?LiB{)8#|%Sz&V2ifgAuQoBC`Ck-{|w4D%BZ_x<QX=?t=~NrThezTuCDxof+)Ql!5rv$uE3P*9&?WZDe0mX)vovTFIryb7WFe!J3(xYfXzKpq?ytF|BygkiN|MaMzB@@njnG61(+FUO~#+oYcm-)Pn#^e|1H7&_brQJSYjK%6rD5BC%0ehmo9#9G6nuh(~d^MRuB;AW2AIjcQST=q<nMxP=!siN13eTv2tHlYg>+;Tp{_Ms9e;dZe2I<wjy^4i(3~7;ucE;@5C4nSLADXd*v0jce}c&}4Uro!z0DEBqpS29I-t>}?VW3b7&3oCU}Bk>bpEM}5XohE-fT4+io~J2CAW`ZzW_GpVwi29I7Vx%}#RDehLv;}K;(jqmfZ39myK27E8$qLu5ojKvQtSGC47Wa@0-CKc9E)1-<f{y76uW0rPCF;)PsO}#qk9E7}<`Y<XgFdr@KjoUIVfdSri5Rj=;*FS{bUgz&RT0SaxpA6eWvp|fOsLG;&JL$!E_F}U2njqfhPK@@;0Bd8m)&@E_44)YRY9TkZ_)R)VO_~NB5rz>^@r-&6AFWKlmlR#Saa-Hx*D4ul8{-6^PewkWjt|}q|Cytadurt>d$_cUQP{A#Yh0)B0Y*V~ux#YJBjl8fx~h^mQ-HCeoQEti2#oWPN8)M3=Nm8Pg6Vlot<*$P1BQPwm!bO2U{I&V#R~!_`uZ}cRiJgM1OlIx#A3y-)&j7ky|EVenM>S5=xQborq!+IpcV6Ki+3@z6j~J*<CS3Ir4Ws}4}Fdmzyf?m$~f;fBL)0Pu4bL>L*2TvqAtrh__RoWAvCe{Zh%`U2ytEsFTjY^xz6W1#vs;I<rh%-9hZc&0U*{?a!_$(KIgvq?0_BJ8=vy21M^pxF<v$bHF=MPijLM!4Xp)o7=Up^G$P?!FIeYb8_)7W`FvxDb}NFEe0u0~1?a$%5e9m=G9J5?cpkAF6r75%;j8^d25$@;a1igP#Ji7e&*MER2x&zTAe@wF2CVuJ;!;(AQBRBe-d=XU_~Pb}UUEAFR>+gcDNJOpT|*+Xn4oueAwiW7n&i9x9nkVVQJp}M7jgwigp7(_X-eg}oYq0ZcaLNK<4^w;uViO0aDH1b@GSmVN1J$#cJE{72wS^-mvH8#1m$-E$`>_!VkNdn%o*m%k%v6nL9-@h!Ho|7BzU9TzxeUDFTYYL?tZdo<3fbG%9qUNbS!>x2|5>yZ6qZ38Rh9{qf}_65k^f?Y<*Z!z>lw<ExCGH7Cz5nMQZ5eZME+9F$Kn*JmVD3|L)#y?A5V#wuFLL+g5MZIyWG4_L=geu_(#ASMfhoPHsVmlv!21OKmj*gfLr1#6`Pl&j<fh;&e<cY9%;1l+eT6pJBfRC3PEHuqubth0)hUl~sK@Y@9zE!&Sq};Hm<*D(d+dm?mXkO}$<Y<rEU$@`c+qBU$$qwAezNpCkrRAx5}IT!ruB7sbMqj<oW)W%9Q&;f~{c7FX#a{c(HBw@Paft3w)qNXEGC31vs~F_&<QY8&ZY-RUjywaPlzm;rcihOgJXPmHtWi%cHf;Vbf8l~L`9E4O~TaTwKqWcc2s<39Q&Km48Mb0&BIBNLL(R;*~(d*3qyFaHRpet7!AAU6S`?X#_0#JTmfw!^F(X46zqgXzR9@})k7j}MY-j;@9pGxtmN%GK^hBfC=6vlK|EvV4YylRDcrQQ#q)AQb#TuOO_%I=~Q|Gf!ER+1FJdH_{@n9*`C-X}-$TbvaX9!cr=5uPr<h2y|=ak}A6E8-Z`9uD6i|1|~CgsYbg&BS@Dq>hyRqeRO;|J3hQ@BZ*Couq<W$#aR819o+XNI?k(}f4!5tsPv&bLG7s<#lGaQP_1hGD2_D<+>BN|I`5IoU+dyWNbBHCsS|<VZf7D#u>otLaw-}`5cKaoG=7m3sjx?SbxPYgsyTJb(a^v&jld#Cz^7Q@<H6=?5tnoKV0mgFR(Bwv4*3J5v!?~XlXG7u`Cc{%TZ2^ix7Kvu2~(W9reZG!BT^L2cWfumm&Y6Y8{)bIL%-qv$F6?Uu**p2FBB8;QmOewY<z3sbo}ugEYzV&iynlzsi+9|*{$^<LQ28yD30cjjt+eN9lw34H`*Uxe*WQ)FV(lnhCQYCuiyQ)jLJ`boCEt>AsPF&v>pN4UYDI;lr(%#t*gnqe~`I|o{){xrzeHQ9uC~^am0<!NsEbOh(OxnL(nZv?uTcyCR0&558@goSVOkB>u05Cj#E)iUq=`Oll=skATQStCa0S2ps~wqWg&>WU{*y;Rk2N@;kASl2EO+T9db+f3$%M{p|Fd56R94pFE|>AAC27eN-HQ`=T|gd!8d^;#}c<wQ5aA3SMcDHm3t%FN<=vbw6XtQ+pb|ft2O4zG5GqO)8zX*+>{ZlD6qaRD}+H<b(6F=qq|q=ZDW^p`t`WFJZvf|>@DFeW)1AL$^a4Vv7cY7vqiN!8B-s^r6zf@e1ETJ=az(4Vn*e|rb#OWz`!W@8e*KiS>0^{4}Vr1LQmmrVj)WU?mf>n6s7-UC-L+lRkTpYHa#t(8*_i{ZN#`JOaPzvGCaZN&aP~(uk=Q&GQ3sHqKWuGE0hGR07u@Dp4?)r#Fwqxp9+Bi5(LEr9sBMxk}`k?%8#yVn(gS+nA<0y@;PiE*z|RbN--1fh6!P{k27vNyE;9sdhOV9(zREA!3rp@XK|@^P-9cPTwLK!7BXLd@c~z<bao+ccJyfZk4C0S)q_MKx(iP+q~5I4wrg)bi}ju1i)cvT`zLNaZ%@^+!*Xq=Bv=)`v!Xyh$~!u<w{)gPy*$l+aIV4z8>r&Bxt6Y>kiE`zFivQWCjt%b&|EIyK_o>XBJN;<qsGLgo7m&iGUVBYiFU@^Nk*t@G_{%v9S5_DH(UP9s)T~NqFgVgT=_1^mvN3-vf@W+pMk~Y`$r*)s$a!Nw}bguJDP0hJOui7H7E?t9mOWVt1??bJtbrxY<8WglU8jC2KpJe%z1e~qxNv4xFr(XXs!)^rY3V*{EAYam9Nnz8`Ti%oYR_ddHihGJ)umubXKu19DiB<eJ;7RZ!Jp(4;EEM16X+xTe(f}cUluQEF$y8Q6t5wOC8DU=$E(qn*ySpL2k+y8s-bGs_?ze(>Y61Zqe}<jZY8eE)zEowTVbHA-U%4wEt8frW|gSJuSIxIJOIw2vGYGyNt3ze@B|go2;XqYqDaVw7VYt#<WOH%5|Z%6E`c=BaYhyQldbQhnyW-yKlu+9Mid*&evQaG(pI(1vTqU^nJk}HB}vh%J*sOUV)nR-wQR{6xc7L{{(Cn|AuA~>nCOP8BxbcT0lo7S`;wiA}f@?!n=PodVET>q<%O?IVI}1rY$w6ZSor$7X&jr!Fh2-*9~azEH*_9<s^V1!s!v3lf;6dmKTM^S%vgNogL%y&ww@v2Z6&$uaLW+3dskR65~QcSenNYzn7#fu*|kZfEbK0z|Q$AHkED;H^`pyBVx!%yp>ET;PP;i+v3~<g+7EQ7NS5A5jZeU0zOCeB<u=gC#O^$K){V58E*t=chR|B)rkrz)|$nkL=SC{FH$0N&!#<7>Y1i?iP9Kyy^xK9LW(_Clo<iMh%EIU>XjgC%=i4o0lIZxcyrq!=E>x-GcQKP!7g8H9a-k)cvGq!w+36T;9isJ4~~im8!W}K19(7mlNE9gfTj^!h|v5HEOiSZD2~-I<081k*8pK!I4OFU*SeW-3RatCJOdm^tov~8q;(IqmTRdPXh1!pjXq1E2(S^ju*EI5m^J-*gBwrg4EQ>m3uy>cw}&>+q^`+SM#`c~wceR?ryOHdqaJ_GfGpz+`<9FpneUyNUV&u|Q4!>etx4ui;pmR{L{hi$`(jxi{pwZl?n%^AxtV8lmg=*u&jsm>XdmX|i;D(<`54nWl|sPYYt^Pbo|yBnG=meir#j^-Q!iCkC06X&x@>zoyJ%}sgw$~K0d*u=cFyGBISMM4vlrWQCtH0_eFw099(J1~Na=f=)7pG~F*oElFQFlk`nix>U<r$d8y+3>v~G+7<{I*z3u%J-jHcL9j3q{Dx)h?1YgOk$Za|$-lz@_Yemx<iX=)=w2lAuWW3F&pSakvxPqUBN(ZI=%#1bYKaw-_BC~9gZS%Sbi0$?)|wk7KV=oRy*o=*%%5!tAKjbbWAg28RiZull)o|#Y5whE5?<`-Q*yQqn@1+D0V=f-|^U{9=dn)9_YO|dSji9*j(j)3~9R$#)D9t!XkXyyv$q-p_IQcRFr2yVs5@xh5X4GE7Lz7s8@Y0s-QC}f+Zwg7yVgC!pZW&BZ4o%b#yYCbzK*|~1!9!oR#S^spfDCXv+U6*NQ+=)b>Ro~u*v>}K8ro}Fo{^W8UK{{9=GIOajYwG+N&z36z0aQd9N9AtWJfS{H?fY4Z0^Eq#i><9e?UqxO+jCM3;6`d_xiAZ>NtYX07SaZ_n}}OK&r(AW0^(z;beKzSXgEBDteoNc+&@<a{RDRJHy@Ot_ehxZyb|XpHTo_g>HHdOXl@eb1IMWZgktP^a~rN<o>@@_nS6tQyl6yj{R_hb;^>A-L7*a%cqVN3nRJ7DbAHZ8)vRa<njaMhXp9ZQsP=As@;t8%AmaTGo^KIuLM<a9$6Jxzlk?^(oCIpuZvK?eTyPYA&#1)bMYZ<gpl{yWL{E62s$`6+*#=J`C*)&2TZ{_91{(*4tyvUS59&Gk&^K_qKVMO7D<#mN*nZiwu!wirGT733mY;eeG*cp+esw3%5}KFM6$?`q3Xjkbj__&PAod+{Pr_w-g?t!`z`zyDd10&~jk*8Mg-(D>O?cpmfE(2fWr6^#h?pMni+W8ki28npXuy$0d@ygw4Aps^K0j2h?~jij@H55j29NEG)oWi~TUkGOX%m;bwU~f{4gt29GFY4oO#u*&wg}HKOVC8Yz_X>(5d-uh<2A3HO(<^SqnPTWX?rsosvlkJ&26R7EOp}vLn>5>U=r@qevjvNEc6VV?TC9R5LWiKp;8pV`*9r`cch@h5{-MN&mv@i3tFU}xAmN!DZvMAQU(-hP@kdfEm{*YJ2R*2{DfsuS`*P9OpOhC{XAdQs}M|P@22lX8!MF#f+}o?sZ%t}(mWhOWXAYq3UORo@x`^Y`TXQ<1XbU0v_k1WAtcAxW2=0oP`+0!r4<z^^RU|m5BDT^xcOp-@;SyNwwf%O-?>;pJz1560$fTIbWU1$(rhP3jb-$9ZjepZXo%+!l-Y!<(C}VyT7JF)w=q!{3sz05pQ?ypLSY^k<=7@?oi$a(81JAro~vl?)a)-aTFj7|w5Tw(v4DsII@@9&b|UQe{VlF;$h*?`Vn~LlaM)I7QPz<%yG9A6$^zk4_;s{=^H*LTA7hJ*!R-93K3cvjwt(`5!riG0VI&`d*KKE&I_JG>JL2Gh>k&N=0LWk*1x??*70)j9iDg!%u8v<8oDI<etHbcNtij_0p7n5W3s>b8>e+P=G1Z3wqnV(i<zwpQ7O<;*p&vVoB}Jn_UnYN@vHM%VDi1oP6(g@Wz>O_JLGnVMK^${%e-vKe6^Hp@x!fEgo-`tB=;dP6LPv>O_=ZEB^Au?68#wuz+gDpb-A=;EL&MZ5OUz=(X%z&&UX&eau?fb-yczCl&UpmjiWYU?%jopgSOARdWIOJ=?PQ<y?-jH`xNjr^xX^j7zay5-JzcSMUEaa`vaI@NV8Ny9eHu2x<``ze0l^s0i%d&~bWdXxYB>8p_%(J^tI<+167<WY;mK0yOVGx%po^&Pzk*gc<dDIon|wJQ|KUZXQMCDGP;i^Z372lp*eTG3)`%B!gOpqTWpi|FfvLy)`vacrHrBz5xC|PwTb{Udt9?B)?Tn-~1W}JS6vmI1Z@!ql2>zJ{zwZsf7|Urs=(*nRXP?ABZV(bHU&YekqK-4`Q9`_&OW3YKka9ouoj;rG6`zs)XNUtg67jp$=a_Bv9`oFZVBDki@l%QZo?{|QuP_nN*!;$9vNURO2LVs|4`g{z<6sCaaE=?=uK;r39vtj8@z<}fVl9CjLKy~+PPW7|WU;=E$<BvYZ#+(J@!m5{t7{04Qd#Z$uU``P-}$F&0IR8RE|FU{0oSU2wpxj6@+9S0%fo8I+&@lEm;c5UiFiZDE*l2vU`cy;L66IH+0BzlVX*0wJ99mIxl5mtRXq;seb-cmkYjwhCOIG796H}=KGwv*KZGGfQjM3c#G!xs{jJED;%>~m^(;F*6Zxxo#&fW1$8)Tt`bC@wmM0a*zL`yJ{SPHDxEuaXCFVDbt>qm;2hVioj^R_2>zQIj-sgOJUBUG75>n(c%x>1wM}WBXbEcAdc?HZ#lM&0XG>8d;$0>C(;D!w*GMwtw>Pt+$8+>rndcvZqdHwKa_uk)4lqb@MOe@umnrS2HA58x>kf5WNyQ^U$($`GHhjyg^BW#?$kgK%COn7<|?YWpnW%3Sc#JUi%1P^ReL=b?TnM*EDEI8UfxSJzq;w1M6M66u6&FtiTg^jivG<^!Od=`2gS!i3hvZhAaQKrpEu~0S$JQxz8`q81;_l`H^`+4;p2fQ+{^L-&LP2z?=lIg<`g1>mnl`7mzkvN=?)Y>#@HgxII8uE4<=k4rKA}!>-@l513o&I@X)UX-aZTU53cdifuDtX!f!Cowl7b(Z7?#SHk;^iPWt?OW)A4ze}9C_1_o(Lfk@@_Q?|D5lXk$$1_$>=o<PlVLwD`43V(Q!e&(UKAl&UozUM440<r3YjEz@%%58eLEoCSj2BFzZu;u_k^8$n+gs-}pK1Wchld_Pm<KxpC{W{p%Z%1?BoY6iikA<_-Wx_+1M1Q<Sx+^jxX-uOrbd${_;t>SdCQ7!QB^+@91`o2p)u`Km=RJv9ZW?zl|ql~KS}Cb|`T%b*Gl!9QhL(hG{R0a=2#E8zIo-}v~?gcR?F!W@s&f-6kgN7nJvn83I3={I_nMS?3IpPVA@FE}ke24$7x&D(q4mBltvx1K*^G_m!OH#}~p&sX6aEF^+pyeuKI-8Rmb(bW#*W4k}>uyg&;7lFIKKv&N{Sq#dzZy#MATO2;1t<TZrZ~OTC!{9g;qK(YxPj~9A<Z&OpoSWo-?}m5v#ZiB8|1kVjw)q`eF|_}m<9+niPdzxMOKm#5_iXD}wsd>mgQ?bh8Ts+Q7F12Xv0dRQe~1$7lRA-opeSqK<&8P(Ml<r-eFfjYuxJ!j-UuAGQE|mZ>|rganMX5J4W#1NG2RzMIi;rhOdsI1f<z3^xo_rkM7DOlqEEZdYnXl<AHjE@6EY7DV|;Qw{N=B`{rda*Vf*Ws^^>rjy8h{>lkojCCq>H#$>Y#3Y-=wa4V*j8<9(RSMG|!t)m*EN(FJ}zyUPOZuW{dx_apv?Uw-=ehi^;g%kAMaG~L|KgKMe!*KZ9Df%-*Ke5ZySL7$EW$!FBx{`~2mKmP0MU-;wCz?cH=-TI%Qr{z!w&HX&NM@Mx~gyL-P&lTqOvy@*uT5wJq#ToA3st2j~j+^1{XJsSGWUdIF^l-<EM=r?T_se8gswzEkqRYyYR!2(~J%OmhL>&cE!D?s-{9b?jR$r8$f$8Sjx1Eb@p)RklyyuR;r~FzoP89ko!%zA9Isf}V-rs-y9E`Qg-Mv1fm4(2xAYQ-rE|bHkTFqIx_Jy)4@mXNCb9Jghx`6ftPGmbDC`Z=%6>iqjf+kLFJ|K??8+7%hDFo=3@F<GCcHZc*w$83xxhg9D*pph3$O&iBiMKAWcz|#k&^U$?FY(Yvp}B1ND9^1`z4%ZT>|Qo;A8@&5;){~J&ILcUUwsSIXlK;thasRybrY}oDo`5TufFp*cc%=gWyQNC@=5GV?NC!Nu-<Sy2h2;c!_i`yzkcf*29eEeFm_?44~*u}GMdgFv0N|vLaUP%gVZh~_o>vfp)a1uspVPATmtwm;4>*V@1{_eIt;FtP`Jk8-2<k3@dr++euKXY`C0%oBQvYQ(0ZsykX}bqWeN%m(bf=hg4l?Mc`=ZPF0E~E9~G8<qQGW6Nrg(Jr5{x%l57Do(#oSf{R_118IdCV!^6J|t}O!F-Kb)-s-nhBX-!_3{Jvr)b<Naq8d$GR*$bE@qqM$`$k3sdyWNhzjw66iHx(mRvpv^zIZBfYD@1@7iFBBl_P)~M#L0<}%m9>WEVg7S#<L5XO(-c|!XJZ_dkb4yQPq6i+q%1kdR}b`8^@shWav8A`_80{vg#5$r*VwX(Dg5}vn!s-CUukuZe^aGgVxsrco|pwN<5fhs2&Xao9@f#E?W6=7Bn}+^=TRWDZRoef!yy*X5f#u&fjUh>(l`z$VP(EL$}!8X>|oLc@l@^tC>+$p2oFi9#c?dw9N2WRgT1hf=1O|qr)J#EplGMHsq2wuFoZK2dxRm${<0wK_u~I96$6b9aD!}H*1omJT#7khF;}peEYMyebftugwj{4!qAUxrQoeYsKUpgmr)U-JdF0ZNmRgn-wuU38EV$_9U^YOq0`yWB_Zkjx`2G>Wl{u2-XPYoDdZ`tC6~CUQ$0@LHuQefLt~0m$nUF{hBtMg=mpx%lEvWBOtTw0!#xa&<tB^LY&m5b)9Ea2F_J^ymVFMwb*2fDZg>nw4a3l&BpFwRS`{>zQ5{9|sP+%?qlg~n(y)0LCVOcz%LiZKR}9_Js=1N%(2&Xi-(r#B(ZI#mQHLv=2@D6su?HUPCe?I#Bp&4chhc3|DTPvo^=gUg3*0CAU>l;>$9t;MpU*@BZhE8L(N^i=R<L3Wz$l5yz#lCuG?l>pslC>bS2tPcd4lqJn2x<&07<b%AfZ%`SQxMsN=R_yu#u4WIvuoRtXn7=k&P6_C!W5r8qFkQDd^2)F93TVB^PbHETqL2BcXaEhbRgJtyz2t*g6)LmIS#FIf~*7l_1*4O!!QF2wUT3EdWGfbVl(zLcqo$1<o(SD6gAOHNl1m-dTTB_is<97h(L=yM*zZv=z2~M!R&hX~>h<bB%feUVvBcdGb!<GxU4+D@HR9SkuEa*-kUhG!3a}m}&q=JLimj1E&h|SF0ggU1B((xl5wjSV?|GpT!lhp~Ep~<?6D>m9jp2P6O?CdM|=@ZuxdnjXPEk%rZlX*Y>pA7anMh(qNauxp#KW`#-<@a!^#LuIEXBIY0l=i=yhZ{;lu=2Y;K&^`U=&zW4bT5QJ=1t{%T`IAQX+H=G-)hHz0h^e+f#ro=yu?({>5Wb_Kjm<JoMN1!gBZ1Ol@rd~#umnV9h=L|{?KL@d7&{_{hHLgz%1`Y}5sl~u76o9&XtS-q#+eTJp6=Q80xDRv2M(CrdfB*93S4{B7d!HCJqe47UfCc&V!Ku91vqrhjVTmnroUWIsq<jvufs)qCgteK!@$B7|#DV6`r>>Hs5Kzfq08`R%UUbk96CK2fpcwYh3#_bYi<g-4ArqG&t?G|^wRCP#Kgc(L#fKEsfh#(~^sa+tcR(@wYZ!_tR<V7K2fog<)d~hjQ^zMvwNqatOLK$Lj_S_b&M}|zuGp6c8A`m4Px?ncM#}-kY)}uN#V^A`4{ZlGc?CkHO5#35WR5N^iL`>^l1hpx#f!k}7d#lFl+t3y<Q&idG~ma#rPsd%-S>QVEt}0Ks1N-*IG}E7w^xwEmz~`0i(-k(qC}BNDgIrHZ#F9hzxP58gB0ONB!h#_x#o>^aLKlfT#;-4OvU(9J1Pc1Q%iIm>>k*AT&-YANU;stVQ)r%r2*JDw{hg6B?^vWrh*6?cG*YS6NCX!FHpOT7vtpV3LLGTebXg%r3N@z6gE30)h-gSE;c!n3*Ca&)wLC_W0~FhwaNL)2u^PA*<^oAYy*pD^HqhbLn{%Nu*!CBZ)0Ns#{S-YH34v@G1{aZ8Qaw;#R4m2O!&)La%rjB9ld|h3UwHen_}KV6&45R0xeUUJ623`1O07q-~W{J;Cpt+r>ap<7j$LxO`jzB&NYyz^LT9S_>3sHifZ&Occ(RqgACi;u;xL#*^Q?5d@)gAa1-_-Y;bRulDZ4Tg{}1sMm(pHrjI+El7pu-c9PGjW{%P;J-trlP;{g$#$I_t(xeh)o`-16sP!r1(ui?XRjgD?45>wv3JUmn?i%vg=G9kX1}cK%w6{1w$m@bU>%i<0LEOkZ=ipk5^ZuN;>yte9CS!;7XnUEN$QqJ=O3lBH{WmVXtH@e0G0}YkW;@1QNWDhn@vt^qlTT-d6ABR^5nj=1AMP95lAV(e8wc#@-uRT>U$|RCS3oM39}_;0)=mwr1+=2NxP{f)K)nycF8pY-N~v6ZooTyOHH!?w0Q-Op{?UOYL$E|Hj?O_!XO2s+gbkMf3G*SxbVj1VrS*xO$I<zg<H`83NT$F^iDtmU*@)U#{Y5=3X1p>kyANV9t)0f50htCw8!@T@9oNoQU4dqozSVccmLgg?fvM)v@;-s`(7GCO1xP4?l81HC^0}PWL6@yRj`@#2{a3t_oxRZLW*UNS<2u>_JlegFog-0i`!3;WIVqq=d}+rb7a~?-%WK^bp^mip*$$eu?hV}N;7>AR^Sc#GRMOl}_G}Oj<r76%7ayc!1}xTNi?iI~V^>zX(Fo(_IvS_%_F^j8>e-U3r)A-D<$mc}2U@+`#}sotHTmy!p(PI4^P1Q?n~LHAV8lX$d)gDMly;zp)Re*m7IsL9e%Zzw>>^4EI#=ekr00WwD%I`6H(3i?kV<(A6>Zq>PV{?hvAHG_<Jw$nw7NbWHm-;g!&Sq};Hm<*D)J%>Oq1nvX5Ax)a*9%D?e^M?WZhTLViz=hqN=PGljGaGn&IOY#RWc2iR!o|Y*s9z4-n_GxJr{9#_cKnFJ05A4ru@)8RNPqDrC&ZTtaoLZKQYG0yhy~D=XO=GXU?+@b$X)iE*~{rOBf^d_}$sCCzb9T)Fkzjl-z^Bg5Bt9rw}Kzu@mQFq;|CIHsPQ%4a=@%;V>Qb`S8iM<VZa3{yWmePNKB0MYi@=6}N3LYuH&nVi3xHg256#4PfqK824Dk|&L>24G|D`R0Mu?nWc~svU?mlZ#g98_1LqErKPtDbq&P1fhgLsS3fC@e&0m<a2an7c`0+X%Q;Rt~U-9a;mmmHP%z<XrRP}>lReCa>pQS;gLX~TQiqb4ETb#`vKohU2h``mW_(dG<-#nE@RZGwryX|jt?)}NMchXEK5nKvFg{y4(|IB9p}oh{u-^Fp!U=$dJ~6*>gv!(lJOvLGmBp1PX5{7R}RjUIuQu&b|!L^opoLCP05!8LI2)EGuySYgqDoBaH>YOmc_T!`slzkjlkksmdUdZ9}jlfFj0$l50<9}VtvB9?E>lS=|bw{+}BCImkq+!P;&jPHQjf@6sK;_xs!ijUX~FkgbAm%66?$J<?#mphPW=l&~Lc^u{z>3>@w2%3&rFP93~sHCMt(G9e+Fr3w5Z{q6cAa8l}mJeTYPAu9+x~=8ujJeEl82eW^FvA76g{;g2uXx5<V*B@C|L{kDwCPkx*O`&uCx`?j<m0a~UwX*%-xt$S)+P2T;3OpWz~Y@9v~&yjo|4&3i?#EoOi5vP@*K0YUqw)haVeJ+M)vnEp^jSS)%CeTQ>xT_1MXpU1MkX%O?1e5&)m>@6LDDbAW@u0EGD}2<D{!xAYlckk(qd(eiXjb8bfv=%MhaBR3WgGz7y|qx-MZSsX_th614aAQ|K4rQ2`3&&OG_K&Az>(up!D+IMI`QC=l^f<fe8aY*js5r9b`9%UtugRjdD3&b^fdW888;=U3(4q^>=j@TVPU$7w@;Jp^hs|UyI7Js&v3mVuoP|APaz1W@@!PHg&Jwnv44pXC}nV?ACj6&H4}_PeROU;JC|`cfP<dsujIkg6N9|G_p>*vyG`KX&x%9nDV$9#L`mPh=edSyb9WL?AA-Z0sA5QsLzcZd8os~wHey^9CM3Xn8J=LX62wB8Oj`v8W0m2pVirxr2in}{0~~orQY0D`BGn;z%Ghd}2R8_c2|D)OXC!3+50oEW*EHMFshk@t(liJg$Q*cY1S==GUk!o})fu;)U7Z^JvXH__EN@EJUSuz0Snf=Ps5HQ)xQVpFof`dQKHw^q&PKWnQz0e&pN32o0@9g6bQhjtNWEF7ZP(s>7VA617txSno26;qo~mPq<=Tj^5Ej0(qCh{&J36zsbf!kVC_T8Qj)(>usN%V~mad_YojLA;%t4AL0)+z6TrS{2Bt;=2?qGtW#$^AR*yGbO<k^OacE;REMyP5O2b-3$rHVIO{>-X`g1VwyFQ#1iF3Fd1j#{$fryd9e$}heS7ow>8ReW?in2)ui$%f7YW?TVK7>Z<yO@LQrwt{*}$UfNYI^bh%mCiBH&%kBQ%ljF%ha1H$k=RCaZTK@anbYD|l=`fEjW*e+Ml2-$(f&1~migJPdqSCRX~u;Wxs7D`_qpT>S%^egGI+44G8(|ji`dHPvWcTRi5eD>`QoTii;H`BB(I}i-tKP-h;|0KDWQ#hljn3);d`B@bC#yuqT??bpB@Y~v>g(DRluA0{=L)wQvp14h>I!2p=rrw!?C?8KTD$4$_o7*X(Dg3j&`oeih0uRdh{F9A~h-3h0;#ktWb|QZWBm}0zDpbO8CB-Fhi-lyXkz*t-DKpEvQ*<qVEg-D2M5kKl8M8uRzWE?}eIey)9iDME?ocEdCA6B-T&L>NBE_la$hqO0+0o#6?ype}#AdX!Q7$Xi5EWjB-lg%|j?^prMoB(6}I&;R()*E4pq#duOpJVkjp83=vL`(44G!T>;V?7H1XG4|R5onus9UARGh^C(*HTpBshbgGz~Up`jc1*=COsN!kL-Y)b@)!3YEFoWEjI>E>{QNVwe=6^gf#DFs{}PI6nEd!W#V@WetCC?Wy}AdAqT5`DB^f$ZdzssjkPF(l)S0PQY1x2rl)A;pSZ<hkgfZ`SdyZwz)e?U_=~G_^~V#*piUY!nny?75=M2;gNVHY~Hsy#HJ|bzt^3?Q`29=E>x-GcQKP!7g8H9a$*!T8^E3zN)>zG$D>AEA<CQMT8BO;@E`_y`Zg|qG_NLUEKmvsaps^ajd4Kgvuqp1_;x_Nzr@4+<~Lh@8(g=ER=b2uA0iZP?KQJd0Y<0uNY`RJ)(_1OQ8s`5xB5Lq$z2%w^W@?<_!2cn+s_ORJVsV&?F6=G8rk0F4cNx&Yg0$R*ic6IRmm9y{}V>%=b=BufVcGzv~xUlgypM(H-xJq;BK)#j-y7)vMs$lc=R~GtcNO)n{9u3(^_UKFr4#7YzdQF{X7Yg$N75j5h7@#GHqv8JwucKt`M-N6o`h#<u&|vvt|_bav6!q6n$s=mY9V43BE_;5iB^ma`Yzb0=GUPkjflejaw4BuMFdoYUHTem&g%T2#Ifsh<nE1?si-dBdZFp4N>~z+6M#b0JMopV1Usim}8<O_xISajoiH$PK6yiV{##&#xzhG)-;f*syON$6VnysL2!M!OcEqM+2u9+UzN*cNz^T;s1HeBufxjM*wU_!nR~x0KH-!)$@trC?Xpbuu)8<NHDnV*$v+$%ro;z+E&4l-~6KMXBRb*wh;F4;M~~H4(y4wPIJC?rYY7%HBsnU$`P<~)*4KB(nA5h0?k~(oK!8~N{R_`3&E`zIX*Zsry=1{!*?PrxF_YjR0^vY^D(jJL6zg9WHAoP_@kgY?_EaJe0E^6bKN2CqcZn)F>e?mCuIb%M@K_diVC#q+uM*f<nUi1D!|I6Ke=2-kPcRe%v|csnmT{Rv*k)a02PtOQMp?-pKyu?3u|+Apuy_5wKc$o;Y4k+JaS?HH&R2(g;`ily4=XJkT$5@MBMs$mKuT(5Fb;e!(4Jh!{I4p<qX&7{<$*fC$M|J`JfEFN5Z7%l{i1C(RT?+=ht9EbCWP1I8G%X6l2$$+i(r@%!)F|<QoL!MI&<SUl<+`M>kXo0u_<OGhw^Wq#N9u^K(9`W<^WT{HQoUV{8ycwRh{2=Xq@a5$}KSe2Z`sY8eSR-iqv=oHtkDBv89{^QVO7f}`+zMkPKks<jsfee>QXdcp%$C1X_0Hh2m-As_46VpIq=*f=n3&7!b+P|wkazJc5Q`HEs&DS-yX_RF4yMZC+F!Isvu{L~YnnG)gjt2=>~(7cSUSeUX<c!Y*<giq53vG0(35-!s#<il752Ci7n3u6^&%>8#RbOK~*!UInP+^B9S69iyI#Po<?)N6u4)b}$)1CA`>gLy+{sLt#3`Jr-se|+?SpDAuPcx-2^Ui<Re%KFJmo4DMq#RL>|2(ZPJ!QxzK3V?95MR<l;f+h+Eo-Lh@7@!v!uX*ikLU9ux#Z(_n+ndo){peb6ZYzamsT)riQlUx&lW>>zdpx&ep=aQ1N8C$+u(G!em7)mVkL%dDBLy9nXxuY>79j&%&?5D`t>^Si2|j3(GN4F<`V3`n(VCFinK@nOCoGH7nuz{jYHZN!=lQB$g<vv!H+?VKSgCXnRAEC*ouXlu=HU<`GsZ7dh~v_VFRrD{=O=F?sQQkh6-xgJAvwk#Tjeu_^1W&)t*A(uhutoCxF^BG%@;eA&oL&k)nw89&czDq$*Lq2;8LQXbJD_-W;;1*ETgw`gKV-!Lp+C|%qCoghWCoo^79qAjfuKguxeWUR7C_63iG%q$2K|Ztf?x-cn7`lTt#!IW`CK{VusYDMTM!21w<6k*%te-6JfvaZ*g@)-j&7|Lo!5#!?rq$vW}G5HA*N|76`AxucPIgzw+|<7+YivX6I-1(ehof1(Yuo?oM3@Bl!@#Zab^gIqzND5eE-kkLZB_KnCL|X!`E0cy_5zEVD9ob^Nm6Y={<E9fr4M4IUrxtcQbJxGJwu&#r@rsXh!C%>*4SA5$;4fL-ki{n%M7DH;v>GWqL_-QNOMdC)1X7<t73Zfp?>k{9|6;+TW`qwoT+ILr^r<>nCaq!C#|FBhX0I!e^SHyrAmr$AHRz{%I#zS;`vb`nk=8m3NJVirSAt04IGqU=bEO)xIz&2U$9&LaR<w5S7LMyIdF0$^k(+i~A*C;Oy-ub>UWeIpUTh0b&R9kFcg>58T6@($*gWz|0e3oc#n)36aX$1oEP2*!9`WLh$$dm5uq!`c7Aud$<Ajh2d$pkF2pPnJSof;OH7T|{;N6|}-3hYT*=<je8+4=*B(qRlUZg4;AsxO8*IPJu48M!b+4q}=i^o1<e3Og-M;AMj+iu?}9uWzc}#^2DWE?dzFoXC$p5h<d!CFn+Xr^Tq5%@Xs{(eQyZHSWfdn&-Hdc`y~ExgOFJHDwYNpb(~p`65{1t!gdXUl>4dg{Mlr$_>Am7Lmaq~h~KR~$84+jnCDIe;~uS#pGx%i91~f3g^7U1<~L@OrBRDJ2zb(eAj^Xq2SaFqbKKB=1&{;x;9$3jzkYocYYF5K$}o6zvL&7&i}iI(c0Rm%<8g9}_nv85T|;=3%4*+#{gSx<&OcoPSWSg<iQKXYxK{PE)k<8GCn?8T9##|P{&8};{5P&h#2Y$x*)T{4OWMN=dR(T<Zk|jEgH4~@nd{lhUHX))>Tyu-yQVUP9OKh9$@%E!(D_dDu_gxoAq*jsYP@tM4*k>bZ$-uwcVp(QXW8kQ$Y0Gfo`YRGo?|7|FXBY7JgGSL&1`Dxe<*>$-SBrRF~4DKE$<LIc&0OV44;}@&lD^2KIhZx3Z|ErkRq31cC(f~0>rJKGnLfKD_~BVj97-HK}--lPN|atH*7GG;Z(0yUt;Rr;Deji6BbR)>xVbH_x^68Jdr+RTB&Z-OdCo6VEV6t1RcHHT@4eFzGfmmv?~P|VdM0LT%|2$!qb~*&&4z<lXp-f)`f^Acwn0%f&lEyTylA0!O{M~-5fa+C%Hc$V&%eZW+(3}Y_!#&=~Ia1v(W3vLfgWXH8skPGHphRg|b25!H@{mj}Fbgcf2Xz&#Uh^;FW=$?+a;Z5;ydbOdp02{KZ?YRN-EV#NmXb)}~3bp-Y$6khj}7Z)cAZX(8{8XCklZ^v?sMhRx7!%dauJbA=F4$<qc1_F`$gNI6b*N9J}HF9*44T?hO8NQ!gj$eV`rL<otHcdJ?W=X|G(^b3_wMz3LbBBVB70n2`fjtlCImXvUC#$!(>%A~p|Js9f;CS6O^=z^*+34@e}S)Uq=HSs$@rtjGL#?Nsl%hwyV=hZCEja#4XU*Cu<DA(tqV5;&rcK|TL?^39rqO3)w=SsDI9f@vH4iT7FFOy`%c=+Sz_N1=bRP~z7S1pR^sVP8p$7NEli~_bY(XHTH232qf{wd3nUQm<`$P&C=0mr}o#>amqq<A+J=6IYITw&5avW}m|1ip<=ztO8K5?uNC<P>p#!D;a^D61rI-rn=BEVhxl_52y5iLH;k;c+v4z6#%9ArS=QWeJh(wsF3Uu67_F+x=mOo$H6b2;BVzx_bV}Vo<()`{?r6;_v}&eU2`F+sEf02FI}wZDdA&x>Ii@kNfE5+$8^dH@vGaj{1xHhvBcX&F|2Pq5c0H@1w7N>cKHxYSZDpXIsazrQ7o!Ott3A$dCWEplb4s?Fvu%LzG~j)QRi^MOphUZ_HUYnvvJ;EBO9}MWd+lM&P)OiYqQ+4{JfqJer|uAQiuk@xCC+DK*t+`T(aDBw~QheKVgUvbF0KecE+i!}R0$2)_HAka=(z<CE**FMsXr|NMX6{*V9r|N3A5`=eif`{BR8|Ft3RU-aEa41fRrZ-4&s_kaBB_g_E$+<5unfBWILpWlD`{a-)-@Y{cX|Mv6g^7Ehm{{FAO|MvdF&;R=UA72OQ>(A%Q&wqXY<6nRO;lI8A^^@iLlb`;_|M=nluhz@Ye*gK)mp}gT)BF9$AI!1GhCXy>20ui7x_qMQ*g?{}d?@PO<wK8M?7@#gKQAAsI{WQ!l<oWM@5h6!{`sZL9}rUYp<p_z&($4Y;pZOu{t>6upSW}%cMXp~*@kk)>z`jI9e=1E0sOgO>Z{K^&VKNT%Lr`nGk63(fA>S*$MPrFd0&bj*Xw*OJ`wcv;S-Ouyp=zzm-oX@gMK~yo6nwoL><?kff>Dgpz7VwSD&f+Hw@Khs#(1L^s$e_SpB^0<?wN5UB6o{-|EMgzJBzh{7kTT%Z~*!T7InRboGIH@0K5_CipLw>;DVp-1tB'
_C171_DATA = _c171_json.loads(_c171_zlib.decompress(_c171_base64.b85decode(_C171_PAYLOAD)))
_C171_NEW_ROUTES = frozenset((100, 101, *range(103, 129)))
_C171_ROUTE_MAP = {tuple(row[:2]): int(row[2]) for row in _C171_DATA["shops"]}
if len(_C171_ROUTE_MAP) != 49 or any("YARN_STORE" in shops for shops in _C171_ROUTE_MAP):
    raise RuntimeError("c171 shop-map contract failed")
if _IMPL.chassis.players or _IMPL.chassis._future_sells:
    raise RuntimeError("c171 routes must be installed before the first observation")
if set(map(int, _C171_DATA["patches"])) != _C171_NEW_ROUTES:
    raise RuntimeError("c171 route-id contract failed")

for _c171_raw_id, _c171_patch in _C171_DATA["patches"].items():
    _c171_route_id = int(_c171_raw_id)
    _c171_tape = list(_ROUTES[0])
    for _c171_step, _c171_action in _c171_patch:
        _c171_tape[int(_c171_step)] = _c171_action
    _c171_tape[0] = dict(_c171_tape[0], market=[list(order) for order in _R42_OPENING])
    if len(_c171_tape) != 719:
        raise RuntimeError("c171 route-length contract failed")
    _ROUTES[_c171_route_id] = _c171_tape
    _IMPL.chassis.routes[_c171_route_id] = list(_c171_tape)

del _C171_DATA, _C171_PAYLOAD
del _c171_raw_id, _c171_patch, _c171_route_id, _c171_tape, _c171_step, _c171_action


_C171_LEGACY_ROUTER = _IMPL.chassis.router


def _c171_v42_route(observation):
    raw = _get(_get(observation, "town", {}), "unlocked_shops", None)
    if not isinstance(raw, (list, tuple)) or len(raw) < 2:
        return None
    pair = tuple(raw[:2])
    if not all(isinstance(shop, str) for shop in pair):
        return None
    return _C171_ROUTE_MAP.get(pair)


def _c171_router(observation, step, state):
    first_day6 = 144 <= step < 648 and not state.get("day6")
    try:
        route = _C171_LEGACY_ROUTER(observation, step, state)
    except (KeyError, TypeError, ValueError, IndexError):
        # Malformed observations must retain a safe legacy route.  A cold
        # terminal callback still closes irreversibly onto route 2.
        if step >= 648:
            state["route"] = 2
            state["day27"] = True
        route = state.get("route", 0)
    if first_day6:
        v42_route = _c171_v42_route(observation)
        if v42_route is not None:
            route = v42_route
            state["route"] = route
            state["c171_expert"] = "V42"
        else:
            state["c171_expert"] = "o182"
    return route


_IMPL.chassis.router = _c171_router


def _c171_selected_route(observation):
    step = int(_get(observation, "step", 0))
    if step >= 648:
        return 2
    seat = int(_get(observation, "player", 0))
    native = _IMPL.chassis.players.get(seat, {})
    route = native.get("route")
    if route is not None:
        return route
    if 144 <= step < 648:
        v42_route = _c171_v42_route(observation)
        if v42_route is not None:
            return v42_route
    return 0


# o170 calls the o171 wrapper through _O170_PARENT.  The later r97 wrapper
# calls o170 through _R97_PARENT.  Rebind only these parent links so every
# earlier and later o182 layer remains in the original order.
_C171_BEFORE_O171 = _O171_PARENT
_C171_ORIGINAL_O171 = _O170_PARENT
_C171_ORIGINAL_O170 = _R97_PARENT
_C171_GUARD_STATES = {}


def _c171_guard_state(observation):
    seat = int(_get(observation, "player", 0))
    step = int(_get(observation, "step", 0))
    state = _C171_GUARD_STATES.get(seat)
    # The o171/o170 gate and the final telemetry wrapper can both inspect one
    # external callback.  Equal steps are the same callback, not a new game.
    if state is None or step < state["last"]:
        state = _C171_GUARD_STATES[seat] = {
            "last": -1, "o171_guarded": 0, "o170_guarded": 0, "errors": 0,
        }
    state["last"] = step
    return state


def _c171_gate_o171(observation, configuration=None):
    step = int(_get(observation, "step", 0))
    if _c171_selected_route(observation) in _C171_NEW_ROUTES and 150 <= step <= 182:
        state = _c171_guard_state(observation)
        if step == 150:
            state["o171_guarded"] += 1
        return _C171_BEFORE_O171(observation, configuration)
    return _C171_ORIGINAL_O171(observation, configuration)


_O170_PARENT = _c171_gate_o171


def _c171_gate_o170(observation, configuration=None):
    step = int(_get(observation, "step", 0))
    if _c171_selected_route(observation) in _C171_NEW_ROUTES and 241 <= step < 300:
        state = _c171_guard_state(observation)
        if step == 241:
            state["o170_guarded"] += 1
        return _O170_PARENT(observation, configuration)
    return _C171_ORIGINAL_O170(observation, configuration)


_R97_PARENT = _c171_gate_o170


_C171_PARENT = agent
_C171_REPORT = {}
del agent


def agent(observation, configuration=None):
    result = _C171_PARENT(observation, configuration)
    try:
        state = _c171_guard_state(observation)
        route = _c171_selected_route(observation)
        _C171_REPORT.clear()
        _C171_REPORT.update(getattr(_C171_PARENT, "telemetry", {}))
        _C171_REPORT.update({
            "c171_route": route,
            "c171_v42_selected": int(route in _C171_NEW_ROUTES),
            "c171_o171_guarded": state["o171_guarded"],
            "c171_o170_guarded": state["o170_guarded"],
            "c171_guard_errors": state["errors"],
        })
    except Exception:
        _C171_REPORT["c171_guard_errors"] = _C171_REPORT.get("c171_guard_errors", 0) + 1
    return result


agent.telemetry = _C171_REPORT
agent = globals().pop("agent")


# o215_c171_guard (Claude/o-series, 2026-09-15). Overlay for c171: drop the V42 routes for shop pairs where
# the world bank shows V42 losing to the legacy o182 route (n>=8 & wins>=base & worst>-8000 required to keep).
# Kept pairs: 27, dropped pairs: 16.
_O215_DROP = [["FARMERS_MARKET", "FARMERS_MARKET"], ["PET_CAFE", "FARMERS_MARKET"], ["PET_CAFE", "BRUNCH_SPOT"], ["SMOOTHIE_SHOP", "PIZZA_SHOP"], ["PIZZA_SHOP", "ICE_CREAM_SHOP"], ["BAKERY", "PET_CAFE"], ["PIZZA_SHOP", "SMOOTHIE_SHOP"], ["PIZZA_SHOP", "PIZZA_SHOP"], ["BAKERY", "FARMERS_MARKET"], ["PET_CAFE", "BAKERY"], ["BAKERY", "BAKERY"], ["FARMERS_MARKET", "BAKERY"], ["BRUNCH_SPOT", "BRUNCH_SPOT"], ["BRUNCH_SPOT", "PET_CAFE"], ["ICE_CREAM_SHOP", "PIZZA_SHOP"], ["SMOOTHIE_SHOP", "BRUNCH_SPOT"]]
for _p in _O215_DROP:
    _C171_ROUTE_MAP.pop(tuple(_p), None)
agent = globals().pop('agent')


# o199c_carrot_switch price-only ratio 2.0 (Claude/o-series, 2026-09-15). Overlay for o182.
"""World-conditional WHEAT -> CARROT switch for the tape's wheat cycle.
Evidence: holdout loss -34k in a PET_CAFE x3 world - carrot price 35 -> 229 (hinge), rival planted
102 carrots vs our fixed 31. Carrot (seed 20, 1 + 1 unit per watered day at age 2-3, decays from
age 4) fits the wheat cycle the tape already runs (plant, water, harvest at age 2-4).
Rule (per planting step): switch when carrot demand 6*(2*PET_CAFE + FARMERS_MARKET) >= _O199_DEMAND
or carrot price >= _O199_RATIO * wheat price. Mechanics:
  * market: every BUY_SEED WHEAT n gets a companion BUY_SEED CARROT n (wheat seeds are kept, so a
    failed switch never blocks a planting; unused wheat seeds are worth $10 each);
  * field: PLANT WHEAT -> PLANT CARROT while carrot seeds cover this step's switched plantings;
  * harvest: on a CARROT tile at age 3 any non-HARVEST command by the worker standing there becomes
    HARVEST (the wheat schedule may only come back at age 4, when the carrot is already decaying);
  * sale: projected carrot stock beyond the parent's SELL CARROT orders is appended as one SELL.
Feed wheat is replenished by the existing grain/feed overlays (C126, o177, r97). Never touches the
opening (day < _O199_MIN_DAY) or day >= 27 (a carrot planted then cannot be harvested by day 29).
Telemetry: o199_switches, o199_harvest_swaps, o199_seed_orders, o199_extra_sales, o199_errors.
"""
import copy as _o199_copy

_O199_PARENT = agent
_O199_STATE = {}
_O199_REPORT = {}
_O199_DEMAND = 9999     # b: price-only rule
_O199_RATIO = 2.0
_O199_MIN_DAY = 8
_O199_MAX_DAY = 26
del agent


def _o199_hot(observation):
    shops = observation['town'].get('unlocked_shops', []) or []
    demand = 6 * (2 * shops.count('PET_CAFE') + shops.count('FARMERS_MARKET'))
    prices = observation['market']['prices']
    return demand >= _O199_DEMAND or prices['CARROT'] >= _O199_RATIO * max(1, prices['WHEAT'])


def agent(observation, configuration=None):
    step = int(observation.get('step', 0))
    seat = int(observation.get('player', 0))
    st = _O199_STATE.get(seat)
    if st is None or step <= st['last']:
        st = _O199_STATE[seat] = {'last': -1, 'switches': 0, 'harvest_swaps': 0, 'seed_orders': 0, 'extra_sales': 0, 'errors': 0, 'mine': {}}
    st['last'] = step
    parent_action = _O199_PARENT(observation, configuration)
    result = parent_action
    try:
        day = step // 24
        farm = observation['farms'][seat]
        private = observation['private']
        positions = [farm['farmer'], *farm['hands']]
        cmds = [parent_action.get('farmer') or ['PASS'], *(parent_action.get('hands') or [])]
        out = None
        hot = _O199_MIN_DAY <= day <= _O199_MAX_DAY and _o199_hot(observation)
        # 1) harvest OUR switched carrots at age 3 (the tape's native carrots keep their own schedule)
        for i, c in enumerate(cmds[:len(positions)]):
            x, y = positions[i]
            tile = farm['tiles'][y][x]
            if (isinstance(tile, dict) and tile.get('kind') == 'PLANT' and tile.get('crop') == 'CARROT'
                    and st['mine'].get((x, y)) == int(tile.get('planted_day', -1))
                    and day - int(tile.get('planted_day', day)) >= 3 and int(tile.get('yield_units', 0)) > 0
                    and c != ['HARVEST']):
                out = out or _o199_copy.deepcopy(parent_action)
                if i == 0:
                    out['farmer'] = ['HARVEST']
                else:
                    out['hands'][i - 1] = ['HARVEST']
                st['harvest_swaps'] += 1
        if hot:
            # 2) PLANT WHEAT -> PLANT CARROT within available carrot seeds
            seeds = int(private['seeds'].get('CARROT', 0) or 0)
            for i, c in enumerate(cmds[:len(positions)]):
                if c == ['PLANT', 'WHEAT'] and seeds > 0:
                    x, y = positions[i]
                    if farm['tiles'][y][x] is not None:
                        continue
                    out = out or _o199_copy.deepcopy(parent_action)
                    if i == 0:
                        out['farmer'] = ['PLANT', 'CARROT']
                    else:
                        out['hands'][i - 1] = ['PLANT', 'CARROT']
                    seeds -= 1; st['switches'] += 1; st['mine'][(x, y)] = day
            # 3) companion carrot seed orders for the wheat seed purchases
            orders = (out or parent_action).get('market') or []
            extra = [['BUY_SEED', 'CARROT', int(o[2])] for o in orders if o and o[0] == 'BUY_SEED' and o[1] == 'WHEAT' and int(o[2]) > 0]
            if extra and len(orders) + len(extra) <= 10:
                out = out or _o199_copy.deepcopy(parent_action)
                out['market'] = list(out.get('market') or []) + extra
                st['seed_orders'] += len(extra)
        # 4) sell carrot stock beyond the parent's carrot sales (only once we have switched)
        if st['switches']:
            act = out or parent_action
            orders = act.get('market') or []
            stock = projected_shed(act, FarmView(observation)).get('CARROT', 0)
            sale = sum(max(0, int(o[2])) for o in orders if o and o[:2] == ['SELL', 'CARROT'])
            if stock > sale and len(orders) < 10:
                out = out or _o199_copy.deepcopy(parent_action)
                out['market'] = list(out.get('market') or []) + [['SELL', 'CARROT', int(stock - sale)]]
                st['extra_sales'] += 1
        if out is not None:
            result = out
    except Exception:
        st['errors'] += 1
        result = parent_action
    _O199_REPORT.clear()
    _O199_REPORT.update(getattr(_O199_PARENT, 'telemetry', {}))
    _O199_REPORT.update({'o199_' + k: v for k, v in st.items() if k not in ('last', 'mine')})
    return result


agent.telemetry = _O199_REPORT
agent = globals().pop('agent')


# o206_yarn_sheep_feed (Claude/o-series, 2026-09-15). Overlay for the o199c stack.
"""Never skip SHEEP feeds on yarn routes (YARN_STORE among the first two shops).
World bank: o162's feed gate loses -540 vs V43/FSV4/MSF in yarn worlds (11-14 sheep) while winning
elsewhere - skipped sheep feeds cut wool output, which is our dumping weapon there. Implemented by
wrapping o159's value function: on a yarn route a SHEEP feed is valued as infinite (abandonment path
untouched). Telemetry o206_on (1 = yarn route this game).
"""
_O206_PARENT = agent
_O206_FLAG = {}
_O206_REPORT = {}
_o206_orig_value = _o159_value
del agent


def _o159_value(tile, kind, day, prices):
    v, a = _o206_orig_value(tile, kind, day, prices)
    if kind == 'SHEEP' and _O206_FLAG.get('on'):
        return 1e9, a
    return v, a


def agent(observation, configuration=None):
    shops = observation.get('town', {}).get('unlocked_shops', []) or []
    _O206_FLAG['on'] = 'YARN_STORE' in shops[:2]
    result = _O206_PARENT(observation, configuration)
    _O206_REPORT.clear()
    _O206_REPORT.update(getattr(_O206_PARENT, 'telemetry', {}))
    _O206_REPORT['o206_on'] = int(_O206_FLAG['on'])
    return result


agent.telemetry = _O206_REPORT
agent = globals().pop('agent')


# o211_fsv5_r132 (Claude/o-series, 2026-09-15). lynnsakurai Farming Score V5 block ported verbatim onto the o199c stack: r132 same-day weed recovery + confirmed-mirror sale reorder (bounded pair swaps, gain>=25, similarity>=0.9, cash lead<=500)
# Source lines 2954-3253; upstream notices retained.



# EXP-260: replay-supported conservative guards.
#
# 1. A PLANT blocked by a same-day weed may be recovered when the original
#    per-worker tape contains an immediate WATER and a later PASS before dawn.
#    The inserted PLANT delays that worker's commands by one position; the PASS
#    absorbs the delay, so the worker is synchronized again within the same day.
# 2. At the end of a 72-turn block, an already-confirmed mirror race may reorder
#    an all-SELL queue.  Quantities and field actions are immutable.  A bounded
#    pair-swap search accepts only a positive gain under the exact public price
#    curve and the conservative hypothesis that the rival has the same queue and
#    saleable stock.  This layer never changes buys, hires, land or input stock.

_R132_PARENT = agent
_R132_STATES = {}
_R132_REPORT = {}


def _r132_commands(action):
    return [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]


def _r132_set_command(action, actor, command):
    result = copy.deepcopy(action)
    if actor == 0:
        result['farmer'] = list(command)
    else:
        hands = list(result.get('hands') or [])
        if actor - 1 >= len(hands):
            return action
        hands[actor - 1] = list(command)
        result['hands'] = hands
    return result


def _r132_standard(configuration):
    return configuration is None or all(
        configuration.get(key, value) == value
        for key, value in (
            ('boardSize', 10),
            ('turnsPerDay', 24),
            ('shedCapacity', 100),
            ('maxMarketOrdersPerTurn', 10),
            ('farmHandCostMult', 1),
        )
    )


def _r132_command_valid(observation, action, actor, command):
    view = FarmView(observation)
    if actor >= len(view.positions):
        return False
    position = view.positions[actor]
    tile = _tile_at(view.tiles, position)
    if _is_noop(command, tile, view.inv(actor), view.seeds, position, view.board):
        return False
    if command and command[0] == 'PLANT':
        crop = command[1]
        demand = sum(
            1 for current in _r132_commands(action)
            if current[:2] == ['PLANT', crop]
        )
        # Include the replacement if the parent's command was not this plant.
        parent = _r132_commands(action)[actor]
        demand += int(parent[:2] != ['PLANT', crop])
        if demand > int(view.seeds.get(crop, 0)):
            return False
    return True


def _r132_start_repair(observation, action, state):
    step = int(observation['step'])
    if step % 24 > 20 or state.get('repair'):
        return
    player = int(observation['player'])
    native = _IMPL.chassis.players.get(player)
    if not native or native.get('route') not in _IMPL.chassis.routes:
        return
    tape = _IMPL.chassis.routes[native['route']]
    if step + 2 >= len(tape):
        return
    raw = _r132_commands(tape[step])
    actual = _r132_commands(action)
    farm = observation['farms'][player]
    positions = [farm['farmer'], *farm['hands']]
    private = observation['private']
    day_end = min(len(tape), (step // 24 + 1) * 24)
    for actor, intended in enumerate(raw[:len(positions)]):
        if intended[:1] != ['PLANT'] or actor >= len(actual) or actual[actor] != ['DIG']:
            continue
        x, y = positions[actor]
        tile = farm['tiles'][y][x]
        crop = intended[1]
        if not (isinstance(tile, dict) and tile.get('kind') == 'WEED'):
            continue
        same_crop = sum(1 for command in raw if command[:2] == ['PLANT', crop])
        if int(private['seeds'].get(crop, 0)) < same_crop:
            continue
        next_commands = _r132_commands(tape[step + 1])
        if actor >= len(next_commands) or next_commands[actor] != ['WATER']:
            continue
        deadline = None
        for future_step in range(step + 1, day_end):
            future = _r132_commands(tape[future_step])
            command = future[actor] if actor < len(future) else ['PASS']
            if command == ['PASS']:
                deadline = future_step
                break
        if deadline is None:
            continue
        state['repair'] = {
            'actor': actor,
            'queue': [list(intended)],
            'next_step': step + 1,
            'deadline': deadline,
            'route': native['route'],
        }
        _R132_REPORT['weed_repair_started'] += 1
        return


def _r132_continue_repair(observation, action, state):
    repair = state.get('repair')
    if not repair:
        return action
    step = int(observation['step'])
    player = int(observation['player'])
    native = _IMPL.chassis.players.get(player) or {}
    if (step != repair['next_step'] or step > repair['deadline'] or
            native.get('route') != repair['route']):
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    actor = repair['actor']
    commands = _r132_commands(action)
    if actor >= len(commands) or not repair['queue']:
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    command = repair['queue'].pop(0)
    if not _r132_command_valid(observation, action, actor, command):
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    displaced = commands[actor]
    if displaced != ['PASS']:
        repair['queue'].append(list(displaced))
    if step >= repair['deadline'] and repair['queue']:
        state.pop('repair', None)
        _R132_REPORT['weed_repair_aborted'] += 1
        return action
    result = _r132_set_command(action, actor, command)
    repair['next_step'] = step + 1
    _R132_REPORT['weed_repair_shifted_steps'] += 1
    if command[:1] == ['PLANT']:
        _R132_REPORT['weed_repair_plants'] += 1
    if command == ['WATER']:
        _R132_REPORT['weed_repair_waters'] += 1
    if not repair['queue']:
        state.pop('repair', None)
        _R132_REPORT['weed_repair_completed'] += 1
    return result


def _r132_price_params(observation):
    params = {item: dict(values) for item, values in _R37_MARKET_PARAMS.items()}
    for item, patch in observation['market'].get('params', {}).items():
        if item in params:
            params[item].update(patch)
    return params


def _r132_mirror_revenue(observation, own_orders, rival_orders, stock):
    inventory = dict(observation['market']['inventory'])
    params = _r132_price_params(observation)
    stocks = [dict(stock), dict(stock)]
    revenue = 0
    for index in range(max(len(own_orders), len(rival_orders))):
        pair = []
        for side, orders in enumerate((own_orders, rival_orders)):
            if index >= len(orders):
                pair.append(None)
                continue
            order = orders[index]
            if not order or len(order) < 3 or order[0] != 'SELL':
                pair.append(None)
                continue
            item = order[1]
            quantity = min(
                max(0, int(order[2])),
                max(0, int(stocks[side].get(item, 0))),
            )
            pair.append([item, quantity])
        while any(current is not None and current[1] > 0 for current in pair):
            sold = []
            for side, current in enumerate(pair):
                if current is None or current[1] <= 0:
                    continue
                item = current[0]
                quote = _r37_market_price(item, inventory[item], params)
                if side == 0:
                    revenue += quote
                current[1] -= 1
                stocks[side][item] = max(0, stocks[side].get(item, 0) - 1)
                sold.append((item, quote))
            for item, quote in sold:
                if quote > 1:
                    inventory[item] += 1
    return revenue


def _r132_mirror_reorder(observation, action):
    step = int(observation['step'])
    player = int(observation['player'])
    rival = 1 - player
    orders = action.get('market') or []
    probe = _R44_PROBES.get(player) or {}
    if not (336 <= step < 696 and step % 72 == 71 and probe.get('matched')):
        return action
    if observation['farms'][player]['money'] > observation['farms'][rival]['money'] + 500:
        return action
    if _r37_similarity(observation) < 0.90 or len(orders) < 2:
        return action
    if any(
        not order or len(order) < 3 or order[0] != 'SELL' or
        order[1] not in PRODUCTS or type(order[2]) is not int or order[2] < 0
        for order in orders
    ):
        return action
    stock = projected_shed(action, FarmView(observation))
    if not any(min(order[2], max(0, int(stock.get(order[1], 0)))) > 0 for order in orders):
        return action
    rival_orders = copy.deepcopy(orders)
    current = copy.deepcopy(orders)
    baseline = _r132_mirror_revenue(observation, current, rival_orders, stock)
    score = baseline
    # At most ten orders: bounded deterministic pair-swap ascent is inexpensive.
    for _ in range(10):
        best_score = score
        best_orders = None
        for left in range(len(current)):
            for right in range(left + 1, len(current)):
                if current[left] == current[right]:
                    continue
                trial = copy.deepcopy(current)
                trial[left], trial[right] = trial[right], trial[left]
                trial_score = _r132_mirror_revenue(
                    observation, trial, rival_orders, stock
                )
                if trial_score > best_score:
                    best_score, best_orders = trial_score, trial
        if best_orders is None:
            break
        current, score = best_orders, best_score
    gain = score - baseline
    if gain < 25 or current == orders:
        return action
    _R132_REPORT['mirror_reorders'] += 1
    _R132_REPORT['mirror_modeled_gain'] += gain
    result = copy.deepcopy(action)
    result['market'] = current
    return result


def agent(observation, configuration=None):
    result = _R132_PARENT(observation, configuration)
    try:
        player = int(observation['player'])
        step = int(observation.get('step', observation['day'] * 24 + observation['hour']))
        state = _R132_STATES.get(player)
        if state is None or step <= state['step']:
            state = _R132_STATES[player] = {'step': -1}
            _R132_REPORT.update(
                weed_repair_started=0,
                weed_repair_shifted_steps=0,
                weed_repair_plants=0,
                weed_repair_waters=0,
                weed_repair_completed=0,
                weed_repair_aborted=0,
                mirror_reorders=0,
                mirror_modeled_gain=0,
                replay_guard_errors=0,
            )
        state['step'] = step
        if not _r132_standard(configuration):
            return result
        if state.get('repair'):
            result = _r132_continue_repair(observation, result, state)
        else:
            _r132_start_repair(observation, result, state)
        result = _r132_mirror_reorder(observation, result)
    except Exception:
        _R132_REPORT['replay_guard_errors'] = _R132_REPORT.get('replay_guard_errors', 0) + 1
    _R132_REPORT.update(getattr(_R132_PARENT, 'telemetry', {}))
    return result


agent.telemetry = _R132_REPORT
agent = globals().pop('agent')


# SPDX-License-Identifier: Apache-2.0
# c177 (GPT/Codex, 2026-09-15): tomato substitution on o199c's native strawberry lane.
"""Use an already-funded ongoing-crop lane instead of adding land/labor.

The parent already buys, plants, waters, fertilizes, harvests and carries a final
day-11 STRAWBERRY tranche.  c177 may change only a bounded number of units in
that tranche to TOMATO, preserving the same worker geometry and later field
commands.  Unlike c176 it adds no HIRE, BUY_LAND or WHEAT replacement program.

KAGG_C177_FORCE=KEEP|TOMATO and KAGG_C177_SIZE=1..13 are local-screen hooks.
Force bypasses the economic gate only; it still waits for the certified native
strawberry seed/plant lane.
"""

import copy as _c177_copy
import os as _c177_os

_C177_PARENT = agent
_C177_STATES = {}
_C177_REPORT = {}
_C177_FORCE = (_c177_os.environ.get('KAGG_C177_FORCE', '') or '').strip().upper()
try:
    _C177_SIZE_OVERRIDE = int(_c177_os.environ.get('KAGG_C177_SIZE', '0') or 0)
except Exception:
    _C177_SIZE_OVERRIDE = 0

_C177_DECISION_START = 11 * 24
_C177_DECISION_END = 12 * 24
_C177_MAX_TRANCHE = 13
_C177_MIN_PRICE = 60
_C177_CASH_RESERVE = 2500

del agent


def _c177_new_state():
    return {
        'last': -1,
        'mode': None,
        'target': 0,
        'seed_units': 0,
        'plant_units': 0,
        'sites': set(),
        'pending': [],
        'counts': {
            'decisions': 0,
            'activations': 0,
            'seed_units_rewritten': 0,
            'plant_requests_rewritten': 0,
            'plants_confirmed': 0,
            'plant_failures': 0,
            'deposit_rewrites': 0,
            'sale_turns': 0,
            'sale_units': 0,
            'full_queue_declines': 0,
            'cash_declines': 0,
            'errors': 0,
        },
    }


def _c177_standard(configuration):
    return configuration is None or all(configuration.get(key, value) == value for key, value in (
        ('boardSize', 10), ('turnsPerDay', 24), ('shedCapacity', 100),
        ('maxMarketOrdersPerTurn', 10), ('farmHandCostMult', 1),
    ))


def _c177_tomato_demand(observation):
    shops = observation.get('town', {}).get('unlocked_shops', []) or []
    return sum(shop in ('PIZZA_SHOP', 'FARMERS_MARKET') for shop in shops)


def _c177_has_strawberry_seed(action):
    return any(len(order) >= 3 and order[:2] == ['BUY_SEED', 'STRAWBERRY']
               and int(order[2]) > 0 for order in (action.get('market') or []))


def _c177_decide(observation, action, state):
    if state['mode'] is not None:
        return
    step = int(observation['step'])
    if not (_C177_DECISION_START <= step < _C177_DECISION_END) or not _c177_has_strawberry_seed(action):
        return
    state['counts']['decisions'] += 1
    demand = _c177_tomato_demand(observation)
    price = int(observation['market']['prices'].get('TOMATO', 0))
    farm = observation['farms'][int(observation['player'])]
    forced = _C177_FORCE == 'TOMATO'
    if _C177_FORCE == 'KEEP':
        state['mode'] = 'KEEP'
        return
    if not forced and (demand < 2 or price < _C177_MIN_PRICE):
        state['mode'] = 'KEEP'
        return
    if float(farm.get('money', 0)) < _C177_CASH_RESERVE:
        state['counts']['cash_declines'] += 1
        state['mode'] = 'KEEP'
        return
    if 1 <= _C177_SIZE_OVERRIDE <= _C177_MAX_TRANCHE:
        target = _C177_SIZE_OVERRIDE
    else:
        target = 10 if demand >= 3 else (8 if demand >= 2 else 4)
    state['mode'] = 'TOMATO'
    state['target'] = target
    state['counts']['activations'] += 1


def _c177_rewrite_seed_orders(action, state):
    remaining = state['target'] - state['seed_units']
    if remaining <= 0:
        return action
    market = action.get('market') or []
    changed = _c177_copy.deepcopy(action)
    rewritten = []
    used = 0
    for order in changed.get('market', []):
        if not (len(order) >= 3 and order[:2] == ['BUY_SEED', 'STRAWBERRY']):
            rewritten.append(order)
            continue
        quantity = max(0, int(order[2]))
        take = min(quantity, remaining - used)
        if take <= 0:
            rewritten.append(order)
            continue
        leftover = quantity - take
        # Route 12 has a single 23-unit order in a full queue: only the known
        # 13-unit complete tranche can be safely compacted (10 units are surplus).
        if leftover and len(market) >= 10:
            if not (state['seed_units'] == 0 and quantity == 23 and take == 13):
                state['counts']['full_queue_declines'] += 1
                return action
            leftover = 0
        rewritten.append(['BUY_SEED', 'TOMATO', take])
        if leftover:
            rewritten.append(['BUY_SEED', 'STRAWBERRY', leftover])
        used += take
    if used <= 0 or len(rewritten) > 10:
        return action
    changed['market'] = rewritten
    state['seed_units'] += used
    state['counts']['seed_units_rewritten'] += used
    return changed


def _c177_confirm(observation, state):
    step = int(observation['step'])
    if not state['pending']:
        return
    farm = observation['farms'][int(observation['player'])]
    keep = []
    for request in state['pending']:
        if request['step'] >= step:
            keep.append(request)
            continue
        x, y = request['xy']
        tile = farm['tiles'][y][x]
        if (isinstance(tile, dict) and tile.get('crop') == 'TOMATO'
                and int(tile.get('planted_day', -1)) == request['step'] // 24):
            state['counts']['plants_confirmed'] += 1
        else:
            state['sites'].discard((x, y))
            state['counts']['plant_failures'] += 1
    state['pending'] = keep


def _c177_rewrite_field(observation, action, state):
    if state['plant_units'] >= state['target']:
        # Deposits may still need rewriting after all plants were created.
        remaining_plants = False
    else:
        remaining_plants = True
    result = _c177_copy.deepcopy(action)
    commands = [result.get('farmer') or ['PASS'], *(result.get('hands') or [])]
    farm = observation['farms'][int(observation['player'])]
    positions = [farm.get('farmer'), *farm.get('hands', [])]
    inventories = observation.get('private', {}).get('inventories', [])
    seeds = max(0, int(observation.get('private', {}).get('seeds', {}).get('TOMATO', 0)))
    changed = False
    position_counts = {}
    for pos in positions:
        key = tuple(pos)
        position_counts[key] = position_counts.get(key, 0) + 1
    for actor in range(min(len(commands), len(positions))):
        command = commands[actor]
        pos = tuple(positions[actor])
        x, y = pos
        if (remaining_plants and seeds > 0 and state['plant_units'] < state['target']
                and command == ['PLANT', 'STRAWBERRY']
                and position_counts.get(pos) == 1 and farm['tiles'][y][x] is None):
            commands[actor] = ['PLANT', 'TOMATO']
            state['sites'].add(pos)
            state['pending'].append({'step': int(observation['step']), 'xy': pos})
            state['plant_units'] += 1
            state['counts']['plant_requests_rewritten'] += 1
            seeds -= 1
            changed = True
        elif (len(command) >= 2 and command[:2] == ['PLACE', 'STRAWBERRY']
              and actor < len(inventories)):
            inv = inventories[actor] or {}
            if int(inv.get('STRAWBERRY', 0)) <= 0 and int(inv.get('TOMATO', 0)) > 0:
                commands[actor] = ['PLACE', 'TOMATO', int(inv.get('TOMATO', 0))]
                state['counts']['deposit_rewrites'] += 1
                changed = True
    if not changed:
        return action
    result['farmer'], result['hands'] = commands[0], commands[1:]
    return result


def _c177_add_sale(observation, action, state):
    step = int(observation['step'])
    if step < 19 * 24 or step % 4 != 1:
        return action
    market = action.get('market') or []
    if len(market) >= 10 or any(len(order) >= 3 and order[:2] == ['SELL', 'TOMATO'] for order in market):
        return action
    price = int(observation['market']['prices'].get('TOMATO', 0))
    if price < _C177_MIN_PRICE:
        return action
    stock = max(0, int(projected_shed(action, FarmView(observation)).get('TOMATO', 0)))
    if stock <= 0:
        return action
    # One shop consumes one unit per shop tick.  Match visible absorption rather
    # than dumping the whole shed into a hinge market.
    quantity = min(stock, max(1, min(4, _c177_tomato_demand(observation))))
    result = _c177_copy.deepcopy(action)
    result['market'] = list(result.get('market') or []) + [['SELL', 'TOMATO', quantity]]
    try:
        result = _v224_sales_first(result)
        result = _r37_reorder_sales(observation, result)
    except Exception:
        pass
    state['counts']['sale_turns'] += 1
    state['counts']['sale_units'] += quantity
    return result


def agent(observation, configuration=None):
    step = int(observation.get('step', 0)); seat = int(observation.get('player', 0))
    state = _C177_STATES.get(seat)
    if state is None or step <= state.get('last', -1):
        state = _C177_STATES[seat] = _c177_new_state()
    state['last'] = step
    _c177_confirm(observation, state)
    parent = _C177_PARENT(observation, configuration)
    result = parent
    try:
        if _c177_standard(configuration):
            _c177_decide(observation, parent, state)
            if state.get('mode') == 'TOMATO':
                result = _c177_rewrite_seed_orders(result, state)
                result = _c177_rewrite_field(observation, result, state)
                result = _c177_add_sale(observation, result, state)
    except Exception:
        state['counts']['errors'] += 1
        result = parent
    _C177_REPORT.clear()
    _C177_REPORT.update(getattr(_C177_PARENT, 'telemetry', {}))
    _C177_REPORT.update({'c177_' + key: value for key, value in state['counts'].items()})
    _C177_REPORT.update({
        'c177_mode': state.get('mode') or 'UNDECIDED',
        'c177_target': int(state.get('target', 0)),
        'c177_sites': len(state.get('sites', ())),
    })
    return result


agent.telemetry = _C177_REPORT
agent = globals().pop('agent')


# SPDX-License-Identifier: Apache-2.0
# c179 (GPT/Codex, 2026-09-15): small early tomato lane while preserving V219.
"""Allow o199c's proven V219 SE investment even after c177 planted early tomato.

For the active c177 lane only, qualification is the frozen V219 predicate with
the three 'already have tomato' exclusions removed.  All land/cash/shop/native
route safety gates remain unchanged.  This tests a small early supply tranche as
an addition to the champion regime rather than replacing the champion regime.
"""

_C179_PARENT = agent
_C179_FROZEN_V219_QUALIFIES = _v219_qualifies
_C179_REPORT = {}
del agent


def _c179_v219_qualifies_with_early_tomato(obs, native):
    farm = obs['farms'][obs['player']]
    if len(farm['tiles']) != 10 or set(farm['unlocked_quadrants']) != {'NW', 'NE', 'SW'}:
        return False
    if farm['money'] < 12000 or obs['market']['prices']['TOMATO'] < CROP_MIN_PRICE:
        return False
    if sum(s in ('PIZZA_SHOP', 'FARMERS_MARKET') for s in obs['town']['unlocked_shops']) < 3:
        return False
    if any(farm['tiles'][y][x] != 'LOCKED' for y in (5, 6) for x in range(5, 10)):
        return False
    for tape in _IMPL.chassis.routes.values():
        for a in tape[432:719]:
            if any(o and o[0] == 'BUY_LAND' for o in a.get('market', [])):
                return False
            if any(c == ['PLANT', 'TOMATO'] for c in [a.get('farmer')] + a.get('hands', [])):
                return False
    return True


def _v219_qualifies(observation, native):
    seat = int(observation.get('player', 0))
    lane = _C177_STATES.get(seat) or {}
    if lane.get('mode') == 'TOMATO' and int(lane.get('plant_units', 0)) > 0:
        return _c179_v219_qualifies_with_early_tomato(observation, native)
    return _C179_FROZEN_V219_QUALIFIES(observation, native)


def agent(observation, configuration=None):
    result = _C179_PARENT(observation, configuration)
    _C179_REPORT.clear()
    _C179_REPORT.update(getattr(_C179_PARENT, 'telemetry', {}))
    seat = int(observation.get('player', 0))
    v219 = _V219_STATES.get(seat) or {}
    _C179_REPORT['c179_v219_eligible'] = int(bool(v219.get('eligible')))
    _C179_REPORT['c179_v219_committed'] = int(bool(v219.get('committed')))
    return result


agent.telemetry = _C179_REPORT
agent = globals().pop('agent')


# SPDX-License-Identifier: Apache-2.0
# c180 (GPT/Codex, 2026-09-15): guarded two-tile early tomato addition.
"""Production selector learned from the first paired falsification panel.

Use exactly two native late-strawberry slots for early TOMATO only when current
observed tomato demand is present and the same observation does not already have
two or more strawberry-consuming shops.  The latter state was the consistent
negative slice in c179; KEEP remains exact o199c there.
"""

_C180_ORIGINAL_C177_DECIDE = _c177_decide
if _C177_SIZE_OVERRIDE == 0:
    _C177_SIZE_OVERRIDE = 2


def _c180_strawberry_demand(observation):
    shops = observation.get('town', {}).get('unlocked_shops', []) or []
    return sum(shop in ('BRUNCH_SPOT', 'ICE_CREAM_SHOP', 'SMOOTHIE_SHOP', 'FARMERS_MARKET') for shop in shops)


def _c177_decide(observation, action, state):
    # Explicit force remains a local experiment hook and bypasses this learned
    # economic guard.  Production/AUTO never sees it.
    if (state.get('mode') is None and _C177_FORCE != 'TOMATO'
            and _C177_DECISION_START <= int(observation.get('step', 0)) < _C177_DECISION_END
            and _c177_has_strawberry_seed(action)
            and _c180_strawberry_demand(observation) >= 2):
        state['counts']['decisions'] += 1
        state['mode'] = 'KEEP'
        return
    return _C180_ORIGINAL_C177_DECIDE(observation, action, state)


_C180_PARENT = agent
_C180_REPORT = {}
del agent


def agent(observation, configuration=None):
    result = _C180_PARENT(observation, configuration)
    _C180_REPORT.clear()
    _C180_REPORT.update(getattr(_C180_PARENT, 'telemetry', {}))
    seat = int(observation.get('player', 0))
    state = _C177_STATES.get(seat) or {}
    _C180_REPORT['c180_strawberry_guard'] = int(state.get('mode') == 'KEEP' and _c180_strawberry_demand(observation) >= 2)
    return result


agent.telemetry = _C180_REPORT
agent = globals().pop('agent')


# o224_v44_race_window (Claude/o-series, 2026-09-16). Port of V44 EXP283 with WINDOWED escalation: a lost race raises the
# horizon to 24 for 72 steps only (re-armed by each new lost race), so a spurious race vs a non-mirror tape derivative
# (aurax7/MSF share the public tapes) does not lock the pull-forward for the rest of the game. Base: (Ahmed Berat Ozer, Apache-2.0) onto the o219 stack.
# Clone-gated sale pre-emption: while the rival is observed executing our tape (same worker positions >=4 of last 6
# turns, route similarity >= .95) the R36 reservation horizon is at least 8; if the rival is then seen selling a race
# product at the very turn it dropped into our shed while we did not sell it, the horizon escalates to 24 for the rest
# of the game. Our stack already runs horizon 8/12 (r37/c115) for confirmed mirrors, so the new arm is the escalation.
_RACE_PARENT=agent
_RACE_HORIZON_CLONE=8
_RACE_HORIZON_ESCALATED=24
_RACE_WINDOW=72
_RACE_ITEMS=('CARROT','TOMATO','STRAWBERRY','MELON','EGG','MILK','WOOL')
_RACE_SHOPS={'BAKERY':('EGG','WHEAT'),'PIZZA_SHOP':('MILK','TOMATO','WHEAT'),'BRUNCH_SPOT':('EGG','WHEAT','STRAWBERRY'),'YARN_STORE':('WOOL',),
             'ICE_CREAM_SHOP':('STRAWBERRY','MILK','WHEAT'),'PET_CAFE':('CARROT',),'SMOOTHIE_SHOP':('STRAWBERRY','MILK'),'FARMERS_MARKET':('WHEAT','CARROT','TOMATO','STRAWBERRY')}
_RACE_STATE={}
_RACE_REPORT=dict(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0)
_RACE_ORIG_RESERVE=_r36_reserve
del agent

def _race_positions_equal(farms,player):
    own,rival=farms[player],farms[1-player]
    return len(own['hands'])>0 and own['hands']==rival['hands'] and own['farmer']==rival['farmer']

def _race_clone(observation,state):
    farms=observation['farms'];player=int(observation['player'])
    if len(farms[player]['hands'])>0:
        state['hist'].append(_race_positions_equal(farms,player))
        if len(state['hist'])>6:state['hist'].pop(0)
    return len(state['hist'])>=4 and sum(state['hist'])>=4 and _r37_similarity(observation)>=.95

def _race_town(step,shops):
    out={}
    if step%4==0:
        for shop in shops:
            items=_RACE_SHOPS.get(shop,())
            for item in items:out[item]=out.get(item,0)+(2 if len(items)==1 else 1)
    if step%24==0:
        for item in _RACE_ITEMS:out[item]=out.get(item,0)+1
    return out

def _race_lost(observation,state):
    """True when the rival sold a race product at the previous turn, our shed stock of it rose at that turn
    (a drop) and we did not sell any of it: the rival quotes at the drop while we hold."""
    prev=state.get('prev');prev_action=state.get('prev_action')
    if prev is None or prev_action is None:return False
    step=int(observation['step'])
    if step!=prev['step']+1 or step%24==0:return False
    shed=observation['private']['shed'];inv=observation['market']['inventory'];pinv=prev['inventory'];prices=prev['prices']
    town=_race_town(step-1,prev['shops'])
    sold={}
    for order in prev_action.get('market',[]):
        if len(order)>=3 and order[0]=='SELL' and order[1] in _RACE_ITEMS:sold[order[1]]=1
    for item in _RACE_ITEMS:
        held=int(shed.get(item,0));before=int(prev['view'].shed.get(item,0))
        if held<=before or item in sold or prices.get(item,0)<=1:continue
        rival=int(inv[item])-int(pinv[item])+town.get(item,0)
        if rival>0:return True
    return False

def _race_snapshot(observation):
    market=observation['market']
    return dict(step=int(observation['step']),inventory=dict(market['inventory']),prices=dict(market['prices']),shops=list(observation['town'].get('unlocked_shops',[])),view=FarmView(observation))

def _r36_reserve(obs,action):
    player=int(obs['player']);h=_RACE_STATE.get(player,{}).get('horizon',0)
    if h>_R37_HORIZONS.get(player,2):
        saved=_R37_HORIZONS.get(player);_R37_HORIZONS[player]=h
        try:return _RACE_ORIG_RESERVE(obs,action)
        finally:
            if saved is None:_R37_HORIZONS.pop(player,None)
            else:_R37_HORIZONS[player]=saved
    return _RACE_ORIG_RESERVE(obs,action)

def agent(observation,configuration=None):
    state=None
    try:
        player=int(observation['player']);step=int(observation['step'])
        state=_RACE_STATE.get(player)
        if state is None or step<=state['step']:
            state=_RACE_STATE[player]={'step':-1,'hist':[],'horizon':0,'level':_RACE_HORIZON_CLONE,'prev':None,'prev_action':None,'until':-1}
        if step==0:_RACE_REPORT.update(race_clone_turns=0,race_horizon_turns=0,race_lost_races=0,race_escalations=0,race_errors=0)
        state['step']=step;state['horizon']=0
        standard=configuration is None or all(configuration.get(k,v)==v for k,v in [('boardSize',10),('turnsPerDay',24),('shedCapacity',100),('maxMarketOrdersPerTurn',10)])
        if standard and 216<=step<696 and _race_clone(observation,state):
            _RACE_REPORT['race_clone_turns']+=1
            if _race_lost(observation,state):
                _RACE_REPORT['race_lost_races']+=1;state['until']=step+_RACE_WINDOW
                if state['level']<_RACE_HORIZON_ESCALATED:_RACE_REPORT['race_escalations']+=1
                state['level']=_RACE_HORIZON_ESCALATED
            elif state['level']==_RACE_HORIZON_ESCALATED and step>state['until']:
                state['level']=_RACE_HORIZON_CLONE
            state['horizon']=state['level'];_RACE_REPORT['race_horizon_turns']+=1
    except Exception:_RACE_REPORT['race_errors']+=1
    snapshot=None
    try:
        if state is not None and 215<=int(observation['step'])<696:snapshot=_race_snapshot(observation)
    except Exception:_RACE_REPORT['race_errors']+=1
    action=_RACE_PARENT(observation,configuration)
    try:
        if state is not None:state['prev']=snapshot;state['prev_action']=action if snapshot is not None else None
    except Exception:_RACE_REPORT['race_errors']+=1
    _RACE_REPORT.update(getattr(_RACE_PARENT,'telemetry',{}))
    return action
agent.telemetry=_RACE_REPORT
agent=globals().pop('agent')


# o227_stealth_drop (Claude/o-series, 2026-09-16). Stealth pull-forward for the o224 stack.
# V44's race arm escalates (horizon 24 for the rest of the game) the moment it sees us SELL a product at the very turn
# it dropped into the shed while V44 held. Our c115 widening (12 vs the public 8) makes exactly that visible at drop
# turns. Rule: on a turn where our own action PLACEs a race product into the shed (a drop turn, identical for a mirror),
# run the native R36 reservation with horizon 8 (what the public lineage sells too); the 9..12-step pull-forward is
# deferred one turn (still ahead of an 8-horizon mirror) and V44 never observes a lost race. Off outside 288..695.
# Telemetry: o227_stealth_turns.
_O227_ITEMS = ('CARROT', 'TOMATO', 'STRAWBERRY', 'MELON', 'EGG', 'MILK', 'WOOL')
_O227_INNER = _r36_reserve
_O227_NATIVE = _C115_NATIVE_R36_RESERVE
_O227_COUNT = {'turns': 0}
_O227_PARENT = agent
_O227_REPORT = {}
del agent


def _r36_reserve(obs, action):
    step = int(obs['step']); player = int(obs['player'])
    if 288 <= step < 696:
        cmds = [action.get('farmer') or ['PASS'], *(action.get('hands') or [])]
        if any(len(c) >= 2 and c[0] == 'PLACE' and c[1] in _O227_ITEMS for c in cmds):
            saved = _R37_HORIZONS.get(player); _R37_HORIZONS[player] = 8
            _O227_COUNT['turns'] += 1
            try:
                return _O227_NATIVE(obs, action)
            finally:
                if saved is None: _R37_HORIZONS.pop(player, None)
                else: _R37_HORIZONS[player] = saved
    return _O227_INNER(obs, action)


def agent(observation, configuration=None):
    if int(observation.get('step', 0)) == 0:
        _O227_COUNT['turns'] = 0
    result = _O227_PARENT(observation, configuration)
    _O227_REPORT.clear()
    _O227_REPORT.update(getattr(_O227_PARENT, 'telemetry', {}))
    _O227_REPORT['o227_stealth_turns'] = _O227_COUNT['turns']
    return result


agent.telemetry = _O227_REPORT
agent = globals().pop('agent')


# o231_fert_tours (Claude/o-series, 2026-09-16). Re-priced R51 fertilizer tours on the o227 stack.
# R51 (EXP182) hires a hand to fertilize wheat/carrot tiles in their yield window but priced every fertilizer unit at
# the market quote and demanded value >= 1.5*cost+50, so it never fired (0/128 games): live data show our late
# fertilizer is dumped at $7-15/unit while a fertilized watering adds +1 crop unit (~$38). Changes: own shed
# fertilizer beyond the native pickups is priced at _O231_OWN_VALUE (its late dump value) and only the shortfall is
# bought; ratio 1.5 -> 1.2 (+25). Everything else (targets, paths, hires, pickups, telemetry) is the original R51.
_O231_OWN_VALUE=12
_O231_RATIO=1.2
def _r51_input_control(obs,action,state):
    step=int(obs['step']);day=step//24;hour=step%24;player=int(obs['player']);farm=obs['farms'][player];private=obs['private']
    native=_IMPL.chassis.players[player]
    if state.get('day')!=day:state.update(day=day,workers={},pending=None,placed=[])
    for x,y in state['placed']:
        tile=farm['tiles'][y][x]
        if isinstance(tile,dict) and tile.get('fertilized_until_day',-1)>=day+2:_R51_INPUT_REPORT['input_confirmed_applications']+=1
        else:_R51_INPUT_REPORT['input_application_errors']+=1
    state['placed']=[]
    if state.get('pending'):
        pending=state.pop('pending')
        for actor,plan in pending.items():
            if len(farm['hands'])>=actor:state['workers'][actor]=plan;_R51_INPUT_REPORT['input_confirmed_hires']+=1
            else:_R51_INPUT_REPORT['input_hire_errors']+=1
    if state['workers']:
        changed=copy.deepcopy(action)
        for actor,plan in state['workers'].items():
            inv=private['inventories'][actor];pos=tuple(farm['hands'][actor-1]);cmd=['PASS']
            if not plan['loaded']:
                stock=projected_shed(changed,FarmView(obs));q=min(plan['quantity'],max(0,stock.get('FERTILIZER',0)))
                if q and _shed_adjacent(pos,10):
                    cmd=['PICKUP','FERTILIZER',q];plan['loaded']=True;_R51_INPUT_REPORT['input_loaded_units']+=q
                    if q<plan['quantity']:_R51_INPUT_REPORT['input_stock_shortfalls']+=plan['quantity']-q
            elif inv.get('FERTILIZER',0):
                while plan['path']:
                    x,y,crop,birth=plan['path'][0];tile=farm['tiles'][y][x]
                    if not isinstance(tile,dict) or tile.get('crop')!=crop or tile.get('planted_day')!=birth or tile.get('fertilized_until_day',-1)>=day+2:
                        plan['path'].pop(0);continue
                    cmd=_v219_walk(pos,(x,y)) or ['FERTILIZE']
                    if cmd==['FERTILIZE']:state['placed'].append((x,y));plan['path'].pop(0);_R51_INPUT_REPORT['input_application_requests']+=1
                    break
            changed['hands'][actor-1]=cmd
        return changed
    if hour not in (1,2,3) or not 12<=day<=28:return action
    planned=_v219_native_day(native,day);expected=max(len(a.get('hands',[])) for a in planned)
    if any(o and o[0]=='HIRE' for a in planned[hour:] for o in a.get('market',[])) or native['pending']:return action
    parents=[_V219_STATES.get(player,{}),_V233_STATES.get(player,{})]
    # A parent may retry after a full market queue; its headcount must remain native.
    if day in (12,18) or any(p.get('committed') and p.get('requested_day')!=day for p in parents):return action
    if any(p.get('pending') for p in parents) or any(o and o[0]=='HIRE' for o in action.get('market',[])):return action
    owned=set(range(1,expected+1))
    for p in parents:
        actors=set(p.get('workers',{}))
        if owned&actors:return action
        owned|=actors
    if owned!=set(range(1,len(farm['hands'])+1)):return action
    targets=_r51_input_forecast(obs,native['route'],expected);plans=[];total_q=0;total_cost=0;all_units={'WHEAT':0,'CARROT':0}
    stock=projected_shed(action,FarmView(obs));purchases=sum(max(0,int(o[2])) for o in action.get('market',[]) if len(o)>2 and o[0] in ('BUY_PRODUCT','BUY_ANIMAL'))
    # Units act before market orders. Preserve the native next-turn pickup,
    # after the current parent's actual sales/purchases, before buying tour inputs.
    available=max(0,stock.get('FERTILIZER',0))
    for o in action.get('market',[]):
        if len(o)>=3 and o[:2]==['SELL','FERTILIZER']:available=max(0,available-max(0,int(o[2])))
        elif len(o)>=3 and o[:2]==['BUY_PRODUCT','FERTILIZER']:available+=max(0,int(o[2]))
    next_native=planned[hour+1];native_pickups=sum(max(0,int(c[2]) if len(c)>2 else 1) for c in [next_native.get('farmer') or ['PASS'],*(next_native.get('hands') or [])] if len(c)>1 and c[:2]==['PICKUP','FERTILIZER'])
    topup=max(0,native_pickups-available)
    spare=max(0,available-native_pickups);total_own=0
    for i in range(_R51_INPUT_MAX_WORKERS):
        path,units=_r51_input_path(obs,targets);q=len(path)
        if q<3 or len(action.get('market',[]))+2+i>10 or sum(stock.values())+purchases+total_q+q+topup>95:break
        quote=_r37_market_price('FERTILIZER',obs['market']['inventory']['FERTILIZER']-total_q-q-topup)
        own=min(q,max(0,spare-total_own));cost=(q-own+(topup if i==0 else 0))*(quote+2)+own*_O231_OWN_VALUE+_v219_fib(int(farm['hires_today'])+i)
        value=sum(n*max(1,_r37_market_price(item,obs['market']['inventory'][item]+all_units[item]+n)-2) for item,n in units.items())
        if value<_O231_RATIO*cost+25 or farm['money']<total_cost+cost+3000:break
        plans.append({'path':path,'quantity':q,'loaded':False});total_q+=q;total_cost+=cost;total_own+=own
        for item,n in units.items():all_units[item]+=n
        for x,y,_,_ in path:targets.pop((x,y),None)
    if not plans:return action
    state['pending']={len(farm['hands'])+1+i:plan for i,plan in enumerate(plans)}
    _R51_INPUT_REPORT['input_hire_requests']+=len(plans);_R51_INPUT_REPORT['input_purchase_requests']+=total_q+topup
    _R51_INPUT_REPORT['input_forecast_wheat']+=all_units['WHEAT'];_R51_INPUT_REPORT['input_forecast_carrot']+=all_units['CARROT']
    changed=copy.deepcopy(action);buy=max(0,total_q-total_own+topup)
    if buy:changed['market'] += [['BUY_PRODUCT','FERTILIZER',buy]]
    changed['market'] += [['HIRE'] for _ in plans];_R51_INPUT_REPORT['o231_own_units']=_R51_INPUT_REPORT.get('o231_own_units',0)+total_own;return changed


agent = globals().pop('agent')

# c326: make the embedded predictor respect the parent's existing glut gate.
# No new threshold, training set, replay lookup or production change.
_C326_PREDICT = _v92_predict
_C326_ON = True
_C326_REPORT = dict(calls=0, restricted_item_calls=0, errors=0)

def _v92_predict(obs, action, state):
    if int(obs['step']) == 0:
        _C326_REPORT.update(calls=0, restricted_item_calls=0, errors=0)
    global _V92_P_USE
    allowed = _V92_P_USE
    if not _C326_ON:
        return _C326_PREDICT(obs, action, state)
    try:
        _V92_P_USE = tuple(item for item in allowed if obs['market']['prices'].get(item, 0) > V9_RACEGATE_BASE[item] + V9_RACEGATE_MARGIN)
        _C326_REPORT['calls'] += 1
        _C326_REPORT['restricted_item_calls'] += len(allowed) - len(_V92_P_USE)
        return _C326_PREDICT(obs, action, state)
    finally:
        _V92_P_USE = allowed

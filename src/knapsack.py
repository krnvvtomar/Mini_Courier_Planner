"""0/1 Knapsack dynamic programming for selecting parcels under van capacity."""

def select_parcels(parcels, capacity):
    """
    Maximize total parcel value without exceeding capacity.
    Each parcel can be selected at most once.
    Returns selected parcels and a summary dictionary.
    """
    n = len(parcels)
    weights = [int(p["weight_kg"]) for p in parcels]
    values = [int(p["value"]) for p in parcels]

    # dp[i][w] = maximum value using first i parcels and capacity w.
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        wt, val = weights[i - 1], values[i - 1]
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if wt <= w:
                dp[i][w] = max(dp[i][w], val + dp[i - 1][w - wt])

    selected = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected.append(parcels[i - 1])
            w -= weights[i - 1]
    selected.reverse()

    summary = {
        "capacity_kg": capacity,
        "used_capacity_kg": sum(int(p["weight_kg"]) for p in selected),
        "total_value": sum(int(p["value"]) for p in selected),
        "dp_table": dp,
    }
    return selected, summary

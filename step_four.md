Now we move to the core: IMPACT MODELING.

This is where your project stops being academic and starts becoming quant.

## STEP 4: impact_model.py

We model three components:

Spread Cost

Temporary Market Impact (Square-root model)

Total Execution Cost

Mathematical Framework


**Let:**

Q = shares to liquidate

ADV = average daily volume

σ = daily volatility

Participation rate = Q / ADV


**Spread Cost:**

SpreadCost = (Spread / 2) × Q

Temporary Impact (square-root model):

Impact per share = k × σ × √(Q / ADV)

k is impact coefficient (0.5–1.5 typical empirical range)


**Total Impact Cost:**

ImpactCost = Impact per share × Q

Total Cost:

TotalCost = SpreadCost + ImpactCost

Now implementation.

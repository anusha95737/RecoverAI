import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load payment data
data = pd.read_csv("payments.csv")

# Features used by RecoverAI
features = [
    "amount",
    "previous_successes",
    "previous_failures",
    "retry_count"
]

X = data[features]
y = data["recovered"]

# Train the recovery prediction model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)


def predict_recovery(payment):
    """Predict the probability that a failed payment can be recovered."""

    values = [[
        payment["amount"],
        payment["previous_successes"],
        payment["previous_failures"],
        payment["retry_count"]
    ]]

    probability = model.predict_proba(values)[0][1]

    return round(probability * 100, 2)


def recommend_action(payment, probability):
    """Choose a bounded recovery action."""

    if probability >= 75 and payment["retry_count"] == 0:
        return "Retry payment immediately"

    elif probability >= 50 and payment["retry_count"] < 2:
        return "Send payment retry link"

    elif probability >= 30:
        return "Retry later"

    else:
        return "Stop recovery and escalate"
from datetime import datetime


def execute_recovery(payment, probability, action):
    """
    Simulated and bounded payment recovery workflow.
    No real payment is processed.
    """

    amount = float(payment["amount"])

    # Simulate the outcome based on recovery probability
    if probability >= 75:
        status = "Recovered"
        recovered_amount = amount

    elif probability >= 50:
        status = "Recovery Link Sent"
        recovered_amount = 0

    elif probability >= 30:
        status = "Scheduled for Later"
        recovered_amount = 0

    else:
        status = "Stopped / Escalated"
        recovered_amount = 0

    return {
        "payment_id": payment["payment_id"],
        "amount": amount,
        "probability": probability,
        "action": action,
        "status": status,
        "recovered_amount": recovered_amount,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
import json

def load_campaign(file_path: str):
    with open(file_path, "r") as f:
        data = json.load(f)

    campaign = {
        "name": data["campaign_name"],
        "product_name": data["product_name"],
        "target_audience": data["target_audience"],
        "features": data["features"],
        "email_series": data["email_series"],
        "recipients": data["recipients"]
    }
    return campaign

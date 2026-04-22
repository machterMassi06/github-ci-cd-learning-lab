import json

alerts = []

# here we generate 1M alerts (you can adjust it)
for i in range(1_000_000):
    rnd = abs(hash(i))

    alert = {
        "objectId": f"ZTF_{i}",
        "jd": 2459000.5 + (rnd % 1000) / 1000,
        "mag": (rnd % 500) / 100 + 15,
        "fid": int((rnd % 2) + 1),
    }

    alerts.append(alert)

# save in JSON lines
with open("data/alerts.json", "w") as f:
    for alert in alerts:
        f.write(json.dumps(alert) + "\n")

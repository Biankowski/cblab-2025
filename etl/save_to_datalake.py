import os
import json

def save_to_datalake(endpoint: str, payload: dict, base_dir: str = "data-lake/raw"):
    bus_dt = payload["busDt"]
    store_id = payload["storeId"].replace(" ", "_")

    dir_path = os.path.join(base_dir, endpoint, f"store_id={store_id}", f"bus_dt={bus_dt}")
    os.makedirs(dir_path, exist_ok=True)

    filename = os.path.join(dir_path, f"{endpoint}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, ensure_ascii=False)

    print(f"Arquivo salvo em: {filename}")


if __name__ == "__main__":
    response = {
        "busDt": "2024-01-01",
        "storeId": "99 CB CB",
        "guestChecks": [
            {
                "guestCheckId": 1122334455,
                "chkNum": 1234
            }
        ]
    }

    save_to_datalake(endpoint="getGuestChecks", payload=response)

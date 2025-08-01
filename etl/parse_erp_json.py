import json
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    dbname="cocobambu",
    user="postgres",
    password="postgres"
)
cursor = conn.cursor()

with open("exemplos/ERP.json", "r") as f:
    data = json.load(f)

for check in data["guestChecks"]:
    cursor.execute("""
        INSERT INTO guest_checks (
            guest_check_id, chk_num, opn_utc, clsd_utc, gst_cnt, sub_ttl
        ) VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        check["guestCheckId"],
        check["chkNum"],
        check["opnUTC"],
        check["clsdUTC"],
        check["gstCnt"],
        check["subTtl"]
    ))

    for tax in check.get("taxes", []):
        cursor.execute("""
            INSERT INTO taxes (
                guest_check_id, tax_num, txbl_sls_ttl, tax_coll_ttl, tax_rate, type
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            check["guestCheckId"],
            tax["taxNum"],
            tax.get("txblSlsTtl"),
            tax.get("taxCollTtl"),
            tax.get("taxRate"),
            tax.get("type")
        ))

    for line in check.get("detailLines", []):
        cursor.execute("""
            INSERT INTO detail_lines (
                guest_check_line_item_id, guest_check_id, line_num, detail_utc, dsp_ttl
            ) VALUES (%s, %s, %s, %s, %s)
        """, (
            line["guestCheckLineItemId"],
            check["guestCheckId"],
            line.get("lineNum"),
            line.get("detailUTC"),
            line.get("dspTtl")
        ))

        if "menuItem" in line:
            cursor.execute("""
                INSERT INTO menu_items (
                    guest_check_line_item_id, mi_num, mod_flag, incl_tax, active_taxes, prc_lvl
                ) VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                line["guestCheckLineItemId"],
                line["menuItem"].get("miNum"),
                line["menuItem"].get("modFlag"),
                line["menuItem"].get("inclTax"),
                line["menuItem"].get("activeTaxes"),
                line["menuItem"].get("prcLvl")
            ))

        for discount in line.get("discount", []):
            cursor.execute("""
                INSERT INTO discounts (
                    guest_check_line_item_id, discount_code, amount
                ) VALUES (%s, %s, %s)
            """, (
                line["guestCheckLineItemId"],
                discount.get("code"),
                discount.get("amount")
            ))

        for charge in line.get("serviceCharge", []):
            cursor.execute("""
                INSERT INTO service_charges (
                    guest_check_line_item_id, description, amount
                ) VALUES (%s, %s, %s)
            """, (
                line["guestCheckLineItemId"],
                charge.get("description"),
                charge.get("amount")
            ))

        for tender in line.get("tenderMedia", []):
            cursor.execute("""
                INSERT INTO tender_medias (
                    guest_check_line_item_id, type, amount
                ) VALUES (%s, %s, %s)
            """, (
                line["guestCheckLineItemId"],
                tender.get("type"),
                tender.get("amount")
            ))

        for error in line.get("errorCode", []):
            cursor.execute("""
                INSERT INTO error_codes (
                    guest_check_line_item_id, code, message
                ) VALUES (%s, %s, %s)
            """, (
                line["guestCheckLineItemId"],
                error.get("code"),
                error.get("message")
            ))

conn.commit()
cursor.close()
conn.close()
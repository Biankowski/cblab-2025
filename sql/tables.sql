CREATE TABLE guest_checks (
    guest_check_id BIGINT PRIMARY KEY,
    chk_num INT,
    opn_bus_dt DATE,
    opn_utc TIMESTAMP,
    opn_lcl TIMESTAMP,
    clsd_bus_dt DATE,
    clsd_utc TIMESTAMP,
    clsd_lcl TIMESTAMP,
    last_trans_utc TIMESTAMP,
    last_trans_lcl TIMESTAMP,
    last_updated_utc TIMESTAMP,
    last_updated_lcl TIMESTAMP,
    clsd_flag BOOLEAN,
    gst_cnt INT,
    sub_ttl DECIMAL(10,2),
    non_txbl_sls_ttl DECIMAL(10,2),
    chk_ttl DECIMAL(10,2),
    dsc_ttl DECIMAL(10,2),
    pay_ttl DECIMAL(10,2),
    bal_due_ttl DECIMAL(10,2),
    rvc_num INT,
    ot_num INT,
    oc_num INT,
    tbl_num INT,
    tbl_name VARCHAR(50),
    emp_num BIGINT,
    num_srvc_rd INT,
    num_chk_prntd INT,
    loc_ref VARCHAR(50)
);

CREATE TABLE taxes (
    id BIGSERIAL PRIMARY KEY,
    guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),
    tax_num INT,
    txbl_sls_ttl DECIMAL(10,2),
    tax_coll_ttl DECIMAL(10,2),
    tax_rate DECIMAL(5,2),
    type INT
);

CREATE TABLE detail_lines (
    guest_check_line_item_id BIGINT PRIMARY KEY,
    guest_check_id BIGINT REFERENCES guest_checks(guest_check_id),
    rvc_num INT,
    dtl_ot_num INT,
    dtl_oc_num INT,
    line_num INT,
    dtl_id INT,
    detail_utc TIMESTAMP,
    detail_lcl TIMESTAMP,
    last_update_utc TIMESTAMP,
    last_update_lcl TIMESTAMP,
    bus_dt DATE,
    ws_num INT,
    dsp_ttl DECIMAL(10,2),
    dsp_qty INT,
    agg_ttl DECIMAL(10,2),
    agg_qty INT,
    chk_emp_id BIGINT,
    chk_emp_num BIGINT,
    svc_rnd_num INT,
    seat_num INT
);

CREATE TABLE menu_items (
    id BIGSERIAL PRIMARY KEY,
    guest_check_line_item_id BIGINT REFERENCES detail_lines(guest_check_line_item_id),
    mi_num INT,
    mod_flag BOOLEAN,
    incl_tax DECIMAL(10,2),
    active_taxes VARCHAR(50),
    prc_lvl INT
);

CREATE TABLE discounts (
    id BIGSERIAL PRIMARY KEY,
    guest_check_line_item_id BIGINT REFERENCES detail_lines(guest_check_line_item_id),
    discount_code VARCHAR(50),
    amount DECIMAL(10,2)
);

CREATE TABLE service_charges (
    id BIGSERIAL PRIMARY KEY,
    guest_check_line_item_id BIGINT REFERENCES detail_lines(guest_check_line_item_id),
    description VARCHAR(100),
    amount DECIMAL(10,2)
);

CREATE TABLE tender_medias (
    id BIGSERIAL PRIMARY KEY,
    guest_check_line_item_id BIGINT REFERENCES detail_lines(guest_check_line_item_id),
    type VARCHAR(50),
    amount DECIMAL(10,2)
);

CREATE TABLE error_codes (
    id BIGSERIAL PRIMARY KEY,
    guest_check_line_item_id BIGINT REFERENCES detail_lines(guest_check_line_item_id),
    code VARCHAR(50),
    message TEXT
);

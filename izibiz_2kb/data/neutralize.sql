-- disable izibiz
UPDATE gib_base_2kb_provider
   SET asiapay_merchant_id = NULL,
       asiapay_currency_id = NULL,
       asiapay_secure_hash_secret = NULL,
       asiapay_secure_hash_function = NULL;
WHERE provider = 'izibiz';
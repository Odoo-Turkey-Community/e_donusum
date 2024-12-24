-- disable izibiz
UPDATE gib_base_2kb_provider
   SET izibiz_username = NULL,
       izibiz_password = NULL,
       izibiz_jwt = NULL;
WHERE provider = 'izibiz';


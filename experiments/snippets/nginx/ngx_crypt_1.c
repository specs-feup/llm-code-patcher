#define NULL ((void *)0)

static ngx_int_t ngx_crypt_plain(ngx_pool_t *pool, u_char *key, u_char *salt, u_char **encrypted)
{
    size_t   len;
    u_char  *p;

    len = ngx_strlen(key);

    *encrypted = ngx_pnalloc(pool, sizeof("{PLAIN}") - 1 + len + 1);
    if (*encrypted == NULL) {
        return NGX_ERROR;
    }

    p = ngx_cpymem(*encrypted, "{PLAIN}", sizeof("{PLAIN}") - 1);
    ngx_memcpy(p, key, len + 1);

    return NGX_OK;
}
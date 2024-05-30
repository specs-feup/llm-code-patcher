#define NULL ((void *)0)

OPENSSL_STACK *OPENSSL_sk_dup(const OPENSSL_STACK *sk)
{
    OPENSSL_STACK *ret;

    if ((ret = OPENSSL_malloc(sizeof(*ret))) == NULL)
        goto err;

    if (sk == NULL) {
        ret->num = 0;
        ret->sorted = 0;
        ret->comp = NULL;
    } else {
        /* direct structure assignment */
        *ret = *sk;
    }

    if (sk == NULL || sk->num == 0) {
        /* postpone |ret->data| allocation */
        ret->data = NULL;
        ret->num_alloc = 0;
        return ret;
    }

    /* duplicate |sk->data| content */
    ret->data = OPENSSL_malloc(sizeof(*ret->data) * sk->num_alloc);
    if (ret->data == NULL)
        goto err;
    memcpy(ret->data, sk->data, sizeof(void *) * sk->num);
    return ret;

 err:
    OPENSSL_sk_free(ret);
    return NULL;
}
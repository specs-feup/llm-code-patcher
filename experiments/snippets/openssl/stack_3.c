#define NULL ((void *)0)

OPENSSL_STACK *OPENSSL_sk_deep_copy(const OPENSSL_STACK *sk,
                                    OPENSSL_sk_copyfunc copy_func,
                                    OPENSSL_sk_freefunc free_func)
{
    OPENSSL_STACK *ret;
    int i;

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
        /* postpone |ret| data allocation */
        ret->data = NULL;
        ret->num_alloc = 0;
        return ret;
    }

    ret->num_alloc = sk->num > min_nodes ? sk->num : min_nodes;
    ret->data = OPENSSL_zalloc(sizeof(*ret->data) * ret->num_alloc);
    if (ret->data == NULL)
        goto err;

    for (i = 0; i < ret->num; ++i) {
        if (sk->data[i] == NULL)
            continue;
        if ((ret->data[i] = copy_func(sk->data[i])) == NULL) {
            while (--i >= 0)
                if (ret->data[i] != NULL)
                    free_func((void *)ret->data[i]);
            goto err;
        }
    }
    return ret;

 err:
    OPENSSL_sk_free(ret);
    return NULL;
}
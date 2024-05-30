#define NULL ((void *)0)

int RSA_flags(const RSA *r)
{
    return r == NULL ? 0 : r->meth->flags;
}
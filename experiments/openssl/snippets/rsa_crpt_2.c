int RSA_size(const RSA *r)
{
    return BN_num_bytes(r->n);
}
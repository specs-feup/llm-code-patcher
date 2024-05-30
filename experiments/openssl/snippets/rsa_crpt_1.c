int RSA_bits(const RSA *r)
{
    return BN_num_bits(r->n);
}
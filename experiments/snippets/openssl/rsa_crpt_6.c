int RSA_public_decrypt(int flen, const unsigned char *from, unsigned char *to,
                       RSA *rsa, int padding)
{
    return rsa->meth->rsa_pub_dec(flen, from, to, rsa, padding);
}
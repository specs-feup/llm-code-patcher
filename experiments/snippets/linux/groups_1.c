#define NULL ((void *)0)

struct group_info *groups_alloc(int gidsetsize)
{
	struct group_info *gi;
	gi = kvmalloc(struct_size(gi, gid, gidsetsize), GFP_KERNEL_ACCOUNT);
	if (!gi)
		return NULL;

	refcount_set(&gi->usage, 1);
	gi->ngroups = gidsetsize;
	return gi;
}
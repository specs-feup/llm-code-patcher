#define NULL ((void *)0)

void groups_sort(struct group_info *group_info)
{
	sort(group_info->gid, group_info->ngroups, sizeof(*group_info->gid), gid_cmp, NULL);
}
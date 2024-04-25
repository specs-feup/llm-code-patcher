/* export the group_info to a user-space array */
static int groups_to_user(gid_t __user *grouplist, const struct group_info *group_info)
{
	struct user_namespace *user_ns = current_user_ns();
	int i;
	unsigned int count = group_info->ngroups;

	for (i = 0; i < count; i++) {
		gid_t gid;
		gid = from_kgid_munged(user_ns, group_info->gid[i]);
		if (put_user(gid, grouplist+i))
			return -EFAULT;
	}
	return 0;
}
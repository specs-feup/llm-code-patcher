static inline void cpuhp_reset_state(int cpu, struct cpuhp_cpu_state *st,
		  enum cpuhp_state prev_state)
{
	bool bringup = !st->bringup;

	st->target = prev_state;

	/*
	 * Already rolling back. No need invert the bringup value or to change
	 * the current state.
	 */
	if (st->rollback)
		return;

	st->rollback = true;

	/*
	 * If we have st->last we need to undo partial multi_instance of this
	 * state first. Otherwise start undo at the previous state.
	 */
	if (!st->last) {
		if (st->bringup)
			st->state--;
		else
			st->state++;
	}

	st->bringup = bringup;
	if (cpu_dying(cpu) != !bringup)
		set_cpu_dying(cpu, !bringup);
}
def combine_reducers(reducers_dict):

    def root_reducer(state, action):
        if state is None:
            state = {}

        next_state = {}
        has_changed = False

        for key, reducer in reducers_dict.items():

            previous_state_for_key = state.get(key)

            next_state_for_key = reducer(previous_state_for_key, action)

            next_state[key] = next_state_for_key

            if next_state_for_key is not previous_state_for_key:
                has_changed = True

        return next_state if has_changed else state

    return root_reducer

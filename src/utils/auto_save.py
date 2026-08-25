import functools
from src.utils.save_state import save_state

def auto_save(step_name: str):
    def decorator(node_func):
        @functools.wraps(node_func)
        def wrapper(state, config, *args, **kwargs):
            # Execute the real node 
            result = node_func(state, config, *args, **kwargs)
            
            # Merge the result into the state
            temp_state = {**state, **result}
            
            # Save the state after the node execution
            save_state(temp_state, step_name)
            
            # Return the real result of the node
            return result
        return wrapper
    return decorator
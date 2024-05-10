from chainpipe.logger import Logger
from chainpipe.timer import Timer


class Chain:
    def __init__(self, operations=None):
        self.operations = operations if operations is not None else []
        self.logger = Logger(__name__)
        self.timer = Timer()

    def __or__(self, func):
        """ Overload the | operator to add a new operation to the current chain. """
        self.operations.append(func)
        return self

    def add_operation(self, func):
        """ Add a new operation to the current chain explicitly. """
        self.operations.append(func)
        return self

    def undo_last_operation(self):
        """ Removes the last operation added to the chain, if any. """
        if self.operations:
            self.operations.pop()

    def copy(self):
        """ Return a shallow copy of the current chain. """
        return Chain(list(self.operations))

    def execute(self, input_data, verbose=False):
        """
        Execute the chain of operations on the input data.

        Args:
        input_data: The initial data to pass through the chain.
        verbose (bool): If True, enables detailed logging of each operation.

        Returns:
        The result after all operations have been applied.
        """
        result = input_data
        for operation in self.operations:
            self.timer.start()
            try:
                result = operation(result)
                self.timer.stop()
                if verbose:
                    self.logger.debug(f"Operation {operation.__name__} output: {result}")
                    self.logger.debug(f"Time taken: {self.timer.format_time(self.timer.elapsed_ns())}")
            except Exception as e:
                if verbose:
                    self.logger.error(f"Error during operation {operation.__name__}: {e}")
                break
        return result

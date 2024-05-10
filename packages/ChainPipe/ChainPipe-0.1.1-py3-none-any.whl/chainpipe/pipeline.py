from chainpipe.logger import Logger
from chainpipe.timer import Timer


class Pipeline:
    def __init__(self, operations=None):
        self.operations = operations if operations is not None else []
        self.logger = Logger(__name__)
        self.timer = Timer()

    def add_operation(self, operation):
        """ Adds an operation to the pipeline. """
        self.operations.append(operation)
        return self

    def execute(self, verbose=False):
        """ Execute all operations in the pipeline, tracking the time for each. """
        for operation in self.operations:
            self.timer.start()
            try:
                operation()  # Execute operation without passing data
                self.timer.stop()
                if verbose:
                    elapsed_time = self.timer.format_time(self.timer.elapsed_ns())
                    self.logger.debug(f"Operation {operation.__name__} completed successfully in {elapsed_time}.")
            except Exception as e:
                self.timer.stop()  # Ensure timer stops on exception
                if verbose:
                    elapsed_time = self.timer.format_time(self.timer.elapsed_ns())
                    self.logger.error(f"Error during operation {operation.__name__}: {e}. Time elapsed: {elapsed_time}")
                # Decide whether to continue or stop; here we continue
        if verbose:
            self.logger.debug("All operations executed.")

    def __or__(self, operation):
        """ Enables the use of the | operator to add operations. """
        return self.add_operation(operation)
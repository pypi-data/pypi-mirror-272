class Emitter:
    """
    A class that allows for event-driven programming by registering listeners for specific events and triggering those events
    when necessary.
    """

    def __init__(self):
        """
        Initializes an instance of the Emitter class with an empty dictionary to store listeners.
        """
        self.listeners = {}

    def on(self, event, callback):
        """
        Register a callback function to be called when the specified event is emitted.

        Args:
            event (str): The name of the event to listen for.
            callback (function): The function to call when the event is emitted.

        Returns:
            self: The Emitter instance, to allow for method chaining.
        """
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(callback)
        return self

    def off(self, event, callback):
        """
        Remove a previously registered callback function for the specified event.

        Args:
            event (str): The name of the event to remove the callback from.
            callback (function): The function to remove from the event's callback list.

        Returns:
            self: The Emitter instance, to allow for method chaining.
        """
        if event in self.listeners:
            self.listeners[event].remove(callback)
        return self

    def trigger(self, event, *args, **kwargs):
        """
        Trigger all registered callback functions for the specified event.

        Args:
            event (str): The name of the event to trigger.
            *args: Any additional arguments to pass to the callback functions.
            **kwargs: Any additional keyword arguments to pass to the callback functions.

        Returns:
            self: The Emitter instance, to allow for method chaining.
        """
        if event in self.listeners:
            for callback in self.listeners[event]:
                callback(*args, **kwargs)
        return self

    def __del__(self):
        """
        Destructor for the Emitter class.
        Clears the listeners dictionary.
        """
        self.listeners = {}

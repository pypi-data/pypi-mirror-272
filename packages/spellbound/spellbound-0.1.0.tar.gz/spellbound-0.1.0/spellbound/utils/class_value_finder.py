class ClassValueFinder(dict):
    """
    A dict-like object that can find a value by a class or an instance.
    It searches for a value by a class first.
    If it cannot find a value, it searches for a value by a base class.
    """

    def find_by_class(self, klass):
        """
        Search for a value by a class.
        If it cannot find a value, search for a value by a base class.

        Args:
            klass (type): class to search for

        Returns:
            Any: value found or None
        """
        queue = [klass]
        while queue:
            k = queue.pop()
            if k in self:
                return self[k]
            queue.extend(k.__bases__)
        return None

    def find_by_instance(self, instance):
        """
        Search for a value for the class of an instance.
        If the class of the instance is not found, search for a value by a base class.

        Args:
            instance (object): instance to search for

        Returns:
            Any: value found or None
        """
        return self.find_by_class(type(instance))

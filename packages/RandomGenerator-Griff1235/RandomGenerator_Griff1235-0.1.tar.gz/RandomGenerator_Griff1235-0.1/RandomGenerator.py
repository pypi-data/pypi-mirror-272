import datetime

class RandomGenerator:
    """
    A class used to generate pseudorandom numbers.

    This class uses a linear congruential generator (LCG) algorithm to generate pseudorandom numbers.
    The LCG algorithm is a widely used and well-established method for generating pseudorandom numbers.
    It works by iteratively calculating a new seed value based on the previous seed value, using the formula:

    seed = (a * seed + c) mod m

    where a, c, and m are constants. The choice of these constants can affect the quality of the pseudorandom numbers generated.
    In this implementation, the constants a, c, and m are set to 1664525, 1013904223, and 2^32, respectively.
    """

    def __init__(self, seed=None):
        """
        The constructor for the RandomGenerator class.

        :param seed: The seed for the random number generator. If None, a seed will be generated based on the current time.
        :type seed: int
        """
        if seed is None:
            # Generate a seed based on the current time if one is not provided
            self.seed = int(datetime.datetime.now().timestamp() * 1000) % (2**32)
        else:
            self.seed = seed

        # Constants for the linear congruential generator algorithm
        self.a = 1664525
        self.c = 1013904223
        self.m = 2**32
    
    def get_state(self):
        """
        Returns the current state of the random number generator.

        The state of the random number generator is defined by the seed value and the constants a, c, and m.
        This function returns a tuple containing these values, which can be used to restore the state of the random number generator later.

        :return: A tuple containing the current state of the random number generator.
        :rtype: tuple
        """
        return (self.seed, self.a, self.c, self.m)

    def set_state(self, state):
        """
        Sets the current state of the random number generator to the given input.

        The state of the random number generator is defined by the seed value and the constants a, c, and m.
        This function takes a tuple containing these values as input and sets the state of the random number generator accordingly.

        :param state: A tuple containing the new state of the random number generator.
        :type state: tuple
        :raises ValueError: If the input state is not a tuple or does not contain four elements.
        :raises TypeError: If the elements of the input state are not integers.
        """
        if not isinstance(state, tuple) or len(state) != 4:
            raise ValueError("Input state must be a tuple containing four elements")
        if not all(isinstance(x, int) for x in state):
            raise TypeError("All elements of the input state must be integers")
        self.seed, self.a, self.c, self.m = state

    def set_seed(self, new_seed):
        """
        Sets the seed for the random number generator.

        :param new_seed: The new seed for the random number generator.
        :type new_seed: int
        """
        self.seed = new_seed

    def random(self):
        """
        Generates a random floating point number between 0 and 1.

        :return: A random floating point number between 0 and 1.
        :rtype: float
        """
        # Calculate the next seed using the linear congruential generator algorithm
        self.seed = (self.a * self.seed + self.c) % self.m
        # Return the seed as a floating point number between 0 and 1
        return self.seed / self.m

    def range(self, end, start=0, step=1):
        """
        Generates a random integer within a specified range.

        :param end: The end of the range.
        :type end: int
        :param start: The start of the range. Defaults to 0.
        :type start: int
        :param step: The step size. Defaults to 1.
        :type step: int
        :return: A random integer within the specified range.
        :rtype: int
        """
        random_value = self.random()
        value_range = end - start
        steps_in_range = value_range // step
        random_step = int(random_value * steps_in_range)
        result = start + random_step * step
        return result

    def int_range(self, start, end):
        """
        Generates a random integer within a specified range.

        :param start: The start of the range.
        :type start: int
        :param end: The end of the range.
        :type end: int
        :return: A random integer within the specified range.
        :rtype: int
        """
        return self.range(end+1, start)

    def float_range(self, start, end):
        """
        Generates a random floating point number within a specified range.

        :param start: The start of the range.
        :type start: float
        :param end: The end of the range.
        :type end: float
        :return: A random floating point number within the specified range.
        :rtype: float
        """
        random_value = self.random()
        value_range = end - start
        result = start + random_value * value_range
        return result
    
    def triangular(self, end=1, start=0, mid=None):
        """
        Generates a random floating point number within a specified range with a triangular distribution.

        The triangular distribution is a continuous probability distribution that has a triangular shape.
        It is defined by three parameters: start, end, and mid. The start and end parameters define the range of the distribution,
        while the mid parameter defines the mode of the distribution. If mid is not provided, it defaults to the midpoint between start and end.

        :param end: The end of the range. Defaults to 1.
        :type end: float
        :param start: The start of the range. Defaults to 0.
        :type start: float
        :param mid: The mode of the distribution. Defaults to the midpoint between start and end.
        :type mid: float
        :return: A random floating point number within the specified range with a triangular distribution.
        :rtype: float
        """
        if mid is None:
            mid = (start + end) / 2

        random_value = self.random()

        if random_value < (mid - start) / (end - start):
            return start + (random_value * (end - start) * (mid - start)) ** 0.5
        else:
            return end - ((1 - random_value) * (end - start) * (end - mid)) ** 0.5

    def choice(self, sequence):
        """
        Returns a random element from a given sequence.

        :param sequence: The sequence from which to select a random element.
        :type sequence: Sequence
        :return: A random element from the sequence.
        :rtype: Any
        """
        index = self.range(len(sequence))
        return sequence[index]

    def choices(self, sequence, weights=None, cum_weights=None, amount=1):
        """
        Returns a list of random elements from a given sequence.

        :param sequence: The sequence from which to select random elements.
        :type sequence: Sequence
        :param weights: A list of weights for each element in the sequence. Defaults to None.
        :type weights: List[float]
        :param cum_weights: A list of cumulative weights for each element in the sequence. Defaults to None.
        :type cum_weights: List[float]
        :param amount: The number of random elements to select. Defaults to 1.
        :type amount: int
        :return: A list of random elements from the sequence.
        :rtype: List[Any]
        :raises ValueError: If the length of weights or cum_weights is not equal to the length of the sequence.
        """
        if weights is None and cum_weights is None and amount == 1:
            return [self.choice(sequence)]

        if weights is not None and len(weights) != len(sequence):
            raise ValueError("The length of weights must be equal to the length of the sequence")

        if cum_weights is not None and len(cum_weights) != len(sequence):
            raise ValueError("The length of cum_weights must be equal to the length of the sequence")

        result = []
        for _ in range(amount):
            if weights is None and cum_weights is None:
                result.append(self.choice(sequence))
            elif cum_weights is not None:
                # Generate a random value between 0 and the last cumulative weight
                random_value = self.random() * cum_weights[-1]
                # Find the index of the first cumulative weight that is greater than or equal to the random value
                index = next(i for i, weight in enumerate(cum_weights) if weight >= random_value)
                result.append(sequence[index])
            else:
                # Calculate the cumulative sum of the weights
                cum_weights = [sum(weights[:i+1]) for i in range(len(weights))]
                # Generate a random value between 0 and the sum of the weights
                random_value = self.random() * sum(weights)
                # Find the index of the first weight that is greater than or equal to the random value
                index = next(i for i, weight in enumerate(cum_weights) if weight >= random_value)
                result.append(sequence[index])

        if isinstance(sequence, str):
            return ''.join(result)
        elif isinstance(sequence, tuple):
            return tuple(result)
        else:
            return result

        if isinstance(sequence, str):
            return ''.join(result)
        elif isinstance(sequence, tuple):
            return tuple(result)
        else:
            return result
    
    def sample(self, sequence, amount):
        """
        Returns a list of unique random elements from a given sequence.

        :param sequence: The sequence from which to select random elements.
        :type sequence: Sequence
        :param amount: The number of random elements to select.
        :type amount: int
        :return: A list of unique random elements from the sequence.
        :rtype: List[Any]
        :raises ValueError: If amount is greater than the length of the sequence.
        """
        if amount > len(sequence):
            raise ValueError("Amount cannot be greater than the length of the sequence")

        sequence_list = list(sequence)
        result = []
        for _ in range(amount):
            element = self.choice(sequence_list)
            result.append(element)
            sequence_list.remove(element)

        if isinstance(sequence, str):
            return ''.join(result)
        elif isinstance(sequence, tuple):
            return tuple(result)
        else:
            return result
    
    def shuffle(self, sequence):
        """
        Reorders the elements in a given sequence.

        :param sequence: The sequence to be shuffled.
        :type sequence: Sequence
        :return: The shuffled sequence.
        :rtype: Sequence
        """
        sequence_list = list(sequence)
        for i in range(len(sequence_list) - 1, 0, -1):
            j = self.range(i + 1)
            sequence_list[i], sequence_list[j] = sequence_list[j], sequence_list[i]

        if isinstance(sequence, str):
            return ''.join(sequence_list)
        elif isinstance(sequence, tuple):
            return tuple(sequence_list)
        else:
            return sequence_list

# Create a new generator with the default seed
generator = RandomGenerator()
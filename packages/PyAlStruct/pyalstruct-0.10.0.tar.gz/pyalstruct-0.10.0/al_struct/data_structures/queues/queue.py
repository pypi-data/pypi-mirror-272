from typing import Any

from utils.exceptions import EmptyQueueException
from al_struct.utils.nodes import Node


class Queue:
    """Simple queue data structure."""

    def __init__(self):
        """Initialize the queue with an empty stack."""
        self._front: Node | None = None
        self._back: Node | None = None
        self._size: int = 0

    def __str__(self):
        values = []
        temp: Node = self._front
        while temp:
            values.append(str(temp.data))
            temp = temp.next
        del temp
        return " | ".join(values)

    def __repr__(self):
        return f"PyAlStruct.Queue({str(self)})"

    def __len__(self):
        """Return len(self)"""
        return self._size

    def __iter__(self):
        """Initialize an iterator over the linked list."""
        self._current = self._front
        return self

    def __next__(self):
        """Get the next element in the iteration."""
        if self._current:
            current = self._current
            self._current = self._current.next
            return current.data
        else:
            raise StopIteration

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """
        Check if the queue is empty.
        :returns: bool -- True if the queue is empty, otherwise False.
        """
        return self._front is None

    def enqueue(self, item: Any) -> None:
        """
        Add a new node with item to the back of the queue.
        :param item: The item to be added to the queue.
        """
        node: Node = Node(item)
        if self._front is None:
            self._front = node
            self._back = node
            return
        self._back.next = node
        self._back = node

    def dequeue(self) -> None:
        """
        Removes and returns an item from the front of the queue.
        :return: The item at the front of the queue if exists.
        :raise EmptyQueueException: If the stack is empty.
        """
        if self._front is None:
            raise EmptyQueueException()
        if self._front == self._back:
            self._front = None
        data: Any = self._front.data
        temp: Node = self._front
        self._front = self._front.next
        del temp
        return data

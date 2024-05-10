from typing import Any

from utils.exceptions import EmptyStackException
from al_struct.utils.nodes import Node


class Stack:
    """Simple stack data structure."""

    def __init__(self):
        self._top: Node = None
        self._size: int = 0

    def __str__(self):
        values = []
        temp: Node = self._top
        while temp:
            values.append(str(temp.key))
            temp = temp.next
        del temp
        return ", ".join(values)

    def __repr__(self):
        return f"PyAlStruct.Stack({str(self)})"

    def __len__(self):
        """Return len(self)"""
        return self._size

    def __iter__(self):
        """Initialize an iterator over the linked list."""
        self._current = self._top
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
        Check if the stack is empty.
        :returns: bool -- True if the stack is empty, otherwise False.
        """
        return self._top is None

    def push(self, item: Any) -> None:
        """
        Add a new item to the top of the stack.
        :param item: The item to be added to the stack.
        """
        node: Node = Node(item)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self) -> None:
        """
        Removes and returns an item from the top of the stack.
        :return: The item at the top of the stack if exists.
        :raise EmptyStackException: If the stack is empty.
        """
        if self._top is None:
            raise EmptyStackException()
        item = self._top.data
        temp = self._top
        self._top = self._top.next
        del temp
        self._size -= 1
        return item

    def peek(self) -> Any:
        """
        Return the item in the top of the stack without removing it.
        :return: The item of the node at the top of the stack.
        """
        if not self._top:
            raise EmptyStackException()
        return self._top.data

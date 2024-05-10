from typing import Any

from al_struct.utils.exceptions import NodeNotFoundException, EmptyListException
from al_struct.utils.nodes import Node


class BaseLinkedList:
    """Base linked list data structure."""

    def __init__(self):
        """Initialize an empty base linked list."""
        self._head: Node | None = None
        self._size: int = 0

    def __len__(self):
        """Return len(self)"""
        return self._size

    def __iter__(self):
        """Initialize an iterator over the linked list."""
        self._current = self._head
        return self

    def __next__(self):
        """Get the next element in the iteration."""
        if self._current:
            current: Node = self._current
            self._current = self._current.next
            return current.data
        else:
            raise StopIteration

    @property
    def size(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        """
        Check if the linked list is empty.
        :returns: bool -- True if the linked list is empty, otherwise False.
        """
        return self._head is None

    def get_head(self) -> Any:
        """
        Get data of the first node in the list.
        :return: The data of the first node in the list.
        """
        if self._head is None:
            raise EmptyListException()
        return self._head.data

    def get(self, data: Any) -> Any:
        """
        Return the node that contains data if exist in the list.
        :param data: The data to search for.
        :return: Node -- The node that contains data if exists.
        """
        temp: Node = self._head
        while temp:
            if temp.data == data:
                return temp
            temp = temp.next
        raise NodeNotFoundException(data)

    def search(self, data: Any) -> bool:
        """
        Return boolean value if data exists in the list.
        :param data: The data to search for.
        :return: bool -- True if data exists, otherwise False.
        :raises NodeNotFoundException: If the data is not found in the linked list.
        """
        temp: Node = self._head
        while temp:
            if temp.data == data:
                return True
            temp = temp.next
        return False

    def index(self, data: Any) -> int:
        """
        Find the index of the first occurrence of data in the linked list.
        :param data: The data to search for in the list.
        :returns: int -- The index of the first occurrence of the data.
        :raises NodeNotFoundException: If the data is not found in the linked list.
        """
        index: int = 0
        temp: Node = self._head
        while temp:
            if temp.data == data:
                return index
            temp = temp.next
            index += 1
        raise NodeNotFoundException(data)

    def delete(self, data: Any) -> None:
        """
        Delete the first occurrence of data in the linked list.
        :param data: The data to be deleted
        """
        if self._head is None:
            raise EmptyListException()
        current: Node = self._head
        while current:
            if current.data == data:
                temp: Node = current
                current = current.next
                del temp
                self._size -= 1
                return
            current = current.next
        raise NodeNotFoundException(data)

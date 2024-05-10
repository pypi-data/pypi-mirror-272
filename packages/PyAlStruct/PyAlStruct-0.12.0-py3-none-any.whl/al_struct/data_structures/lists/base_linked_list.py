from typing import Any

from al_struct.utils.exceptions import EmptyListException, NodeNotFoundException
from al_struct.utils.nodes import Node, BinaryNode


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
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                return temp
            temp = temp.next
        raise NodeNotFoundException(data)

    def get_all(self, data: Any) -> list[Any]:
        """
        Return a list of all the nodes data that contain data if exist in the list.
        :param data: The data to search for.
        :return: list[Any] -- List of all the nodes data that contain data in the list.
        """
        nodes: list[Any] = []
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                nodes.append(temp.data)
            temp = temp.next
        return nodes

    def search(self, data: Any) -> bool:
        """
        Return boolean value if data exists in the list.
        :param data: The data to search for.
        :return: bool -- True if data exists, otherwise False.
        :raises NodeNotFoundException: If the data is not found in the linked list.
        """
        temp: Node | BinaryNode = self._head
        while temp:
            if temp.data == data:
                return True
            temp = temp.next
        return False

    def index(self, data: Any) -> int:
        """
        Find the index of the first occurrence of data in the list.
        :param data: The data to search for in the list.
        :returns: int -- The index of the first occurrence of the data in the list.
        :raises NodeNotFoundException: If the data is not found in the list.
        """
        index: int = 0
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                return index
            temp = temp.next
            index += 1
        raise NodeNotFoundException(data)

    def indexes(self, data: Any) -> list[int]:
        """
        Find the indexes of the all occurrences of data in the list.
        :param data: The data to search for in the list.
        :return: list[int] -- List of indexes of all occurrences of the data in the list.
        """
        index: int = 0
        indexes: list[int] = []
        temp: Node | BinaryNode = self._head
        while temp is not None:
            if temp.data == data:
                indexes.append(index)
            temp = temp.next
            index += 1
        return indexes

    def delete(self, data: Any) -> Any:
        """
        Delete the first occurrence of data in the linked list.
        :param data: The data to be deleted
        """
        if self._head is None:
            raise EmptyListException()
        if self._head.data == data:
            temp: Node | BinaryNode = self._head
            value: Any = self._head.data
            self._head = self._head.next
            if type(self._head) is BinaryNode:
                self._head.prev = None
            del temp
            self._size -= 1
            return value
        current: Node | BinaryNode = self._head
        next_node: Node | BinaryNode = self._head.next
        while next_node is not None:
            if next_node.data == data:
                temp: BinaryNode = next_node
                value: Any = temp.data
                current.next = next_node.next
                if type(next_node.next) is BinaryNode:
                    next_node.next.prev = current
                del temp
                self._size -= 1
                return value
            current = current.next
            next_node = next_node.next
        raise NodeNotFoundException(data)

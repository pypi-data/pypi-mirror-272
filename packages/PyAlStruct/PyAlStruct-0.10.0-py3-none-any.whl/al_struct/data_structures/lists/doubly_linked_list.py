from typing import Any

from al_struct.utils.exceptions import EmptyListException
from al_struct.utils.nodes import Node
from al_struct.data_structures.lists.base_linked_list import BaseLinkedList


class DoublyLinkedList(BaseLinkedList):
    """Doubly Linked List data structure."""

    def __init__(self):
        """Initialize empty doubly linked list."""
        super().__init__()
        self._tail: Node | None = None

    def __str__(self):
        values = []
        temp= self._head
        while temp:
            values.append(str(temp.key))
            temp = temp.next
        del temp
        return " <-> ".join(values)

    def __repr__(self):
        return f"PyAlStruct.DoublyLinkedList({str(self)})"

    def is_empty(self) -> bool:
        """
        Check if the linked list is empty.
        :returns: bool -- True if the linked list is empty, otherwise False.
        """
        return self._head is None

    def prepend(self, data: Any) -> None:
        """
        Add a new node with data to the end of the list.
        :param data: The data to be added to the list.
        """
        node = Node(data)
        if self._head is not None:
            node.next = self._head
        self._head = node
        if self._head is None:
            self._tail = self._head
        self._size += 1

    def append(self, data: Any) -> None:
        """
        Add a new node with data to the end of the list.
        :param data: The data to be added to the list.
        """
        node = Node(data)
        if self._head is None:
            self._head = node
            self._tail = node
        else:
            self._tail.next = node
            self._tail = node
        self._size += 1

    def get_tail(self) -> Any:
        """
        Get data of the last node in the list.
        :return: The data of the last node in the list.
        """
        if self._tail is None:
            raise EmptyListException()
        return self._tail.data

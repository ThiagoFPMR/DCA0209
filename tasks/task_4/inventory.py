import csv
from typing import Union


class Inventory:
    """
    The inventory class represents the inventory of laptops in the store.

    It can be instantiated by passing it the path to a CSV file containing
    the inventory.

    Parameters
    ----------
    csv_path : str
        The path to the CSV file containing the inventory.

    Attributes
    ----------
    header : list of str
        The header of the CSV file.
    rows : list of list of str
        A list of rows of the CSV file.
    prices : set of int
        A set containing all laptop prices.
    id_to_row : dict
        A dictionary mapping laptop ids to rows.
    rows_by_price : list of list of str
        A list of rows sorted by price.

    Examples
    --------
    >>> inventory = Inventory('laptops.csv')
    """

    def __init__(self, csv_path: str):
        """
        Create an inventory from a CSV file.

        Parameters
        ----------
        csv_path : str
            The path to the CSV file containing the inventory.

        Returns
        -------
        Inventory
            A new inventory instance.
        """
        with open(csv_path, "r") as file:
            reader = csv.reader(file)
            self.header = next(reader)
            self.rows = []
            self.prices = set()
            self.id_to_row = dict()
            for i, row in enumerate(reader):
                row[-1] = int(row[-1])
                self.rows.append(row)
                self.prices.add(row[-1])
                self.id_to_row[row[0]] = i
            row_price = lambda row: row[-1]
            row_specs = lambda row: (row[7], row[8])
            preprocessed_rows = self.rows.copy()
            for i in range(len(preprocessed_rows)):
                preprocessed_rows[i][7] = int(preprocessed_rows[i][7].replace("GB", ""))
                storage = [
                    s for s in preprocessed_rows[i][8].split() if "GB" in s or "TB" in s
                ]
                storage = [
                    int(s.replace("GB", "")) if "GB" in s else s for s in storage
                ]
                storage = [
                    1000 * int(float(s.replace("TB", ""))) if type(s) == str else s
                    for s in storage
                ]
                preprocessed_rows[i][8] = sum(storage)
            self.rows_by_price = sorted(self.rows, key=row_price)
            self.rows_by_specs = sorted(preprocessed_rows, key=row_specs)

    def get_laptop_from_id(self, laptop_id: str) -> Union[list, None]:
        """
        Find a laptop from its id.

        Parameters
        ----------
        laptop_id : str
            The id of the laptop to find.

        Returns
        -------
        None
            If the laptop id does not exist.
        list
            A list containing the laptop information.
        """
        result = None
        for row in self.rows:
            if row[0] == laptop_id:
                result = row
        return result

    def get_laptop_from_id_fast(self, laptop_id: str) -> Union[list, None]:
        """
        Find a laptop from its id, but FAST.

        Parameters
        ----------
        laptop_id : str
            The id of the laptop to find.

        Returns
        -------
        None
            If the laptop id does not exist.
        list
            A list containing the laptop information.
        """
        # Speeds up the search by using a dictionary
        if laptop_id in self.id_to_row.keys():
            return self.rows[self.id_to_row[laptop_id]]
        return None

    def check_promotion_dollars(self, dollars: int) -> bool:
        """
        Ensure that there are laptops in the inventory whose price is
        exactly the given amount, or that there are two laptops whose price adds
        up to the given amount.

        Parameters
        ----------
        dollars : int
            The dollar amount to check.

        Returns
        -------
        bool
            True if there are laptops whose price is exactly the given amount,
            or that there are two laptops whose price adds up to the given
            amount. False otherwise.
        """
        for row in self.rows:
            if row[-1] == dollars:
                return True
        for row1 in self.rows:
            for row2 in self.rows:
                if row1[-1] + row2[-1] == dollars:
                    return True
        return False

    def check_promotion_dollars_fast(self, dollars: int) -> bool:
        """
        Ensure that there are laptops in the inventory whose price is
        exactly the given amount, or that there are two laptops whose price adds
        up to the given amount. FAST.

        Parameters
        ----------
        dollars : int
            The dollar amount to check.

        Returns
        -------
        bool
            True if there are laptops whose price is exactly the given amount,
            or that there are two laptops whose price adds up to the given
            amount. False otherwise.
        """
        # Speeds up the singular laptop search by using a set
        if dollars in self.prices:
            return True
        # Speeds up the double laptop search by checking if the difference
        # between the target and any laptop price is zero.
        for row in self.rows:
            if (dollars - row[-1]) in self.prices:
                return True
        return False

    def _find_first_laptop_more(
        self, target: int, start: int, end: int, key: int, rows_by: list
    ) -> int:
        """
        Find the first laptop in the inventory (from left to right)
        with a value for key that is greater than the target value.

        Parameters
        ----------
        target : int
            The target value to compare against.
        start : int
            The starting index of the search.
        end : int
            The ending index of the search.
        key : int
            The index of the value to compare against.

        Returns
        -------
        int
            The index of the first laptop in the inventory (from left to right)
            with a value for key that is greater than the target value.
        """
        if start == end:
            if rows_by[start][key] > target:
                return start
            else:
                return -1
        elif start > end:
            return -1
        else:
            mid = (start + end) // 2
            if rows_by[mid][key] > target:
                return self._find_first_laptop_more(target, start, mid, key, rows_by)
            else:
                return self._find_first_laptop_more(target, mid + 1, end, key, rows_by)

    def _find_first_laptop_less(
        self, target: int, start: int, end: int, key: int, rows_by: list
    ) -> int:
        """
        Find the first laptop in the inventory (from right to left)
        with a value for key that is lesser than the target value.

        Parameters
        ----------
        target : int
            The target value to compare against.
        start : int
            The starting index of the search.
        end : int
            The ending index of the search.
        key : int
            The index of the value to compare against.

        Returns
        -------
        int
            The index of the first laptop in the inventory (from left to right)
            with a value for key that is greater than the target value.
        """
        if start == end:
            if rows_by[start][key] < target:
                return start
            else:
                return -1
        elif start > end:
            return -1
        elif start + 1 == end:
            if rows_by[end][key] < target:
                return end
            return start
        else:
            mid = (start + end) // 2
            if rows_by[mid][key] < target:
                return self._find_first_laptop_less(target, mid, end, key, rows_by)
            else:
                return self._find_first_laptop_less(
                    target, start, mid - 1, key, rows_by
                )

    def find_first_laptop_more_expensive(self, price: int) -> int:
        """
        Find the first laptop in the inventory (from left to right)
        with a price that is greater than the target price.

        Parameters
        ----------
        price : int
            The target price to compare against.

        Returns
        -------
        int
            The index of the first laptop in the inventory (from left to right)
            with a price that is greater than the target price.
        """
        return self._find_first_laptop_more(
            price, 0, len(self.rows_by_price) - 1, -1, self.rows_by_price
        )

    def find_first_laptop_less_expensive(self, price: int) -> int:
        """
        Find the first laptop in the inventory (from right to left)
        with a price that is lesser than the target price.

        Parameters
        ----------
        price : int
            The target price to compare against.

        Returns
        -------
        int
            The index of the first laptop in the inventory (from right to left)
            with a price that is lesser than the target price.
        """
        return self._find_first_laptop_less(
            price, 0, len(self.rows_by_price) - 1, -1, self.rows_by_price
        )

    def find_laptops_between_prices(self, min_price: int, max_price: int) -> list:
        """
        Find all laptops in the inventory whose price is between the
        given prices.

        Parameters
        ----------
        min_price : int
            The minimum price to compare against.
        max_price : int
            The maximum price to compare against.

        Returns
        -------
        list
            A list of laptops whose price is between the given prices.
        """
        first_laptop_more_expensive = self.find_first_laptop_more_expensive(max_price)
        first_laptop_less_expensive = self.find_first_laptop_less_expensive(min_price)

        if first_laptop_more_expensive == -1 and first_laptop_less_expensive == -1:
            return []
        elif first_laptop_more_expensive == -1:
            return self.rows_by_price[first_laptop_less_expensive + 1 :]
        elif first_laptop_less_expensive == -1:
            return self.rows_by_price[:first_laptop_more_expensive]

        return self.rows_by_price[
            first_laptop_less_expensive + 1 : first_laptop_more_expensive
        ]

    def find_cheapest_laptop_with_specs(self, ram: int, storage: int) -> list:
        """
        Find the cheapest laptop in the inventory that has the specified
        amount of RAM and storage.

        Parameters
        ----------
        ram : int
            The amount of RAM to compare against (in GB).
        storage : int
            The amount of storage to compare against (in GB).

        Returns
        -------
        list
            The cheapest laptop in the inventory that has the specified
            amount of RAM and storage.
        """
        # Limiting the search to laptops with the desired amount of RAM
        start = self._find_first_laptop_less(
            ram, 0, len(self.rows_by_price) - 1, 7, self.rows_by_specs
        )
        end = self._find_first_laptop_more(
            ram, 0, len(self.rows_by_price) - 1, 7, self.rows_by_specs
        )

        # If there are no laptops with the desired amount of RAM, return -1
        if start == -1 and end == -1:
            return -1
        elif start == -1:
            start = 0
        elif end == -1:
            end = len(self.rows_by_price) - 1

        if start == len(self.rows_by_price) - 1 or end == 0:
            return -1

        # Gettng the index of the first laptop with the desired amount of storage and RAM
        start_with_specs = self._find_first_laptop_less(
            storage, start + 1, end - 1, 8, self.rows_by_specs
        )
        end_with_specs = self._find_first_laptop_more(
            storage, start + 1, end - 1, 8, self.rows_by_specs
        )  # here for sanity check

        # If there are no laptops with the desired amount of storage and RAM, return -1
        if start_with_specs == -1 and end_with_specs == -1:
            return -1
        elif start_with_specs == -1:
            start_with_specs = start
        elif end_with_specs == -1:
            end_with_specs = end

        # If there are no laptops with the desired amount of storage and RAM, return -1
        if start_with_specs == len(self.rows_by_price) - 1 or end_with_specs == 0:
            return -1

        return self.rows_by_price[start_with_specs + 1]

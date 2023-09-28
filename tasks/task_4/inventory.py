import csv


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

    def __init__(self, csv_path):
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
            row_price = lambda row: (row[-1], row[7], row[8])
            self.rows_by_price = sorted(self.rows, key=row_price)

    def get_laptop_from_id(self, laptop_id):
        """
        R
        """
        result = None
        for row in self.rows:
            if row[0] == laptop_id:
                result = row
        return result

    def get_laptop_from_id_fast(self, laptop_id):
        if laptop_id in self.id_to_row.keys():
            return self.rows[self.id_to_row[laptop_id]]
        return None

    def check_promotion_dollars(self, dollars):
        for row in self.rows:
            if row[-1] == dollars:
                return True
        for row1 in self.rows:
            for row2 in self.rows:
                if row1[-1] + row2[-1] == dollars:
                    return True
        return False

    def check_promotion_dollars_fast(self, dollars):
        if dollars in self.prices:
            return True
        for row in self.rows:
            if (dollars - row[-1]) in self.prices:
                return True
        return False

    def find_first_laptop_more_expensive(self, price):
        range_start = 0
        range_end = len(self.rows_by_price) - 1
        while range_start < range_end:
            range_middle = (range_end + range_start) // 2
            found_price = self.rows_by_price[range_middle][-1]
            if found_price > price:
                range_end = range_middle
            else:
                range_start = range_middle + 1
        if self.rows_by_price[range_start][-1] <= price:
            return -1
        return range_start

    def find_first_laptop_less_expensive(self, price):
        range_start = 0
        range_end = len(self.rows_by_price) - 1
        while range_start < range_end:
            range_middle = (range_end + range_start) // 2
            found_price = self.rows_by_price[range_middle][-1]
            if found_price < price:
                range_start = range_middle
            else:
                range_end = range_middle - 1
            if range_end - range_start == 1:
                if self.rows_by_price[range_end][-1] < price:
                    range_start = range_start + 1
                else:
                    range_end = range_end - 1
        if self.rows_by_price[range_end][-1] >= price:
            return -1
        return range_start

    def find_laptops_between_prices(self, min_price, max_price):
        first_laptop_more_expensive = self.find_first_laptop_more_expensive(max_price)
        first_laptop_less_expensive = self.find_first_laptop_less_expensive(min_price)

        if first_laptop_more_expensive == -1 and first_laptop_less_expensive == -1:
            return []
        elif first_laptop_more_expensive == -1:
            return self.rows_by_price[first_laptop_less_expensive + 1 :]
        elif first_laptop_less_expensive == -1:
            return self.rows_by_price[:first_laptop_more_expensive]

        print(first_laptop_less_expensive + 1, first_laptop_more_expensive)
        return self.rows_by_price[
            first_laptop_less_expensive + 1 : first_laptop_more_expensive
        ]

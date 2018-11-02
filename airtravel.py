class Flight:
    """A flight with a particular passenger aircraft """

    def __init__(self,number,aircraft):
        if not number[:2].isalpha():
            raise ValueError("No airline code in '{}'".format(number))

        if not number[:2].isupper():
            raise ValueError("Invalid airline code '{}'".format(number))

        if not (number[2:].isdigit() and int(number[2:]) <= 9999):
            raise ValueError("Invalid route number'{}'".format(number))

        self._number = number
        self._aircraft = aircraft

        rows, seats = self._aircraft.seating_plan()
        self._seating = [None] + [{letter: None for letter in seats} for _ in rows]

    def number(self):
        return self._number

    def airline(self):
        return self._number[:2]

    def aircraft_model(self):
        return self._aircraft.model()

    def allocate_seat(self, seat, passenger):
        """Allocate a sit to a passenger.

        Args:
            seat: A seat designator such as '12C' or '21F'.
            passenger: The passenger name.

        Raises:
            ValueError: If the seat is unabailable.
        """
        rows, seat_letters = self._aircraft.seating_plan()

        letter = seat[-1]
        if letter not in seat_letters:
            raise ValueError("Invalid seat letter '{}'".format(letter))

        row_text = seat[:-1]
        try:
            row = int(row_text)
        except ValueError:
            raise ValueError("Invalid seat row '{}'".format(row_text))

        if row not in rows:
            raise ValueError("Invalid row number '{}'".format(row))

        if self._seating[row][letter] is not None:
            raise ValueError("Seat {} already occupied.".format(seat))

        self._seating[row][letter] = passenger

    def num_available_seats(self):
        return sum(sum(1 for s in row.values() if s is None)
                for row in self._seating if row is not None)

    def make_boarding_cards(self, card_printer):
        for passenger, seat in sorted(self._passenger_seats()):
            card_printer(passenger, seat, self.number(), self.aircraft_model())

    def _passenger_seats(self):
        """An iterable series of passenger seating allocations."""
        row_numbers, seat_letters = self._aircraft.seating_plan()
        for row in row_numbers:
            for letter in seat_letters:
                passenger = self._seating[row][letter]
                if passenger is not None:
                    yield(passenger, "{}{}".format(row, letter))


class Aircraft:

    def num_seats(self):
        rows, row_seats = self.seating_plan()
        return len(rows) * len(row_seats)

    def __init__(self, registration):
        self._registration = registration
    # def __init__(self, registration, model, num_rows, num_seats_per_row):
    #     self._registration = registration
    #     self._model = model
    #     self._num_rows = num_rows
    #     self._num_seats_per_row = num_seats_per_row

    def registration(self):
        return self._registration

    # def model(self):
    #     return self._model

    # def seating_plan(self):
    #     return (range(1, self._num_rows + 1), 
    #             "ABCDEFGHJK"[:self._num_seats_per_row])

    def seating_plan(self):
        return None


class Boeing777(Aircraft):
    # def __init__(self, registration):
    #     self._registration = registration

    # def registration(self):
    #     return self._registration

    def model(self):
        return "Boeing 777"

    def seating_plan(self):
        return range(1, 56), "ABCDEFGHJK"

    # def num_seats(self):
    #     rows, row_seats = self.seating_plan()
    #     return len(rows) * len(row_seats)

class Airbus319(Aircraft):
    # def __init__(self, registration):
    #     self._registration = registration

    # def registration(self):
    #     return self._registration

    def model(self):
        return "Airbus A319"

    def seating_plan(self):
        return range(1, 23), "ABCDEF"

    # def num_seats(self):
    #     rows, row_seats = self.seating_plan()
    #     return len(rows) * len(row_seats)


def make_flight():
    # f = Flight("BA758", Aircraft("G-EUPT", "Airbus A319", num_rows=22, num_seats_per_row=6))
    # f.allocate_seat('12A', 'Guido van Rossum')
    # f.allocate_seat('15F', 'Bjarne Stroustrup')
    # f.allocate_seat('15E', 'Andres Hejlsberg')
    # f.allocate_seat('1C', 'John McCarthy')
    # f.allocate_seat('1D', 'Richard Hickey')

    f = Flight("BA758", Airbus319("G-EUPT"))
    f.allocate_seat('12A', 'Guido van Rossum')
    f.allocate_seat('15F', 'Bjarne Stroustrup')
    f.allocate_seat('15E', 'Andres Hejlsberg')
    f.allocate_seat('1C', 'John McCarthy')
    f.allocate_seat('1D', 'Richard Hickey')

    g = Flight("AF72", Boeing777("F-GSPS"))
    g.allocate_seat('55K', 'Larry Wall')
    g.allocate_seat('33G', 'Yukihiro Matsumoto')
    g.allocate_seat('4B', 'Brian Kernighan')
    g.allocate_seat('4A', 'Dennis Ritchie')

    return f, g

def console_card_printer(passenger, seat, flight_number, aircraft):
    output = "| Name: {0}"      \
             "  Flight: {1}"    \
             "  Seat: {2}"      \
             "  Aircraft: {3}"  \
             " |".format(passenger, flight_number, seat, aircraft)

    banner = "+" + "-" * (len(output) - 2) + "+"
    border = "|" + " " * (len(output) - 2) + "|"
    lines = [banner, border, output, border, banner]
    card = "\n".join(lines)
    print(card)
    print()

class Tour:
    def __init__(self, tour_id, destination, price, duration, seats):
        self.tour_id = tour_id
        self.destination = destination
        self.price = float(price)
        self.duration = int(duration)
        self.seats = int(seats)


class Customer:
    def __init__(self, customer_id, name, phone, email):
        self.customer_id = customer_id
        self.name = name
        self.phone = phone
        self.email = email


class Booking:
    def __init__(self, customer, tour):
        self.customer = customer
        self.tour = tour


# In-memory storage
tours = []
customers = []
bookings = []


def find_tour(tour_id):
    for tour in tours:
        if tour.tour_id == tour_id:
            return tour
    return None


def find_customer(customer_id):
    for customer in customers:
        if customer.customer_id == customer_id:
            return customer
    return None

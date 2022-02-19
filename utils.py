
def nonZeroPrice(func):
    def deco(self, price):
        if not price:
            raise ValueError("Please provide a valid value for Price")
        else:
            return func(self, price)

    return deco
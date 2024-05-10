class MathOperations():
    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2
    def add(self):
        return self.num1 + self.num2
    def sub(self):
        return self.num1 - self.num2
    def mult(self):
        return self.num1 * self.num2
    def div(self):
        if self.num2 == 0:
            raise Exception('Sorry, I cannot divide by 0!')
        else:
            return self.num1 / self.num2
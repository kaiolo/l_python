class Accumulator :
    def __init__(self, n):
        self.data = [0.0] * n
    def add (self , *args):
        self.data = [a+float(b) for a, b in zip(self.data , args)]
        return self.data
    def reset(self):
        self.data = [0.0]*len(self.data)
    def __getitem__(self , idx):
        return self.data[idx]
if __name__ == "__main__":
    meric = Accumulator(3)
    meric.add(1, 2, 3)
    meric.reset()
    print(meric[0])  # Output: 1.0
    print(meric[1])  # Output: 2.0
    print(meric[2])  # Output: 3.0
   
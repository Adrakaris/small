# recursion
# 
# when a function calls itself

# Recursive function:
# - base case: "lowest level" case, where the function does NOT call itself
# - recursive case: where the function DOES call itself

# factorial
# 5! = 5 * 4 * 3 * 2 * 1
# 0! = 1

# iteration: loops
def factorial_iterative(n:int) -> int:
    if n < 0:
        raise ValueError("no")

    if n == 0:
        return 1

    total = 1
    while n > 0:
        total *= n 
        n -= 1
    return total


# recursion: function calls inside function calls 
def factorial_recursive(n:int) -> int:
    print(f"fac called with {n}")
    # base case:
    if n < 0:
        raise ValueError("no")
    if n == 0:
        return 1
    else:
        return n * factorial_recursive(n-1)

# 5! = 5 * 4 * 3 * 2 * 1
# 5! = 5 * 4!



if __name__ == "__main__":
    factorial = factorial_recursive
    print(f"fac 0 = {factorial(0)}")
    print(f"fac 3 = {factorial(3)}")
    print(f"fac 5 = {factorial(5)}")
    print(f"fac 100 = {factorial(100)}")

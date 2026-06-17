print("Start small. Ship something.")
#1 Reverse string
text = "Hello"
rev = text[::-1]
print(rev)
rev = ""
for ch in text:
    rev = ch + rev
    
print(rev)

#2 Factorial
def fact(n):
    if n<=1:
        return 1
        
    return n * fact(n-1)
    
print(fact(10))
#3 Freq character
text ="aaaabbcddda"
freq={}
for ch in text:
    freq[ch] = freq.get(ch, 0) + 1

print(freq)
max_freq = max(freq, key=freq.get)
print(f" Max character {max_freq} and it is present {freq[max_freq]} times")

#4 Fibonacci series
fib=[0, 1]
n = 10
for i in range(n):
    fib.append(fib[-1]+fib[-2])

print(f" Fibonacci series for {n} value {fib}")

#5 Palindrome check
text = "radar"
if text == text[::-1]:
    print(f" The given text '{text}' is palindrome")
else:
    print(f" The given text '{text}' is not palindrome")

#6 Fine max number in a list 
numbers = [5, 8, 2, 7, 40, 35, 22, 75, 10]
first_max = second_max= numbers[0]
for num in numbers:
    if num > first_max:
        second_max = first_max
        first_max = num
    if num > second_max and num != first_max:
        second_max = num

print(f" First max {first_max}  and second max {second_max}")

#7 URL Encode pattern
text ="aaaabbcddda"
result = ""
count=0
for i in range(len(text)):
    if text[i] == text[i-1]:
        count +=1
    else:
        result+=text[i-1]+str(count)
        count=1

result+=text[-1]+str(count)

print(result)

#8 Anagrams
s1 = "silent"
s2 = "listen"
# logics same text with same frequent present in different orders.
clear_s1 = s1.lower().strip()
clear_s2 = s2.lower().strip()
if sorted(clear_s1) == sorted(clear_s2):
    print(f"The given text '{s1}' and  '{s2}' both are Anagram ")
else:
    print(f"The given text '{s1}' and  '{s2}' both are not Anagram ")

#9 Count vowels in text
text ="Hello world"
vowels = "AEIOUaeiou"
presented_vowels = []
for ch in text:
    if ch in vowels  and ch   not in presented_vowels:
        presented_vowels.append(ch)
print(presented_vowels)


#10 Permutations - How many words possible to print
text = "aegest"
from itertools import permutations
unique_words = set("".join(p) for p in permutations(text))
print(len(unique_words))


# Find dublicates values
numbers = [5, 8, 2, 7, 40, 35, 8, 22, 75, 2, 10]
unique = []
seen = []
for num in numbers:
    if num not in unique:
        unique.append(num)
    else:
        seen.append(num)
        unique.remove(num)

print(seen)
print(unique)

numbers = [5, 2, 8, 1, 3]
n = len(numbers)
for i in range(n):
    for j in range(0, n-i-1):
        if numbers[j] > numbers[j+1]:
            print(n-i-1)
            numbers[j], numbers[j+1] = numbers[j+1] , numbers[j]

print(numbers)

# check prime
import math

def is_prime(n):
    if n <=1: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(math.isqrt(n))+ 1, 2):
        if n%i ==0: return False
    return True

print(is_prime(1025))


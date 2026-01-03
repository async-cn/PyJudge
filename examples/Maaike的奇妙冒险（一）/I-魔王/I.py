n = int(input())
maxa = 0
mina = 10**9
for i in range(n):
    a = int(input())
    if a > maxa:
        maxa = a
    if a < mina:
        mina = a
print(maxa, mina)
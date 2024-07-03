import sys
import math

mb = open("./mb.txt","w")

mb.write("max_radix endpoints topology\n")

qs = [3,4,5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37, 41, 43]
deltas = [-1,0,1,-1, 0, 1, -1,  1,  0,  1, -1, -1,  1, -1,  1, -1,  0,  1,  1, -1]

assert(len(qs) == len(deltas))

for i in range(0,len(qs)):
  q = qs[i]
  delta = deltas[i]

  N = 2*q*q
  k = (3*q - delta)/2.0

  mb.write(str(k) + ' ' + str(N) + " SF\n")


qs = [3, 4, 5, 7, 8, 9, 11, 13, 16, 17, 19, 23, 25, 27, 29, 31, 32, 37, 41, 43, 47, 49, 53, 59, 61]

for i in range(0,len(qs)):
  q = qs[i]

  N = q*q + q + 1
  k = q+1 

  mb.write(str(k) + ' ' + str(N) + " ER\n")


qs = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39, 42, 45, 48, 51, 54, 57, 60]

for i in range(0,len(qs)):
  q = qs[i]

  N = (q/3 + 1)*(q/3 + 1)
  k = q 

  mb.write(str(k) + ' ' + str(N) + " HX\n")


qs = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64]

for i in range(0,len(qs)):
  q = qs[i]

  k = q 
  N = 3*k / 2 

  mb.write(str(k) + ' ' + str(N) + " FT2\n")

  N = 3*(k/2)*(k/2) - 3*(k/2) + 3

  mb.write(str(k) + ' ' + str(N) + " OFT\n")


for i in range(0, 64):

  k = i
  N = k*k + 1

  mb.write(str(k) + ' ' + str(N) + " Moore_Bound\n")


mb.close()

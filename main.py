from __future__ import print_function
import math
from collections import defaultdict

TPIcombinations = defaultdict(set)
combinations = defaultdict(set)
changeGears = [45, 48, 48, 50, 52, 60, 70, 77, 81, 100, 120, 127]
changeGears = [float(v) for v in changeGears]
screwGears = [8, 9, 10, 11, 12, 13, 14, 15, 19, 16, 18, 20, 22, 24, 26, 28, 30, 38, 32, 36, 40, 44, 48, 52, 56, 60, 76]
screwGears = [float(v) for v in screwGears]
diametralPitch = 24.0
outputShaftRadius = 0.5

# simple gear train
counter = 0
gearsA = list(changeGears)
for a in gearsA:
  if a < 30 or a > 81: continue  # as per manual
  gearsB = list(gearsA)
  gearsB.remove(a)
  for b in gearsB:
    if a + b < 105: continue  # as per manual (modified)
    gearsD = list(gearsB)
    gearsD.remove(b)
    for d in gearsD:
      # print("A:", a, "B:", b, "D:", d)
      ratio = d / a
      combinations[ratio].add(("s", a, b, d))
      for n in screwGears:
        TPIcombinations[ratio * n].add(("s", a, b, d, n))
      counter += 1

# compound gear train
gearsA = list(changeGears)
for a in gearsA:
  if a < 30 or a > 81: continue  # as per manual
  gearsB = list(gearsA)
  gearsB.remove(a)
  for b in gearsB:
    if a + b < 105: continue  # as per manual (modified)
    gearsC = list(gearsB)
    gearsC.remove(b)
    for c in gearsC:
      gearsD = list(gearsC)
      gearsD.remove(c)
      for d in gearsD:
        bShaftDistance = (b + 2) / diametralPitch + outputShaftRadius
        cdDistance = ((c + 2) / diametralPitch) + ((d + 2) / diametralPitch)
        if bShaftDistance > cdDistance: continue  # gear b will crash into output shaft
        # print("A:", a, "B:", b, "C:", c, "D:", d)
        ratio = (d * b) / (a * c)
        combinations[ratio].add(("c", a, b, c, d))
        for n in screwGears:
          TPIcombinations[ratio * n].add(("c", a, b, c, d, n))
        counter += 1

print("gear combinations checked:", counter)
print("unique gear combinations:", len(combinations))
print("unique pitches:", len(TPIcombinations))
# print(sorted([k for k,v in combinations.items()]))
l = sorted([(k, v) for k, v in TPIcombinations.items()])


# print([len(v) for k,v in l])
# print(l[0][1])
def findTPI(tpi):
  for i in range(len(l)):
    if l[i][0] > tpi:
      if i > 0:
        return l[i - 1], l[i]
      else:
        return None, l[i]
  return l[len(l) - 1], None




def printOption(option):
  if option[0] == "s":
    return "A:{} B:{} D:{} N:{}".format(option[1], option[2], option[3], option[4])
  elif option[0] == "c":
    return "A:{} B:{} C:{}, D:{} N:{}".format(option[1], option[2], option[3], option[4], option[5])
  else:
    return "Unknown Option:{}".format(option)

def id(x): return x
def fromTPI(tpi, converstionFunc=id, unit="tpi"):
    if len(TPIcombinations[tpi]) > 0:
        for option in TPIcombinations[tpi]:
            print("\t", printOption(option))
    else:
        lower, upper = findTPI(tpi)
        if lower is not None:
            print("closet Lower : {}{} \t error: {}%".format(converstionFunc(lower[0]), unit, 100 * abs(converstionFunc(tpi) - converstionFunc(lower[0])) / converstionFunc(tpi)))
            for option in lower[1]:
                print("\t", printOption(option))
        if upper is not None:
            print("closet Higher: {}{} \t error: {}%".format(converstionFunc(upper[0]), unit, 100 * abs(converstionFunc(tpi) - converstionFunc(upper[0])) / converstionFunc(tpi)))
            for option in upper[1]:
                print("\t", printOption(option))

def search():
    lookupType = str(input("tpi(1), pitch(2), mm-pitch(3), diametral pitches(4), metric module(5)"))

    if lookupType == "1" or lookupType == "2":
        tpi = 0
        if lookupType == "1":
            tpi = float(input("tpi?"))
        else:
            pitch = float(input("pitch?"))
            tpi = 1/pitch
        print("Finding {} tpi".format(tpi))
        fromTPI(tpi)

    elif lookupType == "3":
        pitch = float(input("mm-pitch?"))
        tpi = 25.4 / pitch
        print("Finding {}mm pitch".format(pitch))
        print("Finding {} tpi".format(tpi))
        fromTPI(tpi, converstionFunc=lambda tpi: 25.4/tpi, unit="mm")

    elif lookupType == "4":
        pitch = float(input("dimetral-pitch?"))
        tpi = pitch/math.pi
        print("Finding {}dimetral pitch".format(pitch))
        print("Finding {} tpi".format(tpi))
        fromTPI(tpi, converstionFunc=lambda tpi: tpi*math.pi, unit="dp")

    elif lookupType == "5":
        mod = float(input("metric module?"))
        tpi = (25.4/mod)/math.pi
        print("Finding {}metric module".format(mod))
        print("Finding {} tpi".format(tpi))
        fromTPI(tpi, converstionFunc=lambda tpi: 25.4/(tpi*math.pi), unit="dp")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        search()

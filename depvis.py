#!/usr/bin/python3

import sys
from collections import OrderedDict


IMPLEMENTS = 1
DEPENDS_ON = 2


def padLine(line, cursor):
  padding = line["x"] - cursor
  print("─" * padding, end="")
  return padding


def printGraph(depMatrix, lines, width):
  maxLabelLen = 0
  for name, item in depMatrix.items():
    l = len(name + " " + item["version"])
    if l > maxLabelLen:
      maxLabelLen = l

  for row, (name, item) in enumerate(depMatrix.items()):
    label = name + " " + item["version"]
    paddedLabel = label + " " * (maxLabelLen - len(label) + 1)

    print(paddedLabel, end="")

    cursor = 0
    for col in range(len(lines)):
      print("─", end="")
      cursor += 1

      if lines[col]["end"] == row:
        versionLabel = lines[col]["version"]

        cursor += padLine(lines[col], cursor)
        print("▴" + versionLabel, end="")

        cursor += len("▴" + versionLabel)
      elif lines[col]["start"] == row:
        cursor += padLine(lines[col], cursor)
        print("┴" if lines[col]["type"] == IMPLEMENTS else "╨", end="")

        cursor += 1
      elif lines[col]["start"] > row and lines[col]["end"] < row:
        cursor += padLine(lines[col], cursor)
        print("│" if lines[col]["type"] == IMPLEMENTS else "║", end="")

        cursor += 1
      else:
        print("─", end="")
        cursor += 1

    print("─" * (width - cursor))


def parseDescription(description):
  descs = description.split("/")
  depMatrix = OrderedDict()

  for desc in descs:
    nameString, implsString, depsString = [s.strip() for s in desc.split(";")]
    name, version = nameString.partition("=")[::2]

    item = ({"version": version, "implements": [], "dependsOn": []})

    for implPair in implsString.split(","):
      impl, version = implPair.partition("=")[::2]
      if impl:
        item["implements"] += [(list(depMatrix).index(impl), version)]

    for depPair in depsString.split(","):
      dep, version = depPair.partition("=")[::2]
      if dep:
        item["dependsOn"] += [(list(depMatrix).index(dep), version)]

    depMatrix[name] = item

  return depMatrix


def computeLines(depMatrix):
  lines = ()

  for idx, item in enumerate(depMatrix.values()):
    for impl in item["implements"]:
      lines += tuple([{
        "start": idx,
        "end": impl[0],
        "version": impl[1],
        "type": IMPLEMENTS
      }])

    for dep in item["dependsOn"]:
      lines += tuple([{
        "start": idx,
        "end": dep[0],
        "version": dep[1],
        "type": DEPENDS_ON
      }])

  return lines


def positionLines(lines):
  prev = None
  x = 1
  for line in lines:
    if prev:
      if prev["end"] >= line["end"]:
        x += len(prev["version"]) + 2
      else:
        x += 2

    line["x"] = x
    prev = line

  return x + len(lines[-1]["version"]) + 2


if __name__ == "__main__":
  depMatrix = parseDescription(sys.argv[1])
  lines = computeLines(depMatrix)
  width = positionLines(lines)

  printGraph(depMatrix, lines, width)


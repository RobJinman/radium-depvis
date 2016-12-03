import sys;


IMPLEMENTS = 1
DEPENDS_ON = 2


def printGrid(grid, names):
  maxLen = 0
  for name in names:
    if len(name) > maxLen:
      maxLen = len(name)

  for r, row in enumerate(grid):
    name = names[r]
    paddedName = name + " " * (maxLen - len(name))

    print(paddedName + " ─", end="")

    for cell in row:
      print("─" + cell, end="")

    print("──")


def parseDescription(desc):
  descs = desc.split("/")
  depMatrix = [[0] * len(descs) for d in descs]
  names = ()

  for idx, depString in enumerate(descs):
    name, impls, deps = depString.split(";")
    names = names + (name,)

    for i in impls.split(","):
      if i != '':
        depMatrix[idx][names.index(i)] = IMPLEMENTS

    for d in deps.split(","):
      if d != '':
        depMatrix[idx][names.index(d)] = DEPENDS_ON

  return names, depMatrix


def populateGrid(names, depMatrix):
  totalDeps = 0
  for row in depMatrix:
    for cell in row:
      if cell == IMPLEMENTS or cell == DEPENDS_ON:
        totalDeps = totalDeps + 1

  grid = [["─"] * totalDeps for i in names]

  cursor = 0
  for lhs, row in enumerate(depMatrix):
    for rhs, cell in enumerate(row):
      if depMatrix[lhs][rhs] == IMPLEMENTS:
        grid[lhs][cursor] = "┴"

        for r in range(1, lhs - rhs):
          grid[rhs + r][cursor] = "│"

        grid[rhs][cursor] = "▴"
        cursor = cursor + 1

      elif depMatrix[lhs][rhs] == DEPENDS_ON:
        grid[lhs][cursor] = "┴"

        for r in range(1, lhs - rhs):
          grid[rhs + r][cursor] = "╎"

        grid[rhs][cursor] = "▴"
        cursor = cursor + 1

  return grid


if __name__ == "__main__":
  names, depMatrix = parseDescription(sys.argv[1])
  grid = populateGrid(names, depMatrix)

  printGrid(grid, names)


class unionfind:
	def __init__(self, n):
		self.parent = list(range(n))
	def find(self, i):
		if self.parent[i] != i: self.parent[i] = self.find(self.parent[i])
		return self.parent[i]
	def unite(self, i, j):
		i = self.find(i)
		j = self.find(j)
		if i != j: self.parent[i] = j
	def issame(self, i, j):
		return self.find(i) == self.find(j)
	def groups(self):
		r = range(len(self.parent))
		return [[j for j in r if self.issame(j, i)] for i in r if i == self.parent[i]]
	def sizes(self):
		# Find all roots, and update all non-roots
		roots = []
		for i, p in enumerate(self.parent):
			if (p == i):
				roots.append(i)
			else:
				self.find(i)
		# Make a dictionary of all groups' sizes
		sizes = { r: 0 for r in roots }
		# Count members of each group
		for p in self.parent:
			sizes[p] += 1
		# Return result
		return sizes
	@staticmethod
	def isconnected(l, u = None):
		nw, nh = len(l), len(l[0])
		rw, rh = range(nw), range(nh)
		if not u: u = unionfind(nw * nh)
		f = -1
		for i in rw:
			for j in rh:
				if not l[i][j]: continue
				if f < 0: f = i + j * nw
				if j > 0 and l[i][j] == l[i][j - 1]: u.unite(i + j * nw, i + j * nw - nw)
				if i > 0 and l[i][j] == l[i - 1][j]: u.unite(i + j * nw, i + j * nw - 1)
		return f >= 0 and all([u.issame(f, i + j * nw) for i in rw for j in rh if l[i][j]])
	@staticmethod
	def isconnectedlist(nw, nh, lst):
		l = [[False] * nw for j in range(nh)]
		for i, j in lst: l[i][j] = True
		return unionfind.isconnected(l)

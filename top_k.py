MAX_INPUTS = 10000
# Limit max size of the dict
# TODO: make configurable

class Frequency(object):
    def __init__(self, it):
        self._it = it; self._count = 1

    def bump_frequency(self):
        self._count += 1

    def __eq__(self, other):
        return self._it == other._it and self._count == other._count

    def __lt__(self, other):
        return self._count < other._count


class TopK(object):
    def __init__(self, k):
        self._counts = {}
        self._k = k

    def count_obj(self, obj):
        if obj not in self._counts:
            self._counts[obj] = Frequency(obj)
        self._counts[obj].bump_frequency()

        # truncate when the dict is getting too large
        if len(self._counts) > min(self._k * 2, MAX_INPUTS): self._truncate()

    def get_top_k(self):
        out = []
        values = list(sorted(self._counts.items(), key = lambda item: item[1], reverse=True))
        while True:
            item = values.pop()
            out.append((item[0], item[1]._count))
            if len(out) == self._k:
                break
        return out

    def _truncate(self):
        items = 0
        new_counts = {}
        for x in sorted(self._counts.items(), key=lambda item: item[1]._count):
            new_counts[x[0]] = x[1]
            items += 1
            if self._k * 2 <= items:
                break


if __name__ == "__main__":
    top_k = TopK(10)
    for i in range(1000):
        import random, string, pprint
        top_k.count_obj(random.choice(string.ascii_letters))
    pprint.pprint(top_k.get_top_k())

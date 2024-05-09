import hashlib as _hl


def path(p):
  h = _hl.sha3_384()
  with open(p, "rb") as f:
    for i in f:
      h.update(i)
  return h.hexdigest()


def file(f):
  h = _hl.sha3_384()
  for i in f:
    h.update(i)
  return h.hexdigest()


def text(t, encoding="utf-8"):
  return _hl.sha3_384(str(t).encode(encoding)).hexdigest()


def bytes(b):
  return _hl.sha3_384(b).hexdigest()

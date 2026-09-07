# -*- coding: utf-8 -*-
"""Μελικίδης — «Ολοκληρωμένες λύσεις για κάθε ανάγκη»: the before/after photos whole, not cropped."""
import io

p = 'index.html'
s = io.open(p, encoding='utf-8').read()
start = len(s)


def rep(a, b, label=''):
    global s
    if s.count(a) != 1:
        raise SystemExit('COUNT %d [%s]: %r' % (s.count(a), label, a[:110]))
    s = s.replace(a, b)


# Each of the five service photos is 400x600 — an upright pair, the "before" above the
# "after". A 230px-tall landscape window was showing only a slice through the middle, so
# the whole point of the picture was being cut away.
rep(""".svc-img{height:230px;overflow:hidden;position:relative;cursor:pointer}
.svc-img img{width:100%;height:100%;object-fit:cover;transition:transform .8s cubic-bezier(.2,.8,.2,1)}""",
    """/* the photo keeps its own 2:3 shape — nothing is cut off — and sits on a soft plate,
   the same size in every card so the row stays even whatever the card width */
.svc-img{
  position:relative;cursor:pointer;padding:22px 22px 4px;
  background:linear-gradient(180deg,#f4f8f8,#eef4f4);
}
.svc-img .svc-shot{
  width:100%;max-width:300px;margin:0 auto;aspect-ratio:2/3;overflow:hidden;
  border-radius:14px;box-shadow:0 10px 30px -14px rgba(14,27,36,.35);background:#fff;
}
.svc-img img{width:100%;height:100%;object-fit:cover;display:block;transition:transform .8s cubic-bezier(.2,.8,.2,1)}""",
    'svc-img')

# the zoom badge belongs to the plate, so keep it clear of the photo's rounded corner
rep(""".svc-img::after{content:"⤢";position:absolute;top:14px;right:14px;""",
    """.svc-img::after{content:"⤢";position:absolute;top:32px;right:32px;z-index:2;""", 'zoom-badge')

# the sixth card has no photograph, only an icon — give it the same plate so the
# two rows of three stay exactly level
rep("""        <div class="svc-img" style="background:linear-gradient(135deg,var(--teal),var(--teal-bright));display:flex;align-items:center;justify-content:center;cursor:default">
          <svg""",
    """        <div class="svc-img" style="cursor:default">
          <div class="svc-shot svc-shot-icon">
          <svg""", 'icon-card-open')
rep("""c-1 1.5-2.5 3-5 3z"/></svg>
        </div>""",
    """c-1 1.5-2.5 3-5 3z"/></svg>
          </div>
        </div>""", 'icon-card-close')
rep(""".svc-img:hover::after{opacity:1}""",
    """.svc-img:hover::after{opacity:1}
.svc-img[style*="default"]::after{display:none}
.svc-shot-icon{
  display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,var(--teal),var(--teal-bright));
}
.svc-shot-icon svg{width:88px;height:88px}""", 'icon-card-css')

# wrap each photo in its plate
n = 0
out = []
i = 0
while True:
    j = s.find('<div class="svc-img" onclick=', i)
    if j < 0:
        out.append(s[i:])
        break
    k = s.index('</div>', s.index('<img ', j))
    block = s[j:k]
    img_at = block.index('<img ')
    head, img = block[:img_at], block[img_at:]
    out.append(s[i:j])
    out.append(head.rstrip() + '\n          <div class="svc-shot">' + img.strip() + '</div>\n        ')
    i = k
    n += 1
s = ''.join(out)
assert n == 5, n
print('wrapped %d service photos' % n)

io.open(p, 'w', encoding='utf-8').write(s)
print('melikidis ok, %d -> %d bytes' % (start, len(s)))

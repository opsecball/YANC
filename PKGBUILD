pkgname=yanc
pkgver=1.0.0
pkgrel=1
pkgdesc="Yet another neofetch clone"
arch=('any')
url="local"
license=('GPL v3')
depends=('python')
options=(!strip)

prepare() {
  cp -f "$startdir/yanc.py" "$srcdir/yanc.py"
}

package() {
  install -Dm755 "$srcdir/yanc.py" "$pkgdir/usr/bin/yanc"
}

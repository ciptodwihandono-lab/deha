# Peta Survei (pindah)

Peta Survei kini berdiri sendiri di repo
[ciptodwihandono-lab/Peta-survey](https://github.com/ciptodwihandono-lab/Peta-survey),
alamat https://ciptodwihandono-lab.github.io/Peta-survey/.

Folder ini hanya berisi pengalih untuk alamat lama `/deha/peta/`:
`index.html` mengalihkan ke alamat baru, dan `sw.js` melepas service worker lama
tanpa menghapus data (localStorage/IndexedDB satu domain, jadi data tetap terbaca
di alamat baru).

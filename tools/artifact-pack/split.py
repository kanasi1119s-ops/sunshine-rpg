# 1ファイルのHTMLを Artifact に載る形に分ける（composer/split.py と同じやり方。音源は sf/NNN.wasm、JS は sf/NNN.js、14MB をこえるものは .pK.wasm に分割）
import re, base64, os, sys
inp, outdir = sys.argv[1], sys.argv[2]
src = open(inp, encoding="utf-8").read()
os.makedirs(outdir + "/sf", exist_ok=True)
pat = re.compile(r'data:[a-zA-Z0-9.+/-]*;base64,([A-Za-z0-9+/=]{270000,})')
CH = 14 * 1024 * 1024
out = []; last = 0; n = 0
for m in pat.finditer(src):
    raw = base64.b64decode(m.group(1))
    js = raw[:200].lstrip().startswith((b"var ", b"//", b"(function", b"\"use strict", b"class ", b"const ", b"let ", b"import", b"export"))
    if js: name = f"sf/{n:03d}.js"; open(f"{outdir}/{name}", "wb").write(raw); ref = name
    elif len(raw) <= CH: name = f"sf/{n:03d}.wasm"; open(f"{outdir}/{name}", "wb").write(raw); ref = name
    else:
        k = (len(raw) + CH - 1) // CH
        for i in range(k): open(f"{outdir}/sf/{n:03d}.p{i}.wasm", "wb").write(raw[i * CH:(i + 1) * CH])
        ref = f"sf/{n:03d}.wasm#parts={k}"
    out.append(src[last:m.start()]); out.append(ref); last = m.end(); n += 1
out.append(src[last:])
html = "".join(out)
shim = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "shim.html"), encoding="utf-8").read()
i = html.find("<script")
html = html[:i] + shim + html[i:]
open(outdir + "/index.html", "w", encoding="utf-8").write(html)
print(n, "files; page", round(len(html.encode()) / 1e6, 2), "MB")

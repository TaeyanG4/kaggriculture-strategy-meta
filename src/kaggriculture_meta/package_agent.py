"""Build an immutable single-file Kaggle artifact and deterministic tar.gz."""
import argparse
import ast
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile


def source_audit(source):
    trees = [ast.parse(source)]
    imports = set()
    dynamic_exec = 0
    for tree in trees:
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split('.')[0])
            elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ('open', 'eval', '__import__'):
                    raise ValueError(f'Unreviewed runtime capability: {node.func.id}')
                if node.func.id == 'exec':
                    if not node.args or not isinstance(node.args[0], ast.Constant) or not isinstance(node.args[0].value, str):
                        raise ValueError('Nonliteral exec requires separate review')
                    trees.append(ast.parse(node.args[0].value))
                    dynamic_exec += 1
    unexpected = imports - sys.stdlib_module_names
    blocked = imports & {'socket', 'urllib', 'http', 'subprocess', 'os', 'pathlib'}
    if unexpected or blocked:
        raise ValueError(f'Unreviewed dependencies/capabilities: {unexpected | blocked}')
    return {'standard_library_imports': sorted(imports), 'inspected_literal_exec_bodies': dynamic_exec,
            'note': 'Static capability screen, not a security proof; official-loader matches are a separate gate'}


def package(source_path, out):
    content = Path(source_path).read_bytes()
    compile(content, 'main.py', 'exec')
    audit = source_audit(content.decode('utf-8'))
    archive = io.BytesIO()
    with gzip.GzipFile(filename='', fileobj=archive, mode='wb', mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode='w', format=tarfile.USTAR_FORMAT) as tar:
            member = tarfile.TarInfo('main.py')
            member.size = len(content)
            member.mode = 0o644
            member.mtime = 0
            tar.addfile(member, io.BytesIO(content))
    payload = archive.getvalue()
    with tarfile.open(fileobj=io.BytesIO(payload), mode='r:gz') as tar:
        if tar.getnames() != ['main.py'] or tar.extractfile('main.py').read() != content:
            raise ValueError('Package readback mismatch')
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    for name, data in [('main.py', content), ('submission.tar.gz', payload)]:
        path = out / name
        if path.exists() and path.read_bytes() != data:
            raise ValueError('Refusing to overwrite a different artifact; use a new output directory')
        path.write_bytes(data)
    manifest = {'source_sha256': hashlib.sha256(content).hexdigest(), 'source_bytes': len(content),
                'archive_sha256': hashlib.sha256(payload).hexdigest(), 'archive_bytes': len(payload),
                'archive_members': ['main.py'], 'static_audit': audit}
    (out / 'manifest.json').write_text(json.dumps(manifest, indent=2)+'\n', encoding='utf-8')
    return manifest


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    print(json.dumps(package(args.source, args.out), indent=2))


if __name__ == '__main__':
    main()

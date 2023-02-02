import sys

print("Abrindo o releaser...")

if len(sys.argv) == 1:
    from . import build_from_sources
    build_from_sources.build_from_current_path()


elif len(sys.argv) == 2:
    from . import build_from_sources
    build_from_sources.build_from_json_file(sys.argv[1])


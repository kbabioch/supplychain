from supplychain.rpmspec import Editor

r = Editor('tests/specfiles/llvm.spec')
s = r.get_last_source_line()
print(s)
r.add_source('## TEST ##')


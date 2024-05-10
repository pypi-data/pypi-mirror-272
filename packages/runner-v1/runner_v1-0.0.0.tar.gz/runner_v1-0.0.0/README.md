# runner

## usage

required
profile.name, profile.run, from_ext.ext, from_ext.profile

optional
profile.pre_run, profile.post_run

```toml
[[profile]]
name = 'c++'
pre_run = 'g++ -O2 <file>'
run = './a.out'
post_run = 'rm a.out'


[[from_ext]]
ext = 'cpp'
profile = 'c++'

```

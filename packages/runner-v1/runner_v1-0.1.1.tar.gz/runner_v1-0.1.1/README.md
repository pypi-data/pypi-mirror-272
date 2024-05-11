# runner

## usage

### configuratioins

```sh
pip install runner-v1
```

make `runner.toml` in your project directory.

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

[[profile]]
name = 'python'
run = 'python <file>'

[[from_ext]]
ext = 'cpp'
profile = 'c++'

[[from_ext]]
ext = 'py'
profile = 'python'

```

```sh
run main.cpp
```

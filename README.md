# do-script

## install
- step 1: install python
- step 2: use make for os
#### unix
```
make install-unix
```
#### linux
```
make install-linux
```
#### windows
if you want full installation then you need to run script 
```
pip install pyinstaller
make build-exe
set path=%path%;DIR/dist
```
if you just want to install original or debug then you need to choose 1 of 2

##### 1: original
```
pip install pyinstaller
pyinstaller src/doS.py --onefile -w
set path=%path%;DIR/dist
```

##### 1: debug
```
pip install pyinstaller
pyinstaller src/debug.do.py --onefile -w
set path=%path%;DIR/dist
```

## example
#### output
```
out "hello"
```
#### variable
```
$name = "quangladn"
out $name
```
#### input
```
input "report error: " $error
out "reported"
out $error
```
#### if
```
input "enter a num: " $x
if $x == 1: 1
  out "lmmao"
else: 2
  out 123
  out "$x not equals 1"
```
### token
#### output
```
> ['out','"hello"']
```
#### variable
```
> [ '$name','equals','"quangladn"','out','$name' ]
> { '$name':'"quangladn"' }
```
#### input
```
> [ 'input','"report error"','$error','out','"reported"','out','$error' ]
> { '$error':input }
```
#### if
```
> [ 'input','"enter a num: "','$x','if','$x','eqeq','1','then','1','out','"lmmao"',
  'else','then','2','out','123','out':'"$x not equals"' ]
> { '$x':input }
```

## tutorial syntax
#### output
```
out <content>
```
#### variable
```
$<varName> = <value>
```
#### input
```
input "<question>" $<varName>
```
#### if 
```
if <value-1> <operator> <value-2>: <total line in if>
<code>
else: <total line in else>
<code>
```

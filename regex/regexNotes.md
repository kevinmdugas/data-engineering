# Regular Expressions

- [RegEx cheatsheet](https://regexlearn.com/cheatsheet)
- [RegEx checker](https://regex101.com/)
- [RegEx interpreter](https://regexr.com/)

## Syntax

- `\d` - match any digit
- `.` - wildcard
- `[abc]` - match a single character in the group (`a, b, or c`) and nothing else
- `[^abc]` - match a single character except for the characters in the group
- `[^n-p]` - match a single character except for the letters from `n to p`
- `\w` - match a single alphanumeric character (equivalent to `[A-Za-z0-9_]`)
- `\W` - match a non-alphanumeric character
- `a{3}` - match three `a` characters in a row
- `a{1,3}` - match at least one but no more than 3 `a` chars
- `\d*` - any number of digits, including zero
- `\d+` - at least one digit
- `ab?c` - `b` is optional so match either `abc` or `ac`
- `\s` - match a whitespace character (space, tab, newline, carriage return)
- `^success$` - match a line that starts (denoted by `^`) and ends (denoted by `$`)
  with `success`
- `^(IMG\d+)\.png$` - captured groups: capture only an image filename begining with
  `IMG` and some number of digits. Do not save the extension `.png`
- `^(IMG(\d+))\.png$` - nested groups: capture both the image file name and the
  sequence of digits in that filename and store it in two separate groups
- `([cb]ats*|[dh]ogs?)` - match either cats or bats, or, dogs or hogs

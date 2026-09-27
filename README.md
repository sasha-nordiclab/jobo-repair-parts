# Jobo Knob

Ручка Ø33 × 16 мм, FreeCAD 1.1. Модификаторы `Modifier 1` / `Modifier 2` —
тела для печати метки другим цветом.

## Diff для .FCStd

`.FCStd` — zip-архив, поэтому `git diff` идёт через `tools/fcstd-textconv.py`:
он показывает имена, параметры фич и размеры в эскизах. После клонирования
включить один раз:

    git config diff.fcstd.textconv "python3 tools/fcstd-textconv.py"
    git config diff.fcstd.cachetextconv true

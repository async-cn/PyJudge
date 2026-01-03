# G 魔法石铭文

牧羊人确认 Maaike 是真正的勇者之后，将魔法石给予了 Maaike。

牧羊人告诉 Maaike，这块魔法石的使用方式较为特别：每次使用时，魔法石会显示一个字母 $char$ 和一行诗句 $s$，只有正确地说出诗句 $s$ 中字母 $char$ 出现的次数才能释放魔法石的能量。

这是块魔法石是崭新的。为了将其激活，Maaike 需要按上述方法使用一次魔法石。

请你根据魔法石显示的字母 $char$ 和诗句 $s$ 统计 $s$ 中字母 $char$ 出现的次数，帮助 Maaike 激活魔法石。

## 输入格式

一行，一个字符 $char$

一行，一个字符串，代表诗句 $s$

## 输出格式

一行，一个整数，代表 $s$ 中字符 $char$ 出现的次数

## 输入输出样例

### 样例输入 #1

```text
e
Hope is the thing with feathers.
```

### 样例输出 #1

```text
4
```

### 样例解释

字符串 `Hope is the thing with feathers.` 中，字符 `e` 共出现了 $4$ 次。

## 数据范围

对于所有测试数据，$\mathrm{len}(char)=1,1\le \mathrm{len}(s)\le {10}^5$
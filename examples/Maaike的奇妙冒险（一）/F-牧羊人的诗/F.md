# F 牧羊人的诗

将紫水晶换成硬币后，Maaike 在山坡上遇见一个牧羊人。他的嘴里念着一首诗，听起来很有美感。

牧羊人注意到了 Maaike 的靠近。他转过身来，面带和蔼的微笑说到：“你就是去拯救猫咪们的勇士吧？”

“当然。” Maaike 回答。

牧羊人从口袋里掏出一个魔法石，说道：“勇敢的勇士 Maaike，这是我想送给你用来打败魔王的法宝。然而，在此之前，我需要确认你是否是真正的勇士，真正的勇士是充满智慧的。”

牧羊人随即念出了一句诗 $s_0$。接下来，牧羊人念出了 $n$ 句诗，分别是 $s_1,s_2,\cdots,s_n$。牧羊人让 Maaike 答出后来念出的 $n$ 句诗中与 $s_0$ 相同的诗句数量。如果回答正确，牧羊人才能确认 Maaike 是真正的勇士。

请你帮助 Maaike 判断 $s_1,s_2,\cdots,s_n$ 中与 $s_0$ 相同的诗句数量。

## 输入格式

一行，一个字符串，代表诗句 $s_0$

一行，一个正整数，代表牧羊人接下来即将念出的诗句数量 $n$

$n$ 行，每行一个字符串，代表牧羊人念出的诗句 $s_1,s_2,\cdots,s_n$

## 输出格式

一行，一个整数，代表 $s_1,s_2,\cdots,s_n$ 中与 $s_0$ 相同的诗句数量。

## 输入输出样例

### 样例输入 #1

```text
The hero is coming.
8
The hero is coming.
Sheep are staring at him.
The hero is coming.
Cats are waiting for rescue.
The hero is coming.
Devil is still unaware of it.
Where is the hero?
He is right in front of me!
```

### 样例输出 #1

```text
3
```

### 样例解释 #1

$s_1\sim s_8$ 中，共有 $s_1,s_3,s_5$ 与 $s_0$ 相同，故与 $s_0$ 相同的诗句数量为 $3$。

## 数据范围

对于所有测试数据，$1\le n\le {10}^4,1\le \mathrm{len}(s_i)\le 100$
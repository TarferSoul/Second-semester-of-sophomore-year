# Course_Project_1B

专业班级：**提高2201班**

姓名：        **王翎羽**

学号：        **U202213806**

## 实验环境

**编程语言**:  ***Python***

**实验工具**:  ***PyCharm 2023.1.3***、***Jupyter Notebook***

## 实验任务

- *Read Steve Jobs’ 2005 Stanford Commencement Address “You’ve got to find what you love”as in the file ”Steve Jobs Speech.txt”.*

- *Collect the statistics of the letters, punctuation, space in “Steve Jobs Speech.doc”.*

- *Compute the entropy of “Steve Jobs Speech.doc”.*

- *Apply the Huffman coding method and Shannon coding method for “Steve Jobs Speech.doc”.Output the letters/punctuation/space and their Huffman codewords and Shannon codes,respectively.*

- *Compute the average code length of “Steve Jobs Speech.doc” using your Huffman codes andShannon codes, respectively.*

Note: For the Huffman code, please develop your code to generate a Q-ary Huffman code,where Q is an input variable which can be random chosen.

## 实验结果

### 熵的计算

这个任务与之前的任务相同，所以直接Copy过来。得到结果如图所示。

<img src="E:\备份\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\基础信息论\作业\Course_Project_2\1.png" style="zoom:150%;" />

### Shannon 编码

![](E:\备份\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\基础信息论\作业\Course_Project_2\2.png)

### Huffman 编码

![](E:\备份\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\基础信息论\作业\Course_Project_2\3.png)

### 平均码长

![](E:\备份\OneDrive - hust.edu.cn\电子课本课件及资料\大二下\基础信息论\作业\Course_Project_2\4.png)

### 结果分析

程序完成了任务要求，可以读取文本后为其生成Q-Huffman编码和Shannon编码。

## 附：实验源码

```python
import math
from collections import Counter, defaultdict
import string
import heapq


# 统计字母、标点符号和空格的频率
def collect_statistics(text):
    letters_and_punctuation = string.ascii_letters + string.punctuation + ' '
    filtered_text = [char for char in text if char in letters_and_punctuation]
    char_count = Counter(filtered_text)
    total_chars = sum(char_count.values())
    return char_count, total_chars

file_path = 'Steve_Jobs_Speech.txt'
with open(file_path, 'r', encoding='utf-8') as f:
    speech_text = f.read()
Text_stats, total = collect_statistics(speech_text)
print(Text_stats)


def calculate_entropy(filtered_text, order=0):

    if order == 0:
        # 0阶马尔可夫模型：每个字符独立选择
        char_count = Counter(filtered_text)
        total_chars = sum(char_count.values())
        entropy = 0
        for count in char_count.values():
            probability = count / total_chars
            entropy -= probability * math.log2(probability)
        return entropy
    else:
        # 高阶马尔可夫模型
        storage = defaultdict(Counter)
        total_ngrams = 0

        for i in range(len(filtered_text) - order):
            prefix = filtered_text[i:i + order]
            next_char = filtered_text[i + order]
            storage[prefix][next_char] += 1
            total_ngrams += 1

        entropy = 0
        for prefix, suffix_counts in storage.items():
            prefix_total = sum(suffix_counts.values())
            for count in suffix_counts.values():
                probability = count / prefix_total
                entropy -= (prefix_total / total_ngrams) * probability * math.log2(probability)

        return entropy

    
Text_entropy_0 = calculate_entropy(speech_text, 0)
Text_entropy_3 = calculate_entropy(speech_text, 3)
Text_entropy_5 = calculate_entropy(speech_text, 5)

print(f"Text Entropy (0th order): {Text_entropy_0}")
print(f"Text Entropy (3rd order): {Text_entropy_3}")
print(f"Text Entropy (5th order): {Text_entropy_5}")


# Shannon编码
def calculate_shannon_codes(frequencies, total_chars):
    codes = {}
    probabilities = {char: freq / total_chars for char, freq in frequencies.items()}
    sorted_chars = sorted(probabilities.items(), key=lambda item: item[1], reverse=True)
    cumulative_prob = 0.0
    for char, prob in sorted_chars:
        code_length = math.ceil(-math.log2(prob))
        cumulative_prob_bin = bin(int(cumulative_prob * (1 << code_length)))[2:].zfill(code_length)
        codes[char] = cumulative_prob_bin[:code_length]
        cumulative_prob += prob
    return codes


# Huffman编码
class QaryHuffmanNode:
    # 定义节点
    def __init__(self, symbol=None, frequency=0):
        self.symbol = symbol
        self.frequency = frequency
        self.children = []

    def __lt__(self, other):
        return self.frequency < other.frequency

def qary_huffman_code(symbols, frequencies, Q):
    # 将所有节点压入堆中
    heap = [QaryHuffmanNode(symbol=symbol, frequency=freq) for symbol, freq in zip(symbols, frequencies)]
    heapq.heapify(heap)

    # 转换最小堆
    while len(heap) > 1:
        children = [heapq.heappop(heap) for _ in range(min(Q, len(heap)))]
        parent_frequency = sum(child.frequency for child in children)
        parent_node = QaryHuffmanNode(frequency=parent_frequency)
        parent_node.children.extend(children)
        heapq.heappush(heap, parent_node)

    # 递归编码
    def build_code(node, prefix, code):
        if node.symbol is not None:
            code[node.symbol] = prefix
        else:
            for i, child in enumerate(node.children):
                build_code(child, prefix + str(i), code)

    root = heap[0]
    code = {}
    build_code(root, "", code)
    return code

def generate_qary_huffman_code(counter, Q):
    symbols = list(counter.keys())
    frequencies = list(counter.values())
    return qary_huffman_code(symbols, frequencies, Q)

Q = 3
huffman_codes = generate_qary_huffman_code(Text_stats, Q)
shannon_codes = calculate_shannon_codes(Text_stats, total)

print(huffman_codes)


# 计算平均码长
def calculate_average_code_length(codes, frequencies):
    total_length = sum(len(code) * freq for char, code in codes.items() for freq in [frequencies[char]])
    total_symbols = sum(frequencies.values())
    average_length = total_length / total_symbols
    return average_length

average_length_shannon = calculate_average_code_length(shannon_codes, Text_stats)
average_length_huffman = calculate_average_code_length(huffman_codes, Text_stats)

print(f"Shannon Code Average Length: {average_length_shannon}")
print(f"{Q}-array Huffman Code Average Length: {average_length_huffman}")


# 保存
def save_codes_to_file(filename, codes):
    with open(filename, 'w', encoding='utf-8') as f:
        for char, code in codes.items():
            f.write(f"{char}: {code}\n")

save_codes_to_file('shannon_codes.txt', shannon_codes)
save_codes_to_file('huffman_codes.txt', huffman_codes)
```


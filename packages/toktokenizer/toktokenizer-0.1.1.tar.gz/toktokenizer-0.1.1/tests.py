import toktokenizer
import time
import sys
import copy
from transformers import AutoTokenizer
import tiktoken
from tqdm import tqdm

with open("../wikidump_test.txt", "r") as f:
    data = f.read()

bpe = toktokenizer.BPETokenizer.from_pretrained("wikibpe50k.json")
tokenizer = AutoTokenizer.from_pretrained("openai-community/gpt2")
enc = tiktoken.get_encoding("gpt2")


def foo(nbytes=1e6):
    size = sys.getsizeof(data)
    print(f"file size: {size/1e6}MB")

    test_data = copy.copy(data)[: int(len(data) * min(1.0, (nbytes / size)))]

    now = time.time()
    test_data = bpe.preprocess(test_data)
    ids = bpe.encode(test_data)
    elapsed = time.time() - now

    t1 = sys.getsizeof(test_data) / (elapsed * 1e06)
    print(f"throughput tok: {t1:.2f}MB/s")

    decoded = bpe.decode(ids)
    assert decoded == test_data

    # gpt2 speed
    now = time.time()
    _ = tokenizer.encode(test_data)
    elapsed = time.time() - now

    t2 = sys.getsizeof(test_data) / (elapsed * 1e06)
    print(f"throughput HF: {t2:.2f}MB/s")

    # tiktoken
    now = time.time()
    _ = enc.encode(test_data)
    elapsed = time.time() - now

    t3 = sys.getsizeof(test_data) / (elapsed * 1e06)
    print(f"throughput tiktoken: {t3:.2f}MB/s")

    return (t1, t2, t3)


if __name__ == "__main__":
    niters = 50

    times = []
    for _ in tqdm(range(niters)):
        times.append(foo(nbytes=1e6))

    print(f"tok: {sum([t[0] for t in times])/niters:.2f}MB/s")
    print(f"tokenizers: {sum([t[1] for t in times])/niters:.2f}MB/s")
    print(f"tiktoken: {sum([t[2] for t in times])/niters:.2f}MB/s")

    # another example
    print(
        bpe.decode(
            bpe.encode("i'm SkEpTIcaL of the performance for this tokenizer 🤖🦀")
        )
    )

# 使用步骤
## 下载模型
从HuggingFace下载模型mistralai/Mistral-7B-v0.1，并且做量化处理（Quantize）来加速处理过程
```console
# 目录：/lora
python convert.py --hf-path mistralai/Mistral-7B-v0.1 -q
```

## 使用对话数据（已经完成）
从[self-llm](https://github.com/datawhalechina/self-llm/blob/master/dataset/huanhuan.json)下载甄嬛对话文件
目标目录：data_甄嬛
在目标目录运行以下程序来拆分训练数据，同时转换格式：
```console
# 目录：/lora/data_甄嬛
python split.py
```

## 运行Lora微调
生成目标文件“adapters_甄嬛.npz”
```console
# 目录：/lora
python lora.py --model mlx_model \
               --train \
               --data data_甄嬛/ \
               --adapter-file adapters_甄嬛.npz \
               --iters 600
```

## 使用微调模型
```console
# 目录：/lora
python lora.py --model mlx_model \
               --adapter-file adapters_甄嬛.npz \
               --max-tokens 100 \
               --prompt "假设你是皇帝身边的女人——甄嬛。
Q: 甄嬛你怎么了，朕替你打抱不平！
A: "
```
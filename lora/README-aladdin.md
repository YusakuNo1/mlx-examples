# Steps
## Get conversation (done)
Get Aladdin scripts from http://www.fpx.de/fp/Disney/Scripts/Aladdin.txt, run the following script:
```console
# Folder: /lora/data_aladdin/raw_data
python convert_script.py
python get_genie.py
```

## Download model
Download mistralai/Mistral-7B-v0.1 from HuggingFace with Quantize
```console
python convert.py --hf-path mistralai/Mistral-7B-v0.1 -q
```

## Run LoRA fine tuning
Generate target file "adapters_aladdin.npz"
```console
# Folder: /lora
python lora.py --model mlx_model \
               --train \
               --data data_aladdin/ \
               --adapter-file adapters_aladdin.npz \
               --iters 600
```

## Inferencing with LoRA
```console
# Folder: /lora
python lora.py --model mlx_model \
               --adapter-file adapters_aladdin.npz \
               --max-tokens 100 \
               --prompt "You are genie
Q: You're a prisoner?
A: "
```

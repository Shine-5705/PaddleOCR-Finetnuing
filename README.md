
<h1>PaddleOCR Finetuning Project</h1>

<h2>Introduction</h2>

<p>Welcome! If you're here, you might be struggling with PaddleOCR finetuning, just like I was. This guide will walk you through the process step-by-step, helping you avoid the pitfalls I encountered. Whether you’re completely new or have been battling with the documentation for hours, this guide is for you.</p>

<h2>Steps to Finetune PaddleOCR</h2>

<h3>1. Create Conda Environments</h3>

<p>Create two conda environments with Python 3.8: one for training and one for inference.</p>
<pre><code>conda create --name paddleocr_train python=3.8
conda create --name paddleocr_infer python=3.8
</code></pre>

<h3>2. Download PaddlePaddle</h3>

<p>Install PaddlePaddle in your training environment based on your GPU setup.</p>
<pre><code>conda activate paddleocr_train
python -m pip install paddlepaddle==2.6.0 -i https://mirror.baidu.com/pypi/simple
</code></pre>

<h3>3. Install PaddleOCR</h3>

<p>Clone PaddleOCR repository and install dependencies.</p>
<pre><code>git clone https://github.com/PaddlePaddle/PaddleOCR
cd PaddleOCR
pip install -r requirements.txt
</code></pre>

<h3>4. Prepare Dataset and Annotations</h3>

<p>Organize your dataset into <code>Train_img</code> and <code>Val_img</code> directories.</p>
<p>Place your annotation files in <code>Train_ann.json</code> and <code>Val_ann.json</code>.</p>

<h3>5. Combine JSON Files into JSONL</h3>

<p>Combine and validate JSON files using a script to create <code>combined_train.jsonl</code> and <code>combined_val.jsonl</code>.</p>

<h3>6. Download Pre-trained Weights</h3>

<p>Download the pre-trained model weights from <a href="https://paddleocr.bj.bcebos.com/ppstructure/models/tablemaster/table_structure_tablemaster_infer.tar">PaddleOCR GitHub</a>.</p>
<p>Extract the model into a <code>pretrained_model</code> directory.</p>

<h3>7. Configure YAML File</h3>

<p>Edit the YAML configuration file with your training parameters and dataset paths.</p>
<pre><code>save_model_dir: "path/to/save/checkpoints"
epoch_num: 100
eval_batch_step: [0, 1000]
character_dict_path: "path/to/dictionary"
save_res_path: "path/to/save/results"
train:
  data_dir: "path/to/train/data"
  label_file_list: ["path/to/combined_train.jsonl"]
eval:
  data_dir: "path/to/eval/data"
  label_file_list: ["path/to/combined_val.jsonl"]
</code></pre>

<h3>8. Run the Training Command</h3>

<p>Execute the training command with the specified configuration and pre-trained model.</p>
<pre><code>python tools/train.py -c config.yml -o Global.pretrained_model="path/to/pretrained_model/best_accuracy"
</code></pre>

<h3>9. Handle Common Errors</h3>

<p>If you encounter <code>RecursionError: maximum recursion depth exceeded</code>, ensure your JSON files are correctly formatted and paths are properly escaped.</p>

<h3>10. Export to Inference Model</h3>

<p>Export the fine-tuned model for inference.</p>
<pre><code>python tools/export_model.py -c config.yml -o Global.pretrained_model=path/to/checkpoints Global.save_inference_dir=path/to/inference_model
</code></pre>

<h3>11. Create Second Conda Environment for Inference</h3>

<p>Install PaddleOCR in the inference environment.</p>
<pre><code>conda activate paddleocr_infer
python -m pip install paddlepaddle==2.6.0 -i https://mirror.baidu.com/pypi/simple
pip install paddleocr
</code></pre>

<h3>12. Write and Run Inference Script</h3>

<p>Test your fine-tuned model with an inference script.</p>
<pre><code>from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

ocr = PaddleOCR(rec_model_dir="path/to/inference_model", use_angle_cls=True, lang='en')
img_path = 'path/to/test/image.png'
result = ocr.ocr(img_path, cls=True)
for line in result:
    print(line)
</code></pre>

<h2>Common Errors and Solutions</h2>

<h3>Error: <code>RecursionError: maximum recursion depth exceeded</code></h3>

<p>This error often occurs due to improper JSON formatting. Ensure that all file paths are correctly escaped.</p>

<h3>Error: <code>Invalid \escape: line 1 column 17</code></h3>

<p>Check that your JSON lines are correctly formatted, especially file paths containing backslashes.</p>

<h2>References</h2>

<ul>
    <li><a href="https://github.com/PaddlePaddle/PaddleOCR">PaddleOCR GitHub Repository</a></li>
    <li><a href="https://github.com/PaddlePaddle/PaddleOCR/blob/main/doc/doc_en/algorithm_table_master_en.md">PaddleOCR TableMaster Documentation</a></li>
</ul>

<p>With this guide, you should be able to finetune PaddleOCR with ease. If you run into issues, review each step and ensure all paths and formats are correct. Happy finetuning!</p>

</body>
</html>

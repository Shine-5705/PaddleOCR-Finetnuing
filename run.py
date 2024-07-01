import subprocess
import os

def activate_virtualenv_and_run():
    # Paths
    project_dir = r"C:\Users\BQ Team 4\Desktop\OCR Finetuning"
    venv_activate = os.path.join(project_dir, r".venv\Scripts\activate.bat")
    paddle_ocr_dir = os.path.join(project_dir, r".venv\Lib\PaddleOCR")
    config_file = os.path.join(paddle_ocr_dir, "table_master.yml")
    pretrained_model_path = os.path.join(paddle_ocr_dir, r"pre_trained_my_model\table_structure_tablemaster_train\best_accuracy")

    # Command to activate virtual environment and run the training script
    command = f'cmd /c ""{venv_activate}" && cd "{paddle_ocr_dir}" && python tools/train.py -c "{config_file}" -o Global.pretrained_model="{pretrained_model_path}""'

    # Run the command
    subprocess.run(command, shell=True, check=True)

if __name__ == '__main__':
    activate_virtualenv_and_run()

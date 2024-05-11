# 德姆斯AI驱动的工业设备故障诊断服务
仓库简介：

本仓库是德姆斯AI驱动的工业设备故障诊断服务的代码仓库

包含了工业设备故障诊断服务的mvp版本实现的源代码。

版本：诊断中心mvp版本1.0

日期：2024年4月23日

---
## mvp版本推理依赖库

4090服务器 cuda版本：12.2 / cudnn版本：8.9.5

本地电脑 cuda版本：11.8 / cudnn版本：8.7.0

pytorch环境

conda install pytorch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 pytorch-cuda=11.8 -c pytorch -c nvidia
```angular2html
# 其它环境
pandas==2.1.1
numpy==1.26.0
tensorflow==2.14.0
zipp==3.17.0
h5py==3.9.0
scipy==1.11.4
matplotlib==3.8.0
tqdm==4.65.0
openpyxl==3.1.2
scikit-learn==1.3.0
seaborn==0.13.2
wget==3.2
loguru==0.7.2
pydantic==2.7.0
torchsummary==1.5.1
```

---

## <font color="#00FFFF">项目结构</font>

- <font color="#00FFFF">Configuration_Files</font>

  - <font color="#00FFFF">inference_configuration</font>
   
      存放 推理 时需要使用的配置文件
  
  - <font color="#00FFFF">train_configuration</font>
   
      存放 训练 时需要使用的配置文件

- <font color="#00FFFF">train

    - results</font>
   
      存放训练结果(包含混淆矩阵、权重文件、标准化器)
    - <font color="#00FFFF">running_record</font>
  
      存放训练日志(tensorboard打开)

- <font color="#00FFFF">necessary_files</font>

    - <font color="#00FFFF">rolling_bearing</font>
  
      滚动轴承故障诊断推理前 必须具备的文件，包括 权重文件、标准化器

    - <font color="#00FFFF">gear</font>

      齿轮故障诊断推理前 必须具备的文件，包括 权重文件、标准化器

- <font color="#00FFFF">datasets</font>
    
  数据集

---

## <font color="#FFA500">故障诊断测试用例的 使用方法 及 输入、输出 说明：</font>

- <font color="#FFA500">使用方法：</font>

  python model_inference.py

  根据实际情况选择下面中的一种：

  ```angular2html
  一、基于 src数据 进行诊断  
  # 以本地数据举例(线上调用应该传入config_info、rpm给instantiate_model初始化模型,传入src给
  # src_inference用于诊断)
    config_path = "E:\\Python_files\\dhms_projects\\improved_wdcnn\\Configuration_Files\\" \
                  "inference_configuration\\inference_config.JSON"
    file_path = "E:\\Python_files\\dhms_projects\\improved_wdcnn\\example_data\\2-x.257-2023-08-23T21-15-01.aiff"

    rpm = 1480  # 线上应传入
    src = read_local_file(file_path)  # 线上应传入
    with open(config_path, "r") as file:  # 线上应传入
        config_info = json.load(file)

    # 实例化模型
    net, device = instantiate_model(config_info['pth_path'], rpm=rpm,
                                    activation_function=config_info['activation_function'])
    
    # 基于src数据诊断
    result_json = src_inference(
        src, net, device, config_info['pkl_path'],
        probability_output=config_info['probability_output'],
        confidence=config_info['confidence'],
        length=config_info['model_processing_signal_length']
    )
  
  
  二、基于 原始振动文件夹 的诊断
  # 本地数据举例(线上调用应该传入config_info、file_path、rpm)
  config_path = "E:\\Python_files\\dhms_projects\\improved_wdcnn\\Configuration_Files\\" \
                  "inference_configuration\\inference_config.JSON"
  file_path = "E:\\Python_files\\dhms_projects\\improved_wdcnn\\example_data"  # 线上应传入

  rpm = 1480  # 线上应传入
  with open(config_path, "r") as file:  # 线上应传入
      config_info = json.load(file)

  # 实例化模型
  net, device = instantiate_model(config_info['pth_path'], rpm=rpm,
                                    activation_function=config_info['activation_function'])

  # 基于原始振动文件夹的诊断
  result_json = inference(
        file_path, net, device, config_info['pkl_path'],
        probability_output=config_info['probability_output'],
        confidence=config_info['confidence'],
        length=config_info['model_processing_signal_length']
  )

  ```
      
  默认输入数据需满足采样点数为8192长度，否则测试无效且报错


- <font color="#FFA500">输入说明：</font>

  确保 inference_config.JSON 中的路径存在且正确，须符合python os库的格式
 
  1. "pkl_path": "inference/necessary_input/rolling_bearing/8192_resample_WDCNN.pkl"
    
     用于推理的标准器文件的路径，由训练得到。默认已配置
  2. "pth_path": "inference/necessary_input/rolling_bearing/best_weight.pth"
      
     用于推理的权重文件的路径，由训练得到。默认已配置
  3. "activation_function": "ReLU"
      
     激活函数，应与 train_config.JSON 文件中的 "activation_function": "ReLU" 一致。默认已配置
  4. "probability_output": false
      
     是否以概率形式输出。 false则直接输出类别
  5. "confidence": 0.5
      
     置信度。推理时，只有概率值 >=0.5 时，才认为分类正确，否则分到相反的类别
  6. "model_processing_signal_length": 8192
      
     当前推理模型适用的 信号输入长度。过长会被截断

- <font color="#FFA500">输出说明：</font>
  
  运行成功结果：
```angular2html
结果一:
只输出预测的类别

{
    "status": "fault"
}


结果二:
输出预测的类别及对应的概率

{
    "status": "fault",
    "probability": "0.9995"
}
```


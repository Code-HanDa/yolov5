### 预训练模型
| 模型                                                                                             | 尺寸<br><sup>（像素） | mAP<sup>val<br>50-95 | mAP<sup>val<br>50 | 推理速度<br><sup>CPU b1<br>（ms） | 推理速度<br><sup>V100 b1<br>（ms） | 速度<br><sup>V100 b32<br>（ms） | 参数量<br><sup>(M) | FLOPs<br><sup>@640 (B) |
| ---------------------------------------------------------------------------------------------- | --------------- | -------------------- | ----------------- | --------------------------- | ---------------------------- | --------------------------- | --------------- | ---------------------- |
| [YOLOv5n](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n.pt)             | 640             | 28.0                 | 45.7              | **45**                      | **6.3**                      | **0.6**                     | **1.9**         | **4.5**                |
| [YOLOv5s](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s.pt)             | 640             | 37.4                 | 56.8              | 98                          | 6.4                          | 0.9                         | 7.2             | 16.5                   |
| [YOLOv5m](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5m.pt)             | 640             | 45.4                 | 64.1              | 224                         | 8.2                          | 1.7                         | 21.2            | 49.0                   |
| [YOLOv5l](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5l.pt)             | 640             | 49.0                 | 67.3              | 430                         | 10.1                         | 2.7                         | 46.5            | 109.1                  |
| [YOLOv5x](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5x.pt)             | 640             | 50.7                 | 68.9              | 766                         | 12.1                         | 4.8                         | 86.7            | 205.7                  |
|                                                                                                |                 |                      |                   |                             |                              |                             |                 |                        |
| [YOLOv5n6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5n6.pt)           | 1280            | 36.0                 | 54.4              | 153                         | 8.1                          | 2.1                         | 3.2             | 4.6                    |
| [YOLOv5s6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5s6.pt)           | 1280            | 44.8                 | 63.7              | 385                         | 8.2                          | 3.6                         | 12.6            | 16.8                   |
| [YOLOv5m6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5m6.pt)           | 1280            | 51.3                 | 69.3              | 887                         | 11.1                         | 6.8                         | 35.7            | 50.0                   |
| [YOLOv5l6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5l6.pt)           | 1280            | 53.7                 | 71.3              | 1784                        | 15.8                         | 10.5                        | 76.8            | 111.4                  |
| [YOLOv5x6](https://github.com/ultralytics/yolov5/releases/download/v7.0/yolov5x6.pt)<br>+[TTA] | 1280<br>1536    | 55.0<br>**55.8**     | 72.7<br>**72.7**  | 3136<br>-                   | 26.2<br>-                    | 19.4<br>-                   | 140.7<br>-      | 209.8<br>-             |

使用go视频服务源:

```angular2html
教程地址: https://blog.csdn.net/qq_33398946/article/details/118404857
git地址： https://github.com/gwuhaolin/livego.git
livego使用步骤：
    1、转到 livego 目录并执行go build或make build
    2、make run运行livego   
    3、获取串流密钥 http://localhost:8090/control/get?room=movie
    4、推流地址 rtmp://localhost:1935/live
    5、拉取播放地址 rtmp://localhost:1935/live/movie

    验证一下是否获取到窗口rtmp视频流，
    OBS自定义推流到livego的推流地址rtmp://localhost:1935/live，
    随便用个播放器找到网络播放输入livego的播放地址
    rtmp://localhost:1935/live/movie，
    就能看到你的窗口rtmp视频流了。
    
    yolov5推理指令–source后
    输入livego的播放地址rtmp://localhost:1935/live/movie，
    后面在跟一个–view-img，就能实时推理某一特定窗口了。
```


### 第一步
使用
```bash 
pip install -r requirements.txt
```
即可安装requirement.txt（见上）中所需要的依赖项
### 第二步
测试是否可以使用
```bash 
执行 detect.py 内的  main函数
```
### 第三步
下载素材标注工具
```bash 
pip install labelimg
```
或者直接找git上有官网 window包，可以直接下载安装
w 标记。  ctrl + j 编辑标记
### 第四步
创建ymal配置文件到 lableimg 文件夹下
```bash 
pip install labelimg
```
或者直接找git上有官网 window包，可以直接下载安装
w 标记。  ctrl + j 编辑标记

### 第五步
训练自己的模型
https://colab.research.google.com/drive/13lfzLFw8DHVOV_d6GbLIhVSOrZ#scrollTo=i8R
```bash 
先修改
文件|修改|视图|插入。。。 点击修改
笔记本设置---硬件加速---选择GPU

第一步挂载磁盘
import os
from google.colab import drive
drive.mount('/content/drive')

第二步进入yolo目录
cd drive/MyDrive/colab/yolov5

第三安装yolo依赖包
pip install -r requirements.txt

第四步训练模型
!python train.py --img 640 --batch 50 --epochs 100 --data ./mymodle/Aerbien_caiji.yaml --weights yolov5s.pt --nosave --cache

```

### 第六步把训练好的模型下载下来放到yolo5根目录下
```bash 
修改best.pt 名字为 myaerbien.pt
```
### 第七步测试使用训练模型
```bash 
修改best.pt 名字为 myaerbien.pt
```
修改使用的自己模型yaml配置写法
```angular2html
# train and val data as 1) directory: path/images/, 2) file: path/images.txt, or 3) list: [path1/images/, path2/images/]
train: ../mydata/images/
val: ../mydata/images/
# number of classes
nc: 1

# class names
names: [sijima]
```
修改 detect run()函数调用文件  注意这里的权重文件仍然使用的是 yolov5s的
```angular2html
@smart_inference_mode()
def run(
        weights=ROOT / 'yolov5s.pt',  # model path or triton URL
        source=ROOT / 'data/images',  # file/dir/URL/glob/screen/0(webcam)
        data=ROOT / 'mydata/aerbien.yaml',  # dataset.yaml path
。。。。
```
修改 detect parse_opt()函数调用文件
```angular2html
def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'myaerbien.pt', help='model path or triton URL')
    parser.add_argument('--source', type=str, default=ROOT / 'mydata/images', help='file/dir/URL/glob/screen/0(webcam)')
    parser.add_argument('--data', type=str, default=ROOT / 'mydata/aerbien.yaml', help='(optional) dataset.yaml path')
。。。。
```
最后调用myaerbiendetect.py 里的 main方法 （先将之前截图的图片放到你模型的那个选择的图片路径）进行测试，输出结果在 runs 目录下。能看到已经框定出来了
```angular2html
if __name__ == '__main__':
    opt = parse_opt()
    main(opt)
```
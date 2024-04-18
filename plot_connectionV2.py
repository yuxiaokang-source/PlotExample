########## 导入库 ################
from math import cos, sin, atan
import matplotlib.pyplot as plt
from itertools import product
########## mac显示中文############
plt.rcParams['font.sans-serif']=['Songti SC'] 

# 单个神经元类Neuron
class Neuron():

    # 初始化函数
    def __init__(self, x, y,radius,name=None):
        # x：横轴坐标
        # y: 纵轴坐标
        # radius: 神经元对应的圆的半径
        # name: 神经元对应的ID(可以不用，用于调试)
        self.x = x
        self.y = y
        self.radius = radius
        self.name = name

    # 画图函数
    def draw(self):
        circle = plt.Circle((self.x, self.y), radius=self.radius, fill=False,linewidth=0.3) # 画圆
        plt.gca().add_patch(circle) # 加入到matplotlib中的patch中
        ################################## 仅调试 ################
        if(self.name is not None):
            plt.text(self.x,self.y,self.name)
        #########################################################

# 沿水平方向改造对应的神经元类NeuronLayer(即构造垂直方向均匀分布的多个Neuron)
class NeuronLayer():

    # 初始化函数
    def __init__(self,positionX,numNeurons,numNeuronsWidestLayer):
    # positionX: 该层对应的水平位置
    # numNeurons:该层对应的神经元个数
    # numNeuronsWidestLayer: 最宽层对应的神经元个数(为了达到居中的效果)
        self.positionX = positionX 
        self.numNeurons = numNeurons
        self.numNeuronsWidestLayer = numNeuronsWidestLayer
        self.NeuronList=[] # 存储各个神经元的列表
    
    # 画图函数
    def draw(self,vertical_distance_between_neurons,radius):
    # radius: 每个神经元的半径
    # vertical_distance_between_neurons: 相邻神经元的间隔
        self.vertical_distance_between_neurons = vertical_distance_between_neurons
        self.radius = radius
        self.initY =  vertical_distance_between_neurons * (self.numNeuronsWidestLayer - self.numNeurons) / 2 #从下往上，第一个神经元对应圆心的纵轴坐标
        positionY = self.initY
        for i in range(self.numNeurons):
            neu = Neuron(self.positionX,positionY,radius)
            neu.draw()
            self.NeuronList.append(neu)
            positionY = positionY + vertical_distance_between_neurons

## 通过已知的一层网络构造出另一个镜像对称的神经网络(应该写成继承关系，不过我也不用管这个了，太麻烦了)
class MirrorNeuronLayer():
    # 初始化函数
    def __init__(self, neuronlayer, middle_pos):
        self.baselayer = neuronlayer
        self.positionX = neuronlayer.positionX
        self.numNeurons =neuronlayer.numNeurons
        self.NeuronList=[]
        self.middle_pos = middle_pos

    # 画图函数
    def draw(self):
        for i in range(self.numNeurons):
            neu_posY = self.baselayer.NeuronList[i].y
            mirror_neu = Neuron(self.positionX, 2*self.middle_pos - neu_posY, self.baselayer.NeuronList[i].radius)
            mirror_neu.draw()
            self.NeuronList.append(mirror_neu)
    

# 画图连接两个给定的神经元
def TwoNeuronsConnection(neuron1,neuron2):
    neuron_radius= neuron1.radius
    angle = atan((neuron2.y - neuron1.y)/float(neuron2.x - neuron1.x))
    x_adjustment = neuron_radius * cos(angle)
    y_adjustment = neuron_radius * sin(angle)
    ##################### 添加直线 ###########################
    line = plt.Line2D((neuron1.x + x_adjustment, neuron2.x - x_adjustment), (neuron1.y + y_adjustment, neuron2.y - y_adjustment),color="#4d4d4d",linewidth=0.2)
    plt.gca().add_line(line)
    #########################################################
    ##################### 添加箭头(不好看) ###########################
    # startX,startY = neuron1.x + x_adjustment,neuron1.y + y_adjustment
    # deltaX,deltaY = neuron2.x - x_adjustment - startX ,neuron2.y - y_adjustment - startY 
    # plt.gca().arrow(startX,startY,deltaX,deltaY, width=0.001, color="#4d4d4d", 
    #      head_width=0.03, head_length=0.03, overhang=1.0,length_includes_head=True,linewidth=0.2)

    #########################################################

# 画图连接相邻两层神经元
def TwoLayersConnection(NeuronLayer1,NeuronLayer2):
    Layer1 = NeuronLayer1.NeuronList
    Layer2 = NeuronLayer2.NeuronList
    for neuron1,neuron2 in product(Layer1,Layer2):
        TwoNeuronsConnection(neuron1,neuron2)

##############################################
fig = plt.figure()


## 输入层是均匀分布的

## 这个对称轴的选择是多少是有讲究的，得让输入层看起来是均匀的，
#mid_pos = vertical_distance_between_neurons*(numNeuronsWidestLayer-numNeurons)/2 + numNeuronsWidestLayer*(numNeurons-0.5) 
mid_pos = 1.625
initX =1
deltaX = 1
radius =0.075
margin = 2 * radius

#################### 第一层##############################
#构造下半部分4个神经元对应的神经网络层
Layer11 = NeuronLayer(positionX=initX,numNeurons=4,numNeuronsWidestLayer=10) 
#画下半部分的神经元
Layer11.draw(vertical_distance_between_neurons=0.25,radius=radius)
#构造上半部分4个神经元对应的神经网络层
Layer12 = MirrorNeuronLayer(Layer11,middle_pos=mid_pos)
#画上半部分的神经元
Layer12.draw()

#################### 第二层##############################
#网络1
Layer21 = NeuronLayer(positionX=initX + deltaX,numNeurons=10,numNeuronsWidestLayer=10)
Layer21.draw(vertical_distance_between_neurons=margin,radius=radius)
#网络2
Layer22 = MirrorNeuronLayer(Layer21,middle_pos=mid_pos)
Layer22.draw()

#################### 第三层##############################
#网络1
Layer31 = NeuronLayer(positionX=initX + 2*deltaX,numNeurons=8,numNeuronsWidestLayer=10)
Layer31.draw(vertical_distance_between_neurons=margin,radius=radius)
#网络2
Layer32 = MirrorNeuronLayer(Layer31,middle_pos=mid_pos)
Layer32.draw()

#################### 第四层##############################
#网络1
Layer41 = NeuronLayer(positionX=initX + 3*deltaX,numNeurons=5,numNeuronsWidestLayer=10)
Layer41.draw(vertical_distance_between_neurons=margin,radius=radius)
#网络2
Layer42 = MirrorNeuronLayer(Layer41,middle_pos=mid_pos)
Layer42.draw()

#################### 第五层##############################
#网络1
Layer51 = NeuronLayer(positionX=initX + 4*deltaX,numNeurons=1,numNeuronsWidestLayer=10)
Layer51.draw(vertical_distance_between_neurons=margin,radius=radius)
#网络2
Layer52 = MirrorNeuronLayer(Layer51,middle_pos=mid_pos)
Layer52.draw()

#################### 第六层##############################
#网络1
Layer61 = NeuronLayer(positionX=initX + 5*deltaX,numNeurons=1,numNeuronsWidestLayer=10)
Layer61.draw(vertical_distance_between_neurons=margin,radius=radius)
#网络2
Layer62 = MirrorNeuronLayer(Layer61,middle_pos=mid_pos)
Layer62.draw()

#################### 画网络层之间的连接###################
TwoLayersConnection(Layer11,Layer21)
TwoLayersConnection(Layer11,Layer22)
TwoLayersConnection(Layer12,Layer21)
TwoLayersConnection(Layer12,Layer22)
TwoLayersConnection(Layer21,Layer31)
TwoLayersConnection(Layer22,Layer32)
TwoLayersConnection(Layer31,Layer41)
TwoLayersConnection(Layer32,Layer42)
TwoLayersConnection(Layer41,Layer51)
TwoLayersConnection(Layer42,Layer52)
TwoLayersConnection(Layer51,Layer61)
TwoLayersConnection(Layer52,Layer62)
############################################################################################

############# 添加末尾神经元 #################################################################
posX1,posY1 = Layer52.NeuronList[0].x, Layer52.NeuronList[0].y 
neu1 = Neuron(posX1,posY1 +0.2, radius=radius)
neu1.draw()
TwoNeuronsConnection(neu1,Layer62.NeuronList[0])

posX2,posY2= Layer51.NeuronList[0].x, Layer51.NeuronList[0].y 
neu2 = Neuron(posX2,posY2 + 0.2, radius=radius)
neu2.draw()
TwoNeuronsConnection(neu2,Layer61.NeuronList[0])

neu3 = Neuron(posX2,posY2 - 0.2, radius=radius)
neu3.draw()
TwoNeuronsConnection(neu3,Layer61.NeuronList[0])
#############################################################################################

############ 添加神经元标识##########################################################
plt.text(Layer62.NeuronList[0].x+0.2,Layer62.NeuronList[0].y-0.05,"输出$\hat{\mu}$")
plt.text(Layer61.NeuronList[0].x+0.2,Layer61.NeuronList[0].y-0.05,"输出$\hat{\phi}/{\omega}$")
plt.text(neu2.x-0.2,neu2.y+0.15,"$log(1/{\omega})$")

############################## 添加变量名 ###########################
cnt = 1
for neu in Layer11.NeuronList:
    plt.text(neu.x -0.5,neu.y-0.04,"变量{}".format(9-cnt))
    cnt=cnt+1
cnt = 1
for neu in Layer12.NeuronList:
    plt.text(neu.x -0.5,neu.y-0.04,"变量{}".format(cnt))
    cnt=cnt+1
###################################################################

############################## 添加上箭头 ###########################
line1 = plt.Line2D((1, 1), (2.8,3.5),color="#4d4d4d",linewidth=0.2)
plt.gca().add_line(line1)

line2 = plt.Line2D((1, 5), (3.5,3.5),color="#4d4d4d",linewidth=0.2)
plt.gca().add_line(line2)
plt.text(2.5,3.6,"$\mu$参数通过GLM连接")

plt.gca().arrow(5,3.5, 0, -0.6, width=0.001, color="#4d4d4d", 
    head_width=0.05, head_length=0.05, overhang=1.0,length_includes_head=True,linewidth=0.2)
###################################################################

############################## 添加下箭头 ###########################
line1 = plt.Line2D((1, 1), (0.4,-0.3),color="#4d4d4d",linewidth=0.2)
plt.gca().add_line(line1)

line2 = plt.Line2D((1, 5), (-0.3,-0.3),color="#4d4d4d",linewidth=0.2)
plt.gca().add_line(line2)
plt.text(2.5,-0.5,"$\phi$参数通过GLM连接")

plt.gca().arrow(5,-0.3, 0, 0.6, color="#4d4d4d", 
    head_width=0.05, head_length=0.05, overhang=1.0,length_includes_head=True,linewidth=0.2)
###################################################################

######################### 去除画图边框并保存文件 ##############################
plt.axis("scaled")
plt.axis('off')
plt.savefig("./network.pdf")
plt.show()
####################################################################





 


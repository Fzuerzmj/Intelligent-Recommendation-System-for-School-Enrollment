
from Get_Tip import Get_Tip
from Get_Mes import Spider

spider = Spider()
tip = Get_Tip()
spider.Update_Spider()   #更新原网页新添加的信息
print("开始分类贴标签。。。")
tip.Tip()                #分类贴标签

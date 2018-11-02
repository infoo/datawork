import re
import jieba
html = '<pre> class="line mt-10 q-content" accuse="qContent">\
目的是通过第一次soup.find按class粗略筛选并通过soup.find_all \n筛选出列表中的a标签并读入href和title属性<br><br>\
但是由于目标链接可能有图片链接,而这是我不想要的.请问如何去除?<br></pre>\
    </pre> test test   ccc<pre>lllll</pre>'

regs = jieba.cut_for_search(html)
for seg in regs:
    print(seg)

print("===")
print(html)
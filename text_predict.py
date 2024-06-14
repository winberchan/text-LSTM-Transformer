import jieba
jieba.load_userdict('user_dict.txt')
from tensorflow.keras import models
import re
model = models.load_model('text_model')
model.summary()

# transfer chinise text to token style string
def text_preprocess(line):
    line = line.strip("\n")
    word_list = jieba.lcut(line)
    word_list = list(filter(lambda x : re.findall('[\u4e00-\u9fa5]', x),word_list))
    return " ".join(word_list)
text_total = []
text_results = 'text_res.txt'
outopen = open(text_results,'w',encoding='utf-8')
with open('Shoted_urls.txt','r',encoding='utf-8') as file:
    i = 0
    print_link = False
    for line in file:
        if not line.startswith('https'):
            text = line[20:]
            # text = line
            token_seq = text_preprocess(text)
            print(text[:-1]+" -----> "+token_seq)
            text_total.append(token_seq)
            predictions = model.predict([token_seq])
            print("预测结果：",predictions[0])
            if predictions[0]>0.5:
                print_link = True
                outopen.write(text)
        else:
            if print_link:
                outopen.write(str(predictions[0])+" "+line)
                print_link = False
            continue
outopen.close()
print('done')
# predictions = model.predict(np.array(text_total))
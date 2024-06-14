import jieba
jieba.load_userdict('user_dict.txt')
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import re
import random

BUFFER_SIZE = 8000
BATCH_SIZE = 64
VOCAB_SIZE = 5000
SEQ_LENGTH = 20

text_total_T = []
text_total_F = []
TEXT2TOKENSEQ_DICT = {}
# transfer chinise text to token style string
def text_preprocess(line):
    line = line.strip("\n")
    word_list = jieba.lcut(line)
    word_list = list(filter(lambda x : len(x)>1 and re.findall('[\u4e00-\u9fa5]', x),word_list))
    return " ".join(word_list)

with open('y1.txt','r',encoding='utf-8') as file:
    for line in file:
        token_seq = text_preprocess(line)
        TEXT2TOKENSEQ_DICT[line]=token_seq
        text_total_T.append(token_seq)
#正样本较少，采用过采样
text_total_T = text_total_T*2
labels_T = np.ones(len(text_total_T))
random.shuffle(text_total_T)
dataset_T = tf.data.Dataset.from_tensor_slices((np.array(text_total_T),labels_T))
print(dataset_T.take(1))
with open('f5.txt','r',encoding='utf-8') as file:
    for line in file:
        token_seq = text_preprocess(line)
        TEXT2TOKENSEQ_DICT[line]=token_seq
        text_total_F.append(token_seq)
# print(TEXT2TOKENSEQ_DICT)
labels_F = np.zeros(len(text_total_F))
random.shuffle(text_total_F)
dataset_F = tf.data.Dataset.from_tensor_slices((np.array(text_total_F),labels_F))
dataset = dataset_T.concatenate(dataset_F)
dataset = dataset.shuffle(BUFFER_SIZE).shuffle(BUFFER_SIZE//10).shuffle(BUFFER_SIZE//100)
train_dataset = dataset.take(4000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
validate_dataset = dataset.skip(4000).take(1000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
test_dataset = dataset.skip(5000).batch(BATCH_SIZE).prefetch(tf.data.AUTOTUNE)

encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(max_tokens = VOCAB_SIZE,output_mode = 'int',output_sequence_length=SEQ_LENGTH)
encoder.adapt(train_dataset.map(lambda text,_ : text))
vocab = np.array(encoder.get_vocabulary())

print(vocab[:50])
print("--------------------------------------------------------------------")
print(vocab[-20:])
print('vocab size:'+str(len(vocab)))
for example, label in test_dataset.take(10):
    print(example[:2])
    print(encoder(example)[:2].numpy())
    print(label[:2])

model = tf.keras.Sequential([
    encoder,
    tf.keras.layers.Embedding(
        input_dim = len(encoder.get_vocabulary()),
        output_dim = 64,
        mask_zero = True),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64,return_sequences=True)),
    tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1,activation='sigmoid')
])

model.compile(loss=tf.keras.losses.BinaryCrossentropy(from_logits=False),
              optimizer=tf.keras.optimizers.Adam(1e-4),metrics=['accuracy'])
sample_text = ('外资 全走了 工厂 倒闭 没人 可以 上班 大家 在家 喝 西北风')
predictions = model.predict(np.array([sample_text]))
print('训练前模型预测样例得到归一化后的logits：',predictions[0])
history = model.fit(train_dataset,epochs=25,validation_data=validate_dataset)
model.summary()
test_loss, test_acc = model.evaluate(test_dataset)
print("Test Loss:", test_loss)
print('Test Accuracy', test_acc)

def plot_graphs(history, metric):
    plt.plot(history.history[metric])
    plt.plot(history.history['val_'+metric],'')
    plt.xlabel("Epochs")
    plt.ylabel("metric")
    plt.legend([metric,'val_'+metric])
    plt.pause(2)
plt.figure(figsize=(16,6))
plt.subplot(1,2,1)
plot_graphs(history,'accuracy')
plt.ylim(None,1)
plt.subplot(1,2,2)
plot_graphs(history,'loss')
plt.ylim(0, None)
sample_text = ('共产党 真 伟大 我们 过上 小康 生活 我们 要 歌颂 祖国')
sample_text1 = ('外资 全走了 工厂 倒闭 没人 可以 上班 大家 在家 喝 西北风')
sample_text2 = ('惠州 三星 工厂 大裁员 操他妈了 没人 在 出租屋 整理 行李 滚回家 未来 没有 希望')
predictions = model.predict(np.array([sample_text,sample_text1,sample_text2]))
print("训练后模型预测结果",predictions)
model.save('text_model')

# def custom_standardize(input_data):
#     print(input_data)
#     return tf.strings.regex_replace(input_data, '\n', '')

# def custom_split(input_data):
#     # print(len(input_data.numpy()))
#     word_list = []
#     for text in input_data:
#         # print(text)
#         word_list += jieba.lcut(text)
#     word_list = list(filter(lambda x : re.findall('[\u4e00-\u9fa5]', x),word_list))
#     return word_list

# encoder = tf.keras.layers.experimental.preprocessing.TextVectorization(standardize = custom_standardize,
#                                                                      split = custom_split,
#                                                                      max_tokens = VOCAB_SIZE,
#                                                                      output_mode = 'int',
#                                                                      output_sequence_length=SEQ_LENGTH)

# jieba分词器测试
# token_list = []
# with open('f5.txt','r',encoding='utf-8') as file:
#     for line in file:
#         line = line.strip("\n")
#         # print(line)
#         word_list = jieba.lcut(line)
#         print(word_list)
# print("done")
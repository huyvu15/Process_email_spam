import pandas as pd
import re 


sms_spam = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])

# Randomize the dataset
data_randomized = sms_spam.sample(frac=1, random_state=1)
# Calculate index for split
training_test_index = round(len(data_randomized) * 0.8)
# Split into training and test sets
training_set = data_randomized[:training_test_index].reset_index(drop=True)
test_set = data_randomized[training_test_index:].reset_index(drop=True)


training_set['SMS'] = training_set['SMS'].str.replace('\W', ' ')
training_set['SMS'] = training_set['SMS'].str.lower()

training_set['SMS'] = training_set['SMS'].str.split()
vocabulary = []
for sms in training_set['SMS']:
    for word in sms:
        vocabulary.append(word)
        vocabulary = list(set(vocabulary))
        
        
word_counts_per_sms = {'secret': [2,1,1], 'prize': [2,0,1], 'claim': [1,0,1], 'now': [1,0,1], 'coming': [0,1,0], 'to': [0,1,0], 'my': [0,1,0], 'party': [0,1,0], 'winner': [0,0,1] }
word_counts = pd.DataFrame(word_counts_per_sms)


word_counts_per_sms = {unique_word: [0] * len(training_set['SMS']) for unique_word in vocabulary}
for index, sms in enumerate(training_set['SMS']):
    for word in sms:
        word_counts_per_sms[word][index] += 1
        
word_counts = pd.DataFrame(word_counts_per_sms)
training_set_clean = pd.concat([training_set, word_counts], axis=1)

# Isolating spam and ham messages first
spam_messages = training_set_clean[training_set_clean['Label'] == 'spam']
ham_messages = training_set_clean[training_set_clean['Label'] == 'ham']
# P(Spam) and P(Ham)
p_spam = len(spam_messages) / len(training_set_clean)
p_ham = len(ham_messages) / len(training_set_clean)
# N_Spam
n_words_per_spam_message = spam_messages['SMS'].apply(len)
n_spam = n_words_per_spam_message.sum()
# N_Ham
n_words_per_ham_message = ham_messages['SMS'].apply(len)
n_ham = n_words_per_ham_message.sum()
# N_Vocabulary
n_vocabulary = len(vocabulary)
# Laplace smoothing
alpha = 1

# Initiate parameters
parameters_spam = {unique_word:0 for unique_word in vocabulary}
parameters_ham = {unique_word:0 for unique_word in vocabulary}
# Calculate parameters
for word in vocabulary:
    n_word_given_spam = spam_messages[word].sum()
    # spam_messages already defined
    p_word_given_spam = (n_word_given_spam + alpha) / (n_spam + alpha*n_vocabulary)
    parameters_spam[word] = p_word_given_spam
    n_word_given_ham = ham_messages[word].sum()
    # ham_messages already defined
    p_word_given_ham = (n_word_given_ham + alpha) / (n_ham + alpha*n_vocabulary)
    parameters_ham[word] = p_word_given_ham
    
def classify(message):
    message = re.sub('\W', ' ', message)
    message = message.lower().split()
    p_spam_given_message = p_spam
    p_ham_given_message = p_ham
    for word in message:
        if word in parameters_spam:
            p_spam_given_message *= parameters_spam[word]
        if word in parameters_ham:
            p_ham_given_message *= parameters_ham[word]
    return p_ham_given_message > p_spam_given_message

mess = """
WorldQuant BRAIN Việt Nam hân hạnh được tổ chức buổi gặp gỡ tháng 12/2023 dành riêng cho các bạn BRAIN consultant onboard trong năm 2023!

Do số lượng chỗ ngồi giới hạn, các bạn hãy nhanh chóng đăng ký ngay nào!
Đăng ký tham dự tại đây
Chương trình sự kiện
Cơ hội gặp gỡ các thành viên khác của cộng đồng BRAIN cũng như các WorldQuant researcher.
Cập nhật thêm nhiều sáng kiến mới
Cơ hội học tập thực tiễn với các phần nội dung được hướng dẫn bởi WorldQuant researcher
Mini-game với cơ hội nhận được các phần quà hấp dẫn

"""

if classify(mess):
    print("Ham")
else:
    print("Spam") 
    
    

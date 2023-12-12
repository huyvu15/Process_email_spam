import pandas as pd
import re

class NaiveBayes:
    def __init__(self, alpha=1):
        self.alpha = alpha
        self.vocabulary = []
        self.parameters_spam = {}
        self.parameters_ham = {}
        self.p_spam = 0
        self.p_ham = 0

    def clean_text(self, text):
        text = re.sub('\W', ' ', text)
        text = text.lower().split()
        return text

    def train(self, training_set):
        # Tạo một từ điển để lưu số lần xuất hiện của mỗi từ trong spam và ham
        word_counts_per_sms = {'spam': {}, 'ham': {}}

        # Tổng số lượng tin nhắn spam và ham
        n_spam = 0
        n_ham = 0

        for index, row in training_set.iterrows():
            label = row['Label']
            message = self.clean_text(row['SMS'])
            if label == 'spam':
                n_spam += 1
            else:
                n_ham += 1

            for word in message:
                if word not in word_counts_per_sms[label]:
                    word_counts_per_sms[label][word] = 1
                else:
                    word_counts_per_sms[label][word] += 1

                if word not in self.vocabulary:
                    self.vocabulary.append(word)

        # Tính xác suất của từng từ cho spam và ham
        self.parameters_spam = {}
        self.parameters_ham = {}

        for word in self.vocabulary:
            if word not in word_counts_per_sms['spam']:
                word_counts_per_sms['spam'][word] = 0
            if word not in word_counts_per_sms['ham']:
                word_counts_per_sms['ham'][word] = 0

            p_word_given_spam = (word_counts_per_sms['spam'][word] + self.alpha) / (n_spam + self.alpha * len(self.vocabulary))
            p_word_given_ham = (word_counts_per_sms['ham'][word] + self.alpha) / (n_ham + self.alpha * len(self.vocabulary))

            self.parameters_spam[word] = p_word_given_spam
            self.parameters_ham[word] = p_word_given_ham

        # Xác suất trước
        self.p_spam = n_spam / len(training_set)
        self.p_ham = n_ham / len(training_set)
    def classify(self, message):
        message = self.clean_text(message)
        p_spam_given_message = self.p_spam
        p_ham_given_message = self.p_ham
        for word in message:
            if word in self.parameters_spam:
                p_spam_given_message *= self.parameters_spam[word]
            if word in self.parameters_ham:
                p_ham_given_message *= self.parameters_ham[word]
        return p_ham_given_message > p_spam_given_message
    
# Sử dụng mô hình
if __name__ == "__main__":
    # Đọc dữ liệu
    sms_spam = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])

    # Randomize the dataset
    data_randomized = sms_spam.sample(frac=1, random_state=1)
    # Calculate index for split
    training_test_index = round(len(data_randomized) * 0.8)
    # Split into training and test sets
    training_set = data_randomized[:training_test_index].reset_index(drop=True)

    # Tạo và huấn luyện mô hình
    spam_classifier = NaiveBayes(alpha=1)
    spam_classifier.train(training_set)

    mess = """
WorldQuant BRAIN Việt Nam hân hạnh được tổ chức buổi gặp gỡ tháng 12/2023 dành riêng cho các bạn BRAIN consultant onboard trong năm 2023!

Do số lượng chỗ ngồi giới hạn, các bạn hãy nhanh chóng đăng ký ngay nào!
Đăng ký tham dự tại đây
Chương trình sự kiện
Cơ hội gặp gỡ các thành viên khác của cộng đồng BRAIN cũng như các WorldQuant researcher.
Cập nhật thêm nhiều sáng kiến mới
Cơ hội học tập thực tiễn với các phần nội dung được hướng dẫn bởi WorldQuant researcher
Mini-game với cơ hội nhận được các phần quà hấp dẫn
Tham quan văn phòng WorldQuant và dùng bữa trưa

 Tại Hà Nội
Ngày & Giờ: Thứ Bảy, ngày 23/12/2023, vào lúc 09:00 sáng – 12:00 trưa
Địa điểm: Văn phòng WorldQuant tại tòa nhà Lotte Tower, Quận Ba Đình

 Tại Thành phố Hồ Chí Minh
Ngày & Giờ: Thứ Bảy ngày 16/12/2023, vào lúc 09:00 sáng – 12:00 trưa
Địa điểm: Văn phòng WorldQuant tại tòa nhà Saigon Centre, Quận 1

Nếu bạn có bất kỳ câu hỏi nào, vui lòng gửi về địa chỉ email: vietnam@worldquantbrain.com

Rất mong sẽ được tiếp đón bạn.

Trân trọng,
WorldQuant BRAIN Việt Nam

 """
 
    mess1 = "10%"

    result = spam_classifier.classify(mess1)
    if result:
        print("Ham")
    else:
        print("Spam")


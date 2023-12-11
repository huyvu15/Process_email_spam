import pandas as pd
sms_spam = pd.read_csv('SMSSpamCollection', sep='\t', header=None, names=['Label', 'SMS'])


# Randomize the dataset
data_randomized = sms_spam.sample(frac=1, random_state=1)
# Calculate index for split
training_test_index = round(len(data_randomized) * 0.8)
# Split into training and test sets
training_set = data_randomized[:training_test_index].reset_index(drop=True)
test_set = data_randomized[training_test_index:].reset_index(drop=True)



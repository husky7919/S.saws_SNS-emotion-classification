import numpy as np
from transformers import BertTokenizer

# from tensorflow.python.ops.gen_array_ops import edit_distance

# from transformers import BertForSequenceClassification
from transformers.models.bert.modeling_bert import BertForSequenceClassification
import torch
from keras.preprocessing.sequence import pad_sequences


class BertModels:
    def __init__(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print("There are %d GPU(s) available." % torch.cuda.device_count())
            print("We will use the GPU:", torch.cuda.get_device_name(0))
        else:
            self.device = torch.device("cpu")
            print("No GPU available, using the CPU instead.")

        output_dir = "C:\Capstone\Caps\Project\BertFine"
        self.model = BertForSequenceClassification.from_pretrained(output_dir)
        self.tokenizer = BertTokenizer.from_pretrained(output_dir)

        # Load a trained model and vocabulary that you have fine-tuned
        # Copy the model to the GPU.
        self.model.to(self.device)

    def convert_input_data(self, sentences):
        # BERT의 토크나이저로 문장을 토큰으로 분리
        tokenized_texts = [self.tokenizer.tokenize(sent) for sent in sentences]

        # 입력 토큰의 최대 시퀀스 길이
        MAX_LEN = 512

        # 토큰을 숫자 인덱스로 변환
        input_ids = [self.tokenizer.convert_tokens_to_ids(
            x) for x in tokenized_texts]

        # 문장을 MAX_LEN 길이에 맞게 자르고, 모자란 부분을 패딩 0으로 채움
        input_ids = pad_sequences(
            input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post"
        )

        # 어텐션 마스크 초기화
        attention_masks = []

        # 어텐션 마스크를 패딩이 아니면 1, 패딩이면 0으로 설정
        # 패딩 부분은 BERT 모델에서 어텐션을 수행하지 않아 속도 향상
        for seq in input_ids:
            seq_mask = [float(i > 0) for i in seq]
            attention_masks.append(seq_mask)

        # 데이터를 파이토치의 텐서로 변환
        inputs = torch.tensor(input_ids)
        masks = torch.tensor(attention_masks)

        return inputs, masks

    # 문장 테스트
    def test_sentences(self, sentences):
        # 평가모드로 변경
        self.model.eval()
        # 문장을 입력 데이터로 변환
        inputs, masks = self.convert_input_data(sentences)
        inputs = inputs.type(torch.LongTensor)
        masks = masks.type(torch.LongTensor)

        # 데이터를 GPU에 넣음
        b_input_ids = inputs.to(self.device)
        b_input_mask = masks.to(self.device)

        # 그래디언트 계산 안함
        with torch.no_grad():
            # Forward 수행
            outputs = self.model(
                b_input_ids, token_type_ids=None, attention_mask=b_input_mask
            )

        # 로스 구함
        logits = outputs[0]

        # CPU로 데이터 이동
        logits = logits.detach().cpu().numpy()

        return logits

    sentiment_dic = {
        0: "anger",
        1: "fear",
        2: "joy",
        3: "love",
        4: "sadness",
        5: "surprise",
    }

    def emotionR(self, sentences):
        logit = self.test_sentences([sentences])
        return np.argmax(logit)

import seaborn as sns
import matplotlib.pyplot as plt
from nltk import word_tokenize
from wordcloud import WordCloud
import collections
import json


class Data_Visualizer:
    def __init__(self, df):
        self.df = df

    @staticmethod
    def generate_wordcloud(df, sentiment, title):
        sns.set(style="white", font_scale=1.2)
        plt.figure(figsize=(20, 20))
        wc = WordCloud(max_words=2000, width=1600, height=800).generate(" ".join(df[df.sentiment == sentiment].review))
        plt.imshow(wc, interpolation='bilinear')
        plt.title(title)
        plt.axis('off')
        plt.show()

    def wordcloud_positive(self):
        self.generate_wordcloud(self.df, 1, "Positive Review Text")

    def wordcloud_negative(self):
        self.generate_wordcloud(self.df, 0, "Negative Review Text")

    def sentiment_distribution(self):
        plt.figure(figsize=(10, 6))
        sns.countplot(x='sentiment', data=self.df, palette='viridis')
        plt.title('Distribution of Positive and Negative Reviews')
        plt.xlabel('Sentiment')
        plt.ylabel('Count')
        plt.xticks(ticks=[0, 1], labels=['Negative', 'Positive'])
        plt.show()

    def unigram_analysis(self, top_n=20):
        all_words = ' '.join(self.df['review']).lower()
        tokens = word_tokenize(all_words)
        unigram_counts = collections.Counter(tokens)
        common_unigrams = unigram_counts.most_common(top_n)

        unigrams, counts = zip(*common_unigrams)
        plt.figure(figsize=(12, 8))
        sns.barplot(x=list(counts), y=list(unigrams), palette='Paired')
        plt.title(f'Top {top_n} Common Words in Reviews')
        plt.xlabel('Frequency')
        plt.ylabel('Unigrams')
        plt.show()
    @staticmethod
    def plot_metrics(model):
        # Read metrics from JSON file
        metrics_file = 'models/bert/metrics.json' if model == 'bert' else 'models/lstm/metrics.json'
        with open(metrics_file, 'r') as f:
            metrics = json.load(f)

        # Create bar plot
        metrics_values = [
            metrics['accuracy'] * 100,
            metrics['precision'] * 100,
            metrics['recall'] * 100,
            metrics['f1_score'] * 100
        ]
        metrics_labels = ['Accuracy', 'Precision', 'Recall', 'F1 Score']

        plt.figure(figsize=(10, 6))
        bars = plt.bar(metrics_labels, metrics_values, color=['#2ecc71', '#3498db', '#e74c3c', '#f1c40f'])

        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.2f}%',
                    ha='center', va='bottom')

        plt.title(f'{"BERT" if model == "bert" else "LSTM"} Model Performance Metrics')
        plt.ylabel('Percentage (%)')
        plt.ylim(0, 100)  # Set y-axis limit to 100%

        plt.show()

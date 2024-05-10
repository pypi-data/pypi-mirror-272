from functools import partial
from typing import List, Optional

from langkit.core.metric import MetricCreator
from langkit.transformer import EmbeddingChoiceArg


class lib:
    class presets:
        @staticmethod
        def all(prompt: bool = True, response: bool = True) -> MetricCreator:
            from langkit.metrics.injections import prompt_injections_metric
            from langkit.metrics.input_output_similarity import prompt_response_input_output_similarity_metric
            from langkit.metrics.pii import prompt_presidio_pii_metric, response_presidio_pii_metric
            from langkit.metrics.regexes.regexes import prompt_regex_metric, response_regex_metric
            from langkit.metrics.sentiment_polarity import prompt_sentiment_polarity, response_sentiment_polarity
            from langkit.metrics.text_statistics import prompt_textstat_metric, response_textstat_metric
            from langkit.metrics.themes.themes import prompt_jailbreak_similarity_metric
            from langkit.metrics.token import prompt_token_metric, response_token_metric

            prompt_metrics = [
                prompt_textstat_metric,
                prompt_token_metric,
                prompt_regex_metric,
                prompt_sentiment_polarity,
                lib.prompt.toxicity(),
                prompt_response_input_output_similarity_metric,
                lib.prompt.similarity.context(),
                prompt_injections_metric,
                prompt_jailbreak_similarity_metric,
                prompt_presidio_pii_metric,
                lib.prompt.topics.medicine(),
            ]

            response_metrics = [
                response_textstat_metric,
                response_token_metric,
                response_regex_metric,
                response_sentiment_polarity,
                lib.response.similarity.refusal(),
                response_presidio_pii_metric,
                lib.response.toxicity(),
                lib.response.similarity.context(),
                lib.response.topics.medicine(),
            ]

            return [
                *(prompt_metrics if prompt else []),
                *(response_metrics if response else []),
            ]

        @staticmethod
        def recommended(prompt: bool = True, response: bool = True) -> MetricCreator:
            """
            These are the recommended set of metrics for the prompt and response. It pulls in the following groups of metrics:

            - prompt.pii.*
            - prompt.stats.token_count
            - prompt.stats.char_count
            - prompt.similarity.injection
            - prompt.similarity.jailbreak

            - response.pii.*
            - response.stats.token_count
            - response.stats.char_count
            - response.stats.flesch_reading_ease
            - response.sentiment.sentiment_score
            - response.toxicity.toxicity_score
            - response.similarity.refusal
            """

            prompt_metrics = [
                lib.prompt.pii,
                lib.prompt.stats.token_count,
                lib.prompt.stats.char_count,
                lib.prompt.similarity.injection,
                lib.prompt.similarity.jailbreak,
            ]

            response_metrics = [
                lib.response.pii,
                lib.response.stats.token_count,
                lib.response.stats.char_count,
                lib.response.stats.flesch_reading_ease,
                lib.response.sentiment.sentiment_score,
                lib.response.toxicity.toxicity_score,
                lib.response.similarity.refusal,
            ]

            return [
                *(prompt_metrics if prompt else []),
                *(response_metrics if response else []),
            ]

    class prompt:
        @staticmethod
        def pii(entities: Optional[List[str]] = None, input_name: str = "prompt") -> MetricCreator:
            """
            Analyze the input for Personally Identifiable Information (PII) using Presidio. This group contains
            various pii metrics that check for email address, phone number, credit card number, etc. The pii metrics
            can't be used individually for performance reasons. If you want to customize the entities to check for
            then use the `entities` parameter.

            :param entities: The list of entities to analyze for. See https://microsoft.github.io/presidio/supported_entities/.
            :return: The MetricCreator
            """
            from langkit.metrics.pii import pii_presidio_metric, prompt_presidio_pii_metric

            if entities:
                return partial(pii_presidio_metric, entities=entities, input_name=input_name)

            return prompt_presidio_pii_metric

        class toxicity:
            def __call__(self) -> MetricCreator:
                return self.toxicity_score()

            @staticmethod
            def toxicity_score(
                onnx: bool = True, onnx_tag: Optional[str] = None, hf_model: Optional[str] = None, hf_model_revision: Optional[str] = None
            ) -> MetricCreator:
                """
                Analyze the input for toxicity. The output of this metric ranges from 0 to 1, where 0 indicates
                non-toxic and 1 indicates toxic.

                :param onnx: Whether to use the ONNX model for toxicity analysis. This is mutually exclusive with model options.
                :param hf_model: The Hugging Face model to use for toxicity analysis. Defaults to martin-ha/toxic-comment-model
                :param hf_model_revision: The revision of the Hugging Face model to use. This default can change between releases so you
                    can specify the revision to lock it to a specific version.
                """
                if onnx:
                    from langkit.metrics.toxicity_onnx import prompt_toxicity_metric

                    return partial(prompt_toxicity_metric, tag=onnx_tag)
                else:
                    from langkit.metrics.toxicity import prompt_toxicity_metric

                    return partial(prompt_toxicity_metric, hf_model=hf_model, hf_model_revision=hf_model_revision)

        class stats:
            def __call__(self) -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_textstat_metric

                return [lib.prompt.stats.token_count, prompt_textstat_metric]

            @staticmethod
            def char_count() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_char_count_metric

                return prompt_char_count_metric

            @staticmethod
            def flesch_reading_ease() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_reading_ease_metric

                return prompt_reading_ease_metric

            @staticmethod
            def grade() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_grade_metric

                return prompt_grade_metric

            @staticmethod
            def syllable_count() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_syllable_count_metric

                return prompt_syllable_count_metric

            @staticmethod
            def lexicon_count() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_lexicon_count_metric

                return prompt_lexicon_count_metric

            @staticmethod
            def sentence_count() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_sentence_count_metric

                return prompt_sentence_count_metric

            @staticmethod
            def letter_count() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_letter_count_metric

                return prompt_letter_count_metric

            @staticmethod
            def difficult_words() -> MetricCreator:
                from langkit.metrics.text_statistics import prompt_difficult_words_metric

                return prompt_difficult_words_metric

            @staticmethod
            def token_count(tiktoken_encoding: Optional[str] = None) -> MetricCreator:
                """
                Analyze the input for the number of tokens. This metric uses the `tiktoken` library to tokenize the input for
                the cl100k_base encoding by default (the encoding for gpt-3.5 and gpt-4).
                """
                from langkit.metrics.token import prompt_token_metric, token_metric

                if tiktoken_encoding:
                    return partial(token_metric, column_name="prompt", encoding=tiktoken_encoding)

                return prompt_token_metric

        class regex:
            def __call__(self) -> MetricCreator:
                from langkit.metrics.regexes.regexes import prompt_regex_metric

                return prompt_regex_metric

            @staticmethod
            def ssn() -> MetricCreator:
                from langkit.metrics.regexes.regexes import prompt_ssn_regex_metric

                return prompt_ssn_regex_metric

            @staticmethod
            def phone_number() -> MetricCreator:
                from langkit.metrics.regexes.regexes import prompt_phone_number_regex_metric

                return prompt_phone_number_regex_metric

            @staticmethod
            def email_address() -> MetricCreator:
                from langkit.metrics.regexes.regexes import prompt_email_address_regex_metric

                return prompt_email_address_regex_metric

            @staticmethod
            def mailing_address() -> MetricCreator:
                from langkit.metrics.regexes.regexes import prompt_mailing_address_regex_metric

                return prompt_mailing_address_regex_metric

            @staticmethod
            def credit_card_number() -> MetricCreator:
                from langkit.metrics.regexes.regexes import prompt_credit_card_number_regex_metric

                return prompt_credit_card_number_regex_metric

            @staticmethod
            def url() -> MetricCreator:
                from langkit.metrics.regexes.regexes import prompt_url_regex_metric

                return prompt_url_regex_metric

        class similarity:
            """
            These metrics are used to compare the response to various examples and use cosine similarity/embedding distances
            to determine the similarity between the response and the examples.
            """

            def __call__(self) -> MetricCreator:
                return [
                    self.injection(),
                    self.jailbreak(),
                ]

            @staticmethod
            def injection(version: Optional[str] = None) -> MetricCreator:
                """
                Analyze the input for injection themes. The injection score is a measure of how similar the input is
                to known injection examples, where 0 indicates no similarity and 1 indicates a high similarity.
                """
                from langkit.metrics.injections import prompt_injections_metric

                if version:
                    return partial(prompt_injections_metric, version=version)

                return partial(prompt_injections_metric)

            @staticmethod
            def jailbreak(embedding: EmbeddingChoiceArg = "default") -> MetricCreator:
                """
                Analyze the input for jailbreak themes. The jailbreak score is a measure of how similar the input is
                to known jailbreak examples, where 0 indicates no similarity and 1 indicates a high similarity.
                """
                from langkit.metrics.themes.themes import prompt_jailbreak_similarity_metric

                return partial(prompt_jailbreak_similarity_metric, embedding=embedding)

            @staticmethod
            def context(embedding: EmbeddingChoiceArg = "default") -> MetricCreator:
                from langkit.metrics.input_context_similarity import input_context_similarity

                return partial(input_context_similarity, embedding=embedding)

        class sentiment:
            def __call__(self) -> MetricCreator:
                return self.sentiment_score()

            @staticmethod
            def sentiment_score() -> MetricCreator:
                """
                Analyze the sentiment of the response. The output of this metric ranges from -1 to 1, where -1
                indicates a negative sentiment and 1 indicates a positive sentiment.
                """
                from langkit.metrics.sentiment_polarity import prompt_sentiment_polarity

                return prompt_sentiment_polarity

        class topics:
            def __init__(
                self,
                topics: List[str],
                hypothesis_template: Optional[str] = None,
                onnx: bool = True,
                hf_model: Optional[str] = None,
                hf_model_revision: Optional[str] = None,
            ):
                self.topics = topics
                self.hypothesis_template = hypothesis_template
                self.onnx = onnx
                self.hf_model = hf_model
                self.hf_model_revision = hf_model_revision

            def __call__(self) -> MetricCreator:
                from langkit.metrics.topic import topic_metric

                return partial(topic_metric, "prompt", self.topics, self.hypothesis_template, use_onnx=self.onnx)

            @staticmethod
            def medicine(onnx: bool = True) -> MetricCreator:
                from langkit.metrics.topic import topic_metric

                return lambda: topic_metric("prompt", ["medicine"], use_onnx=onnx)

    class response:
        @staticmethod
        def pii(entities: Optional[List[str]] = None, input_name: str = "response") -> MetricCreator:
            """
            Analyze the input for Personally Identifiable Information (PII) using Presidio. This group contains
            various pii metrics that check for email address, phone number, credit card number, etc. The pii metrics
            can't be used individually for performance reasons. If you want to customize the entities to check for
            then use the `entities` parameter.

            :param entities: The list of entities to analyze for. See https://microsoft.github.io/presidio/supported_entities/.
            :return: The MetricCreator
            """
            from langkit.metrics.pii import pii_presidio_metric, response_presidio_pii_metric

            if entities:
                return lambda: pii_presidio_metric(entities=entities, input_name=input_name)

            return response_presidio_pii_metric

        class toxicity:
            def __call__(self) -> MetricCreator:
                return self.toxicity_score()

            @staticmethod
            def toxicity_score(
                onnx: bool = True, onnx_tag: Optional[str] = None, hf_model: Optional[str] = None, hf_model_revision: Optional[str] = None
            ) -> MetricCreator:
                """
                Analyze the toxicity of the response. The output of this metric ranges from 0 to 1, where 0
                indicates a non-toxic response and 1 indicates a toxic response.
                """
                if onnx:
                    from langkit.metrics.toxicity_onnx import response_toxicity_metric

                    return partial(response_toxicity_metric, tag=onnx_tag)
                else:
                    from langkit.metrics.toxicity import response_toxicity_metric

                    return partial(response_toxicity_metric, hf_model=hf_model, hf_model_revision=hf_model_revision)

        class stats:
            def __call__(self) -> MetricCreator:
                from langkit.metrics.text_statistics import response_textstat_metric

                return [lib.response.stats.token_count, response_textstat_metric]

            @staticmethod
            def char_count() -> MetricCreator:
                from langkit.metrics.text_statistics import response_char_count_metric

                return response_char_count_metric

            @staticmethod
            def flesch_reading_ease() -> MetricCreator:
                from langkit.metrics.text_statistics import response_reading_ease_metric

                return response_reading_ease_metric

            @staticmethod
            def grade() -> MetricCreator:
                from langkit.metrics.text_statistics import response_grade_metric

                return response_grade_metric

            @staticmethod
            def syllable_count() -> MetricCreator:
                from langkit.metrics.text_statistics import response_syllable_count_metric

                return response_syllable_count_metric

            @staticmethod
            def lexicon_count() -> MetricCreator:
                from langkit.metrics.text_statistics import response_lexicon_count_metric

                return response_lexicon_count_metric

            @staticmethod
            def sentence_count() -> MetricCreator:
                from langkit.metrics.text_statistics import response_sentence_count_metric

                return response_sentence_count_metric

            @staticmethod
            def letter_count() -> MetricCreator:
                from langkit.metrics.text_statistics import response_letter_count_metric

                return response_letter_count_metric

            @staticmethod
            def difficult_words() -> MetricCreator:
                from langkit.metrics.text_statistics import response_difficult_words_metric

                return response_difficult_words_metric

            @staticmethod
            def token_count(tiktoken_encoding: Optional[str] = None) -> MetricCreator:
                """
                Analyze the input for the number of tokens. This metric uses the `tiktoken` library to tokenize the input for
                the cl100k_base encoding by default (the encoding for gpt-3.5 and gpt-4).
                """
                from langkit.metrics.token import response_token_metric, token_metric

                if tiktoken_encoding:
                    return lambda: token_metric(column_name="response", encoding=tiktoken_encoding)

                return response_token_metric

        class regex:
            def __call__(self) -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_regex_metric

                return response_regex_metric

            @staticmethod
            def refusal() -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_refusal_regex_metric

                return response_refusal_regex_metric

            @staticmethod
            def ssn() -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_ssn_regex_metric

                return response_ssn_regex_metric

            @staticmethod
            def phone_number() -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_phone_number_regex_metric

                return response_phone_number_regex_metric

            @staticmethod
            def email_address() -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_email_address_regex_metric

                return response_email_address_regex_metric

            @staticmethod
            def mailing_address() -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_mailing_address_regex_metric

                return response_mailing_address_regex_metric

            @staticmethod
            def credit_card_number() -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_credit_card_number_regex_metric

                return response_credit_card_number_regex_metric

            @staticmethod
            def url() -> MetricCreator:
                from langkit.metrics.regexes.regexes import response_url_regex_metric

                return response_url_regex_metric

        class sentiment:
            def __call__(self) -> MetricCreator:
                return self.sentiment_score()

            @staticmethod
            def sentiment_score() -> MetricCreator:
                """
                Analyze the sentiment of the response. The output of this metric ranges from -1 to 1, where -1
                indicates a negative sentiment and 1 indicates a positive sentiment.
                """
                from langkit.metrics.sentiment_polarity import response_sentiment_polarity

                return response_sentiment_polarity

        class similarity:
            """
            These metrics are used to compare the response to various examples and use cosine similarity/embedding distances
            to determine the similarity between the response and the examples.
            """

            def __call__(self) -> MetricCreator:
                return [
                    self.prompt(),
                    self.refusal(),
                ]

            @staticmethod
            def prompt(embedding: EmbeddingChoiceArg = "default") -> MetricCreator:
                """
                Analyze the similarity between the input and the response. The output of this metric ranges from 0 to 1,
                where 0 indicates no similarity and 1 indicates a high similarity.
                """
                from langkit.metrics.input_output_similarity import prompt_response_input_output_similarity_metric

                return partial(prompt_response_input_output_similarity_metric, embedding=embedding)

            @staticmethod
            def refusal(embedding: EmbeddingChoiceArg = "default", additional_data_path: Optional[str] = None) -> MetricCreator:
                """
                Analyze the response for refusal themes. The refusal score is a measure of how similar the response is
                to known refusal examples, where 0 indicates no similarity and 1 indicates a high similarity.
                """
                from langkit.metrics.themes.themes import response_refusal_similarity_metric

                return partial(response_refusal_similarity_metric, embedding=embedding, additional_data_path=additional_data_path)

            @staticmethod
            def context(embedding: EmbeddingChoiceArg = "default") -> MetricCreator:
                from langkit.metrics.input_context_similarity import input_context_similarity

                return partial(input_context_similarity, embedding=embedding, input_column_name="response")

        class topics:
            def __init__(
                self,
                topics: List[str],
                hypothesis_template: Optional[str] = None,
                onnx: bool = True,
                hf_model: Optional[str] = None,
                hf_model_revision: Optional[str] = None,
            ):
                self.topics = topics
                self.hypothesis_template = hypothesis_template
                self.onnx = onnx
                self.hf_model = hf_model
                self.hf_model_revision = hf_model_revision

            def __call__(self) -> MetricCreator:
                from langkit.metrics.topic import topic_metric

                return partial(topic_metric, "response", self.topics, self.hypothesis_template, use_onnx=self.onnx)

            @staticmethod
            def medicine(onnx: bool = True) -> MetricCreator:
                from langkit.metrics.topic import topic_metric

                return partial(topic_metric, "response", ["medicine"], use_onnx=onnx)

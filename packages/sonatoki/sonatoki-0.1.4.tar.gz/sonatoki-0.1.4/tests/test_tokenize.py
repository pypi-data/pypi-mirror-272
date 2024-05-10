# STL
from typing import List, TypedDict

# PDM
import yaml
import pytest

# LOCAL
from sonatoki.Tokenizers import (
    SentTokenizerRe,
    WordTokenizerRe,
    SentTokenizerTok,
    WordTokenizerTok,
)

try:
    # PDM
    import nltk

    # LOCAL
    from sonatoki.Tokenizers import SentTokenizerNLTK, WordTokenizerNLTK

except ImportError as e:
    nltk = e
    # TODO: warn user


class TokenizerTest(TypedDict):
    name: str
    input: str
    output: List[str]
    should_be_equal: bool
    xfail: bool


def load_params_from_yaml(json_path: str) -> List[TokenizerTest]:
    with open(json_path) as f:
        return yaml.safe_load(f)


def load_tokenizer_tests(json_path: str) -> List[TokenizerTest]:
    tests = load_params_from_yaml(json_path)
    formatted_tests: List[TokenizerTest] = []
    for test in tests:
        formatted_tests.append(
            TokenizerTest(
                xfail=test.get("xfail", False),
                name=test.get("name", ""),
                input=test["input"],
                output=test.get("output", []),
                should_be_equal=test.get("should_be_equal", True),
            )
        )

    return formatted_tests


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_sentences.yml")
)
def test_sentences_re(test: TokenizerTest):
    if isinstance(nltk, ImportError):
        pytest.skip("nltk not installed")
    if test["xfail"]:
        pytest.xfail()

    transformed_re = SentTokenizerRe.tokenize(test["input"])
    transformed_nltk = SentTokenizerNLTK.tokenize(test["input"])
    assert (transformed_re == transformed_nltk) == test["should_be_equal"], test["name"]


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_words.yml")
)
def test_word_tokenize_re(test: TokenizerTest):
    if isinstance(nltk, ImportError):
        pytest.skip("nltk not installed")
    if test["xfail"]:
        pytest.xfail()

    transformed_re = WordTokenizerRe.tokenize(test["input"])
    transformed_nltk = WordTokenizerNLTK.tokenize(test["input"])
    assert (transformed_re == transformed_nltk) == test["should_be_equal"], test["name"]


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_sentences_tok.yml")
)
def test_sentences_tok(test: TokenizerTest):
    if test["xfail"]:
        pytest.xfail()

    transformed_tok = SentTokenizerTok.tokenize(test["input"])
    if test["should_be_equal"]:
        assert transformed_tok == test["output"], test["name"]
    else:
        assert transformed_tok != test["output"], test["name"]


@pytest.mark.parametrize(
    "test", load_tokenizer_tests("tests/tokenize_cases/tokenize_words_tok.yml")
)
def test_word_tokenize_tok(test: TokenizerTest):
    if test["xfail"]:
        pytest.xfail()

    transformed_tok = WordTokenizerTok.tokenize(test["input"])
    if test["should_be_equal"]:
        assert transformed_tok == test["output"], test["name"]
    else:
        assert transformed_tok != test["output"], test["name"]

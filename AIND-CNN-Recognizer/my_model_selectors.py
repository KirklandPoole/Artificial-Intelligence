import math
import statistics
import warnings

import numpy as np
from hmmlearn.hmm import GaussianHMM
from sklearn.model_selection import KFold
from asl_utils import combine_sequences


class ModelSelector(object):
    '''
    base class for model selection (strategy design pattern)
    '''

    def __init__(self, all_word_sequences: dict, all_word_Xlengths: dict, this_word: str,
                 n_constant=3,
                 min_n_components=2, max_n_components=10,
                 random_state=14, verbose=False):
        self.words = all_word_sequences
        self.hwords = all_word_Xlengths
        self.sequences = all_word_sequences[this_word]
        self.X, self.lengths = all_word_Xlengths[this_word]
        self.this_word = this_word
        self.n_constant = n_constant
        self.min_n_components = min_n_components
        self.max_n_components = max_n_components
        self.random_state = random_state
        self.verbose = verbose

    def select(self):
        raise NotImplementedError

    def base_model(self, num_states):
        # with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        # warnings.filterwarnings("ignore", category=RuntimeWarning)
        try:
            hmm_model = GaussianHMM(n_components=num_states, covariance_type="diag", n_iter=1000,
                                    random_state=self.random_state, verbose=False).fit(self.X, self.lengths)
            if self.verbose:
                print("model created for {} with {} states".format(self.this_word, num_states))
            return hmm_model
        except:
            if self.verbose:
                print("failure on {} with {} states".format(self.this_word, num_states))
            return None


class SelectorConstant(ModelSelector):
    """ 
        select the model with value self.n_constant
    """

    def select(self):
        """ select based on n_constant value

        :return: GaussianHMM object
        """
        best_num_components = self.n_constant
        return self.base_model(best_num_components)


class SelectorBIC(ModelSelector):
    """ select the model with the lowest Baysian Information Criterion(BIC) score

    http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
    Bayesian information criteria: BIC = -2 * logL + p * logN
    """


    def select(self):
        """ select the best model for self.this_word based on
        BIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        #
        # Reference:
        #
        # http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
        # calculate using BIC = -2 * logL + p * logN
        #
        # https://discussions.udacity.com/t/issues-when-solving-cv-bic-and-dic/240013
        # https://stats.stackexchange.com/questions/12341/number-of-parameters-in-markov-model
        #
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        try:
            bestBICScoreFound = np.float('inf')
            bic_Model = self.base_model(self.n_constant)
            best_n_components = self.min_n_components
            for n_components in range(self.min_n_components, self.max_n_components + 1):
                model = self.base_model(n_components)
                if model:
                    #
                    # Reference: http://www2.imm.dtu.dk/courses/02433/doc/ch6_slides.pdf
                    # calculate using BIC = -2 * logL + p * logN
                    #
                    logL = model.score(self.X, self.lengths)
                    p_state = model.transmat_.shape[0] * (model.transmat_.shape[1] - 1)
                    p_output = n_components * self.X.shape[1] * 2
                    p = p_state + p_output + (n_components - 1)
                    logN = np.log(self.X.shape[0])
                    calculatedBIC_Score = (-2.0 * logL) + (p * logN)
                    if calculatedBIC_Score < bestBICScoreFound:
                        bestBICScoreFound = calculatedBIC_Score
                        best_n_components = n_components

            return self.base_model(best_n_components)

        except Exception as e:
            return self.base_model(self.n_constant)



class SelectorDIC(ModelSelector):
    """ select best model based on Discriminative Information Criterion

    Biem, Alain. "A model selection criterion for classification: Application to hmm topology optimization."
    Document Analysis and Recognition, 2003. Proceedings. Seventh International Conference on. IEEE, 2003.
    http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
    DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
    """

    def select(self):
        """ select the best model for self.this_word based on
        DIC score for n between self.min_n_components and self.max_n_components

        :return: GaussianHMM object
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        #
        # Reference: http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.58.6208&rep=rep1&type=pdf
        # DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
        #

        try:
            bestDICScoreFound = np.float('-inf')
            best_n_components = self.min_n_components
            for n_components in range(self.min_n_components, self.max_n_components + 1):
                model = self.base_model(n_components)
                if model:
                    #
                    # calculate DIC = log(P(X(i)) - 1/(M-1)SUM(log(P(X(all but i))
                    #
                    logPx = model.score(self.X, self.lengths)
                    words_Average  = 0
                    number_of_words = 0
                    for word in self.words:
                        if word == self.this_word: continue
                        other_word_X, word_lengths = self.hwords[word]
                        words_Average = words_Average + model.score(other_word_X, word_lengths)
                        number_of_words = number_of_words + 1
                        words_Average = words_Average+ number_of_words

                    dic = logPx - words_Average
                    if dic >= bestDICScoreFound:
                        bestDICScoreFound = dic
                        best_n_components = n_components

            return self.base_model(best_n_components)

        except Exception as e:
            return self.base_model(self.n_constant)

class SelectorCV(ModelSelector):
    ''' select best model based on average log Likelihood of cross-validation folds

    '''
    #
    # Reference: https://en.wikipedia.org/wiki/Cross-validation_(statistics)
    #
    def select(self):
        """
            select the best model based on CV score.
        """
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        try:
            cv_model = self.base_model(self.n_constant)
            if len(self.sequences) == 1:
                return cv_model

            bestCVScoreFound = np.float('-inf')
            best_n_components = self.min_n_components

            numberOfSplits = 3 if len(self.sequences) >= 3 else len(self.sequences)
            split_method = KFold(numberOfSplits)

            for n_components in range(self.min_n_components, self.max_n_components + 1):
                averageLogL = 0
                for train_idx, test_idx in split_method.split(self.sequences):
                    train_X, train_lengths = combine_sequences(train_idx, self.sequences)
                    test_X, test_lengths = combine_sequences(test_idx, self.sequences)

                    model = GaussianHMM(n_components=n_components, covariance_type="diag", n_iter=1000,
                                            random_state=self.random_state, verbose=False).fit(train_X,
                                                                                               train_lengths)
                    testLogL = model.score(test_X, test_lengths)
                    averageLogL = averageLogL + testLogL

                averageLogL = averageLogL / numberOfSplits

                if averageLogL >= bestCVScoreFound:
                    bestCVScoreFound = averageLogL
                    best_n_components = n_components

            cv_Model = GaussianHMM(n_components=best_n_components, covariance_type="diag", n_iter=1000,
                         random_state=self.random_state, verbose=False).fit(self.X, self.lengths)

            return cv_Model

        except Exception as e:
            return self.base_model(self.n_constant)
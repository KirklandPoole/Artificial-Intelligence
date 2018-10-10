import warnings
from asl_data import SinglesData


def recognize(models: dict, test_set: SinglesData):
    """ Recognize test word sequences from word models set

   :param models: dict of trained models
       {'SOMEWORD': GaussianHMM model object, 'SOMEOTHERWORD': GaussianHMM model object, ...}
   :param test_set: SinglesData object
   :return: (list, list)  as probabilities, guesses
       both lists are ordered by the test set word_id
       probabilities is a list of dictionaries where each key a word and value is Log Liklihood
           [{SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            {SOMEWORD': LogLvalue, 'SOMEOTHERWORD' LogLvalue, ... },
            ]
       guesses is a list of the best guess words ordered by the test set word_id
           ['WORDGUESS0', 'WORDGUESS1', 'WORDGUESS2',...]
   """
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # Initialize variables for list of probabilities, list of guesses, probability dictionary, best guess found and best score found
    probabilities_list = []
    guesses_list = []
    probability_dict = {}
    best_guess_found = ""
    best_score_found = float("-inf")
    #
    # Reference: https://discussions.udacity.com/t/recognizer-implementation/234793/6
    # for word, model in models.items():
    #            calculate the scores for each model(word) and update the 'probabilities' list.
    #            determine the maximum score for each model(word).
    #            Append the corresponding word (the tested word is deemed to be the word for which with the model was trained) to the list 'guesses

    # Outer Loop
    for testing_set_word, (X, lengths) in test_set.get_all_Xlengths().items():
        best_score_found = float("-inf")
        best_guess_found = ""
        probability_dict = {}
        # Inner Loop - Loop through models.items()
        for current_word_from_trained_model, models_item in models.items():
            try:
                model_score = models_item.score(X, lengths)
                probability_dict[current_word_from_trained_model] = model_score
            except:
                probability_dict[current_word_from_trained_model] = float("-inf")
            # Is this be best score found?
            if model_score > best_score_found:
                # set best score and best guess
                best_score_found = model_score
                best_guess_found = current_word_from_trained_model

        probabilities_list.append(probability_dict)
        guesses_list.append(best_guess_found)

    return probabilities_list, guesses_list
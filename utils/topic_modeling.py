def topic_render(topic, number_of_words_per_topic, vocabArray):  # specify vector id of words to actual words
    terms = topic[0]
    prob = topic[1]
    
    result = []
    for i in range(number_of_words_per_topic):
        term = str(round(prob[i],3))+"  "+vocabArray[terms[i]]
        result.append(term)
    return result
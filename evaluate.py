class fpl_evaluate:
    def __init__(self):
        pass
    
    def score_model(self, predictions, labels):
        # Calculate error
        error = 0
        square_error = 0
        accuracy = 0
        for i in range(len(predictions)):
            error += abs(predictions[i] - labels[i])
            square_error += (predictions[i] - labels[i]) ** 2
            if round(predictions[i]) == labels[i]:
                accuracy += 1
        error /= len(predictions)
        square_error /= len(predictions)
        accuracy /= len(predictions)

        return error, square_error, accuracy
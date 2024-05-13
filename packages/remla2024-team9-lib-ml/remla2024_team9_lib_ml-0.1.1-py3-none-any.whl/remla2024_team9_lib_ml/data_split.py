def load_and_split_data(data):
    """
    Takes raw data, splits into features and labels, and returns them.
    """

    # Split into features and labels
    features = [line.split("\t")[1].strip() for line in data]
    labels = [line.split("\t")[0].strip() for line in data]

    return features, labels

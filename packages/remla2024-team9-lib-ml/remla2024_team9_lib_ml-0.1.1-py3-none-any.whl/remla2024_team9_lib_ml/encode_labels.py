from sklearn.preprocessing import LabelEncoder

def encode_labels(train_labels, val_labels, test_labels):
    """
    Encodes labels using sklearn LabelEncoder and returns numpy arrays of encoded labels.
    """

    encoder = LabelEncoder()

    # Transform labels
    train_labels_encoded = encoder.fit_transform([label.strip() for label in train_labels])
    val_labels_encoded = encoder.transform([label.strip() for label in val_labels])
    test_labels_encoded = encoder.transform([label.strip() for label in test_labels])

    return train_labels_encoded, val_labels_encoded, test_labels_encoded

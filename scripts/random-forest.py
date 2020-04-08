import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split


def main():
    dataset = pd.read_csv('../data/crimes_dataset_processed.csv')
    x = dataset.iloc[:, [i for i in range(8) if i != 6]].values
    y = dataset.iloc[:, 6].values

    # Get training and test sets
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # Train the model
    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(x_train, y_train)

    # Predict the class for the test set
    y_pred = classifier.predict(x_test)

    print(confusion_matrix(y_test, y_pred))
    print(classification_report(y_test, y_pred))
    print(accuracy_score(y_test, y_pred))


if __name__ == '__main__':
    main()
